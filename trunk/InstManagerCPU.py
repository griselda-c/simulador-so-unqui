

class InstManagerCPU(): 
    def __init__(self,irqManager):
        self.irqManager = irqManager
        
    def evaluate(self,instruccion,cpu):
        print(instruccion.message)
        cpu.incrementarPCB(self.irqManager) #incrementa pc y evalua si termino