# -*- coding: utf-8 -*-

"""The functional object of the validation in algorithm."""

# __author__ = "Yuan Chang"
# __copyright__ = "Copyright (C) 2016-2018"
# __license__ = "AGPL"
# __email__ = "pyslvs@gmail.com"

from tinycadlib import (
    PLAP,
    PLLP,
    legal_crank,
    legal_triangle,
    Coordinate
)
import numpy as np
cimport numpy as np

#Large fitness
cdef double FAILURE = 9487945

cdef str strbetween(str s, str front, str back):
    return s[s.find(front)+1:s.find(back)]

cdef str strbefore(str s, str front):
    return s[:s.find(front)]

cdef list path_error(list path, tuple target):
    """A list of each error value."""
    cdef list tmp_list = []
    cdef int i
    for i in range(len(path)):
        tmp_list.append(path[i].distance(target[i]))
    return tmp_list

cdef class build_planar:
    
    """This class used to verified kinematics of the linkage mechanism."""
    
    cdef int POINTS, VARS
    cdef list constraint, Link, driver_list, follower_list
    cdef tuple targetPoint
    cdef dict Driver, Follower
    cdef np.ndarray exprs, target, upper, lower
    
    def __cinit__(self, dict mech_params):
        '''
        mech_params = {
            'Target',
            'Driver',
            'Follower',
            'Target',
            'constraint',
            'Expression',
            'IMax', 'LMax', 'FMax', 'AMax',
            'IMin', 'LMin', 'FMin', 'AMin'
        }
        '''
        cdef object value
        cdef int l
        cdef object check_tuple = tuple(len(value) for value in mech_params['Target'].values())
        if not all([l==check_tuple[0] for l in check_tuple]):
            raise ValueError("Target path should be in the same size.")
        #counting how many action to satisfied require point
        self.POINTS = check_tuple[0]
        #driving point, string
        self.Driver = mech_params['Driver']
        #folower point, string
        self.Follower = mech_params['Follower']
        #target point name
        #[Coordinate(x0, y0), Coordinate(x1, y1), Coordinate(x2, y2), ...]
        cdef double x, y
        self.targetPoint = tuple(mech_params['Target'])
        self.target = np.ndarray((len(mech_params['Target']),), dtype=np.object)
        cdef int i
        for i, value in enumerate(mech_params['Target'].values()):
            self.target[i] = tuple(Coordinate(x, y) for x, y in value)
        
        #constraint
        self.constraint = mech_params['constraint']
        
        """
        Expression
        
        ['A', 'B', 'C', 'D', 'E', 'L0', 'L1', 'L2', 'L3', 'L4', 'a0']
        """
        cdef object ExpressionL = mech_params['Expression'].split(';')
        
        '''
        Link: L0, L1, L2, L3, ...
        driver_list: The name of the point in "self.Driver" (Sorted).
        follower_list: The name of the point in "self.Follower" (Sorted).
        exprs:
            {'relate': 'PLAP', 'target': 'B', 'params': ['A', 'L0', 'a0', 'D']},
            {'relate': 'PLLP', 'target': 'C', 'params': ['B', 'L1', 'L2', 'D']}, ...
        Expression: PLAP[A,L0,a0,D](B);PLLP[B,L1,L2,D](C);PLLP[B,L3,L4,C](E)
        '''
        cdef str expr, params
        self.Link = []
        self.driver_list = []
        self.follower_list = []
        self.exprs = np.ndarray((len(ExpressionL),), dtype=np.object)
        for i, expr in enumerate(ExpressionL):
            params = strbetween(expr, '[', ']')
            self.exprs[i] = (
                #[0]: relate
                strbefore(expr, '['),
                #[1]: target
                strbetween(expr, '(', ')'),
                #[2]: params
                params.split(',')
            )
            for p in params.split(','):
                if ('L' in p) and ('L' != p):
                    self.Link.append(p)
                if (p in self.Driver) and (p not in self.driver_list):
                    self.driver_list.append(p)
                if (p in self.Follower) and (p not in self.follower_list):
                    self.follower_list.append(p)
        #The number of all variables (except angles).
        self.VARS = 2*len(self.driver_list) + 2*len(self.follower_list) + len(self.Link)
        
        """Limitations.
        
        The data will as same as a chromosome.
        [I, L, F, L, L, ..., A0, A0, ..., A1, A1, ...]
        self.VARS = length before matching angles.
        """
        
        cdef str name
        
        #upper
        cdef object tmp_upper = []
        for name in self.driver_list:
            for i in [0, 1]:
                tmp_upper.append(self.Driver[name][i] + self.Driver[name][2]/2)
        for name in self.follower_list:
            for i in [0, 1]:
                tmp_upper.append(self.Follower[name][i] + self.Follower[name][2]/2)
        for name in ['IMax', 'LMax', 'FMax'] + ['LMax']*(len(self.Link)-3):
            tmp_upper.append(mech_params[name])
        tmp_upper += [mech_params['AMax']]*len(self.driver_list)*self.POINTS
        self.upper = np.array(tmp_upper, dtype=np.float32)
        
        #lower
        cdef object tmp_lower = []
        for name in self.driver_list:
            for i in [0, 1]:
                tmp_lower.append(self.Driver[name][i] - self.Driver[name][2]/2)
        for name in self.follower_list:
            for i in [0, 1]:
                tmp_lower.append(self.Follower[name][i] - self.Follower[name][2]/2)
        for name in ['IMin', 'LMin', 'FMin'] + ['LMin']*(len(self.Link)-3):
            tmp_lower.append(mech_params[name])
        tmp_lower += [mech_params['AMin']]*len(self.driver_list)*self.POINTS
        self.lower = np.array(tmp_lower, dtype=np.float32)
    
    cpdef np.ndarray get_upper(self):
        return self.upper
    
    cpdef np.ndarray get_lower(self):
        return self.lower
    
    cpdef int get_nParm(self):
        """Return size of chromosome."""
        return len(self.upper)
    
    cdef inline dict get_data_dict(self, np.ndarray v):
        """Create and return data dict."""
        cdef str name, L
        cdef dict tmp_dict = {}
        cdef int vi = 0
        #driving
        for name in self.driver_list:
            tmp_dict[name] = Coordinate(v[vi], v[vi+1])
            vi += 2
        #follower
        for name in self.follower_list:
            tmp_dict[name] = Coordinate(v[vi], v[vi+1])
            vi += 2
        #links
        for L in self.Link:
            tmp_dict[L] = v[vi]
            vi += 1
        return tmp_dict
    
    cdef inline np.ndarray get_path_array(self):
        """Create and return path array."""
        cdef np.ndarray path = np.ndarray((len(self.targetPoint),), dtype=np.object)
        cdef int i
        for i in range(len(self.targetPoint)):
            path[i] = []
        return path
    
    cdef object from_formula(self, object expression_dict, object data_dict):
        """Formulas using PLAP and PLLP."""
        cdef str fun = expression_dict[0]
        cdef object params = tuple(data_dict[p] for p in expression_dict[2])
        if fun=='PLAP':
            return Coordinate(*PLAP(*params))
        if fun=='PLLP':
            return Coordinate(*PLLP(*params))
    
    cdef double run(self, np.ndarray v):
        """
        v:
        [Ax, Ay, Dx, Dy, ..., L0, L1, ..., A00, A01, ..., A10, A11, ...]
        
        target: a list of target. [(1,5), (2,5), (3,5)]
        
        POINTS: length of target.
        
        VARS: mechanism variables count.
        """
        # all variable
        cdef object test_dict = self.get_data_dict(v)
        cdef np.ndarray path = self.get_path_array()
        # calculate the target point, and sum all error.
        #My fitness
        cdef double fitness = 0
        cdef int i, j, k
        cdef str name
        cdef object e, target_coordinate
        for i in range(self.POINTS):
            #a0: random angle to generate target point.
            #match to path points.
            for j in range(len(self.driver_list)):
                test_dict['a{}'.format(j)] = np.deg2rad(v[self.VARS + i*len(self.driver_list) + j])
            for e in self.exprs:
                #PLLP(test_dict['B'], test_dict['L1'], test_dict['L2'], test_dict['D'])
                target_coordinate = self.from_formula(e, test_dict)
                if target_coordinate.isnan():
                    return FAILURE
                #target
                test_dict[e[1]] = target_coordinate
            for i, name in enumerate(self.targetPoint):
                path[i].append(test_dict[name])
        #constraint
        for constraint in self.constraint:
            if not legal_crank(*[test_dict[name] for name in constraint]):
                return FAILURE
        #swap
        cdef list errors
        for k in range(len(self.targetPoint)):
            errors = path_error(path[k], self.target[k])
            path[k] = [e for _, e in sorted(zip(errors, path[k]))]
            fitness += sum(path_error(path[k], self.target[k]))
        return fitness
    
    cpdef object get_coordinates(self, np.ndarray v):
        """Return the last answer."""
        cdef str k
        cdef object e, value
        cdef dict final_dict = self.get_data_dict(v)
        for j in range(len(self.driver_list)):
            final_dict['a{}'.format(j)] = np.deg2rad(v[self.VARS + j])
        for e in self.exprs:
            #target
            final_dict[e[1]] = self.from_formula(e, final_dict)
        for k, value in final_dict.items():
            if type(value) == Coordinate:
                final_dict[k] = (value.x, value.y)
        cdef list tmp_list
        for j in range(len(self.driver_list)):
            tmp_list = []
            for i in range(self.POINTS):
                tmp_list.append(v[self.VARS + i*len(self.driver_list) + j])
            final_dict['a{}'.format(j)] = tuple(tmp_list)
        return final_dict
    
    def __call__(self, np.ndarray v):
        """Python callable object."""
        return self.run(v)
