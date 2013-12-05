
from Block import *
from Compactador import *

class AsignacionContinua:
    def __init__(self,typeFit):
        self.blockFree = [] # la lista de bloques libres debe estar ordenada
        #typeFit es el tipo de algoritmo que va a usar (first fit, best fit, worst fit)
        self.typeFit = typeFit
        self.blockBusy = []
        self.memoria = None # se setea cuando se agrega a la memoria
        
    def liberarBloque(self,bloqueInicio):
        bloque = self.getBloqueUsado(bloqueInicio)
        
        indice = self.getIndice(bloque) #busca en que indice se va a guardar
       
        if not self.hayBloquesLibres():
            self.blockFree.append(bloque)
        elif self.esElUltimo(indice):
            self.manejarBloqueContiguoArriba(bloque, indice)
        else:
            self.manejarBloqueContiguoArriba(bloque, indice)
            self.manejarBloqueContiguoAbajo(bloque, indice)
            
    def agregarBloque(self,indice,bloque):
        self.blockFree.insert(indice, bloque)
        
    def yaSeUnioConElBloqueDeArriba(self,bloque):
        return not self.blockFree.__contains__(bloque) #si es false es porque se unio con el bloque de arriba entonces el indice no cambia
        
    def getBloqueUsado(self,bloqueInicio):
        bloqueRetornado = None
        for bloque in self.blockBusy:
            if bloque.first == bloqueInicio:
                bloqueRetornado = bloque
                self.blockBusy.remove(bloque)
                return bloqueRetornado
            
    # devuelve en que indice se va a guardar el bloque, la idea es que este ordenado
    #para el caso que sea necesario unir dos bloques contiguos   
    def getIndice(self,bloque):
        indice = 0
        if self.hayBloquesLibres():
            indice = self.buscarIndice(bloque)
        return indice
            
        
    def hayBloquesLibres(self):
        return len(self.blockFree) > 0
    
    def buscarIndice(self,bloque):
        encontre = False
        indice = 0
        while not encontre and indice < len(self.blockFree):
            if bloque.first <= self.blockFree[indice].first:
                encontre = True
            else:
                indice+=1
        return indice
            
        
        
    def esElUltimo(self,indice):
        return len(self.blockFree) == indice
        
    def manejarBloqueContiguoArriba(self,bloque,indice):
         if self.existeBloqueContiguoArriba(bloque,indice):
                    self.unirConBloqueDeArriba(bloque, indice)
         else:   
                    self.agregarBloque(indice, bloque)
                    
                    
    def existeBloqueContiguoArriba(self,bloque,indice):
        if indice > 0:
            bloqueDeArriba = self.blockFree[indice-1]
            return bloque.first - bloqueDeArriba.last == 1#bloqueDeArriba.last - bloque.first == -1
        else:
             return False
    
    def manejarBloqueContiguoAbajo(self,bloque,indice):
        indiceV = indice
        if not self.yaSeUnioConElBloqueDeArriba(bloque):
            indiceV = indice + 1 # el indice varia si se unio con el de arriba o no
        if self.existeBloqueContiguaAbajo(bloque, indiceV):
            self.unirConBloqueDeABajo(bloque, indiceV)
           
                
    def imprimirBloquesLibres(self):
        indice = 0
        while indice < len(self.blockFree):
            bloque = self.blockFree[indice]
            print("("+str(bloque.first)+","+str(bloque.last)+")")
            indice+=1
        
           
    
    def existeBloqueContiguaAbajo(self,bloque,indice):
        resultado = False
        if(len(self.blockFree) > indice):
            bloqueDeAbajo = self.blockFree[indice]
            resultado = bloqueDeAbajo.first - bloque.last == 1
        return resultado
    
    def unirConBloqueDeArriba(self,bloque,indice):
        bloqueDeArriba = self.blockFree[indice - 1]
        bloqueDeArriba.last = bloque.last
        
        
    def unirConBloqueDeABajo(self,bloque,indice):
        bloqueDeAbajo = self.blockFree[indice] 
        bloqueAnterior = self.blockFree[indice - 1]
        bloqueDeAbajo.first = bloqueAnterior.first
        self.blockFree.remove(bloqueAnterior) #porque lo uni con el siguiente
        
        
    def updateBlockFree(self,blockBefore, size):
        # si el bloque retornada resulto mas grande que el pedido, se crea un bloque nuevo con lo que resta y se elimina el bloque anterior
        if blockBefore.size() > size:
            first = size + blockBefore.first # bf = (5,19), necesito un bloque de 3. sobra (8,19)
                                             # first = 3 + 5
            blockBefore.first = first
        else:
            #no sobro nada
            self.blockFree.remove(blockBefore)
        self.imprimirBloquesLibres()

        

    def recortarBloque(self, size, block):
        # ahora debo reacomodar el bloque
        first = block.first
        last = first + (size - 1)
    # bloque que va ser usado por la memoria
        blockUsed = Block(first, last)
        self.updateBlockFree(block, size)
        self.blockBusy.append(blockUsed)
        return blockUsed

    def findBlockEmpty(self,size,memory):
        block = self.typeFit.getBlock(self.blockFree,size) # retorna un bloque
        if block != None:          
            blockUsed = self.recortarBloque(size, block)
            print("el programa ocupa el bloque (" +str(blockUsed.first) +"," +str(blockUsed.last)+")\n")
            return blockUsed
        else:
            block = self.compactacion(memory)
            blockUsed = self.recortarBloque(size, block)
            return blockUsed
    
    def compactacion(self,memory):
        compactador = Compactador(self)
        compactador.compactar(memory)
        return self.blockFree[0] #al terminar la compactacion queda un unico bloque libre

    def hayLugar(self,tamanio,limit,celdas):
        resultado = (limit - len(celdas)) >= tamanio
        print("Hay lugar en memoria ----->"+str(resultado)+"\n")
        return resultado

