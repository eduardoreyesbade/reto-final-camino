# Notas técnicas

## Estado de los pasos del proyecto

| Paso | Qué pedía | Dónde quedó |
|---|---|---|
| Paso 4 | Menú, validaciones, unidad y resumen | `main.py` |
| Paso 5 | API de geocodificación Open-Meteo | `api.py` (+ `pruebas_api.py`) |
| Siguiente | Distancia (Haversine) y tiempos | `utils.py` (pendiente) |
| 21 nov | Clase `Ciudad` (POO) | `ciudad.py` (pendiente) |

## Casos de prueba de la API

| Caso | Resultado |
|---|---|
| Ciudad conocida (`Madrid, España`) | `lat 40.4165, lon -3.7026` |
| Ciudad inventada (`Xyzabc, Nolandia`) | "No encontramos…" y vuelve a preguntar |
| Sin internet (wifi apagado) | "No se pudo conectar con la API…" y el programa sigue vivo |
| Falta el país (`Madrid`) | Avisa del formato "ciudad, país" |

Para correrlos: `python pruebas_api.py`

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

En Windows la consola no usa UTF-8 por defecto, por eso `main.py` y
`pruebas_api.py` empiezan con `sys.stdout.reconfigure(encoding="utf-8")`.
