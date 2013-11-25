'''
Created on 24/11/2013

@author: Griselda
'''
import threading
from threading import Semaphore
import time
from miFifo import *

class RoundRobin(threading.Thread):
    def __init__(self,cpu):
        threading.Thread.__init__(self)
        self.semaphore = Semaphore(1)
        self.ready = miFifo() #fifo
        self.cpu = cpu
    
    def addReady(self, pcb): 
        if not pcb.termino(): # si termino se cpu envia IRQ al manager, pero roundRobin no tiene forma de saberlo por eso esta condicion
            self.ready.addElement(pcb)
            print("el PCB " +str(pcb.pid) +" esta en el scheduler Round Robin con PC---->"+str(pcb.pc)+"\n")
            
        
    def next(self):
        pcb = self.ready.getElement()
        return pcb
    
    def guardarPCBAnterior(self):
        pcb = self.cpu.pcb
        if pcb != None : 
            self.addReady(pcb)
            
    def desalojarPCBAnterior(self):
        pcb = self.cpu.pcb
        if pcb != None:
            self.cpu.pcb = None
            print("PCB  "+str(pcb.pid)+" fue desalojado por el roundRobin\n")
            
    def runCpu(self):
        #desaloja el anterior
        self.cpu.pcb = None
        pcb = self.next()
        if pcb != None:
            self.cpu.addPcb(pcb)
            
    def run(self):
        while True:
            self.guardarPCBAnterior()
            self.desalojarPCBAnterior()
            time.sleep(15)
     
   
              
   
            
            
            
            
    
        
        