# ============================================================
# MODELO DE USUÁRIO
# ============================================================


class Usuario:
    """
    Representa um usuário do sistema.
    """

    def __init__(
        self,
        nome,
        email,
        senha,
        imoveis=None,
    ):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.imoveis = imoveis if imoveis is not None else []

    def adicionar_imovel(self, imovel_id):
        """
        Adiciona um imóvel à lista de imóveis do usuário.
        """
        if imovel_id not in self.imoveis:
            self.imoveis.append(imovel_id)

    def remover_imovel(self, imovel_id):
        """
        Remove um imóvel da lista do usuário.
        """
        if imovel_id in self.imoveis:
            self.imoveis.remove(imovel_id)

    def para_dict(self):
        """
        Converte o usuário para dicionário,
        permitindo salvar no dados.json.
        """
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "imoveis": self.imoveis,
        }

    @classmethod
    def de_dict(cls, dados):
        """
        Cria um objeto Usuario a partir de um dicionário.
        """
        return cls(
            nome=dados.get("nome", ""),
            email=dados.get("email", ""),
            senha=dados.get("senha", ""),
            imoveis=dados.get("imoveis", []),
        )