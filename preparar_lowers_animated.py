"""
Gera um arquivo de importacao para o Animated Lower Thirds com a liturgia do dia.
"""

from __future__ import annotations
import argparse
from pathlib import Path
CAMINHO_PADRAO_SAIDA = Path("output/animated_lower_thirds_liturgia.json")
from buscar_liturgia import (
    URL_LITURGIA,
    LiturgiaDoDia,
    buscar_liturgia_ou_none
)

from animated_lower_thirds import (
    LowerThird,
    criar_lowers_da_liturgia,
    gerar_e_validar_json_dos_lowers,
    montar_resumo_dos_lowers
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

    liturgia = buscar_liturgia_ou_none(URL_LITURGIA)
    if liturgia is None:
        return

    lowers = criar_lowers_da_liturgia(liturgia, celebrante=args.celebrante)

    if not gerar_e_validar_json_dos_lowers(lowers, args.saida):
        return

    print("✅ JSON gerado e validado com sucesso!\n")
    print(montar_resumo_dos_lowers(liturgia, lowers, args.saida))
    print("\n➡️  Abra o painel do Animated Lower Thirds no OBS e clique em Import.")


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