

class IRQNEW:
    #Alerta para avisar que no hay pcb asignado a la cpu
    def execute(self,pcb,kernel):
        kernel.schedulerNext()