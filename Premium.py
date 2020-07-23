from Piso import Piso

class Premium(Piso):

    name = 'Premium'
    
    def __init__(self, capacidad, referencia, precio, informacion):
        Piso.__init__(self, capacidad, referencia, precio)
        self.informacion = informacion

    def acceso_premium(self):
        print(f"Informacion: {self.informacion}")
