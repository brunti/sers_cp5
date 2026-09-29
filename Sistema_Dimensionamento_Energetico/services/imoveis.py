# ============================================================
# SERVIÇO DE IMÓVEIS
# ============================================================

from models.imovel import Imovel
from utils.arquivos import carregar_json, salvar_json
from utils.constantes import ARQUIVO_DADOS
from utils.validacoes import (
    ler_texto_obrigatorio,
    ler_numero_obrigatorio,
    ler_mes,
    ler_ano,
)


def carregar_dados():
    """
    Carrega os dados do sistema.
    """

    return carregar_json(
        ARQUIVO_DADOS,
        estrutura_padrao={
            "usuarios": []
        }
    )


def salvar_dados(dados):
    """
    Salva os dados do sistema.
    """

    salvar_json(
        ARQUIVO_DADOS,
        dados
    )


def obter_usuario_dados(dados, email):
    """
    Localiza o usuário pelo e-mail.
    """

    for usuario in dados.get(
        "usuarios",
        []
    ):

        if usuario.get(
            "email",
            ""
        ).lower() == email.lower():

            return usuario

    return None


def gerar_id_imovel(imoveis):
    """
    Gera um novo ID numérico para o imóvel.
    """

    if not imoveis:
        return 1

    ids = []

    for imovel in imoveis:

        try:
            ids.append(
                int(imovel.get(
                    "id_imovel",
                    0
                ))
            )

        except (TypeError, ValueError):
            continue

    if not ids:
        return 1

    return max(ids) + 1


def cadastrar_imovel(usuario):
    """
    Cadastra um novo imóvel para o usuário.
    """

    dados = carregar_dados()

    usuario_dados = obter_usuario_dados(
        dados,
        usuario.email
    )

    if usuario_dados is None:
        print(
            "\nUsuário não encontrado."
        )
        return None

    nome = ler_texto_obrigatorio(
        "Nome do imóvel: "
    )

    tipo = ler_texto_obrigatorio(
        "Tipo do imóvel: "
    )

    endereco = ler_texto_obrigatorio(
        "Endereço: "
    )

    cidade = ler_texto_obrigatorio(
        "Cidade: "
    )

    estado = ler_texto_obrigatorio(
        "Estado/UF: "
    )

    imoveis = usuario_dados.setdefault(
        "imoveis",
        []
    )

    novo_id = gerar_id_imovel(
        imoveis
    )

    novo_imovel = Imovel(
        id_imovel=novo_id,
        nome=nome,
        tipo=tipo,
        endereco=endereco,
        cidade=cidade,
        estado=estado,
        consumos=[],
        dimensionamentos=[]
    )

    imoveis.append(
        novo_imovel.para_dict()
    )

    salvar_dados(dados)

    usuario.imoveis.append(
        novo_id
    )

    print(
        "\nImóvel cadastrado com sucesso!"
    )

    return novo_imovel


def listar_imoveis(usuario):
    """
    Retorna os imóveis pertencentes ao usuário.
    """

    dados = carregar_dados()

    usuario_dados = obter_usuario_dados(
        dados,
        usuario.email
    )

    if usuario_dados is None:
        return []

    return [
        Imovel.de_dict(imovel)
        for imovel in usuario_dados.get(
            "imoveis",
            []
        )
    ]


def buscar_imovel(usuario, id_imovel):
    """
    Localiza um imóvel pelo ID.
    """

    imoveis = listar_imoveis(
        usuario
    )

    for imovel in imoveis:

        if str(imovel.id_imovel) == str(
            id_imovel
        ):

            return imovel

    return None


