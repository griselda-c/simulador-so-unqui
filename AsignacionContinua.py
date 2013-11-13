
from Block import *

class AsignacionContinua:
    def __init__(self,typeFit):
        self.blockFree = []
        #typeFit es el tipo de algoritmo que va a usar (first fit, best fit, worst fit)
        self.typeFit = typeFit
        
    def updateBlockFree(self,blockBefore, size):
        # si el bloque retornada resulto mas grande que el pedido, se crea un bloque nuevo con lo que resta y se elimina el bloque anterior
        if blockBefore.size() > size:
            first = size + blockBefore.first
            last = blockBefore.last
            newBlock = Block(first,last)
            self.blockFree.append(newBlock)
        self.blockFree.remove(blockBefore)
        self.printBloquesLibres()

    def printBloquesLibres(self):
        for bloque in self.blockFree:
            print(" el bloque libre de " +str(bloque.first) + " a " +str(bloque.last))  
        
    def findBlockEmpty(self,size):
        block = self.typeFit.getBlock(self.blockFree,size) # retorna un bloque
        if block != None:          
            # ahora debo reacomodar el bloque
            first = block.first
            last = first + (size - 1)
            # bloque que va ser usado por la memoria
            blockUsed = Block(first, last)
            self.updateBlockFree(block, size)
            print("el programa ocupa el bloque (" +str(blockUsed.first) +"," +str(blockUsed.last)+")")
            return blockUsed
        return block

    def agregarBloqueLibre(self,bloque):
        self.blockFree.append(bloque)