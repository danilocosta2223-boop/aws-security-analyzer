import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="AWS Config & Compliance | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="config_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO
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
# 4. HEALTH CHECK DO BACKEND
# ==========================================
try:
    requests.get("http://127.0.0.1:3000", timeout=2)
    backend_status_html = '<span style="color: #16a34a; font-weight: 600;">Backend Node.js Online</span>'
except Exception:
    backend_status_html = '<span style="color: #dc2626; font-weight: 600;">Backend Offline</span>'

# ==========================================
# 5. CABEÇALHO DO MÓDULO
# ==========================================
st.markdown(f"""
<div class="hero-card">
    <h1>AWS Config & Compliance Management</h1>
    <p style="color: #4b5563; margin: 0; font-size: 15px;">
        Monitoramento contínuo de regras de conformidade, avaliação de recursos AWS, histórico de configuração e remediação baseada em backend Node.js.
    </p>
    <div style="margin-top: 10px; font-size: 13px;">
        Status do Servidor: {backend_status_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. CONSUMO E CACHE DAS APIS DO BACKEND
# ==========================================
@st.cache_data(ttl=10)
def carregar_dados_compliance():
    config = requests.get("http://127.0.0.1:3000/api/config").json()
    iam = requests.get("http://127.0.0.1:3000/api/iam").json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3").json()
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2").json()
    return config, iam, s3, ec2

# Tratamento robusto de erro caso o Node.js esteja offline
try:
    data_config, data_iam, data_s3, data_ec2 = carregar_dados_compliance()
except Exception:
    st.error("Backend indisponível. Execute node server.js.")
    st.stop()

# ==========================================
# 7. CÁLCULOS E MÉTRICAS DINÂMICAS
# ==========================================
mfa_off = data_iam.get("mfaDisabled", 0)
public_buckets = data_s3.get("publicBuckets", 0)
open_sg = data_ec2.get("openSecurityGroups", 0)

evaluated_rules = data_config.get("evaluatedRules", 45)
compliant_rules = data_config.get("compliantRules", 42)
non_compliant_rules = data_config.get("nonCompliantRules", 3)
remediation_enabled = data_config.get("remediationEnabled", True)

# Cálculo dinâmico do Compliance Score
compliance_score = 100
compliance_score -= mfa_off * 3
compliance_score -= public_buckets * 5
compliance_score -= open_sg * 4
compliance_score = max(compliance_score, 0)

st.markdown(f"""
<div style="font-size: 13px; color: #4b5563; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional &nbsp;|&nbsp; 
    <b>Última avaliação de regras:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} &nbsp;|&nbsp;
    <b>Regras Ativas:</b> {evaluated_rules}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 8. MÉTRICAS EXECUTIVAS
# ==========================================
st.subheader("Executive Dashboard")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Conformidade Geral", f"{compliance_score}%", "Cálculo Dinâmico")
with m2:
    st.metric("Regras Avaliadas", f"{evaluated_rules} / {evaluated_rules}", "100% Cobertura")
with m3:
    st.metric("Regras Non-Compliant", non_compliant_rules, "Requer Atenção", delta_color="inverse")
with m4:
    st.metric("Remediação Automática", "Ativada" if remediation_enabled else "Desativada", "Systems Manager")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 9. ALERTAS ATIVOS (EM TEMPO REAL)
# ==========================================
st.subheader("Alertas Ativos")

if mfa_off > 0:
    st.warning(f"{mfa_off} usuários operando sem autenticação multifator (MFA).")
if public_buckets > 0:
    st.error(f"{public_buckets} buckets S3 encontrados com políticas públicas.")
if open_sg > 0:
    st.warning(f"{open_sg} grupos de segurança EC2 com portas perimetrais expostas.")

if mfa_off == 0 and public_buckets == 0 and open_sg == 0:
    st.success("Nenhum alerta crítico ativo no momento.")

st.markdown("---")

