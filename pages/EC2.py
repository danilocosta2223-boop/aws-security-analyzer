import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EC2 Security Center | AWS Cyber Defense Platform",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="ec2_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO (DARK THEME)
# ==========================================
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
        background-color: #1F2937;
        color: #93c5fd;
        border: 1px solid #374151;
    }

    h1, h2, h3, h4 {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. CONSUMO ROBUSTO DAS APIS DO BACKEND (TIMEOUT=5)
# ==========================================
@st.cache_data(ttl=10)
def carregar_dados_ec2():
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2", timeout=5).json()
    score = requests.get("http://127.0.0.1:3000/api/security-score", timeout=5).json()
    return ec2, score

try:
    ec2_data, score_data = carregar_dados_ec2()
    backend_online = True
except Exception:
    backend_online = False
    st.error("Backend indisponível. Certifique-se de que o servidor Node.js está em execução na porta 3000.")
    st.stop()

# ==========================================
# 5. VARIÁVEIS E CÁLCULOS DINÂMICOS
# ==========================================
total_instances = ec2_data.get("totalInstances", 5)
running_instances = ec2_data.get("runningInstances", 4)
stopped_instances = ec2_data.get("stoppedInstances", 1)
open_security_groups = ec2_data.get("openSecurityGroups", 2)

compliance_score = max(100 - (open_security_groups * 8), 60)
ec2_score = max(100 - (open_security_groups * 5), 0)

# ==========================================
# 6. HERO CARD DO MÓDULO
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>EC2 Security Center</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Monitoramento de instâncias elétricas, superfície de ataque, regras de Security Groups, custos e compliance de infraestrutura compute AWS.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional &nbsp;|&nbsp; 
    <b>Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} &nbsp;|&nbsp;
    <b>Open SGs:</b> {open_security_groups}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 1. EC2 MISSION CONTROL
# ==========================================
st.subheader("EC2 Mission Control")

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Instâncias", total_instances)
m2.metric("Running", running_instances)
m3.metric("Stopped", stopped_instances)
m4.metric("Open SG", open_security_groups)
m5.metric("Compliance", f"{compliance_score}%")
m6.metric("Status", "Operational")

st.markdown("---")

# ==========================================
# 2. EC2 SECURITY SCORE
# ==========================================
st.subheader("EC2 Security Score")

st.progress(ec2_score / 100)
st.success(f"EC2 Security Score: {ec2_score}%")

st.markdown("---")

# ==========================================
# 3. FLEET OVERVIEW
# ==========================================
st.subheader("Fleet Overview")

inventory = pd.DataFrame({
    "Instância": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01",
        "prod-api-02",
        "staging-app"
    ],
    "Status": [
        "Running",
        "Running",
        "Stopped",
        "Running",
        "Running"
    ],
    "Compliance": [
        "OK",
        "OK",
        "Atenção",
        "OK",
        "OK"
    ]
})

st.dataframe(
    inventory,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# RUNNING INSTANCES (Detalhes Complementares)
# ==========================================
st.subheader("Running Instances")
running_df = inventory[inventory["Status"] == "Running"]
st.dataframe(running_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 4. ATTACK SURFACE
# ==========================================
st.subheader("Attack Surface")

surface = pd.DataFrame({
    "Controle": [
        "SSH",
        "RDP",
        "Security Group"
    ],
    "Exposição": [
        2,
        1,
        open_security_groups
    ]
})

st.dataframe(
    surface,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# SECURITY FINDINGS
# ==========================================
st.subheader("Security Findings")
findings_df = pd.DataFrame({
    "Vetor de Risco": ["Porta 22 Exposta", "RDP Publicamente Acessível", "Security Group com All-Traffic"],
    "Severidade": ["High", "Critical", "High"]
})
st.dataframe(findings_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# COMPLIANCE STATUS
# ==========================================
st.subheader("Compliance Status")
st.info(f"Índice atual de adequação às normas CIS e AWS Foundational Security Best Practices: **{compliance_score}%**")

st.markdown("---")

# ==========================================
# 6. COST ANALYTICS
# ==========================================
st.subheader("Cost Analytics")

cost_df = pd.DataFrame({
    "Instância": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01",
        "prod-api-02"
    ],
    "Custo": [
        "$18",
        "$70",
        "$12",
        "$45"
    ]
})

st.dataframe(
    cost_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# PATCH MANAGEMENT
# ==========================================
st.subheader("Patch Management")

patch_df = pd.DataFrame({
    "Instância": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01"
    ],
    "Status": [
        "Atualizada",
        "Pendente",
        "Atualizada"
    ]
})

st.dataframe(
    patch_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 5. THREAT INTELLIGENCE INTEGRATION
# ==========================================
st.subheader("Threat Intelligence Integration")

threat_df = pd.DataFrame({
    "Threat": [
        "Open SSH",
        "Exposed RDP",
        "Public Subnet"
    ],
    "Severity": [
        "High",
        "Critical",
        "Medium"
    ]
})

st.dataframe(
    threat_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 8. EC2 COPILOT
# ==========================================
st.subheader("EC2 Copilot")

question = st.text_area(
    "Pergunte sobre sua infraestrutura EC2 (ex: ssh, custo, compliance):"
)

if st.button("Analisar EC2"):
    p = question.lower()
    
    if "ssh" in p:
        st.info("Existem instâncias com SSH exposto na porta 22 sem restrição de IP de origem.")
    elif "custo" in p:
        st.info("A instância prod-db-01 possui maior custo operacional mensal devido à classe de instância e volume de IOPS provisionado.")
    elif "compliance" in p:
        st.info(f"Compliance atual da frota EC2: {compliance_score}%")
    else:
        st.info("Análise de infraestrutura EC2 concluída com base nos parâmetros atuais da AWS.")

st.markdown("---")

# ==========================================
# 9. EXECUTIVE REPORT
# ==========================================
st.subheader("Executive Report")

report = f"""
EC2 SECURITY REPORT

Security Score: {ec2_score}%
Compliance Score: {compliance_score}%

Running Instances: {running_instances}
Stopped Instances: {stopped_instances}
Open Security Groups: {open_security_groups}
"""

st.download_button(
    "📥 Baixar Relatório",
    report,
    file_name="ec2_report.txt"
)

st.markdown("---")

# ==========================================
# 10. NAVEGAÇÃO INTEGRADA
# ==========================================
st.subheader("Navegação Integrada")

n1, n2, n3, n4, n5 = st.columns(5)

with n1:
    st.page_link(
        "pages/security_hub.py",
        label="Security Hub"
    )

with n2:
    st.page_link(
        "pages/security_copilot.py",
        label="Security Copilot"
    )

with n3:
    st.page_link(
        "pages/compliance.py",
        label="Compliance"
    )

with n4:
    st.page_link(
        "pages/threat_intelligence.py",
        label="Threat Intelligence"
    )

with n5:
    st.page_link(
        "pages/executive_dashboard.py",
        label="Executive Dashboard"
    )

# ==========================================
# RODAPÉ DO MÓDULO
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • EC2 Security Management • Sincronizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")