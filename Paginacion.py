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
        contador = 0
        nroPag = 0
        while contador < limit:
            pagina = Pagina(nroPag,self.tamanioPag)
            self.listaMarcosLibres.addElement(pagina)
            nroPag = nroPag + 1
            contador = nroPag * self.tamanioPag
        print("Cantidad Paginas totales en memoria: "+str(self.listaMarcosLibres.size()))


    def calcularIndice(self, pagina):
        indexEnMemoria = pagina.id * self.tamanioPag
        return indexEnMemoria
    
    def setearPcbALaPagina(self,pagina,pcb):
        pagina.setPcb(pcb)

    def guardar(self,memoria,programa,pcb):
        marcos = self.buscoMarcosVacio(programa.getCantInst(),memoria)
        instrucciones = programa.instrucciones
        indiceLista = 0
        for pagina in marcos:
            indexEnMemoria = self.calcularIndice(pagina)
            pcb.baseDirection = indexEnMemoria         
            self.setearPcbALaPagina(pagina, pcb)
            self.cargoInstrucciones(instrucciones,indexEnMemoria,pcb,memoria,pagina)
            indiceLista = indiceLista + pagina.tamanio
            instrucciones = instrucciones[indiceLista:len(instrucciones)]
            
        self.mmu.cargarPaginaEnTabla(pcb,marcos)
        
        

    def cargoInstrucciones(self,instrucciones,index,pcb,memoria,pagina):
        i = 0
        print("CANTIDAD DE INSTRUCCIONES " +str(len(instrucciones))+"PAGINA TAMANIO "+str(pagina.tamanio))
        while i < len(instrucciones)and i < pagina.tamanio: #pagina.tamanio
            instruccion = instrucciones[i]
            instruccion.setPcb(pcb)
            memoria.addInstruction(index, instruccion)
            pagina.addInstruccion(instruccion)
            index = index + 1
            i = i + 1
        self.guardarMarcoEnOcupado(pagina)
    

    def getMarcoVacio(self,memoria):
        marco = self.listaMarcosLibres.getElement()
        if marco == None:
            self.swapOut(memoria)
            marco = self.listaMarcosLibres.getElement()           
        return marco


    def guardarMarcoEnOcupado(self, marco):
        return self.listaMarcosOcupados.addElement(marco)

    def buscoMarcosVacio(self,CantidadInstrucciones,memoria): #saque el pcb
        cantidadPag = self.cantPagNecesarias(CantidadInstrucciones)
        marcosVacios = []
        
        for index in range(0,cantidadPag):
            marco = self.getMarcoVacio(memoria) # si no hay lugar hace swap out
            marcosVacios.append(marco)
             
        return marcosVacios    
    
    def cantPagNecesarias(self,cantidadInstrucciones):
        cantidadPag = cantidadInstrucciones // self.tamanioPag
        if(cantidadInstrucciones % self.tamanioPag) > 0:
            cantidadPag = cantidadPag + 1
        return cantidadPag

    def liberar(self,memoria,pcb):
        listaPag = self.mmu.tablaPaginas[pcb.pid]
        print("CANTIDAD DE PAGINAS A LIBERAR " +str(len(listaPag)))
        for pagina in listaPag:
            direInicioPag = self.mmu.getDireccionFisicaPagina(pagina)
            self.limpioCeldas(direInicioPag,memoria,pagina)
            self.limpiarPagina(pagina)
            self.listaMarcosLibres.addElement(pagina)
            self.listaMarcosOcupados.remove(pagina)
        self.mmu.borrarDeTabla(pcb)

        
    def limpiarPagina(self,pagina):
        pagina.limpiarPagina()
        
    def borrarCelda(self, memoria, direction):
       memoria.deleteCell(direction)

    def limpioCeldas(self,direInicioPag,memoria,pagina):
        i = 0
        direction = direInicioPag
        print("LIMPIO CELDAS DE LA PAGINA----> "+str(pagina.id)+" del pcb ----->" +str(pagina.pcb.pid)+" que tiene cant instrucciones "+str(len(pagina.instrucciones)))
        while i < len(pagina.instrucciones): 
            self.borrarCelda(memoria, direction)
            i = i + 1
            direction = direction +1


    def hayLugar(self,tamanio,limit,memoria):
        resultado = True
        return resultado

    def swapOut(self,memoria):
        print("METODO: SWAPOUT  !!!!!!!!!!!!!!")
        pagina = self.listaMarcosOcupados.getElement() # FIFO para la pagina victima
        print("PAGINA VICTIMA ------>"+str(pagina.id))
        
        pagina.setBit(0)
        self.disco.addPagina(pagina) # se baja a disco
        paginaLimpia = Pagina(pagina.id,self.tamanioPag)
        self.listaMarcosLibres.addElement(paginaLimpia)
        direInicioPag = self.mmu.getDireccionFisicaPagina(pagina)
        self.limpioCeldas(direInicioPag,memoria,pagina)
        
    def buscarPaginaEnDisco(self,pagina):
        return self.disco.getPagina(pagina)
    
    def printMetodoSwap(self,pagina,titulo,pcb):
        print("METODO "+titulo+" DE LA PAGINA --->"+str(pagina.id)+"del pcb"+str(pcb.pid))
        
    def swapIn(self,pagina,memoria,pcb):
        self.printMetodoSwap(pagina,"SWAP IN",pcb)
        paginaRecuperada = self.buscarPaginaEnDisco(pagina)
        cantidadInstrucciones = paginaRecuperada.cantInstrucciones()
        marcoNuevo = self.buscoMarcosVacio(cantidadInstrucciones,memoria)[0] # si no hay hace swap out
        indice = self.calcularIndice(marcoNuevo)
        
        self.setearPcbALaPagina(marcoNuevo, pcb)
        self.cargoInstrucciones(paginaRecuperada.instrucciones, indice, pcb, memoria, marcoNuevo)
        self.mmu.modificarTabla(pcb,paginaRecuperada,marcoNuevo)
       
        
    def crearMMU(self,memoria):
        mmu = MMU_paginacion(memoria,self.tamanioPag,self)
        self.mmu = mmu
        return mmu
