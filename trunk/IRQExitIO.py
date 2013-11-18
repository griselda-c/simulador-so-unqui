
from IRQKILL import *

class IRQExitIO:
    
    def execute(self,pcb,kernel):
        kernel.agregarAlScheduler(pcb)