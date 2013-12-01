'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

import threading
from threading import Semaphore
import time
from PCB import *


class Kernel():
    
    def __init__(self,scheduler, hd, memory, plp):
        self.pcbTable = []
        #self.esperando = []
        self.scheduler = scheduler
        self.cont = 0
        self.disco = hd
        self.memory = memory
        self.semaphore = Semaphore(1)
        self.plp = plp
        

    def kill(self, pcb):
        self.pcbTable.remove(pcb)
        self.memory.delete(pcb)
        print("se elimino el PCB " + str(pcb.pid)+"\n")
        self.plp.enviarLosEsperando()
        
    def addProcess(self, programa):
        pcb = PCB(self.getPId(), programa.getCantInst(), programa.nombre)
        print("se creo el PCB" +str(pcb.pid))
        self.pcbTable.append(pcb)
        self.plp.loadMemory(programa,pcb) 
           
    def pcbEstaEnLaTablaDeProcesos(self,pcb):
        return self.pcbTable.__contains__(pcb)

    def agregarAlScheduler(self, pcb):
        #if not self.scheluder.isEmpty(): 
        if not pcb.termino():
            self.scheduler.addReady(pcb)
        elif self.pcbEstaEnLaTablaDeProcesos(pcb): # si todavia no lo borro lo borra. es que cuando la cpu envia un instruccion
                                                #de IO incrementa pc pero no controla si termino o no, solo controla cuando es una 
                                                #instruccion de cpu
            
            self.kill(pcb)

    def getPId(self):
        self.semaphore.acquire()
        self.cont = self.cont + 1
        self.semaphore.release()
        return self.cont
        
    def schedulerNext(self):
        self.scheduler.runCpu() 

    def run(self, nomPrograma):
        programa = self.disco.getPrograma(nomPrograma)
    #se carga en memoria   
        self.addProcess(programa)
        
