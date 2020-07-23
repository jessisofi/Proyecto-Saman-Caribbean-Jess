class Cliente:
    def __init__(self, nombre, dni, edad, discapacidad, habitaciones):
        self.nombre = nombre
        self.dni = dni
        self.edad = edad
        self.discapacidad = discapacidad
        self.habitaciones = habitaciones

    def acceso_cliente(self):
        print(f"Nombre: {self.nombre}")
        print(f"dni: {self.dni}")
        print(f"Edad: {self.edad}")
        print(f"Discapacidad: {self.discapacidad}")
        print(f"Habitaciones: {self.habitaciones}")


