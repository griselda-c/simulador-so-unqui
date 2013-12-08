
class Paginacion:
    def __init__(self, disco,tamanioPag,mmu):
        #self.listaPaginas = []
        self.memoria = None
        self.disco = disco
        self.tamanioPag = tamanioPag
        self.listaMarcosLibres = []
        self.listaMarcosOcupados = []
        self.mmu = mmu
        self.mmu.tamanioPag = self.tamanioPag
        
    def crearLibres(self,limit):
        print("METODO: cearLibres")
        contador = 1
        nroPag = 0
        while contador <= limit:
            self.listaMarcosLibres.append(nroPag)
            nroPag = nroPag + 1
            contador = nroPag * self.tamanioPag
        print("Cantidad Paginas totales en memoria: "+str(nroPag-1))

    def guardar(self,memoria,programa,pcb):
		print("METODO: guardar")
		marcos = self.buscoMarcosVacio(programa.getCantInst())
		for pagina in marcos:
			indexEnMemoria = pagina * self.tamanioPag
			pcb.baseDirection = indexEnMemoria
			self.cargoInstrucciones(programa,indexEnMemoria,pcb,memoria)
		self.mmu.tablaPaginas[pcb.pid] = marcos

    def cargoInstrucciones(self,programa,index,pcb,memoria):
		print("METODO: cargoInstrucciones")
		i = 0
		while i < self.tamanioPag:
			instruccion = programa.instrucciones[i]
			instruccion.setPcb(pcb)
			memoria.addInstruction(index, instruccion)
			index = index + 1
			i = i + 1
		print("se cargo el programa en memoria\n")
	
    def buscoMarcosVacio(self,CantidadInstrucciones):
        print("METODO: buscoMarcosVacio")
        cantidadPag = self.cantPagNecesarias(CantidadInstrucciones)
        marcosVacios = []
        for index in range(0,cantidadPag):
			marco = self.listaMarcosLibres.pop(index)
			self.listaMarcosOcupados.append(marco)
			marcosVacios.append(marco)
        return marcosVacios	
	
    def cantPagNecesarias(self,cantidadInstrucciones):
		print("METODO: cantPagNecesarias")
		cantidadPag = cantidadInstrucciones // self.tamanioPag
		if(cantidadInstrucciones % self.tamanioPag) > 0:
			cantidadPag = cantidadPag + 1
		#cantidadPag = cantidadPag + (CantidadInstrucciones % self.tamanioPag)
		print("Necesito " + str(cantidadPag) + " paginas vacias")
		return cantidadPag

    def liberar(self,memoria,pcb):
		print("METODO: liberar")
		listaPag = self.mmu.tablaPaginas[pcb.pid]
		for pagina in listaPag:
			direInicioPag = pagina * self.tamanioPag
			self.limpioCeldas(direInicioPag,memoria,pcb)
		self.listaMarcosLibres.extend(listaPag)
		#self.listaMarcosOcupados.remove(listaPag)
		del self.mmu.tablaPaginas[pcb.pid]
			
    def limpioCeldas(self,direInicioPag,memoria,pcb):
		print("METODO: limpioCeldas")
		for direction in range(direInicioPag, direInicioPag + self.tamanioPag):
			del memoria.celdas[direction]
			print("Se libero la celda----> "+str(direction)+" del pcb ---->" +str(pcb.pid)+"\n")
		print("Borre de memoria!!\n")

'''
    def buscaDireInicioPag(self,pcb):
		indicePag = ( pcb.pc // self.tamanioPag ) - 1
		print("Indice de pag a liberar: "+ str(indicePag))
		lPaginasProceso = self.mmu.tablaPaginas[pcb.pid]
		pagina = lPaginasProceso[indicePag]
		desplazamiento = pcb.pc % self.tamanioPag
		direction = (pagina*self.tamanioPag) + desplazamiento
		return direction
'''
