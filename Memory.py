
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
        
    def getCantCeldasLibres(self):
        return self.limit - len(self.celdas)
        
    def hayLugar(self,tamanio):
        resultado = self.getCantCeldasLibres() >= tamanio
        print("Hay lugar en memoria ----->"+str(resultado)+"\n")
        return resultado
  
    def load(self,programa,pcb,mode):
        mode.guardar(self,programa,pcb)
        
            
    def delete(self,pcb,mode):
        mode.liberar(self,pcb) 
        
       
                                
   
