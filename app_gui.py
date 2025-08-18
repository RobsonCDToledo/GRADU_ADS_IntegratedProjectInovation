import streamlit as st
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from gui.cad.pag_cad_pacientes import form_cadastro_paciente
from gui.cad.pag_cad_medicos import form_cadastro_medico
from gui.view.view_tables_st import view_pacientes_st, view_medicos_st
from gui.configs.edit import edit_pacientes_st, edit_medicos_st

# ==============================
# Configuração da página
# ==============================
st.set_page_config(page_title="Sistema de Gestão Clínica Vida+", layout="wide")

# Atualiza automaticamente a cada 1 segundo
st_autorefresh(interval=1000, key="data_hora")

# Fuso horário GMT-3
brasil = pytz.timezone("America/Sao_Paulo")
hora_atual = datetime.now(brasil).strftime('%d/%m/%Y %H:%M:%S')

# ==============================
# CSS customizado
# ==============================
st.markdown(
    f"""
    <style>
    /* Faz a sidebar ocupar toda a altura com flex */
    [data-testid="stSidebar"] > div:first-child {{
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    /* Rodapé fixado no fim da sidebar */
    .sidebar-footer {{
        margin-top: auto;
        padding-top: 20px;
        font-size: 13px;
        color: grey;
    }}

    /* Fundo da página com imagem */
    .stApp {{
        background: url("https://images.unsplash.com/photo-1580281657521-3a5a3d5d7b7f") no-repeat center center fixed;
        background-size: cover;
    }}

    /* Cor da sidebar (diferente do fundo) */
    [data-testid="stSidebar"] {{
        background-color: #f5f5f5;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# Conteúdo principal
# ==============================
st.title("Bem vindo, ao seu Sistema de Gestão")

# Sidebar com menu principal
with st.sidebar:
    logo = st.image("C:/ProjetosGRADU/ClinicalScheduleManager/gui/themes/image/logo_clinica.png")

    menu_principal = st.selectbox(
        "Menu Principal",
        ["Início", "Cadastros", "Agendar Consultas",
         "Relatórios", "Configurações", "Ajuda", "Sair"]
    )

    # Dropdown para Cadastros
    cadastro_menu = None
    if menu_principal == "Cadastros":
        cadastro_menu = st.selectbox(
            "Tipo de Cadastro",
            ["Pacientes", "Médicos"]
        )

    # Dropdown para Relatórios
    relatorio_menu = None
    if menu_principal == "Relatórios":
        relatorio_menu = st.selectbox(
            "Tipo de Relatório",
            ["Pacientes Cadastrados", "Médicos Cadastrados"]
        )

    # Dropdown para Configurações
    configuracoes_menu = None
    if menu_principal == "Configurações":
        configuracoes_menu = st.selectbox(
            "Tipo de Configuração",
            ["Gerenciar Usuários", "Editar Cadastros"]
        )

    # Rodapé fixado com data/hora dinâmica
    st.markdown(
        f'<div class="sidebar-footer">Data e Hora Atual (GMT-3):<br><b>{hora_atual}</b></div>',
        unsafe_allow_html=True
    )

# ==============================
# Lógica de exibição na página principal
# ==============================
if menu_principal == "Início":
    st.write("Selecione uma opção no menu lateral.")

elif menu_principal == "Cadastros":
    st.subheader("Cadastros")
    if cadastro_menu == "Pacientes":
        form_cadastro_paciente()
    elif cadastro_menu == "Médicos":
        form_cadastro_medico()

elif menu_principal == "Agendar Consultas":
    st.subheader("Agendar Consultas")
    st.write("Funcionalidade em desenvolvimento.")

elif menu_principal == "Relatórios":
    st.subheader("Relatórios")
    if relatorio_menu == "Pacientes Cadastrados":
        view_pacientes_st()
    elif relatorio_menu == "Médicos Cadastrados":
        view_medicos_st()

elif menu_principal == "Configurações":
    st.subheader("Configurações")
    if configuracoes_menu == "Gerenciar Usuários":
        st.write("Funcionalidade em desenvolvimento.")
    elif configuracoes_menu == "Editar Cadastros":
        editar_cadastro_menu = st.selectbox(
            "Selecione o cadastro que deseja editar:",
            ["Pacientes", "Médicos"]
        )
        if editar_cadastro_menu == "Pacientes":
            edit_pacientes_st()
        elif editar_cadastro_menu == "Médicos":
            edit_medicos_st()

elif menu_principal == "Ajuda":
    st.subheader("Ajuda")
    st.write("Funcionalidade em desenvolvimento.")

elif menu_principal == "Sair":
    st.warning("Sair")
    st.stop()
