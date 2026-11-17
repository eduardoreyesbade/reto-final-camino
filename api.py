# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: api.py  -> Funciones que consumen las APIs
# Paso 5: Conexión con la API de Geocodificación (Open-Meteo)
# Integrantes: Tito Huerta y Eduardo Reyes
# Actualizadd: 17 de noviembre de 2026
# ============================================================
# Privacidad: aquí solo viajan nombres de CIUDAD y PAÍS.
# Nunca direcciones exactas, ni en el código ni en GitHub.

import requests

# La API de Open-Meteo es gratis y no pide API key.
URL_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"


def buscar_ubicacion(lugar):
    """Recibe 'ciudad, país' y devuelve la respuesta completa de Open-Meteo.

    Parámetros:
        lugar (str): texto que escribió el usuario, por ejemplo "Ogden, Estados Unidos".

    Devuelve:
        dict: el JSON que mandó la API (puede traer la lista 'results' o venir vacío).

    Puede lanzar:
        ValueError: si el texto no trae ciudad y país separados por coma.
        requests.exceptions.RequestException: si falla la red o el código de estado.
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
    """Busca un lugar y devuelve sus coordenadas listas para usar.

    Esta es la función que llama main.py. Se apoya en buscar_ubicacion() y se
    encarga de atrapar todos los errores para que el programa NO se cierre.

    Parámetros:
        lugar (str): "ciudad, país" escrito por el usuario.

    Devuelve:
        dict: siempre un diccionario.
            Si todo salió bien:
                {"ok": True, "nombre": str, "pais": str, "lat": float, "lon": float}
            Si hubo un problema:
                {"ok": False, "mensaje": str}  -> el mensaje se le muestra al usuario

    Importante: esta función devuelve los datos, no los imprime. Quien decide
    cómo mostrarlos es main.py.
    """
    try:
        datos = buscar_ubicacion(lugar)

    except ValueError as error:
        # El usuario no escribió el formato "ciudad, país"
        # (o la API devolvió algo que no es JSON).
        return {"ok": False, "mensaje": str(error)}

    except requests.exceptions.Timeout:
        # La API tardó más de 10 segundos en contestar.
        return {"ok": False,
                "mensaje": "La API tardó demasiado en responder. Intenta de nuevo."}

    except requests.exceptions.HTTPError:
        # Respuesta inesperada: un código de estado distinto de 200.
        return {"ok": False,
                "mensaje": "La API respondió con un código de estado inesperado."}

    except requests.exceptions.RequestException:
        # Sin internet, wifi apagado u otro error de red.
        return {"ok": False,
                "mensaje": "No se pudo conectar con la API. Revisa tu internet."}

    # Ojo: la API contesta 200 aunque no encuentre nada; en ese caso no hay 'results'.
    resultados = datos.get("results")
    if not resultados:
        return {"ok": False,
                "mensaje": f"No encontramos '{lugar}'. Revisa cómo lo escribiste."}

    # Si hay varias coincidencias, usamos la primera (la más relevante).
    lugar_encontrado = resultados[0]

    return {
        "ok": True,
        "nombre": lugar_encontrado.get("name", lugar),
        "pais": lugar_encontrado.get("country", "Desconocido"),
        "lat": lugar_encontrado.get("latitude"),
        "lon": lugar_encontrado.get("longitude"),
    }
