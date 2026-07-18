# Modificações no Animated Lower Thirds

> Este documento registra todas as alterações realizadas em arquivos de terceiros utilizadas pelo Pascom Live Manager.

## Objetivo

Evitar perder alterações ao atualizar ou reinstalar o plugin Animated Lower Thirds.

---

# Alteração 01

## Arquivo

control-panel.html

## Motivo

Criar uma Prova de Conceito (PoC) para validar a atualização automática dos Lower Thirds sem utilizar o botão Import.

## Descrição

Foi adicionado um script JavaScript responsável por:

- Ler periodicamente um arquivo JSON local.
- Utilizar o endereço `http://absolute/`.
- Detectar alterações no conteúdo.
- Reutilizar a função `writeLocalStorage()` existente.
- Não alterar o funcionamento original do botão Import.

## Status

🚧 Em desenvolvimento (PoC)

## Observações

Esta implementação é experimental.

Caso a PoC não funcione, a alteração poderá ser removida sem impactar o restante do projeto.

---

## Próximas alterações

*(Adicionar novas modificações conforme forem sendo feitas.)*