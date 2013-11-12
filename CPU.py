
from IRQIO import *
from IRQKILL import *
from IRQNEW import *

class CPU():
    def __init__(self, memoria):
        self.pcb = None
        self.memoria = memoria

    def fetch(self):
        if self.existPcb():
            print(" se pide instruccion del pcb " +str(self.pcb.pid) +"\n")
            instruction = self.memoria.getInstruccion(self.pcb)
            return instruction
                                   
    #metodo para saber si la CPU tiene pcb asignado
    def existPcb(self):
        return self.pcb != None
    
    def addPcb(self,pcbNuevo):
        print("se agrego pcb " + str(pcbNuevo.pid)+  " a la cpu\n")
        self.pcb = pcbNuevo
        
    def incrementarPCB(self,irqManager):
        self.pcb.incrementoPc()       
        if self.pcb.termino():
            irqKill = IRQKILL()
            irqNew = IRQNEW()
            irqManager.handle(irqKill,pcb)
            irqManager.handle(irqNew,pcb)
            
    def handleIO(self,instruccion,io,irqManager):
        tuplaInsPcb = (instruccion,self.pcb)
        io.addInstruccion(tuplaInsPcb) #se agrego pcb
        #Lanzo un irq
        irqIO = IRQIO()
        print("irqio")
        irqManager.handle(irqIO, self.pcb)
        
