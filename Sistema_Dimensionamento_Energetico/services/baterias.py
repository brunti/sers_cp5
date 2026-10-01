# ============================================================
# SERVIÇO DE BATERIAS
# ============================================================

from math import ceil

from services.equipamentos import carregar_baterias


# ============================================================
# CONVERSÃO
# ============================================================

def converter_float(valor):
    """
    Converte valores numéricos para float.
    Aceita ponto ou vírgula decimal.
    """

    try:
        return float(
            str(valor).replace(",", ".")
        )

    except (TypeError, ValueError):
        return None


# ============================================================
# PB08 - CONSUMO MÉDIO DIÁRIO
# ============================================================

def calcular_consumo_diario(
    consumo_referencia,
    dias=30,
):
    """
    Calcula o consumo médio diário.

    Fórmula:

        E_d = C_m / D
    """

    consumo = converter_float(
        consumo_referencia
    )

    dias = converter_float(
        dias
    )

    if consumo is None:
        raise ValueError(
            "O consumo de referência deve ser numérico."
        )

    if dias is None or dias <= 0:
        raise ValueError(
            "A quantidade de dias deve ser maior que zero."
        )

    if consumo < 0:
        raise ValueError(
            "O consumo não pode ser negativo."
        )

    return consumo / dias


# ============================================================
# PB08 - ENERGIA DE AUTONOMIA
# ============================================================

def calcular_energia_autonomia(
    consumo_diario,
    autonomia_horas,
):
    """
    Calcula a energia necessária para a autonomia desejada.

    Fórmula:

        E_autonomia = E_d × (A / 24)
    """

    consumo_diario = converter_float(
        consumo_diario
    )

    autonomia_horas = converter_float(
        autonomia_horas
    )

    if consumo_diario is None:
        raise ValueError(
            "O consumo diário deve ser numérico."
        )

    if autonomia_horas is None:
        raise ValueError(
            "A autonomia deve ser numérica."
        )

    if consumo_diario < 0:
        raise ValueError(
            "O consumo diário não pode ser negativo."
        )

    if autonomia_horas < 0:
        raise ValueError(
            "A autonomia não pode ser negativa."
        )

    if autonomia_horas > 24:
        raise ValueError(
            "A autonomia não pode ser maior que 24 horas."
        )

    return (
        consumo_diario
        * (autonomia_horas / 24)
    )


# ============================================================
# PB08 - CAPACIDADE DA BATERIA
# ============================================================

def calcular_capacidade_bateria(
    energia_autonomia,
    dod,
    eficiencia_bateria,
):
    """
    Calcula a capacidade nominal necessária da bateria.

    Fórmula:

        C_bat = E_autonomia / (DoD × η_bat)
    """

    energia_autonomia = converter_float(
        energia_autonomia
    )

    dod = converter_float(
        dod
    )

    eficiencia_bateria = converter_float(
        eficiencia_bateria
    )

    if energia_autonomia is None:
        raise ValueError(
            "A energia de autonomia deve ser numérica."
        )

    if dod is None or dod <= 0 or dod > 1:
        raise ValueError(
            "O DoD deve estar entre 0 e 1."
        )

    if (
        eficiencia_bateria is None
        or eficiencia_bateria <= 0
        or eficiencia_bateria > 1
    ):
        raise ValueError(
            "A eficiência da bateria deve estar entre 0 e 1."
        )

    if energia_autonomia < 0:
        raise ValueError(
            "A energia de autonomia não pode ser negativa."
        )

    return (
        energia_autonomia
        / (dod * eficiencia_bateria)
    )


# ============================================================
# PB08 - DIMENSIONAMENTO COMPLETO
# ============================================================

