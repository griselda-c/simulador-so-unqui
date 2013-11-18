
from miFifo import *

class SchedulerFifo:
    def __init__(self,cpu):
        self.ready = miFifo() #fifo
        self.cpu = cpu

    def addReady(self, pcb): # llamddo por Kernel al crear el PCB
        print("el PCB " +str(pcb.pid) +" esta en el scheduler\n ")
        self.ready.addElement(pcb)

    def next(self):
        pcb = self.ready.getElement()
        return pcb

    def runCpu(self):
        #desaloja el anterior
        self.cpu.pcb = None
        pcb = self.next()
        if pcb != None:
            self.cpu.addPcb(pcb)
