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
    executar_pb05,
    executar_pb06,
    executar_armazenamento,
    executar_pb10,
    calcular_geracao_estimada,
    calcular_custos,
)
from services.relatorios import (
    gerar_resumo_final,
    exibir_resumo_final,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def pausar():
    input("\nPressione ENTER para continuar...")


def exibir_imoveis(usuario):
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
# DIMENSIONAMENTO COMPLETO
# PB01 ATÉ PB12
# ============================================================
def executar_dimensionamento(usuario):
    imovel = selecionar_imovel(usuario)
    if imovel is None:
        return
    print("\n")
    print("=" * 60)
    print("       DIMENSIONAMENTO FOTOVOLTAICO")
    print("=" * 60)
    # ========================================================
    # PB01 - CONSUMO
    # ========================================================
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
        f"\nPB01 - Consumo de referência: "
        f"{consumo_referencia:.2f} kWh/mês"
    )
    # ========================================================
    # PB02 - HSP
    # ========================================================
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
        pausar()
        return
    hsp = hsp_resultado["hsp"]
    origem_hsp = hsp_resultado["origem"]
    print(
        f"PB02 - HSP: {hsp:.3f} h"
    )
    print(
        f"Origem: {origem_hsp}"
    )
    # ========================================================
    # PB03 - PERCENTUAL DE ATENDIMENTO
    # ========================================================
    try:
        percentual = (
            solicitar_percentual_atendimento()
        )
    except ValueError as erro:
        print(
            f"\nErro: {erro}"
        )
        pausar()
        return
    print(
        f"PB03 - Atendimento: {percentual:.2f}%"
    )
    # ========================================================
    # PB04 - POTÊNCIA FV
    # ========================================================
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
        f"PB04 - Potência FV necessária: "
        f"{resultado.potencia_fv:.3f} kWp"
    )
    # ========================================================
    # PB05 - PAINEL
    # ========================================================
    try:
        resultado = executar_pb05(
            resultado
        )
    except ValueError as erro:
        print(
            f"\nErro no PB05: {erro}"
        )
        pausar()
        return
    if resultado is None:
        print(
            "\nNenhum painel compatível foi encontrado."
        )
        pausar()
        return
    print("\nPB05 - PAINEL SELECIONADO")
    print("-" * 60)
    print(
        "Fabricante:",
        resultado.painel.get(
            "fabricante",
            ""
        )
    )
    print(
        "Modelo:",
        resultado.painel.get(
            "modelo",
            ""
        )
    )
    print(
        "Potência:",
        resultado.painel.get(
            "potencia_wp",
            ""
        ),
        "Wp"
    )
    print(
        "Quantidade:",
        resultado.quantidade_paineis
    )
    print(
        "Potência instalada:",
        resultado.potencia_instalada,
        "kWp"
    )
    # ========================================================
    # BATERIA
    # ========================================================
    print("\nARMAZENAMENTO")
    print("-" * 60)
    resposta = input(
        "Deseja utilizar bateria? (s/n): "
    ).strip().lower()
    if resposta in ("s", "sim"):
        try:
            autonomia = float(
                input(
                    "Digite a autonomia desejada "
                    "em horas: "
                ).strip()
            )
        except ValueError:
            print(
                "\nAutonomia inválida."
            )
            pausar()
            return
        if autonomia <= 0:
            print(
                "\nA autonomia deve ser maior que zero."
            )
            pausar()
            return
        try:
            resultado = executar_armazenamento(
                resultado=resultado,
                autonomia_horas=autonomia,
            )
        except ValueError as erro:
            print(
                f"\nErro no armazenamento: {erro}"
            )
            pausar()
            return
        if resultado.baterias is None:
            print(
                "\nNenhuma bateria compatível "
                "foi encontrada."
            )
            pausar()
            return
        print(
            "\nBateria selecionada:"
        )
        print(
            "Fabricante:",
            resultado.baterias.get(
                "fabricante",
                ""
            )
        )
        print(
            "Modelo:",
            resultado.baterias.get(
                "modelo",
                ""
            )
        )
        print(
            "Quantidade:",
            resultado.quantidade_baterias
        )
        print(
            "Capacidade instalada:",
            resultado.capacidade_bateria_instalada,
            "kWh"
        )
    else:
        resultado.possui_bateria = False
        resultado.autonomia_horas = 0.0
        resultado.capacidade_bateria_necessaria = 0.0
        resultado.baterias = None
        resultado.quantidade_baterias = 0
        resultado.capacidade_bateria_instalada = 0.0
        print(
            "\nSistema sem bateria."
        )
    # ========================================================
    # PB06 - INVERSOR
    # ========================================================
    try:
        resultado = executar_pb06(
            resultado
        )
    except ValueError as erro:
        print(
            f"\nErro no PB06: {erro}"
        )
        pausar()
        return
    if resultado is None:
        print(
            "\nNenhum inversor compatível foi encontrado."
        )
        pausar()
        return
    print("\nPB06 - INVERSOR SELECIONADO")
    print("-" * 60)
    print(
        "Fabricante:",
        resultado.inversor.get(
            "fabricante",
            ""
        )
    )
    print(
        "Modelo:",
        resultado.inversor.get(
            "modelo",
            ""
        )
    )
    print(
        "Potência nominal:",
        resultado.inversor.get(
            "potencia_nominal_kw",
            ""
        ),
        "kW"
    )
    print(
        "Potência FV máxima:",
        resultado.inversor.get(
            "potencia_fv_max_kw",
            ""
        ),
        "kW"
    )
    # ========================================================
    # PB10 - COMPATIBILIDADE
    # ========================================================
    try:
        resultado = executar_pb10(
            resultado
        )
    except ValueError as erro:
        print(
            f"\nErro no PB10: {erro}"
        )
        pausar()
        return
    print("\nPB10 - COMPATIBILIDADE")
    print("-" * 60)
    print(
        "Sistema compatível:",
        resultado.compatibilidade.get(
            "compativel",
            False
        )
    )
    problemas = resultado.compatibilidade.get(
        "problemas",
        []
    )
    if problemas:
        print("\nProblemas:")
        for problema in problemas:
            print(
                "-",
                problema
            )
    # ========================================================
    # GERAÇÃO ESTIMADA
    # ========================================================
    resultado.geracao_estimada = (
        calcular_geracao_estimada(
            potencia_instalada=(
                resultado.potencia_instalada
            ),
            hsp=resultado.hsp,
            dias_periodo=resultado.dias_periodo,
            eficiencia=resultado.eficiencia_sistema,
        )
    )
    # ========================================================
    # CUSTOS
    # ========================================================
    try:
        resultado = calcular_custos(
            resultado
        )
    except ValueError as erro:
        print(
            f"\nErro ao calcular custos: {erro}"
        )
        pausar()
        return
    # ========================================================
    # PB12 - RELATÓRIO FINAL
    # ========================================================
    try:
        relatorio = gerar_resumo_final(
            resultado
        )
    except ValueError as erro:
        print(
            f"\nErro no PB12: {erro}"
        )
        pausar()
        return
    # ========================================================
    # MOSTRA O RELATÓRIO PARA O USUÁRIO
    # ========================================================
    exibir_resumo_final(
        relatorio
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
        print("4 - Dimensionamento FV completo")
        print("0 - Sair")
        opcao = input(
            "\nEscolha: "
        ).strip()
        if opcao == "1":
            cadastrar_imovel(usuario)
            pausar()
        elif opcao == "2":
            exibir_imoveis(usuario)
            pausar()
        elif opcao == "3":
            menu_consumo(usuario)
        elif opcao == "4":
            executar_dimensionamento(
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
        opcao = input(
            "\nEscolha: "
        ).strip()
        if opcao == "1":
            cadastrar_usuario()
            pausar()
        elif opcao == "2":
            usuario = autenticar_usuario()
            if usuario is not None:
                menu_usuario(
                    usuario
                )
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
