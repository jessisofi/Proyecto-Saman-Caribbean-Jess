class Producto:
    def __init__(self, nombre, clasificacion, precio):
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.precio = precio

    def iva_producto(self, precio):
        self.precio += (self.precio * 0.16)

    def acceso_producto(self):
        print(f"Nombre: {self.nombre}")
        print(f"Clasificacion: {self.clasificacion}")
        print(f"Precio: {self.precio}")