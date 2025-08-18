""""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: cadastro_pacientes.py
------------------------------------------------------------
Descrição:
    Responsável por exibir um formulário para cadastro de pacientes.

Autor: Robson Carlos Donizette de Toledo
Data de criação: 16/08/2025
Última atualização: 16/08/2025
Versão: 1.0
============================================================
"""

import re
import sqlite3
from datetime import datetime
from db.repos.repositorio_pacientes import inserir_paciente, buscar_cpf


def input_nome():
    """
    Função para entrada do nome do paciente.
    """
    while True:
        nome = input("Nome do Paciente: ").strip().title()
        if not nome:
            print("O nome é obrigatório. Por favor, insira um nome válido.")
            continue
        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
            print("O nome contém caracteres inválidos. Use apenas letras e espaços.")
            continue
        return nome


def input_data_nascimento():
    """
    Função para entrada da data de nascimento do paciente.
    """
    while True:
        data_nascimento = input(
            "Data de nascimento no formato (Dia/Mês/Ano): ").strip()
        padroes = [
            (r"^\d{2}/\d{2}/\d{4}$", "%d/%m/%Y"),
            (r"^\d{2}-\d{2}-\d{4}$", "%d-%m-%Y"),
            (r"^\d{2}\.\d{2}\.\d{4}$", "%d.%m.%Y"),
            (r"^\d{8}$", "%d%m%Y"),
        ]
        for regex, formato in padroes:
            if re.match(regex, data_nascimento):
                try:
                    data = datetime.strptime(data_nascimento, formato)
                    return data.strftime("%Y-%m-%d")
                except ValueError:
                    print("Data inválida no calendário.")
        print("Formato inválido, tente algo como 25/01/1995.")


def input_genero():
    """
    Função para entrada do gênero do paciente.
    """
    while True:
        genero = input("Gênero (M | F | Outro): ").strip().capitalize()
        if genero in ["M", "F", "Outro"]:
            return genero
        print("Gênero inválido. Por favor, insira M, F ou Outro.")


def input_telefone():
    """
    Função para entrada do telefone do paciente.
    """
    while True:
        telefone = input("Celular (DDD + numero): ")
        if re.fullmatch(r"\d{11}", telefone):
            return telefone
        print("Telefone inválido. Por favor, insira um número de celular válido.")


def input_email():
    """
    Função para entrada do e-mail do paciente.
    """
    while True:
        email = input("E-mail de contato: ").strip()
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return email
        print("E-mail inválido. Por favor, insira um e-mail válido.")


def input_cpf():
    """
    Função para entrada do CPF do paciente.
    """
    while True:
        cpf = input("Insira o CPF (Apenas numero): ").strip()
        if cpf.isdigit() and len(cpf) >= 11:
            existente = buscar_cpf(cpf)
            if existente:
                print("CPF já cadastrado.")
                continue
            return cpf
        print("CPF inválido. Digite apenas os números, com 11 digitos")


def form_cadastro_paciente():
    """
    Função para o formulário de cadastro de pacientes.
    """
    print("\n=== Cadastro de novos pacientes ===")
    dados_paciente = {
        'nome': input_nome(),
        'data_nascimento': input_data_nascimento(),
        'genero': input_genero(),
        'telefone': input_telefone(),
        'email': input_email(),
        'cpf': input_cpf(),
    }
    while True:
        print("\n === Valide os dados inseridos ====")
        for index, (key, value) in enumerate(dados_paciente.items(), start=1):
            print(f"{index}. {key.replace('_', ' ').title()}: {value}")
        escolha = input(
            "\n === Os dados estão corretos? [S] para Sim, [N] para Não: ").strip().upper()
        if escolha == "S":
            break
        elif escolha == "N":
            print("1 - Nome")
            print("2 - Data de Nascimento")
            print("3 - Gênero")
            print("4 - Telefone")
            print("5 - E-mail")
            print("6 - CPF")
            campo = input(
                "\n=== Escolha o campo a ser editado: ===").strip()
            if campo.isdigit() and 1 <= int(campo) <= len(dados_paciente):
                campo_nome = list(dados_paciente.keys())[int(campo)-1]
                if campo_nome == 'nome':
                    dados_paciente['nome'] = input_nome()
                elif campo_nome == 'data_nascimento':
                    dados_paciente['data_nascimento'] = input_data_nascimento()
                elif campo_nome == 'genero':
                    dados_paciente['genero'] = input_genero()
                elif campo_nome == 'telefone':
                    dados_paciente['telefone'] = input_telefone()
                elif campo_nome == 'email':
                    dados_paciente['email'] = input_email()
                elif campo_nome == 'cpf':
                    dados_paciente['cpf'] = input_cpf()
            else:
                print("Campo inválido. Por favor, escolha um número de campo válido.")
        else:
            print(
                "Opção inválida. Por favor, escolha S para prosseguir ou N para editar.")
    try:
        inserir_paciente(dados_paciente)
        print("\nDados do paciente cadastrados com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar paciente: {e}")
