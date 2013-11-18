
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
        return self.cantInst == self.pc

    def incrementoPc(self):
        self.pc = self.pc + 1
        print("PCB "+str(self.pid)+"------->PC "+str(self.pc))