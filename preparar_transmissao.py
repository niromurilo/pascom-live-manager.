"""
Pascom Live Manager
Fluxo único: busca a liturgia uma vez e gera todos os arquivos da transmissão.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from animated_lower_thirds import criar_lowers_da_liturgia, gerar_e_validar_json_dos_lowers, montar_resumo_dos_lowers
from buscar_liturgia import URL_LITURGIA, buscar_liturgia_ou_none
from config import NOME_PAROQUIA
from gerador_descricao import gerar_descricao, gerar_titulo, salvar_texto

PASTA_SAIDA_PADRAO = Path("output")
NOME_ARQUIVO_JSON = "animated_lower_thirds_liturgia.json"
NOME_ARQUIVO_TITULO = "titulo.txt"
NOME_ARQUIVO_DESCRICAO = "descricao.txt"
NOME_ARQUIVO_RESUMO = "resumo.txt"


def parse_args() -> argparse.Namespace:
    """Lê os argumentos opcionais do script."""
    parser = argparse.ArgumentParser(
        description="Prepara todos os arquivos da transmissão a partir da liturgia do dia.",
    )
    parser.add_argument("--celebrante", help="Nome do celebrante usado no Lower 1 e na descrição.")
    parser.add_argument("--paroquia", help="Sobrepõe NOME_PAROQUIA do .env, se informado.")
    parser.add_argument("--pasta-saida", type=Path, default=PASTA_SAIDA_PADRAO, help="Pasta onde os arquivos serão gerados.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    nome_paroquia = args.paroquia or NOME_PAROQUIA
    if not nome_paroquia:
        print("❌ Nome da paróquia não informado. Defina NOME_PAROQUIA no .env ou use --paroquia.")
        return

    hoje = date.today()

    liturgia = buscar_liturgia_ou_none(URL_LITURGIA)
    if liturgia is None:
        return

    caminho_json = args.pasta_saida / NOME_ARQUIVO_JSON
    lowers = criar_lowers_da_liturgia(liturgia, celebrante=args.celebrante)
    if not gerar_e_validar_json_dos_lowers(lowers, caminho_json):
        return

    titulo = gerar_titulo(liturgia, hoje)
    descricao = gerar_descricao(liturgia, hoje, nome_paroquia=nome_paroquia, celebrante=args.celebrante)
    caminho_titulo = args.pasta_saida / NOME_ARQUIVO_TITULO
    caminho_descricao = args.pasta_saida / NOME_ARQUIVO_DESCRICAO

    try:
        salvar_texto(titulo, caminho_titulo)
        salvar_texto(descricao, caminho_descricao)
    except OSError as erro:
        print(f"❌ Problema ao salvar título/descrição: {erro}")
        return

    caminho_resumo = args.pasta_saida / NOME_ARQUIVO_RESUMO
    resumo = "\n\n".join([
    f"TÍTULO DO VÍDEO:\n{titulo}",
    f"DESCRIÇÃO DO VÍDEO:\n{descricao}",
    f"LOWER THIRDS:\n{montar_resumo_dos_lowers(liturgia, lowers, caminho_json)}",
    "ARQUIVOS GERADOS:",
    f"• {caminho_json}",
    f"• {caminho_titulo}",
    f"• {caminho_descricao}",
    f"• {caminho_resumo}",
    ])

    try:
        salvar_texto(resumo, caminho_resumo)
    except OSError as erro:
        print(f"❌ Problema ao salvar o resumo: {erro}")
        return

    print("✅ Transmissão preparada com sucesso!\n")
    print(resumo)
    print("\n➡️  Abra o painel do Animated Lower Thirds no OBS e clique em Import.")


if __name__ == "__main__":
    main()