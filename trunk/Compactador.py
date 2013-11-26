'''
Created on 25/11/2013

@author: Griselda
'''
from Block import *

class Compactador:
    def __init__(self,asignacionContinua):
        self.bloquesIntermedios = []
        self.bloquesAfectados = []
        self.asignacion = asignacionContinua
        
    def getCantidadDeCeldasLibres(self):
        tamanio = 0
        for bloque in self.asignacion.blockFree:
            tamanio+=bloque.size()
            
        return tamanio
                
    def esIntermedio(self,inicio,fin,bloque):
        return bloque.first >= inicio and bloque.last <=fin
        
        
    def setBloquesOcupadosAModificar(self,inicio,fin):
        for bloque in self.asignacion.blockBusy:
            if bloque.first >= inicio:
                if self.esIntermedio(inicio, fin, bloque):
                    self.bloquesIntermedios.append(bloque)
                else:
                    self.bloquesAfectados.append(bloque)
                    
                    
    def moverBloquesAfectados(self):
        finDelBloqueLibre = self.asignacion.blockFree[0].last # el bloque es unico
        cantMovimientos = (self.bloquesAfectados[0].first  - finDelBloqueLibre) - 1 #los bloques tienen que estar ordenados
        for bloque in self.bloquesAfectados:
            bloque.first = bloque.first - cantMovimientos #siempre se mueve hacia arriba.
            bloque.last = bloque.last - cantMovimientos
     
        self.asignacion.blockBusy = self.bloquesAfectados #se setean a la asignacion la nueva lista de ocupados
    
    def getUltimoDeLaLista(self,lista):
        indice = len(lista) - 1
        return lista[indice]
        
    def moverBloquesIntermedios(self):
        for bloque in self.bloquesIntermedios:
            bloqueUltimoDeOcupados = self.getUltimoDeLaLista(self.asignacion.blockBusy)
            inicio = bloqueUltimoDeOcupados.last + 1
            fin = inicio + bloque.size()
            bloqueNuevo = Block(inicio,fin)
            #agrega el bloque al final 
            self.asignacion.blockBusy.append(bloqueNuevo)
                        
    def compactar(self):
        self.unirBloquesLibres()
        self.moverBloquesAfectados()
        self.moverBloquesIntermedios()
        print("se compacto\n")
        
                    
    def unirBloquesLibres(self):
        inicio = self.asignacion.blockFree[0].first
        final =  inicio + self.getCantidadDeCeldasLibres() - 1
        #ahora existe un unico bloque libre 
        self.asignacion.blockFree = [Block(inicio,final)]
        self.setBloquesOcupadosAModificar(inicio,final)
        
        
