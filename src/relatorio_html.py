"""
relatorio_html.py

Gera um relatório em HTML simples e legível com a rota otimizada,
sem depender de nenhuma biblioteca externa de front-end.
"""

from typing import List

from src.distancia import distancia_km
from src.modelos import Parada


def gerar_html(
    rota: List[Parada],
    distancia_inicial: float,
    distancia_final: float,
    velocidade_media_kmh: float = 25.0,
) -> str:
    tempo_estimado_min = round((distancia_final / velocidade_media_kmh) * 60)
    economia_km = round(distancia_inicial - distancia_final, 2)
    economia_pct = round((economia_km / distancia_inicial) * 100, 1) if distancia_inicial > 0 else 0

    linhas_tabela = ""
    distancia_acumulada = 0.0
    for i, parada in enumerate(rota):
        if i > 0:
            trecho = distancia_km(
                rota[i - 1].latitude, rota[i - 1].longitude, parada.latitude, parada.longitude
            )
            distancia_acumulada += trecho
            trecho_str = f"{trecho:.2f} km"
        else:
            trecho_str = "— (ponto de partida)"

        linhas_tabela += f"""
        <tr>
            <td>{i}</td>
            <td>{parada.nome}</td>
            <td>{trecho_str}</td>
            <td>{distancia_acumulada:.2f} km</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Relatório de Rota Otimizada</title>
<style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f8; color: #222; padding: 2rem; }}
    .container {{ max-width: 700px; margin: 0 auto; background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
    h1 {{ color: #2c3e50; font-size: 1.4rem; }}
    .resumo {{ display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }}
    .cartao {{ background: #ecf6ff; border-radius: 8px; padding: 1rem; flex: 1; min-width: 140px; text-align: center; }}
    .cartao .valor {{ font-size: 1.4rem; font-weight: bold; color: #2980b9; }}
    .cartao .rotulo {{ font-size: 0.8rem; color: #555; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
    th, td {{ text-align: left; padding: 0.5rem 0.7rem; border-bottom: 1px solid #eee; font-size: 0.9rem; }}
    th {{ background: #2c3e50; color: white; }}
    tr:nth-child(even) {{ background: #fafafa; }}
</style>
</head>
<body>
<div class="container">
    <h1>🛵 Relatório de Rota Otimizada</h1>
    <div class="resumo">
        <div class="cartao"><div class="valor">{len(rota) - 1}</div><div class="rotulo">Paradas</div></div>
        <div class="cartao"><div class="valor">{distancia_final:.2f} km</div><div class="rotulo">Distância total</div></div>
        <div class="cartao"><div class="valor">{tempo_estimado_min} min</div><div class="rotulo">Tempo estimado*</div></div>
        <div class="cartao"><div class="valor">{economia_pct}%</div><div class="rotulo">Redução vs. rota inicial</div></div>
    </div>
    <table>
        <tr><th>#</th><th>Parada</th><th>Trecho</th><th>Acumulado</th></tr>
        {linhas_tabela}
    </table>
    <p style="font-size:0.75rem;color:#888;margin-top:1rem;">
        *Tempo estimado considerando velocidade média de {velocidade_media_kmh} km/h.
        Distância calculada em linha reta (aproximação, fórmula de Haversine).
    </p>
</div>
</body>
</html>"""
