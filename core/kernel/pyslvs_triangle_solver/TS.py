# -*- coding: utf-8 -*-
from math import *

##Directions:
##[{'p1':Point1, 'p2':Point2, 'len1':Line1, ('len2':Line2, 'angle':angle)}, ...]

class solver():
    def __init__(self, Directions=list()):
        #Cosine Theorem
        self.CosineTheoremAngle = lambda a, b, c: acos(float(b**2+c**2-a**2)/(float(2*b*c) if float(2*b*c)!=0 else 0.001))
        self.Directions = Directions
    
    def set(self, Directions): self.Directions = Directions
    
    def answer(self):
        answer = self.Iterator() if self.Parser() else list()
        self.Directions.clear()
        return answer
    
    def Parser(self):
        for e in self.Directions:
            pos = self.Directions.index(e)
            if e.get('p1', False) is False: return False
            if e.get('p2', False) is False: return False
            if e.get('len1', False) is False: return False
            if e.get('len2', False) is False and e.get('angle', False) is False and e.get('p3', False) is False: return False
            if not(e.get('angle', False) is False): self.Directions[pos]['Type'] = 'PLAP'
            elif not(e.get('len2', False) is False): self.Directions[pos]['Type'] = 'PLLP'
            elif not(e.get('p3', False) is False): self.Directions[pos]['Type'] = 'PLPP'
        return bool(self.Directions)
    
    def Iterator(self):
        results = list()
        for e in self.Directions:
            p1 = results[e['p1']] if type(e['p1'])==int else e['p1']
            p2 = results[e['p2']] if type(e['p2'])==int else e['p2']
            #Direction of the point
            other = e.get('other', False)
            ##True: angle1-angle2
            ##False: angle1+angle2
            if e['Type']=='PLAP': results.append(self.PLAP(p1, e['len1'], e['angle'], p2, other))
            elif e['Type']=='PLLP': results.append(self.PLLP(p1, e['len1'], e['len2'], p2, other))
            elif e['Type']=='PLPP': results.append(self.PLPP(p1, e['len1'], e['p3'], p2, other))
        return results
    
    def PLAP(self, p1, line1, angle, p2, other=False):
        x1 = p1[0] #p1 start point
        y1 = p1[1]
        len1 = float(line1)
        angle2 = radians(float(angle))
        angle1 = self.m(p1, p2)
        if other:
            cx = x1+len1*cos(angle1-angle2)
            cy = y1+len1*sin(angle1-angle2)
        else:
            cx = x1+len1*cos(angle1+angle2)
            cy = y1+len1*sin(angle1+angle2)
        return cx, cy
    
    def PLLP(self, p1, line1, line2, p2, other=False):
        x1 = p1[0] #p1 start point
        y1 = p1[1]
        x2 = p2[0] #p2 start point2
        y2 = p2[1]
        len1 = float(line1)
        len2 = float(line2)
        d = sqrt((x1-x2)**2+(y2-y1)**2)
        angle1 = self.m(p1, p2)
        angle2 = self.CosineTheoremAngle(len2, d, len1)
        if other:
            cx = x1+len1*cos(angle1-angle2)
            cy = y1+len1*sin(angle1-angle2)
        else:
            cx = x1+len1*cos(angle1+angle2)
            cy = y1+len1*sin(angle1+angle2)
        return cx, cy
    
    def PLPP(self, p1, line1, p2, p3, other=False):
        x1 = p1[0] #p1 start point
        y1 = p1[1]
        x2 = p2[0] #p2 slider start point
        y2 = p2[1]
        x3 = p3[0] #p3 slider end point
        y3 = p3[1]
        len1 = float(line1) #len1 slider link
        if other:
            ex = ((x2-x3)*(x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (-y2 + y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2)) - (x2*y3 - y2*x3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))/((y2 - y3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))
            ey = (x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (-y2 + y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2))/(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)
        else:
            ex = ((x2-x3)*(x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (y2 - y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2)) - (x2*y3 - y2*x3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))/((y2 - y3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))
            ey = (x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (y2 - y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2))/(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)
        return ex, ey
    
    def m(self, p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        x = x2-x1
        y = y2-y1
        d = sqrt(x**2+y**2)
        return self.CosineTheoremAngle(y, x, d)*(-1 if y<0 else 1)

if __name__=='__main__':
    #Test
    s = solver([
        {'p1':(-60, 0), 'p2':(0, 0), 'len1':30, 'angle':50}, #C
        {'p1':0, 'p2':(0, 0), 'len1':50, 'len2':60}, #D
        {'p1':0, 'p2':1, 'len1':50, 'len2':50}, #E
        {'p1':(-45, 0), 'p2':(0, 12), 'len1':30, 'angle':55},
        {'p1':3, 'len1':40, 'p2':(0, 12), 'p3':(10, 30)}, #Slider E
        ])
    answer = s.answer()
    print("C={}\nD={}\nE={}\n\nSlider B={}\nSlider E={}".format(*answer))
    
    ##C= (-40.716371709403816, 22.98133329356934)
    ##D= (-6.698073034033397, 59.62495968661744)
    ##E= (-55.44153371488418, 70.76385733649067)
    
    ##Silder B=(-34.705658808271956, 28.17847652780915)
    ##Silder E=(4.452256484254149, 20.01406167165747)
