from conexionDB import get_db
import os
from rich import print

db = get_db()

def iniciar_sesion(usuario, password):
    obtener_usuario = db["usuarios"].find_one({"usuario":usuario})
    if obtener_usuario is not None:
        usuarioDB = obtener_usuario
        if usuarioDB["password"] == password:
            return True
        else:
            return "Contraseña incorrecta"
    else:
        return "Usuario no encontrado"
    

def limpiarconsola():
    os.system("cls" if os.name == "nt" else "clear")

cc = limpiarconsola  # ✅ CORREGIDO: sin paréntesis, se asigna la función, no su resultado

def menu_nuevo_pedido():
    
    productos_pedido=[]

    cc()
    print("--- Nuevo Pedido ---")
    rut_cliente= input("Ingrese rut del cliente, si no esta registrado, ingrese 0: ")
    if rut_cliente != "0":
        cliente=db["clientes"].find_one({"rut":rut_cliente})
        if cliente is None:
            pressAny=input("Cliente no encontrado, intentelo nuevamente...")
            return
        else:
            cc()
            print(f"Cliente {cliente["nombre"]} encontrado.")
            while True:
                producto=input("Indique el producto a sumar al pedido: ")
                busqueda_producto = list(db["productos"].find({
                                                    "nombre": 
                                                    {
                                                    "$regex": producto,
                                                    "$options": "i"
                                                    }
                                                    }))
                if not busqueda_producto:
                    pressAny=input("Producto no encontrado, intentelo nuevamente...")
                else:
                    for i, item in enumerate(busqueda_producto, start=1):
                        print(f"{i}. {item["nombre"]}. Valor: {item["precio"]}")
                    seleccion=int(input("Seleccione el numero de producto que va a sumar al pedido: "))
                    producto_seleccionado= busqueda_producto[seleccion - 1]
                    productos_pedido.append(producto_seleccionado)
                    print(f"Se agrego el producto {producto_seleccionado["nombre"]} al pedido.")
                    otro_producto= input("Desea agregar otro producto? s/n:")
                    if otro_producto == "n":
                        break
            cc()
            print("El pedido incluye: ")
            total=0
            for i,producto in enumerate(productos_pedido, start=1):
                print(f"{i}. {producto["nombre"]}, con un valor de {producto["precio"]}")
                total+=producto["precio"]
            print(f"Con un valor total de: ${total} pesos.")
            correcto=input("¿Esta correcto? s/n:")
            if correcto == "s":
                ultimo_pedido = db["pedidos"].find_one(sort=[("_id", -1)])
                nuevo_id = (ultimo_pedido["_id"] + 1)

                nuevo_pedido = {
                    "_id": nuevo_id,
                    "cliente_id": cliente["_id"],
                    "productos": [p["_id"] for p in productos_pedido],
                    "total": total
                }

                db["pedidos"].insert_one(nuevo_pedido)
                cc()
                print(nuevo_pedido)
                pressAny=input("Pedido guardado correctamente.")
                return
    elif rut_cliente == "0":
            cc()
            print(f"Procediendo a venta de cliente no registrado.")
            while True:
                producto=input("Indique el producto a sumar al pedido: ")
                busqueda_producto = list(db["productos"].find({
                                                    "nombre": 
                                                    {
                                                    "$regex": producto,
                                                    "$options": "i"
                                                    }
                                                    }))
                if not busqueda_producto:
                    pressAny=input("Producto no encontrado, intentelo nuevamente...")
                else:
                    for i, item in enumerate(busqueda_producto, start=1):
                        print(f"{i}. {item["nombre"]}. Valor: {item["precio"]}")
                    seleccion=int(input("Seleccione el numero de producto que va a sumar al pedido: "))
                    producto_seleccionado= busqueda_producto[seleccion - 1]
                    productos_pedido.append((producto_seleccionado))
                    print(f"Se agrego el producto {producto_seleccionado["nombre"]} al pedido.")
                    otro_producto= input("Desea agregar otro producto? s/n:")
                    if otro_producto == "n":
                        break
            cc()
            print("El pedido incluye: ")
            total=0
            for i,producto in enumerate(productos_pedido, start=1):
                print(f"{i}. {producto["nombre"]}, con un valor de {producto["precio"]}")
                total+=producto["precio"]
            print(f"Con un valor total de: ${total} pesos.")
            correcto=input("¿Esta correcto? s/n:")
            if correcto == "s":
                ultimo_pedido = db["pedidos"].find_one(sort=[("_id", -1)])
                nuevo_id = (ultimo_pedido["_id"] + 1)

                nuevo_pedido = {
                    "_id": nuevo_id,
                    "cliente_id": None,
                    "productos": [p["_id"] for p in productos_pedido],
                    "total": total
                }

                db["pedidos"].insert_one(nuevo_pedido)
                cc()
                print(nuevo_pedido)
                pressAny=input("Pedido guardado correctamente.")
                return
    
