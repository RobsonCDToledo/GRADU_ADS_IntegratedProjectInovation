import streamlit as st
import pytz
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# ======== AUTH ========
from auth import (
    list_users, create_user, set_role, set_active, update_password, delete_user
)

# ======== IMPORTS DO SEU APP ========
from gui.cad.pag_cad_pacientes import form_cadastro_paciente
from gui.cad.pag_cad_medicos import form_cadastro_medico
from gui.view.view_tables_st import view_pacientes_st, view_medicos_st
from gui.configs.edit import edit_pacientes_st, edit_medicos_st
from dict.dicionarios import (
    dict_opcoes_de_configuracoes,  # ex.: ["Gerenciar Usuários", "Editar Cadastros", "Excluir Cadastros"]
    dict_tipos_de_cadastros,       # ex.: ["Pacientes","Médicos"]
    dict_relatorios,               # ex.: ["Pacientes Cadastrados","Médicos Cadastrados"]
    dict_consultas,                # ex.: ["Agendar Consulta","Consultar Agenda"]
    dict_funcionalidades           # ex.: ["Início","Cadastros","Consultas","Relatórios","Configurações","Ajuda","Sair"]
)

# ====== Guarda de rota (proteção) ======
if "auth" not in st.session_state or not st.session_state.auth.get("authenticated"):
    st.warning("Faça login para acessar o sistema.")
    st.switch_page("Home.py")

# (opcional) Expiração de sessão
SESSION_TTL_MIN = 120
lt = st.session_state.auth.get("login_time")
if lt is None or (datetime.utcnow() - lt) > timedelta(minutes=SESSION_TTL_MIN):
    st.warning("Sessão expirada. Faça login novamente.")
    st.session_state.auth = {"authenticated": False, "username": None, "role": None, "login_time": None}
    st.switch_page("Home.py")

# ====== Usuário logado ======
username = st.session_state.auth["username"]
role     = st.session_state.auth["role"]

# ====== Config geral ======
st.set_page_config(page_title="Vida+ | Sistema", layout="wide")

