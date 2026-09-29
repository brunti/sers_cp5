# ============================================================
# SERVIÇO DE EQUIPAMENTOS E DATASETS
# ============================================================

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
    Procura a HSP no dataset utilizando cidade e estado.

    Retorna um dicionário contendo:

        {
            "hsp": valor,
            "origem": origem
        }

    Caso não encontre o local, retorna None.

    IMPORTANTE:
    O funcionamento depende do formato real do hsp.csv.
    Por isso, não estamos assumindo ainda nomes de colunas
    além das possibilidades tratadas abaixo.
    """

    if not cidade or not estado:
        return None

    registros = carregar_hsp()

    cidade_busca = cidade.strip().lower()
    estado_busca = estado.strip().lower()

    for registro in registros:

        cidade_registro = str(
            registro.get(
                "cidade",
                ""
            )
        ).strip().lower()

        estado_registro = str(
            registro.get(
                "estado",
                ""
            )
        ).strip().lower()

        if (
            cidade_registro == cidade_busca
            and
            estado_registro == estado_busca
        ):

            valor_hsp = registro.get(
                "hsp"
            )

            origem = registro.get(
                "origem",
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
                "origem": origem,
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