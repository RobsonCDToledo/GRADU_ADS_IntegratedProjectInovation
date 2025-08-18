"""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: view_tables.py
------------------------------------------------------------
Descrição:
    Responsável por exibir os dados das tabelas do banco de dados.
Autor: Robson Carlos Donizette de Toledo
Data de criação: 16/08/2025
Última atualização: 16/08/2025
Versão: 1.0
============================================================
"""

import sqlite3
from tabulate import tabulate

DB_PATH = 'db/data/clinica_vidaplus.db'

# Função que retorna todos os registros de uma tabela consultada do sqlite


def view_tabela(tabela):
    """Exibe os dados de uma tabela específica.
    Args:
        tabela (str): O nome da tabela a ser exibida.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(f'SELECT * FROM {tabela}')
        dados = cursor.fetchall()
        if dados:
            colunas = [descricao[0] for descricao in cursor.description]
            print(tabulate(dados, headers=colunas, tablefmt="grid"))
        else:
            print(f"Tabela '{tabela}' vazia ou sem registros.")
    except sqlite3.Error as e:
        print(f"Erro ao acessar a tabela '{tabela}': {e}")
    finally:
        connection.close()

# Funções específicas


def view_medicos():
    """Exibe os dados da tabela de médicos."""
    view_tabela('medicos')


def view_pacientes():
    """Exibe os dados da tabela de pacientes."""
    view_tabela('pacientes')


if __name__ == "__main__":
    print("=== MÉDICOS ===")
    view_medicos()
    print("\n=== PACIENTES ===")
    view_pacientes()
