from Producto import Producto

class Bebida(Producto):
    def __init__(self, nombre, clasificacion, precio, tamaño):
        Producto.__init__(self, nombre, clasificacion, precio)
        self.tamaño = tamaño

    def acceso_bebida(self):
        print(f"Nombre: {self.nombre}")
        print(f"Clasificacion: {self.clasificacion}")
        print(f"Precio: {self.precio}")
        print(f"Tamaño: {self.tamaño}")
