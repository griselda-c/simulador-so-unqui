
from Block import *

class Memory:
    def __init__(self, limit):
    #a validar
        self.celdas = {} # las celdas es ahora un diccionario
        #limit es la capacidad total de la memoria
        self.limit = limit
            
    def addInstruction(self,index,instruction):
        print("en el indice " +str(index) + " se guardo instruccion " +str(instruction)+"\n")
        self.celdas[index] = instruction
        
    def hayLugar(self,tamanio,mode):
		return mode.hayLugar(tamanio,self.limit,self)
 
    def load(self,programa,pcb,mode):
        mode.guardar(self,programa,pcb)
        
            
    def delete(self,pcb,mode):
        mode.liberar(self,pcb) 
        
       
                                
   
