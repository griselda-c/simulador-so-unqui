
class Instruction():
    def __init__(self,instManager,message):
        self.instManager = instManager
        #self.pcb = None
        self.message = message

    def execute(self,cpu): #ahora conocen a la cpu
        self.instManager.evaluate(self,cpu)