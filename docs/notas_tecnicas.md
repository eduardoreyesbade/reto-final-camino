# Notas técnicas

## Estado de los pasos del proyecto

| Paso | Qué pedía | Dónde quedó |
|---|---|---|
| Paso 4 | Menú, validaciones, unidad y resumen | `main.py` |
| Paso 5 | API de geocodificación Open-Meteo | `api.py` |
| Paso 6 | Distancia (Haversine), tiempos y MVP | `utils.py`, `main.py` |
| Paso 7 | Clase `Ciudad` (POO) | `ciudad.py` |
| Paso 8 | Clima actual (Forecast API) | `clima.py`, `main.py` |
| Paso 9 | Conversión de divisas (ExchangeRate-API) | `divisas.py`, `main.py` |

## Casos de prueba de la API

| Caso | Resultado |
|---|---|
| Ciudad conocida (`Madrid, España`) | `lat 40.4165, lon -3.7026` |
| Ciudad inventada (`Xyzabc, Nolandia`) | "Ciudad no encontrada" y regreso al menú |
| Sin internet y ciudad fuera del caché | "Error de red" y regreso al menú |
| Falta el país (`Madrid`) | Avisa del formato "ciudad, país" |

Para correrlos: desde el menú de `main.py`, opción 1.


## Clima API (Paso 8)

Es la **segunda API** del proyecto, y conviene no confundirla con la primera:

| | Geocoding (`api.py`) | Forecast (`clima.py`) |
|---|---|---|
| Dominio | `geocoding-api.open-meteo.com` | `api.open-meteo.com` |
| Recibe | `"ciudad, país"` | `latitude` y `longitude` |
| Devuelve | nombre, país, lat, lon | temperatura y `weather_code` |

Las dos se usan en cadena: `api.py` traduce lo que escribió el usuario a
coordenadas, y con esas mismas coordenadas `clima.py` pide el clima. Al usuario
no se le pregunta nada nuevo, así que la privacidad del proyecto no cambia.

La consulta (gratis, sin API key):

```
https://api.open-meteo.com/v1/forecast?latitude=14.97&longitude=-91.79&current=temperature_2m,weather_code
```

Y la respuesta:

```json
{
  "current_units": { "temperature_2m": "°C" },
  "current": { "time": "2026-11-24T17:00", "temperature_2m": 12.4, "weather_code": 3 }
}
```

### La tabla de códigos

`weather_code` es un **número**, no un texto. La traducción está en el
diccionario `CODIGOS_CLIMA` de `clima.py`, copiado de la tabla oficial
*"WMO Weather interpretation codes (WW)"* de <https://open-meteo.com/en/docs>
(está al final de la lista de variables, en la propia página; no es un archivo
descargable).

**Ojo:** no sirve la tabla `conditions.json` de weatherapi.com. Es de otra
empresa y sus códigos son de 4 dígitos (1000, 1003, 1006...). No hay ni uno en
común con los códigos WMO (0 a 99), así que el programa correría igual pero
nunca mostraría el clima: un bug silencioso. Por eso `describir_clima()`
devuelve `"Código desconocido (NN)"` en vez de fallar — la tabla WMO tampoco
está completa en todos los modelos: los códigos 96 y 99, de granizo, solo los
reportan algunos.

### Dos decisiones de diseño

- **Si el clima falla, el viaje se muestra igual.** En `procesar_viaje()` hay
  dos `try/except ConnectionError` distintos: el de las coordenadas hace
  `return` y vuelve al menú (sin coordenadas no hay nada que calcular), y el
  del clima guarda `None` y sigue adelante (sin clima sí hay viaje que
  mostrar). Es la diferencia entre un dato esencial y un extra.
- **El clima NO se guarda en el caché.** `cache.py` guarda coordenadas porque
  no cambian nunca; la temperatura cambia cada hora. Guardarla sería un bug.
  Por eso una ciudad que viene "(desde el caché)" igual gasta una consulta a
  internet para el clima.

### Casos de prueba del clima

| Caso | Resultado |
|---|---|
| Ciudad válida (`Ogden, Estados Unidos`) | `Ogden: 5.0 °C  -  Despejado` |
| Código fuera de la tabla WMO | `Código desconocido (1000)` |
| Sin internet, ciudades ya en el caché | `clima no disponible`, y la distancia y los tiempos salen completos |

El tercero es el importante: si en vez de eso el programa te devuelve al menú,
el `try/except` del clima quedó mal puesto.

## Conversión de divisas (Paso 9)

La opción 3 del menú usa ExchangeRate-API, la tercera API del proyecto.
La opción 4 termina el programa.

