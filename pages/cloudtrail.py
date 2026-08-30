import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="CloudTrail Investigation Center | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="cloudtrail_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO
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

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

p, span, label, div {
    color: #E5E7EB;
}

.hero-card {
    background: #1F2937;
    border: 1px solid #374151;
    border-radius: 15px;
    padding: 24px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HEALTH CHECK DO BACKEND
# ==========================================
try:
    requests.get("http://127.0.0.1:3000", timeout=2)
    backend_status_html = 'Backend Node.js Online'
except Exception:
    backend_status_html = 'Backend Offline'

# ==========================================
# 5. CABEÇALHO DO MÓDULO
# ==========================================
st.markdown(f"""
<div class="hero-card">
    <h1>CloudTrail Investigation Center</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Monitoramento e investigação forense de eventos AWS em tempo real.
    </p>
    <p style="color: #6EE7B7; margin-top: 8px; font-size: 13px;">Status do Servidor: {backend_status_html}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# ADIÇÃO 9: RESUMO EXECUTIVO
# ==========================================
st.subheader("Resumo Executivo")
st.info("""
Eventos totais: 127

Eventos críticos: 3

Mudanças IAM: 12

Status: Requer Atenção
""")

st.markdown("---")

# ==========================================
# 6. MÉTRICAS EXECUTIVAS
# ==========================================
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos",
    "127"
)

c2.metric(
    "Logins",
    "42"
)

c3.metric(
    "Mudanças IAM",
    "12"
)

c4.metric(
    "Eventos Críticos",
    "3"
)

st.markdown("---")

# ==========================================
# ADIÇÃO 1: RISK SCORE
# ==========================================
risk_score = 82

st.subheader("Risk Score")

st.progress(risk_score / 100)

if risk_score >= 80:
    st.error(f"Risk Score: {risk_score}/100")
elif risk_score >= 50:
    st.warning(f"Risk Score: {risk_score}/100")
else:
    st.success(f"Risk Score: {risk_score}/100")

st.markdown("---")

# ==========================================
# ADIÇÃO 2: SEVERIDADE DOS EVENTOS
# ==========================================
st.subheader("Severidade")

s1, s2, s3 = st.columns(3)

with s1:
    st.metric("Críticos", "3")

with s2:
    st.metric("Altos", "7")

with s3:
    st.metric("Médios", "12")

st.markdown("---")

# ==========================================
# ADIÇÃO 10: DETECTOR DE AMEAÇAS (THREAT DETECTION)
# ==========================================
st.subheader("Threat Detection")
st.error("Atividade suspeita detectada no CloudTrail.")

st.markdown("---")

# ==========================================
# ADIÇÃO 3: DETECTION ENGINE
# ==========================================
st.subheader("Detection Engine")
st.write("✓ Login Root Detectado")
st.write("✓ Alteração IAM Detectada")
st.write("✓ Bucket Policy Modificada")
st.write("✓ Security Group Alterado")

st.markdown("---")

# ==========================================
# ADIÇÃO 4: ATTACK PATH CORRELATION
# ==========================================
st.subheader("Attack Path Correlation")

st.warning("""
Possível caminho de ataque detectado:

IAM
↓
EC2
↓
S3
↓
Exfiltração de Dados
""")

st.markdown("---")

# ==========================================
# 7. EVENTOS RECENTES
# ==========================================
st.subheader("Eventos Recentes")

eventos = [
    {
        "Data": "27/08/2026 14:00",
        "Evento": "CreateUser",
        "Serviço": "IAM"
    },
    {
        "Data": "27/08/2026 14:08",
        "Evento": "PutBucketPolicy",
        "Serviço": "S3"
    }
]

st.dataframe(eventos, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# ADIÇÃO 5: TIMELINE MELHOR (DATAFRAME)
# ==========================================
st.subheader("Timeline")

timeline = pd.DataFrame([
    {
        "Hora": "14:01",
        "Evento": "ConsoleLogin",
        "Serviço": "IAM",
        "Severidade": "Alta"
    },
    {
        "Hora": "14:08",
        "Evento": "PutBucketPolicy",
        "Serviço": "S3",
        "Severidade": "Crítica"
    }
])

st.dataframe(
    timeline,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 9. INVESTIGAÇÃO (PESQUISA DE EVENTOS)
# ==========================================
st.subheader("Investigação")

filtro = st.selectbox(
    "Filtrar",
    [
        "IAM",
        "S3",
        "EC2",
        "CloudTrail",
        "GuardDuty"
    ]
)

if st.button("Pesquisar"):
    st.success(f"Eventos localizados para o filtro: {filtro}.")

st.markdown("---")

# ==========================================
# ADIÇÃO 8: LABORATÓRIO FORENSE
# ==========================================
st.subheader("Laboratório Forense")

tipo = st.selectbox(
    "Simular Evento Forense",
    [
        "Investigar Login Root",
        "Investigar IAM",
        "Investigar S3",
        "Investigar EC2",
        "Investigar GuardDuty"
    ]
)

if st.button("Executar Simulação Forense"):
    st.success(f"Simulação {tipo} executada com sucesso.")

st.markdown("---")

# ==========================================
# ADIÇÃO 7: CLOUDTRAIL COPILOT MAIS INTELIGENTE
# ==========================================
st.subheader("CloudTrail Copilot")

pergunta = st.text_area(
    "Pergunte ao Copilot (IAM, S3, EC2, Root, CloudTrail, GuardDuty, Ransomware, Credential Theft)"
)

if st.button("Analisar Evento"):
    p = pergunta.lower()
    
    if "iam" in p:
        st.info("Evento IAM detectado. Verifique MFA, políticas e credenciais.")
    elif "s3" in p:
        st.info("Verifique alterações em Bucket Policies e Block Public Access.")
    elif "ec2" in p:
        st.info("Validar criação de instâncias e alterações em Security Groups.")
    elif "root" in p:
        st.info("Verifique imediatamente atividades da conta root e confirme o uso de MFA.")
    elif "cloudtrail" in p:
        st.info("Assegure integridade dos logs e valide trilhas multi-regionais ativas.")
    elif "guardduty" in p:
        st.info("Correlacione achados do GuardDuty com eventos suspeitos de API no CloudTrail.")
    elif "ransomware" in p:
        st.info("Alerta crítico: monitore deleções em massa de objetos S3 e alteração de snapshots.")
    elif "credential" in p or "theft" in p:
        st.info("Investigue acessos via chaves vazadas (Access Keys) de localizações IP atípicas.")
    else:
        st.info("Análise concluída com base nos logs do CloudTrail.")

st.markdown("---")

# ==========================================
# ADIÇÃO 6: COMPLIANCE LINK E INTEGRAÇÕES
# ==========================================
st.subheader("Módulos Relacionados")

col_l1, col_l2, col_l3, col_l4, col_l5 = st.columns(5)

with col_l1:
    st.page_link("pages/Attack_Path.py", label="Attack Path")
with col_l2:
    st.page_link("pages/AWS_Config.py", label="AWS Config")
with col_l3:
    st.page_link("pages/Threat_Intelligence.py", label="Threat Intelligence")
with col_l4:
    st.page_link("pages/Compliance.py", label="Compliance")
with col_l5:
    st.page_link("pages/AWS_Config.py", label="Ver Compliance Relacionado")

# ==========================================
# RODAPÉ
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • CloudTrail Investigation Center • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")