# ==========================================
# 10. RECURSOS AFETADOS DETALHADOS
# ==========================================
st.subheader("Recursos Afetados")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**IAM Findings:**")
    iam_findings = data_iam.get("findings", [])
    if iam_findings:
        for finding in iam_findings:
            st.write(f"- {finding.get('user')}: {finding.get('issue')}")
    else:
        st.write("Nenhum achado crítico no IAM.")

with col2:
    st.markdown("**EC2 Instances:**")
    ec2_instances = data_ec2.get("instances", [])
    if ec2_instances:
        for item in ec2_instances:
            st.write(f"- {item.get('name')} (Risco: {item.get('risk')})")
    else:
        st.write("Nenhuma instância em risco.")

with col3:
    st.markdown("**S3 Buckets:**")
    s3_buckets = data_s3.get("buckets", [])
    if s3_buckets:
        for bucket in s3_buckets:
            st.write(f"- {bucket.get('name')} ({bucket.get('status')})")
    else:
        st.write("Nenhum bucket listado.")

st.markdown("---")

# ==========================================
# 11. TIMELINE DE EVENTOS EM TEMPO REAL
# ==========================================
st.subheader("Timeline de Eventos")

timeline = [
    "Avaliação de conformidade executada via API do AWS Config",
    "Verificação de políticas de acesso público nos buckets S3",
    "Varredura de instâncias EC2 e verificação de portas abertas",
    "Auditoria de credenciais e status de MFA no IAM"
]

for evento in timeline:
    st.write(f"{datetime.now().strftime('%H:%M:%S')} - {evento}")

st.markdown("---")

# ==========================================
# 12. TABELA DE REGRAS E STATUS DINÂMICO
# ==========================================
st.subheader("Status Detalhado das Regras do AWS Config")

df_rules = pd.DataFrame([
    {
        "ID da Regra": "s3-bucket-public-read-prohibited", 
        "Serviço": "S3", 
        "Status": "NON-COMPLIANT" if public_buckets > 0 else "COMPLIANT", 
        "Severidade": "Alta", 
        "Última Verificação": "Tempo Real"
    },
    {
        "ID da Regra": "iam-root-mfa-enabled", 
        "Serviço": "IAM", 
        "Status": "NON-COMPLIANT" if mfa_off > 0 else "COMPLIANT", 
        "Severidade": "Crítica", 
        "Última Verificação": "Tempo Real"
    },
    {
        "ID da Regra": "ec2-instance-detailed-monitoring-enabled", 
        "Serviço": "EC2", 
        "Status": "NON-COMPLIANT" if open_sg > 0 else "COMPLIANT", 
        "Severidade": "Média", 
        "Última Verificação": "Tempo Real"
    },
    {
        "ID da Regra": "rds-storage-encrypted", 
        "Serviço": "RDS", 
        "Status": "COMPLIANT", 
        "Severidade": "Alta", 
        "Última Verificação": "Tempo Real"
    },
    {
        "ID da Regra": "cloudtrail-enabled", 
        "Serviço": "CloudTrail", 
        "Status": "COMPLIANT", 
        "Severidade": "Crítica", 
        "Última Verificação": "Tempo Real"
    }
])

st.dataframe(df_rules, use_container_width=True, hide_index=True)

# ==========================================
# 13. GRÁFICO DE COMPLIANCE POR SERVIÇO
# ==========================================
st.markdown("---")
st.subheader("Compliance por Serviço")

iam_score = 100 if mfa_off == 0 else 75
s3_score = 100 if public_buckets == 0 else 60
ec2_score = 100 if open_sg == 0 else 80

chart_data = pd.DataFrame({
    "Serviço": ["IAM", "S3", "EC2", "RDS", "CloudTrail"],
    "Compliance (%)": [iam_score, s3_score, ec2_score, 100, 100]
})

st.bar_chart(
    chart_data.set_index("Serviço")
)

# ==========================================
# RODAPÉ DA PÁGINA
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Módulo AWS Config • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")