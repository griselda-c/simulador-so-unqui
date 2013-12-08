


class MMU_paginacion():

    def __init__(self,memory):
		self.memory = memory
		self.tablaPaginas= {}
		self.tamanioPag = None

    def getInstruccion(self,pcb):
		indicePag = pcb.pc // self.tamanioPag
		lPaginasProceso = self.tablaPaginas[pcb.pid]
		pagina = lPaginasProceso[indicePag]
		desplazamiento = ( pcb.pc % self.tamanioPag )
		direction = (pagina * self.tamanioPag) + desplazamiento		
		print("fetch de la instruccion que esta en la direccion-----> " +str(direction))
		instruction = self.memory.celdas[direction]
		return instruction