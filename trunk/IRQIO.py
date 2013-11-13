'''
Created on 24/10/2013

@author: Griselda, Maricruz
'''

class IRQIO:
    def execute(self,pcb,kernel,irqManager):
        #llamar al proximo pcb
        kernel.schedulerNext()
