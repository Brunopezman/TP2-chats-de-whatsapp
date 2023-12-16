import chats_de_whatsapp

OPCION_1 = '1'
OPCION_2 = '2'
OPCION_3 = '3'

def separar_con_guiones() -> None:
    print(100*'-')

def imprimir_menu() -> None:
    '''Imprime el menu de opciones'''

    print("Menu de Opciones:")
    print('1. Contar repeticiones de palabra segun cada contacto')
    print('2. Generar mensaje pseudo-aleatorio segun contacto')
    print('3. Salir del programa')
    separar_con_guiones()

def seleccionar_opcion() -> str:
    """Selecciona la opcion valida entre la que se muestran en pantalla. Si el usuario ingresa un valor no valido, """
    imprimir_menu()
    
    opt = input("Seleccione una opcion: ")

    while opt not in [OPCION_1,OPCION_2,OPCION_3]:
        opt = input(f'La opcion {opt} es invalida. Por favor, seleccione una opcion válida: ')
    
    return opt

def ingresar_palabras_a_contar() -> str:
    palabras = input('Ingrese las palabras para contar entre contactos: ')

    return palabras

def imprimir_contactos(contactos:list):
    
    print('Contactos:')
    for i, contacto in enumerate(contactos):
        print(str(i)+ '. ' + contacto)

def elegir_contacto(contactos:list):
    '''El usuario elige un contacto entre todos los del archivo.
    Pre: Recibe todos los contactos.
    Post: Devuelve el contacto elegido.
    '''

    while True:
        try:
            i = input("Por favor, ingrese el índice del contacto que desea seleccionar o 's' para salir: ")

            if i == 's':
                return 's'
            i = int(i)
            if 0 <= i < len(contactos):
                return contactos[i]
            print("Índice fuera de rango. Intente nuevamente.")

        except ValueError:
            print("Entrada no válida. Ingrese un número entero válido o 's' para salir.")

def main():

    print('Whatsapp Statistics')
    separar_con_guiones()

    archivo = input('ingrese una ruta de archivo: ')
    frecuencia_palabras_por_contacto = chats_de_whatsapp.frecuenciar_palabras_por_contacto(archivo)
    if not frecuencia_palabras_por_contacto:
        return
    contactos = chats_de_whatsapp.listar_contactos(frecuencia_palabras_por_contacto)

    opt = seleccionar_opcion()

    while not opt == OPCION_3:

        if opt == OPCION_1:
                
            palabras_usuario = ingresar_palabras_a_contar()
            cant_pal_contacto = chats_de_whatsapp.contar_repeticiones_palabra(palabras_usuario, frecuencia_palabras_por_contacto)
            destino = input('Ingrese una ruta de destino: ')
            chats_de_whatsapp.guardar_palabras_en_destino(cant_pal_contacto, destino)
            print('Reporte generado!')

        elif opt == OPCION_2:

            imprimir_contactos(contactos)
            
            while True:
                contacto_elegido = elegir_contacto(contactos)
                if contacto_elegido == 's':
                    break
                p_posibles = chats_de_whatsapp.listar_palabras_posibles(contacto_elegido, frecuencia_palabras_por_contacto)
                mensaje_generado = chats_de_whatsapp.generar_mensaje_pseudoaleatorio(contacto_elegido, frecuencia_palabras_por_contacto, p_posibles)
                print(mensaje_generado)

        opt = seleccionar_opcion()

    return

main()