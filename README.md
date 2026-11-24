# Camino a mi casa

Es el programa del Poryecto Final.  de **CS 1400 — Weber State University**, otoño 2026.

Programa de consola en Python que calcula la distancia en línea recta entre dos
ciudades del mundo y estima cuánto tomaría el viaje en avión y en auto.

La idea detrás del proyecto es conectar dos lugares que significan algo: donde
estás y donde está tu casa.

**Integrantes:**
Tito Huerta y Eduardo Reyes

---

## Qué hace

1. Te pide una ciudad de origen y una de destino (formato `ciudad, país`).
2. Te pregunta si prefieres ver la distancia en kilómetros o en millas.
3. Busca las coordenadas de cada lugar en la API de **Open-Meteo Geocoding**.
4. Calcula la distancia con la fórmula de **Haversine**.
5. Estima el tiempo de viaje en avión (800 km/h) y en auto (80 km/h).
6. Muestra un resumen con todo.
7. Muestra -si estan disponible- la informacion del clima en los lugares solicitados.

Las consultas se guardan en un caché local, así que si buscas la misma ciudad
dos veces la segunda es instantánea y no gasta internet.

---

## Requisitos

- **Python 3.10 o superior**
- La librería `requests`
- Conexión a internet (solo para ciudades que no estén en el caché)

---

## Cómo correrlo

**1. Clona el repositorio:**

```bash
git clone https://github.com/eduardoreyesbade/reto-final-camino.git
cd reto-final-camino
```

**2. Instala la dependencia:**

```bash
pip install -r requirements.txt
```

**3. Corre el programa:**

```bash
python main.py
```

En algunas computadoras el comando es `python3` en vez de `python`.

### Probar las piezas por separado

Cada módulo se puede correr solo, sin el menú:

```bash
python utils.py        # prueba los cálculos (Madrid-París debe dar ~1,053 km)
python ciudad.py       # prueba la clase Ciudad y su método distancia_a()
```
---

## Nota sobre la distancia

La distancia es **en línea recta** sobre la superficie de la Tierra, no por
carretera. Los tiempos de viaje son estimaciones con velocidades promedio
constantes: no consideran escalas, tráfico, paradas ni fronteras.

---

## Autores

Tito Huerta y Eduardo Reyes
CS 1400 — Weber State University — Fall 2026
