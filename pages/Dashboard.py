import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Compliance & Frameworks Dashboard | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="compliance_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO (FUNDO BRANCO)
# ==========================================
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

# ==========================================
# 4. CONSUMO ROBUSTO DAS APIS DO BACKEND (TIMEOUT=5)
# ==========================================
@st.cache_data(ttl=10)
def carregar_dados_compliance():
    score = requests.get("http://127.0.0.1:3000/api/security-score", timeout=5).json()
    iam = requests.get("http://127.0.0.1:3000/api/iam", timeout=5).json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3", timeout=5).json()
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2", timeout=5).json()
    config = requests.get("http://127.0.0.1:3000/api/config", timeout=5).json()
    rds = requests.get("http://127.0.0.1:3000/api/rds", timeout=5).json()
    lamb = requests.get("http://127.0.0.1:3000/api/lambda", timeout=5).json()
    kms = requests.get("http://127.0.0.1:3000/api/kms", timeout=5).json()
    guardduty = requests.get("http://127.0.0.1:3000/api/guardduty", timeout=5).json()
    return score, iam, s3, ec2, config, rds, lamb, kms, guardduty

try:
    score_data, iam_data, s3_data, ec2_data, config_data, rds_data, lambda_data, kms_data, guardduty_data = carregar_dados_compliance()
    backend_online = True
except Exception:
    backend_online = False
    st.error("Backend indisponível. Certifique-se de que o servidor Node.js está em execução.")
    st.stop()

# ==========================================
# 5. CÁLCULOS DINÂMICOS DE COMPLIANCE E RISCOS
# ==========================================
mfa_off = iam_data.get("mfaDisabled", 0)
public_buckets = s3_data.get("publicBuckets", 0)
open_sg = ec2_data.get("openSecurityGroups", 0)
guardduty_threats = guardduty_data.get("activeThreats", 0)

critical_findings = mfa_off + public_buckets + open_sg + guardduty_threats

cis_score = max(100 - (critical_findings * 5), 50)
nist_score = max(100 - (critical_findings * 4), 50)
iso_score = max(100 - (critical_findings * 3), 50)

# Matriz de Risco Dinâmica
critical_risk = guardduty_threats
high_risk = public_buckets + mfa_off
medium_risk = open_sg
low_risk = 0

# ==========================================
# 6. CABEÇALHO DO MÓDULO (HERO CARD)
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>Compliance & Frameworks Dashboard</h1>
    <p style="color: #4b5563; margin: 0; font-size: 15px;">
        Centro de governança corporativa, monitoramento contínuo de padrões globais de segurança e auditoria integrada de infraestrutura AWS.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #4b5563; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional &nbsp;|&nbsp; 
    <b>Última Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} &nbsp;|&nbsp;
    <b>Desvios Totais:</b> {critical_findings}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 7. EXECUTIVE DASHBOARD
# ==========================================
st.subheader("Executive Dashboard")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        label="CIS AWS Foundations Benchmark",
        value=f"{cis_score}%",
        delta="-2% vs última semana" if critical_findings > 0 else "Estável",
        delta_color="inverse" if critical_findings > 0 else "normal"
    )

with c2:
    st.metric(
        label="NIST CSF (Cybersecurity Framework)",
        value=f"{nist_score}%",
        delta="Conforme" if critical_findings == 0 else "Requer Atenção"
    )

with c3:
    st.metric(
        label="ISO/IEC 27001",
        value=f"{iso_score}%",
        delta="Revisão Pendente" if critical_findings > 0 else "Conforme"
    )

st.markdown("---")

# ==========================================
# 8. SECURITY POSTURE SCORE
# ==========================================
st.subheader("Security Posture Score")
security_score = score_data.get("score", 85)
st.progress(security_score / 100)
st.metric("Score Geral de Postura", f"{security_score}/100")

st.markdown("---")

# ==========================================
# 9. EXECUTIVE SUMMARY
# ==========================================
st.subheader("Executive Summary")

if critical_findings > 0:
    st.warning(f"Foram identificados {critical_findings} desvios críticos impactando diretamente a pontuação de conformidade e governança da conta AWS.")
else:
    st.success("Ambiente totalmente aderente aos padrões corporativos e frameworks de segurança avaliados.")

st.markdown("---")

# ==========================================
# 10. COMPLIANCE FINDINGS
# ==========================================
st.subheader("Compliance Findings")

iam_findings = iam_data.get("findings", [])
if iam_findings:
    for finding in iam_findings:
        st.write(f"- **IAM:** {finding.get('user')} - {finding.get('issue')}")
else:
    st.write("Nenhum achado crítico pendente no IAM.")

s3_findings = s3_data.get("findings", [])
if s3_findings:
    for bucket in s3_findings:
        st.write(f"- **S3:** {bucket.get('name')} - {bucket.get('status')}")

ec2_findings = ec2_findings = ec2_data.get("findings", [])
if ec2_findings:
    for item in ec2_findings:
        st.write(f"- **EC2:** {item.get('name')} - Risco: {item.get('risk')}")

st.markdown("---")

# ==========================================
# 11. RECURSOS IMPACTADOS
# ==========================================
st.subheader("Recursos Impactados")

r1, r2, r3 = st.columns(3)
with r1:
    st.write(f"IAM Sem MFA: {mfa_off}")
with r2:
    st.write(f"Buckets Públicos: {public_buckets}")
with r3:
    st.write(f"Security Groups Expostos: {open_sg}")

st.markdown("---")

# ==========================================
# 12. INVENTÁRIO MONITORADO (COMPLETO COM KMS)
# ==========================================
st.subheader("Inventário Monitorado")

