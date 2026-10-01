# ============================================================
# SERVIÇO DE EQUIPAMENTOS E DATASETS
# ============================================================

from math import ceil

from utils.arquivos import carregar_csv
from utils.constantes import (
    ARQUIVO_HSP,
    ARQUIVO_PAINEIS,
    ARQUIVO_INVERSORES,
    ARQUIVO_BATERIAS,
)


# ============================================================
# HSP
# ============================================================

def carregar_hsp():
    """
    Carrega o dataset de HSP.
    """

    return carregar_csv(
        ARQUIVO_HSP
    )


def buscar_hsp_por_localizacao(
    cidade,
    estado
):
    """
    Procura a HSP no dataset utilizando cidade e UF.

    Retorna:

        {
            "hsp": valor,
            "origem": origem
        }

    Caso não encontre o local, retorna None.
    """

    if not cidade or not estado:
        return None

    registros = carregar_hsp()

    cidade_busca = str(cidade).strip().lower()
    estado_busca = str(estado).strip().lower()

    for registro in registros:

        cidade_registro = str(
            registro.get(
                "cidade",
                ""
            )
        ).strip().lower()

        uf_registro = str(
            registro.get(
                "uf",
                ""
            )
        ).strip().lower()

        if (
            cidade_registro == cidade_busca
            and
            uf_registro == estado_busca
        ):

            valor_hsp = registro.get(
                "hsp_kwh_m2_dia"
            )

            fonte = registro.get(
                "fonte",
                ""
            )

            try:
                valor_hsp = float(
                    str(valor_hsp).replace(
                        ",",
                        "."
                    )
                )

            except (TypeError, ValueError):
                return None

            if valor_hsp <= 0:
                return None

            return {
                "hsp": valor_hsp,
                "origem": fonte,
            }

    return None


# ============================================================
# PAINÉIS
# ============================================================

def carregar_paineis():
    """
    Carrega o dataset de painéis.
    """

    return carregar_csv(
        ARQUIVO_PAINEIS
    )


# ============================================================
# INVERSORES
# ============================================================

def carregar_inversores():
    """
    Carrega o dataset de inversores.
    """

    return carregar_csv(
        ARQUIVO_INVERSORES
    )


# ============================================================
# BATERIAS
# ============================================================

def carregar_baterias():
    """
    Carrega o dataset de baterias.
    """

    return carregar_csv(
        ARQUIVO_BATERIAS
    )

# ============================================================
# VALIDAÇÃO DOS DATASETS
# ============================================================

def verificar_dataset(registros, nome_dataset):
    """
    Verifica se um dataset possui registros.

    Retorna True quando existem dados.
    Retorna False quando o dataset está vazio.
    """

    if not registros:
        print(
            f"\nDataset '{nome_dataset}' está vazio."
        )
        return False

    return True


def obter_hsp(cidade, estado):
    """
    Obtém a HSP de uma determinada localização.

    Retorna:
        {
            "hsp": valor,
            "origem": origem
        }

    ou None caso não exista informação.
    """

    resultado = buscar_hsp_por_localizacao(
        cidade,
        estado
    )

    if resultado is None:

        print(
            "\nNão foi encontrada HSP para "
            f"{cidade}/{estado}."
        )

        return None

    return resultado

# ============================================================
# PB05 - DIMENSIONAMENTO DOS PAINÉIS
# ============================================================

def validar_painel(painel):
    """
    Valida os dados mínimos necessários de um painel.
    """

    if painel is None:
        raise ValueError(
            "Nenhum painel foi informado."
        )

    campos_obrigatorios = [
        "fabricante",
        "modelo",
        "potencia_wp",
    ]

    for campo in campos_obrigatorios:

        if campo not in painel:
            raise ValueError(
                f"O painel não possui o campo '{campo}'."
            )

    try:
        potencia_wp = float(
            str(
                painel["potencia_wp"]
            ).replace(",", ".")
        )

    except (TypeError, ValueError):
        raise ValueError(
            "A potência do painel deve ser numérica."
        )

    if potencia_wp <= 0:
        raise ValueError(
            "A potência do painel deve ser maior que zero."
        )

    return True


