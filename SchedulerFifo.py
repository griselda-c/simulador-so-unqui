
from miFifo import *

class SchedulerFifo:
    def __init__(self,cpu):
        self.ready = miFifo() #fifo
        self.cpu = cpu

    def addReady(self, pcb): # llamddo por Kernel al crear el PCB
        print("******el pcb con el id " +str(pcb.pid) +" esta en el scheduler\n ")
        self.ready.addElement(pcb)

    def next(self):
        pcb = self.ready.getElement()
        return pcb

    def runCpu(self):
        #primero pongo None por si habia un pcb asignado,de esta manera lo saco y no sigue corriendo en caso
        # en que no haya next
        self.cpu.pcb = None
        #ahora si llamo al proximo
        pcb = self.next()
        if pcb != None:
            self.cpu.addPcb(pcb)