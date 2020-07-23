from Piso import Piso

class Sencilla(Piso):
    
    name = 'Sencilla'

    def __init__(self,capacidad, referencia, precio, informacion):
        Piso.__init__(self, capacidad, referencia, precio)
        self.informacion = informacion

    def acceso_sencilla(self):
        print(f"Informacion: {self.informacion}")
