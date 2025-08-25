"""Visualizações de tabelas (pacientes, médicos) no Streamlit."""
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

# Use o MESMO caminho do auth.py
DB_PATH = Path("db/data/clinica_vidaplus.db")

def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND lower(name)=lower(?);",
        (table,)
    )
    return cur.fetchone() is not None

def view_tabela_st(tabela: str) -> pd.DataFrame | None:
    """
    Lê e exibe uma tabela do SQLite no Streamlit.
    - Retorna o DataFrame (ou None se não existir/erro)
    - Mostra mensagens amigáveis quando não há registros ou tabela não existe
    """
    # Garante diretório do DB
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        st.error(f"Não foi possível abrir o banco em '{DB_PATH}': {e}")
        return None

    try:
        if not _table_exists(conn, tabela):
            st.warning(f"A tabela **{tabela}** não existe no banco de dados.")
            # Dica de nomes alternativos
            alt = "pacientes" if tabela.lower() == "pacientes" else "medicos"
            st.caption(f"Dica: verifique se você está criando registros na tabela correta ({tabela}) "
                       f"e se o nome é exatamente esse. Ex.: '{alt}'.")
            return None

        df = pd.read_sql_query(f'SELECT * FROM "{tabela}"', conn)
        if df.empty:
            st.info(f"Nenhum registro encontrado em **{tabela}**.")
            return df

        st.dataframe(df, use_container_width=True, hide_index=True)
        return df

    except sqlite3.Error as e:
        st.error(f"Erro ao acessar a tabela **{tabela}**: {e}")
        return None
    finally:
        conn.close()

# Funções específicas
def view_medicos_st() -> pd.DataFrame | None:
    st.markdown('<h2 style="color:#2563eb; font-family:Arial; margin-top:0;">Médicos Cadastrados</h2>', unsafe_allow_html=True)
    return view_tabela_st('medicos')

def view_pacientes_st() -> pd.DataFrame | None:
    st.markdown('<h2 style="color:#2563eb; font-family:Arial; margin-top:0;">Pacientes Cadastrados</h2>', unsafe_allow_html=True)
    return view_tabela_st('pacientes')
