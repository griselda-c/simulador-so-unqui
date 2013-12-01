'''
Created on 30/11/2013

@author: Griselda
'''

class ModificadorDeCeldas:
    def __init__(self):
        self.modificados = {}

    def modificarCeldas(self,bloqueAnterior,bloqueNuevo,memory):
        
        llegue = bloqueAnterior.last
        primero = bloqueAnterior.first
        primeroNuevo = bloqueNuevo.first
        
        self.modificarDireccionBase(bloqueAnterior, primeroNuevo, memory)
        
        while primero <= llegue:
            if(self.estaEnModificados(primero)):
                elemento = self.modificados[primero]
            else:
                elemento = memory.celdas[primero]
            
            if(self.tieneDatos(primeroNuevo,memory)): #celda destino
                self.agregarAModificados(primeroNuevo,memory.celdas[primeroNuevo])
            
            memory.celdas[primeroNuevo] = elemento
            #print("en el indice "+str(primeroNuevo)+" se guardo "+str(elemento))
            primero+= 1
            primeroNuevo+= 1
            print("el ultimo indice fue ....................................." +str(primeroNuevo))
        
        
    
    def modificarDireccionBase(self,bloque,nuevaDireccionBase,memory):
        instruccion = memory.celdas[bloque.first]
        instruccion.pcb.baseDirection = nuevaDireccionBase
        
    def estaEnModificados(self,indice):
        return self.modificados.has_key(indice)

    def tieneDatos(self,indiceNuevo,memory):
        return memory.celdas.has_key(indiceNuevo)
    
    def agregarAModificados(self,indice,valor):
        self.modificados[indice] = valor