def calcular_quantidade_paineis(
    potencia_fv,
    potencia_painel_wp,
):
    """
    Calcula a quantidade necessária de painéis.

    Fórmula:

        N = teto(P_FV / P_painel)

    P_FV:
        potência FV necessária em kW.

    P_painel:
        potência nominal do painel em Wp.
    """

    try:
        potencia_fv = float(
            potencia_fv
        )

        potencia_painel_wp = float(
            potencia_painel_wp
        )

    except (TypeError, ValueError):
        raise ValueError(
            "As potências devem ser numéricas."
        )

    if potencia_fv <= 0:
        raise ValueError(
            "A potência FV deve ser maior que zero."
        )

    if potencia_painel_wp <= 0:
        raise ValueError(
            "A potência do painel deve ser maior que zero."
        )

    # Conversão de Wp para kWp.
    potencia_painel_kw = (
        potencia_painel_wp / 1000
    )

    quantidade = ceil(
        potencia_fv / potencia_painel_kw
    )

    return quantidade


def calcular_potencia_instalada(
    quantidade_paineis,
    potencia_painel_wp,
):
    """
    Calcula a potência instalada do conjunto de painéis.

    Resultado em kWp.
    """

    try:
        quantidade_paineis = int(
            quantidade_paineis
        )

        potencia_painel_wp = float(
            potencia_painel_wp
        )

    except (TypeError, ValueError):
        raise ValueError(
            "Quantidade e potência do painel "
            "devem ser numéricas."
        )

    if quantidade_paineis <= 0:
        raise ValueError(
            "A quantidade de painéis deve ser maior que zero."
        )

    if potencia_painel_wp <= 0:
        raise ValueError(
            "A potência do painel deve ser maior que zero."
        )

    potencia_instalada = (
        quantidade_paineis
        * potencia_painel_wp
        / 1000
    )

    return potencia_instalada


def dimensionar_paineis(
    potencia_fv,
    painel,
):
    """
    Executa o PB05 completo para um painel selecionado.

    Retorna:

        {
            "painel": painel,
            "quantidade_paineis": quantidade,
            "potencia_instalada": potencia
        }
    """

    validar_painel(
        painel
    )

    potencia_painel_wp = float(
        str(
            painel["potencia_wp"]
        ).replace(",", ".")
    )

    quantidade = calcular_quantidade_paineis(
        potencia_fv=potencia_fv,
        potencia_painel_wp=potencia_painel_wp,
    )

    potencia_instalada = (
        calcular_potencia_instalada(
            quantidade_paineis=quantidade,
            potencia_painel_wp=potencia_painel_wp,
        )
    )

    return {
        "painel": painel,
        "quantidade_paineis": quantidade,
        "potencia_instalada": potencia_instalada,
    }

# ============================================================
# PB05 - SELEÇÃO DE PAINEL
# ============================================================

def selecionar_painel(
    potencia_fv,
    fabricante=None,
    modelo=None,
):
    """
    Seleciona um painel disponível no dataset.

    Quando fabricante e modelo são informados,
    procura exatamente esse equipamento.

    Quando não são informados, retorna o primeiro
    painel válido disponível no dataset.

    Retorna:
        dicionário do painel selecionado

    Retorna None quando o dataset estiver vazio
        ou nenhum painel compatível com os filtros
        for encontrado.
    """

    paineis = carregar_paineis()

    if not verificar_dataset(
        paineis,
        "paineis.csv"
    ):
        return None

    for painel in paineis:

        try:
            validar_painel(painel)

        except ValueError:
            continue

        fabricante_painel = str(
            painel.get(
                "fabricante",
                ""
            )
        ).strip()

        modelo_painel = str(
            painel.get(
                "modelo",
                ""
            )
        ).strip()

        if fabricante is not None:

            if fabricante_painel.lower() != (
                str(fabricante).strip().lower()
            ):
                continue

        if modelo is not None:

            if modelo_painel.lower() != (
                str(modelo).strip().lower()
            ):
                continue

        return painel

    return None


