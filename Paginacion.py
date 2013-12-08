
#from Block import *
#from miFifo import *

class Paginacion:
    def __init__(self, disco,tamanioPag):
        self.listaPaginas = []
        self.memoria = None
        self.disco = disco
        self.tamanioPag = tamanioPag
        self.listaMarcosLibres = []
        self.listaMarcosOcupados = []
        
    def crearLibres(self,limit):
        print("METODO: cearLibres")
        contador = 1
        nroPag = 0
        while contador <= limit:
            self.listaPaginas.append(nroPag)
            nroPag = nroPag + 1
            contador = nroPag * self.tamanioPag
        self.listaMarcosLibres = self.listaPaginas  
        print("Cantidad Paginas totales en memoria: "+str(nroPag-1))

    def guardar(self,memoria,programa,pcb):
		print("METODO: guardar")
		marcos = self.buscoMarcosVacio(programa.getCantInst())
		for pagina in marcos:
			indexEnMemoria = (pagina-1) * self.tamanioPag
			pcb.baseDirection = indexEnMemoria
			self.cargoInstrucciones(programa,indexEnMemoria,pcb,memoria)

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
