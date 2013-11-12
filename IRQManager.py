
from Kernel import *

class IRQManager:
    def __init__(self, kernel):
        self.kernel = kernel

    def handle(self, irq, pcb):
        #print(irq)
        irq.execute(pcb,self.kernel,self)