import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configuração da página e Identidade Visual
st.set_page_config(page_title="Pesquisa CarajásNet", page_icon="🔵", layout="centered")

# 2. CSS Customizado para Azul e Branco
st.markdown("""
    <style>
    /* Fundo principal em branco/gelo */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Estilização do Bloco do Formulário */
    [data-testid="stForm"] {
        background-color: #F0F8FF; /* Azul Alice (muito claro) */
        border: 2px solid #0056b3; /* Borda azul forte */
        border-radius: 15px;
        padding: 20px;
    }
    
    /* Estilização dos Títulos */
    h1, h2, h3 {
        color: #004085; /* Azul marinho */
        font-family: 'sans-serif';
    }

    /* Botão de Enviar: Azul Forte com texto Branco */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #0056b3; 
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    /* Efeito ao passar o mouse no botão */
    .stButton>button:hover {
        background-color: #004085;
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
    }

    /* Ajuste nas labels (nomes dos campos) */
    .stWidgetLabel p {
        color: #004085;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho
st.title("🔵 Central de Atendimento")
st.write("Preencha as informações abaixo para que possamos te ajudar.")

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Formulário
with st.form(key="form_pesquisa", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        nome = st.text_input("NOME COMPLETO", placeholder="Ex: João Silva")
    with col2:
        categoria = st.selectbox("TIPO DE MENSAGEM", ["Dica", "Sugestão", "Elogio", "Outros"])
    
    resposta = st.text_area("SUA MENSAGEM", height=120, placeholder="Escreva aqui...")
    
    botao_enviar = st.form_submit_button("ENVIAR AGORA")

# 5. Lógica de Envio
if botao_enviar:
    if nome and resposta:
        with st.spinner("Conectando ao servidor..."):
            url = "https://docs.google.com/spreadsheets/d/1zFbwwSJNZPTXQ9fB5nUfN7BmeOay492QzStB6IIs7M8/edit"
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Lendo a planilha (garanta que as colunas existam no Google Sheets)
            df_existente = conn.read(spreadsheet=url, usecols=[0, 1, 2, 3])
            
            nova_linha = pd.DataFrame([{
                "Data": data_atual, 
                "Nome": nome, 
                "Categoria": categoria, 
                "Resposta": resposta
            }])
            
            df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
            conn.update(spreadsheet=url, data=df_final)
            
            st.balloons()
            st.success("✅ Mensagem enviada! Entraremos em contato se necessário.")
    else:
        st.error("❌ Por favor, preencha todos os campos obrigatórios.")
                