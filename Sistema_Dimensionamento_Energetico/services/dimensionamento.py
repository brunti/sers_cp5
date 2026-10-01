# ============================================================
# SERVIÇO DE DIMENSIONAMENTO ENERGÉTICO
# ============================================================



from models.resultado import ResultadoDimensionamento
from utils.constantes import (
    DIAS_MES_REFERENCIA,
    EFICIENCIA_SISTEMA,
    PERCENTUAL_MINIMO,
    PERCENTUAL_MAXIMO,
)
from utils.validacoes import ler_percentual

from services.equipamentos import (
    obter_hsp,
    dimensionar_paineis,
    selecionar_painel,
    selecionar_inversor,
)

from services.compatibilidade import (
    verificar_compatibilidade,
)

from services.baterias import dimensionar_armazenamento, dimensionar_baterias

# ============================================================
# PB01 - CONSUMO DE REFERÊNCIA
# ============================================================

def calcular_consumo_referencia(consumos):
    """
    Calcula o consumo médio mensal utilizado como referência
    para o dimensionamento.

    PB01:
    O consumo médio do imóvel será utilizado como consumo
    de referência do sistema.

    Parâmetros:
        consumos: lista de dicionários contendo consumo_kwh.

    Retorno:
        float com o consumo médio em kWh/mês.
    """

    if not consumos:
        return 0.0

    valores = []

    for consumo in consumos:

        try:
            valor = float(
                consumo.get(
                    "consumo_kwh",
                    0
                )
            )

        except (TypeError, ValueError):
            continue

        if valor >= 0:
            valores.append(valor)

    if not valores:
        return 0.0

    return sum(valores) / len(valores)


# ============================================================
# PB03 - PERCENTUAL DE ATENDIMENTO
# ============================================================

def validar_percentual_atendimento(percentual):
    """
    Valida o percentual de atendimento.

    O PB03 determina valores entre 1% e 100%.
    """

    try:
        percentual = float(percentual)

    except (TypeError, ValueError):
        raise ValueError(
            "O percentual de atendimento deve ser numérico."
        )

    if (
        percentual < PERCENTUAL_MINIMO
        or percentual > PERCENTUAL_MAXIMO
    ):
        raise ValueError(
            "O percentual de atendimento deve estar "
            "entre 1% e 100%."
        )

    return percentual


def percentual_para_fator(percentual):
    """
    Converte percentual para fator decimal.

    Exemplos:

        100% -> 1.00
        80%  -> 0.80
        50%  -> 0.50
        1%   -> 0.01
    """

    percentual = validar_percentual_atendimento(
        percentual
    )

    return percentual / 100.0


def calcular_energia_fv(
    consumo_referencia,
    percentual_atendimento,
):
    """
    Calcula a energia fotovoltaica necessária.

    Fórmula do PB01/PB03:

        E_FV = C_m × f

    Onde:

        C_m = consumo de referência
        f   = percentual de atendimento em formato decimal

    Retorno:
        energia FV necessária em kWh/mês.
    """

    try:
        consumo_referencia = float(
            consumo_referencia
        )

    except (TypeError, ValueError):
        raise ValueError(
            "O consumo de referência deve ser numérico."
        )

    if consumo_referencia < 0:
        raise ValueError(
            "O consumo de referência não pode ser negativo."
        )

    fator = percentual_para_fator(
        percentual_atendimento
    )

    return consumo_referencia * fator


# ============================================================
# PB04 - POTÊNCIA FOTOVOLTAICA
# ============================================================

def validar_parametros_potencia(
    energia_fv,
    hsp,
    dias_periodo,
    eficiencia,
):
    """
    Valida os parâmetros necessários para o cálculo
    da potência fotovoltaica.
    """

    try:
        energia_fv = float(energia_fv)
        hsp = float(hsp)
        dias_periodo = float(dias_periodo)
        eficiencia = float(eficiencia)

    except (TypeError, ValueError):
        raise ValueError(
            "Todos os parâmetros do cálculo de potência "
            "devem ser numéricos."
        )

    if energia_fv < 0:
        raise ValueError(
            "A energia FV não pode ser negativa."
        )

    if hsp <= 0:
        raise ValueError(
            "A HSP deve ser maior que zero."
        )

    if dias_periodo <= 0:
        raise ValueError(
            "A quantidade de dias deve ser maior que zero."
        )

    if eficiencia <= 0:
        raise ValueError(
            "A eficiência do sistema deve ser maior que zero."
        )

    return (
        energia_fv,
        hsp,
        dias_periodo,
        eficiencia,
    )


