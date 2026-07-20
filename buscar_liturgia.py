"""
Pascom Live Manager
Sprint 2 - busca, extrai e estrutura a liturgia do dia (Canção Nova).
"""

from __future__ import annotations
from config import REQUEST_TIMEOUT
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

URL_LITURGIA = "https://liturgia.cancaonova.com/pb/"


@dataclass(frozen=True)
class LiturgiaDoDia:
    """Representa os dados da liturgia de um dia especifico."""

    titulo: str
    leitura1: str
    salmo: str
    evangelho: str
    leitura2: str | None = None


def buscar_html_da_liturgia(url: str) -> str:
    """Busca o HTML da pagina de liturgia e retorna como texto bruto."""
    resposta = requests.get(url, timeout=REQUEST_TIMEOUT)
    resposta.raise_for_status()
    return resposta.text


def extrair_liturgia(html: str) -> LiturgiaDoDia:
    """Extrai titulo, leituras, salmo e evangelho do HTML da Cancao Nova."""
    soup = BeautifulSoup(html, "html.parser")

    titulo_tag = soup.find("meta", attrs={"property": "og:title"})
    if titulo_tag is None:
        raise ValueError("Nao encontrei o titulo (meta og:title) na pagina.")
    titulo = titulo_tag["content"]

    leitura1_div = soup.find("div", id="liturgia-1")
    if leitura1_div is None:
        raise ValueError("Nao encontrei a primeira leitura (div#liturgia-1) na pagina.")
    leitura1 = _texto_paragrafos(leitura1_div)

    salmo_div = soup.find("div", id="liturgia-2")
    if salmo_div is None:
        raise ValueError("Nao encontrei o salmo (div#liturgia-2) na pagina.")
    salmo = _texto_paragrafos(salmo_div)

    evangelho_div = soup.find("div", id="liturgia-4")
    if evangelho_div is None:
        raise ValueError("Nao encontrei o evangelho (div#liturgia-4) na pagina.")
    evangelho = _texto_paragrafos(evangelho_div)

    leitura2_div = soup.find("div", id="liturgia-3")
    leitura2 = _texto_paragrafos(leitura2_div) if leitura2_div is not None else None

    return LiturgiaDoDia(
        titulo=titulo,
        leitura1=leitura1,
        salmo=salmo,
        evangelho=evangelho,
        leitura2=leitura2,
    )


def _texto_paragrafos(container: Tag) -> str:
    """Extrai o texto de um container, um paragrafo por linha."""
    linhas = []
    for p in container.find_all("p"):
        texto = p.get_text().replace("\xa0", " ")
        texto = re.sub(r"\s+", " ", texto).strip()
        if texto:
            linhas.append(texto)
    return "\n".join(linhas)


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
    print()
    print("2ª LEITURA:", "—" if liturgia.leitura2 is None else "")
    if liturgia.leitura2:
        print(liturgia.leitura2)
    print()
    print("EVANGELHO:")
    print(liturgia.evangelho)

def _primeira_linha(texto: str) -> str:
    for linha in texto.splitlines():
        linha_limpa = linha.strip()
        if linha_limpa:
            return linha_limpa

    return ""

def extrair_citacao (texto: str) -> str:
    """Extrai a citacao biblica (livro, capitulo e versiculo) da primeira linha do texto."""
    primeira_linha = _primeira_linha(texto)
    match = re.search(r"\((?P<referencia>[^)]+)\)", primeira_linha)

    if match:
        return match.group("referencia")

    return primeira_linha


def extrair_citacao_do_salmo(texto: str) -> str:
    primeira_linha = _primeira_linha(texto)
    return primeira_linha.replace("Responsorio", "").replace("Responsório", "").strip()

if __name__ == "__main__":
    main()