def dimensionar_armazenamento(
    consumo_referencia,
    autonomia_horas,
    dod=0.80,
    eficiencia_bateria=0.90,
    dias=30,
):
    """
    Executa o PB08 completo.
    """

    consumo_diario = calcular_consumo_diario(
        consumo_referencia=consumo_referencia,
        dias=dias,
    )

    energia_autonomia = calcular_energia_autonomia(
        consumo_diario=consumo_diario,
        autonomia_horas=autonomia_horas,
    )

    capacidade_necessaria = calcular_capacidade_bateria(
        energia_autonomia=energia_autonomia,
        dod=dod,
        eficiencia_bateria=eficiencia_bateria,
    )

    return {
        "consumo_diario": consumo_diario,
        "autonomia_horas": autonomia_horas,
        "energia_autonomia": energia_autonomia,
        "dod": dod,
        "eficiencia_bateria": eficiencia_bateria,
        "capacidade_necessaria": capacidade_necessaria,
    }


# ============================================================
# PB09 - VALIDAÇÃO DE BATERIA
# ============================================================

def validar_bateria(bateria):
    """
    Valida os campos mínimos de uma bateria
    conforme o dataset baterias.csv.
    """

    if bateria is None:
        raise ValueError(
            "Nenhuma bateria foi informada."
        )

    campos_obrigatorios = [
        "fabricante",
        "modelo",
        "capacidade_nominal_kwh",
    ]

    for campo in campos_obrigatorios:

        if campo not in bateria:
            raise ValueError(
                f"A bateria não possui o campo '{campo}'."
            )

    capacidade = converter_float(
        bateria["capacidade_nominal_kwh"]
    )

    if capacidade is None or capacidade <= 0:
        raise ValueError(
            "A capacidade da bateria deve ser maior que zero."
        )

    return True


# ============================================================
# PB09 - LISTAR BATERIAS
# ============================================================

def listar_baterias():
    """
    Retorna somente baterias válidas do dataset.
    """

    registros = carregar_baterias()

    if not registros:
        return []

    baterias_validas = []

    for bateria in registros:

        try:
            validar_bateria(bateria)

            baterias_validas.append(
                bateria
            )

        except ValueError:
            continue

    return baterias_validas


# ============================================================
# PB09 - SELEÇÃO DA BATERIA
# ============================================================

def selecionar_bateria(
    capacidade_necessaria,
    fabricante=None,
    modelo=None,
):
    """
    Seleciona a bateria para atender à capacidade necessária.

    A quantidade de baterias será calculada separadamente
    por calcular_quantidade_baterias().

    O dataset utiliza:
        capacidade_nominal_kwh
    """

    capacidade_necessaria = converter_float(
        capacidade_necessaria
    )

    if (
        capacidade_necessaria is None
        or capacidade_necessaria <= 0
    ):
        raise ValueError(
            "A capacidade necessária deve ser maior que zero."
        )

    baterias = listar_baterias()

    candidatos = []

    for bateria in baterias:

        if fabricante is not None:
            if str(
                bateria.get("fabricante", "")
            ).strip().lower() != str(
                fabricante
            ).strip().lower():
                continue

        if modelo is not None:
            if str(
                bateria.get("modelo", "")
            ).strip().lower() != str(
                modelo
            ).strip().lower():
                continue

        capacidade = converter_float(
            bateria.get(
                "capacidade_nominal_kwh"
            )
        )

        if capacidade is None or capacidade <= 0:
            continue

        candidatos.append(
            (
                capacidade,
                bateria,
            )
        )

    if not candidatos:
        return None

    # Escolhe a menor bateria disponível.
    # A quantidade necessária será calculada depois.
    candidatos.sort(
        key=lambda item: item[0]
    )

    return candidatos[0][1]

# ============================================================
# PB09 - QUANTIDADE DE BATERIAS
# ============================================================

def calcular_quantidade_baterias(
    capacidade_necessaria,
    capacidade_bateria,
):
    """
    Calcula a quantidade de baterias necessárias.

    Fórmula:

        N_bat = teto(
            C_necessária / C_bateria
        )
    """

    capacidade_necessaria = converter_float(
        capacidade_necessaria
    )

    capacidade_bateria = converter_float(
        capacidade_bateria
    )

    if (
        capacidade_necessaria is None
        or capacidade_necessaria <= 0
    ):
        raise ValueError(
            "A capacidade necessária deve ser maior que zero."
        )

    if (
        capacidade_bateria is None
        or capacidade_bateria <= 0
    ):
        raise ValueError(
            "A capacidade da bateria deve ser maior que zero."
        )

    return ceil(
        capacidade_necessaria
        / capacidade_bateria
    )