def registrar_cliente():
    cc()
    nombre= input("Ingrese el nombre del cliente: ")
    email= input("Ingrese el email del cliente: ")
    ciudad= input("Ingrese la ciudad del cliente: ")
    rut= input("Ingrese el rut del cliente: ")
    id_previo= db["clientes"].find_one(sort=[("_id", -1)])
    nuevo_id= id_previo["_id"] + 1
    nuevo_cliente= {
        "_id": nuevo_id,
        "nombre": nombre,
        "email": email,
        "ciudad": ciudad,
        "rut": rut
    }
    db["clientes"].insert_one(nuevo_cliente)
    print(f"Cliente {nombre} registrado exitosamente con id {nuevo_id}.")
    pressAny=input("Presione Enter para continuar...")
    return

def menu_clientes():
    cc()
    print("--- Menu Clientes ---")
    print("1. Registrar cliente.")
    print("2. Ver clientes.")
    print("3. Volver al menu principal.")
    opcion=int(input("Ingrese su opcion y presione Enter: "))
    if opcion == 1:
        registrar_cliente()
    elif opcion ==2:
        ver_clientes()
    elif opcion ==3:
        return
    else:
        print("Opcion incorrecta, intente nuevamente.")

def ver_clientes():
    cc()
    print("1. Buscar cliente por rut.")
    print("2. Ver todos los clientes.")
    print("3. Volver al menu clientes.")
    opcion=int(input("Ingrese su opcion y presione Enter: "))
    if opcion == 1:
        buscar_cliente()
    elif opcion == 2:
        ver_todos_los_clientes()
    elif opcion == 3:
        return

def buscar_cliente():
    cc()
    rut_cliente= input("Ingrese el rut del cliente que desea buscar: ")
    cliente=db["clientes"].find_one({"rut":rut_cliente})
    if cliente is None:
        pressAny=input("Cliente no encontrado, intentelo nuevamente...")
    else:
        print(f"Cliente encontrado: {cliente}")
        print("1. Actualizar cliente.")
        print("2. Eliminar cliente.")
        print("3. Volver al menu clientes.")
        opcion=int(input("Ingrese su opcion y presione Enter: "))
        if opcion == 1:
            actualizar_cliente(cliente)
        elif opcion == 2:
            eliminar_cliente(cliente)
        elif opcion == 3:
            return
        else:
            print("Opcion incorrecta, intente nuevamente.")

def actualizar_cliente(cliente):
    cc()
    print("Ingrese los nuevos datos del cliente, si desea mantener el dato actual deje el campo vacio.")
    nombre= input(f"Nombre actual: {cliente['nombre']}. Nuevo nombre: ")
    email= input(f"Email actual: {cliente['email']}. Nuevo email: ")
    ciudad= input(f"Ciudad actual: {cliente['ciudad']}. Nueva ciudad: ")
    rut= input(f"Rut actual: {cliente['rut']}. Nuevo rut: ")
    if nombre != "":
        cliente["nombre"] = nombre
    if email != "":
        cliente["email"] = email
    if ciudad != "":
        cliente["ciudad"] = ciudad
    if rut != "":
        cliente["rut"] = rut
    db["clientes"].update_one({"_id": cliente["_id"]}, {"$set": cliente})
    print("Cliente actualizado correctamente.")
    pressAny=input("Presione Enter para continuar...")

def eliminar_cliente(cliente):
    cc()
    confirmacion= input(f"¿Esta seguro que desea eliminar al cliente {cliente['nombre']}? s/n: ")
    if confirmacion == "s":
        db["clientes"].delete_one({"_id": cliente["_id"]})
        print("Cliente eliminado correctamente.")
        pressAny=input("Presione Enter para continuar...")
    else:
        print("Eliminacion cancelada.")
        pressAny=input("Presione Enter para continuar...")

def ver_todos_los_clientes():
    cc()
    clientes= db["clientes"].find()
    print("Lista de clientes: ")
    for cliente in clientes:
        print(cliente)
    pressAny=input("Presione Enter para continuar...")


def menu_pedidos():
    cc()
    print("--- Menu Pedidos ---")
    print("1. Buscar pedido por ID.")
    print("2. Ver todos los pedidos.")
    print("3. Volver al menu principal.")
    opcion=int(input("Ingrese su opcion y presione Enter: "))
    if opcion == 1:
        buscar_pedido_id()
    elif opcion ==2:
        ver_todos_pedidos()
    elif opcion ==3:
        return
    else:
        print("Opcion incorrecta, intente nuevamente.")

