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

    def setBit(self,bit):
        self.bit = bit

    def addInstruccion(self,inst):
        self.instrucciones.append(inst)
