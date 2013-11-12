

class IRQNEW:
    #Alerta para avisar que no hay pcb asignado a la cpu
    #como no existe pcb, al ser execute se pasa None
    def execute(self,pcb,kernel,irqManager):
        kernel.schedulerNext()