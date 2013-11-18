
from Block import *

class Memory:
    def __init__(self, mode, limit):
    #a validar
        self.celdas = {} # las celdas es ahora un diccionario
        # modo: tipos de asignacion (continua o paginacion)
        self.mode = mode
        mode.blockFree.append(Block(0,limit - 1)) #bloque inicial, la memoria entera
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
    '''           
    def load(self,programa,pcb):
        flagCarga = True
        block = self.mode.findBlockEmpty(programa.getCantInst())
        if block == None:
            print(" no hay lugar en memoria\n")
            flagCarga = False
        else:
            pcb.baseDirection = block.first # se le asigna la direccionBase
            index = block.first
            for instruction in programa.instrucciones:
                self.addInstruction(index, instruction)
                index = index + 1       
            print("se cargo el programa en memoria\n")
        return flagCarga
        
    '''
    def load(self,programa,pcb):
        block = self.mode.findBlockEmpty(programa.getCantInst())
        if block == None:
            print("compactacion\n")
            
        else:
            pcb.baseDirection = block.first # se le asigna la direccionBase
            index = block.first
            for instruccion in programa.instrucciones:
                self.addInstruction(index, instruccion)
                index = index + 1       
            print("se cargo el programa en memoria\n")
            
    def delete(self,pcb):
        # borro el valor de esa clave
        for direction in range(pcb.baseDirection,pcb.cantInst):
            del self.celdas[direction]
            print("Se libero la celda----> "+str(direction)+" del pcb ---->" +str(pcb.pid)+"\n")
        print("Borre de memoriaaaaaaaaaaaaaaaaaaa\n")
        last = (pcb.baseDirection + pcb.cantInst) - 1 #porque la memoria empieza con direccion cero
        bloque = Block(pcb.baseDirection,last)
        self.mode.agregarBloque(bloque)
                                
    '''          
    def compactacion(self):
        print("se ejecuta la compactacion")
        
    '''