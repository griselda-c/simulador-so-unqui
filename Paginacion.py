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
        #self.imprimirPaginasVacias()


    def imprimirPaginasVacias(self):
        for pagina in self.listaMarcosLibres.ls:
            print("pagina nro "+str(pagina.id))
            
    def calcularIndice(self, pagina):
        indexEnMemoria = pagina.id * self.tamanioPag
        return indexEnMemoria
    
    def setearPcbALaPagina(self,pagina,pcb):
        pagina.setPcb(pcb)

    def guardar(self,memoria,programa,pcb):
        print("METODO: guardar")
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
        
        #for pagina in marcos:
        #    self.listaMarcosOcupados.addElement(pagina)
            
        print("se cargo el programa en memoria\n")
        

    def cargoInstrucciones(self,instrucciones,index,pcb,memoria,pagina):
        print("METODO: cargoInstrucciones del pcb "+str(pcb.pid))
        i = 0
        print("Cantidad Instrucciones: " + str(len(instrucciones)))
        while i < len(instrucciones) and i < pagina.tamanio:
            instruccion = instrucciones[i]
            instruccion.setPcb(pcb)
            memoria.addInstruction(index, instruccion)
            pagina.addInstruccion(instruccion)
            index = index + 1
            i = i + 1
    

    def getMarcoVacio(self,memoria):
        marco = self.listaMarcosLibres.getElement()
        if marco == None:
            self.swapOut(memoria)
            marco = self.listaMarcosLibres.getElement()           
        return marco


    def guardarMarcoEnOcupado(self, marco):
        print("la pagina "+str(marco.id)+" esta en ocupados")
        return self.listaMarcosOcupados.addElement(marco)

    def buscoMarcosVacio(self,CantidadInstrucciones,memoria): #saque el pcb
        print("METODO: buscoMarcosVacio")
        cantidadPag = self.cantPagNecesarias(CantidadInstrucciones)
        marcosVacios = []
        
        for index in range(0,cantidadPag):
            marco = self.getMarcoVacio(memoria) # si no hay lugar hace swap out
            self.guardarMarcoEnOcupado(marco)
            marcosVacios.append(marco)
            
        print("Se tomaron : "+str(len(marcosVacios)) +" marcos, quedan libres "+str(self.listaMarcosLibres.size())+" marcos\n")
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
        self.mmu.borrarDeTabla(pcb)

        
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
        print("Hay lugar en memoria ----->"+str(resultado)+"\n")
        return resultado

    def swapOut(self,memoria):
        print("METODO: SWAPOUT  !!!!!!!!!!!!!!")
        pagina = self.listaMarcosOcupados.getElement() # FIFO para la pagina victima
        print("pagina victima ------>"+str(pagina.id))
        
        pagina.setBit(0)
        self.disco.addPagina(pagina) # se baja a disco
        paginaLimpia = Pagina(pagina.id,self.tamanioPag)
        self.listaMarcosLibres.addElement(paginaLimpia)
        direInicioPag = pagina.id * self.tamanioPag
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
        self.cargoInstrucciones(pagina.instrucciones, indice, pcb, memoria, marcoNuevo)
        self.mmu.modificarTabla(pcb,paginaRecuperada,marcoNuevo)
        print("Se hizo swap in de la pagina "+str(paginaRecuperada.id)+" del pcb "+str(pcb.pid))
        #ahora hay que cargar en memoria
        
    def crearMMU(self,memoria):
        mmu = MMU_paginacion(memoria,self.tamanioPag,self)
        self.mmu = mmu
        return mmu
