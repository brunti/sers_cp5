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
    quantidade_paineis=1,
):
    """
    Verifica a compatibilidade elétrica básica entre
    os painéis e o inversor.

    A tensão da string considera a quantidade de
    painéis conectados em série.

    Critérios:

    1. Tensão da string dentro da faixa do inversor.
    2. Corrente do painel dentro do limite do inversor.
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

    try:
        quantidade_paineis = int(
            quantidade_paineis
        )
    except (TypeError, ValueError):
        quantidade_paineis = 1

    if quantidade_paineis <= 0:
        quantidade_paineis = 1

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

    # --------------------------------------------------------
    # TENSÃO DA STRING
    # --------------------------------------------------------

    tensao_string = (
        tensao_painel
        * quantidade_paineis
    )

    tensao_compativel = (
        tensao_min_inversor
        <= tensao_string
        <= tensao_max_inversor
    )

    # --------------------------------------------------------
    # CORRENTE
    # --------------------------------------------------------

    corrente_compativel = (
        corrente_painel
        <= corrente_max_inversor
    )

    problemas = []

    if not tensao_compativel:

        problemas.append(
            "A tensão da string está fora "
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
                "quantidade_paineis": quantidade_paineis,
                "string_v": tensao_string,
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