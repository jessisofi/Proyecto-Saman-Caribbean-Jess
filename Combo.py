from Producto import Producto
class Combo(Producto):
    def __init__(self, nombre, clasificacion, precio, cantidad, productos):
        Producto.__init__(self, nombre, clasificacion, precio)
        self.cantidad = cantidad
        self.productos = productos
    
    def acceso_combo(self):
        print(f"Nombre: {self.nombre}")
        print(f"Clasificacion: {self.clasificacion}")
        print(f"Precio: {self.precio}")
        print(f"Cantidad: {self.cantidad}")
        print(f"Productos: {self.productos}")
