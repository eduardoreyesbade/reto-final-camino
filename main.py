# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: main.py  -> Menú y flujo principal
# Paso 4: Entrada, salida y formato base (input / print)
# Paso 5: Llama a api.py para obtener las coordenadas
# Paso 6: Calcula la distancia y los tiempos, y muestra el resumen
# Paso 7: Usa objetos Ciudad en vez de diccionarios sueltos (POO)
# Paso 8: Muestra el clima actual de las dos ciudades (Open-Meteo Forecast)
# Integrantes: Tito Huerta y Eduardo Reyes
# Fecha: 23 de noviembre de 2026 (Updated)
# ============================================================
# Privacidad: al usuario solo se le piden CIUDAD y PAÍS.
# Nunca direcciones exactas, ni en el código ni en GitHub.

# La funcionalidad adicional de Weather la hice Eduardo Reyes

import sys

# trae la data de la ubicacion via API
from api import obtener_coordenadas

# trae la data del clima via API
from clima import obtener_clima

# Paso 7: la clase que agrupa los datos de una ciudad y sus acciones
from ciudad import Ciudad

# De utils traemos las funciones de calculo. Ya no importamos
# calcular_distancia: ahora se llama a traves de Ciudad.distancia_a().
from utils import km_a_millas, calcular_tiempo, formatear_tiempo

VELOCIDAD_AVION = 800   # km/h, velocidad crucero aproximada de un avión comercial
VELOCIDAD_AUTO = 80     # km/h, promedio razonable en carretera

# En Windows la consola no usa UTF-8 por defecto y los acentos salen mal.
sys.stdout.reconfigure(encoding="utf-8")

# Las únicas respuestas que aceptamos para la unidad de medida.
UNIDADES = {
    "km": "kilómetros",
    "kilometros": "kilómetros",
    "kilómetros": "kilómetros",
    "millas": "millas",
    "mi": "millas",
}

def mostrar_bienvenida():
    """Imprime el título y explica de qué se trata el programa."""
    print("=====================================")
    print("   CAMINO A MI CASA")
    print("=====================================")
    print("Este programa te ayudará a encontrar la distancia al destino "
          "deseado entre dos puntos gerograficos.")


def mostrar_menu():
    """Imprime las opciones del menú principal."""
    print()
    print("1. Calcular distancia entre dos ciudades")
    print("2. Clima actual de una ciudad")
    print("3. Salir")

# Usamos dos funciones separadas para pedir el origen y el destino,
# para que cada una sea clara y específica.
def pedir_origen(etiqueta):
    """
    Pide el lugar de ORIGEN y repite la pregunta hasta que sea valido.

    Parámetros:
        etiqueta (str): el texto que se le muestra al usuario.

    Devuelve:
        str: el lugar escrito con el formato "ciudad, país".
    """
    while True:
        # .strip() le quita los espacios de más a lo que escribió el usuario.
        origen = input(f"{etiqueta}: ").strip()

        # Validamos que el usuario no entregue vacío (ni puros espacios).
        if origen == "":
            print("Por favor, ingrese lugares válidos.")
            continue

        # Validamos que por lo menos tenga 2 caracteres.
        if len(origen) < 2:
            print("Por favor, ingrese lugares con al menos 2 caracteres.")
            continue

        # Validamos el formato "ciudad, país" ANTES de gastar una consulta a
        # internet: tiene que haber una coma y algo escrito a cada lado.
        ciudad, separador, pais = origen.partition(",")
        if not separador or not ciudad.strip() or not pais.strip():
            print("Use el formato: ciudad, país. "
                  "Ejemplo: Ogden, Estados Unidos")
            continue

        return origen


# Esta función es igual que pedir_origen, pero para el destino.
# Si cambias la validación en una, cámbiala también en la otra.
def pedir_destino(etiqueta):
    """
    Pide el lugar de DESTINO y repite la pregunta hasta que sea válido.

    Parámetros:
        etiqueta (str): el texto que se le muestra al usuario.

    Devuelve:
        str: el lugar escrito con el formato "ciudad, país".
    """
    while True:
        # .strip() le quita los espacios de más a lo que escribió el usuario.
        destino = input(f"{etiqueta}: ").strip()

        # Validamos que el usuario no entregue vacío (ni puros espacios).
        if destino == "":
            print("Por favor, ingrese lugares válidos.")
            continue

        # Validamos que por lo menos tenga 2 caracteres.
        if len(destino) < 2:
            print("Por favor, ingrese lugares con al menos 2 caracteres.")
            continue

        # Validamos el formato "ciudad, país" ANTES de gastar una consulta a
        # internet: tiene que haber una coma y algo escrito a cada lado.
        ciudad, separador, pais = destino.partition(",")
        if not separador or not ciudad.strip() or not pais.strip():
            print("Use el formato: ciudad, país. "
                  "Ejemplo: Santiago, Chile")
            continue

        return destino


