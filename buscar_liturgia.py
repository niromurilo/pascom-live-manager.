"""
Pascom Live Manager
Sprint 2 - Etapa 3: estruturar os dados da liturgia numa dataclass.
"""

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

URL_LITURGIA = "https://liturgia.cancaonova.com/pb/"


@dataclass(frozen=True)
class LiturgiaDoDia:
    """Representa os dados da liturgia de um dia específico."""
    titulo: str
    leitura1: str
    salmo: str


def buscar_html_da_liturgia(url: str) -> str:
    """Busca o HTML da página de liturgia e retorna como texto bruto."""
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    return resposta.text


def _texto_paragrafos(container: Tag) -> str:
    """Extrai o texto de um container, um parágrafo por linha."""
    linhas = []
    for p in container.find_all("p"):
        texto = p.get_text(strip=True).replace("\xa0", " ")
        if texto:
            linhas.append(texto)
    return "\n".join(linhas)


def extrair_liturgia(html: str) -> LiturgiaDoDia:
    """Extrai título, primeira leitura e salmo do HTML da Canção Nova."""
    soup = BeautifulSoup(html, "html.parser")

    titulo_tag = soup.find("meta", attrs={"property": "og:title"})
    if titulo_tag is None:
        raise ValueError("Não encontrei o título (meta og:title) na página.")
    titulo = titulo_tag["content"]

    leitura1_div = soup.find("div", id="liturgia-1")
    if leitura1_div is None:
        raise ValueError("Não encontrei a primeira leitura (div#liturgia-1) na página.")
    leitura1 = _texto_paragrafos(leitura1_div)

    salmo_div = soup.find("div", id="liturgia-2")
    if salmo_div is None:
        raise ValueError("Não encontrei o salmo (div#liturgia-2) na página.")
    salmo = _texto_paragrafos(salmo_div)

    return LiturgiaDoDia(titulo=titulo, leitura1=leitura1, salmo=salmo)


def main() -> None:
    html = buscar_html_da_liturgia(URL_LITURGIA)
    liturgia = extrair_liturgia(html)

    print("TÍTULO:", liturgia.titulo)
    print()
    print("1ª LEITURA:")
    print(liturgia.leitura1)
    print()
    print("SALMO:")
    print(liturgia.salmo)


if __name__ == "__main__":
    main()