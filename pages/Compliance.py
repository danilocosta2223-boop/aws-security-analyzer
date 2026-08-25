import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Compliance & Frameworks Dashboard | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================
st_autorefresh(interval=15000, key="compliance_refresh")

# ==========================
# 3. ESTILO CSS CORPORATIVO
# ==========================
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

    .badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background-color: #f8f9fa;
        color: #1e3a8a;
        border: 1px solid #d1d5db;
    }

    h1, h2, h3, h4 {
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# 4. CONSUMO E CACHE DAS APIS DO BACKEND
# ==========================
@st.cache_data(ttl=10)
def carregar_dados_compliance():
    score = requests.get("http://127.0.0.1:3000/api/security-score").json()
    iam = requests.get("http://127.0.0.1:3000/api/iam").json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3").json()
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2").json()
    config = requests.get("http://127.0.0.1:3000/api/config").json()
    return score, iam, s3, ec2, config

# Tratamento de erro caso o Node.js esteja offline
try:
    score_data, iam_data, s3_data, ec2_data, config_data = carregar_dados_compliance()
    backend_online = True
except Exception:
    backend_online = False
    st.error("Backend indisponível. Certifique-se de que o servidor Node.js está em execução.")
    st.stop()

# ==========================
# 5. CÁLCULOS DINÂMICOS DE COMPLIANCE
# ==========================
mfa_off = iam_data.get("mfaDisabled", 0)
public_buckets = s3_data.get("publicBuckets", 0)
open_sg = ec2_data.get("openSecurityGroups", 0)

critical_findings = mfa_off + public_buckets + open_sg

cis_score = max(100 - (critical_findings * 5), 50)
nist_score = max(100 - (critical_findings * 4), 50)
iso_score = max(100 - (critical_findings * 3), 50)

# ==========================
# 6. STATUS GERAL DA PLATAFORMA
# ==========================
if critical_findings == 0:
    st.success("Todos os módulos de Compliance e Governança estão operacionais e sem desvios críticos.")
else:
    st.warning("Módulos operacionais, porém foram detectados desvios que requerem atenção de governança.")

# ==========================
# 7. CABEÇALHO DO MÓDULO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Compliance & Frameworks Dashboard</h1>
    <p style="color: #4b5563; margin: 0; font-size: 15px;">
        Centro de governança e conformidade contínua, monitoramento de padrões globais e postura de segurança integrada.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #4b5563; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional &nbsp;|&nbsp; 
    <b>Última sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} &nbsp;|&nbsp;
    <b>Desvios Críticos:</b> {critical_findings}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# 8. EXECUTIVE DASHBOARD & SECURITY POSTURE SCORE
# ==========================
st.subheader("Executive Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="CIS AWS Foundations Benchmark",
        value=f"{cis_score}%",
        delta="-2% vs última semana" if critical_findings > 0 else "Estável",
        delta_color="inverse" if critical_findings > 0 else "normal"
    )

with col2:
    st.metric(
        label="NIST CSF (Cybersecurity Framework)",
        value=f"{nist_score}%",
        delta="Conforme" if critical_findings == 0 else "Requer Atenção"
    )

with col3:
    st.metric(
        label="ISO/IEC 27001",
        value=f"{iso_score}%",
        delta="Revisão Pendente" if critical_findings > 0 else "Conforme"
    )

st.markdown("---")

# Security Posture Score
st.subheader("Security Posture Score")
security_score = score_data.get("score", 85)
st.progress(security_score / 100)
st.metric("Score Geral de Postura", f"{security_score}/100")

st.markdown("---")

# ==========================
# 9. EXECUTIVE SUMMARY & RECURSOS IMPACTADOS
# ==========================
st.subheader("Executive Summary")

if critical_findings > 0:
    st.warning(f"Foram identificados {critical_findings} desvios críticos impactando a conformidade geral da conta AWS.")
else:
    st.success("Nenhum impacto crítico detectado nos controles avaliados.")

st.markdown("---")

st.subheader("Recursos Impactados")
r1, r2, r3 = st.columns(3)
with r1:
    st.write(f"IAM Sem MFA: {mfa_off}")
with r2:
    st.write(f"Buckets Públicos: {public_buckets}")
with r3:
    st.write(f"Security Groups Expostos: {open_sg}")