def calcular_potencia_fv(
    energia_fv,
    hsp,
    dias_periodo=DIAS_MES_REFERENCIA,
    eficiencia=EFICIENCIA_SISTEMA,
):
    """
    Calcula a potência fotovoltaica necessária.

    Fórmula do PB04:

        P_FV = E_FV / (HSP × D × η)

    Resultado:
        potência em kW.
    """

    (
        energia_fv,
        hsp,
        dias_periodo,
        eficiencia,
    ) = validar_parametros_potencia(
        energia_fv,
        hsp,
        dias_periodo,
        eficiencia,
    )

    denominador = (
        hsp
        * dias_periodo
        * eficiencia
    )

    if denominador <= 0:
        raise ValueError(
            "Não é possível calcular a potência: "
            "o denominador deve ser maior que zero."
        )

    potencia = energia_fv / denominador

    return potencia


# ============================================================
# CONSTRUÇÃO DO RESULTADO INICIAL
# ============================================================

def criar_resultado_base(
    consumos,
    percentual_atendimento,
    hsp,
    origem_hsp="",
    dias_periodo=DIAS_MES_REFERENCIA,
    eficiencia=EFICIENCIA_SISTEMA,
):
    """
    Cria um ResultadoDimensionamento contendo os dados
    calculados até o PB04.

    Essa função ainda não seleciona equipamentos.

    Ela será expandida conforme os próximos PBs forem
    implementados.
    """

    consumo_referencia = (
        calcular_consumo_referencia(
            consumos
        )
    )

    percentual_atendimento = (
        validar_percentual_atendimento(
            percentual_atendimento
        )
    )

    energia_fv = calcular_energia_fv(
        consumo_referencia,
        percentual_atendimento,
    )

    potencia_fv = calcular_potencia_fv(
        energia_fv=energia_fv,
        hsp=hsp,
        dias_periodo=dias_periodo,
        eficiencia=eficiencia,
    )

    resultado = ResultadoDimensionamento(
        consumo_referencia=consumo_referencia,
        percentual_atendimento=(
            percentual_atendimento
        ),
        energia_fv=energia_fv,
        hsp=hsp,
        origem_hsp=origem_hsp,
        dias_periodo=dias_periodo,
        eficiencia_sistema=eficiencia,
        potencia_fv=potencia_fv,
    )

    return resultado


# ============================================================
# INTERAÇÃO COM O USUÁRIO
# ============================================================

def solicitar_percentual_atendimento():
    """
    Solicita ao usuário o percentual de atendimento.
    """

    return ler_percentual(
        "Percentual de atendimento do consumo (1-100%): "
    )


# ============================================================
# RESUMO DOS CÁLCULOS
# ============================================================

def gerar_resumo_dimensionamento_basico(resultado):
    """
    Gera um resumo textual dos resultados calculados
    até o PB04.

    Essa função será substituída/expandida pelo PB12.
    """

    return (
        "\n"
        "============================================\n"
        "DIMENSIONAMENTO FOTOVOLTAICO\n"
        "============================================\n"
        f"Consumo de referência: "
        f"{resultado.consumo_referencia:.2f} kWh/mês\n"
        f"Percentual de atendimento: "
        f"{resultado.percentual_atendimento:.2f}%\n"
        f"Energia FV necessária: "
        f"{resultado.energia_fv:.2f} kWh/mês\n"
        f"HSP: "
        f"{resultado.hsp:.2f} h\n"
        f"Origem HSP: "
        f"{resultado.origem_hsp}\n"
        f"Dias do período: "
        f"{resultado.dias_periodo:.0f}\n"
        f"Eficiência global: "
        f"{resultado.eficiencia_sistema:.2f}\n"
        f"Potência FV necessária: "
        f"{resultado.potencia_fv:.3f} kW\n"
        "============================================\n"
    )

# ============================================================
# PB02 - OBTENÇÃO DA HSP
# ============================================================

def obter_hsp_imovel(imovel):
    """
    Obtém a HSP correspondente à localização do imóvel.

    Retorna:
        {
            "hsp": valor,
            "origem": origem
        }

    Caso não exista informação no dataset, retorna None.
    """

    if not imovel.cidade or not imovel.estado:
        raise ValueError(
            "O imóvel precisa possuir cidade e estado "
            "para obter a HSP."
        )

    resultado = obter_hsp(
        imovel.cidade,
        imovel.estado
    )

    return resultado

# ============================================================
# PB05 - SELEÇÃO E DIMENSIONAMENTO DOS PAINÉIS
# ============================================================

