"""
Utilitarios para preparar dados do Animated Lower Thirds.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from buscar_liturgia import LiturgiaDoDia

QUANTIDADE_MAXIMA_DE_LOWERS = 4


@dataclass(frozen=True)
class LowerThird:
    """Representa um lower de dois campos: nome e informacao."""

    numero: int
    nome: str
    info: str


def criar_lowers_da_liturgia(
    liturgia: LiturgiaDoDia,
    celebrante: str | None = None,
) -> list[LowerThird]:
    """Cria os lowers disponiveis a partir dos dados extraidos da liturgia."""
    lower_titulo = _criar_lower_titulo(liturgia, celebrante)
    lower_leitura1 = LowerThird(
        numero=2,
        nome="Primeira Leitura",
        info=_extrair_referencia_da_primeira_leitura(liturgia.leitura1),
    )
    lower_salmo = LowerThird(
        numero=3,
        nome="Salmo Responsorial",
        info=_extrair_referencia_do_salmo(liturgia.salmo),
    )

    return [lower_titulo, lower_leitura1, lower_salmo]


def gerar_configuracao_importacao(lowers: list[LowerThird]) -> dict[str, str]:
    """Gera um dicionario compativel com a importacao do Animated Lower Thirds."""
    dados = {"lower-thirds-masterswitch": "true"}

    for numero in range(1, QUANTIDADE_MAXIMA_DE_LOWERS + 1):
        dados[f"lower-thirds-switch{numero}"] = "false"
        dados[f"alt-{numero}-name"] = ""
        dados[f"alt-{numero}-info"] = ""
        dados[f"alt-{numero}-title"] = f"Lower Third {numero}"

    for lower in lowers:
        _validar_numero_do_lower(lower.numero)
        dados[f"alt-{lower.numero}-name"] = lower.nome
        dados[f"alt-{lower.numero}-info"] = lower.info
        dados[f"alt-{lower.numero}-title"] = lower.nome

    return dados


def salvar_configuracao_importacao(dados: dict[str, str], caminho: Path) -> None:
    """Salva a configuracao em JSON para importar no painel do Animated Lower Thirds."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _criar_lower_titulo(
    liturgia: LiturgiaDoDia,
    celebrante: str | None,
) -> LowerThird:
    if celebrante:
        return LowerThird(numero=1, nome=liturgia.titulo, info=celebrante)

    return LowerThird(numero=1, nome="Liturgia Diaria", info=liturgia.titulo)


def _extrair_referencia_da_primeira_leitura(texto: str) -> str:
    primeira_linha = _primeira_linha(texto)
    match = re.search(r"\((?P<referencia>[^)]+)\)", primeira_linha)

    if match:
        return match.group("referencia")

    return primeira_linha


def _extrair_referencia_do_salmo(texto: str) -> str:
    primeira_linha = _primeira_linha(texto)
    return primeira_linha.replace("Responsorio", "").replace("Responsório", "").strip()


def _primeira_linha(texto: str) -> str:
    for linha in texto.splitlines():
        linha_limpa = linha.strip()
        if linha_limpa:
            return linha_limpa

    return ""


def _validar_numero_do_lower(numero: int) -> None:
    if numero < 1 or numero > QUANTIDADE_MAXIMA_DE_LOWERS:
        raise ValueError(f"Numero de lower invalido: {numero}")
