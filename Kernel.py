'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

import threading
from threading import Semaphore
import time
from PCB import *


class Kernel():
    
    def __init__(self,scheduler, hd, memory):
        self.pcbTable = []
        self.scheduler = scheduler
        self.cont = 0
        self.disco = hd
        self.memory = memory
        self.semaphore = Semaphore(1)

    def kill(self, pcb):
        self.pcbTable.remove(pcb)
        self.memory.delete(pcb)
        print("se elimino el pcb con id " + str(pcb.pid)+"\n")
        
    def loadMemory(self,programa, pcb):
		return self.memory.load(programa, pcb)
		
    def compactacionMemoria(self):
		self.memory.compactacion()

    def addProcess(self, programa):
        pcb = PCB(self.getPId(), programa.getCantInst())
        print("se creo el pcb con id " +str(pcb.pid))
        self.cargadoMemoria = self.loadMemory(programa,pcb) 
        if self.cargadoMemoria:  
			self.pcbTable.append(pcb)
			self.agregarAlScheduler(pcb)
        else:
			self.compactacionMemoria()

    def agregarAlScheduler(self, pcb):
        #if not self.scheluder.isEmpty():  
        self.scheduler.addReady(pcb)

    def getPId(self):
        self.semaphore.acquire()
        self.cont = self.cont + 1
        self.semaphore.release()
        return self.cont
        
    def schedulerNext(self):
        self.scheduler.runCpu()

    def run(self, nomPrograma):
        #programa = self.disco.getPrograma(nomPrograma)
    #se carga en memoria   
        self.addProcess(nomPrograma)
		
