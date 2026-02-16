import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configuração da página
st.set_page_config(page_title="Soluções - Equipe Técnica", page_icon="🔵", layout="centered")

# 2. CSS Customizado (Fundo escuro conforme seu código anterior)
st.markdown("""
    <style>
    .stApp { background-color: #4c4c4c; }
    [data-testid="stForm"] {
        background-color: #4c4c4c;
        border: 2px solid #0056b3;
        border-radius: 15px;
        padding: 20px;
    }
    h1, h2, h3, p, span, label { color: white !important; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #0056b3; 
        color: white;
        font-weight: bold;
        border: none;
    }
    [data-testid="stImageCaption"] {
        color: #00bfff !important;
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔵 Soluções - Equipe Técnica")

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Formulário
with st.form(key="form_carajas", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        nome = st.text_input("NOME COMPLETO", placeholder="Digite seu nome")
    with col2:
        categoria = st.selectbox("TIPO DE CONTATO", ["Resposta", "Sugestão", "Comentário"])
    
    pergunta = "Em que ocasião é utilizado o diagnóstico *Equipamento desconfigurado*?"
    resposta = st.text_area(pergunta, height=150, placeholder="Escreva aqui...")
    
    botao_enviar = st.form_submit_button("ENVIAR")

# 5. Lógica de Envio (Ordem: Nome, Categoria, Resposta, Data)
if botao_enviar:
    if nome and resposta:
        with st.spinner("Enviando resposta..."):
            url = "https://docs.google.com/spreadsheets/d/1zFbwwSJNZPTXQ9fB5nUfN7BmeOay492QzStB6IIs7M8/edit"
            
            # Criando o DataFrame na ordem exata da sua planilha
            nova_linha = pd.DataFrame([{
                "Nome": nome, 
                "Categoria": categoria, 
                "Resposta": resposta,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }])

            try:
                # Usamos o create para anexar a linha ao final
                conn.create(spreadsheet=url, data=nova_linha)
                st.balloons()
                st.success("✅ Registrado com sucesso na planilha!")
            except Exception as e:
                st.error("Erro técnico ao salvar. Verifique se a planilha tem os cabeçalhos corretos.")
    else:
        st.error("⚠️ Preencha nome e resposta antes de enviar.")

st.write("---")
st.image("equipe.jpg", use_container_width=True, caption="Equipe CarajásNet - Agentes de Fidelização")
