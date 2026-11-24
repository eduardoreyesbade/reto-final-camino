# Camino a mi casa

Este programa calcula la distancia entre 2 ciudades y cuánto tomaría viajar de una a otra en avión y en auto. Lo hice para la clase CS 1400 de Weber State University.

La idea es conectar dos lugares que significan algo. 

Integrantes:
- Eduardo Reyes
- Tito Huerta

## Qué hace el programa?

Pides dos ciudades y el programa busca sus coordenadas en internet (por medio deuna API), calcula la distancia en línea recta entre ellas y estima los tiempos de viaje y nos permite saber la distancia tanto en millas como en kilometros.

También puedes consultar el clima de una ciudad o convertir un monto entre dos monedas. Consulta el [README principal](../README.md) para ver el ejemplo de conversión, las [notas técnicas](notas_tecnicas.md) para ver las APIs y el [pseudocódigo](pseudocodigo_v2.md) para ver el flujo completo.

## Cómo está organizado

- `main.py` - el menú y el programa principal
- `api.py` - la conexión con Open-Meteo para buscar coordenadas
- `clima.py` - la consulta del clima a Open-Meteo Forecast
- `divisas.py` - la consulta de tasas a ExchangeRate-API
- `requirements.txt` - las librerías que hacen falta


## Cómo correrlo

debes ingresar a nuestro repositorio de github en la ruta: https://github.com/eduardoreyesbade/reto-final-camino luego cargar los archivos en tu computadora y ejecutar pyuthon desde el archivo main.py, luego seguir el procedimiento que se muestra en el siguiente bloque ## Ejemplo


## Ejemplo

```
=====================================
   CAMINO A MI CASA
=====================================

1. Calcular distancia entre dos ciudades
2. Clima actual de una ciudad
3. Conversión de divisas
4. Salir
```

## Nota

Para las búsquedas geográficas, el programa pide lugares en el formato
`ciudad, país`. Para la conversión, pide dos códigos de moneda y un monto.

## Autores

Eduardo Reyes y Tito Huerta
CS 1400 - Weber State University - Fall 2026