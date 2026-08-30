import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Compliance & Frameworks Dashboard | AWS Cyber Defense",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================
st_autorefresh(interval=15000, key="compliance_refresh")

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
def carregar_dados_compliance():
    score = requests.get("http://127.0.0.1:3000/api/security-score").json()
    iam = requests.get("http://127.0.0.1:3000/api/iam").json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3").json()
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2").json()
    config = requests.get("http://127.0.0.1:3000/api/config").json()
    return score, iam, s3, ec2, config

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
# 6. CABEÇALHO DO MÓDULO (RAW HTML)
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Compliance & Frameworks Dashboard</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Centro de governança e conformidade contínua, monitoramento de padrões globais e postura de segurança integrada.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional | 
    <b>Última sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |
    <b>Desvios Críticos:</b> {critical_findings}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# 7. COMPLIANCE EXECUTIVE SUMMARY & POSTURE
# ==========================
st.subheader("Executive Dashboard & Score")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("CIS Benchmark", f"{cis_score}%", "-2%" if critical_findings > 0 else "Estável", delta_color="inverse")
with col2:
    st.metric("NIST CSF", f"{nist_score}%", "Atenção" if critical_findings > 0 else "Conforme")
with col3:
    st.metric("ISO 27001", f"{iso_score}%", "Revisão" if critical_findings > 0 else "Conforme")
with col4:
    st.metric("Score Geral", f"{score_data.get('score', 85)}/100")

st.markdown("---")

# ==========================
# 8. LABORATÓRIO DE AUDITORIA SIMULADA (COM ESCOPO)
# ==========================
st.subheader("Laboratório de Auditoria")

col_fw, col_scope = st.columns(2)
with col_fw:
    framework_escolhido = st.selectbox(
        "Framework de Referência",
        ["CIS Benchmark", "NIST CSF", "ISO 27001"]
    )
with col_scope:
    auditoria_escopo = st.selectbox(
        "Escopo de Avaliação",
        ["IAM", "S3", "EC2", "Completo"]
    )

if st.button("Executar Auditoria"):
    st.success(f"Auditoria {framework_escolhido} concluída com sucesso.")
    
    # Lógica de simulação de escopo
    if auditoria_escopo == "IAM":
        st.write("Controles avaliados: 15")
        st.markdown("- **IAM.1 (MFA Root):** Conforme\n- **IAM.2 (Key Rotation):** Atenção")
    elif auditoria_escopo == "S3":
        st.write("Controles avaliados: 10")
        st.markdown("- **S3.1 (Public Access):** Não Conforme\n- **S3.2 (Encryption):** Conforme")
    elif auditoria_escopo == "EC2":
        st.write("Controles avaliados: 20")
        st.markdown("- **EC2.1 (Port 22 Open):** Não Conforme\n- **EC2.2 (IMDSv2):** Conforme")
    else:
        st.write("Controles avaliados: 45")
        st.markdown("- Auditoria completa finalizada em todos os serviços essenciais.")

st.markdown("---")

# ==========================
# 9. SIMULAÇÃO DE REMEDIAÇÃO CONTROLADA
# ==========================
st.subheader("Remediação Controlada")

acao = st.selectbox(
    "Selecionar Ação para Execução Rápida",
    [
        "Ativar MFA (Root/Admin)",
        "Bloquear Bucket Público (Block Public Access)",
        "Fechar Security Group (Porta 22/3389)"
    ]
)

if st.button("Executar Remediação"):
    st.success(f"Ação '{acao}' iniciada e aplicada no ambiente simulado.")

st.markdown("---")

# ==========================
# 10. GOVERNANÇA, SLA E STATUS DE REMEDIAÇÃO
# ==========================
st.subheader("Governança de Correções e SLA")
gov_col1, gov_col2 = st.columns(2)

with gov_col1:
    owners = pd.DataFrame({
        "Controle": ["IAM", "S3", "EC2"],
        "Responsável": ["Equipe IAM", "Equipe Cloud", "Equipe Infraestrutura"],
        "Status": ["Aberto", "Aberto", "Em análise"],
        "Prazo (SLA)": ["7 dias", "3 dias", "15 dias"]
    })
    st.dataframe(owners, use_container_width=True, hide_index=True)

with gov_col2:
    remediation = pd.DataFrame({
        "Ação de Remediação": ["Ativar MFA", "Bloquear Bucket Público", "Revisão de Security Group"],
        "Progresso": ["100%", "50%", "80%"]
    })
    st.dataframe(remediation, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================
# 11. CENTRO DE EVIDÊNCIAS COM SIMULAÇÃO POR TIPO
# ==========================
st.subheader("Repositório de Evidências (Download)")

tipo_evidencia = st.selectbox(
    "Tipo de Evidência para Exportação",
    ["IAM", "CloudTrail", "Config", "S3", "Completo"]
)

evidencia_texto = f"""
========================================
EVIDÊNCIA DE COMPLIANCE - {tipo_evidencia.upper()}
========================================
Data de Extração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Framework Aplicado: {framework_escolhido}
Escopo Avaliado: {auditoria_escopo}

Status de Validação: Conforme com ressalvas.
Score Registrado: {score_data.get('score', 85)}/100
Hash de Validação: a8f9c1...
========================================
Este relatório foi gerado automaticamente pela AWS Cyber Defense Platform.
"""

st.download_button(
    label=f"Baixar Evidência ({tipo_evidencia})",
    data=evidencia_texto,
    file_name=f"evidence_{tipo_evidencia.lower()}.txt",
    mime="text/plain"
)

st.markdown("---")

# ==========================
# 12. CENTRO EDUCACIONAL E COMPLIANCE CHALLENGE
# ==========================
st.subheader("Compliance Challenge")
st.write("Teste seus conhecimentos de resposta a incidentes de compliance:")

st.info("**Cenário:** O módulo AWS Config detectou um Bucket S3 contendo dados sensíveis com acesso público (ACL e Policy abertas).")
resposta_challenge = st.radio(
    "Qual a ação de remediação recomendada pelo AWS Well-Architected Framework?",
    [
        "Manter público e monitorar via CloudTrail.",
        "Habilitar o 'Block Public Access' (BPA) no S3.",
        "Criar uma nova VPC e mover o bucket."
    ]
)

if st.button("Validar Resposta"):
    if resposta_challenge == "Habilitar o 'Block Public Access' (BPA) no S3.":
        st.success("Correto! O Block Public Access é a medida de mitigação imediata recomendada para isolar a exposição.")
        st.balloons()
    else:
        st.error("Incorreto. Revise as políticas do AWS S3 e o controle de Block Public Access.")

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Centro de Governança • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")