import requests
from Producto import Producto
from Bebida import Bebida
from Alimento import Alimento
from Sencilla import Sencilla
from Premium import Premium
from Vip import Vip
from Tour import Tour
from Crucero import Crucero
from Cliente import Cliente
from Combo import Combo
ocupacion = {}
clientes = []

#------MODULO 1: GESTION DE CRUCEROS------
#En este modulo se desarrollaron fuciones que permiten ver a los clientes los cruceros disponibles usando la informacion de la API

def crear_habitacion(crucero):
    habitaciones = []
    # Simple
    sencilla = Sencilla(crucero['capacity']['simple'],crucero['rooms']['simple'], crucero['cost']['simple'], 'Sin ventana' )
    habitaciones.append(sencilla)
    # Premium
    premium = Premium(crucero['capacity']['premium'],crucero['rooms']['simple'], crucero['cost']['premium'], 'Con ventana' )
    habitaciones.append(premium)
    # Vip
    vip = Vip(crucero['capacity']['vip'],crucero['rooms']['vip'], crucero['cost']['vip'], 'Con Balcon' )
    habitaciones.append(vip)
    return habitaciones

def crear_cruceros(cruceros):
    print('Cargando datos de API...')
    datos = api()
    for crucero in datos:
        rooms = crear_habitacion(crucero)
        name = crucero["name"]
        route = crucero["route"]
        departure = crucero["departure"]
        cost = crucero["cost"]
        capacity = crucero["capacity"]
        sells = crucero["sells"]
        barco = Crucero(name, route, departure, cost, rooms, capacity,sells)
        cruceros.append(barco)
    return cruceros

def ver_cruceros(cruceros):
    for crucero in cruceros:
        crucero.acceso_crucero()

#----MODULO 2: GESTION DE HABITACIONES----
#En este modulo se desarrollaron funciones para consultar habitaciones disponibles, comprar habitaciones, ocuparlas y desocuparlas.
def por_destino(cruceros):
    rutas = set()
    for crucero in cruceros:
        for ruta in crucero.route:
            rutas.add(ruta)
    rutas = list(rutas)
    print('\n Rutas 🏖️: ')
    for i, ruta in enumerate(rutas):
        print(f'{i+1} {ruta}')
    while True:
        try:
            ruta = int(input('Selecciona la ruta (el número): '))
            if ruta > len(rutas) or ruta < 1:
                raise Exception
            break
        except:
            print('Error, ingrese un número valido')
    ruta = rutas[ruta - 1]

    print(f'\nRuta seleccionada {ruta}! \n')
    print('Seleccione el crucero: ')

    contador_cruceros = []
    for i, crucero in enumerate(cruceros):
        if ruta in crucero.route:
            print(f'{i+1} {crucero.name}')
            contador_cruceros.append(i+1)
            
    while True:
        try:
            crucero = int(input('Selecciona el crucero (el número): '))
            if crucero not in contador_cruceros:
                raise Exception('Error')
            break
        except:
            print('Error, ingrese un número valido')
    crucero = cruceros[crucero - 1] 
    print(f'\nCrucero seleccionado {crucero.name} 🚢 !! \n')   
    return crucero    

def por_barco(cruceros):
    contador_cruceros = []
    for i, crucero in enumerate(cruceros):
        print(f'{i+1} {crucero.name}')
        contador_cruceros.append(i+1)
            
    while True:
        try:
            crucero = int(input('Selecciona el crucero (el número): '))
            if crucero not in contador_cruceros:
                raise Exception('Error')
            break
        except:
            print('Error, ingrese un número valido')
    crucero = cruceros[crucero - 1] 
    print(f'\nCrucero seleccionado {crucero.name} 🚢 !! \n')   
    return crucero

def validar_ocupacion(crucero, letra, numero, tipo_hab):
    crucero_ocupacion = ocupacion.get(crucero.name)
    if crucero_ocupacion:
        piso_ocupacion = crucero_ocupacion.get(crucero.rooms[tipo_hab-1].name)
        if piso_ocupacion:
            letra_ocupacion = piso_ocupacion.get(letra)
            if letra_ocupacion:
                numeros_reservados = letra_ocupacion
                if numero in numeros_reservados:
                    return 'X'      
    return '0'

