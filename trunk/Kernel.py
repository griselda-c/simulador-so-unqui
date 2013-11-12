'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

import threading
from threading import Semaphore
import time
#import random

class Kernel():
    
    def __init__(self,scheduler, hd, memory):
        self.pcbTable = []
        self.scheduler = scheduler
        self.cont = 0
        self.disco = hd
        self.memory = memory
        self.semaphore = Semaphore(1)

    def kill(self, pcb):
        self.pcbTable.remove(pcb)
        self.memory.delete(pcb)
        print("se elimino el pcb con id " + str(pcb.pid)+"\n")
        
    def loadMemory(self,programa, pcb):
        self.memory.load(programa, pcb)
 
    def addProcess(self, programa):
        pcb = PCB(self.getPId(), programa.getCantInst())
        print("se creo el pcb con id " +str(pcb.pid))
        self.pcbTable.append(pcb)
        self.loadMemory(programa,pcb) 
        self.agregarAlScheduler(pcb)

    def agregarAlScheduler(self, pcb):
        #if not self.scheluder.isEmpty():  
        self.scheduler.addReady(pcb)

    def getPId(self):
        self.semaphore.acquire()
        self.cont = self.cont + 1
        self.semaphore.release()
        return self.cont
        
    def schedulerNext(self):
        self.scheduler.runCpu()

    def run(self, nomPrograma):
        #programa = self.disco.getPrograma(nomPrograma)
    #se carga en memoria   
        self.addProcess(nomPrograma)



class Disco:
    def __init__(self):
        self.programas = []

    def addProgram(self,p):
        self.programa.append(p)

    def getPrograma(self,nomProg):
    #busco el programa en la lista
        return self.programa(nomProg)   

class CPU():
    def __init__(self, memoria):
        self.pcb = None
        self.memoria = memoria

    def fetch(self):
        if self.existPcb():
            print(" se pide instruccion del pcb " +str(self.pcb.pid) +"\n")
            instruction = self.memoria.getInstruccion(self.pcb)
            return instruction
                                   
    #metodo para saber si la CPU tiene pcb asignado
    def existPcb(self):
        return self.pcb != None
    
    def addPcb(self,pcbNuevo):
        print("se agrego pcb " + str(pcbNuevo.pid)+  " a la cpu\n")
        self.pcb = pcbNuevo
        
    def incrementarPCB(self,irqManager):
        self.pcb.incrementoPc()       
        if self.pcb.termino():
            irqKill = IRQKILL()
            irqNew = IRQNEW()
            irqManager.handle(irqKill,pcb)
            irqManager.handle(irqNew,pcb)
            
    def handleIO(self,instruccion,io,irqManager):
        tuplaInsPcb = (instruccion,self.pcb)
        io.addInstruccion(tuplaInsPcb) #se agrego pcb
        #Lanzo un irq
        irqIO = IRQIO()
        print("irqio")
        irqManager.handle(irqIO, self.pcb)
        
        
                
class Timer(threading.Thread):
    def __init__(self, cpu,irqManager): 
        threading.Thread.__init__(self)
        self.cpu = cpu
        self.irqManager = irqManager
        
    def evaluar(self):
        instruction = self.cpu.fetch()
        if instruction != None:
            instruction.execute(self.cpu) #ejecuta la instruccion
        else:
            # no hay pcb asignado por eso se llama irqNew
            irqNew = IRQNEW()
            self.irqManager.handle(irqNew, None)
            
        time.sleep(5)

    def run(self):
        while True:
            self.evaluar()
            
                
class IO(threading.Thread):
    def __init__(self,irqManager):
        threading.Thread.__init__(self)
        self.cola = miFifo()
        self.irqManager = irqManager

    def addInstruccion(self,tupla):
        print("an instruction is added to the queue of isIO\n")
        self.cola.addElement(tupla)
        
    def existInstruction(self):
        return self.cola.size() > 0


    def run(self):
        while True:
            if self.existInstruction():
                tupla = self.cola.getElement()
                instruction = tupla[0]
                print(instruction.message)
                #lanza un alerta irqExistIO para avisar al kernel que el pcb ya salio de IO
                irqExistIo = IRQExitIO()
                self.irqManager.handle(irqExistIo, tupla[1])
                
class IRQIO:
    def execute(self,pcb,kernel,irqManager):
        #pcb.incrementoPc()
        #llamar al proximo pcb
        kernel.schedulerNext()


class IRQExitIO:
    
    def execute(self,pcb,kernel,irqManager):
        pcb.incrementoPc()
        if pcb.termino():           
            # el pcb termino, entonces envia un alerta de kill
            irqKill = IRQKILL()
            irqManager.handle(irqKill,pcb)
            
        else:
            print("IO devolvio el pcb al scheduler")
            kernel.agregarAlScheduler(pcb)

            
            