def adicionar_consumo(usuario, id_imovel):
    """
    Adiciona um consumo mensal ao imóvel.
    """

    dados = carregar_dados()

    usuario_dados = obter_usuario_dados(
        dados,
        usuario.email
    )

    if usuario_dados is None:
        print(
            "\nUsuário não encontrado."
        )
        return False

    imovel_dados = None

    for imovel in usuario_dados.get(
        "imoveis",
        []
    ):

        if str(imovel.get(
            "id_imovel"
        )) == str(id_imovel):

            imovel_dados = imovel
            break

    if imovel_dados is None:
        print(
            "\nImóvel não encontrado."
        )
        return False

    mes = ler_mes()

    ano = ler_ano()

    consumo_kwh = ler_numero_obrigatorio(
        "Consumo mensal (kWh): "
    )

    consumos = imovel_dados.setdefault(
        "consumos",
        []
    )

    # Verifica se já existe registro
    # para o mesmo mês/ano.
    for consumo in consumos:

        if (
            consumo.get("mes") == mes
            and
            consumo.get("ano") == ano
        ):

            print(
                "\nJá existe um consumo "
                "cadastrado para esse mês e ano."
            )

            return False

    novo_consumo = {
        "mes": mes,
        "ano": ano,
        "consumo_kwh": consumo_kwh
    }

    consumos.append(
        novo_consumo
    )

    salvar_dados(dados)

    print(
        "\nConsumo cadastrado com sucesso!"
    )

    return True


def obter_consumos(usuario, id_imovel):
    """
    Retorna os consumos de um imóvel.
    """

    imovel = buscar_imovel(
        usuario,
        id_imovel
    )

    if imovel is None:
        return []

    return imovel.obter_consumos()


def calcular_consumo_medio(
    usuario,
    id_imovel
):
    """
    Calcula o consumo médio do imóvel.
    """

    imovel = buscar_imovel(
        usuario,
        id_imovel
    )

    if imovel is None:
        return 0.0

    return imovel.calcular_consumo_medio()


def calcular_consumo_maximo(
    usuario,
    id_imovel
):
    """
    Calcula o consumo máximo do imóvel.
    """

    imovel = buscar_imovel(
        usuario,
        id_imovel
    )

    if imovel is None:
        return 0.0

    return imovel.calcular_consumo_maximo()


def obter_mes_maior_consumo(
    usuario,
    id_imovel
):
    """
    Retorna o mês de maior consumo.
    """

    imovel = buscar_imovel(
        usuario,
        id_imovel
    )

    if imovel is None:
        return None

    return imovel.obter_mes_maior_consumo()


def atualizar_imovel(
    usuario,
    id_imovel
):
    """
    Atualiza os dados básicos do imóvel.
    """

    dados = carregar_dados()

    usuario_dados = obter_usuario_dados(
        dados,
        usuario.email
    )

    if usuario_dados is None:
        return False

    for imovel in usuario_dados.get(
        "imoveis",
        []
    ):

        if str(imovel.get(
            "id_imovel"
        )) == str(id_imovel):

            nome = ler_texto_obrigatorio(
                "Novo nome: "
            )

            tipo = ler_texto_obrigatorio(
                "Novo tipo: "
            )

            endereco = ler_texto_obrigatorio(
                "Novo endereço: "
            )

            imovel["nome"] = nome
            imovel["tipo"] = tipo
            imovel["endereco"] = endereco

            salvar_dados(dados)

            print(
                "\nImóvel atualizado com sucesso!"
            )

            return True

    print(
        "\nImóvel não encontrado."
    )

    return False


def excluir_imovel(
    usuario,
    id_imovel
):
    """
    Exclui um imóvel do usuário.
    """

    dados = carregar_dados()

    usuario_dados = obter_usuario_dados(
        dados,
        usuario.email
    )

    if usuario_dados is None:
        return False

    imoveis = usuario_dados.get(
        "imoveis",
        []
    )

    for indice, imovel in enumerate(
        imoveis
    ):

        if str(imovel.get(
            "id_imovel"
        )) == str(id_imovel):

            imoveis.pop(indice)

            if id_imovel in usuario.imoveis:
                usuario.imoveis.remove(
                    id_imovel
                )

            salvar_dados(dados)

            print(
                "\nImóvel excluído com sucesso!"
            )

            return True

    print(
        "\nImóvel não encontrado."
    )

    return False