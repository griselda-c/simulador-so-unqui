'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

class Disco:
    def __init__(self):
        self.programas = {}
        self.paginas = {}
        #self.tablaPagDico = {}

    def addProgram(self,p):
        self.programas[p.nombre] = p
        #self.programa.append(p)

    def getPrograma(self,nomProg):
    #busco el programa en la lista
        return self.programas[nomProg]
        #return self.programa(nomProg)   


	def getPagina(self,pag):
		return self.paginas[pag.direInicial]

    def addPagina(self,pag):
        self.paginas[pag.direInicial] = pag
        

