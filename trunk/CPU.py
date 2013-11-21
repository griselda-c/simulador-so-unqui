
from IRQIO import *
from IRQKILL import *
from IRQNEW import *

class CPU():
    def __init__(self, mmu):
        self.pcb = None
        self.mmu = mmu

    def fetch(self):
        if self.existPcb():
            print("se pide instruccion del pcb " +str(self.pcb.pid) +"\n")
            instruction = self.mmu.getInstruccion(self.pcb)
            return instruction
        else:
            return None
                                   
    #metodo para saber si la CPU tiene pcb asignado
    def existPcb(self):
        return self.pcb != None
    
    def addPcb(self,pcbNuevo):
        print("se agrego el pcb " + str(pcbNuevo.pid)+  " a la cpu\n")
        self.pcb = pcbNuevo
        
    def incrementarPCB(self,irqManager):# esto solo se ejecuta si las instruccion es de cpu
        self.pcb.incrementoPc()      
        if self.pcb.termino():
            irqKill = IRQKILL() #mata
            irqNew = IRQNEW()   #llama al proximo
            irqManager.handle(irqKill,self.pcb)
            irqManager.handle(irqNew,self.pcb)
            
    def handleIO(self,instruccion,io,irqManager):
        tuplaInsPcb = (instruccion,self.pcb)
        io.addInstruccion(tuplaInsPcb) #se agrego pcb
        #self.incrementarPCB(irqManager)
        self.pcb.incrementoPc()
        #Lanzo un irq
        irqIO = IRQIO()
        irqManager.handle(irqIO, self.pcb)
        
