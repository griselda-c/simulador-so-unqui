from Disco import *
from CPU import *
from miFifo import *
from IO import *
from FirstFit import *
from Paginacion import *
from Memory import *
from SchedulerFifo import *
from Kernel import *
from IRQManager import *
from InstManagerCPU import *
from InstManagerIO import *
from Timer import *
from Instruction import *
from Program import *
from MMU_paginacion import *
from PLP import *
from WorstFit import *
from RoundRobin import *
import time
from Asignador import *

firstFit = FirstFit()
worstFit = WorstFit()
disco = Disco()

pag = Paginacion(disco,4)#saque el mmu
asignador = Asignador(pag)
memoria = Memory(12,asignador)
#mmu = MMU_paginacion(memoria)
cpu = CPU(asignador)
sh = SchedulerFifo(cpu)
robin = RoundRobin(cpu)
plp = PLP(sh,memoria,disco)
k = Kernel(sh, disco,memoria,plp)
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
i17 = Instruction(managerIO,"instruccion de IO ejecutandose")

p = Program("prog1")
p.addInstruction(i1) #0
p.addInstruction(i2) #1
p.addInstruction(i3) #2
p.addInstruction(i4) #3
disco.addProgram(p)
i9 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
p2 = Program("prog2")
p2.addInstruction(i5) #4
p2.addInstruction(i6) #5
p2.addInstruction(i7) #6
p2.addInstruction(i8) #7
p2.addInstruction(i9) #7
disco.addProgram(p2)

k.run("prog1") #cambie start por run poque todavia no estamos seguras que el kernel sea un Thread
io.start()
k.run("prog2")



i10 = Instruction(managerIO,"instruccion de IO ejecutandose")
i11 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i12 = Instruction(managerIO,"instruccion de IO ejecutandose")

i13 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i14 = Instruction(managerIO,"instruccion de IO ejecutandose")
i15 = Instruction(managerCPU,"instruccion de cpu ejecutandose")
i16 = Instruction(managerIO,"instruccion de IO ejecutandose")


p3 = Program("prog3")
p3.addInstruction(i9) #
p3.addInstruction(i10) #10
p3.addInstruction(i11) 
p3.addInstruction(i12) 
disco.addProgram(p3)

k.run("prog3")

time.sleep(5)

p4 = Program("prog4")
p4.addInstruction(i13) #4
p4.addInstruction(i14) #5
p4.addInstruction(i15) #6
p4.addInstruction(i16) #7
disco.addProgram(p4)

k.run("prog4")

