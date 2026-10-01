# ============================================================
# SERVIÇO DE ORÇAMENTO
# ============================================================


def converter_float(valor):
    """
    Converte um valor para float.

    Aceita:
        790.5
        "790.5"
        "790,5"
        "R$ 790,50"
        "R$ 1.299,90"
    """

    if valor is None:
        return 0.0

    try:
        texto = str(valor).strip()

        if not texto:
            return 0.0

        # Remove símbolo de moeda e espaços
        texto = (
            texto
            .replace("R$", "")
            .replace("r$", "")
            .replace(" ", "")
        )

        # Caso brasileiro:
        # 1.299,90 -> 1299.90
        if "," in texto and "." in texto:
            texto = (
                texto
                .replace(".", "")
                .replace(",", ".")
            )

        # Caso brasileiro sem separador de milhar:
        # 790,50 -> 790.50
        elif "," in texto:
            texto = texto.replace(",", ".")

        # Caso decimal padrão:
        # 790.5 -> 790.5
        return float(texto)

    except (TypeError, ValueError):
        return 0.0


# ============================================================
# PB11 - CUSTO DOS PAINÉIS
# ============================================================

def calcular_custo_paineis(
    painel,
    quantidade_paineis,
):
    """
    Calcula o custo total dos painéis.

    Fórmula:

        C_paineis =
            preco_painel × quantidade
    """

    if not painel:
        return 0.0

    try:
        quantidade_paineis = int(
            quantidade_paineis
        )
    except (TypeError, ValueError):
        return 0.0

    preco = converter_float(
        painel.get("preco", 0)
    )

    if quantidade_paineis <= 0:
        return 0.0

    if preco < 0:
        return 0.0

    return preco * quantidade_paineis


# ============================================================
# PB11 - CUSTO DO INVERSOR
# ============================================================

def calcular_custo_inversor(
    inversor,
):
    """
    Retorna o preço do inversor selecionado.
    """

    if not inversor:
        return 0.0

    preco = converter_float(
        inversor.get("preco", 0)
    )

    if preco < 0:
        return 0.0

    return preco


# ============================================================
# PB11 - CUSTO DAS BATERIAS
# ============================================================

def calcular_custo_baterias(
    baterias,
    quantidade_baterias,
):
    """
    Calcula o custo total das baterias.

    Quando não houver bateria selecionada,
    o custo será zero.
    """

    if not baterias:
        return 0.0

    try:
        quantidade_baterias = int(
            quantidade_baterias
        )
    except (TypeError, ValueError):
        return 0.0

    preco = converter_float(
        baterias.get("preco", 0)
    )

    if quantidade_baterias <= 0:
        return 0.0

    if preco < 0:
        return 0.0

    return preco * quantidade_baterias


# ============================================================
# PB11 - CUSTO TOTAL
# ============================================================

def calcular_custo_total(
    custo_paineis,
    custo_inversor,
    custo_baterias,
    custos_adicionais=0.0,
):
    """
    Calcula o custo total estimado da solução.

    Fórmula prevista no PB11:

        C_equipamentos =
            C_módulos
            + C_inversor
            + C_baterias
            + C_demais

    O custo total considera os custos adicionais
    informados separadamente.
    """

    custo_paineis = converter_float(
        custo_paineis
    )

    custo_inversor = converter_float(
        custo_inversor
    )

    custo_baterias = converter_float(
        custo_baterias
    )

    custos_adicionais = converter_float(
        custos_adicionais
    )

    return (
        custo_paineis
        + custo_inversor
        + custo_baterias
        + custos_adicionais
    )


# ============================================================
# PB11 - ORÇAMENTO COMPLETO
# ============================================================

def calcular_orcamento(
    resultado,
    custos_adicionais=0.0,
):
    """
    Calcula o orçamento completo a partir
    dos equipamentos selecionados.

    Atualiza o ResultadoDimensionamento.

    Retorna:
        ResultadoDimensionamento atualizado.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento "
            "não informado."
        )

    custo_paineis = calcular_custo_paineis(
        painel=resultado.painel,
        quantidade_paineis=(
            resultado.quantidade_paineis
        ),
    )

    custo_inversor = calcular_custo_inversor(
        inversor=resultado.inversor,
    )

    custo_baterias = calcular_custo_baterias(
        baterias=resultado.baterias,
        quantidade_baterias=(
            resultado.quantidade_baterias
        ),
    )

    custo_total = calcular_custo_total(
        custo_paineis=custo_paineis,
        custo_inversor=custo_inversor,
        custo_baterias=custo_baterias,
        custos_adicionais=custos_adicionais,
    )

    resultado.custo_paineis = custo_paineis
    resultado.custo_inversor = custo_inversor
    resultado.custo_baterias = custo_baterias
    resultado.custos_adicionais = (
        converter_float(custos_adicionais)
    )
    resultado.custo_total = custo_total

    return resultado