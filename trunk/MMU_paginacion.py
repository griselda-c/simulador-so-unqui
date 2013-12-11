


class MMU_paginacion():

    def __init__(self,memory,tamanioPag,paginacion):
        self.memory = memory
        self.tablaPaginas= {}
        self.tamanioPag = tamanioPag
        self.paginacion = paginacion


    def buscarEnMemoria(self, pcb, pagina):
        desplazamiento = pcb.pc % self.tamanioPag
        direction = (pagina.id * self.tamanioPag) + desplazamiento
        print "fetch de la instruccion que esta en la direccion-----> " + str(direction)+"del pcb "+str(pcb.pid)
        instruction = self.memory.celdas[direction]
        return instruction


    def getPagina(self, pcb):
        indicePag = pcb.pc // self.tamanioPag
        lPaginasProceso = self.tablaPaginas[pcb.pid]
        pagina = lPaginasProceso[indicePag]
        return pagina

    def getInstruccion(self,pcb):
        print("se pide en MMU la instruccion del PCB " +str(pcb.pid) +"\n")
        pagina = self.getPagina(pcb)
        instruction = None
        if self.paginaEstaEnMemoria(pagina):
            instruction = self.buscarEnMemoria(pcb, pagina)
        else:
            self.paginacion.swapIn(pagina,self.memory,pcb)
            paginaNueva = self.getPagina(pcb)
            instruction = self.buscarEnMemoria(pcb, paginaNueva)
            
        return instruction

    def paginaEstaEnMemoria(self,pagina):
        return pagina.bit == 1
    
   
    def cargarPaginaEnTabla(self,pcb,pagina):
        self.tablaPaginas[pcb.pid] = pagina
        
    def existePagina(self,pcb,pagina):
        resultado = False
        for pag in self.tablaPaginas[pcb.pid]:
            if pag.id == pagina.id:
                resultado = True
        return resultado
    
    def buscarPagina(self,pcb,pagina):
        pagEnc= None
        for pag in self.tablaPaginas[pcb.pid]:
            if pag.id == pagina.id:
                pagEnc = pag
        return pagEnc
    
    def borrarDeTabla(self,pcb):
        del self.tablaPaginas[pcb.pid]
        print("SE BORRO DEL MMU EL PCB "+str(pcb.pid))
            
        
        
    def modificarTabla(self,pcb,paginaAnterior,paginaNueva):
        paginas = self.tablaPaginas[pcb.pid]
        if self.existePagina(pcb, paginaAnterior):
            paginaVieja = self.buscarPagina(pcb, paginaAnterior)
            indice = paginas.index(paginaVieja, )       
            paginas.insert(indice,paginaNueva)
            paginas.remove(paginaVieja)
        else:
            paginas.append(paginaNueva)
                 
    
