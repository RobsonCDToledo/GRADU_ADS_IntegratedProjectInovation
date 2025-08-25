"""Formulário de Cadastro de Médicos com Revisão e Validação de Dados"""

import re
import streamlit as st
from db.repos.repositorio_medicos import inserir_medico, buscar_crm
from dict.dicionarios import dict_especialidades_medicas


def form_cadastro_medico():
    """
    Função para exibir o formulário de cadastro 
    de médico no Streamlit com revisão antes da submissão.
    Permite usar HTML/CSS para customizar títulos e textos.
    """
    # Título customizado com cor e fonte
    st.markdown('<h2 style="color:blue; font-family:Arial;">Formulário de Cadastro de Médicos:</h2>',
                unsafe_allow_html=True)

    # Sessão para manter dados temporários e controle de revisão
    if 'dados_medico' not in st.session_state:
        st.session_state.dados_medico = {
            'nome': '',
            'crm': '',
            'especialidade': '',  # deixar vazio inicialmente
            'status': 'Selecionar'
        }
    if 'revisar' not in st.session_state:
        st.session_state.revisar = False

    # Entrada de dados
    nome = st.text_input(
        "Nome do médico: ", value=st.session_state.dados_medico['nome'])
    crm = st.text_input("CRM do médico (Formato: 00000/XX): ",
                        value=st.session_state.dados_medico['crm']).upper()

    # Preparar lista de opções e índice inicial seguro
    opcoes_especialidade = list(dict_especialidades_medicas.keys())
    valor_atual = st.session_state.dados_medico.get('especialidade', '')
    if valor_atual in opcoes_especialidade:
        index_especialidade = opcoes_especialidade.index(valor_atual)
    else:
        index_especialidade = 0  # selecionar a primeira opção por padrão

    especialidade = st.selectbox(
        "Especialidade: ",
        options=opcoes_especialidade,
        index=index_especialidade
    )

    # Status
    opcoes_status = ["Selecionar", "Ativo", "Inativo", "Afastado"]
    valor_status = st.session_state.dados_medico.get('status', 'Selecionar')
    if valor_status in opcoes_status:
        index_status = opcoes_status.index(valor_status)
    else:
        index_status = 0

    status = st.selectbox(
        "Status: ",
        options=opcoes_status,
        index=index_status
    )

    # Atualizar sessão
    st.session_state.dados_medico.update({
        'nome': '',
        'crm': '',
        'especialidade': '',
        'status': ''
    })

    # Botão para revisão
    if st.button("Revisar Dados"):
        st.session_state.revisar = True

    # Exibir revisão e botão de confirmação apenas após clicar em Revisar
    if st.session_state.revisar:
        st.markdown(
            '<h4 style="color:green; font-family:Verdana;">Revise os dados antes de cadastrar</h4>', unsafe_allow_html=True)
        st.write(f"**Nome:** {nome}")
        st.write(f"**CRM:** {crm}")
        st.write(f"**Especialidade:** {especialidade}")
        st.write(f"**Status:** {status}")
        st.info(
            "Se algum dado estiver incorreto, ajuste os campos acima antes de confirmar.")

        if st.button("Confirmar Cadastro"):
            erros = []

            if not nome or not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
                erros.append("Nome inválido. Use apenas letras e espaços.")

            padrao_crm = r"^\d{5}/[A-Z]{2}$"
            if not re.fullmatch(padrao_crm, crm):
                erros.append("CRM inválido. Deve seguir o padrão 00000/XX.")
            elif buscar_crm(crm):
                erros.append("CRM já cadastrado. Insira um CRM diferente.")

            if especialidade not in dict_especialidades_medicas:
                erros.append(
                    "Especialidade inválida. Selecione uma opção válida.")

            if status not in ["Ativo", "Inativo", "Afastado"]:
                erros.append("Status inválido.")

            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                dados_medico_final = {
                    'nome': nome.title(),
                    'crm': crm,
                    'especialidade': especialidade.title(),
                    'status': status
                }
                try:
                    inserir_medico(dados_medico_final)
                    st.success("Médico cadastrado com sucesso!")
                    # Limpar sessão após cadastro
                    st.session_state.dados_medico = {
                        'nome': '', 'crm': '', 'especialidade': '', 'status': 'Selecionar'
                    }
                    st.session_state.revisar = False
                except Exception as e:
                    st.error(f"Erro ao cadastrar médico: {e}")
