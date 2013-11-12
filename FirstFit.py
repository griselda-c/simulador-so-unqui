

class FirstFit:
    def getBlock(self,blocks,size):
        for block in blocks:
            if block.size() >= size:
                print("block size " +str(block.size()))
                return block
        return None