def generar_ocupacion(crucero,letra, numero, tipo_hab):
    crucero_ocupacion = ocupacion.get(crucero.name)
    if crucero_ocupacion:
        piso_ocupacion = crucero_ocupacion.get(crucero.rooms[tipo_hab-1].name)
        if piso_ocupacion:
            letra_ocupacion = piso_ocupacion.get(letra)
            if letra_ocupacion:
                numeros_reservados = letra_ocupacion
                if numero not in numeros_reservados:
                    numeros_reservados.append(numero)
                    ocupacion[crucero.name] = {crucero.rooms[tipo_hab-1].name: {letra: numeros_reservados} }
            else:
                ocupacion[crucero.name][crucero.rooms[tipo_hab-1].name][letra] = [numero]
        else:
            ocupacion[crucero.name][crucero.rooms[tipo_hab-1].name] = {letra: [numero]} 
    else:
        ocupacion[crucero.name] = {crucero.rooms[tipo_hab-1].name: {letra: [numero]} }

def generar_desocupacion(crucero,letra, numero, tipo_hab):
    print(ocupacion[crucero.name][crucero.rooms[tipo_hab-1].name][letra])
    try:
        del ocupacion[crucero.name][crucero.rooms[tipo_hab-1].name][letra]
        print(ocupacion)
        print('Habitación desocupada!')
    except:
        print('No se encuentra la habitación')


def representar_piso(crucero,f, c, tipo_hab):
    print(f' ------------------Mapa del Piso----------------')
    letras = ['a', 'b', 'c', 'd','e','f','g','h','i','j','k','l','m']

    numeros = [i for i in range(c + 1)]

    numeros_ref = []
    for n in numeros:
        print(f"{n}", end=" | ", flush=True)
        numeros_ref.append(n)

    print() 
    letras_ref = []
    for i in range(f):
        print(letras[i], end=" | ", flush=True)
        letras_ref.append(letras[i])
        for j in range(c):
            print(validar_ocupacion(crucero, letras[i], j+1, tipo_hab), end=" | ")
        print()
    print(f' --------------------------------------------')
    print('\n')

    while True:
        try:
            letra = input('Ingrese el pasillo (letra): ')
            numero = int(input('Ingrese la columna (número): '))
            if letra not in letras_ref or numero not in numeros_ref:
                raise Exception('Ingrese datos del mapa')
            if validar_ocupacion(crucero, letra, numero, tipo_hab) == 'X':
                print('Habitación ocupada!')
                raise Exception
            else:
                generar_ocupacion(crucero, letra, numero, tipo_hab)
                with open('ocupaccion.txt','a') as f:
                    f.write(ocupacion)
            break
        except:
            print('Error ingrese datos validos')
    return letra, numero

def formulario(crucero,compra,i):
    nombre = input(f'Ingrese el nombre del pasajero {i}: ')
    while True:
        try:
            dni =  int(input(f'Ingrese el documento del pasajero {i}: '))
            edad = int(input(f'Ingrese la edad del pasajero {i}: '))
            break
        except:
            print('Error, ingrese un valor valido')
    discapacidad = input(f'El pasajero {i} posee discapacidad? (1)Si (2)No: ')

    if compra['tipo_hab'] == '1':
        hab = 'simple'
    elif compra['tipo_hab'] == '2':
        hab = 'premium'
    else:
        hab = 'vip'
    
    print(crucero.cost)
    costo  = crucero.cost[hab]

    subtotal = costo

    # Descuentos
    descuento = 0
    if is_prime(dni):
        descuento = .1
        costo = costo - costo * descuento
    elif abundante(dni):
        descuento = .15
        costo = costo - costo * descuento
    if edad > 65 and hab == 'simple':
        upgrade = input('Desea hacer un upgrade a premium? (1)Si (2)No: ')
        if upgrade:
            compra['tipo_hab'] = '2'
    if discapacidad == '1':
        descuento = .30
        costo = costo - costo * descuento
    
    impuestos = costo * .16

    costo += impuestos

    cliente = {}
    cliente['nombre'] = nombre
    cliente['edad'] = edad
    cliente['dni'] = dni
    cliente['discapacidad'] = discapacidad == '1'
    cliente['costo'] = costo
    cliente['subtotal'] = subtotal
    cliente['descuento'] = descuento
    cliente['impuestos'] = impuestos
    cliente['hab'] = hab
    cliente['crucero']: compra['crucero']

    return cliente, compra

