
import threading
from threading import Semaphore

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