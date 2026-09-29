# ============================================================
# FUNÇÕES DE VALIDAÇÃO E LEITURA DE DADOS
# ============================================================

from utils.constantes import (
    MES_MINIMO,
    MES_MAXIMO,
    ANO_MINIMO,
    PERCENTUAL_MINIMO,
    PERCENTUAL_MAXIMO,
)


def campo_preenchido(valor):
    """
    Verifica se um campo de texto possui algum conteúdo.
    """
    return valor is not None and valor.strip() != ""


def ler_texto_obrigatorio(mensagem):
    """
    Solicita um texto ao usuário e impede que o campo fique vazio.
    """
    while True:
        valor = input(mensagem).strip()

        if campo_preenchido(valor):
            return valor

        print("Este campo é obrigatório. Tente novamente.")


def ler_numero_obrigatorio(mensagem, permitir_negativo=False):
    """
    Lê um número decimal obrigatório.

    Aceita vírgula ou ponto como separador decimal.
    """
    while True:
        valor = input(mensagem).strip()

        if not campo_preenchido(valor):
            print("Este campo é obrigatório. Tente novamente.")
            continue

        try:
            numero = float(valor.replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número.")
            continue

        if not permitir_negativo and numero < 0:
            print("O valor não pode ser negativo.")
            continue

        return numero


def ler_inteiro_obrigatorio(mensagem, minimo=None, maximo=None):
    """
    Lê um número inteiro obrigatório, permitindo definir
    valor mínimo e máximo.
    """
    while True:
        valor = input(mensagem).strip()

        if not campo_preenchido(valor):
            print("Este campo é obrigatório. Tente novamente.")
            continue

        try:
            numero = int(valor)
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")
            continue

        if minimo is not None and numero < minimo:
            print(f"O valor mínimo permitido é {minimo}.")
            continue

        if maximo is not None and numero > maximo:
            print(f"O valor máximo permitido é {maximo}.")
            continue

        return numero


def ler_mes(mensagem="Mês (1-12): "):
    """
    Lê e valida um mês.
    """
    return ler_inteiro_obrigatorio(
        mensagem,
        minimo=MES_MINIMO,
        maximo=MES_MAXIMO,
    )


def ler_ano(mensagem="Ano: "):
    """
    Lê e valida um ano.
    """
    return ler_inteiro_obrigatorio(
        mensagem,
        minimo=ANO_MINIMO,
    )


def ler_percentual(mensagem="Percentual de atendimento (1-100%): "):
    """
    Lê e valida o percentual de atendimento do consumo.

    PB03:
    O percentual deve estar entre 1% e 100%.
    """
    return ler_numero_obrigatorio_percentual(
        mensagem,
        minimo=PERCENTUAL_MINIMO,
        maximo=PERCENTUAL_MAXIMO,
    )


def ler_numero_obrigatorio_percentual(
    mensagem,
    minimo=1,
    maximo=100,
):
    """
    Lê um número decimal dentro de um intervalo específico.
    """
    while True:
        valor = input(mensagem).strip()

        if not campo_preenchido(valor):
            print("Este campo é obrigatório. Tente novamente.")
            continue

        try:
            numero = float(valor.replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número.")
            continue

        if numero < minimo or numero > maximo:
            print(
                f"O percentual deve estar entre "
                f"{minimo}% e {maximo}%."
            )
            continue

        return numero


def confirmar(mensagem):
    """
    Solicita confirmação do usuário.
    """
    while True:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()

        if resposta == "s":
            return True

        if resposta == "n":
            return False

        print("Resposta inválida. Digite 's' ou 'n'.")