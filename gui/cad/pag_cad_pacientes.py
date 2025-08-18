'''
============================================================
Sistema de Gestão Clínica Vida+
Módulo: 
------------------------------------------------------------
Descrição:
   Descrição do código

Autor: Robson Carlos Donizette de Toledo
Data de criação: `date +'%d/%m/%Y'`
Última atualização: `date +'%d/%m/%Y'`
Versão: 1.0
============================================================
'''

import re
import streamlit as st
from datetime import datetime, date
from db.repos.repositorio_pacientes import inserir_paciente, buscar_cpf
from dict.dicionarios import dict_generos


def form_cadastro_paciente():
    """ Função para exibir o formulário de cadastro de paciente no Streamlit com revisão antes da submissão.
    """
    st.markdown('<h2 style="color:blue; font-family:Arial;">Formulário de Cadastro de Pacientes:</h2>',
                unsafe_allow_html=True)

    if 'dados_paciente' not in st.session_state:
        st.session_state.dados_paciente = {
            'nome': '',
            'genero': 'Selecionar',
            'data_nascimento': '',
            'telefone': '',
            'email': '',
            'cpf': ''
        }
    if 'revisar' not in st.session_state:
        st.session_state.revisar = False

    # Campo nome do Paciente
    nome = st.text_input("Nome do Paciente:",
                         value=st.session_state.dados_paciente['nome'])
    # Lista de opções de Gênero
    opcoes_genero = list(dict_generos.keys())
    valor_atual = st.session_state.dados_paciente.get('genero', '')
    if valor_atual in opcoes_genero:
        index_genero = opcoes_genero.index(valor_atual)
    else:
        index_genero = 0
    # Campo de seleção de Gênero
    genero = st.selectbox(
        "Gênero:",
        options=opcoes_genero,
        index=index_genero
    )
    # Calendário para selecionar data
    data_str_armazenada = st.session_state.dados_paciente['data_nascimento']
    if isinstance(data_str_armazenada, str) and data_str_armazenada:
        # Se for string, converte para date
        data_padrao = datetime.strptime(data_str_armazenada, "%Y-%m-%d").date()
    elif isinstance(data_str_armazenada, date):
        # Se já for date, usa diretamente
        data_padrao = data_str_armazenada
    else:
        data_padrao = date.today()
    # Campo de Data de Nascimento
    data_nascimento = st.date_input(
        "Data de Nascimento:",
        value=data_padrao,
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    # Converte data para armazenar no banco
    data_str = data_nascimento.strftime("%Y-%m-%d")

    # Campo Telefone
    telefone = st.text_input(
        "Celular (DDD + número):",
        value=st.session_state.dados_paciente.get('telefone', '')
    )
    if telefone and not re.fullmatch(r"\d{11}", telefone):
        st.warning(
            "Telefone inválido. Por favor, insira 11 dígitos sem espaços ou símbolos.")

    # Campo e-mail
    email = st.text_input(
        "E-mail:",
        value=st.session_state.dados_paciente.get('email', '')
    )
    if email and not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning("E-mail inválido. Por favor, insira um e-mail válido.")

    # Campo CPF
    cpf = st.text_input(
        "CPF (Formato: 000.000.000-00):",
        value=st.session_state.dados_paciente.get('cpf', '')
    )
    if cpf and not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        st.warning("CPF inválido. Deve seguir o padrão 000.000.000-00.")

    # Armazenar dados inseridos
    st.session_state.dados_paciente.update({
        'nome': nome,
        'genero': genero,
        'data_nascimento': data_nascimento,
        'telefone': telefone,
        'email': email,
        'cpf': cpf
    })

    # Botão de revisão
    if st.button("Revisar Dados"):
        st.session_state.revisar = True

    # Exibir os dados para serem revisados
    if st.session_state.revisar:
        st.markdown(
            '<h4 style="color:green; font-family:Verdana;">Revise os dados antes de cadastrar</h4>', unsafe_allow_html=True)
        st.write(f"**Nome:** {nome}")
        st.write(f"**Gênero:** {genero}")
        st.write(f"**Data de Nascimento:** {data_nascimento}")
        st.write(f"**Telefone:** {telefone}")
        st.write(f"**E-mail:** {email}")
        st.write(f"**CPF:** {cpf}")
        st.info(
            "Se algum dado estiver incorreto, ajuste os campos acima antes de confirmar.")

        if st.button("Confirmar Cadastro"):
            erros = []

            if not nome or not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome):
                erros.append("Nome inválido. Use apenas letras e espaços.")

            if genero == "Selecionar":
                erros.append("Selecione um gênero válido.")

            if not data_nascimento:
                erros.append("Data de nascimento não pode estar vazia.")
            elif data_nascimento > date.today():
                erros.append("Data de nascimento não pode ser futura.")

            padrao_telefone = r"^\d{11}$"
            if telefone and not re.fullmatch(padrao_telefone, telefone):
                erros.append(
                    "Telefone inválido. Deve conter 11 dígitos sem espaços ou símbolos.")

            padrao_email = r"[^@]+@[^@]+\.[^@]+"
            if email and not re.fullmatch(padrao_email, email):
                erros.append(
                    "E-mail inválido. Deve seguir o padrão nome@dominio.com")

            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                dados_paciente_final = {
                    'nome': nome.title(),
                    'genero': genero,
                    'data_nascimento': data_str,
                    'telefone': telefone,
                    'email': email,
                    'cpf': cpf
                }
                try:
                    inserir_paciente(dados_paciente_final)
                    st.success("Cadastro realizado com sucesso!")
                    st.session_state.dados_paciente = {
                        'nome': '',
                        'genero': 'Selecionar',
                        'data_nascimento': '',
                        'telefone': '',
                        'email': '',
                        'cpf': ''
                    }
                except Exception as e:
                    st.error(f"Erro ao cadastrar paciente: {e}")
