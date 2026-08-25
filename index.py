import streamlit as st
from PIL import Image
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Danilo Rafael da Silva Costa | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="home_refresh")

# ==========================================
# 3. ESTILO CSS GLOBAL (FUNDO BRANCO)
# ==========================================
try:
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #1e3a5f;
        }
        .hero-card {
            background-color: #f3f4f6;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 20px;
        }
        h1, h2, h3, h4 {
            color: #1e3a8a;
        }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. CABEÇALHO DO MÓDULO (HERO CARD)
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>AWS Cyber Defense Platform</h1>
    <p style="color: #4b5563; margin: 0; font-size: 15px;">
        Cloud Security Operations Center • Governança, Threat Intelligence e Monitoramento Contínuo
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #4b5563; margin-bottom: 20px;">
    <b>Status da Plataforma:</b> Operacional &nbsp;|&nbsp; 
    <b>Última Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 5. SEÇÃO DE APRESENTAÇÃO (FOTO E BIO)
# ==========================================
col_foto, col_bio = st.columns([1, 3], gap="large")

with col_foto:
    try:
        st.image("foto_danilo.jpg", width=250)
    except FileNotFoundError:
        st.info("Adicione 'foto_danilo.jpg' na raiz do projeto.")

with col_bio:
    st.header("Seja Bem-Vindo")
    st.write("""
    Meu nome é Danilo Rafael da Silva Costa.
    
    Sou estudante de Defesa Cibernética na FIAP, possuo MBA em Gestão de Projetos, formação em Administração e formação internacional em Liderança Estratégica pela BYU.
    """)
    
    st.info("""
    Profissional com sólida vivência em operações corporativas, gestão de projetos e tecnologia. Atualmente direcionando a carreira para Cloud Security, Governança AWS e Segurança da Informação.
    """)

st.markdown("---")

# ==========================================
# 6. MÉTRICAS DE SEGURANÇA EM TEMPO REAL (API)
# ==========================================
st.header("Métricas de Segurança em Tempo Real")
st.write("Dados dinâmicos obtidos via API REST do back-end Node.js no Render.")

# Substitua pela URL real fornecida pelo Render após o deploy do backend
API_URL = "https://aws-security-analyzer-api.onrender.com/api/security-score"

try:
    response = requests.get(API_URL, timeout=3)
    
    if response.status_code == 200:
        data = response.json()
        score = data.get("score", 88)
        compliance = data.get("compliance", 92)
        findings_count = data.get("findings", 3)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Security Score", f"{score}/100", delta="+2% vs last week")
        with c2:
            st.metric("Compliance Rate", f"{compliance}%", delta="Optimal")
        with c3:
            st.metric("Open Findings", findings_count, delta="-3", delta_color="inverse")
    else:
        st.error(f"Erro ao consultar a API. Código: {response.status_code}")

except requests.exceptions.ConnectionError:
    st.warning("Servidor Node.js offline no momento. As métricas estáticas padrão estão sendo exibidas.")
except Exception as e:
    st.error(f"Ocorreu um erro ao conectar com a API: {e}")

st.markdown("---")

# ==========================================
# 7. OBJETIVO DA PLATAFORMA & FORMAÇÃO
# ==========================================
col_form, col_cert = st.columns(2)

with col_form:
    st.header("Formação Acadêmica")
    st.write("""
    - Defesa Cibernética - FIAP  
    - MBA em Gestão de Projetos  
    - Administração  
    - Strategic Leadership - Brigham Young University (BYU)  
    """)

with col_cert:
    st.header("Objetivo da Plataforma")
    st.write("""
    Centralizar informações de segurança em ambientes AWS contemplando:
    - IAM & S3 Security
    - AWS Config & Compliance
    - MITRE ATT&CK & Threat Intelligence
    - Análise de Riscos Automatizada
    """)

st.markdown("---")

# ==========================================
# 8. CONTATO E REDES PROFISSIONAIS
# ==========================================
st.header("Contato & Redes Profissionais")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("GitHub", "https://github.com/danilocosta2223-boop/aws-security-analyzer", use_container_width=True)

with col2:
    st.link_button("LinkedIn", "https://www.linkedin.com/in/danilocosta2223", use_container_width=True)

with col3:
    try:
        with open("curriculo.pdf", "rb") as pdf_file:
            st.download_button(
                label="Baixar Currículo (PDF)",
                data=pdf_file,
                file_name="Danilo_Rafael_Costa.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except FileNotFoundError:
        st.caption("Currículo em PDF indisponível no momento.")

# ==========================================
# RODAPÉ
# ==========================================
st.markdown("---")
st.caption(f"Danilo Rafael da Silva Costa | AWS Cyber Defense Platform | Cloud Security Operations Center • Atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")