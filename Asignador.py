'''
Created on 08/12/2013

@author: Griselda
'''

class Asignador():
    def __init__(self,modoDeAsignacion):
        self.modoDeAsignacion = modoDeAsignacion
        self.memoria = None
        self.mmu = None
        
        
        
    def getMMU(self):
        return self.mmu
        
    def setMemoria(self,memoria):
        self.memoria = memoria
        self.mmu = self.modoDeAsignacion.crearMMU(memoria)
        
    def getModo(self):
        return self.modoDeAsignacion
    
    

