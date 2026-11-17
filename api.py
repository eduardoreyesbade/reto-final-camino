# Funciones que consumen las APIs

import requests

def buscar_ubicacion(start):
    """Recibe 'ciudad, país' y devuelve la respuesta completa de Open-Meteo."""
    # Paso 2: separamos la ciudad y el país usando la primera coma.
    ciudad, separador, pais = start.partition(",")
    # Comprobamos que ambos datos estén presentes antes de hacer la consulta.
    if not separador or not ciudad.strip() or not pais.strip():
        raise ValueError("Ingrese cada ubicación con el formato: ciudad, país.")

    # Paso 3: enviamos ciudad y país; requests prepara los espacios y las tildes.
    # Pedimos hasta 5 coincidencias en español y esperamos como máximo 15 segundos.
    respuesta = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": f"{ciudad.strip()}, {pais.strip()}",
            "count": 5,
            "language": "es",
        },
        timeout=15,
    )


'''
URL: https://geocoding-api.open-meteo.com/v1/search

Parámetros:

Parámetro	Valor
name	la ciudad que escribió el usuario
count	1 (el enunciado dice “usar el primero”)
language	es
format	json
'''
