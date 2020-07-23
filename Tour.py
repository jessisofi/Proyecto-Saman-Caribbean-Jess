class Tour:
    def __init__(self, tour, precio, cantidad, hora, cupos):
        self.tour = tour
        self.precio = precio
        self.cantidad = cantidad
        self.hora = hora
        self.cupos = cupos

    def acceso_tour(self):
        print(f"Nombre del Tour: {self.tour}")
        print(f"Precio: {self.precio}")
        print(f"Cantidad de personas: {self.cantidad}")
        print(f"Hora del tour: {self.hora}")
        print(f"Cupos disponibles: {self.cupos}")