def executar_pb05(
    resultado,
    fabricante=None,
    modelo=None,
):
    """
    Executa o PB05 completo:

        1. Seleciona o painel.
        2. Calcula a quantidade necessária.
        3. Calcula a potência instalada.
        4. Atualiza o ResultadoDimensionamento.

    Retorna:
        ResultadoDimensionamento atualizado.

    Retorna None caso nenhum painel esteja disponível.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento não informado."
        )

    painel = selecionar_painel(
        potencia_fv=resultado.potencia_fv,
        fabricante=fabricante,
        modelo=modelo,
    )

    if painel is None:
        return None

    dimensionamento = dimensionar_paineis(
        potencia_fv=resultado.potencia_fv,
        painel=painel,
    )

    resultado.painel = (
        dimensionamento["painel"]
    )

    resultado.quantidade_paineis = (
        dimensionamento["quantidade_paineis"]
    )

    resultado.potencia_instalada = (
        dimensionamento["potencia_instalada"]
    )

    return resultado

# ============================================================
# PB06 - SELEÇÃO DO INVERSOR
# ============================================================

def executar_pb06(
    resultado,
    fabricante=None,
    modelo=None,
):
    """
    Executa o PB06.

    Seleciona um inversor considerando:
        - potência FV instalada
        - necessidade de bateria

    Se resultado.possui_bateria for True,
    somente inversores compatíveis com bateria
    serão considerados.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento "
            "não informado."
        )

    if resultado.potencia_instalada <= 0:
        raise ValueError(
            "A potência instalada dos painéis "
            "deve ser maior que zero."
        )

    possui_bateria = bool(
        getattr(
            resultado,
            "possui_bateria",
            False,
        )
    )

    inversor = selecionar_inversor(
        potencia_instalada=(
            resultado.potencia_instalada
        ),
        fabricante=fabricante,
        modelo=modelo,
        possui_bateria=possui_bateria,
    )

    if inversor is None:
        return None

    resultado.inversor = inversor

    return resultado

# ============================================================
# PB10 - VERIFICAÇÃO DE COMPATIBILIDADE
# ============================================================

def executar_pb10(resultado):
    """
    Executa o PB10.

    Verifica a compatibilidade entre:
        - painel selecionado no PB05;
        - inversor selecionado no PB06;
        - bateria selecionada no armazenamento, quando houver.

    Utiliza a quantidade real de painéis definida no PB05.

    Retorna:
        ResultadoDimensionamento atualizado.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento "
            "não informado."
        )

    if resultado.painel is None:
        raise ValueError(
            "Nenhum painel foi selecionado."
        )

    if resultado.inversor is None:
        raise ValueError(
            "Nenhum inversor foi selecionado."
        )

    quantidade_paineis = getattr(
        resultado,
        "quantidade_paineis",
        0,
    )

    if quantidade_paineis <= 0:
        raise ValueError(
            "A quantidade de painéis deve ser "
            "maior que zero."
        )

    bateria = None

    if getattr(
        resultado,
        "possui_bateria",
        False,
    ):
        bateria = getattr(
            resultado,
            "baterias",
            None,
        )

        if bateria is None:
            raise ValueError(
                "O sistema foi configurado com bateria, "
                "mas nenhum equipamento de bateria foi selecionado."
            )

    compatibilidade = verificar_compatibilidade(
        painel=resultado.painel,
        inversor=resultado.inversor,
        quantidade_paineis=quantidade_paineis,
        bateria=bateria,
    )

    resultado.compatibilidade = compatibilidade

    return resultado

# ============================================================
# PB08 + PB09 - INTEGRAÇÃO DO ARMAZENAMENTO
# ============================================================

def executar_armazenamento(
    resultado,
    autonomia_horas,
    fabricante=None,
    modelo=None,
    dod=0.80,
    eficiencia_bateria=0.90,
):
    """
    Executa o PB08 e o PB09 e atualiza o
    ResultadoDimensionamento.

    Parâmetros:
        resultado:
            ResultadoDimensionamento já criado.

        autonomia_horas:
            Autonomia desejada em horas.

        fabricante/modelo:
            Filtros opcionais para seleção da bateria.

        dod:
            Profundidade de descarga utilizada no dimensionamento.

        eficiencia_bateria:
            Eficiência considerada no dimensionamento.

    Retorna:
        ResultadoDimensionamento atualizado.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento "
            "não informado."
        )

    # --------------------------------------------------------
    # PB08 - Dimensionamento da capacidade necessária
    # --------------------------------------------------------

    armazenamento = dimensionar_armazenamento(
        consumo_referencia=(
            resultado.consumo_referencia
        ),
        autonomia_horas=autonomia_horas,
        dod=dod,
        eficiencia_bateria=eficiencia_bateria,
        dias=resultado.dias_periodo,
    )

    # --------------------------------------------------------
    # Atualiza dados do PB08
    # --------------------------------------------------------

    resultado.possui_bateria = True

    resultado.autonomia_horas = (
        armazenamento["autonomia_horas"]
    )

    resultado.capacidade_bateria_necessaria = (
        armazenamento["capacidade_necessaria"]
    )

    # --------------------------------------------------------
    # PB09 - Seleção e quantidade de baterias
    # --------------------------------------------------------

    dimensionamento = dimensionar_baterias(
        capacidade_necessaria=(
            armazenamento["capacidade_necessaria"]
        ),
        fabricante=fabricante,
        modelo=modelo,
    )

    if dimensionamento is None:
        resultado.baterias = None
        resultado.quantidade_baterias = 0
        resultado.capacidade_bateria_instalada = 0.0

        return resultado

    # --------------------------------------------------------
    # Atualiza dados do PB09
    # --------------------------------------------------------

    resultado.baterias = (
        dimensionamento["bateria"]
    )

    resultado.quantidade_baterias = (
        dimensionamento["quantidade"]
    )

    resultado.capacidade_bateria_instalada = (
        dimensionamento["capacidade_instalada"]
    )

    return resultado

