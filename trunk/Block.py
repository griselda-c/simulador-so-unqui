

class Block:
    def __init__(self,first, last):
        self.first = first
        self.last = last
        
    def size(self):
        return (self.last - self.first ) + 1