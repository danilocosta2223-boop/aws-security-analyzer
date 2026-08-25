import streamlit as st
from PIL import Image
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Danilo Rafael da Silva Costa | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARREGAMENTO DO CSS GLOBAL ---
try:
    with open("style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except FileNotFoundError:
    pass

# --- TÍTULO PRINCIPAL ---
st.title("AWS Cyber Defense Platform")
st.subheader("Cloud Security Operations Center")

st.markdown("---")

# --- SEÇÃO DE APRESENTAÇÃO (FOTO E BOAS-VINDAS) ---
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
    
    Sou estudante de Defesa Cibernética na FIAP,
    possuo MBA em Gestão de Projetos,
    formação em Administração
    e formação internacional em Liderança Estratégica pela BYU.
    """)
    
    st.info("""
    Profissional com formação em Administração, MBA em Gestão de Projetos e especialização em Defesa Cibernética.
    Atualmente direcionando a carreira para Cloud Security, Governança AWS e Segurança da Informação.
    """)

st.markdown("---")

# --- QUEM SOU EU ---
st.header("Quem Sou Eu")
st.write("""
Profissional multidisciplinar com sólida vivência em operações corporativas, gestão de projetos e tecnologia. 
Busco unir a visão estratégica de negócios e governança com a execução técnica avançada em segurança da informação e ambientes em nuvem.
""")

st.markdown("---")

# --- MÉTRICAS DE SEGURANÇA (INTEGRADO VIA API NODE.JS) ---
st.header("Métricas de Segurança em Tempo Real")
st.write("Dados dinâmicos obtidos via API REST do back-end Node.js (`/api/security-score`).")

API_URL = "http://127.0.0.1:3000/api/security-score"

try:
    response = requests.get(API_URL, timeout=3)
    
    if response.status_code == 200:
        data = response.json()
        score = data.get("score")
        compliance = data.get("compliance")
        findings = data.get("findings")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Security Score", f"{score}/100", delta="+2% vs last week")
        with col2:
            st.metric("Compliance Rate", f"{compliance}%", delta="Optimal")
        with col3:
            st.metric("Open Findings", findings, delta="-3", delta_color="inverse")
    else:
        st.error(f"Erro ao consultar a API. Código: {response.status_code}")

except requests.exceptions.ConnectionError:
    st.warning("⚠️ **Servidor Node.js offline.** Certifique-se de executar `node server.js` no terminal para carregar as métricas em tempo real.")
except Exception as e:
    st.error(f"Ocorreu um erro ao conectar com a API: {e}")

st.markdown("---")

# --- EXPERIÊNCIA PROFISSIONAL ---
st.header("Experiência Profissional")
st.write("""
Atuação profissional em coordenação operacional, gestão de fornecedores, gestão de projetos, infraestrutura tecnológica e operações corporativas.

Experiência destacada no **Grupo Fleury**, participando de iniciativas estratégicas, migração de infraestrutura e suporte a operações críticas.
""")

st.markdown("---")

# --- FORMAÇÃO ---
st.header("Formação")
st.write("""
• Defesa Cibernética - FIAP  
• MBA em Gestão de Projetos  
• Administração  
• Strategic Leadership - Brigham Young University (BYU)  
""")

st.markdown("---")

# --- CERTIFICAÇÕES E CURSOS ---
st.header("Certificações e Cursos")
st.write("""
• Defesa Cibernética - FIAP  
• MBA em Gestão de Projetos  
• Strategic Leadership - BYU  
• Gestão de Infraestrutura de TI - FIAP  
• Cursos AWS e Cloud Security  
""")

st.markdown("---")

# --- OBJETIVO DA PLATAFORMA ---
st.header("Objetivo da Plataforma")
st.info("""
A AWS Cyber Defense Platform foi desenvolvida como projeto de demonstração profissional para apresentar competências em Cloud Security, Governança AWS, Threat Intelligence, Compliance, MITRE ATT&CK e Defesa Cibernética.

A solução centraliza informações de segurança em ambientes AWS e contempla:

- IAM Security
- S3 Security
- EC2 Security
- AWS Config
- Compliance
- MITRE ATT&CK
- Threat Intelligence
- Attack Path Analysis
- Relatórios Executivos
""")

st.markdown("---")

# --- PROJETOS REALIZADOS ---
st.header("Projetos Realizados")
st.write("""
• AWS Cyber Defense Platform (CSOC Enterprise)  
• Análise de Vulnerabilidades AWS  
• Projetos de Infraestrutura e Tecnologia (Grupo Fleury)  
• Monitoramento e Governança Cloud  
• Análise de Segurança utilizando AWS Security Hub  
""")

st.markdown("---")

# --- OBJETIVOS PROFISSIONAIS ---
st.header("Objetivos Profissionais")
st.write("""
Busco oportunidades relacionadas a Cloud Security, Governança de TI, Cyber Security, Gestão de Projetos e Operações Tecnológicas.

Esta plataforma foi criada para demonstrar minha evolução técnica e capacidade de desenvolver soluções voltadas para segurança em nuvem.
""")

st.markdown("---")

# --- COMPETÊNCIAS ---
st.header("Competências")
st.write("""
Cloud Security • AWS • Cyber Security • Governança • Compliance • Threat Intelligence • Python • Boto3 • Gestão de Projetos • Liderança
""")

st.markdown("---")

# --- TECNOLOGIAS ---
st.header("Tecnologias")

cols = st.columns(4)
tech_items = [
    ("assets/aws.png", "AWS"),
    ("assets/python.png", "Python"),
    ("assets/streamlit.png", "Streamlit"),
    ("assets/mitre.png", "MITRE ATT&CK")
]

for col, (img_path, nome) in zip(cols, tech_items):
    with col:
        try:
            st.image(img_path, width=70)
        except FileNotFoundError:
            pass
        st.caption(nome)

st.write("""
**Ecossistema e Serviços Utilizados:**  
AWS Config • GuardDuty • Security Hub • IAM • S3 • EC2 • RDS • Lambda • KMS • Boto3 • Python • Streamlit
""")

st.markdown("---")

# --- CONTATO, REDES PROFISSIONAIS E CURRÍCULO ---
st.header("Contato & Redes Profissionais")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        st.image("assets/github.png", width=80)
    except FileNotFoundError:
        pass
    st.link_button("GitHub", "https://github.com/danilocosta/aws-security-analyzer", use_container_width=True)

with col2:
    try:
        st.image("assets/linkedin.png", width=80)
    except FileNotFoundError:
        pass
    st.link_button("LinkedIn", "https://www.linkedin.com/in/danilocosta2223", use_container_width=True)

with col3:
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    try:
        with open("curriculo.pdf", "rb") as pdf_file:
            st.download_button(
                label="📄 Baixar Currículo (PDF)",
                data=pdf_file,
                file_name="Danilo_Rafael_Costa.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except FileNotFoundError:
        st.caption("💡 *Adicione 'curriculo.pdf' na raiz para habilitar o download.*")

st.markdown("""
**E-mail de Contato:** profissional@danilocosta.com
""")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Danilo Rafael da Silva Costa | AWS Cyber Defense Platform | Cloud Security Operations Center")