# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: cache.py  -> Guarda en disco las coordenadas ya consultadas
# Extensión: evita repetir consultas a la API (lo usa api.py)
# Integrantes: Tito Huerta y Eduardo Reyes
# Actualizado: 17 de noviembre de 2026
# ============================================================
# Privacidad: aquí solo se guardan nombres de CIUDAD y PAÍS.
# Nunca direcciones exactas, ni en el código ni en GitHub.

import json
import os

CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(CARPETA_PROYECTO, "data")
CACHE_FILE = os.path.join(CACHE_DIR, "coordenadas_cache.json")

def cargar_cache():
    """
    Lee el archivo JSON del caché.
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def guardar_cache(cache):
    """
    Escribe el diccionario completo en el archivo JSON.

    """
    try:
        # Crea la subcarpeta automáticamente si no existe.
        os.makedirs(CACHE_DIR, exist_ok=True)

        # ensure_ascii=False para que los acentos se guarden como acentos
        # y el archivo se pueda leer a simple vista.
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"[CACHE] No se pudo guardar el archivo: {e}")