class IRQKILL:    
    def execute(self,pcb,kernel,irqManager):
        kernel.kill(pcb)
        
        
class IRQNEW:
    #Alerta para avisar que no hay pcb asignado a la cpu
    #como no existe pcb, al ser execute se pasa None
    def execute(self,pcb,kernel,irqManager):
        kernel.schedulerNext()
    
     
#pcb = process control block
class PCB:
    def __init__(self, identificador, cantInst):
        self.pid = identificador
        self.pc = 0 #cantidad de instrucciones ejecutadas
        self.estado = "new"
        self.cantInst = cantInst
        self.baseDirection = 0
        #self.prioridad = prioridad

    def termino(self):
        resultado = self.cantInst == self.pc
        print(resultado)
        return self.cantInst == self.pc

    def incrementoPc(self):
        self.pc = self.pc + 1
        print(" el pc del pcb " + str(self.pid) +" es de " +str(self.pc))



class Program:
    def __init__(self, nombre):
        self.instrucciones = []
        self.nombre = nombre

    def addInstruction(self, instruccion): 
        self.instrucciones.append(instruccion)

    def getCantInst(self):
        return len(self.instrucciones)



class SchedulerFifo:
    def __init__(self,cpu):
        self.ready = miFifo() #fifo
        self.cpu = cpu

    def addReady(self, pcb): # llamddo por Kernel al crear el PCB
        print("******el pcb con el id " +str(pcb.pid) +" esta en el scheduler\n ")
        self.ready.addElement(pcb)

    def next(self):
        pcb = self.ready.getElement()
        return pcb

    def runCpu(self):
        #primero pongo None por si habia un pcb asignado,de esta manera lo saco y no sigue corriendo en caso
        # en que no haya next
        cpu.pcb = None
        #ahora si llamo al proximo
        pcb = self.next()
        if pcb != None:
            self.cpu.addPcb(pcb)


class Memory:
    def __init__(self, mode, limit):
    #a validar
        self.celdas = {} # las celdas es ahora un diccionario
        # modo: tipos de asignacion (continua o paginacion)
        self.mode = mode
        mode.blockFree.append(Block(0,limit - 1)) #bloque inicial, la memoria entera
        #limit: capacidad total de la memoria
        self.limit = limit
            
    def addInstruction(self,index,instruction):
        print(" en el indice " +str(index) + " se guardo instruccion " +str(instruction))
        self.celdas[index] = instruction
        
        
               
    def load(self,programa,pcb):
        block = self.mode.findBlockEmpty(programa.getCantInst())
        if block == None:
            print(" there is not enough place in memory")
            
        else:
            pcb.baseDirection = block.first # se le asigna la direccionBase
            index = block.first
            for instruction in programa.instrucciones:
                #instruction.pcb = pcb
                self.addInstruction(index, instruction)
                index = index + 1
            
        
            print("se cargo el programa en memoria\n")
            
    def delete(self,pcb):
        # borro el valor de esa clave
        for direction in range(pcb.baseDirection,pcb.cantInst-1):
            self.celdas[direction] = None
        print("Borre de memoriaaaaaaaaaaaaaaaaaaa")
        bloque = Block(pcb.baseDirection,pcb.baseDirection+pcb.cantInst)
        self.mode.agregarBloqueLibre(bloque)
                                
            
    def getInstruccion(self,pcb):
        #modificar esto para que lo haga la MMU
        #print(" pcb.baseDirection " +str(pcb.baseDirection) + " pc " +str(pcb.pc))
        direction = pcb.baseDirection + pcb.pc
        print("****la direccion retornada es " +str(direction))
        instruction = self.celdas[direction]
        #ESTO NO SE SI SE ELIMINA UNA INSTRUCCION ASI PERO POR EL MOMENTO....
        #self.delete(direction)       
        return self.celdas[direction]
        

       

class miFifo():

    def __init__(self):
        self.ls = []
        self.semaphore = Semaphore(1)

    def getElement(self):
        #volvi a poner los semaforos porque hay veces que explota
        self.semaphore.acquire()
        element = None
        if self.existElement():
            element = self.ls.pop(0)
        self.semaphore.release()
        return element
        

    def addElement(self, elem):       
        self.ls.append(elem)
        
        
    def existElement(self):
        return len(self.ls) > 0
    
    def size(self):
        return len(self.ls)
    
    
class Instruction():
    def __init__(self,instManager,message):
        self.instManager = instManager
        #self.pcb = None
        self.message = message
        
        
    def execute(self,cpu): #ahora conocen a la cpu
        self.instManager.evaluate(self,cpu)