def calcular_geracao_estimada(
    potencia_instalada,
    hsp,
    dias_periodo=30,
    eficiencia=0.8,
):
    """
    Estima a geração de energia do sistema FV
    no período informado.

    Retorno:
        energia estimada em kWh.
    """

    try:
        potencia_instalada = float(potencia_instalada)
        hsp = float(hsp)
        dias_periodo = float(dias_periodo)
        eficiencia = float(eficiencia)

    except (TypeError, ValueError):
        return 0.0

    if (
        potencia_instalada <= 0
        or hsp <= 0
        or dias_periodo <= 0
        or eficiencia <= 0
    ):
        return 0.0

    return (
        potencia_instalada
        * hsp
        * dias_periodo
        * eficiencia
    )

def calcular_custos(resultado):
    """
    Calcula os custos dos equipamentos
    e o custo total do sistema.
    """

    if resultado is None:
        raise ValueError(
            "Resultado de dimensionamento não informado."
        )

    custo_paineis = 0.0
    custo_inversor = 0.0
    custo_baterias = 0.0

    # PAINÉIS
    if resultado.painel is not None:
        preco_painel = resultado.painel.get("preco")

        if preco_painel is not None and str(preco_painel).strip() != "":
            try:
                preco_painel = float(
                    str(preco_painel).replace(",", ".")
                )

                if preco_painel >= 0:
                    custo_paineis = (
                        preco_painel
                        * resultado.quantidade_paineis
                    )

            except (TypeError, ValueError):
                custo_paineis = 0.0

    # INVERSOR
    if resultado.inversor is not None:
        preco_inversor = resultado.inversor.get("preco")

        if preco_inversor is not None and str(preco_inversor).strip() != "":
            try:
                preco_inversor = float(
                    str(preco_inversor).replace(",", ".")
                )

                if preco_inversor >= 0:
                    custo_inversor = preco_inversor

            except (TypeError, ValueError):
                custo_inversor = 0.0

    # BATERIAS
    if (
        resultado.possui_bateria
        and resultado.baterias is not None
    ):
        preco_bateria = resultado.baterias.get("preco")

        if preco_bateria is not None and str(preco_bateria).strip() != "":
            try:
                preco_bateria = float(
                    str(preco_bateria).replace(",", ".")
                )

                if preco_bateria >= 0:
                    custo_baterias = (
                        preco_bateria
                        * resultado.quantidade_baterias
                    )

            except (TypeError, ValueError):
                custo_baterias = 0.0

    # CUSTOS ADICIONAIS
    try:
        custos_adicionais = float(
            resultado.custos_adicionais or 0
        )
    except (TypeError, ValueError):
        custos_adicionais = 0.0

    # TOTAL
    custo_total = (
        custo_paineis
        + custo_inversor
        + custo_baterias
        + custos_adicionais
    )

    # ATUALIZA O RESULTADO
    resultado.custo_paineis = custo_paineis
    resultado.custo_inversor = custo_inversor
    resultado.custo_baterias = custo_baterias
    resultado.custos_adicionais = custos_adicionais
    resultado.custo_total = custo_total

    return resultado