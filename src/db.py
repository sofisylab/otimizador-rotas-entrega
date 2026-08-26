"""
db.py

Persistência simples do histórico de rotas calculadas, usando SQLite
(banco de dados em um único arquivo, sem precisar instalar/configurar
um servidor de banco de dados separado).
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple

CAMINHO_BANCO = "output/historico_rotas.db"


def _conectar() -> sqlite3.Connection:
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS rotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            quantidade_paradas INTEGER NOT NULL,
            distancia_inicial_km REAL NOT NULL,
            distancia_final_km REAL NOT NULL,
            economia_km REAL NOT NULL,
            ordem_paradas TEXT NOT NULL
        )
        """
    )
    return conexao


def salvar_rota(
    quantidade_paradas: int,
    distancia_inicial: float,
    distancia_final: float,
    ordem_nomes: List[str],
) -> None:
    conexao = _conectar()
    economia = round(distancia_inicial - distancia_final, 2)
    conexao.execute(
        """
        INSERT INTO rotas
            (data_hora, quantidade_paradas, distancia_inicial_km, distancia_final_km, economia_km, ordem_paradas)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(timespec="seconds"),
            quantidade_paradas,
            round(distancia_inicial, 2),
            round(distancia_final, 2),
            economia,
            " -> ".join(ordem_nomes),
        ),
    )
    conexao.commit()
    conexao.close()


def listar_historico(limite: int = 10) -> List[Tuple]:
    conexao = _conectar()
    cursor = conexao.execute(
        """
        SELECT data_hora, quantidade_paradas, distancia_inicial_km, distancia_final_km, economia_km
        FROM rotas
        ORDER BY id DESC
        LIMIT ?
        """,
        (limite,),
    )
    linhas = cursor.fetchall()
    conexao.close()
    return linhas
