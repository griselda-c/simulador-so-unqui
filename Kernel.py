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
        
        
#manager deja de ser un thread       
class Manager():
    def __init__(self, kernel,cpu):
        #threading.Thread.__init__(self)
        self.kernel = kernel
        self.cpu = cpu
        
    def callNext(self):
        self.cpu.pcb = None
        self.kernel.schedulerNext()
        
    def addScheduler(self,pcb):
        self.kernel.agregarAlScheduler(pcb)

    def evaluar(self):     
        if cpu.existPcb():
            if cpu.pcb.termino():
                self.kernel.kill(cpu.pcb)
                print("termino\n")
                self.callNext()
            elif cpu.pcb.isIO:
                self.callNext() 
                print("salio por io\n")  
        
# si es de cpu se sigue procesando el mismo pcb hasta que termine       
                
class Timer(threading.Thread):
    def __init__(self, cpu,manager): #agregue un manager
        threading.Thread.__init__(self)
        self.cpu = cpu
        self.manager = manager
        
    def evaluar(self):
        instruction = self.cpu.fetch()
        if instruction != None:
            # va a buscar a memoria la instruccion
            instruction.execute() #ejecuta la instruccion
            self.manager.evaluar() # el manager avisa al kernel que paso con el pcb y pide proximo
            time.sleep(5)
        else:
            self.manager.callNext()

    def run(self):
        while True:
            self.evaluar()
            
                
class IO(threading.Thread):
    def __init__(self,manager):
        threading.Thread.__init__(self)
        self.cola = miFifo()
        self.manager = manager

    def addInstruccion(self,io):
        self.cola.addElement(io)
        
    def existInstruction(self):
        return self.cola.size() > 0
    
    def addScheduler(self,pcb):
        if not pcb.termino():
            print("IO devolvio el pcb al scheduler")
            self.manager.addScheduler(pcb)

    def run(self):
        while True:
            if self.existInstruction():
                instruction = self.cola.getElement()          
                pcb = instruction.pcb
                pcb.incrementoPc()
                print("procesando IO con pcb " + str(pcb.pid)+"\n")
                print("el pc del pcb " + str(pcb.pid) +" es de " +str(pcb.pc)+"\n")
                pcb.isIO = False #para evaluar proxima instruccion
                self.addScheduler(pcb)
                    #despues de evaluar debe volver al scheduler
        
     
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

    def getElement(self):
        #saque los semaforos
        if self.existElement():
            return self.ls.pop(0)
        

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
    def evaluate(self,instruccion):
        print("evaluando instruccion de cpu\n")
        pcb = instruccion.pcb
        pcb.incrementoPc()
        print("el pc es de " +str(pcb.pc))

class InstManagerIO():
    def __init__(self,io):
        self.io = io
    
    def evaluate(self,instruccion):
        self.io.addInstruccion(instruccion) 
        pcb = instruccion.pcb
        pcb.isIO = True #dato para el manager
        print("an instruction is added to the queue of isIO\n")
        



#hacer los schedulers que faltan


memoria = Memory()
cpu = CPU(memoria)
sh = SchedulerFifo(cpu)
disco = Disco()
k = Kernel(sh, disco,memoria)
manager = Manager(k,cpu)
io = IO(manager)

#manager.start() #cambie run por start

managerCPU = InstManagerCPU()
managerIO =  InstManagerIO(io)

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
timer = Timer(cpu,manager)
timer.start()
io.start()

