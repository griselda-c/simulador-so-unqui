'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

class Disco:
    def __init__(self):
        self.programas = {}
        self.paginas = {}

    def addProgram(self,p):
        self.programas[p.nombre] = p
        #self.programa.append(p)

    def getPrograma(self,nomProg):
    #busco el programa en la lista
        return self.programas[nomProg]
        #return self.programa(nomProg)   

    def addPagina(self,pag):
        #self.paginas.append(pag)
        pcbID = pag.getPcb().pid
        if self.paginas.has_key(pcbID):
            lista = self.paginas[pcbID]
            lista.append(pag)
        else:
            self.paginas[pcbID] = [pag]

    def getPagina(self,pag):
        pcbId = pag.getPcb().pid
        listaPaginas = self.paginas[pcbId]
        indice = listaPaginas.index(pag, )
        return listaPaginas[indice]
        
        
