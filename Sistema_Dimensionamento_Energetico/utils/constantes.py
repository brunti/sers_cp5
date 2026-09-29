# ============================================================
# CONSTANTES DO SISTEMA DE DIMENSIONAMENTO ENERGÉTICO
# ============================================================

# Dias utilizados como referência para o cálculo mensal.
# Fórmula utilizada no projeto:
# P_FV = E_FV / (HSP × D × η)
DIAS_MES_REFERENCIA = 30


# Eficiência global inicial do sistema fotovoltaico.
#
# Este valor ficará centralizado aqui para que possa ser
# alterado posteriormente sem precisar procurar o número
# em várias partes do sistema.
#
# IMPORTANTE:
# O valor definitivo da eficiência deverá ser definido e
# documentado durante a implementação do PB04.
EFICIENCIA_SISTEMA = 0.80


# Valores permitidos para o percentual de atendimento.
PERCENTUAL_MINIMO = 1
PERCENTUAL_MAXIMO = 100


# Limites utilizados para validação de dados.
ANO_MINIMO = 1900

MES_MINIMO = 1
MES_MAXIMO = 12


# Nomes dos meses utilizados na exibição dos relatórios.
NOME_MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Marco",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


# Nome do arquivo principal de persistência.
ARQUIVO_DADOS = "dados.json"


# Nome dos datasets utilizados pelo sistema.
ARQUIVO_PAINEIS = "datasets/paineis.csv"
ARQUIVO_INVERSORES = "datasets/inversores.csv"
ARQUIVO_BATERIAS = "datasets/baterias.csv"
ARQUIVO_HSP = "datasets/hsp.csv"


# ============================================================
# CONFIGURAÇÕES DE BATERIAS
# ============================================================

# Profundidade de descarga padrão.
#
# Este valor poderá posteriormente ser substituído pelo
# parâmetro específico da bateria selecionada no dataset.
DOD_BATERIA_PADRAO = 0.80


# Eficiência padrão da bateria.
#
# Assim como o DoD, posteriormente deverá ser considerada
# a eficiência específica do modelo selecionado quando
# essa informação estiver disponível no dataset.
EFICIENCIA_BATERIA_PADRAO = 0.90


# ============================================================
# CONFIGURAÇÕES DE CUSTOS ADICIONAIS
# ============================================================

# Inicialmente os custos adicionais serão zero.
#
# Posteriormente o sistema poderá permitir que a equipe
# defina valores para estrutura, cabeamento, conectores,
# proteções e instalação, conforme decisão do PB11.
CUSTO_ESTRUTURA = 0.0
CUSTO_CABEAMENTO = 0.0
CUSTO_CONECTORES = 0.0
CUSTO_PROTECOES = 0.0
CUSTO_INSTALACAO = 0.0