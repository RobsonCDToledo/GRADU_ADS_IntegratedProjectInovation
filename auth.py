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
from sqlite3 import IntegrityError
from pathlib import Path
from datetime import datetime
import bcrypt
from typing import Optional

DB_PATH = Path("db/data/clinica_vidaplus.db")  # caminho para o banco


def get_connection() -> sqlite3.Connection:
    """Cria uma conexão com o banco de dados SQLite (e garante o diretório)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Inicializa o banco de dados, criando as tabelas necessárias."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                role TEXT NOT NULL,
                user_active INTEGER NOT NULL DEFAULT 1,
                create_in TEXT NOT NULL,
                last_login TEXT
            );
        """)
        connection.commit()


def create_user(username: str, password: str, role: str) -> None:
    """Cria um novo usuário no banco de dados."""
    if not username:
        raise ValueError("Informe um username.")
    if not password or len(password) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        with get_connection() as connection:
            connection.execute("""
                INSERT INTO usuarios (username, password_hash, role, create_in)
                VALUES (?, ?, ?, ?);
            """, (username.strip(), password_hash, role, datetime.utcnow().isoformat()))
            connection.commit()
    except IntegrityError:
        raise ValueError("Usuário já existe.")


def user_exists(username: str) -> bool:
    """Verifica se um usuário existe no banco de dados."""
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT 1 FROM usuarios WHERE username = ?;",
            (username,)
        )
        return cursor.fetchone() is not None


def verify_login(username: str, password: str):
    """Verifica as credenciais de login do usuário."""
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, username, password_hash, role, user_active
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
                "UPDATE usuarios SET last_login = ? WHERE id = ?;",
                (datetime.utcnow().isoformat(), user_id)
            )
            connection.commit()
            return {"id": user_id, "username": uname, "role": role}
        return None


def set_active(username: str, active: bool) -> None:
    """Define se um usuário está ativo ou não."""
    with get_connection() as connection:
        connection.execute(
            "UPDATE usuarios SET user_active = ? WHERE username = ?;",
            (1 if active else 0, username)
        )
        connection.commit()


def update_password(username: str, new_password: str) -> None:
    """Atualiza a senha (hash) do usuário."""
    if not new_password or len(new_password) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

    password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    with get_connection() as connection:
        connection.execute(
            "UPDATE usuarios SET password_hash = ? WHERE username = ?;",
            (password_hash, username)
        )
        connection.commit()


def list_users(search: Optional[str] = None):
    """
    Lista usuários; se search for informado, filtra por username LIKE %search%.
    Retorna com chaves compatíveis com o system.py (usuario_ativo, data_criacao, ultimo_login)
    """
    with get_connection() as connection:
        if search:
            cur = connection.execute(
                "SELECT id, username, role, user_active, create_in, last_login "
                "FROM usuarios WHERE username LIKE ? ORDER BY username;",
                (f"%{search}%",)
            )
        else:
            cur = connection.execute(
                "SELECT id, username, role, user_active, create_in, last_login "
                "FROM usuarios ORDER BY username;"
            )
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "username": r[1],
                "role": r[2],
                "usuario_ativo": bool(r[3]),  # chave adaptada para o system.py
                "data_criacao": r[4],
                "ultimo_login": r[5],
            }
            for r in rows
        ]


def set_role(username: str, new_role: str) -> None:
    """Altera o papel (role) do usuário."""
    with get_connection() as connection:
        connection.execute(
            "UPDATE usuarios SET role = ? WHERE username = ?;",
            (new_role, username)
        )
        connection.commit()


def delete_user(username: str) -> None:
    """Exclui o usuário definitivamente."""
    with get_connection() as connection:
        connection.execute("DELETE FROM usuarios WHERE username = ?;", (username,))
        connection.commit()
