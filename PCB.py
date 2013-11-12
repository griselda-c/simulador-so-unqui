
#pcb = process control block
class PCB:
    def __init__(self, identificador, cantInst):
        self.pid = identificador
        self.pc = 0 #cantidad de instrucciones ejecutadas
        self.estado = "new"
        self.cantInst = cantInst
        self.baseDirection = 0
        #self.prioridad = prioridad

    def termino(self):
        resultado = self.cantInst == self.pc
        print(resultado)
        return self.cantInst == self.pc

    def incrementoPc(self):
        self.pc = self.pc + 1
        print(" el pc del pcb " + str(self.pid) +" es de " +str(self.pc))