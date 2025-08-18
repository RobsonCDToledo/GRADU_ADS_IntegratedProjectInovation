""""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: repositorio_pacientes.py
------------------------------------------------------------
Descrição:
    Responsável por capturar as informações do cadastro de pacientes
    e inserir na tabela pacientes do banco de dados.
Autor: Robson Carlos Donizette de Toledo
Data de criação: 16/08/2025
Última atualização: 17/08/2025
Versão: 1.0
============================================================
"""

import sqlite3
from db.db import get_connection


def inserir_paciente(paciente):
    """
    Insere um novo paciente no banco de dados.
    """
    sql = """
    INSERT INTO pacientes (nome, data_nascimento, genero, telefone, email, cpf)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    connection = get_connection()
    try:
        connection.execute(sql, (
            paciente['nome'],
            paciente['data_nascimento'],
            paciente['genero'],
            paciente['telefone'],
            paciente['email'],
            paciente['cpf'],
        ))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(
            f"Violação de Integridade (Possível CPF já cadastrado), {e}.") from e
    finally:
        connection.close()


def buscar_cpf(cpf):
    """Busca um paciente pelo CPF.
    Args:
        cpf (str): O CPF do paciente a ser buscado.
    """
    connection = get_connection()
    try:
        cursor = connection.execute(
            "SELECT * FROM pacientes WHERE cpf = ?", (cpf,))
        return cursor.fetchone()  # sqlite ou none caso encontrar.
    finally:
        connection.close()


def buscar_id(pid):
    """Busca um paciente pelo ID.
    Args:
        pid (int): O ID do paciente a ser buscado.
    """
    connection = get_connection()
    try:
        cursor = connection.execute(
            "SELECT * FROM pacientes WHERE id = ?", (pid,))
        return cursor.fetchone()  # sqlite ou none caso encontrar.
    finally:
        connection.close()


def listar_pacientes(limit=50, offset=0):
    """Lista os pacientes com paginação.
    Args:
        limit (int): O número máximo de pacientes a serem retornados.
        offset (int): O deslocamento para a paginação.
    """
    connection = get_connection()
    try:
        cursor = connection.execute("""
        SELECT id, nome, data_nascimento, genero, telefone, email, cpf, data_cadastro
        FROM pacientes
        ORDER BY nome
        LIMIT ? OFFSET ?
        """, (limit, offset))
        return cursor.fetchall()  # lista de pacientes ou vazia caso não encontre.
    finally:
        connection.close()