# Remove SOMENTE os links do nav de páginas (home/system) da sidebar
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] a, 
    [data-testid="stSidebarNav"] ul,
    [data-testid="stSidebarNav"] hr { display: none !important; }
    nav[aria-label="Pages"] a, 
    nav[aria-label="Pages"] ul { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ====== HEADER FIXO NO TOPO (sem botão) ======
st.markdown("""
<style>
.app-header {
    position: sticky; top: 0; z-index: 1000;
    background: #ffffff;
    padding: 8px 16px;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-header-title { font-weight: 600; font-size: 18px; color: #111827; margin: 0; }
.app-header-right { display: flex; align-items: center; gap: 12px; }
.badge-role { font-size: 12px; padding: 2px 8px; border-radius: 9999px; background: #f3f4f6; color: #374151; }
.user-name { font-weight: 600; color: #111827; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="app-header">
    <div class="app-header-title">Sistema de Gestão Clínica Vida+</div>
    <div class="app-header-right">
        <span class="user-name">👤 {username}</span>
        <span class="badge-role">{role}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ====== Atualiza relógio 1x/min (leve) ======
st_autorefresh(interval=60000, key="data_hora_minuto")
brasil = pytz.timezone("America/Sao_Paulo")
hora_atual = datetime.now(brasil).strftime('%d/%m/%Y %H:%M')

LOGO_PATH = Path("gui/themes/image/logo_clinica.png")

# ====== Permissões (RBAC) ======
ROLE_PERMISSIONS = {
    "admin":    {"Início","Cadastros","Consultas","Relatórios","Configurações","Ajuda","Sair"},
    "recepcao": {"Início","Cadastros","Consultas","Relatórios","Ajuda","Sair"},
    "medico":   {"Início","Consultas","Relatórios","Ajuda","Sair"},
    "gestor":   {"Início","Relatórios","Configurações","Ajuda","Sair"},
}
FUNCIONALIDADES = list(dict_funcionalidades)
allowed = [f for f in FUNCIONALIDADES if f in ROLE_PERMISSIONS.get(role, set())]

# ====== CSS do app ======
st.markdown(
    """
    <style>
    [data-testid="stSidebar"]  { display: flex; flex-direction: column; height: 100%; }
    .sidebar-spacer { flex: 1 1 auto; }
    .stApp { background: url("https://images.unsplash.com/photo-1580281657521-3a5a3d5d7b7f") no-repeat center center fixed; background-size: cover; }
    [data-testid="stSidebar"] { background-color: #f5f5f5; }
    .sb-divider { border: 0; height: 2px; background: linear-gradient(90deg, #06b6d4 0%, #22c55e 50%, #f59e0b 100%); margin: 12px 0 8px 0; border-radius: 2px; }
    .sidebar-footer { font-size: 13px; color: #6b7280; padding: 8px 0 4px 0; border-top: 1px solid #e5e7eb; }
    </style>
    """,
    unsafe_allow_html=True
)

# ====== Sidebar ======
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH))
    else:
        st.image("https://placehold.co/300x120?text=Vida%2B+Clinica")

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    menu_principal = st.selectbox("Menu Principal", allowed, key="menu_principal")

    # Submenus condicionais
    cadastro_menu = None
    if menu_principal == "Cadastros":
        if role not in {"admin","recepcao"}:
            st.warning("Sem permissão para Cadastros.")
        else:
            cadastro_menu = st.selectbox("Tipo de Cadastro", dict_tipos_de_cadastros, key="cadastro_menu")

    relatorio_menu = None
    if menu_principal == "Relatórios":
        if role not in {"admin","gestor","recepcao","medico"}:
            st.warning("Sem permissão para Relatórios.")
        else:
            relatorio_menu = st.selectbox("Tipo de Relatório", dict_relatorios, key="relatorio_menu")

    configuracoes_menu = None
    gerenciar_users_acao = None
    if menu_principal == "Configurações":
        if role not in {"admin","gestor"}:
            st.warning("Você não tem permissão para Configurações.")
        else:
            # adiciona "Gerenciar Usuários" ao seu dicionário/lista de opções
            opcoes_cfg = list(dict_opcoes_de_configuracoes)
            if "Gerenciar Usuários" not in opcoes_cfg:
                opcoes_cfg.append("Gerenciar Usuários")

            configuracoes_menu = st.selectbox("Tipo de Configuração", opcoes_cfg, key="configuracoes_menu")

            # Submenu de Gerenciar Usuários (apenas admin; remova o 'and' se quiser permitir gestor)
            if configuracoes_menu == "Gerenciar Usuários" and role in {"admin"}:
                gerenciar_users_acao = st.radio(
                    "Gerenciar Usuários",
                    ["Cadastrar", "Editar", "Excluir"],
                    horizontal=True,
                    key="gerenciar_users_acao"
                )

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

    consultas_menu = None
    if menu_principal == "Consultas":
        if role not in {"admin","recepcao","medico"}:
            st.warning("Sem permissão para Consultas.")
        else:
            consultas_menu = st.selectbox("Tipo de Consulta", dict_consultas, key="consultas_menu")

    st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-footer">Data e hora: <b>{hora_atual}</b></div>', unsafe_allow_html=True)

st.divider() 
# ====== Router (conteúdo principal) ======
if menu_principal == "Início":
    st.markdown("""
    <style>
      /* grade 2x2 ocupando toda a largura do conteúdo */
      .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;  /* duas colunas iguais */
        gap: 10px;                        /* 10px entre linhas e colunas */
        width: 100%;
      }
      .card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        display: flex;
        flex-direction: column;
        min-height: 150px;               /* deixa todos com altura mínima igual */
      }
      .card h3 {
        margin: 0 0 8px 0;
        font-size: 16px;
        font-weight: 700;
        color: #111827;
      }
      .card .value {
        font-size: 24px;
        font-weight: 800;
        color: #2563eb;
        margin-bottom: 6px;
      }
      .card p, .card li { color: #374151; margin: 0; }
      .card ul { margin: 6px 0 0 18px; padding: 0; }
    </style>

    <div class="dashboard-grid">

      <!-- Bloco 1 -->
      <div class="card">
        <h3>🗒️ Fila de Espera</h3>
        <div class="value">12 pessoas</div>
        <ul>
          <li>Sequência de senhas: A045 → A046 → A047</li>
          <li>3 senhas pendentes há mais de 10 min</li>
        </ul>
      </div>

      <!-- Bloco 2 -->
      <div class="card">
        <h3>📅 Agendados Não Apresentados</h3>
        <div class="value">5 clientes</div>
        <p>Últimos casos: João S., Maria P., Carlos M...</p>
      </div>

      <!-- Bloco 3 -->
      <div class="card">
        <h3>⏱️ Tempo Médio de Atendimento</h3>
        <div class="value">18 min</div>
        <p>Média baseada nas últimas 20 consultas</p>
      </div>

      <!-- Bloco 4 -->
      <div class="card">
        <h3>⭐ Índice de Qualidade</h3>
        <div class="value">92%</div>
        <p>Avaliação positiva dos últimos 30 dias</p>
      </div>

    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown(        
        """
        <!-- Bloco 4 -->
        <div class="card">
           Possiveis informações sobre médicos ou pacientes urgentes 
        </div>""", unsafe_allow_html=True)

elif menu_principal == "Cadastros":
    if role not in {"admin","recepcao"}:
        st.error("Sem permissão para Cadastros.")
    else:
        st.subheader("Cadastros")
        if cadastro_menu == "Pacientes":
            form_cadastro_paciente()
        elif cadastro_menu == "Médicos":
            form_cadastro_medico()

elif menu_principal == "Consultas":
    if role not in {"admin","recepcao","medico"}:
        st.error("Sem permissão para Consultas.")
    else:
        st.subheader("Agendar Consultas")
        st.write("Funcionalidade em desenvolvimento.")

elif menu_principal == "Relatórios":
    if role not in {"admin","gestor","recepcao","medico"}:
        st.error("Sem permissão para Relatórios.")
    else:
        st.subheader("Relatórios")
        if relatorio_menu == "Relatório de Pacientes":
            view_pacientes_st()
        elif relatorio_menu == "Relatório de Médicos":
            view_medicos_st()
        else:
            st.info("Selecione um relatório na barra lateral.")

elif menu_principal == "Configurações":
    if role not in {"admin","gestor"}:
        st.error("Sem permissão para Configurações.")
    else:
        st.subheader("Configurações")

        # ======= GERENCIAR USUÁRIOS (admin) =======
        if configuracoes_menu == "Gerenciar Usuários" and role in {"admin"}:
            acao = gerenciar_users_acao

            # ---------- CADASTRAR ----------
            if acao == "Cadastrar":
                st.markdown("### ➕ Cadastrar novo usuário")
                col1, col2 = st.columns([1,1])
                with col1:
                    novo_user = st.text_input("Username", key="adm_new_username")
                    novo_role = st.selectbox("Perfil", ["admin","gestor","recepcao","medico"], key="adm_new_role")
                with col2:
                    nova_pwd  = st.text_input("Senha", type="password", key="adm_new_pwd")
                    nova_pwd2 = st.text_input("Confirmar senha", type="password", key="adm_new_pwd2")

                if st.button("Criar usuário", type="primary"):
                    try:
                        if not novo_user:
                            st.error("Informe o username.")
                        elif not nova_pwd or nova_pwd != nova_pwd2:
                            st.error("As senhas não conferem.")
                        else:
                            create_user(novo_user.strip(), nova_pwd, novo_role)
                            st.success(f"Usuário '{novo_user}' criado com sucesso.")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao criar usuário: {e}")

            # ---------- EDITAR ----------
            elif acao == "Editar":
                st.markdown("### ✏️ Editar usuário")
                usuarios = list_users()
                nomes = [u["username"] for u in usuarios]
                if not nomes:
                    st.info("Nenhum usuário cadastrado.")
                else:
                    alvo = st.selectbox("Selecione o usuário", nomes, key="adm_edit_target")
                    alvo_info = next(u for u in usuarios if u["username"] == alvo)

                    col1, col2, col3 = st.columns([1,1,1])
                    with col1:
                        novo_role = st.selectbox(
                            "Perfil (role)",
                            ["admin","gestor","recepcao","medico"],
                            index=["admin","gestor","recepcao","medico"].index(alvo_info["role"]),
                            key="adm_edit_role"
                        )
                    with col2:
                        ativo = st.checkbox("Ativo", value=alvo_info["usuario_ativo"], key="adm_edit_active")
                    with col3:
                        st.caption(" ")

                    if st.button("Salvar alterações", key="adm_edit_save", type="primary"):
                        try:
                            set_role(alvo, novo_role)
                            set_active(alvo, ativo)
                            st.success("Alterações salvas.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao salvar: {e}")

                    st.divider()
                    st.markdown("**Alterar senha**")
                    np1 = st.text_input("Nova senha", type="password", key="adm_edit_np1")
                    np2 = st.text_input("Confirmar nova senha", type="password", key="adm_edit_np2")
                    if st.button("Atualizar senha", key="adm_edit_pwd"):
                        try:
                            if not np1 or np1 != np2:
                                st.error("As senhas não conferem.")
                            else:
                                update_password(alvo, np1)
                                st.success("Senha atualizada.")
                        except Exception as e:
                            st.error(f"Erro: {e}")

                st.divider()
                st.markdown("### 👥 Usuários cadastrados")
                df = pd.DataFrame(list_users())
                if not df.empty:
                    df = df.rename(columns={
                        "username":"Usuário","role":"Perfil",
                        "usuario_ativo":"Ativo","data_criacao":"Criado em","ultimo_login":"Último login"
                    })
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhum usuário encontrado.")

            # ---------- EXCLUIR ----------
            elif acao == "Excluir":
                st.markdown("### 🗑️ Excluir usuários")
                st.warning("A exclusão é permanente. Prefira desativar, quando possível.")
                users = list_users()
                if not users:
                    st.info("Nenhum usuário cadastrado.")
                else:
                    candidatos = [u["username"] for u in users if u["username"] not in {username, "admin"}]
                    marcar = st.multiselect("Selecione usuários para excluir", candidatos)
                    if st.button("Confirmar exclusão", type="primary"):
                        try:
                            if not marcar:
                                st.error("Nenhum usuário selecionado.")
                            else:
                                for uname in marcar:
                                    delete_user(uname)
                                st.success(f"Excluídos: {', '.join(marcar)}")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erro na exclusão: {e}")

            st.stop()  # não deixa cair nos demais blocos quando gerenciando usuários

        # ======= OUTRAS CONFIGURAÇÕES =======
        if configuracoes_menu == "Editar Cadastros":
            if editar_cadastro_menu == "Pacientes":
                edit_pacientes_st()
            elif editar_cadastro_menu == "Médicos":
                edit_medicos_st()

        elif configuracoes_menu == "Excluir Cadastros":
            if 'confirm_excluir' not in st.session_state:
                st.session_state.confirm_excluir = False
            if excluir_cadastro_menu == "Pacientes":
                st.warning("Atenção: exclusão de pacientes é irreversível.")
                alvo = st.text_input("Informe o ID/CPF do paciente a excluir:")
                if st.button("### 🗑️ Excluir Paciente"):
                    st.session_state.confirm_excluir = True
                if st.session_state.confirm_excluir:
                    st.error("Implementar ação de exclusão aqui (backend).")
                    if st.button("Cancelar"):
                        st.session_state.confirm_excluir = False

            elif excluir_cadastro_menu == "Médicos":
                st.warning("Atenção: exclusão de médicos é irreversível.")
                alvo = st.text_input("Informe o CRM do médico a excluir:")
                if st.button("### 🗑️ Excluir Médico"):
                    st.session_state.confirm_excluir = True
                if st.session_state.confirm_excluir:
                    st.error("Implementar ação de exclusão aqui (backend).")

elif menu_principal == "Ajuda":
    st.subheader("Ajuda")
    st.write("Documentação, FAQ, etc.")

elif menu_principal == "Sair":
    st.session_state.auth = {"authenticated": False, "username": None, "role": None, "login_time": None}
    st.switch_page("Home.py")