class IRQManager:
    def __init__(self, kernel):
        self.kernel = kernel
        

    def handle(self, irq, pcb):
        #print(irq)
        irq.execute(pcb,self.kernel,self)
        

           
    
class InstManagerCPU(): 
    def __init__(self,irqManager):
        self.irqManager = irqManager
        
    def evaluate(self,instruccion,cpu):
        print(instruccion.message)
        cpu.incrementarPCB(self.irqManager) #incremente pc y evalue si termino

class InstManagerIO(): 
    def __init__(self,io,irqManager):
        self.io = io
        self.irqManager = irqManager
          
    def evaluate(self,instruccion,cpu):
        cpu.handleIO(instruccion,self.io,self.irqManager)
        
        
class Block:
    def __init__(self,first, last):
        self.first = first
        self.last = last
        
    def size(self):
        return (self.last - self.first ) + 1
    
    
class FirstFit:
    def getBlock(self,blocks,size):
        for block in blocks:
            if block.size() >= size:
                print("block size " +str(block.size()))
                return block
        return None
            
        
class AsignacionContinua:
    def __init__(self,typeFit):
        self.blockFree = []
        #typeFit es el tipo de algoritmo que va a usar (first fit, best fit, worst fit)
        self.typeFit = typeFit
        
    def updateBlockFree(self,blockBefore, size):
        # si el bloque retornada resulto mas grande que el pedido, se crea un bloque nuevo con lo que resta y se elimina el bloque anterior
        if blockBefore.size() > size:
            first = size + blockBefore.first
            last = blockBefore.last
            newBlock = Block(first,last)
            self.blockFree.append(newBlock)
        self.blockFree.remove(blockBefore)
        self.printBloquesLibres()
       
      
    def printBloquesLibres(self):
        for bloque in self.blockFree:
            print(" el bloque libre de " +str(bloque.first) + " a " +str(bloque.last))  
        
    def findBlockEmpty(self,size):
        block = self.typeFit.getBlock(self.blockFree,size) # retorna un bloque
        if block != None:          
            # ahora debo reacomodar el bloque
            first = block.first
            last = first + (size - 1)
            # bloque que va ser usado por la memoria
            blockUsed = Block(first, last)
            self.updateBlockFree(block, size)
            print("el programa ocupa el bloque inicio " +str(blockUsed.first) +" final " +str(blockUsed.last))
            return blockUsed
        return block

    def agregarBloqueLibre(self,bloque):
        self.blockFree.append(bloque)
    
        
        
        



#hacer los schedulers que faltan

firstFit = FirstFit()
continua = AsignacionContinua(firstFit)
memoria = Memory(continua,8)
cpu = CPU(memoria)
sh = SchedulerFifo(cpu)
disco = Disco()
k = Kernel(sh, disco,memoria)
irqManager = IRQManager(k)
io = IO(irqManager)



managerCPU = InstManagerCPU(irqManager)
managerIO =  InstManagerIO(io,irqManager)

timer = Timer(cpu,irqManager) 
timer.start()

i1 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i2 = Instruction(managerIO,"instruccion de IO ejecutandose")
i3 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i4 = Instruction(managerIO,"instruccion de IO ejecutandose")

i5 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i6 = Instruction(managerIO,"instruccion de IO ejecutandose")
i7 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i8 = Instruction(managerIO,"instruccion de IO ejecutandose")

p = Program("prog1")
p.addInstruction(i1) #0
p.addInstruction(i2) #1
p.addInstruction(i3) #2
p.addInstruction(i4) #3

p2 = Program("prog2")
p2.addInstruction(i5) #4
p2.addInstruction(i6) #5
p2.addInstruction(i7) #6
p2.addInstruction(i8) #7

'''
i9 = Instruction(managerCPU)
i10 = Instruction(managerIO)
i11 = Instruction(managerCPU)
i12 = Instruction(managerIO)

i13 = Instruction(managerCPU)
i14 = Instruction(managerIO)
i15 = Instruction(managerCPU)
i16 = Instruction(managerIO)

p3 = Program("prog3")
p3.addInstruction(i9) #
p3.addInstruction(i10) #10
p3.addInstruction(i11) 
p3.addInstruction(i12) 

p4 = Program("prog4")
p2.addInstruction(i5) #4
p2.addInstruction(i6) #5
p2.addInstruction(i7) #6
p2.addInstruction(i8) #7
'''


k.run(p) #cambie start por run poque todavia no estamos seguras que el kernel sea un Thread
io.start()
k.run(p2)
#k.run(p3)
