'''
Created on 10/12/2013

@author: Griselda Maricruz
'''

class Pagina:
    def __init__(self,num,tamanio):
        self.id = num
        self.instrucciones = []
        self.bit = 1
        self.tamanio = tamanio
        self.pcb = None

    def setBit(self,bit):
        self.bit = bit

    def addInstruccion(self,inst):
        self.instrucciones.append(inst)
        
    def cantInstrucciones(self):
        return len(self.instrucciones)
    
    def setPcb(self,pcb):
        self.pcb = pcb
        
    def getPcb(self):
        return self.pcb
