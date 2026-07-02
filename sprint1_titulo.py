"""
Pascom Live Manager
Sprint 1: conectar ao OBS Studio e alterar o texto da fonte PLM_TITULO.
"""

import obsws_python as obs

# Dados de conexão com o OBS.
# Deixar a senha direto no código é só pra Sprint 1 funcionar rápido.
# Isso NÃO é boa prática num projeto open source — mais sobre isso no final.
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_SENHA = "sua_senha_aqui"


def atualizar_texto_da_fonte(cliente: obs.ReqClient, nome_da_fonte: str, novo_texto: str) -> None:
    """Altera o texto exibido por uma fonte de texto no OBS."""
    cliente.set_input_settings(nome_da_fonte, {"text": novo_texto}, True)


def main() -> None:
    with obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_SENHA, timeout=3) as cliente:
        atualizar_texto_da_fonte(cliente, "PLM_TITULO", "Missa de Domingo — Teste Sprint 1")

    print("Texto do PLM_TITULO atualizado com sucesso!")


if __name__ == "__main__":
    main()