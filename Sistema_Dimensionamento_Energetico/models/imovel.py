# ============================================================
# MODELO DE IMÓVEL
# ============================================================


class Imovel:
    """
    Representa um imóvel cadastrado no sistema.
    """

    def __init__(
        self,
        id_imovel,
        nome,
        tipo,
        endereco,
        cidade="",
        estado="",
        latitude=None,
        longitude=None,
        consumos=None,
        dimensionamentos=None,
    ):
        self.id_imovel = id_imovel
        self.nome = nome
        self.tipo = tipo
        self.endereco = endereco

        # Localização utilizada posteriormente para
        # obtenção da HSP.
        self.cidade = cidade
        self.estado = estado
        self.latitude = latitude
        self.longitude = longitude

        self.consumos = (
            consumos if consumos is not None else []
        )

        self.dimensionamentos = (
            dimensionamentos
            if dimensionamentos is not None
            else []
        )

    # ========================================================
    # LOCALIZAÇÃO
    # ========================================================

    def obter_localizacao(self):
        """
        Retorna os dados de localização do imóvel.
        """

        return {
            "endereco": self.endereco,
            "cidade": self.cidade,
            "estado": self.estado,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    # ========================================================
    # CONSUMO
    # ========================================================

    def adicionar_consumo(self, consumo):
        """
        Adiciona um registro de consumo ao imóvel.
        """
        self.consumos.append(consumo)

    def obter_consumos(self):
        """
        Retorna todos os consumos cadastrados.
        """
        return self.consumos

    def calcular_consumo_medio(self):
        """
        Calcula o consumo médio mensal do imóvel.

        Retorna 0 caso não existam registros.
        """
        if not self.consumos:
            return 0.0

        valores = [
            float(consumo["consumo_kwh"])
            for consumo in self.consumos
        ]

        return sum(valores) / len(valores)

    def calcular_consumo_maximo(self):
        """
        Retorna o maior consumo registrado.
        """
        if not self.consumos:
            return 0.0

        valores = [
            float(consumo["consumo_kwh"])
            for consumo in self.consumos
        ]

        return max(valores)

    def obter_mes_maior_consumo(self):
        """
        Retorna o registro correspondente ao maior consumo.
        """
        if not self.consumos:
            return None

        return max(
            self.consumos,
            key=lambda consumo: float(
                consumo["consumo_kwh"]
            ),
        )

    # ========================================================
    # DIMENSIONAMENTO
    # ========================================================

    def adicionar_dimensionamento(self, resultado):
        """
        Adiciona um resultado de dimensionamento ao imóvel.
        """
        self.dimensionamentos.append(resultado)

    def obter_ultimo_dimensionamento(self):
        """
        Retorna o último dimensionamento realizado.
        """
        if not self.dimensionamentos:
            return None

        return self.dimensionamentos[-1]

    # ========================================================
    # PERSISTÊNCIA
    # ========================================================

    def para_dict(self):
        """
        Converte o imóvel para dicionário.
        """

        return {
            "id_imovel": self.id_imovel,
            "nome": self.nome,
            "tipo": self.tipo,
            "endereco": self.endereco,

            "cidade": self.cidade,
            "estado": self.estado,
            "latitude": self.latitude,
            "longitude": self.longitude,

            "consumos": self.consumos,
            "dimensionamentos": self.dimensionamentos,
        }

    @classmethod
    def de_dict(cls, dados):
        """
        Cria um objeto Imovel a partir de um dicionário.
        """

        return cls(
            id_imovel=dados.get(
                "id_imovel"
            ),

            nome=dados.get(
                "nome",
                ""
            ),

            tipo=dados.get(
                "tipo",
                ""
            ),

            endereco=dados.get(
                "endereco",
                ""
            ),

            cidade=dados.get(
                "cidade",
                ""
            ),

            estado=dados.get(
                "estado",
                ""
            ),

            latitude=dados.get(
                "latitude"
            ),

            longitude=dados.get(
                "longitude"
            ),

            consumos=dados.get(
                "consumos",
                []
            ),

            dimensionamentos=dados.get(
                "dimensionamentos",
                []
            ),
        )