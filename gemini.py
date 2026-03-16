import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# 1. Configuração e Estilo
st.set_page_config(page_title="Soluções - Equipe Técnica", page_icon="🔵", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #4c4c4c; }
    [data-testid="stForm"] { background-color: #4c4c4c; border: 2px solid #0056b3; border-radius: 15px; padding: 20px; }
    h1, h2, h3, p, span, label { color: white !important; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #0056b3; color: white; font-weight: bold; border: none; }
    [data-testid="stImageCaption"] { color: #00bfff !important; font-weight: bold; text-align: center; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔵 Soluções - Equipe Técnica")

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Formulário
with st.form(key="form_carajas", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        nome_input = st.text_input("NOME COMPLETO")
    with col2:
        cat_input = st.selectbox("", ["Carburada", "Injetada"])
    with col3:    
        placa - st.text_input("PLACA DO VEICULO")
    
    resp_input = st.text_area("Faça um descrição do estado atual e qual a cilindrada.", height=150)
    botao_enviar = st.form_submit_button("ENVIAR")

# 3. Lógica de Envio
if botao_enviar:
    if nome_input and resp_input:
        with st.spinner("Gravando na planilha..."):
            url = "https://docs.google.com/spreadsheets/d/1zFbwwSJNZPTXQ9fB5nUfN7BmeOay492QzStB6IIs7M8/edit"
            
            nova_linha = pd.DataFrame([{
                "Nome": nome_input, 
                "Placa": cat_input, 
                "Resposta": resp_input,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }])

            try:
                # Lógica simplificada de acúmulo
                df_atual = conn.read(spreadsheet=url, ttl=0)
                df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
                conn.update(spreadsheet=url, data=df_final)
                st.balloons()
                st.success("✅ Resposta salva com sucesso!")
            except Exception as e:
                st.error("Erro ao salvar: Verifique se o e-mail da Service Account está como EDITOR.")
    else:
        st.error("⚠️ Preencha todos os campos.")

st.write("---")

# 4. Carregamento Seguro da Imagem (Correção do NameError)
caminho_foto = os.path.join(os.path.dirname(__file__), "equipe.jpg")

if os.path.exists(caminho_foto):
    img_carregada = Image.open(caminho_foto)
    st.image(img_carregada, width='stretch', caption="Equipe CarajásNet - Agentes de Fidelização")
else:
    st.info("Carregando imagem da equipe...")

# 7. Painel de Resumo das Respostas (Dashboard)
st.write("---")
st.subheader("📊 Resumo da Colaboração")

# Força o Streamlit a esquecer os dados antigos a cada carregamento
st.cache_data.clear() 

try:
    # ttl=0 é fundamental para ignorar o cache do servidor público
    df_resumo = conn.read(spreadsheet=url, ttl=0)
    
    # Limpa a "sujeira" da planilha (remove linhas onde o Nome está em branco)
    df_resumo = df_resumo.dropna(subset=['Nome'])
    
    if not df_resumo.empty:
        col_graf1, col_graf2 = st.columns([2, 1])
        
        with col_graf1:
            st.write("**Distribuição por Tipo de Contato**")
            # Agrupa e conta os dados
            contagem = df_resumo['Placa'].value_counts()
            st.bar_chart(contagem, color="#00bfff")
            
        with col_graf2:
            st.write("**Engajamento**")
            total_mensagens = len(df_resumo)
            st.metric(label="Total de Feedbacks", value=total_mensagens)
            
            # Pega o último nome da lista real
            ultimo_nome = df_resumo['Nome'].iloc[-1]
            st.caption(f"Última colaboração: {ultimo_nome}")

        # Tabela expansível
        with st.expander("📄 Ver histórico completo"):
            st.dataframe(df_resumo[['Data', 'Nome', 'Placa', 'Resposta']], width='stretch')
            
    else:
        st.info("O resumo aparecerá aqui assim que os dados forem validados.")

except Exception as e:
    st.warning("Sincronizando com a planilha... Se demorar, verifique se há dados na aba principal.")
