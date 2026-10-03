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


def _formatar_preco(preco):
    """
    Formata um preço para exibição.
    """

    if preco is None:
        return "Não informado"

    if str(preco).strip() == "":
        return "Não informado"

    try:
        valor = float(
            str(preco).replace(",", ".")
        )

        return f"R$ {valor:,.2f}".replace(
            ",",
            "X"
        ).replace(
            ".",
            ","
        ).replace(
            "X",
            "."
        )

    except (TypeError, ValueError):
        return "Não informado"


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


# ============================================================
# PB12 - EXIBIÇÃO DO RELATÓRIO PARA O USUÁRIO
# ============================================================

def exibir_resumo_final(relatorio):
    """
    Exibe o relatório final do PB12 na tela.

    Mostra:
        - dimensionamento;
        - painel selecionado;
        - inversor selecionado;
        - bateria selecionada;
        - compatibilidade;
        - orçamento;
        - registros reais utilizados dos datasets.
    """

    if relatorio is None:
        raise ValueError(
            "Relatório final não informado."
        )

    dimensionamento = relatorio.get(
        "dimensionamento",
        {}
    )

    painel = relatorio.get(
        "painel"
    )

    inversor = relatorio.get(
        "inversor"
    )

    bateria_info = relatorio.get(
        "bateria",
        {}
    )

    bateria = bateria_info.get(
        "equipamento"
    )

    compatibilidade = relatorio.get(
        "compatibilidade"
    )

    orcamento = relatorio.get(
        "orcamento",
        {}
    )

    precos_nao_informados = relatorio.get(
        "precos_nao_informados",
        []
    )

    print()
    print("=" * 70)
    print(" " * 18 + "PB12 - RELATÓRIO FINAL")
    print("=" * 70)

    # ========================================================
    # DIMENSIONAMENTO
    # ========================================================

    print("\nDIMENSIONAMENTO")
    print("-" * 70)

    print(
        "Consumo:",
        dimensionamento.get(
            "consumo_referencia",
            0
        ),
        "kWh/mês"
    )

    print(
        "Atendimento:",
        dimensionamento.get(
            "percentual_atendimento",
            0
        ),
        "%"
    )

    print(
        "HSP:",
        dimensionamento.get(
            "hsp",
            0
        )
    )

    print(
        "Origem da HSP:",
        dimensionamento.get(
            "origem_hsp",
            "Não informado"
        )
    )

    print(
        "Potência FV necessária:",
        dimensionamento.get(
            "potencia_fv",
            0
        ),
        "kWp"
    )

    print(
        "Potência instalada:",
        dimensionamento.get(
            "potencia_instalada",
            0
        ),
        "kWp"
    )

    print(
        "Quantidade de painéis:",
        dimensionamento.get(
            "quantidade_paineis",
            0
        )
    )

    print(
        "Geração estimada:",
        dimensionamento.get(
            "geracao_estimada",
            0
        ),
        "kWh/mês"
    )

    # ========================================================
    # PAINEL
    # ========================================================

    print("\nPAINEL FOTOVOLTAICO")
    print("-" * 70)

    if painel is None:

        print(
            "Nenhum painel foi selecionado."
        )

    else:

        print(
            "Fabricante:",
            painel.get(
                "fabricante",
                ""
            )
        )

        print(
            "Modelo:",
            painel.get(
                "modelo",
                ""
            )
        )

        print(
            "Potência:",
            painel.get(
                "potencia_wp",
                ""
            ),
            "Wp"
        )

        print(
            "Tensão:",
            painel.get(
                "tensao_v",
                ""
            ),
            "V"
        )

        print(
            "Corrente:",
            painel.get(
                "corrente_a",
                ""
            ),
            "A"
        )

        print(
            "Eficiência:",
            painel.get(
                "eficiencia",
                ""
            ),
            "%"
        )

        print(
            "Preço:",
            _formatar_preco(
                painel.get("preco")
            )
        )

        print(
            "Fonte:",
            painel.get(
                "fonte",
                ""
            )
        )

    # ========================================================
    # INVERSOR
    # ========================================================

    print("\nINVERSOR")
    print("-" * 70)

    if inversor is None:

        print(
            "Nenhum inversor foi selecionado."
        )

    else:

        print(
            "Fabricante:",
            inversor.get(
                "fabricante",
                ""
            )
        )

        print(
            "Modelo:",
            inversor.get(
                "modelo",
                ""
            )
        )

        print(
            "Potência nominal:",
            inversor.get(
                "potencia_nominal_kw",
                ""
            ),
            "kW"
        )

        print(
            "Potência FV máxima:",
            inversor.get(
                "potencia_fv_max_kw",
                ""
            ),
            "kW"
        )

        print(
            "Tensão mínima:",
            inversor.get(
                "tensao_min_v",
                ""
            ),
            "V"
        )

        print(
            "Tensão máxima:",
            inversor.get(
                "tensao_max_v",
                ""
            ),
            "V"
        )

        print(
            "Corrente máxima:",
            inversor.get(
                "corrente_max_a",
                ""
            ),
            "A"
        )

        print(
            "MPPT:",
            inversor.get(
                "mppt",
                ""
            )
        )

        print(
            "Compatibilidade com bateria:",
            inversor.get(
                "compatibilidade_bateria",
                ""
            )
        )

        print(
            "Preço:",
            _formatar_preco(
                inversor.get("preco")
            )
        )

        print(
            "Fonte:",
            inversor.get(
                "fonte",
                ""
            )
        )

    # ========================================================
    # BATERIA
    # ========================================================

    print("\nBATERIA")
    print("-" * 70)

    possui_bateria = bateria_info.get(
        "possui_bateria",
        False
    )

    if not possui_bateria:

        print(
            "Sistema sem bateria."
        )

    elif bateria is None:

        print(
            "Nenhuma bateria foi selecionada."
        )

    else:

        print(
            "Fabricante:",
            bateria.get(
                "fabricante",
                ""
            )
        )

        print(
            "Modelo:",
            bateria.get(
                "modelo",
                ""
            )
        )

        print(
            "Capacidade nominal:",
            bateria.get(
                "capacidade_nominal_kwh",
                ""
            ),
            "kWh"
        )

        print(
            "DOD:",
            bateria.get(
                "dod",
                ""
            )
        )

        print(
            "Eficiência:",
            bateria.get(
                "eficiencia",
                ""
            )
        )

        print(
            "Preço por unidade:",
            _formatar_preco(
                bateria.get("preco")
            )
        )

        print(
            "Quantidade:",
            bateria_info.get(
                "quantidade",
                0
            )
        )

        print(
            "Capacidade necessária:",
            bateria_info.get(
                "capacidade_necessaria",
                0
            ),
            "kWh"
        )

        print(
            "Capacidade instalada:",
            bateria_info.get(
                "capacidade_instalada",
                0
            ),
            "kWh"
        )

        print(
            "Fonte:",
            bateria.get(
                "fonte",
                ""
            )
        )

    # ========================================================
    # COMPATIBILIDADE
    # ========================================================

    print("\nCOMPATIBILIDADE")
    print("-" * 70)

    if compatibilidade is None:

        print(
            "Compatibilidade não calculada."
        )

    else:

        compativel = compatibilidade.get(
            "compativel",
            False
        )

        print(
            "Sistema compatível:",
            "SIM" if compativel else "NÃO"
        )

        problemas = compatibilidade.get(
            "problemas",
            []
        )

        if problemas:

            print("\nProblemas encontrados:")

            for problema in problemas:

                print(
                    "-",
                    problema
                )

    # ========================================================
    # ORÇAMENTO
    # ========================================================

    print("\nORÇAMENTO")
    print("-" * 70)

    print(
        "Painéis:",
        _formatar_preco(
            orcamento.get(
                "custo_paineis",
                0
            )
        )
    )

    print(
        "Inversor:",
        _formatar_preco(
            orcamento.get(
                "custo_inversor",
                0
            )
        )
    )

    print(
        "Baterias:",
        _formatar_preco(
            orcamento.get(
                "custo_baterias",
                0
            )
        )
    )

    print(
        "Adicionais:",
        _formatar_preco(
            orcamento.get(
                "custos_adicionais",
                0
            )
        )
    )

    print(
        "TOTAL:",
        _formatar_preco(
            orcamento.get(
                "custo_total",
                0
            )
        )
    )

    # ========================================================
    # PREÇOS NÃO INFORMADOS
    # ========================================================

    print("\nPREÇOS NÃO INFORMADOS")
    print("-" * 70)

    if not precos_nao_informados:

        print(
            "Nenhum preço não informado."
        )

    else:

        for equipamento in precos_nao_informados:

            print(
                "-",
                equipamento
            )

    # ========================================================
    # DATASETS UTILIZADOS
    # ========================================================

    print("\n")
    print("=" * 70)
    print(
        " " * 18 +
        "DADOS DOS DATASETS UTILIZADOS"
    )
    print("=" * 70)

    print(
        "\nOs equipamentos abaixo são os "
        "registros selecionados pelo sistema "
        "a partir dos datasets."
    )

    # --------------------------------------------------------
    # DATASET DE PAINÉIS
    # --------------------------------------------------------

    print("\nPAINEL")
    print("-" * 70)

    print(
        "Dataset consultado:",
        "datasets/paineis.csv"
    )

    if painel is not None:

        print(
            "Registro selecionado:"
        )

        print(
            "Fabricante:",
            painel.get(
                "fabricante",
                ""
            )
        )

        print(
            "Modelo:",
            painel.get(
                "modelo",
                ""
            )
        )

        print(
            "Potência:",
            painel.get(
                "potencia_wp",
                ""
            ),
            "Wp"
        )

        print(
            "Tensão:",
            painel.get(
                "tensao_v",
                ""
            ),
            "V"
        )

        print(
            "Corrente:",
            painel.get(
                "corrente_a",
                ""
            ),
            "A"
        )

        print(
            "Preço:",
            _formatar_preco(
                painel.get("preco")
            )
        )

    else:

        print(
            "Nenhum registro selecionado."
        )

    # --------------------------------------------------------
    # DATASET DE INVERSORES
    # --------------------------------------------------------

    print("\nINVERSOR")
    print("-" * 70)

    print(
        "Dataset consultado:",
        "datasets/inversores.csv"
    )

    if inversor is not None:

        print(
            "Registro selecionado:"
        )

        print(
            "Fabricante:",
            inversor.get(
                "fabricante",
                ""
            )
        )

        print(
            "Modelo:",
            inversor.get(
                "modelo",
                ""
            )
        )

        print(
            "Potência nominal:",
            inversor.get(
                "potencia_nominal_kw",
                ""
            ),
            "kW"
        )

        print(
            "Potência FV máxima:",
            inversor.get(
                "potencia_fv_max_kw",
                ""
            ),
            "kW"
        )

        print(
            "Compatibilidade com bateria:",
            inversor.get(
                "compatibilidade_bateria",
                ""
            )
        )

        print(
            "Preço:",
            _formatar_preco(
                inversor.get("preco")
            )
        )

    else:

        print(
            "Nenhum registro selecionado."
        )

    # --------------------------------------------------------
    # DATASET DE BATERIAS
    # --------------------------------------------------------

    print("\nBATERIA")
    print("-" * 70)

    print(
        "Dataset consultado:",
        "datasets/baterias.csv"
    )

    if bateria is not None:

        print(
            "Registro selecionado:"
        )

        print(
            "Fabricante:",
            bateria.get(
                "fabricante",
                ""
            )
        )

        print(
            "Modelo:",
            bateria.get(
                "modelo",
                ""
            )
        )

        print(
            "Capacidade:",
            bateria.get(
                "capacidade_nominal_kwh",
                ""
            ),
            "kWh"
        )

        print(
            "Preço:",
            _formatar_preco(
                bateria.get("preco")
            )
        )

    elif possui_bateria:

        print(
            "Nenhum registro de bateria selecionado."
        )

    else:

        print(
            "O sistema não utilizou bateria."
        )

    # ========================================================
    # FINAL
    # ========================================================

    print("\n")
    print("=" * 70)
    print(
        " " * 20 +
        "PB12 CONCLUÍDO"
    )
    print("=" * 70)