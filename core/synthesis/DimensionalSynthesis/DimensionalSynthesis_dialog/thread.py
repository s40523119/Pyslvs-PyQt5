# -*- coding: utf-8 -*-

"""Thread of dimensional synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import timeit
import platform
import numpy
import numpy.distutils.cpuinfo
from psutil import virtual_memory
from typing import (
    Tuple,
    Dict,
    Any,
)
from core.QtModules import (
    QThread,
    pyqtSignal,
    QMutex,
    QMutexLocker,
)
from core.libs import (
    Genetic,
    Firefly,
    DiffertialEvolution,
)
from core.libs import build_planar
from .options import AlgorithmType


class WorkerThread(QThread):
    
    """The QThread class to handle algorithm."""
    
    progress_update = pyqtSignal(int, str)
    result = pyqtSignal(dict, float)
    done = pyqtSignal()
    
    def __init__(self,
        type_num: AlgorithmType,
        mech_params: Dict[str, Any],
        settings: Dict[str, Any]
    ):
        super(WorkerThread, self).__init__(None)
        self.stoped = False
        self.mutex = QMutex()
        self.type_num = type_num
        self.mech_params = mech_params
        self.settings = settings
        self.loop = 1
    
    def setLoop(self, loop):
        """Set the loop times."""
        self.loop = loop
    
    def run(self):
        """Start the algorithm loop."""
        with QMutexLocker(self.mutex):
            self.stoped = False
        for name, path in self.mech_params['Target'].items():
            print("- [{}]: {}".format(name, tuple(
                (round(x, 2), round(y, 2))
                for x, y in path
            )))
        mechanismObj = build_planar(self.mech_params)
        if self.type_num == AlgorithmType.RGA:
            foo = Genetic
        elif self.type_num == AlgorithmType.Firefly:
            foo = Firefly
        elif self.type_num == AlgorithmType.DE:
            foo = DiffertialEvolution
        self.fun = foo(
            mechanismObj,
            self.settings,
            progress_fun=self.progress_update.emit,
            interrupt_fun=self.__isStoped,
        )
        T0 = timeit.default_timer()
        self.currentLoop = 0
        for self.currentLoop in range(self.loop):
            print("Algorithm [{}]: {}".format(
                self.currentLoop + 1,
                self.type_num
            ))
            if self.stoped:
                #Cancel the remaining tasks.
                print("Canceled.")
                continue
            mechanism, time_spand = self.__algorithm()
            self.result.emit(mechanism, time_spand)
        T1 = timeit.default_timer()
        totalTime = round(T1-T0, 2)
        print("total cost time: {} [s]".format(totalTime))
        self.done.emit()
    
    def __algorithm(self) -> Tuple[Dict[str, Any], float]:
        """Get the algorithm result."""
        t0 = timeit.default_timer()
        fitnessParameter, time_and_fitness = self.__generateProcess()
        t1 = timeit.default_timer()
        time_spand = round(t1 - t0, 2)
        cpu = numpy.distutils.cpuinfo.cpu.info[0]
        lastGen = time_and_fitness[-1][0]
        mechanism = {
            'time': time_spand,
            'lastGen': lastGen,
            'interrupted': str(lastGen) if self.stoped else 'False',
            'settings': self.settings,
            'hardwareInfo': {
                'os': "{} {} {}".format(
                    platform.system(),
                    platform.release(),
                    platform.machine()
                ),
                'memory': "{} GB".format(
                    round(virtual_memory().total / (1024. ** 3), 4)
                ),
                'cpu': cpu.get("model name", cpu.get('ProcessorNameString', ''))
            },
            'TimeAndFitness': time_and_fitness
        }
        mechanism['Algorithm'] = self.type_num.value
        mechanism.update(self.mech_params)
        mechanism.update(fitnessParameter)
        print("cost time: {} [s]".format(time_spand))
        return mechanism, time_spand
    
    def __generateProcess(self):
        """Execute algorithm and sort out the result."""
        fitnessParameter, time_and_fitness = self.fun.run()
        return(fitnessParameter, time_and_fitness)
    
    def __isStoped(self) -> bool:
        """Return stop status for Cython function."""
        return self.stoped
    
    def stop(self):
        """Stop the algorithm."""
        with QMutexLocker(self.mutex):
            self.stoped = True
