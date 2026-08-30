import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="AWS Cyber Defense Platform | Enterprise SOC",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. OCULTAR ELEMENTOS PADRÃO DO STREAMLIT
# ==========================================
st.markdown("""
<style>
header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. PALETA DE CORES E ESTILIZAÇÃO CORPORATIVA
# ==========================================
PRIMARY_BLUE = "#2563EB"
LIGHT_BLUE = "#60A5FA"
CARD_BG = "#1E293B"
PAGE_BG = "#0F172A"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#CBD5E1"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"

st.markdown(f"""
<style>
.stApp {{
    background: {PAGE_BG};
    color: {TEXT_COLOR};
}}
h1, h2, h3, h4 {{
    color: {TEXT_COLOR} !important;
}}
p, div, span, label {{
    color: {MUTED_TEXT} !important;
}}
section[data-testid="stSidebar"] {{
    background: {CARD_BG};
}}
.stButton > button {{
    background-color: {PRIMARY_BLUE} !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}}
.stButton > button:hover {{
    background-color: #1D4ED8 !important;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR PROFISSIONAL
# ==========================================
st.sidebar.markdown("""
# AWS Cyber Defense
**Powered by Kali Linux SOC**
---
""")

st.sidebar.markdown("## Módulos do Sistema")
st.sidebar.write("• Executive Dashboard")
st.sidebar.write("• Executive View")
st.sidebar.write("• Security Center")
st.sidebar.write("• Security Hub")
st.sidebar.write("• Threat Intelligence")
st.sidebar.write("• Security Copilot")
st.sidebar.write("• IAM Security")
st.sidebar.write("• EC2 Security")
st.sidebar.write("• Compliance Center")
st.sidebar.write("• Audit History")
st.sidebar.write("• Security AI Engine")
st.sidebar.write("• Prompt Engine")

st.sidebar.markdown("---")

# ==========================================
# 5. HERO PRINCIPAL (ENTERPRISE GRADE)
# ==========================================
st.markdown("""
<div style="
background: linear-gradient(135deg,#020617,#0F172A,#1D4ED8);
padding:60px;
border-radius:30px;
text-align:center;
border:2px solid #2563EB;
box-shadow:0px 0px 50px rgba(37,99,235,.5);
margin-bottom:25px;
">

<h1 style="
font-size:52px;
font-weight:700;
color:white;
margin-bottom:10px;
">
AWS CYBER DEFENSE PLATFORM
</h1>

<h2 style="
font-size:24px;
color:#93C5FD;
font-weight:400;
margin-top:0;
margin-bottom:20px;
">
Powered by Kali Linux Security Operations Center
</h2>

<p style="
font-size:18px;
color:#E2E8F0;
max-width:1100px;
margin:auto;
line-height:1.6;
">
Enterprise Security Platform for Cloud Protection, Threat Intelligence, Governance, Compliance and Advanced Security Operations.
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. O QUE É A PLATAFORMA
# ==========================================
st.markdown("""
<div style="
background:#1E293B;
padding:25px;
border-radius:20px;
border-left:6px solid #2563EB;
margin-bottom:30px;
">

<h2 style="color:white; margin-top:0;">
O que é a AWS Cyber Defense Platform?
</h2>

<p style="
font-size:17px;
line-height:1.8;
color:#CBD5E1;
margin-bottom:15px;
">
A <b>AWS Cyber Defense Platform</b> é uma solução integrada desenvolvida para monitoramento de segurança, governança, compliance, inteligência de ameaças e proteção avançada de ambientes AWS.
</p>

<p style="
font-size:16px;
line-height:1.6;
color:#94A3B8;
margin-bottom:0;
">
<b>Áreas de Atuação:</b> Monitoramento &bull; Governança &bull; Compliance &bull; Threat Intelligence &bull; Cloud Security &bull; Segurança AWS
<br>
<b>Estrutura Atual:</b> 12 módulos integrados &bull; 15 serviços AWS cobertos &bull; Security AI &bull; Kali Linux SOC &bull; Executive Dashboard
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. SECURITY AI COMMAND CENTER
# ==========================================
st.subheader("Security AI Command Center")

ai1, ai2, ai3, ai4, ai5, ai6 = st.columns(6)
ai1.metric("AI Status", "Online")
ai2.metric("AI Modules", "12")
ai3.metric("Prompt Library", "20+")
ai4.metric("Threat Models", "50+")
ai5.metric("IOC Database", "15K")
ai6.metric("Correlations", "3.2K")

st.markdown("""
<div style="
background:#1E293B;
padding:25px;
border-radius:20px;
border-left:6px solid #2563EB;
margin-top:20px;
">

<h3 style="color:white; margin-top:0;">
Artificial Intelligence Security Engine
</h3>

<p style="
color:#CBD5E1;
font-size:16px;
line-height:1.8;
margin-bottom:0;
">
O Security AI Engine atua como o núcleo de inteligência da plataforma.
<br><br>
<b>Responsabilidades:</b><br>
&bull; Análise de Segurança &nbsp;&bull;&nbsp; Threat Intelligence &nbsp;&bull;&nbsp; Compliance Analysis &nbsp;&bull;&nbsp; IAM Governance &nbsp;&bull;&nbsp; Executive Insights<br>
&bull; Audit Intelligence &nbsp;&bull;&nbsp; Risk Prioritization &nbsp;&bull;&nbsp; Security Correlation &nbsp;&bull;&nbsp; IOC Analysis &nbsp;&bull;&nbsp; Executive Reporting
</p>

</div>
""", unsafe_allow_html=True)

# Capacidades de IA
st.subheader("AI Capabilities")
cap1, cap2, cap3, cap4 = st.columns(4)
cap1.metric("Security Analysis", "Active")
cap2.metric("Threat Correlation", "Active")
cap3.metric("Compliance Insights", "Active")
cap4.metric("Executive Reporting", "Active")

# Integração da IA
st.subheader("Security AI Integration")
integration_df = pd.DataFrame({
    "Module": [
        "Executive Dashboard", "Security Hub", "Threat Intelligence",
        "IAM Security", "EC2 Security", "Compliance Center", "Audit History"
    ],
    "AI Support": [
        "Enabled", "Enabled", "Enabled", "Enabled", "Enabled", "Enabled", "Enabled"
    ]
})
st.dataframe(integration_df, use_container_width=True, hide_index=True)

# Mini Copilot na Home
st.subheader("Security AI Assistant")
question = st.text_input("Pergunte algo sobre a plataforma")
if st.button("Analyze"):
    if question:
        st.success(f"""
        Resumo Executivo
        
        Pergunta:
        {question}
        
        A Security AI identificou que a plataforma possui módulos integrados de Security Hub, Threat Intelligence, IAM Security, Compliance e Executive Analytics.
        """)

st.markdown("---")

# ==========================================
# 8. SOBRE O AUTOR
# ==========================================
st.subheader("Sobre o Autor")

col_foto, col_texto = st.columns([1, 3], gap="large")

with col_foto:
    st.markdown("""
    <div style="
        background:#1E293B;
        padding:15px;
        border-radius:20px;
        border:1px solid #2563EB;
        text-align: center;
    ">
    """, unsafe_allow_html=True)
    
    try:
        st.image("foto_danilo.jpg", use_container_width=True)
    except Exception:
        st.info("Insira 'foto_danilo.jpg' na raiz para exibir sua foto.")
        
    st.markdown("""
    </div>
    <div style="text-align:center; margin-top:12px;">
        <h3 style="margin:0; font-size: 18px; color: #FFFFFF;">Danilo Rafael da Silva Costa</h3>
        <p style="color:#94A3B8; margin:0; font-size: 13px;">Cloud Security & Governance</p>
    </div>
    """, unsafe_allow_html=True)

with col_texto:
    st.markdown("""
    <div style="
        background: #1E293B;
        padding: 25px;
        border-radius: 20px;
        border-left: 6px solid #3B82F6;
    ">
        <h3 style="color: #FFFFFF; margin-top: 0;">Formação</h3>
        <p style="color: #CBD5E1; font-size: 15px; line-height: 1.6; margin-bottom: 15px;">
            • Defesa Cibernética - FIAP<br>
            • MBA em Gestão de Projetos<br>
            • Administração
        </p>
        <h3 style="color: #FFFFFF; margin-top: 10px;">Especialidades</h3>
        <p style="color: #CBD5E1; font-size: 15px; line-height: 1.6; margin-bottom: 15px;">
            • Cloud Security &nbsp;|&nbsp; • AWS Governance &nbsp;|&nbsp; • Threat Intelligence &nbsp;|&nbsp; • Compliance &nbsp;|&nbsp; • Security Operations &nbsp;|&nbsp; • Executive Security Analytics
        </p>
        <p style="color: #94A3B8; font-size: 14px; line-height: 1.5; margin: 0; font-style: italic;">
            Projeto desenvolvido com foco em segurança corporativa, governança, automação e proteção de ambientes AWS.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 9. PLATFORM STATISTICS
# ==========================================
st.subheader("Platform Statistics")

a1, a2, a3, a4, a5 = st.columns(5)
a1.metric("Ativos Monitorados", "1.240")
a2.metric("Findings", "127")
a3.metric("Controles", "397")
a4.metric("Serviços AWS", "15")
a5.metric("Módulos", "12")

st.markdown("---")

# ==========================================
# 10. SECURITY OPERATIONS DASHBOARD
# ==========================================
st.subheader("Security Operations Dashboard")

soc1, soc2, soc3, soc4, soc5 = st.columns(5)
soc1.metric("Critical Findings", "12")
soc2.metric("Threat Feeds", "24")
soc3.metric("Open Risks", "18")
soc4.metric("Protected Assets", "1.240")
soc5.metric("Compliance Controls", "397")

st.markdown("---")

# ==========================================
# 11. KALI LINUX SECURITY OPERATIONS CENTER
# ==========================================
st.subheader("Kali Linux Security Operations Center")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Security Tools", "600+")
k2.metric("Threat Hunting", "Active")
k3.metric("Blue Team", "Online")
k4.metric("Red Team", "Ready")

st.markdown("""
<div style="
background: #1E293B;
padding: 20px;
border-radius: 15px;
border: 1px solid #334155;
margin-top: 15px;
">
<p style="color: #E2E8F0; font-size: 15px; line-height: 1.6; margin:0;">
<b>Capacidades operacionais:</b> Threat Hunting &nbsp;&bull;&nbsp; Vulnerability Assessment &nbsp;&bull;&nbsp; Incident Response &nbsp;&bull;&nbsp; Digital Forensics &nbsp;&bull;&nbsp; Security Research &nbsp;&bull;&nbsp; Red Team Operations &nbsp;&bull;&nbsp; Blue Team Operations
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 12. PLATFORM ECOSYSTEM
# ==========================================
st.subheader("Platform Ecosystem & Modules")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**Executive Dashboard**\nVisão Executiva da Segurança")
    st.info("**Security Hub**\nCentralização de Findings")
    st.info("**Compliance Center**\nGovernança e Risco")

with col2:
    st.info("**Executive View**\nMétricas e KPIs de Alto Nível")
    st.info("**Security Copilot**\nAssistente de Resposta Inteligente")
    st.info("**Audit History**\nTrilha de Auditoria e Logs")

with col3:
    st.info("**Security Center**\nCentral de Operações em Nuvem")
    st.info("**Threat Intelligence**\nAnálise e Correlação de Ameaças")
    st.info("**Security AI Engine**\nMotor Inteligente e Insights")

with col4:
    st.info("**IAM Security**\nGovernança de Identidades e Acessos")
    st.info("**EC2 Security**\nHardening e Instâncias")
    st.info("**Prompt Engine**\nBiblioteca de Prompts")

st.markdown("---")

# ==========================================
# 13. PLATFORM ARCHITECTURE
# ==========================================
st.subheader("Platform Architecture Map")

st.code("""
HOME (AWS Cyber Defense Platform)
├── Executive Dashboard
├── Executive View
├── Security Center
├── Security Hub
├── Security Copilot
├── Threat Intelligence
├── IAM Security
├── EC2 Security
├── Compliance Center
├── Audit History
└── Security AI Engine
""", language="text")

st.markdown("---")

# ==========================================
# 14. AWS COVERAGE (EM CARDS VISUAIS)
# ==========================================
st.subheader("AWS Coverage")

c1, c2, c3, c4, c5 = st.columns(5)
c1.success("IAM (100%)")
c2.success("EC2 (100%)")
c3.success("S3 (100%)")
c4.success("Lambda (100%)")
c5.success("GuardDuty (100%)")

c6, c7, c8, c9, c10 = st.columns(5)
c6.success("Security Hub (100%)")
c7.success("CloudTrail (100%)")
c8.success("Config (100%)")
c9.success("Inspector (100%)")
c10.success("Macie (100%)")

c11, c12, c13, c14, c15 = st.columns(5)
c11.success("WAF (100%)")
c12.success("CloudWatch (100%)")
c13.success("KMS (100%)")
c14.success("VPC (100%)")
c15.success("RDS (100%)")

st.markdown("---")

# ==========================================
# 15. NAVIGATION CENTER
# ==========================================
st.subheader("Navigation Center")

n1, n2, n3, n4 = st.columns(4)

with n1:
    if hasattr(st, "page_link"):
        st.page_link("pages/executive_dashboard.py", label="Executive Dashboard")
    else:
        st.write("Executive Dashboard")

with n2:
    if hasattr(st, "page_link"):
        st.page_link("pages/security_hub.py", label="Security Hub")
    else:
        st.write("Security Hub")

with n3:
    if hasattr(st, "page_link"):
        st.page_link("pages/threat_intelligence.py", label="Threat Intelligence")
    else:
        st.write("Threat Intelligence")

with n4:
    if hasattr(st, "page_link"):
        st.page_link("pages/compliance.py", label="Compliance Center")
    else:
        st.write("Compliance Center")

st.markdown("---")

# ==========================================
# 16. RODAPÉ CORPORATIVO
# ==========================================
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 25px; border-top: 1px solid #334155;">
    <h4 style="color: #FFFFFF !important; margin-bottom: 5px;">AWS Cyber Defense Platform</h4>
    <p style="color: #94A3B8 !important; font-size: 14px; margin: 0 0 10px 0; font-weight: 600;">Enterprise Cloud Security Platform</p>
    <p style="color: #64748B !important; font-size: 12px; margin: 0 0 12px 0; line-height: 1.6;">
        Threat Intelligence &bull; Governance Risk & Compliance &bull; Cloud Security &bull; Security Operations &bull; Artificial Intelligence
    </p>
    <p style="color: #93C5FD !important; font-size: 13px; margin: 0; font-weight: 500;">
        Powered by Kali Linux Security Operations Center
    </p>
</div>
""", unsafe_allow_html=True)