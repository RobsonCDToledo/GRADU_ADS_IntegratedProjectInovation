""""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: cadastro_medicos.py
------------------------------------------------------------
Descrição:
    Responsável por exibir um formulário para cadastro de médicos.

Autor: Robson Carlos Donizette de Toledo
Data de criação: 16/08/2025
Última atualização: 16/08/2025
Versão: 1.0
============================================================
"""


import re
import sqlite3
from db.repos.repositorio_medicos import inserir_medico, buscar_crm


def input_nome():
    """
    Função para entrada do nome do médico.
    """
    while True:
        nome = input("Nome do médico: ").strip().title()
        if not nome:
            print(
                "O nome do médico é obrigatório. Por Favor, preencha o campo corretamente.")
            continue
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
            print("O nome contém caracteres inválidos. Use apenas letras e espaços.")
            continue
        return nome


def input_crm():
    """
    Função para entrada do CRM do médico.
    """
    while True:
        crm = input("Insira o CRM do médico: ").upper()
        padrao_crm = r"^\d{5}/[A-Z]{2}$"
        existe_crm = buscar_crm(crm)
        if re.fullmatch(padrao_crm, crm):
            if existe_crm:
                print("CRM já cadastrado. Por favor, insira um CRM diferente.")
                continue
            return crm
        else:
            print('Formato de CRM inválido. CRM deve ser no padrão 00000/XX')


def input_especialidade():
    """
    Função para entrada da especialidade do médico.
    """
    while True:
        especialidade = input("Especialidade do médico: ").strip().title()
        if not especialidade:
            print(
                "A especialidade do médico é obrigatória. Preencha o campo corretamente.")
            continue
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", especialidade):
            print(
                "A especialidade contém caracteres inválidos. Use apenas letras e espaços.")
            continue
        return especialidade


def input_status():
    """
    Função para entrada do status do médico.
    """
    while True:
        status = input(
            "Status do médico (Ativo/Inativo/Afastado): ").strip().title()
        if status not in ["Ativo", "Inativo", "Afastado"]:
            print("Status inválido. Por favor, insira 'Ativo', 'Inativo' ou 'Afastado'.")
            continue
        return status


def form_cadastro_medico():
    """
    Função para exibir o formulário de cadastro de médico.
    """
    print("=== Cadastro de Médico ===")

    dados_medico = {
        'nome': input_nome(),
        'crm': input_crm(),
        'especialidade': input_especialidade(),
        'status': input_status()
    }

    while True:
        print("\n === Valide os dados inseridos ====")

        for index, (key, value) in enumerate(dados_medico.items(), start=1):
            print(f"{index + 1}. {key.replace('_', ' ').title()}: {value}")

        escolha = input(
            "\n === Os dados estão corretos? [S] para Sim, [N] para Não: ").strip().upper()
        if escolha == "S":
            break
        elif escolha == "N":
            print("1 - Nome")
            print("2 - CRM")
            print("3 - Especialidade")
            print("4 - Status")
            campo = input(
                "\n=== Escolha o campo a ser editado: ===").strip()
            if campo.isdigit() and 1 <= int(campo) <= len(dados_medico):
                campo_nome = list(dados_medico.keys())[int(campo)-1]
                if campo_nome == 'nome':
                    dados_medico['nome'] = input_nome()
                elif campo_nome == 'crm':
                    dados_medico['crm'] = input_crm()
                elif campo_nome == 'especialidade':
                    dados_medico['especialidade'] = input_especialidade()
                elif campo_nome == 'status':
                    dados_medico['status'] = input_status()
            else:
                print("Campo inválido. Por favor selecione um campo válido.")
        else:
            print(
                "Opção inválida. Por favor, escolha S para prosseguir ou N para editar.")
    try:
        inserir_medico(dados_medico)
        print("\nMédico cadastrado com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar médico: {e}")
