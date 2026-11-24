# Pseudocódigo v2 — con la clase `Ciudad`

**Proyecto:** Camino a mi casa (CS 1400)
**Integrantes:** Tito Huerta y Eduardo Reyes
**Actualizado:** 24 de noviembre de 2026

Este pseudocódigo describe el flujo con la clase `Ciudad` (Paso 7),
el clima actual (Paso 8) y la conversión de divisas (Paso 9).

---

## Qué cambió respecto a la v1

| v1 (Paso 6) | v2 (Paso 7) |
|---|---|
| Los datos de cada ciudad andaban sueltos: `nombre`, `pais`, `lat`, `lon` | Van juntos dentro de un objeto `Ciudad` |
| `CALCULAR distancia(lat1, lon1, lat2, lon2)` | `origen.distancia_a(destino)` |
| Para mostrar una ciudad había que armar el texto cada vez | El objeto sabe describirse con `__str__` |

La refactorización conservó los cálculos de distancia y tiempos del Paso 6.

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
          3. Conversión de divisas
          4. Salir

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

          INTENTAR consultar el clima de ambas ciudades
          SI falla la consulta, MOSTRAR aviso y CONTINUAR con clima no disponible

          km <- origen.distancia_a(destino)
          ------------------------------------

          millas <- CONVERTIR km a millas

          tiempo_avion <- FORMATEAR (km / VELOCIDAD_AVION)
          tiempo_auto  <- FORMATEAR (km / VELOCIDAD_AUTO)

          MOSTRAR resumen del viaje:
              nombre, país y coordenadas de cada ciudad
              distancia en km y en millas
              tiempo estimado en avión y en auto
              clima de cada ciudad cuando esté disponible
              aviso de que es distancia en línea recta

      SI NO, SI opción es 2 ENTONCES

          REPETIR
              PEDIR lugar para consultar el clima
          HASTA QUE no esté vacío Y tenga el formato "ciudad, país"

          BUSCAR las coordenadas de la ciudad
          SI falla la búsqueda o no hay resultados, MOSTRAR aviso y VOLVER al menú

          CREAR objeto Ciudad con los datos encontrados
          CONSULTAR el clima con la latitud y la longitud
          MOSTRAR temperatura y descripción del cielo, o un aviso si faltan datos

      SI NO, SI opción es 3 ENTONCES

          PEDIR códigos de origen y destino y convertirlos a mayúsculas
          SI algún código no tiene tres letras, MOSTRAR aviso y VOLVER al menú

          PEDIR monto
          SI el monto no es un número finito mayor o igual a cero,
              MOSTRAR aviso y VOLVER al menú

          CONSULTAR tasas de la moneda de origen en ExchangeRate-API
          BUSCAR la tasa de destino
          SI falla la consulta o falta la tasa, MOSTRAR aviso y VOLVER al menú

          equivalente <- monto * tasa
          SI el equivalente no es finito, MOSTRAR aviso y VOLVER al menú
          MOSTRAR recuadro con equivalente, monto original y tasa aplicada
          MOSTRAR la fuente de la tasa

      SI NO, SI opción es 4 ENTONCES
          MOSTRAR despedida
          SALIR del bucle

      SI NO
          MOSTRAR "Opción no válida"
      FIN SI

  FIN REPETIR

FIN
```

---
