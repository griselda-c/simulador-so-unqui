'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

import threading
from threading import Semaphore
import time
from miFifo import *
from IRQExitIO import *


class IO(threading.Thread):
    def __init__(self,irqManager):
        threading.Thread.__init__(self)
        self.cola = miFifo()
        self.irqManager = irqManager

    def addInstruccion(self,tupla):
        print("una instruccion fue agregada a IO\n")
        self.cola.addElement(tupla)
        
    def existInstruction(self):
        return self.cola.size() > 0


    def run(self):
        while True:
            if self.existInstruction():
                tupla = self.cola.getElement()
                instruction = tupla[0]
                print(instruction.message)
                #lanza un alerta irqExistIO para avisar al kernel que el pcb ya salio de IO
                irqExistIo = IRQExitIO()
                self.irqManager.handle(irqExistIo, tupla[1])
