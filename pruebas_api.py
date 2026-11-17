# ============================================================
# Reto Final - "Camino a mi casa" (CS1400)
# Archivo: pruebas_api.py -> Pruebas manuales de la API (Paso 5)
# Integrantes: Tito Huerta y Eduardo Reyes
# Fecha: 17 de noviembre de 2026
# ============================================================
# Cómo usarlo:  python pruebas_api.py
# Sirve para la captura de pantalla de los casos de prueba.

import sys

from api import obtener_coordenadas

# En Windows la consola no usa UTF-8 por defecto y los acentos salen mal.
sys.stdout.reconfigure(encoding="utf-8")


def probar(titulo, lugar):
    """Corre una prueba de obtener_coordenadas() y muestra el resultado."""
    print(f"\n--- {titulo} ---")
    datos = obtener_coordenadas(lugar)

    if datos["ok"]:
        print(f"OK: {datos['nombre']}, {datos['pais']} "
              f"→ lat {datos['lat']:.4f}, lon {datos['lon']:.4f}")
    else:
        print(f"AVISO: {datos['mensaje']}")


print("[PRUEBAS] Probando obtener_coordenadas()...")

# Caso 1: una ciudad conocida -> debe devolver coordenadas.
probar("Caso 1: ciudad conocida", "Madrid, España")

# Caso 2: una ciudad inventada -> mensaje de 'no encontrada', sin errores.
probar("Caso 2: ciudad inventada", "Xyzabc, Nolandia")

# Caso 3: sin conexión a internet -> apaga el wifi y vuelve a correr esto.
#         Debe salir un mensaje de error de red y el programa NO debe cerrarse.
probar("Caso 3: prueba de red (apaga el wifi)", "Ogden, Estados Unidos")

# Caso extra: falta el país -> avisa del formato "ciudad, país".
probar("Caso extra: formato incompleto", "Madrid")

print("\n[FIN] El programa no se cerró en ningún caso.")
