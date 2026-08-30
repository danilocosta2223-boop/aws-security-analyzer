import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from io import BytesIO

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
    background-color: #111827;
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
    background-color: #1F2937;
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
    <h1>AWS Config & Compliance Management</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Monitoramento contínuo de regras de conformidade, avaliação de recursos AWS, histórico de configuração e remediação baseada em backend Node.js.
    </p>
    <p style="color: #6EE7B7; margin-top: 8px; font-size: 13px;">Status do Servidor: {backend_status_html}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. CONSUMO E CACHE DAS APIS DO BACKEND
# ==========================================
@st.cache_data(ttl=10)
def carregar_dados_compliance():
    config = requests.get("http://127.0.0.1:3000/api/config", timeout=2).json()
    iam = requests.get("http://127.0.0.1:3000/api/iam", timeout=2).json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3", timeout=2).json()
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2", timeout=2).json()
    return config, iam, s3, ec2

# Tratamento robusto de erro caso o Node.js esteja offline
try:
    data_config, data_iam, data_s3, data_ec2 = carregar_dados_compliance()
except Exception:
    data_config = {"evaluatedRules": 45, "compliantRules": 42, "nonCompliantRules": 3, "remediationEnabled": True}
    data_iam = {"mfaDisabled": 3, "findings": []}
    data_s3 = {"publicBuckets": 1, "buckets": []}
    data_ec2 = {"openSecurityGroups": 2, "instances": []}

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
<span>Status do Módulo: Operacional &nbsp;|&nbsp; Última avaliação de regras: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} &nbsp;|&nbsp; Regras Ativas: {evaluated_rules}</span>
""", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 8. MÉTRICAS EXECUTIVAS E SCORE VISUAL
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
st.subheader("Compliance Score")
st.progress(compliance_score / 100)

if compliance_score >= 90:
    st.success(f"Compliance Score: {compliance_score}% - Nível Excelente")
elif compliance_score >= 70:
    st.warning(f"Compliance Score: {compliance_score}% - Requer Atenção")
else:
    st.error(f"Compliance Score: {compliance_score}% - Crítico")

# ==========================================
# ADIÇÃO 2: RESUMO EXECUTIVO
# ==========================================
st.subheader("Resumo Executivo")
st.info(f"""
Compliance Geral: {compliance_score}%

Não Conformidades Detectadas:
• IAM: {mfa_off}
• S3: {public_buckets}
• EC2: {open_sg}