def manejar_compra(compra,crucero):
    print(compra)
    print(compra['cantidad_personas'])
    for i in range(compra['cantidad_personas']):
        cliente, compra = formulario(crucero,compra, i+1)
        clientes.append(cliente)
    
    for cliente in clientes:
        print(f''' 
            RESUMEN DE COMPRA:
            Crucero: {compra['crucero']}
            Habitación:  {cliente['hab']}, {compra['habitacion']}
            Nombre: {cliente['nombre']}
            Edad: {cliente['edad']}
            Dni: {cliente['dni']}
            Discapacidad: {cliente['discapacidad']}
            Subtotal: ${cliente['subtotal']}
            Descuentos: {cliente['descuento']*100}%
            Impuestos: ${cliente['impuestos']}
            Costo: ${cliente['costo']}
        ''')
    
def manejo_habitaciones(crucero):

    while True:
        try:
            cantidad_personas = int(input('Cantidad de pasajeros: '))
            if cantidad_personas < 1:
                raise Exception('Error, debe haber al menos 1 pasajero')
            break
        except:
            print('Error, Ingrese solo números')
    
    while True:
        try:    
            tipo_hab = int(input('''¿Qué tipo de habitacion deseas?
                            1. Simple
                            2. Premium
                            3. VIP
                        > '''))
            if tipo_hab < 1 or tipo_hab > 3:
                raise Exception('Error seleccione una opcion valida ')
            break
        except:
            print('Error')
    
    pasillos = crucero.rooms[tipo_hab-1].referencia[0] 
    habitaciones = crucero.rooms[tipo_hab-1].referencia[1] 
    letra, numero = representar_piso(crucero,pasillos,habitaciones,tipo_hab)

    print(f'''\nTu opción es la siguiente:
    Barco: {crucero.name}
    Habitación: {letra, numero}
    ''')
    compra = {}
    compra['crucero'] = crucero.name
    compra['habitacion'] = letra, numero
    compra['tipo_hab'] = tipo_hab
    compra['cantidad_personas'] = cantidad_personas
    return compra

def gestion_habitacion(cruceros):
    opcion = input(''' Bienvenido a la compra de Tickets de los Jessi Cruise de Saman Caribbean:
        1. Por destino
        2. Por barco
        3. Desocupar Habitación
        4. Buscar Habitación
        4. Salir
    > ''')
    if opcion == '1':
       crucero = por_destino(cruceros)
    elif opcion == '2':
        crucero = por_barco(cruceros)
    elif opcion == '3':
        desocupar_habitacion(cruceros)
        return 0
    elif opcion == '4':
        buscar_habitacion(cruceros)
        return 0
    else:
        return 0

    compra = manejo_habitaciones(crucero)

    manejar_compra(compra, crucero)

def desocupar_habitacion(cruceros):
    contador_cruceros = []
    for i, crucero in enumerate(cruceros):
        print(f'{i+1} {crucero.name}')
        contador_cruceros.append(i+1)
            
    while True:
        try:
            crucero = int(input('Selecciona el crucero (el número): '))
            if crucero not in contador_cruceros:
                raise Exception('Error')
            break
        except:
            print('Error, ingrese un número valido')
    crucero = cruceros[crucero - 1] 
    
    while True:
        try:
            tipo_hab = int(input('Ingresa el tipo de habitación: (1)Simple, (2)Premium, (3)VIP: '))
            letra = input('Ingresa la letra de la habitación: ')
            numero = int(input('Ingresa el número de la habitación: '))
            break
        except:
            print('Ingrese un dato valido')
    
    generar_desocupacion(crucero, letra, numero, tipo_hab)

