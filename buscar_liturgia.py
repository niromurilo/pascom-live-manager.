"""
Pascom Live Manager
Sprint 2 - Etapa 2: buscar o HTML da liturgia do dia (Canção Nova).
"""

import requests

URL_LITURGIA = "https://liturgia.cancaonova.com/pb/"


def buscar_html_da_liturgia(url: str) -> str:
    """Busca o HTML da página de liturgia e retorna como texto bruto."""
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    return resposta.text


def main() -> None:
    html = buscar_html_da_liturgia(URL_LITURGIA)
    print(f"Página buscada com sucesso! Tamanho do HTML: {len(html)} caracteres")


if __name__ == "__main__":
    main()