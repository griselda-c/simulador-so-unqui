
from Block import *
from miFifo import *
from Pagina import *

class Paginacion:
    def __init__(self, disco,tamanioMarco):
        self.listaPaginas = miFifo()
        self.memoria = None # se setea cuando se agrega a la memoria
        self.tablaPaginas = []
        self.disco = disco
        self.blockFree = [] # solo por el momento!!
        self.tamanioMarco = tamanioMarco

    def hayLugar(self,tamanio,limit,celdas):
		resultado = True
		return resultado

	# no utilizo CantInst
    def findBlockEmpty(self,CantInst,memoria):
		print("METODO: findBlockEmpty")
		if not self.hayMarcoLibre(memoria):
			self.swapOut()
		# pagina = self.swapIn()
		# return = pagina
		# BLOQUE PROVISORIO  !!!!!!!!!!
		return Block(0,self.tamanioMarco)
	
    def hayMarcoLibre(self,memoria):
		print("METODO: hayMarcoLibre")
		self.memoria = memoria
		return self.memoria.existeMarcoLibre(self.tamanioMarco)

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
