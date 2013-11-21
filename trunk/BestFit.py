
from Block import *

class BestFit:
	# blocks : lista de bloques libres
    # size : tamanio del bloque a agregar
    def getBlock(self, blocks, size):
		
        if len(blocks) == 0:
            return None
        else:
			# inicializo variables
            self.menorDif = 0
            self.dif = 0
            for block in blocks:
			    self.menorDif = self.menorDif + block.size()

			# se busca el bloque de mejor ajuste
            for block in blocks:
                self.dif = (block.size() - size)
                if self.dif < self.menorDif and self.dif >= 0:
                    self.menorDif = self.dif
                    self.bloqueFinal = block
                    print("block size " +str(block.size()))
            return self.bloqueFinal
