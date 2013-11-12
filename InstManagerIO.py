

class InstManagerIO(): 
    def __init__(self,io,irqManager):
        self.io = io
        self.irqManager = irqManager
          
    def evaluate(self,instruccion,cpu):
        cpu.handleIO(instruccion,self.io,self.irqManager)