def pedir_unidad():
    """
    Pregunta la unidad preferida y rechaza lo que no sea km o millas.

    """
    while True:
        respuesta = input("¿En qué unidad quiere ver la distancia "
                          "(km/millas)?: ").strip().lower()
        # nos aseguram,os que la respuesta esté en el diccionario de UNIDADES que esta al niicio y devolvemos el valor
        if respuesta in UNIDADES:
            return UNIDADES[respuesta]
        # por si escribe otra cosa, le decimos que no es válido y vuelve a preguntar
        print("Opción no válida. Escriba 'km' o 'millas'.")


# Esto permite confirmar visualmente la informacion entregada por el usuario antes de hacer la consulta a la API.
def mostrar_resumen(origen, destino, unidad):
    """Imprime el resumen de confirmación antes de consultar la API."""
    print()
    print("--- Resumen ---")
    print(f"Origen:  {origen}")
    print(f"Destino: {destino}")
    print(f"Unidad:  {unidad}")
    print("Consultando datos...")


def mostrar_coordenadas(etiqueta, datos):
    """
    Imprime el nombre, el país y las coordenadas de un lugar.
    """
    # Si el dato venía guardado de una búsqueda anterior, se lo avisamos
    # al usuario para que sepa por qué fue tan rápido.
    if datos.get("desde_cache"):
        origen = "  (desde el caché)"
    else:
        origen = ""

    print(f"{etiqueta} {datos['nombre']}, {datos['pais']} "
          f"→ lat {datos['lat']:.4f}, lon {datos['lon']:.4f}{origen}")


def mostrar_clima(etiqueta, ciudad, clima):
    """
    Imprime el clima actual de una ciudad. 
    """
    # None significa que no se pudo conseguir el dato. Lo decimos y seguimos:
    # el clima es un extra, no la razón de ser del programa.
    if clima is None:
        print(f"{etiqueta} {ciudad.nombre}: clima no disponible")
        return

    print(f"{etiqueta} {ciudad.nombre}: {clima['temperatura']} {clima['unidad']}"
          f"  -  {clima['descripcion']}")

    
def mostrar_resultado(origen, destino, km, millas, tiempo_avion, tiempo_auto,
                      unidad, clima_origen, clima_destino):
    """
    Imprime el resumen final del viaje ya calculado.

    Muestra primero la unidad que el usuario eligió y la otra entre paréntesis.

    Parámetros:
        origen, destino (Ciudad): los objetos Ciudad del viaje.
        km, millas (float): la distancia en cada unidad.
        tiempo_avion, tiempo_auto (str): los tiempos ya con formato "X h Y min".
        unidad (str): "kilómetros" o "millas", lo que el usuario prefirió.
        clima_origen, clima_destino (dict | None): el clima de cada ciudad,
                         o None si no se pudo consultar.
    """
    # El :,.2f pone el separador de miles y deja dos decimales (3,478.52).
    if unidad == "millas":
        distancia = f"{millas:,.2f} millas  ({km:,.2f} km)"
    else:
        distancia = f"{km:,.2f} km  ({millas:,.2f} millas)"

    # Paso 7: ahora leemos los ATRIBUTOS del objeto (origen.nombre)
    
    print()
    print("========== RESUMEN DEL VIAJE ==========")
    print(f"Origen:   {origen.nombre}, {origen.pais}  "
          f"({origen.latitud:.4f}, {origen.longitud:.4f})")
    print(f"Destino:  {destino.nombre}, {destino.pais}  "
          f"({destino.latitud:.4f}, {destino.longitud:.4f})")
    print()
    print(f"Distancia en línea recta: {distancia}")
    print()
    print(f"Tiempo estimado en avión ({VELOCIDAD_AVION} km/h):  {tiempo_avion}")
    print(f"Tiempo estimado en auto  ({VELOCIDAD_AUTO} km/h):   {tiempo_auto}")

    # Paso 8: el clima actual de cada ciudad, dentro del mismo recuadro.
    print()
    print("--- Clima actual ---")
    mostrar_clima("Origen: ", origen, clima_origen)
    mostrar_clima("Destino:", destino, clima_destino)
    print()
    print("* La distancia es una aproximación en línea recta, no por carretera.")
    print("=======================================")

