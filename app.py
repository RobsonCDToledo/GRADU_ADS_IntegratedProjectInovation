"""
===========================================
Sistema de Gestão Clínica Vida+
Módulo: menu.py
------------------------------------------------------------
Descrição:
    Responsável por exibir o menu principal e gerenciar a 
    navegação entre as funcionalidades:
        - Cadastrar
        - Agendamentos de Consultas
        - Relatórios
        - Encerrar aplicação

Autor: Robson Carlos Donizette de Toledo
Data de criação: 16/08/2025
Última atualização: 16/08/2025
Versão: 1.0
============================================================
"""

from cli.cad.cadastro_pacientes import form_cadastro_paciente
from cli.cad.cadastro_medicos import form_cadastro_medico
from cli.view.view_tables import view_pacientes
from cli.view.view_tables import view_medicos


def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    print("\n=== Sistema de Gestão Clínica Vida+ ")
    print("1. Cadastrar")
    print("2. Agendamento de Consultas")
    print("3. Relatórios")
    print("4. Sair")


def main():
    """
    Função principal que gerencia o fluxo do sistema.
    """
    while True:
        exibir_menu()
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            print("\n === Selecione o tipo de cadastro===")
            print("1 - Cadastro de Médicos: ")
            print("2 - Cadastro de Pacientes: ")
            print("3 - Voltar")

            tipo_cadastro = input("selecione uma opção: ")
            if tipo_cadastro == "1":
                form_cadastro_medico()
            elif tipo_cadastro == "2":
                form_cadastro_paciente()
            elif tipo_cadastro == "3":
                exibir_menu()
            elif tipo_cadastro not in ("1", "2", "3"):
                print("Opção inválida. Tente novamente.")
            else:
                print("Selecione uma opção valida")

        elif opcao == "2":
            print("Abrindo Agendamento de Consultas")
        elif opcao == "3":
            print("Abrindo Relatórios")
            print("\n === Selecione o tipo de cadastro===")
            print("1 - Médicos: ")
            print("2 - Pacientes: ")
            print("3 - Voltar")

            tipo_relatorio = input("Selecione uma opção de relatório: ")
            if tipo_relatorio == "1":
                print("=== Médicos ===")
                view_medicos()
            elif tipo_relatorio == "2":
                print("=== Pacientes ===")
                view_pacientes()
            elif tipo_relatorio == "3":
                exibir_menu()
            elif tipo_relatorio not in ("1", "2"):
                print("Opção inválida. Tente novamente.")
            else:
                print("Selecione uma opção valida")
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
