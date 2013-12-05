
from Block import *

class Memory:
    def __init__(self, mode, limit):
    #a validar
        self.celdas = {} # las celdas es ahora un diccionario
        # modo: tipos de asignacion (continua o paginacion)
        self.mode = mode
        self.mode.blockFree.append(Block(0,limit - 1)) #bloque inicial, la memoria entera
        #limit es la capacidad total de la memoria
        self.limit = limit
        # Necesito crear la memoria fisica
        for index in range(0,self.limit):
			self.celdas[index] = None
			
            
    def addInstruction(self,index,instruction):
        print("en el indice " +str(index) + " se guardo instruccion " +str(instruction)+"\n")
        self.celdas[index] = instruction
        
    def getCantCeldasLibres(self):
        return self.limit - len(self.celdas)
        
    def hayLugar(self,tamanio):   # LO LLAMA EL PLP
		return self.mode.hayLugar(tamanio,self.limit,self.celdas)
  
    def load(self,programa,pcb):    # LO LLAMA EL PLP
        block = self.mode.findBlockEmpty(programa.getCantInst(),self)#agrego aca la memoria
        pcb.baseDirection = block.first # se le asigna la direccionBase
        index = block.first
        for instruccion in programa.instrucciones:
            instruccion.setPcb(pcb)
            self.addInstruction(index, instruccion)
            index = index + 1       
        print("se cargo el programa en memoria\n")
            
    def delete(self,pcb): # LO LLAMA EL KERNEL
        for direction in range(pcb.baseDirection,pcb.baseDirection+pcb.cantInst):
            del self.celdas[direction]
            print("Se libero la celda----> "+str(direction)+" del pcb ---->" +str(pcb.pid)+"\n")
        print("Borre de memoriaaaaaaaaaaaaaaaaaaa\n")
        self.mode.liberarBloque(pcb.baseDirection)#buscar el bloque
    
    # Utilizado para la paginacion
    def existeMarcoLibre(self,tamanioMarco):
        contCeldas = 0
        resultado = False
        index = 0
        while index < self.limit or contCeldas == tamanioMarco:
			if self.celdas[index] is None:
				contCeldas = contCeldas + 1
				index = index + 1
			else:
				contCeldas = 0
				index = index + tamanioMarco
			if contCeldas == tamanioMarco:
				resultado = True
        print("existe MARCO LIBRE: "+str(resultado))
        return resultado
