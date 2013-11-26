from AsignacionContinua import *
from Compactador import *
from BestFit import *
        

    
        
    
    
best = BestFit()
AC = AsignacionContinua(best)
AC.blockFree = [Block(9,9),Block(16,18),Block(37,40)] # tamanio 1 , 3 ,  4
AC.blockBusy = [Block(0,8),Block(10,15),Block(19,25),Block(26,36)]
# que hay que hacer, unir todos los huecos blancos, o unir solo lo que necesito
#uno todos los libres
AC.compactacion()