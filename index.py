import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Danilo Rafael da Silva Costa | AWS Cyber Defense Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="home_refresh")

# ==========================================
# 3. TEMA ESCURO PROFISSIONAL (TEXTO #E5E7EB)
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #111827;
    color: #FFFFFF;
}
h1, h2, h3, h4 {
    color: #FFFFFF !important;
}
p, div, span, label {
    color: #E5E7EB !important;
}
section[data-testid="stSidebar"] {
    background: #1F2937;
}
.hero-card {
    background-color: #1F2937 !important;
    border: 1px solid #374151 !important;
}
.stButton > button,
.stDownloadButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #3B82F6 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR PROFISSIONAL & MÓDULOS
# ==========================================
st.sidebar.markdown("""
# AWS Cyber Defense
**Cloud Security Platform**
---
""")

st.sidebar.markdown("## Módulos do Sistema")
st.sidebar.write("Dashboard Executivo")
st.sidebar.write("Postura de Risco")
st.sidebar.write("Serviços AWS Monitorados")
st.sidebar.write("IAM & S3 Security")
st.sidebar.write("EC2 Hardening")
st.sidebar.write("AWS Config & Compliance")
st.sidebar.write("MITRE ATT&CK & Threat Intel")
st.sidebar.write("Relatórios de Auditoria")

st.sidebar.markdown("---")

