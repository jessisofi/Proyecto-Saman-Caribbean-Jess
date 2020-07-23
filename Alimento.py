from Producto import Producto

class Alimento(Producto):
    def __init__(self, nombre, clasificacion, precio, tipo):
        Producto.__init__(self, nombre, clasificacion, precio)
        self.tipo = tipo

    def acceso_alimento(self):
        print(f"Nombre: {self.nombre}")
        print(f"Clasificacion: {self.clasificacion}")
        print(f"Precio: {self.precio}")
        print(f"Tipo: {self.tipo}")
