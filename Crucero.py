class Crucero:
    def __init__(self,name,route,departure,cost,rooms,capacity,sells):
        self.name = name
        self.route = route
        self.departure = departure
        self.cost = cost
        self.rooms = rooms
        self.capacity = capacity
        self.sells = sells

    def acceso_crucero(self):
        print()
        print("--------------------")
        print(f"Nombre: {self.name}")
        print(f"Ruta: {self.route}")
        print(f"Salida: {self.departure}")
        for piso in self.rooms:
            print(f'\n {piso.name}')
            piso.acceso_piso()
        print("--------------------")