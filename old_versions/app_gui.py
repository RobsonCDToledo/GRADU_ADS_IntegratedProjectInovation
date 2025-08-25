import streamlit as st
import pytz
from datetime import datetime
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

from gui.cad.pag_cad_pacientes import form_cadastro_paciente
from gui.cad.pag_cad_medicos import form_cadastro_medico
from gui.view.view_tables_st import view_pacientes_st, view_medicos_st
from gui.configs.edit import edit_pacientes_st, edit_medicos_st
from dict.dicionarios import (
    dict_opcoes_de_configuracoes,
    dict_tipos_de_cadastros,
    dict_relatorios,
    dict_consultas,
    dict_funcionalidades,
)

# ==============================
# Config
# ==============================
st.set_page_config(page_title="Sistema de Gestão Clínica Vida+", layout="wide")

# Atualização do relógio (evite 1s; 30–60s é mais leve)
st_autorefresh(interval=60000, key="data_hora_minuto")

brasil = pytz.timezone("America/Sao_Paulo")
hora_atual = datetime.now(brasil).strftime('%d/%m/%Y %H:%M')

# Caminho da logo (use relativo ao projeto)
LOGO_PATH = Path("gui/themes/image/logo_clinica.png")

# ==============================
# CSS
# ==============================
st.markdown(
    """
    <style>
    /* Sidebar em flex para empurrar o footer pro fim */
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .sidebar-spacer { flex: 1 1 auto; }

    /* Fundo da app (opcional) */
    .stApp {
        background: url("https://images.unsplash.com/photo-1580281657521-3a5a3d5d7b7f") no-repeat center center fixed;
        background-size: cover;
    }

    /* Cor da sidebar */
    [data-testid="stSidebar"] {
        background-color: #f5f5f5;
    }

    /* Separador colorido (gradiente) */
    .sb-divider {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, #06b6d4 0%, #22c55e 50%, #f59e0b 100%);
        margin: 12px 0 8px 0;
        border-radius: 2px;
    }

    /* Footer fixo da sidebar */
    .sidebar-footer {
        font-size: 13px;
        color: #6b7280;
        padding: 8px 0 4px 0;
        border-top: 1px solid #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# Título
# ==============================
st.title("Bem-vindo ao Sistema de Gestão Clínica Vida+")

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH))
    else:
        st.image("https://placehold.co/300x120?text=Vida%2B+Clinica")

    # Separador colorido
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # Menu principal (use key para manter estado)
    menu_principal = st.selectbox(
        "Menu Principal",
        dict_funcionalidades,  # certifique-se de que isso é uma lista de strings
        key="menu_principal"
    )

    # Submenus condicionais
    if menu_principal == "Cadastros":
        cadastro_menu = st.selectbox(
            "Tipo de Cadastro",
            dict_tipos_de_cadastros,
            key="cadastro_menu"
        )
    else:
        cadastro_menu = None

    if menu_principal == "Relatórios":
        relatorio_menu = st.selectbox(
            "Tipo de Relatório",
            dict_relatorios,
            key="relatorio_menu"
        )
    else:
        relatorio_menu = None

    if menu_principal == "Consultas":
        consultas_menu = st.selectbox(
            "Tipo de Consulta",
            dict_consultas,
            key="consultas_menu"
        )
    else:
        consultas_menu = None

    # Configurações (inclui "Excluir Cadastros")
    if menu_principal == "Configurações":
        # Garanta que sua lista/dict tenha essa nova opção
        # Exemplo de lista: ["Gerenciar Usuários", "Editar Cadastros", "Excluir Cadastros"]
        configuracoes_menu = st.selectbox(
            "Tipo de Configuração",
            dict_opcoes_de_configuracoes,
            key="configuracoes_menu"
        )

        # Submenus específicos de Configurações
        if configuracoes_menu == "Editar Cadastros":
            editar_cadastro_menu = st.selectbox(
                "Selecione o cadastro que deseja editar:",
                ["Pacientes", "Médicos"],
                key="editar_cadastro_menu"
            )
        elif configuracoes_menu == "Excluir Cadastros":
            excluir_cadastro_menu = st.selectbox(
                "Selecione o cadastro que deseja excluir:",
                ["Pacientes", "Médicos"],
                key="excluir_cadastro_menu"
            )
        else:
            editar_cadastro_menu = None
            excluir_cadastro_menu = None
    else:
        configuracoes_menu = None
        editar_cadastro_menu = None
        excluir_cadastro_menu = None

    # Espaçador para empurrar o footer
    st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)

    # Footer
    st.markdown(
        f'<div class="sidebar-footer">Data e hora: <b>{hora_atual}</b></div>',
        unsafe_allow_html=True
    )

# ==============================
# Router da área principal
# ==============================
if menu_principal == "Início":
    st.write("Selecione uma opção no menu lateral.")

elif menu_principal == "Cadastros":
    st.subheader("Cadastros")
    if cadastro_menu == "Pacientes":
        form_cadastro_paciente()
    elif cadastro_menu == "Médicos":
        form_cadastro_medico()

elif menu_principal == "Consultas":
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
        st.info("Funcionalidade em desenvolvimento.")
    elif configuracoes_menu == "Editar Cadastros":
        if editar_cadastro_menu == "Pacientes":
            edit_pacientes_st()
        elif editar_cadastro_menu == "Médicos":
            edit_medicos_st()
    elif configuracoes_menu == "Excluir Cadastros":
        # Exemplo de placeholder com confirmação
        if excluir_cadastro_menu == "Pacientes":
            st.warning("Atenção: exclusão de pacientes é irreversível.")
            alvo = st.text_input("Informe o ID/CPF do paciente a excluir:")
            if st.button("Excluir Paciente"):
                st.error("Implementar ação de exclusão aqui (backend).")
        elif excluir_cadastro_menu == "Médicos":
            st.warning("Atenção: exclusão de médicos é irreversível.")
            alvo = st.text_input("Informe o CRM do médico a excluir:")
            if st.button("Excluir Médico"):
                st.error("Implementar ação de exclusão aqui (backend).")

elif menu_principal == "Ajuda":
    st.subheader("Ajuda")
    st.write("Funcionalidade em desenvolvimento.")

elif menu_principal == "Sair":
    st.warning("Saindo…")
    st.stop()