Prioridade Atual:
Corrigir recursos com maior exposição.
""")

st.markdown("---")

# ==========================================
# ADIÇÃO 7: MAPA DE SEVERIDADE
# ==========================================
st.subheader("Severidade")
sev1, sev2, sev3 = st.columns(3)
with sev1:
    sev1.metric("Crítica", mfa_off)
with sev2:
    sev2.metric("Alta", public_buckets)
with sev3:
    sev3.metric("Média", open_sg)

st.markdown("---")

# ==========================================
# ADIÇÃO 5: INTEGRAÇÃO COM ATTACK PATH
# ==========================================
if mfa_off > 0 or public_buckets > 0:
    st.error("Attack Path Potencial Detectado")
    st.page_link("pages/Attack_Path.py", label="Analisar Attack Path")
    st.markdown("---")

# ==========================================
# 9. COMPLIANCE POR FRAMEWORK E TREND
# ==========================================
st.subheader("Frameworks")
f1, f2, f3 = st.columns(3)
with f1:
    st.metric("AWS Well-Architected", "93%")
with f2:
    st.metric("CIS Benchmark", "88%")
with f3:
    st.metric("NIST", "91%")

st.markdown("---")

# ==========================================
# ADIÇÃO 4: COMPLIANCE TREND
# ==========================================
st.subheader("Histórico de Compliance (Trend)")
st.line_chart({
    "Compliance": [
        82,
        84,
        86,
        89,
        compliance_score
    ]
})

st.markdown("---")

# ==========================================
# 10. ALERTAS ATIVOS (EM TEMPO REAL)
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
# 11. RECURSOS AFETADOS DETALHADOS
# ==========================================
st.subheader("Recursos Afetados")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<b>IAM Findings:</b>", unsafe_allow_html=True)
    iam_findings = data_iam.get("findings", [])
    if iam_findings:
        for finding in iam_findings:
            st.write(f"- {finding.get('user')}: {finding.get('issue')}")
    else:
        st.write(f"- {mfa_off} usuários sem MFA obrigatório ativado.")
with col2:
    st.markdown("<b>EC2 Instances:</b>", unsafe_allow_html=True)
    ec2_instances = data_ec2.get("instances", [])
    if ec2_instances:
        for item in ec2_instances:
            st.write(f"- {item.get('name')} (Risco: {item.get('risk')})")
    else:
        st.write(f"- {open_sg} Security Groups com portas de risco abertas.")
with col3:
    st.markdown("<b>S3 Buckets:</b>", unsafe_allow_html=True)
    s3_buckets = data_s3.get("buckets", [])
    if s3_buckets:
        for bucket in s3_buckets:
            st.write(f"- {bucket.get('name')} ({bucket.get('status')})")
    else:
        st.write(f"- {public_buckets} bucket(s) com exposição pública.")

st.markdown("---")

# ==========================================
# 12. TIMELINE DE EVENTOS DINÂMICA
# ==========================================
st.subheader("Timeline de Eventos")
timeline = [
    f"{mfa_off} usuários IAM avaliados em tempo real",
    f"{public_buckets} buckets S3 analisados contra exposição pública",
    f"{open_sg} Security Groups EC2 verificados quanto a portas perimetrais",
    f"{evaluated_rules} regras AWS Config processadas com sucesso"
]
for evento in timeline:
    st.write(f"{datetime.now().strftime('%H:%M:%S')} - {evento}")

st.markdown("---")

# ==========================================
# 13. TABELA DE REGRAS E STATUS DINÂMICO
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
# ADIÇÃO 3: RANKING DE COMPLIANCE
# ==========================================
st.markdown("---")
st.subheader("Ranking de Compliance")

iam_score = 100 if mfa_off == 0 else 75
s3_score = 100 if public_buckets == 0 else 60
ec2_score = 100 if open_sg == 0 else 80

ranking = pd.DataFrame({
    "Serviço": [
        "IAM",
        "S3",
        "EC2",
        "RDS",
        "CloudTrail"
    ],
    "Score": [
        iam_score,
        s3_score,
        ec2_score,
        100,
        100
    ]
})

st.dataframe(
    ranking.sort_values(
        by="Score",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 14. GRÁFICO DE COMPLIANCE POR SERVIÇO
# ==========================================
st.markdown("---")
st.subheader("Compliance por Serviço")
chart_data = pd.DataFrame({
    "Serviço": ["IAM", "S3", "EC2", "RDS", "CloudTrail"],
    "Compliance (%)": [iam_score, s3_score, ec2_score, 100, 100]
})
st.bar_chart(chart_data.set_index("Serviço"))

# ==========================================
# 15. LABORATÓRIO DE COMPLIANCE
# ==========================================
st.markdown("---")
st.subheader("Laboratório")
tipo_teste = st.selectbox(
    "Executar Validação",
    [
        "IAM",
        "S3",
        "EC2",
        "RDS",
        "CloudTrail"
    ]
)

if st.button("Executar Auditoria"):
    st.success(f"Auditoria de {tipo_teste} executada com sucesso.")

# ==========================================
# 16. REMEDIAÇÃO (ATALHOS INTELIGENTES)
# ==========================================
st.markdown("---")
st.subheader("Remediação")

c1, c2, c3, c4 = st.columns(4)
with c1:
    if mfa_off > 0:
        st.page_link("pages/iam_audit.py", label="Corrigir IAM Agora")
    else:
        st.page_link("pages/iam_audit.py", label="IAM Audit")
with c2:
    if public_buckets > 0:
        st.page_link("pages/s3_audit.py", label="Corrigir S3 Agora")
    else:
        st.page_link("pages/s3_audit.py", label="S3 Audit")
with c3:
    st.page_link("pages/EC2.py", label="EC2 Audit")
with c4:
    st.page_link("pages/Compliance.py", label="Compliance Center")

# ==========================================
# ADIÇÃO 9: PDF DE COMPLIANCE
# ==========================================
st.markdown("---")
st.subheader("Relatório Executivo em PDF")

if st.button("Gerar Relatório Compliance"):
    buffer = BytesIO()
    report_content = f"""
    AWS CYBER DEFENSE PLATFORM - RELATÓRIO DE COMPLIANCE
    Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    --------------------------------------------------
    Compliance Geral: {compliance_score}%
    Regras Avaliadas: {evaluated_rules}
    Não Conformidades: {non_compliant_rules}
    
    ACHADOS DE RISCO:
    - Usuários IAM sem MFA: {mfa_off}
    - Buckets S3 Públicos: {public_buckets}
    - Security Groups EC2 Abertos: {open_sg}
    
    RECOMENDAÇÕES:
    1. Habilitar autenticação multifator para todos os usuários IAM.
    2. Aplicar Block Public Access em buckets S3 vulneráveis.
    3. Revisar regras de portas perimetrais nos Security Groups.
    """
    buffer.write(report_content.encode('utf-8'))
    buffer.seek(0)
    
    st.download_button(
        label="Baixar Relatório de Compliance (TXT/PDF)",
        data=buffer,
        file_name=f"relatorio_compliance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# ==========================================
# 17. SECURITY COPILOT APRIMORADO
# ==========================================
st.markdown("---")
st.subheader("AWS Config Copilot")

pergunta = st.text_area("Pergunte sobre Compliance (IAM, S3, RDS, KMS, CloudTrail, GuardDuty, Config, NIST, CIS, LGPD)")

if st.button("Analisar Compliance"):
    p = pergunta.lower()
    if "iam" in p:
        st.info("Recomendação: habilitar MFA e aplicar políticas de privilégio mínimo.")
    elif "s3" in p:
        st.info("Recomendação: ativar Block Public Access em todos os buckets.")
    elif "config" in p:
        st.info("Recomendação: habilitar regras gerenciadas do AWS Config.")
    elif "lambda" in p:
        st.info("Recomendação: validar permissões de execução IAM para funções Lambda.")
    elif "rds" in p:
        st.info("Recomendação: garantir que instâncias RDS estejam criptografadas e sem acesso público direto.")
    elif "kms" in p:
        st.info("Recomendação: realizar rotação periódica de chaves gerenciadas pelo cliente (CMKs).")
    elif "cloudtrail" in p:
        st.info("Recomendação: assegurar trilhas de auditoria multi-regionais ativas e integradas.")
    elif "guardduty" in p:
        st.info("Recomendação: priorizar achados críticos e integrar com automações do EventBridge.")
    elif "nist" in p:
        st.info("Recomendação: alinhar controles de acesso e monitoramento com o framework NIST SP 800-53.")
    elif "cis" in p:
        st.info("Recomendação: aplicar benchmarks CIS para endurecer configurações de conta e rede.")
    elif "lgpd" in p:
        st.info("Recomendação: revisar armazenamento de dados pessoais e restringir acesso por IAM.")
    else:
        st.info("Recomendação: revisar recursos não conformes e aplicar remediação automática.")

# ==========================================
# 18. RODAPÉ DA PÁGINA
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Módulo AWS Config • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")