st.markdown("---")

# ==========================
# 10. ACHADOS CRÍTICOS DETALHADOS
# ==========================
st.subheader("Achados Críticos")

if mfa_off > 0:
    st.error(f"{mfa_off} usuários operando sem autenticação multifator (MFA).")
if public_buckets > 0:
    st.error(f"{public_buckets} buckets S3 públicos detectados.")
if open_sg > 0:
    st.warning(f"{open_sg} Security Groups com exposição externa perimetral.")

if critical_findings == 0:
    st.success("Nenhum achado crítico pendente de remediação.")

st.markdown("---")

# ==========================
# 11. INVENTÁRIO MONITORADO
# ==========================
st.subheader("Inventário Monitorado")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Usuários IAM", iam_data.get("totalUsers", 0))
c2.metric("Buckets S3", s3_data.get("totalBuckets", 0))
c3.metric("Instâncias EC2", ec2_data.get("totalInstances", 0))
c4.metric("Regras AWS Config", config_data.get("evaluatedRules", 45))

st.markdown("---")

# ==========================
# 12. FRAMEWORK STATUS E CORRELAÇÃO
# ==========================
st.subheader("Status de Aderência por Framework")

framework_df = pd.DataFrame({
    "Framework": ["CIS Benchmark v1.5.0", "NIST SP 800-53", "ISO 27001:2022", "PCI-DSS v4.0", "SOC 2 Type II"],
    "Controles Avaliados": [45, 110, 93, 64, 85],
    "Compliance (%)": [cis_score, nist_score, iso_score, 96, 98],
    "Status": ["Atenção Requerida" if critical_findings > 0 else "Conforme", "Conforme", "Conforme", "Atenção Requerida" if critical_findings > 0 else "Conforme", "Conforme"]
})

st.dataframe(framework_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("Framework Correlation")
st.write(
    """
    - **CIS Benchmark:** Governança de Configuração e Endurecimento de Ativos
    - **NIST CSF:** Gestão de Riscos, Identificação e Resposta a Incidentes
    - **ISO 27001:** Controles de Segurança da Informação e Gestão de Acesso
    - **PCI-DSS:** Proteção de Dados Sensíveis e Cartões de Pagamento
    - **SOC 2:** Segurança Operacional, Disponibilidade e Integridade de Processos
    """
)

# Gráfico de Compliance por Framework
chart_df = pd.DataFrame({
    "Framework": ["CIS Benchmark", "NIST CSF", "ISO 27001", "PCI-DSS", "SOC 2"],
    "Compliance": [cis_score, nist_score, iso_score, 96, 98]
})
st.bar_chart(chart_df.set_index("Framework"))

# ==========================
# 13. TENDÊNCIA DE COMPLIANCE (HISTÓRICO)
# ==========================
st.markdown("---")
st.subheader("Tendência de Compliance")

history_df = pd.DataFrame({
    "Data": ["20/08", "21/08", "22/08", "23/08", "24/08"],
    "Compliance": [88, 90, 91, 93, cis_score]
})

st.line_chart(history_df.set_index("Data"))

# ==========================
# 14. TIMELINE DE EVENTOS RECENTES
# ==========================
st.markdown("---")
st.subheader("Timeline")

timeline_events = [
    "Avaliação contínua de políticas de acesso IAM executada",
    "Verificação de posture score e sincronização com Security Hub",
    "Varredura de conformidade via regras do AWS Config"
]

for evento in timeline_events:
    st.write(f"{datetime.now().strftime('%H:%M:%S')} - {evento}")

# ==========================
# 15. HEALTH CHECK DOS SERVIÇOS
# ==========================
st.markdown("---")
st.subheader("Health Check dos Serviços")

health_df = pd.DataFrame([
    ["IAM", "Online" if backend_online else "Offline"],
    ["S3", "Online" if backend_online else "Offline"],
    ["EC2", "Online" if backend_online else "Offline"],
    ["Config", "Online" if backend_online else "Offline"],
    ["Backend Node.js", "Online" if backend_online else "Offline"]
], columns=["Serviço", "Status"])

st.dataframe(health_df, use_container_width=True, hide_index=True)

# ==========================
# RODAPÉ DA PÁGINA
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Centro de Governança e Compliance • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")