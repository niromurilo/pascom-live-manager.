"""
Utilitarios para preparar dados do Animated Lower Thirds.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from buscar_liturgia import (
    LiturgiaDoDia,
    extrair_citacao,
    extrair_citacao_do_salmo,
)

QUANTIDADE_MAXIMA_DE_PAINEIS = 4
QUANTIDADE_MAXIMA_DE_SLOTS = 10
PAINEL_TITULO = 1
PAINEL_LEITURAS = 2


@dataclass(frozen=True)
class LowerThird:
    """Representa um valor a publicar num Lower Third do Animated Lower Thirds.

    slot=None -> valor "ativo" do painel (usado hoje só pelo título).
    slot=1..10 -> memory slot específico dentro do painel.
    """

    painel: int
    nome: str
    info: str
    slot: int | None = None


def criar_lowers_da_liturgia(
    liturgia: LiturgiaDoDia,
    celebrante: str | None = None,
) -> list[LowerThird]:
    """Cria os lowers disponiveis a partir dos dados extraidos da liturgia."""
    lower_titulo = _criar_lower_titulo(liturgia, celebrante)
    sequencia_de_leituras = _criar_sequencia_de_leituras(liturgia)

    return [lower_titulo, *sequencia_de_leituras]


def gerar_configuracao_importacao(lowers: list[LowerThird]) -> dict[str, str]:
    """Gera um dicionario compativel com a importacao do Animated Lower Thirds."""
    dados = {"lower-thirds-masterswitch": "true"}

    for painel in range(1, QUANTIDADE_MAXIMA_DE_PAINEIS + 1):
        dados[f"lower-thirds-switch{painel}"] = "false"
        dados[f"alt-{painel}-name"] = ""
        dados[f"alt-{painel}-info"] = ""
        dados[f"alt-{painel}-title"] = f"Lower Third {painel}"

    dados.update(_resetar_slots_do_painel(PAINEL_LEITURAS))

    for lower in lowers:
        _validar_painel(lower.painel)

        if lower.slot is None:
            dados[f"alt-{lower.painel}-name"] = lower.nome
            dados[f"alt-{lower.painel}-info"] = lower.info
            dados[f"alt-{lower.painel}-title"] = lower.nome
        else:
            _validar_slot(lower.slot)
            dados[f"alt-{lower.painel}-name-{lower.slot}"] = lower.nome
            dados[f"alt-{lower.painel}-info-{lower.slot}"] = lower.info

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
    """Monta o Lower Third do título/celebrante — painel 1, valor único, sem slot."""
    if celebrante:
        return LowerThird(painel=PAINEL_TITULO, nome=liturgia.titulo, info=celebrante)

    return LowerThird(painel=PAINEL_TITULO, nome="Liturgia Diaria", info=liturgia.titulo)


def _criar_sequencia_de_leituras(liturgia: LiturgiaDoDia) -> list[LowerThird]:
    """Monta a sequencia de leituras no painel 2, um slot por item, na ordem da missa."""
    sequencia = [
        LowerThird(
            painel=PAINEL_LEITURAS,
            nome="Primeira Leitura",
            info=extrair_citacao(liturgia.leitura1),
            slot=1,
        ),
        LowerThird(
            painel=PAINEL_LEITURAS,
            nome="Salmo Responsorial",
            info=extrair_citacao_do_salmo(liturgia.salmo),
            slot=2,
        ),
    ]

    proximo_slot = 3
    if liturgia.leitura2 is not None:
        sequencia.append(
            LowerThird(
                painel=PAINEL_LEITURAS,
                nome="Segunda Leitura",
                info=extrair_citacao(liturgia.leitura2),
                slot=proximo_slot,
            )
        )
        proximo_slot += 1

    sequencia.append(
        LowerThird(
            painel=PAINEL_LEITURAS,
            nome="Evangelho",
            info=extrair_citacao(liturgia.evangelho),
            slot=proximo_slot,
        )
    )

    return sequencia


def _resetar_slots_do_painel(painel: int) -> dict[str, str]:
    """Limpa os slots de memoria de um painel antes de preenche-los de novo.

    Evita que um slot usado ontem (ex: leitura2 num domingo) sobreviva
    escondido num dia em que ele nao deveria existir.
    """
    dados: dict[str, str] = {}
    for slot in range(1, QUANTIDADE_MAXIMA_DE_SLOTS + 1):
        dados[f"alt-{painel}-name-{slot}"] = ""
        dados[f"alt-{painel}-info-{slot}"] = ""

    return dados


def _validar_painel(painel: int) -> None:
    if painel < 1 or painel > QUANTIDADE_MAXIMA_DE_PAINEIS:
        raise ValueError(f"Numero de painel invalido: {painel}")


def _validar_slot(slot: int) -> None:
    if slot < 1 or slot > QUANTIDADE_MAXIMA_DE_SLOTS:
        raise ValueError(f"Numero de slot invalido: {slot}")

def validar_configuracao_gerada(lowers: list[LowerThird], caminho: Path) -> None:
    """Valida o JSON gerado antes do operador importar no Animated Lower Thirds.

    Confere que o arquivo existe, é JSON válido, e que cada lower que
    deveria ter sido escrito de fato aparece no arquivo com conteúdo não
    vazio. Levanta ValueError com mensagem clara em caso de problema —
    nunca falha silenciosamente, nunca deixa o operador importar um JSON
    quebrado sem saber.
    """
    if not caminho.exists():
        raise ValueError(f"Arquivo não foi criado: {caminho}")

    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        raise ValueError(f"Arquivo gerado não é um JSON válido: {erro}") from erro

    for lower in lowers:
        if lower.slot is None:
            chave_nome = f"alt-{lower.painel}-name"
            chave_info = f"alt-{lower.painel}-info"
        else:
            chave_nome = f"alt-{lower.painel}-name-{lower.slot}"
            chave_info = f"alt-{lower.painel}-info-{lower.slot}"

        if not dados.get(chave_nome):
            raise ValueError(f"Campo '{chave_nome}' ficou vazio no JSON gerado ({lower.nome}).")
        if not dados.get(chave_info):
            raise ValueError(f"Campo '{chave_info}' ficou vazio no JSON gerado ({lower.nome}).")
        
def gerar_e_validar_json_dos_lowers(lowers: list[LowerThird], caminho: Path) -> bool:
    """Salva e valida o JSON dos lowers, imprimindo mensagem amigável em caso de erro.

    Retorna True se tudo correu bem, False se falhou — quem chama decide
    o que fazer a seguir.
    """
    try:
        dados = gerar_configuracao_importacao(lowers)
        salvar_configuracao_importacao(dados, caminho)
        validar_configuracao_gerada(lowers, caminho)
        return True
    except (OSError, ValueError) as erro:
        print(f"❌ Problema ao gerar o arquivo: {erro}")
        return False


def montar_resumo_dos_lowers(liturgia: LiturgiaDoDia, lowers: list[LowerThird], caminho: Path) -> str:
    """Monta o texto de resumo dos lowers gerados, pra impressão ou gravação em arquivo."""
    linhas = [f"Título: {liturgia.titulo}"]
    for lower in lowers:
        slot_txt = f" slot {lower.slot}" if lower.slot else ""
        linhas.append(f"Painel {lower.painel}{slot_txt} — {lower.nome}: {lower.info}")
    linhas.append(f"\nArquivo: {caminho}")
    return "\n".join(linhas)