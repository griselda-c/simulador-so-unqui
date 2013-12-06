
from Block import *
from miFifo import *
from Pagina import *

class Paginacion:
    def __init__(self, disco,tamanioMarco):
        self.listaPaginas = miFifo()
        self.memoria = None # se setea cuando se agrega a la memoria
        self.tablaPaginas = []
        self.disco = disco
        self.tamanioMarco = tamanioMarco

    def findBlockEmpty(self,programa,pcb,memoria):
		print("METODO: findBlockEmpty")
		if not self.hayMarcoLibre(memoria):
			self.swapOut()
		# pagina = self.swapIn()
		return self.getPagina(programa,pcb)
	
    def getPagina(self,programa,pcb):
		print("METODO: getPagina")
		listaPaginas = self.armoListaPaginas(programa)
		pagina = self.pagInstrucAEjecutar(listaPaginas,pcb)
	
    def armoListaPaginas(self,programa):
		print("METODO: armoListaPaginas")
		listaPaginas = []
		while index <= programa.getCantInst():
			pagina = Pagina(index,self.tamanioMarco)
			pagina = self.cargoIntrucPagina(pagina,programa,index,tamanioMarco)
			index = index + self.tamanioMarco
			listaPaginas.append(pagina)
		return listaPaginas
		
	def cargoIntrucPagina(self,pagina,programa,inicio,tamanioMarco):
		print("METODO: cargoIntrucPagina")
		
		
	def pagInstrucAEjecutar(self,listaPaginas,pcb):
		print("METODO: pagInstrucAEjecutar")
	
    def hayMarcoLibre(self,memoria):
		print("METODO: hayMarcoLibre")
		self.memoria = memoria
		resultado = self.memoria.hayLugar(self.tamanioMarco)
		print("hay Marco Libre: "+str(resultado))
		return resultado

    def swapOut(self):
		print("METODO: swapOut")
		pagina = self.buscoPaginaVictima()
		self.copioPaginaADisco(pagina)
		self.eliminoPaginaEnMemoria(pagina,memoria)
		self.actualizacionTablaPag(pagina)
		return pagina
		
    def buscoPaginaVictima(self):
		return self.listaPaginas.getElement()
		
    def copioPaginaADisco(self,pagina):
		self.disco.addPagina(pagina)
		
    def eliminoPaginaEnMemoria(self,pagina,memoria):
		# ya se hace en buscoPaginaVictima
		
	def actualizacionTablaPag(self,pagina):
		self.tablaPaginas.pop(pagina.direInicial)
		registroTabla = (pagina.direInicial,0) # es una tupla
		self.tablaPaginas.append(registroTabla)

    def swapIn(self):
		self.copioPaginaDeDiscoAMemoria(pagina)
		self.actualizacionTablaPag(pagina)

    def liberarBloque(self,direInicial):
		print("METODO: liberarBloque")
		#self.listaPaginas.pop(baseDirection)
		self.tablaPaginas.pop(direInicial)
		# falta quitarlo de los marcos
		
    def copioPaginaDeDiscoAMemoria(self,pagina):
		print("METODO: copioPaginaDeDiscoAMemoria")