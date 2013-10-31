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
        print("se elimino el pcb con id " + str(pcb.pid)+"\n")
        
    def loadMemory(self,programa,pcb):
        self.memory.load(programa,pcb)
 
    def addProcess(self, programa):
        pcb = PCB(self.getPId(), programa.getCantInst())
        print("se creo el pcb con id " +str(pcb.pid))
        self.pcbTable.append(pcb)
        self.loadMemory(programa, pcb) 
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
        return p    

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
        print("se agrego pcb a la cpu\n")
        self.pcb = pcbNuevo
        
                
class Timer(threading.Thread):
    def __init__(self, cpu,irqManager): 
        threading.Thread.__init__(self)
        self.cpu = cpu
        self.irqManager = irqManager
        
    def evaluar(self):
        instruction = self.cpu.fetch()
        if instruction != None:
            instruction.execute() #ejecuta la instruccion
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

    def addInstruccion(self,io):
        self.cola.addElement(io)
        
    def existInstruction(self):
        return self.cola.size() > 0


    def run(self):
        while True:
            if self.existInstruction():
                instruction = self.cola.getElement()
                print("ejecuta Intruccion I/O")
                #lanza un alerta irqExistIO para avisar al kernel que el pcb ya salio de IO
                irqExistIo = IRQExitIO()
                self.irqManager.handle(irqExistIo, instruction.pcb)
                
class IRQIO:
    def execute(self,pcb,kernel,irqManager):
        pcb.incrementoPc()
        #llamar al proximo pcb
        kernel.schedulerNext()
        print("procesando IO con pcb " + str(pcb.pid)+"\n")
        print("el pc del pcb " + str(pcb.pid) +" es de " +str(pcb.pc)+"\n")


class IRQExitIO:
    
    def execute(self,pcb,kernel,irqManager):
        if not pcb.termino():
            print("IO devolvio el pcb al scheduler")
            kernel.agregarAlScheduler(pcb)
            
        else:
            # el pcb termino, entonces envia un alerta de kill
            irqKill = IRQKILL()
            irqManager.handle(irqKill,pcb)
            

class IRQKILL:    
    def execute(self,pcb,kernel,irqManager):
        #llamar al proximo pcb
        print(" el pcb con id " +str(pcb.pid) +" termino\n")
        kernel.schedulerNext()
        kernel.kill(pcb)
        
        
class IRQNEW:
    #Alerta para avisar que no hay pcb asignado a la cpu
    #como no existe pcb, al ser execute se pasa None
    def execute(self,pcb,kernel,irqManager):
        kernel.schedulerNext()
    

class IRQManager:
    def __init__(self, kernel):
        self.kernel = kernel
        

    def handle(self, irq, pcb):
        irq.execute(pcb,self.kernel,self)
        

        
     
#pcb = process control block
class PCB:
    def __init__(self, identificador, cantInst):
        self.pid = identificador
        self.pc = 0 #cantidad de instrucciones ejecutadas
        self.estado = "new"
        self.cantInst = cantInst
        #self.prioridad = prioridad

    def termino(self):
        return self.cantInst == self.pc

    def incrementoPc(self):
        self.pc = self.pc + 1



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
        print("el pcb con el id " +str(pcb.pid) +" esta en el scheduler\n ")
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
        print(" en el indice " +str(index) + " se guardo instruccion " +str(instruction) + " del pcb " +str(instruction.pcb.pid))
        self.celdas[index] = instruction
        
        
               
    def load(self,programa,pcb):
        block = self.mode.findBlockEmpty(programa. getCantInst())
        if block == None:
            print(" there is not enough place in memory")
            
        else:
            pcb.baseDirection = block.first # se le asigna la direccionBase
            index = block.first
            for instruction in programa.instrucciones:
                instruction.pcb = pcb
                self.addInstruction(index, instruction)
                index = index + 1
            
        
            print("se cargo el programa en memoria\n")
            
    def getInstruccion(self,pcb):
        #modificar esto para que lo haga la MMU
        #print(" pcb.baseDirection " +str(pcb.baseDirection) + " pc " +str(pcb.pc))
        direction = pcb.baseDirection + pcb.pc
        print("****la direccion retornada es " +str(direction))
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
    def __init__(self,instManager):
        self.instManager = instManager
        self.pcb = None
        
        
    def execute(self):
        self.instManager.evaluate(self)
    
    
class InstManagerCPU(): 
    def __init__(self,irqManager):
        self.irqManager = irqManager  
        
    def evaluate(self,instruccion):
        print("evaluando instruccion de cpu\n")
        pcb = instruccion.pcb
        pcb.incrementoPc()
        print(" el pc del pcb " + str(pcb.pid) +" es de " +str(pcb.pc))
        
        if pcb.termino():
            irqKill = IRQKILL()
            self.irqManager.handle(irqKill,pcb)

class InstManagerIO():
    def __init__(self,io,irqManager):
        self.io = io
        self.irqManager = irqManager
    
    def evaluate(self,instruccion):
        self.io.addInstruccion(instruccion) 
        pcb = instruccion.pcb
        #pcb.isIO = True #dato para el manager
        print("an instruction is added to the queue of isIO\n")
        #Lanzo un irq
        irqIO = IRQIO()
        self.irqManager.handle(irqIO, pcb)
        
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
        if blockBefore.size > size:
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
        block = self.typeFit.getBlock(self.blockFree,size)
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
    
        
        
        



#hacer los schedulers que faltan

firstFit = FirstFit()
continua = AsignacionContinua(firstFit)
memoria = Memory(continua,8)
cpu = CPU(memoria)
sh = SchedulerFifo(cpu)
disco = Disco()
k = Kernel(sh, disco,memoria)
#manager = Manager(k,cpu)
irqManager = IRQManager(k)
io = IO(irqManager)


managerCPU = InstManagerCPU(irqManager)
managerIO =  InstManagerIO(io,irqManager)

timer = Timer(cpu,irqManager) # le saque al timer el manager
timer.start()

i1 = Instruction(managerCPU)
i2 = Instruction(managerIO)
i3 = Instruction(managerCPU)
i4 = Instruction(managerIO)

i5 = Instruction(managerCPU)
i6 = Instruction(managerIO)
i7 = Instruction(managerCPU)
i8 = Instruction(managerIO)

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
