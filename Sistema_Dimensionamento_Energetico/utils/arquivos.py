# ============================================================
# FUNÇÕES DE MANIPULAÇÃO DE ARQUIVOS
# ============================================================

import csv
import json
import os


def carregar_json(caminho, estrutura_padrao=None):
    """
    Carrega um arquivo JSON.

    Caso o arquivo não exista ou esteja inválido,
    retorna a estrutura padrão informada.
    """
    if estrutura_padrao is None:
        estrutura_padrao = {}

    if not os.path.exists(caminho):
        return estrutura_padrao

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, ValueError):
        return estrutura_padrao


def salvar_json(caminho, dados):
    """
    Salva dados em um arquivo JSON.
    """
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def carregar_csv(caminho):
    """
    Carrega um arquivo CSV e retorna uma lista de dicionários.

    O CSV deve possuir uma linha de cabeçalho.
    """
    if not os.path.exists(caminho):
        return []

    try:
        with open(
            caminho,
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as arquivo:

            leitor = csv.DictReader(arquivo)

            return list(leitor)

    except (OSError, csv.Error):
        return []


def salvar_csv(caminho, dados, campos):
    """
    Salva uma lista de dicionários em um CSV.
    """
    diretorio = os.path.dirname(caminho)

    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    with open(
        caminho,
        "w",
        encoding="utf-8",
        newline="",
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
        )

        escritor.writeheader()
        escritor.writerows(dados)