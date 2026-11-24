# Pseudocódigo v2 — con la clase `Ciudad`

**Proyecto:** Camino a mi casa (CS 1400)
**Integrantes:** Tito Huerta y Eduardo Reyes
**Fecha:** 23 de noviembre de 2026

Esta es la versión **después** de refactorizar con Programación Orientada a
Objetos (Paso 7). La versión v1 se conserva sin cambios en
[`seudo_codigo.txt`](seudo_codigo.txt).

---

## Qué cambió respecto a la v1

| v1 (Paso 6) | v2 (Paso 7) |
|---|---|
| Los datos de cada ciudad andaban sueltos: `nombre`, `pais`, `lat`, `lon` | Van juntos dentro de un objeto `Ciudad` |
| `CALCULAR distancia(lat1, lon1, lat2, lon2)` | `origen.distancia_a(destino)` |
| Para mostrar una ciudad había que armar el texto cada vez | El objeto sabe describirse con `__str__` |

El comportamiento del programa **no cambió**: los mismos casos de prueba del
Paso 6 dan exactamente el mismo resultado.

---

## La clase

```
CLASE Ciudad

    ATRIBUTOS
        nombre    (texto)
        pais      (texto)
        latitud   (número, en grados)
        longitud  (número, en grados)

    MÉTODO __init__(nombre, pais, latitud, longitud)
        Guardar cada dato recibido dentro del objeto

    MÉTODO distancia_a(otra_ciudad)
        DEVOLVER calcular_distancia(
                     mi latitud, mi longitud,
                     latitud de otra_ciudad, longitud de otra_ciudad)
        * No reescribe la fórmula: llama a la de utils.py

    MÉTODO __str__()
        DEVOLVER "nombre, pais (latitud, longitud)"
        * Ejemplo: "San Marcos, Guatemala (14.97, -91.79)"

FIN CLASE
```

---

## El programa principal

```
INICIO

  MOSTRAR mensaje de bienvenida y qué hace el programa

  REPETIR

      MOSTRAR menú
          1. Calcular distancia entre dos ciudades
          2. El clima de una ciudad
          3. Salir

      PEDIR opción al usuario

      SI opción es 1 ENTONCES

          REPETIR
              PEDIR lugar de origen
          HASTA QUE no esté vacío Y tenga el formato "ciudad, país"

          REPETIR
              PEDIR lugar de destino
          HASTA QUE no esté vacío Y tenga el formato "ciudad, país"

          SI origen y destino son iguales ENTONCES
              MOSTRAR "Ingrese lugares diferentes"
              VOLVER al menú
          FIN SI

          REPETIR
              PEDIR unidad preferida (km o millas)
          HASTA QUE sea una opción válida

          MOSTRAR resumen de confirmación

          INTENTAR
              datos_origen  <- BUSCAR coordenadas del origen en la API
              datos_destino <- BUSCAR coordenadas del destino en la API
          SI OCURRE un error de red (ConnectionError) ENTONCES
              MOSTRAR el mensaje de error
              VOLVER al menú
          FIN INTENTAR

          SI datos_origen es NADA (None) ENTONCES
              MOSTRAR "Ciudad no encontrada"
              VOLVER al menú
          FIN SI

          SI datos_destino es NADA (None) ENTONCES
              MOSTRAR "Ciudad no encontrada"
              VOLVER al menú
          FIN SI

          MOSTRAR las coordenadas encontradas

          --- AQUÍ ESTÁ EL CAMBIO DE LA v2 ---
          origen  <- CREAR Ciudad(nombre, pais, latitud, longitud) del origen
          destino <- CREAR Ciudad(nombre, pais, latitud, longitud) del destino

          km <- origen.distancia_a(destino)
          ------------------------------------

          millas <- CONVERTIR km a millas

          tiempo_avion <- FORMATEAR (km / VELOCIDAD_AVION)
          tiempo_auto  <- FORMATEAR (km / VELOCIDAD_AUTO)

          MOSTRAR resumen del viaje:
              nombre, país y coordenadas de cada ciudad
              distancia en km y en millas
              tiempo estimado en avión y en auto
              aviso de que es distancia en línea recta

      SI NO, SI opcion es 2, ENTONCES
    
      REPETIR
              PEDIR lugar de origen
          HASTA QUE no esté vacío Y tenga el formato "ciudad, país"
        
        origen  <- CREAR Ciudad(nombre, pais, latitud, longitud) del origen



      SI NO, SI opción es 3 ENTONCES
          MOSTRAR despedida
          SALIR del bucle

      SI NO
          MOSTRAR "Opción no válida"
      FIN SI

  FIN REPETIR

FIN
```

---
