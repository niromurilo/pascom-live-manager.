"""
Pascom Live Manager

Gera o título e a descrição da transmissão a partir da liturgia do dia.
"""

from __future__ import annotations

from datetime import date

from buscar_liturgia import (
    LiturgiaDoDia,
    extrair_citacao,
    extrair_citacao_do_salmo,
)

def gerar_titulo(liturgia: LiturgiaDoDia, data: date) -> str:
    """Gera o título da transmissão."""
    return f"Santa Missa | {liturgia.titulo} | {data.strftime('%d/%m/%Y')}"


def gerar_descricao(
    liturgia: LiturgiaDoDia,
    data: date,
    nome_paroquia: str,
    celebrante: str | None = None,
) -> str:
    """Gera a descrição da transmissão."""

    descricao = (
        f"Santa Missa - {liturgia.titulo}\n"
        f"{nome_paroquia}\n"
        f"Data: {data.strftime('%d/%m/%Y')}\n"
    )

    if celebrante:
        descricao += f"Celebrante: {celebrante}\n"

    descricao += "\nLeituras do dia:\n"
    descricao += f"• 1ª Leitura: {extrair_citacao(liturgia.leitura1)}\n"

    if liturgia.leitura2:
        descricao += f"• 2ª Leitura: {extrair_citacao(liturgia.leitura2)}\n"

    descricao += f"• Salmo: {extrair_citacao_do_salmo(liturgia.salmo)}\n"
    descricao += f"• Evangelho: {extrair_citacao(liturgia.evangelho)}"

    return descricao