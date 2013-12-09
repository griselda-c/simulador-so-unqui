'''
Created on 19/11/2013

@author: Griselda Maricruz
'''
from miFifo import *

class PLP:
    def __init__(self, scheduler, memoria, disco):
        self.memory = memoria
        self.esperando = miFifo()
        self.scheduler = scheduler
        self.disco = disco
               
    def agregarPcbAEsperando(self,pcb):
        self.esperando.addElement(pcb)
        
        
    def enviarLosEsperando(self):
        for i in range(0,self.esperando.size()):
            pcb = self.esperando.getElement()
            programa = self.disco.getPrograma(pcb.nomPrograma)
            self.loadMemory(programa, pcb)
            
    def loadMemory(self,programa, pcb):
        if self.memory.hayLugar(pcb.cantInst):
            self.memory.load(programa,pcb)
            self.agregarAlScheduler(pcb)
        else:
            self.esperando.addElement(pcb) #no hay lugar entonces se guarda en la lista de esperando
            print("PCB "+str(pcb.pid)+"----------------> esta esperando por memoria ")
            
            
    def agregarAlScheduler(self, pcb):
        self.scheduler.addReady(pcb)