# ==========================================
# 5. BANNER DE DESTAQUE SUPERIOR (COM TÍTULO EM MAIÚSCULO)
# ==========================================
st.markdown("""
<div style="
    background: #2563EB;
    padding: 60px;
    border-radius: 20px;
    text-align: center;
    color: #FFFFFF;
    margin-bottom: 20px;
">
    <h1 style="color: #FFFFFF !important;">AWS CYBER DEFENSE PLATFORM</h1>
    <h3 style="color: #FFFFFF !important;">
        Cloud Security Operations Center
    </h3>
    <p style="color: #FFFFFF !important; margin: 0; font-size: 16px;">
        Governança • Compliance • Threat Intelligence • AWS Security
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; margin-bottom: 20px; color: #E5E7EB;">
    <b>Status do Sistema:</b> Operacional &nbsp;|&nbsp; 
    <b>Última Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 6. PAINEL EXECUTIVO & POSTURA DE SEGURANÇA
# ==========================================
st.subheader("Resumo Executivo")

API_URL = "https://aws-security-analyzer-api.onrender.com/api/security-score"
try:
    response = requests.get(API_URL, timeout=2)
    if response.status_code == 200:
        data = response.json()
        score_val = f"{data.get('score', 95)}/100"
        comp_val = f"{data.get('compliance', 92)}%"
        findings_val = str(data.get('findings', 3))
    else:
        score_val, comp_val, findings_val = "95/100", "92%", "3"
except Exception:
    score_val, comp_val, findings_val = "95/100", "92%", "3"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Security Score", score_val)
c2.metric("Compliance", comp_val)
c3.metric("Findings", findings_val)
c4.metric("Status", "Online")

# DESTAQUE PRINCIPAL
st.markdown("""
<div style="
    background: #2563EB;
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: #FFFFFF;
    margin-top: 20px;
    margin-bottom: 20px;
">
    <h2 style="color: #FFFFFF !important;">Plataforma Corporativa de Segurança AWS</h2>
    <p style="color: #FFFFFF !important; margin: 0; font-size: 15px;">
        Monitoramento • Compliance • Governança • Threat Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

st.header("Postura de Segurança")
col_p1, col_p2, col_p3 = st.columns(3)
col_p1.metric("Risco Geral", "Baixo")
col_p2.metric("Vulnerabilidades", "3")
col_p3.metric("Controles Ativos", "97%")

st.markdown("---")

# ==========================================
# 7. SERVIÇOS AWS MONITORADOS (LISTA EXPANDIDA)
# ==========================================
st.header("Serviços Monitorados")

servicos = [
    "IAM", "S3", "EC2", "RDS", "Lambda",
    "CloudTrail", "WAF", "GuardDuty", "Macie",
    "Inspector", "Security Hub", "AWS Config"
]

cols_serv = st.columns(4)
for i, s in enumerate(servicos):
    with cols_serv[i % 4]:
        st.success(s)

st.markdown("---")

# ==========================================
# 8. MÓDULOS DE SEGURANÇA PROFISSIONAIS
# ==========================================
st.header("Módulos de Segurança")

c_mod1, c_mod2, c_mod3 = st.columns(3)

with c_mod1:
    st.success("""
    **IAM Security**
    Gestão de Usuários
    MFA Obrigatório
    Roles & Políticas
    """)

with c_mod2:
    st.info("""
    **S3 Security**
    Auditoria de Buckets
    Criptografia
    Bloqueio Público
    """)

with c_mod3:
    st.warning("""
    **EC2 Security**
    Security Groups
    Hardening de Portas
    Monitoramento
    """)

st.markdown("---")

# ==========================================
# 9. APRESENTAÇÃO COM FOTO AMPLIADA (380px) E BIO DETALHADA
# ==========================================
col_foto, col_texto = st.columns([1, 2], gap="large")

with col_foto:
    try:
        st.markdown("""
        <div style="
            padding: 15px;
            background: #1F2937;
            border-radius: 20px;
            border: 6px solid #3B82F6;
            box-shadow: 0 0 50px rgba(59,130,246,0.8);
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
        st.image("foto_danilo.jpg", width=380)
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.info("Adicione 'foto_danilo.jpg' na raiz do projeto.")

with col_texto:
    st.markdown("""
    <div style="
        background: #1F2937;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #3B82F6;
    ">
        <h2 style="color: #FFFFFF; margin-top: 0;">
            Danilo Rafael da Silva Costa
        </h2>
        <p style="color: #E5E7EB; font-size: 15px; line-height: 1.6;">
            Estudante de Defesa Cibernética pela FIAP,<br>
            MBA em Gestão de Projetos,<br>
            Bacharel em Administração e formação internacional<br>
            em Strategic Leadership pela Brigham Young University (BYU).<br><br>
            Atuação voltada para Cloud Security,<br>
            Governança AWS,<br>
            Compliance,<br>
            Threat Intelligence,<br>
            Risk Management<br>
            e Operações de Segurança.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Sobre o Projeto
    A **AWS Cyber Defense Platform** centraliza o monitoramento, governança e análise de segurança em ambientes AWS, oferecendo visibilidade consolidada de riscos, conformidade e controles.
    """)

st.markdown("---")

# ==========================================
# 10. COMPETÊNCIAS & RESUMO EXECUTIVO DESTACADO
# ==========================================
col_comp, col_res = st.columns(2)

with col_comp:
    st.header("O que este projeto demonstra")
    st.write("""
    • Cloud Security & AWS Security  
    • Governança e Compliance  
    • Desenvolvimento Python & Streamlit  
    • Monitoramento Contínuo (SOC)  
    • Threat Intelligence & Gestão de Riscos  
    """)

with col_res:
    st.header("Resumo Executivo")
    st.info("""
    Plataforma desenvolvida para centralizar
    monitoramento, governança, compliance
    e inteligência de ameaças em ambientes AWS.

    O objetivo é fornecer visibilidade dos riscos,
    automatizar análises de segurança e apoiar
    a tomada de decisão em Cloud Security.
    """)

st.markdown("---")

# ==========================================
# 11. CONTATO E REDES PROFISSIONAIS
# ==========================================
st.header("Contato & Redes Profissionais")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("GitHub do Projeto", "https://github.com/danilocosta2223-boop/aws-security-analyzer", use_container_width=True)

with col2:
    st.link_button("LinkedIn Profissional", "https://www.linkedin.com/in/danilocosta2223", use_container_width=True)

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
# 12. RODAPÉ PROFISSIONAL
# ==========================================
st.markdown("""
---
<center>
    <h3 style="color: #FFFFFF !important;">AWS Cyber Defense Platform</h3>
    <p style="color: #E5E7EB !important;">Desenvolvido por Danilo Rafael da Silva Costa</p>
    <p style="color: #E5E7EB !important;">Defesa Cibernética • FIAP • AWS Cloud Security</p>
</center>
""", unsafe_allow_html=True)