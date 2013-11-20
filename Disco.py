'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

class Disco:
    def __init__(self):
        self.programas = {}
        #self.programas = []

    def addProgram(self,p):
        self.programas[p.nombre] = p
        #self.programa.append(p)

    def getPrograma(self,nomProg):
    #busco el programa en la lista
        return self.programas[nomProg]
        #return self.programa(nomProg)   
