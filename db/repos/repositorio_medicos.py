""""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: repositório_medicos.py
------------------------------------------------------------
Descrição:
    Responsável por executar a função que captura as informações do cadastro de médicos e insere
    os dados na tabela médicos do banco de dados.

Autor: Robson Carlos Donizette de Toledo
Data de criação: 17/08/2025
Última atualização: 17/08/2025
Versão: 1.0
============================================================
"""

import sqlite3
from db.db import get_connection


def inserir_medico(medico):
    """
    Insere um novo médico no banco de dados.
    """
    sql = """
    INSERT INTO medicos (nome, crm, especialidade, status)
    VALUES (?, ?, ?, ?)
    """
    connection = get_connection()
    try:
        connection.execute(sql, (
            medico['nome'],
            medico['crm'],
            medico['especialidade'],
            medico['status'],
        ))
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(
            f'Violação de Integridade (Possível CRM já cadastrado), {e}') from e
    finally:
        connection.close()


def buscar_crm(crm):
    """
    Busca um médico pelo CRM.
    Args:
        crm (str): O CRM do médico a ser buscado.
    """
    connection = get_connection()
    try:
        cursor = connection.execute(
            "SELECT * FROM medicos WHERE crm = ?", (crm,))
        return cursor.fetchone()
    finally:
        connection.close()


def buscar_id(pid):
    """
    Busca um médico pelo ID.
    Args:
        pid (int): O ID do médico a ser buscado.
    """
    connection = get_connection()
    try:
        cursor = connection.execute(
            "SELECT * FROM medicos WHERE id_medico = ?", (pid,))
        return cursor.fetchone()
    finally:
        connection.close()


def listar_medicos(limit=50, offset=0):
    """
    Lista os médicos com paginação.
    Args:
        limit (int): O número máximo de médicos a serem retornados.
        offset (int): O deslocamento para a paginação.
    """
    connection = get_connection()
    try:
        cursor = connection.execute("""
        SELECT id_medico, nome, crm, especialidade, status, data_cadastro
        FROM medicos
        ORDER BY nome
        LIMIT ? OFFSET ?
        """, (limit, offset))
        return cursor.fetchall()
    finally:
        connection.close()
