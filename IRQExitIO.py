
from IRQKILL import *

class IRQExitIO:
    
    def execute(self,pcb,kernel,irqManager):
        pcb.incrementoPc()
        if pcb.termino():           
            # el pcb termino, entonces envia un alerta de kill
            irqKill = IRQKILL()
            irqManager.handle(irqKill,pcb)
            
        else:
            print("IO devolvio el pcb al scheduler")
            kernel.agregarAlScheduler(pcb)