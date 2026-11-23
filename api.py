# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: api.py  -> Funciones que consumen las APIs
# Paso 5: Conexión con la API de Geocodificación (Open-Meteo)
# Extensión: caché local para no repetir consultas (ver cache.py)
# Integrantes: Tito Huerta y Eduardo Reyes
# Actualizado: 23 de noviembre de 2026 (Updated)
# ============================================================
# Privacidad: aquí solo viajan nombres de CIUDAD y PAÍS.
# Nunca direcciones exactas, ni en el código ni en GitHub.

import unicodedata

import requests

# Para hacer el caché de las consultas y no repetirlas,
# importamos las funciones de cache.py.
from cache import cargar_cache, guardar_cache

# La API de Open-Meteo es gratis y no pide API key.
URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"


def normalizar_llave(lugar):
    """Convierte lo que escribió el usuario en una llave única para el caché.

    "Ogden, Estados Unidos", "  OGDEN ,estados unidos" y "Ogden, Estados
    Unídos" tienen que dar la MISMA llave; si no, el caché casi nunca acierta.

    Parámetros:
        lugar (str): el texto tal cual lo escribió el usuario.

    Devuelve:
        str: la llave en minúsculas, sin espacios de más y sin acentos.
    """
    ciudad, _, pais = lugar.partition(",")
    texto = f"{ciudad.strip()}, {pais.strip()}".lower()

    # NFD separa cada letra de su acento ("á" pasa a ser "a" + "´") y después
    # nos quedamos solo con los caracteres que NO son acentos.
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


def buscar_ubicacion(lugar):
    """
    Recibe 'ciudad, país' y devuelve la respuesta completa de Open-Meteo web API.

    """
    # Paso 2: separamos la ciudad y el país usando la primera coma.
    ciudad, separador, pais = lugar.partition(",")
    # Comprobamos que ambos datos estén presentes antes de hacer la consulta.
    if not separador or not ciudad.strip() or not pais.strip():
        raise ValueError("Ingrese cada ubicación con el formato: ciudad, país.")

    # Paso 3: enviamos ciudad y país; requests prepara los espacios y las tildes.
    # Pedimos hasta 5 coincidencias en español. El timeout de 10 segundos es
    # obligatorio para que el programa no se quede colgado esperando.
    respuesta = requests.get(
        URL_GEOCODING,
        params={
            "name": f"{ciudad.strip()}, {pais.strip()}",
            "count": 5,
            "language": "es",
            "format": "json",
        },
        timeout=10,
    )

    # Si el código de estado no es 200 (404, 500, etc.) esto lanza una excepción.
    respuesta.raise_for_status()

    return respuesta.json()


def obtener_coordenadas(lugar):
    """
    Busca un lugar y devuelve sus coordenadas listas para usar.
    """
    llave = normalizar_llave(lugar)
    cache = cargar_cache()

    # ¿Ya lo habíamos buscado antes? Entonces ni tocamos la red.
    if llave in cache:
        # dict() hace una copia, para no modificar lo que está guardado.
        guardado = dict(cache[llave])
        return guardado

    try:
        datos = buscar_ubicacion(lugar)

    except ValueError as error:
        return None

    except requests.exceptions.Timeout:
        # La API tardó más de 10 segundos en contestar.
        raise ConnectionError("La API tardó demasiado en responder.")

    except requests.exceptions.HTTPError:
        # Respuesta inesperada: un código de estado distinto de 200.
        raise ConnectionError("La API respondió con un código inesperado.")

    except requests.exceptions.RequestException:
        # Sin internet, wifi apagado u otro error de red.
        raise ConnectionError("No se pudo conectar. Revisa tu internet.")

    # Ojo: la API contesta 200 aunque no encuentre nada; en ese caso no hay 'results'.
    resultados = datos.get("results")
    if not resultados:
        return None

    # Si hay varias coincidencias, usamos la primera (la más relevante).
    lugar_encontrado = resultados[0]

    resultado = {
        "nombre": lugar_encontrado.get("name", lugar),
        "pais": lugar_encontrado.get("country", "Desconocido"),
        "lat": lugar_encontrado.get("latitude"),
        "lon": lugar_encontrado.get("longitude"),
    }

    # Lo guardamos para la próxima vez.
    cache[llave] = resultado
    guardar_cache(cache)

    # Copia otra vez, para que "desde_cache" no termine dentro del archivo.
    nuevo = dict(resultado)
    nuevo["desde_cache"] = False
    return nuevo
