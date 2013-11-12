'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

import threading
from threading import Semaphore
import time
from Disco import *
from CPU import *
from IRQNEW import *

class Timer(threading.Thread):
    def __init__(self, cpu,irqManager): 
        threading.Thread.__init__(self)
        self.cpu = cpu
        self.irqManager = irqManager
        
    def evaluar(self):
        instruction = self.cpu.fetch()
        if instruction != None:
            instruction.execute(self.cpu) #ejecuta la instruccion
        else:
            # no hay pcb asignado por eso se llama irqNew
            irqNew = IRQNEW()
            self.irqManager.handle(irqNew, None)
            
        time.sleep(5)

    def run(self):
        while True:
            self.evaluar()
