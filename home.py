import streamlit as st
from datetime import datetime
from auth import init_db, verify_login, user_exists, create_user

st.set_page_config(
    page_title="Vida+ | Login",
    layout="centered",                 # layout mais compacto
    initial_sidebar_state="collapsed"  # recolhe a sidebar
)
st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;} /* esconde o “hamburger” */
        </style>
    """, unsafe_allow_html=True)

# 🔒 Ocultar COMPLETAMENTE a sidebar só nesta página:
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;} /* esconde o “hamburger” */
    </style>
""", unsafe_allow_html=True)

# Bootstrap do DB e admin padrão (somente 1ª vez)
init_db()
if not user_exists("admin"):
    create_user("admin", "admin123", "admin")  # chamada posicional

# Estado de autenticação
if "auth" not in st.session_state:
    st.session_state.auth = {
        "authenticated": False,
        "username": None,
        "role": None,
        "login_time": None,
    }

# ====== Layout centralizado ======
# ajuste as proporções se quiser
left, center, right = st.columns([1, 1.2, 1])

with center:
    # Logo centralizada
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    st.image("gui/themes/image/logo_clinica.png", width=250)
    st.markdown("</div>", unsafe_allow_html=True)

    # Formulário centralizado
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        ok = st.form_submit_button("Entrar")

    if ok:
        user = verify_login(username, password)
        if user:
            st.session_state.auth.update({
                "authenticated": True,
                "username": user["username"],
                "role": user["role"],
                "login_time": datetime.utcnow(),
            })
            st.success(f"Bem-vindo, {user['username']}!")
            st.switch_page("pages/system.py")
        else:
            st.error("Credenciais inválidas ou usuário inativo.")

# Se já estiver logado, leva direto pro sistema
if st.session_state.auth["authenticated"]:
    st.switch_page("pages/system.py")
