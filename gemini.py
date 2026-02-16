import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configuração da página
st.set_page_config(page_title="Soluções - Equipe Técnica", page_icon="🔵", layout="centered")

# 2. CSS Customizado focado em Azul e Branco
st.markdown("""
    <style>
    .stApp {
        background-color: #4c4c4c;
    }
    [data-testid="stForm"] {
        background-color: #4c4c4c;
        border: 2px solid #0056b3;
        border-radius: 15px;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #004085;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #0056b3; 
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004085;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho Principal
st.title("🔵 Soluções - Equipe Técnica")
st.write("Sua opinião nos ajuda a sermos mais do que técnicos, sermos agentes de fidelização.")

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Formulário de Pesquisa
with st.form(key="form_carajas", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        nome = st.text_input("NOME COMPLETO", placeholder="Digite seu nome completo")
    with col2:
        categoria = st.selectbox("TIPO DE CONTATO", ["Resposta", "Sugestão", "Comentário",])
    
    resposta = st.text_area("Em que ocasião é utilizado o diagnóstico *Equipamento desconfigurado*?", height=150, placeholder="Escreva aqui...")
    
    botao_enviar = st.form_submit_button("ENVIAR")

# 5. Lógica de Envio
if botao_enviar:
    if nome and resposta:
        # ... (dentro do if botao_enviar)
        with st.spinner("Salvando na planilha..."):
            url = "https://docs.google.com/spreadsheets/d/1zFbwwSJNZPTXQ9fB5nUfN7BmeOay492QzStB6IIs7M8/edit"
            
            # 1. Tenta ler os dados atuais. Se falhar (planilha vazia), cria um DF novo.
            try:
                df_existente = conn.read(spreadsheet=url, ttl=0)
            except:
                df_existente = pd.DataFrame(columns=["Data", "Nome", "Categoria", "Resposta"])

            # 2. Cria a nova linha
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"), 
                "Nome": nome, 
                "Categoria": categoria, 
                "Resposta": resposta
            }])
            
            # 3. Empilha os dados (Antigos + Novo)
            df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
            
            # 4. LIMPEZA: Remove linhas que sejam completamente vazias (evita erros de tamanho)
            df_final = df_final.dropna(how='all')

            # 5. ATUALIZAÇÃO CORRIGIDA:
            # O parâmetro 'index=False' é essencial para evitar o UnsupportedOperationError
            conn.update(spreadsheet=url, data=df_final)
            
            st.balloons()
            st.success("✅ Mensagem registrada!")
    else:
        st.error("⚠️ Por favor, preencha todos os campos.")

# 6. Imagem da Equipe abaixo do formulário
st.write("---") # Linha divisória
st.image("equipe.jpg", use_container_width=True, caption="Equipe CarajásNet - Agentes de Fidelização")