def procesar_viaje():
    """
    Opción 1 del menú: pide los lugares, consulta la API y muestra el viaje.

    Si la ciudad no existe o falla la red, avisa y regresa al menú.
    """
    print()
    inicio = pedir_origen("Ingrese el lugar donde te encuentras (ciudad, pais)")
    final = pedir_destino("Ingrese el lugar donde deseas llegar (ciudad, pais)")

    # Validamos que las ubicaciones no sean las mismas.
    if inicio.lower() == final.lower():
        print("El lugar de inicio y destino son iguales. "
              "Por favor, ingrese lugares diferentes.")
        return

    unidad = pedir_unidad()

    # Resumen de confirmación antes de salir a internet.
    mostrar_resumen(inicio, final, unidad)

    # Paso 5: buscamos las coordenadas de cada lugar con la API.
    # Un fallo de red lanza ConnectionError; lo avisamos y volvemos al menú.
    try:
        datos_origen = obtener_coordenadas(inicio)
        datos_destino = obtener_coordenadas(final)
    except ConnectionError as error:
        print(f"  -> Error de red: {error}")
        return

    # obtener_coordenadas devuelve None cuando no encuentra la ciudad.
    if datos_origen is None:
        print(f"  -> Ciudad no encontrada: {inicio}")
        return

    if datos_destino is None:
        print(f"  -> Ciudad no encontrada: {final}")
        return

    print()
    mostrar_coordenadas("Origen: ", datos_origen)
    mostrar_coordenadas("Destino:", datos_destino)

    # Paso 7 (POO): con los datos sueltos de la API armamos dos objetos Ciudad.
    # Así el nombre, el país y las coordenadas dejan de andar por separado.
    origen = Ciudad(datos_origen["nombre"], datos_origen["pais"],
                    datos_origen["lat"], datos_origen["lon"])
    destino = Ciudad(datos_destino["nombre"], datos_destino["pais"],
                     datos_destino["lat"], datos_destino["lon"])

    # Paso 8: el clima es un EXTRA. Si falla, el resumen del viaje se tiene
    # que mostrar igual, así que atrapamos el ConnectionError AQUÍ (no hacemos
    # return como en las coordenadas) y seguimos con None.
    print()
    print("Consultando el clima...")
    try:
        clima_origen = obtener_clima(origen.latitud, origen.longitud)
        clima_destino = obtener_clima(destino.latitud, destino.longitud)
    except ConnectionError as error:
        print(f"  -> No se pudo obtener el clima: {error}")
        clima_origen = None
        clima_destino = None


    # El objeto sabe calcular su propia distancia a otra ciudad.
    # Antes era: calcular_distancia(lat1, lon1, lat2, lon2)
    km = origen.distancia_a(destino)
    millas = km_a_millas(km)
    tiempo_avion = formatear_tiempo(calcular_tiempo(km, VELOCIDAD_AVION))
    tiempo_auto = formatear_tiempo(calcular_tiempo(km, VELOCIDAD_AUTO))

    mostrar_resultado(origen, destino, km, millas,
                      tiempo_avion, tiempo_auto, unidad,
                      clima_origen, clima_destino)


def procesar_clima():
    """
    Opción 2 del menú: muestra solo el clima actual de UNA ciudad.

    Reusa las mismas piezas que la opción 1: la validación del formato,
    obtener_coordenadas() (con su caché) y obtener_clima(). Aquí el clima
    NO es un extra: es lo único que pidió el usuario, así que si falla la
    red avisamos y volvemos al menú.
    """
    print()
    # Reusamos pedir_origen() porque la etiqueta es un parámetro: valida
    # el formato "ciudad, país" igual que en la opción 1.
    lugar = pedir_origen("Ingrese la ciudad (ciudad, pais)")

    print()
    print("Consultando datos...")

    # Primero las coordenadas: el clima se pide por latitud y longitud.
    try:
        datos = obtener_coordenadas(lugar)
    except ConnectionError as error:
        print(f"  -> Error de red: {error}")
        return

    if datos is None:
        print(f"  -> Ciudad no encontrada: {lugar}")
        return

    print()
    mostrar_coordenadas("Ubicación:", datos)

    # Paso 7 (POO): también aquí trabajamos con un objeto Ciudad.
    ciudad = Ciudad(datos["nombre"], datos["pais"], datos["lat"], datos["lon"])

    try:
        clima = obtener_clima(ciudad.latitud, ciudad.longitud)
    except ConnectionError as error:
        print(f"  -> No se pudo obtener el clima: {error}")
        return

    print()
    print("========== CLIMA ACTUAL ==========")
    print(f"Ciudad:      {ciudad.nombre}, {ciudad.pais}")
    if clima is None:
        print("La API no devolvió datos del clima.")
    else:
        print(f"Temperatura: {clima['temperatura']} {clima['unidad']}")
        print(f"Cielo:       {clima['descripcion']}")
    print("==================================")


def main():
    """Programa principal: el menú se repite hasta que el usuario elige salir."""
    mostrar_bienvenida()

    while True:
        mostrar_menu()
        # Le quitamos los espacios de más a la opción elegida.
        opcion = input("Ingrese la opción deseada: ").strip()

        if opcion == "1":
            procesar_viaje()
        elif opcion == "2":
            # Paso 8: el clima por sí solo, sin calcular ningún viaje.
            procesar_clima()
        elif opcion == "3":
            # Si quiere salir del programa.
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            # Esto es por si no responde 1, 2 ni 3.
            print("Opción no válida. Por favor, ingrese una opción válida.")


# El menú solo corre cuando ejecutamos main.py directamente.
if __name__ == "__main__":
    main()
