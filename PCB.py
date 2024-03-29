
#pcb = process control block
class PCB:
    def __init__(self, identificador, cantInst, nomPrograma):
        self.pid = identificador
        self.pc = 0 #cantidad de instrucciones ejecutadas
        self.estado = "new"
        self.cantInst = cantInst
        self.baseDirection = 0
        #self.prioridad = prioridad
        self.nomPrograma = nomPrograma

    def termino(self):
        return self.pc >= self.cantInst

    def incrementoPc(self):
        self.pc = self.pc + 1
        print("PCB "+str(self.pid)+"------->PC "+str(self.pc))