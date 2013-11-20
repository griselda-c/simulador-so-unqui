
from Block import *

class AsignacionContinua:
    def __init__(self,typeFit):
        self.blockFree = [] # la lista de bloques libres debe estar ordenada
        #typeFit es el tipo de algoritmo que va a usar (first fit, best fit, worst fit)
        self.typeFit = typeFit
        self.blockBusy = []
        
    def agregarBloque(self,bloque):
        indice = self.getIndice(bloque)
        if indice == 0:
            self.blockFree.append(bloque)
        elif self.esElUltimo(indice):
            self.manejarBloqueContiguoArriba(bloque, indice)
        else:
            self.manejarBloqueContiguoArriba(bloque, indice)
            self.manejarBloqueContiguoAbajo(bloque, indice)
        
        
        self.imprimirBloquesLibres() 
        
     
    # devuelve en que indice se va a guardar el bloque, la idea es que este ordenado
    #para el caso que sea necesario unir dos bloques contiguos   
    def getIndice(self,bloque):
        encontre = False
        indice = 0
        while not encontre:
            if indice >= len(self.blockFree):
                return indice
                encontre = True
            elif bloque.first <= self.blockFree[indice].first:
                return indice
            else:
                indice+=1
        
        
    def esElUltimo(self,indice):
        return len(self.blockFree) == indice
        
    def manejarBloqueContiguoArriba(self,bloque,indice):
         if self.existeBloqueContiguoArriba:
                    self.unirConBloqueDeArriba(bloque, indice)
         else:
                    self.blockFree.append(block) 
                    
    def manejarBloqueContiguoAbajo(self,bloque,indice):
        if self.existeBloqueContiguaAbajo(bloque, indice):
            self.unirConBloqueDeABajo(bloque, indice)
                
    def imprimirBloquesLibres(self):
         for bloque in self.blockFree:
             print("("+str(bloque.first)+","+str(bloque.last)+")") 
             
    def existeBloqueContiguoArriba(self,bloque,indice):
        if indice > 0:
            bloqueDeArriba = self.blockFree[indice-1]
            return bloqueDeArriba.last - bloque.first == -1
        else:
             return False
    
    def existeBloqueContiguaAbajo(self,bloque,indice):
        if(len(self.blockFree) > indice):
            bloqueDeAbajo = self.blockFree[indice + 1]
            return bloqueDeAbajo.first - bloque.last == 1
        else:
            return False
    
    def unirConBloqueDeArriba(self,bloque,indice):
        bloqueDeArriba = self.blockFree[indice - 1]
        bloqueNuevo = Block(bloqueDeArriba.first,bloque.last)
        #borro los bloque anteriores
        self.blockFree.remove(bloqueDeArriba)
        self.blockFree.insert(indice-1, bloqueNuevo)#agregar en indice, ver cual indice
        print("se unio con el bloque de arriba")
        
    def unirConBloqueDeABajo(self,bloque,indice):
        bloqueDeAbajo = self.blockFree[indice + 1]
        bloqueNuevo = Block(bloque.first,bloqueDeAbajo.last)
        self.blockFree.remove(bloqueDeAbajo)
        self.blockFree.insert(indice, bloqueNuevo)# agregar en indice, ver cual indice
        
        
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

        
    def findBlockEmpty(self,size):
        block = self.typeFit.getBlock(self.blockFree,size) # retorna un bloque
        if block != None:          
            # ahora debo reacomodar el bloque
            first = block.first
            last = first + (size - 1)
            # bloque que va ser usado por la memoria
            blockUsed = Block(first, last)
            self.updateBlockFree(block, size)
            self.blockBusy.append(blockUsed)
            print("el programa ocupa el bloque (" +str(blockUsed.first) +"," +str(blockUsed.last)+")")
            return blockUsed
        else:
            self.compactacion()
        return block
    
    def compactacion(self):
        print("se ejecuta la compactacion")
'''
    def agregarBloqueLibre(self,bloque):
        self.blockFree.agregarBloque(bloque)
'''