""""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: db.py
------------------------------------------------------------
Descrição:
    Responsável por criar todos os repositórios do banco de dados SQLITE 
    para armazenar e manusear os dados inputados no sistema.
Autor: Robson Carlos Donizette de Toledo
Data de criação: 16/08/2025
Última atualização: 16/08/2025
Versão: 1.0
============================================================
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("db/data/clinica_vidaplus.db")

""" Criando uma conexão direta e pronta para uso com o SQLITE sempre que executar o arquivo"""


def get_connection():
    """    Cria uma conexão com o banco de dados SQLite."""
    connection = sqlite3.connect(DB_PATH)  # Abre ou cria caso não exista.
    # Habilita o enforcement das chaves estrangeiras.
    connection.execute("PRAGMA foreign_keys = ON;")
    # ajusta o fabric de linhas para facilitar consultas Select
    connection.row_factory = sqlite3.Row
    return connection


def migrate():
    """ Cria as tabelas e índices no banco de dados. """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento date,
        genero TEXT CHECK (genero IN ('M', 'F', 'Outro')) NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_pacientes_nome ON pacientes(nome);
    CREATE INDEX IF NOT EXISTS idx_pacientes_cpf ON pacientes(cpf);
    
    CREATE TABLE IF NOT EXISTS medicos (
        id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        crm TEXT NOT NULL UNIQUE,
        especialidade TEXT NOT NULL,
        status TEXT CHECK (status IN ('Ativo', 'Inativo', 'Afastado')) NOT NULL,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_medicos_nome ON medicos(nome);
    CREATE INDEX IF NOT EXISTS idx_medicos_crm ON medicos(crm);   
    
    """)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    migrate()
