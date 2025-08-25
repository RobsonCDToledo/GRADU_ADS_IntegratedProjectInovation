# 🏥 Sistema de Gestão Clínica Vida+

**Versão atual:** 0.5 (Em desenvolvimento)  
**Autor:** Robson Carlos Donizette de Toledo  

---

## 📌 Descrição do Projeto
O **Sistema de Gestão Clínica Vida+** é uma aplicação desenvolvida em **Python + Streamlit** para auxiliar clínicas no gerenciamento de pacientes, médicos, consultas e indicadores operacionais.  
O sistema conta com controle de acesso por perfil de usuário (**RBAC**), interface responsiva e integração com banco de dados SQLite.

Atualmente, o projeto encontra-se em desenvolvimento, com **divisão de funcionalidades por módulos** e **autenticação com diferentes níveis de permissão**.

---

## 🚀 Funcionalidades Implementadas

- **🔐 Autenticação e Controle de Acesso**
  - Login com senha criptografada (`bcrypt`).
  - Perfis: `admin`, `gestor`, `recepcao` e `medico`.
  - Sessão com tempo de expiração configurável.

- **📂 Módulos do Sistema**
  - **Cadastros:** Registro de pacientes e médicos.
  - **Consultas:** (em desenvolvimento) Agenda e controle de atendimentos.
  - **Relatórios:** Visualização de pacientes e médicos cadastrados.
  - **Configurações:**
    - Gerenciar Usuários (admin):
      - Cadastrar
      - Editar (perfil, status e senha)
      - Excluir
    - Editar e excluir cadastros de pacientes e médicos.

- **📊 Dashboard Inicial**
  - 4 blocos de indicadores (exemplos estáticos):
    1. Fila de espera
    2. Agendados não apresentados
    3. Tempo médio de atendimento
    4. Índice de qualidade

- **🎨 Interface**
  - Layout responsivo com **sidebar** para navegação.
  - Header fixo exibindo usuário logado e perfil.
  - Cartões de indicadores com estilo unificado.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.13
- **Framework:** [Streamlit](https://streamlit.io/)
- **Banco de Dados:** SQLite
- **Bibliotecas:**
  - `pandas`
  - `pytz`
  - `bcrypt`
  - `streamlit-autorefresh`

---

## 📂 Estrutura de Pastas (parcial)

ClinicalScheduleManager/  
│  
├── auth.py # Autenticação e CRUD de usuários  
├── home.py # Tela inicial de login  
├── pages/  
│ └── system.py # Sistema principal  
│  
├── gui/  
│ ├── cad/ # Telas de cadastros  
│ │ ├── pag_cad_pacientes.py  
│ │ └── pag_cad_medicos.py  
│ ├── view/ # Visualizações e relatórios  
│ │ └── view_tables_st.py  
│ └── configs/ # Telas de edição  
│ └── edit.py  
│  
├── dict/ # Dicionários de opções  
│ └── dicionarios.py  
│  
├── db/  
│ └── data/  
│ └── clinica_vidaplus.db # Banco de dados SQLite  
│  
└── requirements.txt  


---

## 📅 Etapa Atual

✅ Login e RBAC implementados.  
✅ Cadastros de pacientes e médicos funcionando.  
✅ Relatórios básicos exibindo dados do banco.  
✅ CRUD de usuários para administradores.  
✅ Dashboard inicial com 4 blocos de KPIs (dados simulados).  
🚧 Módulo de consultas em desenvolvimento.  
🚧 Integração dos KPIs com dados reais do banco.  
🚧 Melhorias visuais e responsividade total.

---

## ▶️ Como Executar

1. **Clonar o repositório**
```bash 
git clone https://github.com/seu-usuario/vida-plus.git
cd vida-plus
```
2. **Criar e ativar ambiente virtual**
```bash 
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```
3. **Instalar depedências**
```bash 
pip install -r requirements.txt
```
4. **Rodar o sistema**
```bash 
streamlit run home.py
```

🔒 Login Padrão (primeira execução)

Ao iniciar o sistema pela primeira vez, será criado automaticamente:  
Usuário: admin  
Senha: admin123  
Perfil: admin  

⚠️ Recomendado alterar a senha assim que possível.

📌 Próximos Passos
  - Implementar módulo completo de Consultas.  
  - Integrar dashboard inicial com dados reais.  
  - Melhorar layout para dispositivos móveis.  
  - Criar relatórios avançados (filtros e exportação).  

📜 Licença

Este projeto é de uso acadêmico e profissional sob a licença MIT.



