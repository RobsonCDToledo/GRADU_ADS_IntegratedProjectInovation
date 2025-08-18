import sqlite3
import streamlit as st
import pandas as pd

DB_PATH = 'db/data/clinica_vidaplus.db'

def view_tabela_st(tabela):
    """Retorna um DataFrame com os dados de uma tabela específica."""
    connection = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", connection)
        if df.empty:
            st.warning(f"Tabela '{tabela}' vazia ou sem registros.")
        else:
            st.dataframe(df)  # Exibe tabela interativa no Streamlit
    except sqlite3.Error as e:
        st.error(f"Erro ao acessar a tabela '{tabela}': {e}")
    finally:
        connection.close()

# Funções específicas
def view_medicos_st():
    st.markdown('<h2 style="color:blue; font-family:Arial;">Médicos Cadastrados:</h2>',
                unsafe_allow_html=True)
    view_tabela_st('medicos')

def view_pacientes_st():
    st.markdown('<h2 style="color:blue; font-family:Arial;">Pacientes Cadastrados:</h2>',
                unsafe_allow_html=True)
    view_tabela_st('pacientes')
