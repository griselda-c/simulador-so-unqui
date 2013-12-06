


class MMU():

    def __init__(self,memory):
		self.memory = memory
		self.tablaPaginas = []

    def getInstruccion(self,pcb):
        direction = pcb.baseDirection + pcb.pc
        print("fetch de la instruccion que esta en la direccion-----> " +str(direction))
        instruction = self.memory.celdas[direction]     
        return instruction

    def getInstruccion(self,direVirtual):
		print("METODO: getInstruccion")
