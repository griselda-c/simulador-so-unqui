
class IRQKILL:    
    def execute(self,pcb,kernel,irqManager):
        kernel.kill(pcb)
