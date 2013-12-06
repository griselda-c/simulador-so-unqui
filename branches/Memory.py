
from Block import *
from Marco import *

class Memory:
    def __init__(self, mode, limit):
        self.celdas = {}
        self.mode = mode #PAGINACION
        self.limit = limit
        self.marcosLibres = []
        self.marcosOcupados = []

		# Se crean las celdas de memoria vacia
        for index in range(0,self.limit):
			self.celdas[index] = None

		# Se crean los marcos de celdas
        while index < self.limit:
			marco = Marco(index,self.mode.tamanioMarco)
			index = index + self.mode.tamanioMarco
			self.marcosLibres.append(marco)

    def addInstruction(self,index,instruction):
        print("en el indice " +str(index) + " se guardo instruccion " +str(instruction)+"\n")
        self.celdas[index] = instruction

    def hayLugar(self,tamanio):   # LO LLAMA EL PLP
		return len(self.marcosLibres) > 0
  
    def load(self,programa,pcb):    # LO LLAMA EL PLP
        marco = self.mode.findBlockEmpty(programa,pcb,self)#agrego aca la memoria
        self.mode.cargarPagina(pcb,marco)

    def delete(self,pcb): # LO LLAMA EL KERNEL
        for direction in range(pcb.baseDirection,pcb.baseDirection+pcb.cantInst):
            del self.celdas[direction]
            print("Se libero la celda----> "+str(direction)+" del pcb ---->" +str(pcb.pid)+"\n")
        print("Borre de memoriaaaaaaaaaaaaaaaaaaa\n")
        self.mode.liberarBloque(pcb.baseDirection)#buscar el bloque

'''
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
'''
'''		
        pcb.baseDirection = block.first # se le asigna la direccionBase
        index = block.first
        for instruccion in programa.instrucciones:
            instruccion.setPcb(pcb)
            self.addInstruction(index, instruccion)
            index = index + 1       
        print("se cargo el programa en memoria\n")
'''
