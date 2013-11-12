
class Program:
    def __init__(self, nombre):
        self.instrucciones = []
        self.nombre = nombre

    def addInstruction(self, instruccion): 
        self.instrucciones.append(instruccion)

    def getCantInst(self):
        return len(self.instrucciones)