def listar_paineis():
    """
    Retorna os painéis válidos cadastrados no dataset.
    """

    registros = carregar_paineis()

    if not registros:
        return []

    paineis_validos = []

    for painel in registros:

        try:
            validar_painel(painel)
            paineis_validos.append(painel)

        except ValueError:
            continue

    return paineis_validos

# ============================================================
# PB06 - VALIDAÇÃO DE INVERSOR
# ============================================================

def validar_inversor(inversor):
    """
    Valida os dados mínimos necessários de um inversor.
    """

    if inversor is None:
        raise ValueError(
            "Nenhum inversor foi informado."
        )

    campos_obrigatorios = [
        "fabricante",
        "modelo",
        "potencia_kw",
    ]

    for campo in campos_obrigatorios:

        if campo not in inversor:
            raise ValueError(
                f"O inversor não possui o campo "
                f"'{campo}'."
            )

    try:
        potencia_kw = float(
            str(
                inversor["potencia_kw"]
            ).replace(",", ".")
        )

    except (TypeError, ValueError):
        raise ValueError(
            "A potência do inversor deve ser numérica."
        )

    if potencia_kw <= 0:
        raise ValueError(
            "A potência do inversor deve ser "
            "maior que zero."
        )

    return True


def listar_inversores():
    """
    Retorna os inversores válidos cadastrados
    no dataset.
    """

    registros = carregar_inversores()

    if not registros:
        return []

    inversores_validos = []

    for inversor in registros:

        try:
            validar_inversor(
                inversor
            )

            inversores_validos.append(
                inversor
            )

        except ValueError:
            continue

    return inversores_validos


def selecionar_inversor(
    potencia_instalada,
    fabricante=None,
    modelo=None,
):
    """
    Seleciona um inversor para o sistema fotovoltaico.

    A seleção considera inicialmente a potência instalada
    do campo fotovoltaico.

    A compatibilidade elétrica detalhada será realizada
    posteriormente pelo PB10.

    Retorna:
        dicionário do inversor selecionado

    Retorna None quando nenhum inversor adequado for
    encontrado.
    """

    try:
        potencia_instalada = float(
            potencia_instalada
        )

    except (TypeError, ValueError):
        raise ValueError(
            "A potência instalada deve ser numérica."
        )

    if potencia_instalada <= 0:
        raise ValueError(
            "A potência instalada deve ser maior que zero."
        )

    inversores = listar_inversores()

    if not inversores:
        print(
            "\nNenhum inversor válido "
            "está disponível."
        )

        return None

    candidatos = []

    for inversor in inversores:

        fabricante_inversor = str(
            inversor.get(
                "fabricante",
                ""
            )
        ).strip()

        modelo_inversor = str(
            inversor.get(
                "modelo",
                ""
            )
        ).strip()

        if fabricante is not None:

            if fabricante_inversor.lower() != (
                str(fabricante).strip().lower()
            ):
                continue

        if modelo is not None:

            if modelo_inversor.lower() != (
                str(modelo).strip().lower()
            ):
                continue

        try:
            potencia_inversor = float(
                str(
                    inversor["potencia_kw"]
                ).replace(",", ".")
            )

        except (TypeError, ValueError):
            continue

        # O inversor precisa possuir potência suficiente
        # para o sistema fotovoltaico.
        if potencia_inversor >= potencia_instalada:
            candidatos.append(
                (
                    potencia_inversor,
                    inversor,
                )
            )

    if not candidatos:
        return None

    # Seleciona o menor inversor que atende
    # à potência instalada.
    candidatos.sort(
        key=lambda item: item[0]
    )

    return candidatos[0][1]