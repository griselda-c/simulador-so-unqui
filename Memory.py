
from Block import *

class Memory:
    def __init__(self, limit,asignador):
    #a validar
        self.celdas = {} # las celdas es ahora un diccionario
        self.asignador = asignador
        asignador.setMemoria(self)
        #limit es la capacidad total de la memoria
        self.limit = limit
        mode = asignador.getModo()
        mode.crearLibres(self.limit)
        
            
    def addInstruction(self,index,instruction):
        print("en el indice " +str(index) + " se guardo instruccion " +str(instruction)+"del pcb " +str(instruction.pcb.pid)+"\n")
        self.celdas[index] = instruction
        
    def hayLugar(self,tamanio):
		return self.asignador.getModo().hayLugar(tamanio,self.limit,self)
 
    def load(self,programa,pcb):
        modo = self.asignador.getModo()
        modo.guardar(self,programa,pcb)
        
            
    def delete(self,pcb):
        mode = self.asignador.getModo()
        mode.liberar(self,pcb) 
        
       
                                
   
