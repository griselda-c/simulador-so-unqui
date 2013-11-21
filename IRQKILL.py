
class IRQKILL:    
    def execute(self,pcb,kernel):
        kernel.kill(pcb)
        
