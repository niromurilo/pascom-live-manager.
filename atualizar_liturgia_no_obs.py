"""
Pascom Live Manager
Sprint 2: buscar a liturgia do dia e atualizar fontes no OBS.
"""

import obsws_python as obs

from buscar_liturgia import (
    URL_LITURGIA,
    LiturgiaDoDia,
    buscar_html_da_liturgia,
    extrair_liturgia,
)
from sprint1_titulo import (
    OBS_HOST,
    OBS_PORT,
    OBS_SENHA,
    atualizar_texto_da_fonte,
)

FONTE_TITULO = "PLM_TITULO"
FONTE_LEITURA1 = "PLM_LEITURA1"
FONTE_SALMO = "PLM_SALMO"


def buscar_liturgia_do_dia() -> LiturgiaDoDia:
    """Busca a pagina da liturgia e devolve os dados estruturados."""
    html = buscar_html_da_liturgia(URL_LITURGIA)
    return extrair_liturgia(html)


def atualizar_fontes_da_liturgia(cliente: obs.ReqClient, liturgia: LiturgiaDoDia) -> None:
    """Atualiza no OBS as fontes de texto usadas pela liturgia."""
    atualizar_texto_da_fonte(cliente, FONTE_TITULO, liturgia.titulo)
    atualizar_texto_da_fonte(cliente, FONTE_LEITURA1, liturgia.leitura1)
    atualizar_texto_da_fonte(cliente, FONTE_SALMO, liturgia.salmo)


def main() -> None:
    liturgia = buscar_liturgia_do_dia()

    with obs.ReqClient(
        host=OBS_HOST,
        port=OBS_PORT,
        password=OBS_SENHA,
        timeout=3,
    ) as cliente:
        atualizar_fontes_da_liturgia(cliente, liturgia)

    print("Fontes da liturgia atualizadas no OBS com sucesso!")


if __name__ == "__main__":
    main()
