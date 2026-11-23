"""
Descragado de github y editado el 11/23
Clase Ciudad (se agrega el 21 nov)
ciudad.py - Clase Ciudad (Paso 7: POO).

Agrupa los datos de una ciudad (nombre, país, latitud, longitud)
y las acciones relacionadas (calcular la distancia a otra ciudad).
"""

from utils import calcular_distancia

class Ciudad:
    """Representa una ciudad con su ubicación geográfica."""

    def __init__(self, nombre, pais, latitud, longitud):
        """
        Crea una ciudad.

        Parámetros:
            nombre (str): nombre de la ciudad.
            pais (str): país de la ciudad.
            latitud (float): latitud en grados.
            longitud (float): longitud en grados.
        """
        self.nombre = nombre
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud

    def distancia_a(self, otra_ciudad):
        """Devuelve la distancia en km (Haversine) hasta otra Ciudad."""
        # este viene de utils.py, no hay que reimplementar la fórmula de Haversine aquí
        return calcular_distancia(
            self.latitud, self.longitud,
            otra_ciudad.latitud, otra_ciudad.longitud,
        )

    def __str__(self):
        """Texto legible, por ejemplo: 'San Marcos, Guatemala (14.97, -91.79)'."""
        # el formato de los números es opcional, pero es bueno limitar los decimales a 2 para que no se vea feo 
        return f"{self.nombre}, {self.pais} ({self.latitud:.2f}, {self.longitud:.2f})"


# Solo se ejecuta al correr ciudad.py directamente
if __name__ == "__main__":
    origen = Ciudad("San Marcos", "Guatemala", 14.9667, -91.7944)
    destino = Ciudad("Salt Lake City", "Estados Unidos", 40.7608, -111.8910)
    print(origen)
    print(f"{origen.distancia_a(destino):,.2f} km")