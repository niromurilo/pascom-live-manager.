"""
Gera um arquivo de importacao para o Animated Lower Thirds com a liturgia do dia.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import requests
CAMINHO_PADRAO_SAIDA = Path("output/animated_lower_thirds_liturgia.json")
from buscar_liturgia import (
    URL_LITURGIA,
    buscar_html_da_liturgia,
    extrair_liturgia,
    LiturgiaDoDia,
)

from animated_lower_thirds import (
    LowerThird,
    criar_lowers_da_liturgia,
    gerar_configuracao_importacao,
    salvar_configuracao_importacao,
    validar_configuracao_gerada,
)

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

    try:
        html = buscar_html_da_liturgia(URL_LITURGIA)
        liturgia = extrair_liturgia(html)
    except requests.exceptions.RequestException as erro:
        print(f"❌ Não consegui buscar a liturgia (problema de conexão): {erro}")
        return
    except ValueError as erro:
        print(f"❌ A página da liturgia mudou de estrutura e a extração falhou: {erro}")
        print("   Avise quem cuida do projeto — provavelmente precisa ajustar o scraping.")
        return

    lowers = criar_lowers_da_liturgia(liturgia, celebrante=args.celebrante)
    dados = gerar_configuracao_importacao(lowers)

    try:
        salvar_configuracao_importacao(dados, args.saida)
        validar_configuracao_gerada(lowers, args.saida)
    except (OSError, ValueError) as erro:
        print(f"❌ Problema ao gerar o arquivo: {erro}")
        return

    _imprimir_resumo(liturgia, lowers, args.saida)


def _imprimir_resumo(liturgia: LiturgiaDoDia, lowers: list[LowerThird], caminho: Path) -> None:
    """Mostra o que foi gerado, pra conferência antes do Import manual."""
    print("✅ JSON gerado e validado com sucesso!\n")
    print(f"   Título: {liturgia.titulo}")
    for lower in lowers:
        slot_txt = f" slot {lower.slot}" if lower.slot else ""
        print(f"   Painel {lower.painel}{slot_txt} — {lower.nome}: {lower.info}")
    print(f"\n   Arquivo: {caminho}")
    print("\n➡️  Abra o painel do Animated Lower Thirds no OBS e clique em Import.")

if __name__ == "__main__":
    main()