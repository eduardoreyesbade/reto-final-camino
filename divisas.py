"""Consulta una tasa de cambio con ExchangeRate-API."""
# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: divisas.py  -> Consulta de tasas de cambio (ExchangeRate-API)
# Paso 9: Consulta de tasas de cambio (ExchangeRate-API)
# Integrantes: Tito Huerta y Eduardo Reyes
# Fecha: 24 de noviembre de 2026
# ============================================================

import requests

URL_DIVISAS = "https://open.er-api.com/v6/latest"


def obtener_tasa(origen, destino):
    """Devuelve la tasa para el destino o None si la moneda no está disponible."""
    try:
        respuesta = requests.get(f"{URL_DIVISAS}/{origen}", timeout=10)
        if respuesta.status_code == 404:
            return None
        respuesta.raise_for_status()
        datos = respuesta.json()
    except (requests.exceptions.RequestException, ValueError) as error:
        raise ConnectionError("No se pudo consultar la tasa de cambio. "
                              "Intenta de nuevo más tarde.") from error

    if datos.get("result") == "error":
        if datos.get("error-type") in ("unsupported-code", "unknown-code"):
            return None
        raise ConnectionError("La API no pudo devolver la tasa de cambio.")

    # La API devuelve un diccionario con las tasas para la moneda de origen.
    return datos.get("rates", {}).get(destino)
