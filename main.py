"""
main.py

Otimizador Simples de Rotas de Entrega.

Lê um CSV com o ponto de partida e as paradas de entrega, calcula uma
rota otimizada (heurística vizinho mais próximo + melhoria 2-opt),
salva o histórico em SQLite e gera um relatório em HTML.

Uso:
    python main.py
    python main.py --csv data/minhas_paradas.csv --velocidade 30
"""

import argparse
import csv
import sys

from src.modelos import Parada
from src.otimizador import otimizar_rota
from src.db import salvar_rota, listar_historico
from src.relatorio_html import gerar_html


def carregar_paradas(caminho_csv: str):
    """
    Lê o CSV de paradas. Cada linha precisa ter: nome, latitude,
    longitude, tipo (onde tipo é "partida" ou "entrega").
    """
    registros = []
    with open(caminho_csv, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas_esperadas = {"nome", "latitude", "longitude", "tipo"}
        colunas_encontradas = set(leitor.fieldnames or [])

        if not colunas_esperadas.issubset(colunas_encontradas):
            raise ValueError(
                f"O CSV precisa conter as colunas {colunas_esperadas}. "
                f"Colunas encontradas: {colunas_encontradas}"
            )

        for linha in leitor:
            tipo = linha["tipo"].strip().lower()
            parada = Parada(
                nome=linha["nome"].strip(),
                latitude=float(linha["latitude"]),
                longitude=float(linha["longitude"]),
            )
            registros.append((tipo, parada))

    return registros


def main():
    parser = argparse.ArgumentParser(description="Otimizador simples de rotas de entrega.")
    parser.add_argument(
        "--csv",
        default="data/paradas_exemplo.csv",
        help="CSV com colunas: nome, latitude, longitude, tipo ('partida' ou 'entrega').",
    )
    parser.add_argument(
        "--velocidade",
        type=float,
        default=25.0,
        help="Velocidade média em km/h, usada para estimar o tempo (padrão: 25).",
    )
    args = parser.parse_args()

    try:
        registros = carregar_paradas(args.csv)

        partidas = [parada for tipo, parada in registros if tipo == "partida"]
        entregas = [parada for tipo, parada in registros if tipo == "entrega"]

        if len(partidas) != 1:
            raise ValueError(
                f"O CSV precisa ter exatamente 1 linha com tipo='partida'. Encontradas: {len(partidas)}."
            )
        if not entregas:
            raise ValueError("O CSV precisa ter pelo menos 1 linha com tipo='entrega'.")

        ponto_partida = partidas[0]
        print(f"Ponto de partida: {ponto_partida.nome}")
        print(f"Paradas de entrega: {len(entregas)}\n")

        rota, distancia_inicial, distancia_final = otimizar_rota(ponto_partida, entregas)

        print("Rota otimizada:")
        for i, parada in enumerate(rota):
            print(f"  {i}. {parada.nome}")

        economia = round(distancia_inicial - distancia_final, 2)
        economia_pct = round((economia / distancia_inicial) * 100, 1) if distancia_inicial > 0 else 0
        tempo_estimado = round((distancia_final / args.velocidade) * 60)

        print(f"\nDistância antes do 2-opt (ordem gulosa): {distancia_inicial:.2f} km")
        print(f"Distância depois do 2-opt (rota final):   {distancia_final:.2f} km")
        print(f"Redução obtida pelo 2-opt: {economia:.2f} km ({economia_pct}%)")
        print(f"Tempo estimado da rota final: {tempo_estimado} min (a {args.velocidade} km/h)")

        salvar_rota(len(entregas), distancia_inicial, distancia_final, [p.nome for p in rota])

        html = gerar_html(rota, distancia_inicial, distancia_final, args.velocidade)
        with open("output/relatorio_rota.html", "w", encoding="utf-8") as arquivo_html:
            arquivo_html.write(html)
        print("\nRelatório visual salvo em output/relatorio_rota.html")

        print("\nÚltimas rotas calculadas (histórico salvo em SQLite):")
        for linha in listar_historico(5):
            data_hora, qtd, dist_inicial, dist_final, economia_hist = linha
            print(
                f"  [{data_hora}] {qtd} paradas | {dist_inicial} km -> {dist_final} km "
                f"(economia: {economia_hist} km)"
            )

    except (FileNotFoundError, ValueError) as erro:
        print(f"\nErro: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
