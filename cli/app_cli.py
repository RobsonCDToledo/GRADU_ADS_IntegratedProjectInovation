"""
============================================================
Sistema de Gestão Clínica Vida+
Módulo: auth.py
------------------------------------------------------------
Descrição:
    Responsável por criar todos os repositórios do banco de dados SQLITE 
    para armazenar e manusear os dados inputados no sistema.
Autor: Robson Carlos Donizette de Toledo
Data de criação: 24/08/2025
Última atualização: 24/08/2025
Versão: 1.1
============================================================
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import bcrypt

DB_PATH = Path("db/data/clinica_vidaplus.db")  # caminho para o banco

def get_connection():
    """Cria uma conexão com o banco de dados SQLite (garante diretório)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Inicializa o banco de dados, criando as tabelas necessárias."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                role TEXT NOT NULL,
                usuario_ativo INTEGER NOT NULL DEFAULT 1,
                data_criacao TEXT NOT NULL,
                ultimo_login TEXT
            );
        """)
        connection.commit()

def create_user(username: str, password: str, role: str):
    """Cria um novo usuário no banco de dados."""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO usuarios (username, password_hash, role, data_criacao)
            VALUES (?, ?, ?, ?);
        """, (username, password_hash, role, datetime.utcnow().isoformat()))
        connection.commit()

def user_exists(username: str) -> bool:
    """Verifica se um usuário existe no banco de dados."""
    with get_connection() as connection:
        cursor = connection.execute("SELECT 1 FROM usuarios WHERE username = ?;", (username,))
        return cursor.fetchone() is not None

def verify_login(username: str, password: str):
    """Verifica as credenciais de login do usuário."""
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, username, password_hash, role, usuario_ativo
            FROM usuarios
            WHERE username = ?;
        """, (username,))
        row = cursor.fetchone()
        if not row:
            return None
        user_id, uname, pwhash, role, is_active = row
        if not is_active:
            return None
        if bcrypt.checkpw(password.encode('utf-8'), pwhash):
            connection.execute(
                "UPDATE usuarios SET ultimo_login = ? WHERE id = ?;",
                (datetime.utcnow().isoformat(), user_id)
            )
            connection.commit()
            return {"id": user_id, "username": uname, "role": role}
        return None

def set_active(username: str, active: bool):
    """Define se um usuário está ativo ou não."""
    with get_connection() as connection:
        connection.execute(
            "UPDATE usuarios SET usuario_ativo = ? WHERE username = ?;",
            (1 if active else 0, username)
        )
        connection.commit()
