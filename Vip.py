from Piso import Piso

class Vip(Piso):
    
    name = 'VIP'

    def __init__(self, capacidad, referencia, precio, informacion):
        Piso.__init__(self, capacidad, referencia, precio)
        self.informacion = informacion

    def acceso_vip(self):
        print(f"Informacion: {self.informacion}")
