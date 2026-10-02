# ============================================================
# SISTEMA DE DIMENSIONAMENTO ENERGÉTICO
# ============================================================

from services.autenticacao import (
    cadastrar_usuario,
    autenticar_usuario,
)

from services.imoveis import (
    cadastrar_imovel,
    listar_imoveis,
    adicionar_consumo,
    calcular_consumo_medio,
    calcular_consumo_maximo,
    obter_mes_maior_consumo,
)

from services.dimensionamento import (
    solicitar_percentual_atendimento,
    obter_hsp_imovel,
    criar_resultado_base,
    gerar_resumo_dimensionamento_basico,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def pausar():
    """
    Pausa a execução até o usuário pressionar ENTER.
    """
    input("\nPressione ENTER para continuar...")


def exibir_imoveis(usuario):
    """
    Exibe os imóveis cadastrados pelo usuário.
    """

    imoveis = listar_imoveis(usuario)

    if not imoveis:
        print("\nNenhum imóvel cadastrado.")
        return []

    print("\n============================================")
    print("MEUS IMÓVEIS")
    print("============================================")

    for imovel in imoveis:
        print(
            f"\nID: {imovel.id_imovel}"
            f"\nNome: {imovel.nome}"
            f"\nTipo: {imovel.tipo}"
            f"\nEndereço: {imovel.endereco}"
            f"\nCidade: {imovel.cidade}"
            f"\nEstado: {imovel.estado}"
        )

    return imoveis


def selecionar_imovel(usuario):
    """
    Permite ao usuário selecionar um imóvel.
    """

    imoveis = listar_imoveis(usuario)

    if not imoveis:
        print("\nNenhum imóvel cadastrado.")
        return None

    exibir_imoveis(usuario)

    while True:

        valor = input(
            "\nDigite o ID do imóvel: "
        ).strip()

        try:
            id_imovel = int(valor)
        except ValueError:
            print("Digite um ID numérico.")
            continue

        for imovel in imoveis:

            if imovel.id_imovel == id_imovel:
                return imovel

        print("Imóvel não encontrado.")


# ============================================================
# MENU DE CONSUMO
# ============================================================

def menu_consumo(usuario):
    """
    Menu relacionado ao consumo energético.
    """

    imovel = selecionar_imovel(usuario)

    if imovel is None:
        return

    while True:

        print("\n============================================")
        print("CONSUMO ENERGÉTICO")
        print("============================================")
        print("1 - Adicionar consumo")
        print("2 - Ver consumos")
        print("3 - Ver consumo médio")
        print("4 - Ver consumo máximo")
        print("5 - Ver mês de maior consumo")
        print("0 - Voltar")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":

            adicionar_consumo(
                usuario,
                imovel.id_imovel
            )

        elif opcao == "2":

            consumos = imovel.obter_consumos()

            if not consumos:
                print("\nNenhum consumo cadastrado.")
            else:
                print(
                    "\n============================================"
                )
                print("CONSUMOS")
                print(
                    "============================================"
                )

                for consumo in consumos:
                    print(
                        f"{consumo['mes']:02d}/"
                        f"{consumo['ano']} - "
                        f"{consumo['consumo_kwh']:.2f} kWh"
                    )

        elif opcao == "3":

            media = calcular_consumo_medio(
                usuario,
                imovel.id_imovel
            )

            print(
                f"\nConsumo médio: "
                f"{media:.2f} kWh/mês"
            )

        elif opcao == "4":

            maximo = calcular_consumo_maximo(
                usuario,
                imovel.id_imovel
            )

            print(
                f"\nMaior consumo: "
                f"{maximo:.2f} kWh/mês"
            )

        elif opcao == "5":

            maior = obter_mes_maior_consumo(
                usuario,
                imovel.id_imovel
            )

            if maior is None:
                print(
                    "\nNenhum consumo cadastrado."
                )
            else:
                print(
                    f"\nMaior consumo ocorreu em "
                    f"{maior['mes']:02d}/"
                    f"{maior['ano']}: "
                    f"{maior['consumo_kwh']:.2f} kWh"
                )

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")

        if opcao != "0":
            pausar()


# ============================================================
# PB01 ATÉ PB04
# ============================================================

def executar_dimensionamento_basico(usuario):
    """
    Executa o fluxo inicial de dimensionamento:

    PB01 - consumo de referência
    PB02 - HSP
    PB03 - percentual de atendimento
    PB04 - potência FV
    """

    imovel = selecionar_imovel(usuario)

    if imovel is None:
        return

    print("\n============================================")
    print("DIMENSIONAMENTO FOTOVOLTAICO")
    print("============================================")

    # --------------------------------------------------------
    # PB01
    # --------------------------------------------------------

    consumo_referencia = calcular_consumo_medio(
        usuario,
        imovel.id_imovel
    )

    if consumo_referencia <= 0:
        print(
            "\nO imóvel não possui consumo suficiente "
            "para realizar o dimensionamento."
        )

        pausar()
        return

    print(
        f"\nConsumo de referência: "
        f"{consumo_referencia:.2f} kWh/mês"
    )

    # --------------------------------------------------------
    # PB02
    # --------------------------------------------------------

    try:

        hsp_resultado = obter_hsp_imovel(
            imovel
        )

    except ValueError as erro:

        print(
            f"\nErro ao obter HSP: {erro}"
        )

        pausar()
        return

    if hsp_resultado is None:

        print(
            "\nNão foi possível obter a HSP."
        )

        print(
            "Verifique se o hsp.csv possui "
            "dados para essa localização."
        )

        pausar()
        return

    hsp = hsp_resultado["hsp"]
    origem_hsp = hsp_resultado["origem"]

    print(
        f"\nHSP encontrada: "
        f"{hsp:.2f} h"
    )

    print(
        f"Origem: {origem_hsp}"
    )

    # --------------------------------------------------------
    # PB03
    # --------------------------------------------------------

    try:

        percentual = solicitar_percentual_atendimento()

    except ValueError as erro:

        print(
            f"\nErro: {erro}"
        )

        pausar()
        return

    # --------------------------------------------------------
    # PB04
    # --------------------------------------------------------

    try:

        resultado = criar_resultado_base(
            consumos=imovel.obter_consumos(),
            percentual_atendimento=percentual,
            hsp=hsp,
            origem_hsp=origem_hsp,
        )

    except ValueError as erro:

        print(
            f"\nErro no dimensionamento: {erro}"
        )

        pausar()
        return

    print(
        gerar_resumo_dimensionamento_basico(
            resultado
        )
    )

    pausar()


# ============================================================
# MENU PRINCIPAL DO USUÁRIO
# ============================================================

def menu_usuario(usuario):

    while True:

        print("\n============================================")
        print("SISTEMA DE DIMENSIONAMENTO ENERGÉTICO")
        print("============================================")
        print(
            f"Usuário: {usuario.nome}"
        )

        print("\n1 - Cadastrar imóvel")
        print("2 - Listar imóveis")
        print("3 - Consumo energético")
        print("4 - Dimensionamento FV")
        print("0 - Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":

            cadastrar_imovel(usuario)
            pausar()

        elif opcao == "2":

            exibir_imoveis(usuario)
            pausar()

        elif opcao == "3":

            menu_consumo(usuario)

        elif opcao == "4":

            executar_dimensionamento_basico(
                usuario
            )

        elif opcao == "0":

            print(
                "\nEncerrando sessão..."
            )

            break

        else:

            print(
                "\nOpção inválida."
            )


# ============================================================
# MENU INICIAL
# ============================================================

def menu_inicial():

    while True:

        print("\n============================================")
        print("SISTEMA DE DIMENSIONAMENTO ENERGÉTICO")
        print("============================================")

        print("\n1 - Cadastrar usuário")
        print("2 - Login")
        print("0 - Encerrar")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":

            cadastrar_usuario()
            pausar()

        elif opcao == "2":

            usuario = autenticar_usuario()

            if usuario is not None:
                menu_usuario(usuario)

        elif opcao == "0":

            print(
                "\nSistema encerrado."
            )

            break

        else:

            print(
                "\nOpção inválida."
            )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    menu_inicial()