def buscar_habitacion(cruceros):
    contador_cruceros = []
    for i, crucero in enumerate(cruceros):
        print(f'{i+1} {crucero.name}')
        contador_cruceros.append(i+1)
            
    while True:
        try:
            crucero = int(input('Selecciona el crucero (el número): '))
            if crucero not in contador_cruceros:
                raise Exception('Error')
            break
        except:
            print('Error, ingrese un número valido')
    crucero = cruceros[crucero - 1] 
    
    print('Buscando...')

#Representacion para cada piso del crucero
def habitaciones_disponibles(cruceros):
    for crucero in cruceros:
        print(crucero['name'])

def is_prime(num):
    if num == 1:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, num):
            if num % i == 0:
                return False
        return True            

def abundante(n):
    if n<0:
        return False
    count =  1
    suma = 0
    while (count<n):
        if (n%count==0):
            suma+=count
        count = count + 1
    if (suma>(n)):
        return True
    else:
        return False

#------MODULO 3: VENTA DE TOURS------
def seleccion_barco_tour(cruceros, clientes):
    while True:
        print("Bienvenido a los tours del crucero")
        try:
            opcion = int(input("""Seleccione el barco en el que se encuentra para acceder a los tour:
            1. El Dios de los Mares
            2. La Reina Isabel
            3. El Libertador del Océano
            4. Sabas Nieves
            5. Salir
            """))
            if opcion == 1:
                print("1")
            elif opcion == 2:
                print("1")
            elif opcion == 3:
                print("1")
            elif opcion == 4:
                print("1")
            elif opcion == 5:
                print("Hasta luego")
            else:
                raise Exception
            break
        except:
            print("Usted ha ingresado algun dato inválido")
    return venta_tours(clientes,cruceros)

def descuentos_tour_puerto(tour, cantidad,posicion):
    descuento = 0
    precio = 30
    precio_total = 0
    if cantidad >2:
        precio = 30
        if posicion == 3:
            descuento = (precio*0.1)
            precio_total = precio - descuento
        elif posicion == 4:
            descuento = (precio*0.1)
            precio_total = precio - descuento
    else:
        print("No obtiene descuento")

def tour_puerto(clientes):
    cupo_total_puerto = 10
    cupo_puerto = []
    posicion = 0
    limite = 0
    precio = 30
    precio_total = 0
    while True:
        try:
            nombre = input("Ingrese su nombre: ")
            cantidad = int(input("Indique la cantidad de personas que van a ir al tour: "))
            if cantidad >4:
                print("Lo sentimos no puede ingresar al tour, maximo 4 personas por grupo.")
            elif cantidad <4 and cantidad >1:
                limite = cupo_total_puerto - cantidad 
                cupo_puerto.append(limite)
            else:
                raise Exception
                break
        except:
            print("Error. Usted ha ingresado algun dato invalido")
    precio_total = precio * cantidad 
    print(f"El cliente {nombre} ha comprado {cantidad} de entradas")

def tour_trotar(clientes):
    limite = 0
    cupo_trotar = []
    while True:
        try:
            nombre = input("Ingrese su nombre: ")
            cantidad = int(input("Indique la cantidad de personas que van a ir al tour: "))
            if cantidad >0:
                limite += cantidad
                cupo_trotar.append(limite)
            else:
                raise Exception
                break
        except:
            print("Error. Usted ha ingresado algun dato invalido")
    print(f"El cliente {nombre} se ha anotado en el tour de trotar que es totalmente gratuito")

