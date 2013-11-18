


class MMU():

    def __init__(self,memory):
		self.memory = memory

    def getInstruccion(self,pcb):
        direction = pcb.baseDirection + pcb.pc
        print("****la direccion retornada es " +str(direction))
        instruction = self.memory.celdas[direction]     
        return self.memory.celdas[direction]
