from conexionDB import get_db
from funciones import *
from funciones import limpiarconsola as cc
from rich import print
import pwinput


db = get_db()

usuarios = db["usuarios"]

clientes = db["clientes"]
productos = db["productos"]
pedidos = db["pedidos"]

def menu(usuario):
    while True:
        cc()
        print(f"--- Bievenido {usuario} ---")
        print("¿Que desea hacer?")
        print("1. Nuevo Pedido.")
        print("2. Menu Clientes")
        print("3. Menu Productos")
        print("4. Menu Pedidos")
        print("5. Salir")
        opcion=int(input("Ingrese su opcion y presione Enter: "))
        if opcion == 1:
            menu_nuevo_pedido()
        elif opcion ==2:
            menu_clientes()
        elif opcion ==3:
            menu_productos()
        elif opcion ==4:
            menu_pedidos()
        elif opcion ==5:
            quit()
        else:
            print("Opcion incorrecta, intente nuevamente.")



def menu_productos():
    cc()
    print("--- Menu Productos ---")
    print("1. Agregar producto.")
    print("2. Ver productos.")
    print("3. Volver al menu principal.")
    opcion=int(input("Ingrese su opcion y presione Enter: "))
    if opcion == 1:
        agregar_producto()
    elif opcion ==2:
        ver_productos()
    elif opcion ==3:
        return
    else:
        print("Opcion incorrecta, intente nuevamente.")




            



def login(): 
    cc()
    print("--- Bienvenido al programa de gestion de ComercioTech ---")
    exito = False
    while exito == False:
    
        usuario= input("Ingrese su nombre de usuario: ")
        password = pwinput.pwinput(prompt="Ingrese su contraseña: ", mask="*")
        resultado= iniciar_sesion(usuario, password)
        if resultado== True:
            exito = True
            menu(usuario)
        else:
            print(resultado)

login()