def tour_degustacion(clientes):
    cupo_total_degustacion = 100
    cupo_degustacion = []
    posicion = 0
    limite = 0
    precio = 100
    precio_total = 0
    while True:
        try:
            nombre = input("Ingrese su nombre: ")
            cantidad = int(input("Indique la cantidad de personas que van a ir al tour: "))
            if cantidad >4:
                print("Lo sentimos no puede ingresar al tour, maximo 4 personas por grupo.")
            elif cantidad <4 and cantidad >1:
                limite = cupo_total_degustacion - cantidad 
                cupo_degustacion.append(limite)
            else:
                raise Exception
                break
        except:
            print("Error. Usted ha ingresado algun dato invalido")
    precio_total = precio * cantidad 
    print(f"El cliente {nombre} ha comprado {cantidad} de entradas")

def tour_visita(clientes):
    cupo_total_visita = 15
    cupo_visita = []
    posicion = 0
    limite = 0
    precio = 40
    precio_total = 0
    while True:
        try:
            nombre = input("Ingrese su nombre: ")
            cantidad = int(input("Indique la cantidad de personas que van a ir al tour: "))
            if cantidad >4:
                print("Lo sentimos no puede ingresar al tour, maximo 4 personas por grupo.")
            elif cantidad <4 and cantidad >1:
                limite = cupo_total_visita - cantidad 
                cupo_visita.append(limite)
            else:
                raise Exception
                break
        except:
            print("Error. Usted ha ingresado algun dato invalido")
    precio_total = precio * cantidad 
    print(f"El cliente {nombre} ha comprado {cantidad} de entradas")


def venta_tours(clientes,cruceros):
    while True:
        try:
            dni = int(input("🛳 Bienvenidos a los tours que ofrece Saman Caribbean, por favor ingrese su dni para poder acceder: "))
            #for tours in crucero.tours:
                #print(tours.acceso_tour())
            opcion = input('''
            🛳 Bienvenidos a los tours que ofrece el crucero ¿Cual tour desea comprar?:
            1. Tour en el puerto
            2. Degustación de comida local
            3. Trotar por el pueblo/ciudad
            4. Visita lugares historicos
            5. Salir
            >  ''')
            if opcion == "1":
                tour_puerto(clientes)
            elif opcion == "2":
                tour_degustacion(clientes)
            elif opcion == "3":
                tour_trotar(clientes)
            elif opcion == "4":
                print("Visita lugares historicos")
            elif opcion == "5":
                print("Hasta luego")
                break
            else:
                raise Exception
        except:
            print('Error')


# ---MODULO 4: GESTION DE RESTAURANTE----
#Funciones que permiten administrar el restaurante 
def seleccion_barco_restaurante(cruceros):
    while True:
        print("Bienvenido al restaurante")
        try:
            opcion = int(input("""Seleccione el barco en el que se encuentra para acceder al restaurante:
            1. El Dios de los Mares
            2. La Reina Isabel
            3. El Libertador del Océano
            4. Sabas Nieves
            5. Salir
            """))
            if opcion == 1:
                menu = []
                crucero = cruceros[opcion-1]
                menu = restaurante(menu)
                crucero.restaurante.append(menu)
            elif opcion == 2:
                menu = []
                crucero = cruceros[opcion-1]
                menu = restaurante(menu)
                crucero.restaurante.append(menu)
            elif opcion == 3:
                menu = []
                crucero = cruceros[opcion-1]
                menu = restaurante(menu)
                crucero.restaurante.append(menu)
            elif opcion == 4:
                menu = []
                crucero = cruceros[opcion-1]
                menu = restaurante(menu)
                crucero.restaurante.append(menu)
            elif opcion == 5:
                print("Hasta luego")
                break
            else:
                raise Exception
        except:
            print("Usted ha ingresado algun dato inválido")



#1. Agregar producto al menu del restaurante
def agregar_alimento(menu):
    while True:
        try:
            nombre = input("Ingrese el nombre del alimento: ")
            precio = float(input("Ingrese el precio del producto: $"))
            tipo = input("""Indique si su producto es de 
            1. Empaque 
            2. Preparacion 
            """)
            if tipo == "1":
                print("empaque")
            elif tipo == "2":
                print("preparacion")
            else:
                raise Exception
            producto = Alimento(nombre, precio, tipo)
            break
        except:
            print("Usted ha ingresado algún dato inválido. Por favor inténtelo de nuevo. Indique correctamente el tipo de producto")
    menu.append(producto)
    print("Su producto ha sido registrado exitosamente")
    return restaurante(menu)

