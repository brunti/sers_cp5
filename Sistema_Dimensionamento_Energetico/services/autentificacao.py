# ============================================================
# SERVIÇO DE AUTENTICAÇÃO
# ============================================================

from models.usuario import Usuario
from utils.arquivos import carregar_json, salvar_json
from utils.constantes import ARQUIVO_DADOS
from utils.validacoes import ler_texto_obrigatorio


def carregar_dados():
    """
    Carrega os dados gerais do sistema.
    """

    return carregar_json(
        ARQUIVO_DADOS,
        estrutura_padrao={
            "usuarios": []
        }
    )


def salvar_dados(dados):
    """
    Salva os dados gerais do sistema.
    """

    salvar_json(
        ARQUIVO_DADOS,
        dados
    )


def cadastrar_usuario():
    """
    Realiza o cadastro de um novo usuário.
    """

    dados = carregar_dados()

    nome = ler_texto_obrigatorio(
        "Nome: "
    )

    email = ler_texto_obrigatorio(
        "E-mail: "
    ).lower()

    senha = ler_texto_obrigatorio(
        "Senha: "
    )

    # Verifica se o e-mail já está cadastrado.
    for usuario in dados.get("usuarios", []):

        if usuario.get("email", "").lower() == email:

            print(
                "\nJá existe um usuário cadastrado "
                "com esse e-mail."
            )

            return None

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha,
        imoveis=[]
    )

    dados.setdefault(
        "usuarios",
        []
    ).append(
        novo_usuario.para_dict()
    )

    salvar_dados(dados)

    print(
        "\nUsuário cadastrado com sucesso!"
    )

    return novo_usuario


def autenticar_usuario():
    """
    Solicita e-mail e senha e autentica o usuário.
    """

    dados = carregar_dados()

    email = ler_texto_obrigatorio(
        "E-mail: "
    ).lower()

    senha = ler_texto_obrigatorio(
        "Senha: "
    )

    for usuario_dados in dados.get(
        "usuarios",
        []
    ):

        if (
            usuario_dados.get("email", "").lower()
            == email
            and
            usuario_dados.get("senha", "")
            == senha
        ):

            usuario = Usuario.de_dict(
                usuario_dados
            )

            print(
                f"\nLogin realizado com sucesso. "
                f"Bem-vindo, {usuario.nome}!"
            )

            return usuario

    print(
        "\nE-mail ou senha incorretos."
    )

    return None


def listar_usuarios():
    """
    Retorna todos os usuários cadastrados.
    """

    dados = carregar_dados()

    return [
        Usuario.de_dict(usuario)
        for usuario in dados.get(
            "usuarios",
            []
        )
    ]