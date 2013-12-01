'''
Created on 25/11/2013

@author: Griselda
'''
from Block import *
from ModificadorDeCeldas import *

class Compactador:
    def __init__(self,asignacionContinua): #recibe por parametro la memoria
        self.bloquesIntermedios = []
        self.bloquesAfectados = []
        self.asignacion = asignacionContinua
        self.modificadorDeCeldas = ModificadorDeCeldas() # agregue el modificador de celdas
        
    def getCantidadDeCeldasLibres(self):
        tamanio = 0
        for bloque in self.asignacion.blockFree:
            tamanio+=bloque.size()
            
        return tamanio
                
    def esIntermedio(self,inicioBloqueLibre,finBloqueLibre,bloque):
        return bloque.first >= inicioBloqueLibre or bloque.last <=finBloqueLibre
        
        
    def setBloquesOcupadosAModificar(self,inicio,fin):
        for bloque in self.asignacion.blockBusy:
            if bloque.first >= inicio:
                if self.esIntermedio(inicio, fin, bloque):
                    self.bloquesIntermedios.append(bloque)
                else:
                    self.bloquesAfectados.append(bloque)
       

    def modificarBloque(self, cantMovimientos, bloque,memoria):
        bloqueAnterior = bloque
        bloque.first = bloque.first - cantMovimientos #siempre se mueve hacia arriba.
        bloque.last = bloque.last - cantMovimientos
        self.modificadorDeCeldas.modificarCeldas(bloqueAnterior,bloque,memoria)
        
    def existenBloquesAfectados(self):
        return len(self.bloquesAfectados) > 0

    def moverBloquesAfectados(self,memoria): # bloques que quedan por debajo del bloque libre creado
        if self.existenBloquesAfectados():
            finDelBloqueLibre = self.asignacion.blockFree[0].last # el bloque es unico
            cantMovimientos = (self.bloquesAfectados[0].first  - finDelBloqueLibre) - 1 #los bloques tienen que estar ordenados
            for bloque in self.bloquesAfectados:
                self.modificarBloque(cantMovimientos, bloque,memoria)
            
    def imprimirBloques(self,nombre,lista):
        print(nombre)
        for bloque in lista:
            print("("+str(bloque.first)+","+str(bloque.last)+")\n")
            
    
    def getUltimoDeLaLista(self,lista):
        indice = len(lista) - 1
        return lista[indice]


    def crearBloqueAlFinalDe(self,lista, bloque):
        bloqueLibre = self.getUltimoDeLaLista(lista)
        inicio = bloqueLibre.last + 1
        fin = (inicio + bloque.size()) - 1
        bloqueNuevo = Block(inicio, fin)
        return bloqueNuevo

    def moverBloquesIntermedios(self,memoria): # bloque que debe ceder su lugar al bloque libre
        for bloque in self.bloquesIntermedios:
            bloqueNuevo = None
            if self.existenBloquesAfectados():
                bloqueNuevo = self.crearBloqueAlFinalDe(self.asignacion.blockBusy,bloque)               
                
            else:
                bloqueNuevo = self.crearBloqueAlFinalDe(self.asignacion.blockFree,bloque)
            
            self.asignacion.blockBusy.remove(bloque)
            self.asignacion.blockBusy.append(bloqueNuevo)
            self.modificadorDeCeldas.modificarCeldas(bloque,bloqueNuevo,memoria)
            
    def unirBloquesLibres(self):
        inicio = self.asignacion.blockFree[0].first
        final =  inicio + self.getCantidadDeCeldasLibres() - 1
        #ahora existe un unico bloque libre 
        self.asignacion.blockFree = [Block(inicio,final)]
        self.setBloquesOcupadosAModificar(inicio,final)
        self.imprimirBloques("bloque libre", self.asignacion.blockFree)
        
                        
    def compactar(self,memoria):
        self.imprimirBloques("busy antes de la compactacion", self.asignacion.blockBusy)
        self.unirBloquesLibres()
        self.moverBloquesAfectados(memoria)
        self.moverBloquesIntermedios(memoria)
        self.imprimirBloques("busy despues de la compactacion", self.asignacion.blockBusy)
        print("se compacto\n")
        
                    
    
        