def agregar_bebida(menu):
    while True:
        try:
            nombre = input("Ingrese el nombre del alimento: ")
            precio = float(input("Ingrese el precio del producto: $")) 
            tamaño = input("""
            Indique si su producto es 
            1. Pequeño
            2. Mediano
            3. Grande
            """)
            producto = Bebida(nombre, precio, tamaño)
            if tamaño == "1":
                producto.tamaño = "pequeño"
            elif tamaño == "2":
                producto.tamaño = "mediano"
            elif tamaño == "3":
                producto.tamaño = "grande"
            else:
                raise Exception
            break
        except:
            print("Usted ha ingresado algún dato inválido. Por favor inténtelo de nuevo. Indique correctamente el tipo de producto")
    menu.append(producto)
    print("Su producto ha sido registrado exitosamente")
    return restaurante(menu)

#2. Eliminar producto del menu del restaurante
def eliminar_producto(menu):
    nombre = input("Indique el nombre del producto que desea eliminar: ")
    for producto in menu:
        if producto.nombre == nombre:
            menu.remove(producto)
            print("El producto ha sido eliminado correctamente")
        elif producto not in menu: 
            print("No se puede eliminar ese producto del menu, ya que no existe")
    return restaurante(menu)

#3. Modificar producto del menu del restaurante
def modificar_alimento(menu):
    nombre = input("Ingrese el nombre del alimento que desea modificar: ")
    for producto in menu:
        if producto.nombre == nombre:
            while True:
                try:
                    opcion = input("""
                    Modificar: 
                    1. Nombre 
                    2. Precio 
                    3. tipo
                    4. Salir
                    """)
                    if opcion == "1":
                        nombre = input(
                            "Ingrese el nuevo nombre del alimento: ")
                        producto.nombre = nombre
                    elif opcion == "2":
                        precio = float(input("Ingrese el nuevo precio: "))
                        producto.precio = precio
                        raise Exception
                    elif opcion == "3":
                        tipo = input("""
                        Ingrese el nuevo modo:
                        1. Preparación
                        2. Empaque 
                        """)
                        if tipo == "1":
                            producto.tipo = "preparación"
                        elif tipo == "2":
                            producto.tipo = "empaque"
                        else:
                            raise Exception
                    elif opcion == "4":
                        print("Hasta luego")
                    else:
                        raise Exception
                    break
                except:
                    print("Error intente de nuevo, Indique correctamente lo que desea modificar")
            print("Alimento modificado exitosamente!")
        else:
            if not producto(menu):
                print("No se puede modificar ese alimento ya que no existe")
    return restaurante(menu)


def modificar_bebida(menu):
    nombre = input("Ingrese el nombre de la bebida que desea modificar: ")
    for producto in menu:
        if producto.nombre == nombre:
            while True:
                try:
                    opcion = input("""
                    Indique lo que quisiera modificar: 
                    1. Nombre 
                    2. Precio 
                    3. Tamaño
                    4. Salir
                    """)
                    if opcion == "1":
                        nombre = input(
                            "Ingrese el nuevo nombre de la bebida: ")
                        producto.nombre = nombre
                    elif opcion == "2":
                        precio = float(input("Ingrese el nuevo precio: "))
                        producto.precio = precio
                        raise Exception
                    elif opcion == "3":
                        tamaño = input("""
                        Indique el nuevo tamaño de su producto 
                        1. Pequeño
                        2. Mediano
                        3. Grande
                        """)
                        if tamaño == "1":
                            producto.tamaño = "pequeño"
                        elif tamaño == "2":
                            producto.tamaño = "mediano"
                        elif tamaño == "3":
                            producto.tamaño = "grande"
                        else:
                            print("El tamaño de la bebida es incorrecto")
                    elif opcion == "4":
                        print("Hasta luego")
                    break
                except:
                    print("Error intente de nuevo, Indique correctamente lo que desea modificar")
            print("Bebida modificada exitosamente!")
    return restaurante(menu)


