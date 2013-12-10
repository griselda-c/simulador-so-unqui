from miFifo import *
from MMU_paginacion import *
from Pagina import *

class Paginacion:
    def __init__(self, disco,tamanioPag):
        self.memoria = None
        self.disco = disco
        self.tamanioPag = tamanioPag
        self.listaMarcosLibres = miFifo()
        self.listaMarcosOcupados = miFifo()
        self.mmu = None
        #self.mmu.tamanioPag = self.tamanioPag
        
    def crearLibres(self,limit):
        print("METODO: crearLibres")
        contador = 0
        nroPag = 0
        while contador < limit:
            pagina = Pagina(nroPag,self.tamanioPag)
            self.listaMarcosLibres.addElement(pagina)
            nroPag = nroPag + 1
            contador = nroPag * self.tamanioPag
        print("Cantidad Paginas totales en memoria: "+str(self.listaMarcosLibres.size()))

    def guardar(self,memoria,programa,pcb):
        print("METODO: guardar")
        marcos = self.buscoMarcosVacio(programa.getCantInst(),pcb)
        for pagina in marcos:
            indexEnMemoria = pagina.id * self.tamanioPag
            pcb.baseDirection = indexEnMemoria
            self.cargoInstrucciones(programa,indexEnMemoria,pcb,memoria,pagina)
        self.mmu.tablaPaginas[pcb.pid] = marcos
        
        #for pagina in marcos:
        #    self.listaMarcosOcupados.addElement(pagina)
            
        print("se cargo el programa en memoria\n")

    def cargoInstrucciones(self,programa,index,pcb,memoria,pagina):
        print("METODO: cargoInstrucciones")
        i = 0
        print("Cantidad Instrucciones: " + str(programa.getCantInst()))
        while i < pagina.tamanio:
            instruccion = programa.instrucciones[i]
            instruccion.setPcb(pcb)
            memoria.addInstruction(index, instruccion)
            pagina.addInstruccion(instruccion)
            index = index + 1
            i = i + 1
    
    def buscoMarcosVacio(self,CantidadInstrucciones,pcb):
        print("METODO: buscoMarcosVacio")
        cantidadPag = self.cantPagNecesarias(CantidadInstrucciones)
        marcosVacios = []
        for index in range(0,cantidadPag):
            marco = self.listaMarcosLibres.getElement()
            self.listaMarcosOcupados.addElement(marco)
            marcosVacios.append(marco)
        print("marcosVacios : "+str(len(marcosVacios)))
        for pagina in range(0,len(marcosVacios)):
            print("Marco : "+str(marcosVacios[pagina]))
        return marcosVacios    
    
    def cantPagNecesarias(self,cantidadInstrucciones):
        print("METODO: cantPagNecesarias")
        cantidadPag = cantidadInstrucciones // self.tamanioPag
        if(cantidadInstrucciones % self.tamanioPag) > 0:
            cantidadPag = cantidadPag + 1
        print("Necesito " + str(cantidadPag) + " paginas vacias")
        return cantidadPag

    def liberar(self,memoria,pcb):
        listaPag = self.mmu.tablaPaginas[pcb.pid]
        for pagina in listaPag:
            direInicioPag = pagina.id * self.tamanioPag
            self.limpioCeldas(direInicioPag,memoria,pagina)
        for pagina in listaPag:
            self.listaMarcosLibres.addElement(pagina)
            self.listaMarcosOcupados.getElement()
        del self.mmu.tablaPaginas[pcb.pid]

        
    def limpioCeldas(self,direInicioPag,memoria,pagina):
        print("METODO: limpioCeldas")
        i = 0
        direction = direInicioPag
        while i < len(pagina.instrucciones):
            del memoria.celdas[direction]
            print("Se libero la celda----> "+str(direction)) #+" del pcb ---->" +str(pcb.pid)+"\n")
            i = i + 1
            direction = direction +1
        print("Borre de memoria!!\n")

    def hayLugar(self,tamanio,limit,memoria):
        resultado = True
        print("METODO: hayLugar: ---------> "+str(self.listaMarcosLibres.size()))
        if self.listaMarcosLibres.size() == 0:
            self.swapOut(memoria)
            resultado = True
        print("Hay lugar en memoria ----->"+str(resultado)+"\n")
        return resultado

    def swapOut(self,memoria):
        print("METODO: SWAPOUT  !!!!!!!!!!!!!!")
        pagina = self.listaMarcosOcupados.getElement() # FIFO para la pagina victima
        pagina.setBit(0)
        self.disco.addPagina(pagina) # se baja a disco
        paginaLimpia = Pagina(pagina.id,self.tamanioPag)
        self.listaMarcosLibres.addElement(paginaLimpia)
        direInicioPag = pagina.id * self.tamanioPag
        self.limpioCeldas(direInicioPag,memoria,pagina)
        
    def crearMMU(self,memoria):
        mmu = MMU_paginacion(memoria,self.tamanioPag)
        self.mmu = mmu
        return mmu