1. `procesar_divisas()` pide dos códigos de moneda de tres letras, los
   convierte a mayúsculas y valida un monto finito mayor o igual a cero.
   Acepta punto o coma como separador decimal.
2. `obtener_tasa()` envía el código de origen en una petición GET a
   `https://open.er-api.com/v6/latest/{origen}`. Usa `requests` con un
   límite de espera de 10 segundos y obtiene el código de destino
   del diccionario `rates` en la respuesta.
3. `main.py` calcula `monto * tasa` y muestra un recuadro con el equivalente,
   el monto original, la tasa aplicada y la fuente. Los montos se muestran
   con dos decimales.

El servicio publica tasas diarias y su endpoint abierto funciona sin clave.
Solo se envía el código de origen. El monto se usa para el cálculo local.
[Documentación de ExchangeRate-API](https://www.exchangerate-api.com/docs/free)

| Caso | Resultado esperado |
|---|---|
| `usd` → `pen`, monto `87`, tasa simulada `3.45634` | Equivalente de `300.70 PEN` |
| Código con formato inválido | Pide un código de tres letras y regresa al menú |
| Moneda sin tasa disponible, como destino `ZZZ` | Avisa que no hay tasa y regresa al menú |
| Monto negativo o no numérico | Muestra un aviso y regresa al menú |
| Sin conexión o con tiempo de espera agotado | Avisa que no pudo consultar la tasa y regresa al menú |

## Error de certificado SSL (solo en la computadora de Eduardo)

Norton inspecciona el tráfico HTTPS y Python no reconocía su certificado, así
que `requests` fallaba con `CERTIFICATE_VERIFY_FAILED` aunque sí hubiera
internet. Se arregló juntando los certificados de `certifi` con el de Norton en
un solo archivo y apuntando las variables de entorno del usuario:

```
setx REQUESTS_CA_BUNDLE "C:\Users\TU-USUARIO\.certs\ca-bundle.pem"
setx SSL_CERT_FILE "C:\Users\TU-USUARIO\.certs\ca-bundle.pem"
```

Hay que abrir una terminal nueva para que tome efecto. Es configuración de esa
computadora, no del proyecto: en otras máquinas el código corre tal cual.

## Nota sobre acentos

En Windows la consola no usa UTF-8 por defecto, por eso `main.py` empieza
con `sys.stdout.reconfigure(encoding="utf-8")`.

## Flujo del caché de coordenadas

Extensión: el programa recuerda las ciudades que ya buscó, en
`data/coordenadas_cache.json`. Vive dentro de `api.py`, así que `main.py` no se
entera: sigue llamando solo a `obtener_coordenadas()`.

```
Usuario escribe "Layton, Estados Unidos"
            │
            ▼
┌───────────────────────────────────────────────────────────┐
│ api.py                                                    │
│                                                           │
│ 1. normalizar_llave()                                     │
│    "  LAYTON , Estados Unídos" → "layton, estados unidos" │
│       (minúsculas · sin espacios de más · sin acentos)    │
│            │                                              │
│            ▼                                              │
│ 2. cargar_cache()  ←── data/coordenadas_cache.json        │
│            │                                              │
│            ├── ¿la llave ya está guardada?                │
│            │      └─► SÍ ─► devuelve las coordenadas      │
│            │                desde_cache = True            │
│            │                (0 ms de red)                 │
│            │                                              │
│            └── ¿no está?                                  │
│                   │                                       │
│                   ▼                                       │
│ 3. requests.get() ──► Open-Meteo                          │
│                   │                                       │
│                   ├── ¿respondió bien?                    │
│                   │      └─► guardar_cache()  ← se agrega │
│                   │          devuelve las coordenadas     │
│                   │          desde_cache = False          │
│                   │                                       │
│                   └── ¿falló? (sin internet, no existe,   │
│                   │            timeout, formato malo)     │
│                          └─► None o ConnectionError      │
│                              NO se guarda nada en el JSON │
└───────────────────────────────────────────────────────────┘
            │
            ▼
main.py imprime el resultado
(le agrega "(desde el caché)" si desde_cache era True)
```

Dos decisiones que vale la pena explicar:

- **Solo se guardan las búsquedas exitosas.** Si guardáramos los errores, el
  programa "recordaría" que una ciudad no existe nada más porque ese día no
  había internet, y seguiría diciéndolo después.
- **La llave va normalizada.** `"Madrid, España"`, `"  MADRID ,espana"` y
  `"Madrid,Espana"` dan la misma llave `madrid, espana`. Sin esto el caché casi
  nunca acertaría, porque cada usuario escribe distinto.

El archivo `data/` está en `.gitignore`: se genera solo al correr el programa.
