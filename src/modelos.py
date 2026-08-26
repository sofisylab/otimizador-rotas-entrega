"""
modelos.py

Estrutura de dados que representa uma parada de entrega
(pode ser o ponto de partida ou um destino de entrega).
"""

from dataclasses import dataclass


@dataclass
class Parada:
    nome: str
    latitude: float
    longitude: float
