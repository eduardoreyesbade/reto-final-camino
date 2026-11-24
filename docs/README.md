# Camino a mi casa

Este programa calcula la distancia entre 2 ciudades y cuánto tomaría viajar de una a otra en avión y en auto. Lo hice para la clase CS 1400 de Weber State University.

La idea es conectar dos lugares que significan algo. 

Integrantes:
- Eduardo Reyes
- Tito Huerta

## Qué hace el programa?

Pides dos ciudades y el programa busca sus coordenadas en internet (por medio deuna API), calcula la distancia en línea recta entre ellas y estima los tiempos de viaje y nos permite saber la distancia tanto en millas como en kilometros.


## Cómo está organizado

- `main.py` - el menú y el programa principal
- `api.py` - la conexión con Open-Meteo para buscar coordenadas
- `requirements.txt` - las librerías que hacen falta


## Cómo correrlo

debes ingresar a nuestro repositorio de github en la ruta: https://github.com/eduardoreyesbade/reto-final-camino luego cargar los archivos en tu computadora y ejecutar pyuthon desde el archivo main.py, luego seguir el procedimiento que se muestra en el siguiente bloque ## Ejemplo


## Ejemplo

```
=====================================
   CAMINO A MI CASA (EJEMPLO BAISCO)
=====================================

1. Calcular distancia entre dos ciudades
2. Salir

Ingrese la opción deseada: 1

Ciudad de origen: Ogden, Estados Unidos
Ciudad de destino: Santiago, Chile

  Ogden, United States
  41.223, -111.973

  Santiago, Chile
  -33.457, -70.648

  Distancia: 9,318 km (5,790 millas)

```

## Nota

Por seguridad, el programa solo usa ciudad y país. No guarda ni pide direcciones exactas. Unicamente solicita Ciudad y Pais en el siguiente formato "Ciudad","Pais"

## Autores

Eduardo Reyes y Tito Huerta
CS 1400 - Weber State University - Fall 2026