
from Disco import *
from CPU import *
from miFifo import *
from IO import *
from FirstFit import *
from AsignacionContinua import *
from Memory import *
from SchedulerFifo import *
from Kernel import *
from IRQManager import *
from InstManagerCPU import *
from InstManagerIO import *
from Timer import *
from Instruction import *
from Program import *

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