#4. Agregar combo al menu del restaurante
def agregar_combo(menu):
    while True:
        try:
            nombre = input("Indique el nombre del combo: ")
            cantidad_productos_combo = int(input("Indique la cantidad de productos que tendrá el combo (minimo 2):"))
            if cantidad_productos_combo < 2:
                print("Error. El combo debe contener minimo 2 productos")
            precio_combo = float(input("Indique el precio del combo: $"))
            break
        except:
            print("Error intente de nuevo")
    print("Su combo ha sido registrado exitosamente")
    return restaurante(menu)

#5. Eliminar combo del menu
def eliminar_combo(menu):
    nombre = input("Ingrese el nombre del combo que desea eliminar: ")
    for combo in menu:
        if combo.nombre == nombre:
            menu.remove(combo)
            print("El combo ha sido eliminado correctamente")
        elif combo not in menu:
            print("No se puede eliminar ese combo ya que no existe")
    return restaurante(menu)

#6. Buscador de productos del restaurante por nombre o rango
#En construccion
def buscar_producto(menu):
    while True:
        buscador_producto = input("""
        ¿Desea buscar su producto por:
        1. Nombre  
        2. Rango de precios
         """)
        if buscador_producto == "1":
            print("Buscador de producto por nombre")
        elif buscador_producto == "2":
            producto_rango = input("""
            ¿De que rango de precios desea buscar el producto?: 
            1. 0$ - 25$
            2. 25$ - 50$
            3. 50$ - 75$ 
            """)
            if producto_rango == "1":
                print("0$ - 25$")
            elif producto_rango == "2":
                print("25$ - 50$")
            elif producto_rango == "3":
                print("50$ - 75$ ")
            else:
                print("Error, usted ha ingresado algun dato invalido")
        else:
            print("Error, usted ha ingresado algun dato invalido")
        break
    return restaurante(menu)

#  def buscar(menu, nombre):
#     for producto in menu:
#         if producto.nombre == nombre:
#             return producto
#     print("El producto no existe")

                    
#7. Buscador de combos del restaurante por nombre o rango
#En construccion
def buscar_combo(menu):
    while True:
        buscador_combo = input("""
        ¿Desea buscar su producto por:
        1. Nombre  
        2. Rango de precios
         """)
        if buscador_combo == "1":
            print("Buscar combo por nombre")
        elif buscador_combo == "2":
            combo_rango = input("""
            ¿De que rango de precios desea buscar el combo?: 
            1. 0$ - 25$
            2. 25$ - 50$
            3. 50$ - 75$ 
            """)
            if combo_rango == "1":
                print("0$ - 25$")
            elif combo_rango == "2":
                print("25$ - 50$")
            elif combo_rango == "3":
                print("50$ - 75$ ")
            else:
                print("Error, usted ha ingresado algun dato invalido")
        else:
            print("Error, usted ha ingresado algun dato invalido")
        break
    return restaurante(menu)

