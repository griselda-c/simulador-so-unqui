'''
Created on 21/11/2013

@author: Griselda
'''

from WorstFit import *
from AsignacionContinua import *
from Block import *

worst = WorstFit()
AC = AsignacionContinua(worst)

AC.blockFree = [Block(0,8),Block(16,48),Block(52,58)]
# debieria elegir el bloque Bloque(16,48))

bloque = AC.findBlockEmpty(4)

print("("+str(bloque.first)+","+str(bloque.last)+")")
