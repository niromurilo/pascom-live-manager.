"""
Gera um arquivo de importacao para o Animated Lower Thirds com a liturgia do dia.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from animated_lower_thirds import (
    criar_lowers_da_liturgia,
    gerar_configuracao_importacao,
    salvar_configuracao_importacao,
)
from buscar_liturgia import URL_LITURGIA, buscar_html_da_liturgia, extrair_liturgia

CAMINHO_PADRAO_SAIDA = Path("output/animated_lower_thirds_liturgia.json")


def parse_args() -> argparse.Namespace:
    """Le os argumentos opcionais do script."""
    parser = argparse.ArgumentParser(
        description="Prepara os lowers da liturgia para o Animated Lower Thirds.",
    )
    parser.add_argument(
        "--celebrante",
        help="Nome do celebrante usado no Lower 1.",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=CAMINHO_PADRAO_SAIDA,
        help="Caminho do arquivo JSON gerado.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    html = buscar_html_da_liturgia(URL_LITURGIA)
    liturgia = extrair_liturgia(html)
    lowers = criar_lowers_da_liturgia(liturgia, celebrante=args.celebrante)
    dados = gerar_configuracao_importacao(lowers)

    salvar_configuracao_importacao(dados, args.saida)

    print(f"Arquivo gerado: {args.saida}")
    print("Importe esse JSON no painel do Animated Lower Thirds.")


if __name__ == "__main__":
    main()