#Menu principal restaurante
def restaurante(menu):
    while True:
        opcion = input('''
        🛳 Bienvenidos al restaurente del crucero ¿Qué desea realizar?:
        1. Agregar plato
        2. Eliminar producto del menu
        3. Modificar producto del menu
        4. Agregar combo
        5. Eliminar combo
        6. Buscar productos por nombre o rango de precio
        7. Buscar combos por nombre o rango de precio
        8. Salir
        >  ''')
        if opcion == "1":
            clasificacion = input("""Indique si el producto es: 
            1. Alimento
            2. Bebida
            """)
            if clasificacion == "1":
                agregar_alimento(menu)
            elif clasificacion == "2":
                agregar_bebida(menu)
            else:
                print("Usted ha ingresado algún dato inválido, por favor inténtelo de nuevo")
        elif opcion == "2":
            eliminar_producto(menu)
        elif opcion == "3":
            opcion = input("""
            Desea modificar:
            1. Bebida
            2. Alimento
            """)
            if opcion == "1":
                modificar_bebida(menu)
            elif opcion == "2":
                modificar_alimento(menu)
            else:
                print("Usted ha ingresado algún dato inválido, por favor inténtelo de nuevo")
        elif opcion == "4":
            agregar_combo(menu)
        elif opcion == "5":
            print("eliminar_combo_menu_combos")
        elif opcion == "6":
            buscar_producto(menu)
        elif opcion == "7":
            print("Buscar combos por nombre o rango de precio")
        elif opcion == "8":
            print("Hasta luego, ¡Gracias por visitar nuestro restaurante!")
        else:
            print("Usted ha ingresado algún dato inválido, por favor inténtelo de nuevo")
        break


#------MODULO 5: ESTADISTICAS------
#Se evalua la funcion de la gestion de la empresa 
#Se encuentra en construccion ya que la desarrolladora no logro terminar el programa
def estadisticas():
    while True:
        opcion = input(''' 🛳 Bienvenidos a las estadisticas del crucero:
        1. Promedio de gasto de un cliente en el crucero(tickets + tours)
        2. Porcentaje de clientes que no compran tours
        3. Clientes de mayor fidelidad en la linea
        4. Top 3 cruceros con mas ventas en tickets
        5. Top 5 productos mas vendidos en el restaurante
        6. Graficos de las estadisticas
        7. Salir ''')
        if opcion == "1":
            print(
                "Promedio de gasto de un cliente en el crucero(tickets + tours)"
            )
        elif opcion == "2":
            print("Porcentaje de clientes que no compran tours")
        elif opcion == "3":
            print("Clientes de mayor fidelidad en la linea")
        elif opcion == "4":
            print("Top 3 cruceros con mas ventas en tickets")
        elif opcion == "5":
            print("Top 5 productos mas vendidos en el restaurante")
        elif opcion == "6":
            print("Graficos de las estadisticas")
        elif opcion == "7":
            print("Hasta luego")

        else:
            print("Usted ha ingresado algún dato inválido, por favor inténtelo de nuevo")
        break

#API que contiene informacion para el desarrollo del programa
def api():
    url = "https://saman-caribbean.vercel.app/api/cruise-ships"
    resultado = requests.request("GET", url)
    return resultado.json()


#------MENU PRINCIPAL DEL CRUCERO------


#Funcion Principal del Crucero que nos permite acceder a los modulos
def main():
    menu = []
    cruceros = []

    #Tours:
    tour_puerto = Tour("Tour en el puerto", 30, 4, "7:00 AM", 10)
    tour_degustacion = Tour("Degustacion de comida local", 100, 2, "12:00 PM", 100)
    tour_trotar = Tour("Tour trotar por el pueblo/ciudad", 0, 0, "6:00 AM", 0)
    tour_visita = Tour("Visita lugares historicos", 40, 4, "10:00 AM", 15)

    # Creamos cruceros en el background
    cruceros = crear_cruceros(cruceros)

    while True:
        #Menu para poder escojer que se desea hacer en el sistema
        opcion = input('''
        🛳 Bienvenidos a Saman Caribbean ¿Qué desea realizar?:
        1. Ver cruceros
        2. Venta de habitaciónes
        3. Compra de tours
        4. Restaurante
        5. Mostrar estadisticas 
        6. Salir
        >  ''')
        if opcion == '1':
            ver_cruceros(cruceros)
        elif opcion == '2':
            gestion_habitacion(cruceros)
        elif opcion == '3':
            seleccion_barco_tour(cruceros, clientes)
        elif opcion == '4':
           seleccion_barco_restaurante(cruceros)
        elif opcion == '5':
            estadisticas()
        elif opcion == '6':
             print("Adios 👋!")
             break
        else:
            print("Has ingresado un dato incorrecto!")

main()
