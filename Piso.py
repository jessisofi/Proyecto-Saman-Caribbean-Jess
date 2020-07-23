class Piso:
    def __init__(self, capacidad, referencia, precio):
        self.capacidad = capacidad
        self.referencia = referencia
        self.precio = precio
        
    def acceso_piso(self):
        print(f"Capacidad: {self.capacidad}")
        print(f"Referencia: {self.referencia}")
        print(f"Precio: {self.precio}")
        print()