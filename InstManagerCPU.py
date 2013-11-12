

class InstManagerCPU(): 
    def __init__(self,irqManager):
        self.irqManager = irqManager
        
    def evaluate(self,instruccion,cpu):
        print(instruccion.message)
        cpu.incrementarPCB(self.irqManager) #incremente pc y evalue si termino