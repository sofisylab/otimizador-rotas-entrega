"""
distancia.py

Cálculo de distância entre duas coordenadas geográficas usando a
fórmula de Haversine (distância em linha reta sobre a superfície
da Terra, em quilômetros).
"""

import math

RAIO_TERRA_KM = 6371.0


def distancia_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = (math.radians(v) for v in [lat1, lon1, lat2, lon2])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return RAIO_TERRA_KM * c
