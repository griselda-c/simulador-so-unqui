

class Marco:
    def __init__(self,direInicial, tamanio):
        self.celdas = {}
        self.direInicial = direInicial
        for index in range(0,tamanio):
			self.celdas[index] = None
        