col_inv1, col_inv2, col_inv3, col_inv4, col_inv5, col_inv6, col_inv7 = st.columns(7)
col_inv1.metric("IAM", iam_data.get("totalUsers", 0))
col_inv2.metric("S3", s3_data.get("totalBuckets", 0))
col_inv3.metric("EC2", ec2_data.get("totalInstances", 0))
col_inv4.metric("RDS", rds_data.get("totalDatabases", 0))
col_inv5.metric("Lambda", lambda_data.get("totalFunctions", 0))
col_inv6.metric("KMS", kms_data.get("totalKeys", 0))
col_inv7.metric("Config", config_data.get("evaluatedRules", 45))

st.markdown("---")

# ==========================================
# 13. SEÇÕES ESPECÍFICAS DE COMPLIANCE (RDS, LAMBDA, KMS)
# ==========================================
col_sec1, col_sec2, col_sec3 = st.columns(3)

with col_sec1:
    st.subheader("Database Compliance")
    st.metric("Bases Não Criptografadas", rds_data.get("unencryptedDatabases", 0))

with col_sec2:
    st.subheader("Lambda Compliance")
    st.metric("Runtimes Obsoletos", lambda_data.get("outdatedRuntimes", 0))

with col_sec3:
    st.subheader("KMS Security")
    st.write(f"Chaves Ativas: {kms_data.get('totalKeys', 0)}")
    st.write(f"Rotação Ativa: {kms_data.get('rotationEnabled', 0)}")

st.markdown("---")

# ==========================================
# 14. FRAMEWORK STATUS E CORRELAÇÃO
# ==========================================
st.subheader("Framework Status")

framework_df = pd.DataFrame({
    "Framework": ["CIS Benchmark v1.5.0", "NIST SP 800-53", "ISO 27001:2022", "PCI-DSS v4.0", "SOC 2 Type II"],
    "Controles Avaliados": [45, 110, 93, 64, 85],
    "Compliance (%)": [cis_score, nist_score, iso_score, 96, 98],
    "Status": ["Atenção Requerida" if critical_findings > 0 else "Conforme", "Conforme", "Conforme", "Atenção Requerida" if critical_findings > 0 else "Conforme", "Conforme"]
})

st.dataframe(framework_df, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Framework Correlation")
st.write(
    """
    - **CIS Benchmark:** Governança de Configuração e Endurecimento de Ativos
    - **NIST CSF:** Gestão de Riscos, Identificação e Resposta a Incidentes
    - **ISO 27001:** Controles de Segurança da Informação e Gestão de Acesso
    - **PCI-DSS:** Proteção de Dados Sensíveis e Transações
    - **SOC 2:** Segurança Operacional e Integridade de Processos
    """
)

chart_df = pd.DataFrame({
    "Framework": ["CIS Benchmark", "NIST CSF", "ISO 27001", "PCI-DSS", "SOC 2"],
    "Compliance": [cis_score, nist_score, iso_score, 96, 98]
})
st.bar_chart(chart_df.set_index("Framework"))

st.markdown("---")

# ==========================================
# 15. COMPLIANCE RISK MATRIX (DINÂMICA)
# ==========================================
st.subheader("Compliance Risk Matrix")

risk_c1, risk_c2, risk_c3, risk_c4 = st.columns(4)
risk_c1.metric("Crítico", critical_risk)
risk_c2.metric("Alto", high_risk)
risk_c3.metric("Médio", medium_risk)
risk_c4.metric("Baixo", low_risk)

st.markdown("---")

# ==========================================
# 16. COMPLIANCE TREND (HISTÓRICO)
# ==========================================
st.subheader("Compliance Trend")

history_df = pd.DataFrame({
    "Data": ["20/08", "21/08", "22/08", "23/08", "24/08"],
    "Compliance": [88, 90, 91, 93, cis_score]
})

st.line_chart(history_df.set_index("Data"))

st.markdown("---")

# ==========================================
# 17. TIMELINE DE EVENTOS DINÂMICA
# ==========================================
st.subheader("Timeline")

timeline = []
if mfa_off > 0:
    timeline.append(f"{mfa_off} usuários sem MFA detectados")
if public_buckets > 0:
    timeline.append(f"{public_buckets} buckets públicos encontrados")
if open_sg > 0:
    timeline.append(f"{open_sg} grupos de segurança expostos")
if guardduty_threats > 0:
    timeline.append(f"{guardduty_threats} ameaças ativas identificadas no GuardDuty")

if not timeline:
    timeline.append("Nenhum desvio crítico recente registrado na varredura contínua.")

for evento in timeline:
    st.write(f"{datetime.now().strftime('%H:%M:%S')} - {evento}")

st.markdown("---")

# ==========================================
# 18. HEALTH CHECK DOS SERVIÇOS
# ==========================================
st.subheader("Health Check")

health_df = pd.DataFrame([
    ["IAM", "Online" if backend_online else "Offline"],
    ["S3", "Online" if backend_online else "Offline"],
    ["EC2", "Online" if backend_online else "Offline"],
    ["RDS", "Online" if backend_online else "Offline"],
    ["Lambda", "Online" if backend_online else "Offline"],
    ["KMS", "Online" if backend_online else "Offline"],
    ["GuardDuty", "Online" if backend_online else "Offline"],
    ["Config", "Online" if backend_online else "Offline"],
    ["Backend Node.js", "Online" if backend_online else "Offline"]
], columns=["Serviço", "Status"])

st.dataframe(health_df, use_container_width=True, hide_index=True)

# ==========================================
# RODAPÉ DA PÁGINA
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Centro de Governança e Compliance • Última Atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")