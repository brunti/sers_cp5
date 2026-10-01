# ============================================================
# PB12 - RELATÓRIO FINAL
# ============================================================


def _preco_valido(equipamento):
    """
    Verifica se o equipamento possui um preço numérico válido.
    """

    if not equipamento:
        return False

    preco = equipamento.get("preco")

    if preco is None:
        return False

    if str(preco).strip() == "":
        return False

    try:
        return float(
            str(preco).replace(",", ".")
        ) >= 0

    except (TypeError, ValueError):
        return False


def gerar_resumo_final(resultado):
    """
    PB12 - Gera o relatório final do dimensionamento.

    Recebe o objeto ResultadoDimensionamento já processado
    pelos PBs anteriores e retorna um dicionário completo.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento não informado."
        )

    precos_nao_informados = []

    # ========================================================
    # PREÇO DO PAINEL
    # ========================================================

    if (
        resultado.painel is not None
        and not _preco_valido(resultado.painel)
    ):
        precos_nao_informados.append(
            "painel"
        )

    # ========================================================
    # PREÇO DO INVERSOR
    # ========================================================

    if (
        resultado.inversor is not None
        and not _preco_valido(resultado.inversor)
    ):
        precos_nao_informados.append(
            "inversor"
        )

    # ========================================================
    # PREÇO DA BATERIA
    # ========================================================

    if (
        resultado.possui_bateria
        and resultado.baterias is not None
        and not _preco_valido(resultado.baterias)
    ):
        precos_nao_informados.append(
            "bateria"
        )

    # ========================================================
    # RELATÓRIO FINAL
    # ========================================================

    return {

        # ----------------------------------------------------
        # DIMENSIONAMENTO
        # ----------------------------------------------------

        "dimensionamento": {

            "consumo_referencia":
                resultado.consumo_referencia,

            "percentual_atendimento":
                resultado.percentual_atendimento,

            "energia_fv":
                resultado.energia_fv,

            "hsp":
                resultado.hsp,

            "origem_hsp":
                resultado.origem_hsp,

            "dias_periodo":
                resultado.dias_periodo,

            "eficiencia_sistema":
                resultado.eficiencia_sistema,

            "potencia_fv":
                resultado.potencia_fv,

            "potencia_instalada":
                resultado.potencia_instalada,

            "quantidade_paineis":
                resultado.quantidade_paineis,

            # ESTA ERA A CHAVE QUE ESTAVA FALTANDO
            "geracao_estimada":
                resultado.geracao_estimada,
        },

        # ----------------------------------------------------
        # PAINEL
        # ----------------------------------------------------

        "painel":
            resultado.painel,

        # ----------------------------------------------------
        # INVERSOR
        # ----------------------------------------------------

        "inversor":
            resultado.inversor,

        # ----------------------------------------------------
        # BATERIA
        # ----------------------------------------------------

        "bateria": {

            "possui_bateria":
                resultado.possui_bateria,

            "autonomia_horas":
                resultado.autonomia_horas,

            "capacidade_necessaria":
                resultado.capacidade_bateria_necessaria,

            "equipamento":
                resultado.baterias,

            "quantidade":
                resultado.quantidade_baterias,

            "capacidade_instalada":
                resultado.capacidade_bateria_instalada,
        },

        # ----------------------------------------------------
        # COMPATIBILIDADE
        # ----------------------------------------------------

        "compatibilidade":
            resultado.compatibilidade,

        # ----------------------------------------------------
        # ORÇAMENTO
        # ----------------------------------------------------

        "orcamento": {

            "custo_paineis":
                resultado.custo_paineis,

            "custo_inversor":
                resultado.custo_inversor,

            "custo_baterias":
                resultado.custo_baterias,

            "custos_adicionais":
                resultado.custos_adicionais,

            "custo_total":
                resultado.custo_total,
        },

        # ----------------------------------------------------
        # PREÇOS NÃO INFORMADOS
        # ----------------------------------------------------

        "precos_nao_informados":
            precos_nao_informados,
    }