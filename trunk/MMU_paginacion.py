


class MMU_paginacion():

    def __init__(self,memory,tamanioPag):
        self.memory = memory
        self.tablaPaginas= {}
        self.tamanioPag = tamanioPag

    def getInstruccion(self,pcb):
        indicePag = pcb.pc // self.tamanioPag
        lPaginasProceso = self.tablaPaginas[pcb.pid]
        pagina = lPaginasProceso[indicePag]
        desplazamiento = ( pcb.pc % self.tamanioPag )
        direction = (pagina.id * self.tamanioPag) + desplazamiento        
        print("fetch de la instruccion que esta en la direccion-----> " +str(direction))
        instruction = self.memory.celdas[direction]
        return instruction
