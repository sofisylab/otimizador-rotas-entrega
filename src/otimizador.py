"""
otimizador.py

Núcleo do otimizador de rotas: heurística do vizinho mais próximo
(nearest neighbor) seguida de uma melhoria local por 2-opt.

Este é um problema clássico de otimização (o "problema do caixeiro
viajante" / TSP) — encontrar a ordem exata que minimiza a distância
total é computacionalmente caro para muitas paradas (o número de
rotas possíveis cresce fatorialmente). Por isso usamos heurísticas:
soluções boas e rápidas de calcular, embora não garantidamente perfeitas.
"""

from typing import List, Tuple

from src.distancia import distancia_km
from src.modelos import Parada


def distancia_total_rota(rota: List[Parada]) -> float:
    """Soma a distância de todos os trechos consecutivos da rota."""
    total = 0.0
    for i in range(len(rota) - 1):
        total += distancia_km(
            rota[i].latitude, rota[i].longitude, rota[i + 1].latitude, rota[i + 1].longitude
        )
    return total


def vizinho_mais_proximo(ponto_partida: Parada, paradas: List[Parada]) -> List[Parada]:
    """
    Constrói uma rota gulosa: a cada passo, vai para a parada não
    visitada mais próxima do ponto atual. É rápido (O(n²)), mas não
    garante a menor distância total possível — só uma boa aproximação.
    """
    nao_visitadas = paradas.copy()
    rota = [ponto_partida]
    atual = ponto_partida

    while nao_visitadas:
        mais_proxima = min(
            nao_visitadas,
            key=lambda p: distancia_km(atual.latitude, atual.longitude, p.latitude, p.longitude),
        )
        rota.append(mais_proxima)
        nao_visitadas.remove(mais_proxima)
        atual = mais_proxima

    return rota


def melhorar_com_2opt(rota: List[Parada], max_iteracoes: int = 100) -> List[Parada]:
    """
    Melhora uma rota existente com a heurística 2-opt: testa inverter
    trechos da rota e mantém a inversão se ela reduzir a distância
    total. Repete até não haver mais melhoria ou atingir o limite de
    iterações (evita loop infinito em casos raros).

    O primeiro ponto (partida) nunca é movido, pois é a origem fixa da rota.
    """
    melhor_rota = rota.copy()
    melhorou = True
    iteracoes = 0

    while melhorou and iteracoes < max_iteracoes:
        melhorou = False
        iteracoes += 1
        for i in range(1, len(melhor_rota) - 1):
            for j in range(i + 1, len(melhor_rota)):
                nova_rota = melhor_rota[:i] + melhor_rota[i : j + 1][::-1] + melhor_rota[j + 1 :]
                if distancia_total_rota(nova_rota) < distancia_total_rota(melhor_rota):
                    melhor_rota = nova_rota
                    melhorou = True

    return melhor_rota


def otimizar_rota(ponto_partida: Parada, paradas: List[Parada]) -> Tuple[List[Parada], float, float]:
    """
    Executa o pipeline completo: gera a rota inicial gulosa, melhora
    com 2-opt, e retorna a rota final junto com a distância antes e
    depois da melhoria (para mostrar o ganho obtido).
    """
    rota_inicial = vizinho_mais_proximo(ponto_partida, paradas)
    distancia_inicial = distancia_total_rota(rota_inicial)

    rota_final = melhorar_com_2opt(rota_inicial)
    distancia_final = distancia_total_rota(rota_final)

    return rota_final, distancia_inicial, distancia_final
