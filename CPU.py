
from IRQIO import *
from IRQKILL import *
from IRQNEW import *
from threading import Semaphore
from Asignador import *

class CPU():
    def __init__(self, asignador):
        self.pcb = None
        self.mmu = asignador.getMMU()
        self.semaforo = Semaphore(1)

    def fetch(self):
        
        instruccion = None
        self.semaforo.acquire()# para que no pueda cambiar de Pcb mientras se intenta leer una instruccion
        if self.existPcb():
            print("se pide instruccion del PCB " +str(self.pcb.pid) +"\n")
            instruccion = self.mmu.getInstruccion(self.pcb)
        self.semaforo.release()
        return instruccion
                                   
    #metodo para saber si la CPU tiene pcb asignado
    def existPcb(self):
        resultado = self.pcb != None
        return resultado
    
    def addPcb(self,pcbNuevo):
        self.semaforo.acquire()
        self.pcb = pcbNuevo
        self.semaforo.release()
        
    def incrementarPCB(self,irqManager):# esto solo se ejecuta si las instruccion es de cpu
        self.pcb.incrementoPc()      
        if self.pcb.termino():
            irqKill = IRQKILL() #mata
            irqNew = IRQNEW()   #llama al proximo
            irqManager.handle(irqKill,self.pcb)
            irqManager.handle(irqNew,self.pcb)
            
    def handleIO(self,instruccion,io,irqManager):
        self.semaforo.acquire() #agregue semaforo
        tuplaInsPcb = (instruccion,self.pcb)
        io.addInstruccion(tuplaInsPcb) #se agrego pcb
        self.pcb.incrementoPc()
        self.semaforo.release()
        #Lanzo un irq
        irqIO = IRQIO()
        irqManager.handle(irqIO, self.pcb)
        
        
        
