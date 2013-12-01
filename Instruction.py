
class Instruction():
    def __init__(self,instManager,message): #agregue pcb
        self.instManager = instManager
        self.message = message
        self.pcb = None
        
    def setPcb(self,pcb):
        self.pcb = pcb

    def execute(self,cpu): #ahora conocen a la cpu
        self.instManager.evaluate(self,cpu)