def buscar_pedido_id():
    cc()
    id_pedido = int(input("Ingrese el ID del pedido que desea buscar: "))
    pedido = db["pedidos"].find_one({"_id": id_pedido})
    if pedido:
        print(pedido)
        print("1. Eliminar pedido.")
        print("2. Volver al menu anterior.")
        opcion=int(input("Ingrese su opcion y presione Enter: "))
        if opcion == 1:
            db["pedidos"].delete_one({"_id": id_pedido})
            print("Pedido eliminado exitosamente.")
            pressAny= input("Presione Enter para continuar...")
        elif opcion ==2:
            return
        else:
            print("Opcion incorrecta, intente nuevamente.")
            pressAny= input("Presione Enter para continuar...")
    else:
        print("Pedido no encontrado.")
        pressAny= input("Presione Enter para continuar...")

def ver_todos_pedidos():
    cc()
    print("--- Todos los Pedidos ---")
    for pedido in db["pedidos"].find():
        print(pedido)
    pressAny= input("Presione Enter para continuar...")


def agregar_producto():
    cc()
    nombre= input("Ingrese el nombre del producto: ")
    precio= float(input("Ingrese el precio del producto: "))
    descripcion= input("Ingrese la descripcion del producto: ")
    stock= int(input("Ingrese el stock disponible: "))
    id_previo= db["productos"].find_one(sort=[("_id", -1)])
    nuevo_id= id_previo["_id"] + 1
    nuevo_producto= {
        "_id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
        "descripcion": descripcion,
        "stock": stock
    }
    db["productos"].insert_one(nuevo_producto)
    print(f"Producto {nombre} registrado exitosamente con id {nuevo_id}.")
    pressAny=input("Presione Enter para continuar...")
    return

def ver_productos():
    cc()
    print("1. Buscar producto por nombre.")
    print("2. Ver todos los productos.")
    print("3. Volver al menu productos.")
    opcion=int(input("Ingrese su opcion y presione Enter: "))
    if opcion == 1:
        buscar_producto()
    elif opcion == 2:
        ver_todos_los_productos()
    elif opcion == 3:
        return

def buscar_producto():
    cc()
    nombre_producto= input("Ingrese el nombre del producto que desea buscar: ")
    producto=db["productos"].find_one({"nombre": {"$regex": nombre_producto, "$options": "i"}})
    if producto is None:
        pressAny=input("Producto no encontrado, intentelo nuevamente...")
    else:
        print(f"Producto encontrado: {producto}")
        print("1. Actualizar producto.")
        print("2. Eliminar producto.")
        print("3. Volver al menu productos.")
        opcion=int(input("Ingrese su opcion y presione Enter: "))
        if opcion == 1:
            actualizar_producto(producto)
        elif opcion == 2:
            eliminar_producto(producto)
        elif opcion == 3:
            return
        else:
            print("Opcion incorrecta, intente nuevamente.")

def actualizar_producto(producto):
    cc()
    print("Ingrese los nuevos datos del producto, si desea mantener el dato actual deje el campo vacio.")
    nombre= input(f"Nombre actual: {producto['nombre']}. Nuevo nombre: ")
    precio_str= input(f"Precio actual: {producto['precio']}. Nuevo precio: ")
    descripcion= input(f"Descripcion actual: {producto['descripcion']}. Nueva descripcion: ")
    stock_str= input(f"Stock actual: {producto['stock']}. Nuevo stock: ")
    if nombre != "":
        producto["nombre"] = nombre
    if precio_str != "":
        producto["precio"] = float(precio_str)
    if descripcion != "":
        producto["descripcion"] = descripcion
    if stock_str != "":
        producto["stock"] = int(stock_str)
    db["productos"].update_one({"_id": producto["_id"]}, {"$set": producto})
    print("Producto actualizado correctamente.")
    pressAny=input("Presione Enter para continuar...")

def eliminar_producto(producto):
    cc()
    confirmacion= input(f"¿Esta seguro que desea eliminar el producto {producto['nombre']}? s/n: ")
    if confirmacion == "s":
        db["productos"].delete_one({"_id": producto["_id"]})
        print("Producto eliminado correctamente.")
        pressAny=input("Presione Enter para continuar...")
    else:
        print("Eliminacion cancelada.")
        pressAny=input("Presione Enter para continuar...")

def ver_todos_los_productos():
    cc()
    productos= db["productos"].find()
    print("Lista de productos: ")
    for producto in productos:
        print(producto)
    pressAny=input("Presione Enter para continuar...")
