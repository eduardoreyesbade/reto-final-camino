# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: main.py  -> Menú y flujo principal
# Paso 4: Entrada, salida y formato base (input / print)
# Paso 5: Llama a api.py para obtener las coordenadas
# Integrantes: Tito Huerta y Eduardo Reyes
# Fecha: 23 de noviembre de 2026 (Updated)
# ============================================================
# Privacidad: al usuario solo se le piden CIUDAD y PAÍS.
# Nunca direcciones exactas, ni en el código ni en GitHub.

import sys

from api import obtener_coordenadas

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
    print("2. Salir")


def pedir_lugar(etiqueta):
    """
    Pide un lugar al usuario y repite la pregunta hasta que sea válido.

    """
    while True:
        # .strip() le quita los espacios de más a lo que escribió el usuario.
        lugar = input(f"{etiqueta}: ").strip()

        # Validamos que el usuario no entregue vacío (ni puros espacios).
        if lugar == "":
            print("Por favor, ingrese lugares válidos.")
            continue

        # Validamos que por lo menos tenga 2 caracteres.
        if len(lugar) < 2:
            print("Por favor, ingrese lugares con al menos 2 caracteres.")
            continue

        return lugar


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


def buscar_lugar(etiqueta, lugar):
    """
    Busca un lugar en la API y, si no lo encuentra, vuelve a preguntar.

    """
    while True:
        datos = obtener_coordenadas(lugar)

        # Si todo salió bien, ya terminamos.
        if datos["ok"]:
            return datos

        # Aquí llegamos si no se encontró la ciudad o si falló la red.
        print(f"  -> {datos['mensaje']}")
        print("     Intente otra vez (o escriba 'cancelar' para volver al menú).")

        lugar = pedir_lugar(etiqueta)
        if lugar.lower() == "cancelar":
            return None


def mostrar_coordenadas(etiqueta, datos):
    """Imprime el nombre, el país y las coordenadas de un lugar."""
    # Si el dato venía guardado de una búsqueda anterior, se lo avisamos
    # al usuario para que sepa por qué fue tan rápido.
    if datos.get("desde_cache"):
        origen = "  (desde el caché)"
    else:
        origen = ""

    print(f"{etiqueta} {datos['nombre']}, {datos['pais']} "
          f"→ lat {datos['lat']:.4f}, lon {datos['lon']:.4f}{origen}")


def calcular_distancia():
    """Opción 1 del menú: pide los datos y muestra las coordenadas de la API."""
    print()
    inicio = pedir_lugar("Ingrese el lugar donde te encuentras (ciudad, pais)")
    final = pedir_lugar("Ingrese el lugar donde deseas llegar (ciudad, pais)")

    # Validamos que las ubicaciones no sean las mismas.
    if inicio.lower() == final.lower():
        print("El lugar de inicio y destino son iguales. "
              "Por favor, ingrese lugares diferentes.")
        return

    unidad = pedir_unidad()

    # Resumen de confirmación antes de salir a internet.
    mostrar_resumen(inicio, final, unidad)

    # Paso 5: buscamos las coordenadas de cada lugar con la API.
    datos_origen = buscar_lugar("Ingrese el lugar donde te encuentras (ciudad, pais)",
                                inicio)
    if datos_origen is None:
        return

    datos_destino = buscar_lugar("Ingrese el lugar donde deseas llegar (ciudad, pais)",
                                 final)
    if datos_destino is None:
        return

    print()
    mostrar_coordenadas("Origen: ", datos_origen)
    mostrar_coordenadas("Destino:", datos_destino)

    # Pendiente (utils.py): calcular la distancia con la fórmula de Haversine
    # y los tiempos de viaje en avión y en auto.
    print(f"(La distancia en {unidad} se calculará en el siguiente paso.)")


def main():
    """Programa principal: el menú se repite hasta que el usuario elige salir."""
    mostrar_bienvenida()

    while True:
        mostrar_menu()
        # Le quitamos los espacios de más a la opción elegida.
        opcion = input("Ingrese la opción deseada: ").strip()

        if opcion == "1":
            calcular_distancia()
        elif opcion == "2":
            # Si quiere salir del programa.
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
        else:
            # Esto es por si no responde ni 1 ni 2.
            print("Opción no válida. Por favor, ingrese una opción válida.")


# El menú solo corre cuando ejecutamos main.py directamente.
if __name__ == "__main__":
    main()
