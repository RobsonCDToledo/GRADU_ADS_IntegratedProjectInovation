import streamlit as st
import sqlite3
from datetime import datetime
from datetime import date
import locale

DB_PATH = "db/data/clinica_vidaplus.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.row_factory = sqlite3.Row
    return connection


# ------------------ Editar Pacientes ------------------
def edit_pacientes_st():
    st.subheader("Editar Pacientes")

    # Inicializa session_state
    if 'dados_paciente' not in st.session_state:
        st.session_state.dados_paciente = {
            'nome': '',
            'genero': 'Selecionar',
            'data_nascimento': None,
            'telefone': '',
            'email': '',
            'cpf': ''
        }

    # Define locale para português
    try:
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")  # Linux / Mac
    except:
        try:
            locale.setlocale(
                locale.LC_TIME, "Portuguese_Brazil.1252")  # Windows
        except:
            pass  # fallback, meses podem aparecer em inglês

    # Conectar e buscar pacientes
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    connection.close()

    if not pacientes:
        st.warning("Nenhum paciente cadastrado.")
        return

    # Seletor de paciente
    paciente_dict = {f"{p['nome']} (ID {p['id']})": p['id'] for p in pacientes}
    selecionado = st.selectbox("Selecione o paciente", [
                               ""] + list(paciente_dict.keys()))

    if selecionado:  # só renderiza inputs se houver seleção
        paciente_id = paciente_dict[selecionado]

        # Buscar dados do paciente selecionado
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
        paciente = cursor.fetchone()
        connection.close()

        # Atualiza session_state
        st.session_state.dados_paciente.update({
            'nome': paciente['nome'],
            'genero': paciente['genero'],
            'data_nascimento': paciente['data_nascimento'],
            'telefone': paciente['telefone'],
            'email': paciente['email'],
            'cpf': paciente['cpf']
        })

        # Inputs para edição
        st.session_state.dados_paciente['nome'] = st.text_input(
            "Nome", st.session_state.dados_paciente['nome'])

        st.session_state.dados_paciente['genero'] = st.selectbox(
            "Gênero",
            ["M", "F", "Outro"],
            index=["M", "F", "Outro"].index(
                st.session_state.dados_paciente['genero'])
            if st.session_state.dados_paciente['genero'] in ["M", "F", "Outro"] else 0
        )

        # Data de nascimento com limites e meses em português
        data_str = st.session_state.dados_paciente['data_nascimento']
        if isinstance(data_str, str):
            try:
                data_dt = datetime.strptime(data_str, "%Y-%m-%d").date()
            except ValueError:
                data_dt = date.today()
        elif isinstance(data_str, date):
            data_dt = data_str
        else:
            data_dt = date.today()

        st.session_state.dados_paciente['data_nascimento'] = st.date_input(
            "Data de Nascimento",
            value=data_dt,
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        st.session_state.dados_paciente['telefone'] = st.text_input(
            "Telefone", st.session_state.dados_paciente['telefone'])
        st.session_state.dados_paciente['email'] = st.text_input(
            "Email", st.session_state.dados_paciente['email'])
        st.session_state.dados_paciente['cpf'] = st.text_input(
            "CPF", st.session_state.dados_paciente['cpf'])

        # Botão salvar
        if st.button("Salvar alterações", key=f"salvar_paciente_{paciente_id}"):
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE pacientes 
                SET nome=?, genero=?, data_nascimento=?, telefone=?, email=?, cpf=?
                WHERE id=?
            """, (
                st.session_state.dados_paciente['nome'],
                st.session_state.dados_paciente['genero'],
                st.session_state.dados_paciente['data_nascimento'],
                st.session_state.dados_paciente['telefone'],
                st.session_state.dados_paciente['email'],
                st.session_state.dados_paciente['cpf'],
                paciente_id
            ))
            connection.commit()
            connection.close()
            st.success(
                f"Paciente {st.session_state.dados_paciente['nome']} atualizado com sucesso!")


# ------------------ Editar Médicos ------------------
def edit_medicos_st():
    st.subheader("Editar Médicos")

    # Inicializa session_state se não existir
    if 'dados_medico' not in st.session_state:
        st.session_state.dados_medico = {
            'nome': '',
            'crm': '',
            'especialidade': '',
            'status': 'Selecionar'
        }

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicos")
    medicos = cursor.fetchall()
    connection.close()

    if not medicos:
        st.warning("Nenhum médico cadastrado.")
        return

    # Selecionar médico
    medico_dict = {
        f"{m['nome']} (ID {m['id_medico']})": m['id_medico'] for m in medicos}
    selecionado = st.selectbox("Selecione o médico", [
                               ""] + list(medico_dict.keys()))

    if selecionado:  # só continua se houver seleção
        medico_id = medico_dict[selecionado]

        # Buscar dados do médico
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM medicos WHERE id_medico = ?", (medico_id,))
        medico = cursor.fetchone()
        connection.close()

        # Atualiza session_state
        st.session_state.dados_medico.update({
            'nome': medico['nome'],
            'crm': medico['crm'],
            'especialidade': medico['especialidade'],
            'status': medico['status']
        })

        # Inputs para edição
        st.session_state.dados_medico['nome'] = st.text_input(
            "Nome", st.session_state.dados_medico['nome'])
        st.session_state.dados_medico['crm'] = st.text_input(
            "CRM", st.session_state.dados_medico['crm'])
        st.session_state.dados_medico['especialidade'] = st.text_input(
            "Especialidade", st.session_state.dados_medico['especialidade']
        )
        st.session_state.dados_medico['status'] = st.selectbox(
            "Status", ["Ativo", "Inativo", "Afastado"],
            index=["Ativo", "Inativo", "Afastado"].index(
                st.session_state.dados_medico['status'])
            if st.session_state.dados_medico['status'] in ["Ativo", "Inativo", "Afastado"] else 0
        )

        # Botão para salvar alterações
        if st.button("Salvar alterações", key=f"salvar_medico_{medico_id}"):
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE medicos
                SET nome=?, crm=?, especialidade=?, status=?
                WHERE id_medico=?
            """, (
                st.session_state.dados_medico['nome'],
                st.session_state.dados_medico['crm'],
                st.session_state.dados_medico['especialidade'],
                st.session_state.dados_medico['status'],
                medico_id
            ))
            connection.commit()
            connection.close()
            st.success(
                f"Médico {st.session_state.dados_medico['nome']} atualizado com sucesso!")
