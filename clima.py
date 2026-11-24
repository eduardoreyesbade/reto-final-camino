# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: clima.py  -> Clima actual de una ciudad (Open-Meteo Forecast API)
# Paso 8: Clima actual (segunda API del proyecto)
# Integrantes: Tito Huerta y Eduardo Reyes
# Fecha: 24 de noviembre de 2026
# ============================================================


import requests

# La Forecast API de Open-Meteo 

URL_FORECAST = "https://api.open-meteo.com/v1/forecast"

# Esta es la tabla oficial "WMO Weather interpretation codes (WW)",
# copiada de https://open-meteo.com/en/docs y traducida al español.

CODIGOS_CLIMA = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna densa",
    56: "Llovizna helada ligera",
    57: "Llovizna helada densa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia fuerte",
    66: "Lluvia helada ligera",
    67: "Lluvia helada fuerte",
    71: "Nevada ligera",
    73: "Nevada moderada",
    75: "Nevada fuerte",
    77: "Granos de nieve",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    85: "Chubascos de nieve ligeros",
    86: "Chubascos de nieve fuertes",
    95: "Tormenta",
    96: "Tormenta con granizo ligero",
    97: "Tormenta fuerte",
    99: "Tormenta con granizo fuerte",
}

def describir_clima(codigo):
    """
    Traduce el weather_code de la API a un texto en español.
    """
    return CODIGOS_CLIMA.get(codigo, f"Código desconocido ({codigo})")


def obtener_clima(latitud, longitud):
    """
    Pide a Open-Meteo el clima actual de un punto geográfico.
    """
    try:
        # current= pide los datos del momento. 
        # El timeout de 10 segundos 
        respuesta = requests.get(
            URL_FORECAST,
            params={
                "latitude": latitud,
                "longitude": longitud,
                "current": "temperature_2m,weather_code",
            },
            timeout=10,
        )

        # Si el código de estado no es 200 (404, 500, etc.) esto lanza excepción.
        respuesta.raise_for_status()

        datos = respuesta.json()

    except requests.exceptions.Timeout:
        raise ConnectionError("La API del clima tardó demasiado en responder.")

    except requests.exceptions.HTTPError:
        raise ConnectionError("La API del clima respondió con un código inesperado.")

    except requests.exceptions.RequestException:
        raise ConnectionError("No se pudo consultar el clima. Revisa tu internet.")

    except ValueError:
        # La respuesta llegó, pero no era JSON válido.
        raise ConnectionError("La API del clima devolvió una respuesta inválida.")

    # La API contesta 200
    actual = datos.get("current")
    if not actual:
    #si no viene "current" no muestra nada
        return None

    temperatura = actual.get("temperature_2m")
    codigo = actual.get("weather_code")

    # Sin temperatura no vale la pena devolver el dato a medias.
    if temperatura is None:
        return None

    # current_units trae la unidad que usó la API ("°C" por defecto).
    unidades = datos.get("current_units", {})

    return {
        "temperatura": temperatura,
        "unidad": unidades.get("temperature_2m", "°C"),
        "codigo": codigo,
        "descripcion": describir_clima(codigo),
    }


# Pruebas rápidas: solo se ejecutan al correr clima.py directamente
if __name__ == "__main__":
    import sys

    # En Windows la consola no usa UTF-8 por defecto y los acentos salen mal.
    sys.stdout.reconfigure(encoding="utf-8")

    print("--- Traducción de códigos (sin internet) ---")
    for codigo in (0, 3, 61, 95, 1000):      # 1000 NO existe en la tabla WMO
        print(f"  {codigo:>4} -> {describir_clima(codigo)}")