# ============================================================
# PB09 - DIMENSIONAMENTO COMPLETO DA BATERIA
# ============================================================

def dimensionar_bateria(
    capacidade_necessaria,
    fabricante=None,
    modelo=None,
):
    """
    Executa o PB09 completo.

    1. Seleciona uma bateria.
    2. Calcula a quantidade necessária.
    3. Calcula a capacidade instalada.

    Retorna None se nenhuma bateria atender
    aos critérios.
    """

    bateria = selecionar_bateria(
        capacidade_necessaria=capacidade_necessaria,
        fabricante=fabricante,
        modelo=modelo,
    )

    if bateria is None:
        return None

    capacidade_bateria = converter_float(
        bateria.get("capacidade_kwh")
    )

    quantidade = calcular_quantidade_baterias(
        capacidade_necessaria=capacidade_necessaria,
        capacidade_bateria=capacidade_bateria,
    )

    capacidade_instalada = (
        capacidade_bateria
        * quantidade
    )

    return {
        "bateria": bateria,
        "quantidade_baterias": quantidade,
        "capacidade_bateria_instalada": (
            capacidade_instalada
        ),
    }

def dimensionar_baterias(
    capacidade_necessaria,
    fabricante=None,
    modelo=None,
):
    """
    Executa o PB09 completo.

    Seleciona uma bateria e calcula a quantidade necessária.

    Retorna:
        {
            "bateria": bateria selecionada,
            "quantidade": quantidade,
            "capacidade_unitaria": ...,
            "capacidade_instalada": ...
        }
    """

    bateria = selecionar_bateria(
        capacidade_necessaria=capacidade_necessaria,
        fabricante=fabricante,
        modelo=modelo,
    )

    if bateria is None:
        return None

    capacidade_unitaria = converter_float(
        bateria.get("capacidade_nominal_kwh")
    )

    quantidade = calcular_quantidade_baterias(
        capacidade_necessaria=capacidade_necessaria,
        capacidade_bateria=capacidade_unitaria,
    )

    capacidade_instalada = (
        capacidade_unitaria * quantidade
    )

    return {
        "bateria": bateria,
        "quantidade": quantidade,
        "capacidade_unitaria": capacidade_unitaria,
        "capacidade_instalada": capacidade_instalada,
    }


# ============================================================
# PB09/PB11 - SELEÇÃO DE BATERIA COM PREÇO
# ============================================================

def selecionar_bateria_com_preco(
    capacidade_necessaria,
    fabricante=None,
    modelo=None,
):
    """
    Seleciona uma bateria que:

    1. Possua capacidade válida;
    2. Possua preço válido;
    3. Permita calcular a quantidade necessária.

    Não altera o dataset.
    """

    capacidade_necessaria = converter_float(
        capacidade_necessaria
    )

    if (
        capacidade_necessaria is None
        or capacidade_necessaria <= 0
    ):
        raise ValueError(
            "A capacidade necessária deve ser maior que zero."
        )

    baterias = listar_baterias()

    candidatos = []

    for bateria in baterias:

        # Filtro por fabricante
        if fabricante is not None:

            if str(
                bateria.get("fabricante", "")
            ).strip().lower() != str(
                fabricante
            ).strip().lower():

                continue

        # Filtro por modelo
        if modelo is not None:

            if str(
                bateria.get("modelo", "")
            ).strip().lower() != str(
                modelo
            ).strip().lower():

                continue

        capacidade = converter_float(
            bateria.get(
                "capacidade_nominal_kwh"
            )
        )

        preco = converter_float(
            bateria.get("preco")
        )

        if capacidade is None or capacidade <= 0:
            continue

        if preco is None or preco <= 0:
            continue

        candidatos.append(
            (
                capacidade,
                preco,
                bateria,
            )
        )

    if not candidatos:
        return None

    # Escolhe inicialmente a menor capacidade válida.
    candidatos.sort(
        key=lambda item: item[0]
    )

    return candidatos[0][2]