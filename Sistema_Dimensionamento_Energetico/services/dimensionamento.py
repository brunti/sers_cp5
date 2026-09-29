# ============================================================
# SERVIÇO DE DIMENSIONAMENTO ENERGÉTICO
# ============================================================

from services.equipamentos import obter_hsp

from models.resultado import ResultadoDimensionamento
from utils.constantes import (
    DIAS_MES_REFERENCIA,
    EFICIENCIA_SISTEMA,
    PERCENTUAL_MINIMO,
    PERCENTUAL_MAXIMO,
)
from utils.validacoes import ler_percentual


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