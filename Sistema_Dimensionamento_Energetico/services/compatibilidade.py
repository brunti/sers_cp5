# ============================================================
# SERVIÇO DE COMPATIBILIDADE
# ============================================================


def converter_float(valor):
    """
    Converte um valor para float.

    Aceita números utilizando vírgula ou ponto decimal.
    """

    try:
        return float(
            str(valor).replace(",", ".")
        )

    except (TypeError, ValueError):
        return None


# ============================================================
# VALIDAÇÃO DOS EQUIPAMENTOS
# ============================================================

def validar_dados_compatibilidade(
    painel,
    inversor,
):
    """
    Verifica se painel e inversor possuem os dados
    necessários para uma análise de compatibilidade.

    Retorna uma lista de problemas encontrados.
    """

    problemas = []

    if painel is None:
        problemas.append(
            "Painel não informado."
        )

    if inversor is None:
        problemas.append(
            "Inversor não informado."
        )

    if problemas:
        return problemas

    campos_painel = [
        "tensao_v",
        "corrente_a",
    ]

    campos_inversor = [
        "tensao_min_v",
        "tensao_max_v",
        "corrente_max_a",
    ]

    for campo in campos_painel:

        if campo not in painel:
            problemas.append(
                f"Painel sem campo '{campo}'."
            )

        elif converter_float(
            painel[campo]
        ) is None:

            problemas.append(
                f"Valor inválido no painel: "
                f"{campo}."
            )

    for campo in campos_inversor:

        if campo not in inversor:
            problemas.append(
                f"Inversor sem campo '{campo}'."
            )

        elif converter_float(
            inversor[campo]
        ) is None:

            problemas.append(
                f"Valor inválido no inversor: "
                f"{campo}."
            )

    return problemas


# ============================================================
# PB10 - COMPATIBILIDADE
# ============================================================

def verificar_compatibilidade(
    painel,
    inversor,
):
    """
    Verifica a compatibilidade elétrica básica entre
    o painel selecionado e o inversor.

    Critérios utilizados:

    1. Tensão do painel dentro da faixa aceita
       pelo inversor.

    2. Corrente do painel dentro do limite aceito
       pelo inversor.

    Retorna um dicionário detalhado.
    """

    problemas = validar_dados_compatibilidade(
        painel,
        inversor,
    )

    if problemas:

        return {
            "compativel": False,
            "problemas": problemas,
            "criterios": {},
        }

    tensao_painel = converter_float(
        painel["tensao_v"]
    )

    corrente_painel = converter_float(
        painel["corrente_a"]
    )

    tensao_min_inversor = converter_float(
        inversor["tensao_min_v"]
    )

    tensao_max_inversor = converter_float(
        inversor["tensao_max_v"]
    )

    corrente_max_inversor = converter_float(
        inversor["corrente_max_a"]
    )

    tensao_compativel = (
        tensao_min_inversor
        <= tensao_painel
        <= tensao_max_inversor
    )

    corrente_compativel = (
        corrente_painel
        <= corrente_max_inversor
    )

    problemas = []

    if not tensao_compativel:

        problemas.append(
            "A tensão do painel está fora "
            "da faixa aceita pelo inversor."
        )

    if not corrente_compativel:

        problemas.append(
            "A corrente do painel excede "
            "o limite do inversor."
        )

    return {
        "compativel": (
            tensao_compativel
            and corrente_compativel
        ),

        "problemas": problemas,

        "criterios": {
            "tensao": {
                "painel_v": tensao_painel,
                "min_inversor_v": (
                    tensao_min_inversor
                ),
                "max_inversor_v": (
                    tensao_max_inversor
                ),
                "compativel": (
                    tensao_compativel
                ),
            },

            "corrente": {
                "painel_a": corrente_painel,
                "max_inversor_a": (
                    corrente_max_inversor
                ),
                "compativel": (
                    corrente_compativel
                ),
            },
        },
    }