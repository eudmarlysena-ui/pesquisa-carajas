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
        cat_input = st.selectbox("TIPO DE CONTATO", ["Resposta", "Sugestão", "Comentário"])
    
    resp_input = st.text_area("Em que ocasião é utilizado o diagnóstico Equipamento desconfigurado?", height=150)
    botao_enviar = st.form_submit_button("ENVIAR")

# 3. Lógica de Envio
if botao_enviar:
    if nome_input and resp_input:
        with st.spinner("Gravando na planilha..."):
            url = "https://docs.google.com/spreadsheets/d/1zFbwwSJNZPTXQ9fB5nUfN7BmeOay492QzStB6IIs7M8/edit"
            
            nova_linha = pd.DataFrame([{
                "Nome": nome_input, 
                "Categoria": cat_input, 
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
st.subheader("📊 Resumo de Atendimentos")

try:
    # Lê os dados mais recentes da planilha
    df_resumo = conn.read(spreadsheet=url, ttl=0)
    
    if not df_resumo.empty:
        # 1. Gráfico por Categoria
        contagem_categorias = df_resumo['Categoria'].value_counts()
        
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.write("**Distribuição por Tipo**")
            # Cria um gráfico de barras simples e elegante
            st.bar_chart(contagem_categorias, color="#00bfff")
            
        with col_graf2:
            st.write("**Total de Registros**")
            total = len(df_resumo)
            st.metric(label="Mensagens Recebidas", value=total, delta=f"+ {len(nova_linha)}" if botao_enviar else None)
            
        # 2. Tabela de Últimas Respostas (opcional, para visualização rápida)
        with st.expander("Ver últimas mensagens recebidas"):
            st.dataframe(df_resumo.tail(5)[['Data', 'Nome', 'Categoria']], use_container_width=True)
            
    else:
        st.info("Ainda não há dados suficientes para gerar o resumo.")

except Exception as e:
    st.write("O resumo será exibido assim que os primeiros dados forem processados.")
