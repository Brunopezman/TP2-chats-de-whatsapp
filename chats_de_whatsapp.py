import csv
import random

def frecuenciar_palabras_por_contacto(archivo:str) -> dict:
    """Arma un diccionario que contiene las frecuencias de las palabras que le suceden a la palabra inicial de los dialogos segun el contacto elegido.
    Pre: Recibe el archivo de conversaciones de android y el contacto elegido por el usuario.
    Post: Devuelve un diccionario estructurado de la forma `'palabra':{'siguiente_palabra':frecuencia}`
    """

    frecuencia_palabras_por_contacto = {}

    try:
        with open(archivo, encoding='utf-8') as chat:
            for linea in chat:
                partes = linea.rstrip().split(' - ')
                mensaje = partes[1]
                if ':' in mensaje:
                    mensaje_contacto = mensaje.split(': ')
                    contacto, dialogo = mensaje_contacto[0], mensaje_contacto[1].split(' ')
                    for i in range(len(dialogo) - 1):
                        p_actual = dialogo[i]
                        sig_palabra = dialogo[i + 1]
                        if not (p_actual == '<multimedia' or p_actual == 'omitido>' or '()' in p_actual):
                            frecuencia_palabras_por_contacto[contacto] = frecuencia_palabras_por_contacto.get(contacto,{})       
                            frecuencia_palabras_por_contacto[contacto][p_actual] = frecuencia_palabras_por_contacto[contacto].get(p_actual,{})       
                            frecuencia_palabras_por_contacto[contacto][p_actual][sig_palabra] = frecuencia_palabras_por_contacto[contacto][p_actual].get(sig_palabra, 0) + 1
                        

    except FileNotFoundError:
        print('No se encontro el archivo o es inexistente.')
        return {}  
    except IOError:
        print('Se produjo un error al intentar escribir en el archivo.')
        return {}

    return frecuencia_palabras_por_contacto

def contar_repeticiones_palabra(palabras_usuario:str, frecuencia_palabras_por_contacto:dict) -> dict:
    '''Cuenta la cantidad de apariciones de palabras segun cada contacto del archivo y las guarda en un diccionario.
    Pre: Fue inicializada la funcion ingresar_palabras_a_contar() y recibe un archivo de convesaciones de android.
    Post: Devuelve un diccionario con formato `contacto: {palabra: cantidad}`.
    '''
    cant_palabras_contacto = {}
    
    for contacto, palabras_conversacion in frecuencia_palabras_por_contacto.items():
        cant_palabras_contacto[contacto] = {}
        for palabra_usuario in palabras_usuario.lower().split(' '):
            for palabras1, palabras_siguientes in palabras_conversacion.items():
                if palabras1.lower() == palabra_usuario:
                    cant_palabras_contacto[contacto][palabra_usuario] = cant_palabras_contacto[contacto].get(palabra_usuario, 0) + 1
                for palabras2 in palabras_siguientes.keys():
                    if palabras1.lower() == palabra_usuario or palabras2.lower() == palabra_usuario:
                        cant_palabras_contacto[contacto][palabra_usuario] = cant_palabras_contacto[contacto].get(palabra_usuario, 0) + 1
    return cant_palabras_contacto

def guardar_palabras_en_destino(cant_palabras_contacto:dict, destino:str) -> bool:
    """Guardar las palabras en un archivo destino en formato csv
    Pre: Recibe un diccionario que contiene a los contactos con las veces que dijeron c/u cada palabra. Debe estar inicializada la funcion `contar_repeticiones_palabra`
    Post: Devuelve un archivo en formato csv con las palabras escritas de la siguiente manera `contacto,palabra,frecuencia`
    """
    try:
        with open(destino, 'w',newline='') as destino_csv:
            archivo_escrito = csv.writer(destino_csv)
            archivo_escrito.writerow(["contacto", "palabra", "frecuencia"])
            for contacto, recuento in cant_palabras_contacto.items():
                for palabra, frecuencia in recuento.items():
                    archivo_escrito.writerow([contacto, palabra, frecuencia])

    except FileNotFoundError:
        print('Ingrese una entrada de archivo destino valida')
        
def listar_contactos(frecuencia_palabras_por_contacto:dict) -> list:
    """lista a todos los contactos del archivo de conversaciones.
    Pre: Recibe un archivo con las conversaciones de android.
    Pro: Devuelve una lista con todos los contactos. 
    """

    contactos = []
    for contacto in frecuencia_palabras_por_contacto.keys():
        contactos.append(contacto)
        
    return contactos

def listar_palabras_posibles(contacto_elegido:str, frecuencia_palabras_por_contacto:dict) -> list:
    """Devuelve una lista con todas las palabras del diccionario que haya dicho el contacto elegido."""

    p_posibles = []

    for palabras in frecuencia_palabras_por_contacto[contacto_elegido].keys():
        p_posibles.append(palabras)

    return p_posibles

def listar_palabras_siguientes(contacto_elegido, frecuencia_palabras_por_contacto, p_actual):
    """Devuelve una lista con todas las palabras siguientes a la palabra actual, del diccionario que haya dicho el contacto elegido.
    PRE: Debe haberse inicializado la funcion `listar_palabras_posibles`. Recibe la variable p_actual en la cual se encuentra una palabra elegida de forma aleatoria de la lista de palabras posibles
    POST: Devuelve la lista de palabras siguientes.
    """

    p_siguientes = []

    for palabra in frecuencia_palabras_por_contacto[contacto_elegido][p_actual].keys():
        p_siguientes.append(palabra)

    return p_siguientes

def listar_frecuencias(contacto_elegido, frecuencia_palabras_por_contacto, p_actual):
    """Devuelve las frecuencias de de cada palabra siguiente a la palabra actual
    PRE: Deben estar inicializadas las funciones `listar_palabras_posibles` y `listar_palabras_siguientes` en ese orden.
    """
    frecuencias = []

    for frecuencia in frecuencia_palabras_por_contacto[contacto_elegido][p_actual].values():
        frecuencias.append(frecuencia)

    return frecuencias

def generar_mensaje_pseudoaleatorio(contacto_elegido:str, frecuencia_palabras_por_contacto:dict, p_posibles:list) -> str:
    """Genera un mensaje aleatorio dicho por el contacto elegido. 
    Pre: Recibe el contacto elegido por el usuario, el diccionario con las frecuencias de las palabras segun el contacto y las palabras posibles.
    Post: Devuelve el mensaje generado.
    """
    
    p_actual = random.choice(p_posibles) 
    mensaje_generado = [p_actual]
    p_siguientes = listar_palabras_siguientes(contacto_elegido, frecuencia_palabras_por_contacto, p_actual)
    frecuencias = listar_frecuencias(contacto_elegido, frecuencia_palabras_por_contacto, p_actual)
    
    while not len(p_siguientes) == 0:
        try:
            p_agregada = random.sample(p_siguientes, counts = frecuencias, k = 1)[0]
            mensaje_generado.append(p_agregada)
            p_siguientes = listar_palabras_siguientes(contacto_elegido, frecuencia_palabras_por_contacto, p_agregada)
            frecuencias = listar_frecuencias(contacto_elegido, frecuencia_palabras_por_contacto, p_agregada)
        except KeyError:
            break

    return f'{contacto_elegido}: ' + ' '.join(mensaje_generado).capitalize()
