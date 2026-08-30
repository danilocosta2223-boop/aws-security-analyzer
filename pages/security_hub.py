import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="AWS Security Hub | Enterprise Security Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================
st_autorefresh(interval=15000, key="security_hub_refresh")

# ==========================
# 3. ESTILO CSS CORPORATIVO (RAW HTML)
# ==========================
st.markdown("""
<style>
    .stApp {
        background: #111827;
        color: #E5E7EB;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1F2937;
    }
    
    .hero-card {
        background: #1F2937;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background-color: #374151;
        color: #93c5fd;
        border: 1px solid #4b5563;
    }

    h1, h2, h3, h4 {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# 4. CONSUMO E CACHE DAS APIS DO BACKEND
# ==========================
@st.cache_data(ttl=10)
def carregar_dados_hub():
    score = requests.get("http://127.0.0.1:3000/api/security-score").json()
    iam = requests.get("http://127.0.0.1:3000/api/iam").json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3").json()
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2").json()
    return score, iam, s3, ec2

try:
    score_data, iam_data, s3_data, ec2_data = carregar_dados_hub()
    backend_online = True
except Exception:
    backend_online = False
    st.error("Backend indisponível. Certifique-se de que o servidor Node.js está em execução na porta 3000.")
    st.stop()

# ==========================
# 5. CÁLCULOS DINÂMICOS DE FINDINGS
# ==========================
mfa_off = iam_data.get("mfaDisabled", 0)
public_buckets = s3_data.get("publicBuckets", 0)
open_sg = ec2_data.get("openSecurityGroups", 0)

total_findings = mfa_off + public_buckets + open_sg + 2

# ==========================
# 6. CABEÇALHO DO MÓDULO (RAW HTML)
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>AWS Security Hub & Enterprise Threat Center</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Plataforma unificada de postura de segurança em nuvem (CSPM), correlação cross-module e gestão de incidentes SOC.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status do Servidor Hub:</b> Operacional (AWS Multi-Region) | 
    <b>Última varredura:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |
    <b>Total de Alertas Ativos:</b> {total_findings}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# 7. EXECUTIVE SECURITY DASHBOARD
# ==========================
st.subheader("Executive Security Dashboard")
e1, e2, e3, e4 = st.columns(4)
hub_score = max(100 - (total_findings * 3), 60)
e1.metric("Risk Score", hub_score)
e2.metric("Findings", total_findings)
e3.metric("Assets", 96)
e4.metric("Cobertura", "97%")

st.markdown("---")

# ==========================
# 8. CROSS-PLATFORM CORRELATION
# ==========================
st.subheader("Cross-Platform Correlation")
correlation = pd.DataFrame({
    "Módulo": [
        "IAM Audit",
        "S3 Audit",
        "Compliance",
        "CloudTrail",
        "CloudWatch"
    ],
    "Achados": [
        3,
        2,
        4,
        1,
        0
    ],
    "Status": [
        "Aberto",
        "Aberto",
        "Em Análise",
        "Mitigado",
        "Normal"
    ]
})
st.dataframe(correlation, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================
# 9. SECURITY HUB SCORE & HEALTH
# ==========================
st.subheader("Security Hub Score & Health")
st.progress(hub_score / 100)
st.success(f"Score Consolidado: {hub_score}%")

health = 96
st.progress(health / 100)
st.success(f"Saúde Geral do Hub: {health}%")

st.markdown("---")

# ==========================
# 10. RECURSOS MONITORADOS & SEVERITY METRICS
# ==========================
st.subheader("Recursos Monitorados")
r1, r2, r3, r4 = st.columns(4)
r1.metric("IAM", "42")
r2.metric("S3", "18")
r3.metric("EC2", "12")
r4.metric("Roles", "24")

st.markdown("---")

st.subheader("Findings por Severidade")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Critical", 2)
s2.metric("High", 4)
s3.metric("Medium", 3)
s4.metric("Low", 1)

st.markdown("---")

# ==========================
# 11. WORKFLOW DE TRATAMENTO & RESPONSÁVEIS
# ==========================
col_w1, col_w2 = st.columns(2)

with col_w1:
    st.subheader("Workflow de Tratamento")
    workflow = pd.DataFrame({
        "Finding": [
            "Bucket Público",
            "IAM sem MFA",
            "Security Group"
        ],
        "Status": [
            "Novo",
            "Em Tratamento",
            "Resolvido"
        ]
    })
    st.dataframe(workflow, use_container_width=True, hide_index=True)

with col_w2:
    st.subheader("Responsáveis")
    owners = pd.DataFrame({
        "Achado": [
            "IAM",
            "S3",
            "EC2"
        ],
        "Responsável": [
            "Equipe IAM",
            "Equipe Cloud",
            "SOC"
        ]
    })
    st.dataframe(owners, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================
# 12. THREAT INVESTIGATION LAB & SIMULAÇÃO DE INCIDENTE
# ==========================
col_i1, col_i2 = st.columns(2)

with col_i1:
    st.subheader("Threat Investigation Lab")
    ioc = st.text_input("Digite um IOC")
    if st.button("Investigar IOC"):
        st.success(f"Investigação iniciada para {ioc}")
        st.info("IOC localizado em eventos simulados.")

with col_i2:
    st.subheader("Incident Simulation")
    incidente = st.selectbox(
        "Cenário",
        [
            "Credential Theft",
            "Data Exfiltration",
            "Ransomware",
            "Crypto Mining"
        ]
    )
    if st.button("Executar Incidente"):
        st.error(f"Incidente {incidente} detectado.")
        st.info("Playbook SOAR iniciado.")

st.markdown("---")

# ==========================
# 13. SOC OPERATIONS & COVERAGE MAP
# ==========================
col_soc1, col_soc2 = st.columns(2)

with col_soc1:
    st.subheader("SOC Operations")
    soc1, soc2, soc3 = st.columns(3)
    soc1.metric("MTTD", "12 min")
    soc2.metric("MTTR", "31 min")
    soc3.metric("Incidentes", "7")

with col_soc2:
    st.subheader("Coverage Map")
    coverage_df = pd.DataFrame({
        "Serviço": ["IAM", "S3", "EC2", "CloudTrail", "Config"],
        "Cobertura": ["100%", "95%", "92%", "100%", "100%"]
    })
    st.dataframe(coverage_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================
# 14. AWS SECURITY LEARNING (PORTFÓLIO & CERTIFICAÇÃO)
# ==========================
st.subheader("AWS Security Learning")
pergunta_cert = st.radio(
    "Qual serviço AWS atua centralizando achados de segurança de múltiplos serviços (GuardDuty, Inspector, Macie)?",
    [
        "GuardDuty",
        "Security Hub",
        "CloudWatch",
        "IAM Access Analyzer"
    ]
)

if st.button("Validar Conhecimento de Certificação"):
    if pergunta_cert == "Security Hub":
        st.success("Correto! O AWS Security Hub é o agregador central para postura e conformidade em nuvem.")
    else:
        st.error("Incorreto. Revise os conceitos do AWS Security Hub para exames de certificação de segurança.")

st.markdown("---")

# ==========================
# 15. INTEGRAÇÃO COM A PLATAFORMA
# ==========================
st.subheader("Navegação Integrada")
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1:
    st.page_link("pages/security_center.py", label="Security Center")
with c2:
    st.page_link("pages/compliance.py", label="Compliance")
with c3:
    st.page_link("pages/s3_audit.py", label="S3 Audit")
with c4:
    st.page_link("pages/iam_audit.py", label="IAM Audit")
with c5:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")
with c6:
    st.page_link("pages/cloudwatch.py", label="CloudWatch")
with c7:
    st.page_link("pages/pdf_reports.py", label="PDF Reports")

# ==========================
# RODAPÉ DA PÁGINA
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Enterprise Security Hub • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")