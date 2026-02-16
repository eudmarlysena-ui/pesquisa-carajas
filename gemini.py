import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import os

# 1. Configuração da página
st.set_page_config(page_title="Soluções - Equipe Técnica", page_icon="🔵", layout="centered")

# 2. Estilo Visual (Fundo Escuro e Letras Claras)
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

# 3. Formulário
with st.form(key="form_carajas", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        nome_input = st.text_input("NOME COMPLETO", placeholder="Digite seu nome")
    with col2:
        cat_input = st.selectbox("TIPO DE CONTATO", ["Resposta", "Sugestão", "Comentário"])
    
    resp_input = st.text_area("Em que ocasião é utilizado o diagnóstico Equipamento desconfigurado?", height=150)
    botao_enviar = st.form_submit_button("ENVIAR")

# 4. Lógica de Envio Otimizada para 2026
# 4. Lógica de Envio (Método Append Direto)
if botao_enviar:
    if nome_input and resp_input:
        with st.spinner("Gravando na planilha..."):
            url = "https://docs.google.com/spreadsheets/d/1zFbwwSJNZPTXQ9fB5nUfN7BmeOay492QzStB6IIs7M8/edit"
            
            # Criamos os dados exatamente na ordem da planilha: Nome, Categoria, Resposta, Data
            nova_linha = pd.DataFrame([{
                "Nome": nome_input, 
                "Categoria": cat_input, 
                "Resposta": resp_input,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }])

            try:
                # O comando .create() atua como um 'Append' quando a planilha já existe
                # É mais estável que o .update() para formulários
                conn.create(spreadsheet=url, data=nova_linha)
                
                st.balloons()
                st.success("✅ Resposta salva com sucesso!")
            except Exception as e:
                st.error("Erro ao salvar: Verifique se o e-mail da Service Account está como EDITOR.")
                # st.write(e) # Descomente esta linha se precisar ver o erro técnico exato
    else:
        st.error("⚠️ Preencha todos os campos.")

# 5. Imagem da Equipe com o novo parâmetro 'width'
# Substituindo use_container_width=True por width='stretch'
st.image("equipe.jpg", width='stretch', caption="Equipe CarajásNet - Agentes de Fidelização")
