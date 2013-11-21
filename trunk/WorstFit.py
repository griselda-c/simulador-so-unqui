'''
Created on 20/11/2013

@author: Griselda
'''

class WorstFit:
    def getBlock(self,blocks,size):
        diferencia = 0
        bloque = None
        for block in blocks:
            if(self.diferencia(block,size) >= diferencia):
                diferencia = self.diferencia(block, size)
                bloque = block
            
        return bloque
    
    def diferencia(self,block,tamanio):
        return block.size()-tamanio