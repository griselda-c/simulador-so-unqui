'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

import threading
from threading import Semaphore
import time
import random

class Kernel():
    
    def __init__(self,scheduler, hd, memory):
        #threading.Thread.__init__(self)
        self.pcbTable = []
        self.scheduler = scheduler
        #self.timer = timer
        #self.io = io
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
        self.pcbTable.append(pcb)
        self.loadMemory(programa, pcb) 
        self.agregarAlScheduler(pcb)

    def agregarAlScheduler(self, pcb):
        #if not self.scheluder.isEmpty():  
        self.scheduler.addReady(pcb)

    def getPId(self):
        self.semaphore.acquire()
        cont = self.cont + 1
        self.semaphore.release()
        return cont
        
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
            instruction = self.memoria.getInstruccion()
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
        #self.manager = manager
        
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
        self.isIO= False
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
    def __init__(self):
    #a validar
        self.celdas = [ ]

    def cargoPrograma(self, programa):
        if self.hayEspacio():
            #inicio = buscoCeldaLibre()
            #agregoPrograma(inicio, programa)
            print("hay espacio")
            
    #METODO SOLO DE PRUEBA DEBE SE MODIFICADO      
    def addInstruction(self,instruction):
        self.celdas.append(instruction)
               
        
    #METODO SOLO DE PRUEBA DEBE SER MODIFICADO
    def load(self,programa,pcb):
        for inst in programa.instrucciones:
            inst.pcb = pcb   #ahora cada instruccion sabe a que pcb pertenece
            self.addInstruction(inst)
            
        print("se cargo el programa en memoria\n")
            
            
    def returnNumeroAleatorio(self):
        index = random.randint(0,3)
        return index
      
    #def getInstruccion(self,pc,inicio)  

    def getInstruccion(self):
        index = self.returnNumeroAleatorio()
        instruction = self.celdas[index]
        return instruction
       

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
        print("el pc es de " +str(pcb.pc))
        
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
        
        



#hacer los schedulers que faltan


memoria = Memory()
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

p = Program("prog1")
p.addInstruction(i1)
p.addInstruction(i2)
p.addInstruction(i3)
p.addInstruction(i4)

k.run(p) #cambie start por run poque todavia no estamos seguras que el kernel sea un Thread
io.start()

