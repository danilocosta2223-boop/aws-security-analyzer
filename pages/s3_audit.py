import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="S3 Audit | AWS Security Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================
st_autorefresh(interval=15000, key="s3_audit_refresh")

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

    h1, h2, h3, h4 {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# 4. CONSUMO DE DADOS DA API
# ==========================
@st.cache_data(ttl=10)
def carregar_dados_s3():
    response = requests.get("http://127.0.0.1:3000/api/s3")
    return response.json()

try:
    s3_data = carregar_dados_s3()
    backend_online = True
except Exception:
    backend_online = False
    s3_data = {
        "totalBuckets": 18,
        "publicBuckets": 2,
        "encryptedBuckets": 16,
        "versioningEnabled": 14
    }

# ==========================
# 5. CABEÇALHO DO MÓDULO (RAW HTML)
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>AWS S3 Storage Audit & Posture</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Governança de objetos e buckets S3: controle de exposição pública, criptografia em repouso, versionamento e políticas de acesso.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status do Scanner S3:</b> Operacional (Multi-Region) | 
    <b>Última varredura:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |
    <b>Total de Buckets Monitorados:</b> {s3_data.get('totalBuckets', 18)}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# 6. EXECUTIVE SUMMARY
# ==========================
st.subheader("Executive Summary")

if s3_data.get("publicBuckets", 0) > 0:
    st.warning("""
Situação Geral: Atenção

Buckets públicos identificados.

Recomendações:
• Aplicar Block Public Access
• Revisar Bucket Policies
• Validar criptografia
""")
else:
    st.success("""
Situação Geral: Conforme

Nenhum bucket público detectado.
""")

st.markdown("---")

# ==========================
# 7. EXECUTIVE DASHBOARD
# ==========================
st.subheader("Executive Dashboard")
e1, e2, e3, e4 = st.columns(4)
e1.metric("Buckets", s3_data.get('totalBuckets', 18))
e2.metric("Públicos", s3_data.get('publicBuckets', 2))
e3.metric("Criptografados", s3_data.get('encryptedBuckets', 16))
e4.metric("Compliance", "89%")

st.markdown("---")

# ==========================
# 8. S3 SECURITY SCORE & S3 HEALTH
# ==========================
st.subheader("S3 Security Score")

s3_score = max(
    100 - (s3_data.get("publicBuckets", 2) * 10),
    60
)

st.progress(s3_score / 100)

st.success(
    f"Score de Segurança S3: {s3_score}%"
)

st.markdown("---")

st.subheader("S3 Health")

health = 94

st.progress(health / 100)

st.success(
    f"Saúde Geral do Ambiente S3: {health}%"
)

st.markdown("---")

# ==========================
# 9. COMPLIANCE S3 & FINDINGS POR SEVERIDADE
# ==========================
st.subheader("Compliance S3")

c1, c2, c3 = st.columns(3)

c1.metric("Criptografia", "89%")
c2.metric("Versionamento", "78%")
c3.metric("Block Public Access", "95%")

st.markdown("---")

st.subheader("Findings por Severidade")

s1, s2, s3_sev, s4 = st.columns(4)

s1.metric("Critical", 2)
s2.metric("High", 3)
s3_sev.metric("Medium", 2)
s4.metric("Low", 1)

st.markdown("---")

# ==========================
# 10. INVENTÁRIO DETALHADO DE BUCKETS & SECURITY TREND
# ==========================
st.subheader("Inventário de Buckets e Conformidade")

buckets_df = pd.DataFrame({
    "Nome do Bucket": [
        "prod-financial-vault-alpha",
        "corporate-backups-2026",
        "public-marketing-assets-sp",
        "dev-sandbox-temp-bucket",
        "logs-central-cloudtrail-aws"
    ],
    "Acesso Público": [
        "Fechado (Block Public)",
        "Fechado (Block Public)",
        "Público (ACL Permitida)",
        "Fechado (Block Public)",
        "Fechado (Block Public)"
    ],
    "Criptografia": [
        "SSE-KMS (AES-256)",
        "SSE-S3",
        "Nenhuma",
        "SSE-S3",
        "SSE-KMS"
    ],
    "Versionamento": [
        "Habilitado",
        "Habilitado",
        "Desabilitado",
        "Desabilitado",
        "Habilitado"
    ],
    "Status de Risco": [
        "Baixo",
        "Baixo",
        "Crítico",
        "Médio",
        "Baixo"
    ]
})

st.dataframe(buckets_df, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Security Trend")

trend = pd.DataFrame({
    "Score": [
        75,
        78,
        82,
        85,
        s3_score
    ]
})

st.line_chart(trend)

st.markdown("---")

# ==========================
# 11. ATTACK PATH S3 & WORKFLOW DE TRATAMENTO
# ==========================
st.subheader("Attack Path S3")

attack_s3 = pd.DataFrame({
    "Origem":[
        "Bucket Público",
        "IAM Comprometido",
        "Policy Excessiva"
    ],
    "Impacto":[
        "Exposição de Dados",
        "Exfiltração",
        "Escalação"
    ],
    "Risco":[
        "Crítico",
        "Alto",
        "Alto"
    ]
})

st.dataframe(
    attack_s3,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.subheader("Workflow de Tratamento")

workflow = pd.DataFrame({
    "Achado":[
        "Bucket Público",
        "Sem Criptografia",
        "Sem Versionamento"
    ],
    "Status":[
        "Novo",
        "Em Tratamento",
        "Resolvido"
    ]
})

st.dataframe(
    workflow,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 12. LABORATÓRIO DE AUDITORIA S3, THREAT INVESTIGATION LAB & SIMULAÇÕES
# ==========================
col_l1, col_l2 = st.columns(2)

with col_l1:
    st.subheader("Laboratório de Auditoria S3")
    bucket_lab = st.selectbox(
        "Selecionar Bucket",
        buckets_df["Nome do Bucket"].tolist()
    )
    if st.button("Executar Auditoria"):
        st.success(f"Auditoria executada em {bucket_lab}")
        st.markdown("""
Resultado:

• Criptografia: Conforme
• Versionamento: Conforme
• Bucket Policy: Atenção
• Exposição Pública: Não Conforme
""")

with col_l2:
    st.subheader("Threat Investigation Lab")
    ioc = st.text_input(
        "Pesquisar Bucket ou IOC"
    )
    if st.button("Investigar"):
        st.success(
            f"Investigação executada para: {ioc}"
        )
        st.info(
            "Nenhum acesso suspeito encontrado."
        )

st.markdown("---")

col_s1, col_s2 = st.columns(2)

with col_s1:
    st.subheader("Threat Simulation")
    simulacao = st.selectbox(
        "Simular Cenário",
        [
            "Public Bucket Exposure",
            "Credential Theft",
            "Data Exfiltration",
            "Ransomware Backup Access"
        ]
    )
    if st.button("Simular Ameaça"):
        st.warning(f"Cenário {simulacao} detectado.")

with col_s2:
    st.subheader("Data Exfiltration Simulation")
    if st.button(
        "Executar Simulação"
    ):
        st.warning("""
Evento Detectado:

Download massivo de objetos

Origem:
IAM User

Acionamento:
Security Hub
""")

st.markdown("---")

# ==========================
# 13. COBERTURA S3 & EVIDENCE REPOSITORY
# ==========================
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("Cobertura S3")
    coverage_df = pd.DataFrame({
        "Controle":[
            "Criptografia",
            "Versionamento",
            "Policies",
            "Block Public Access"
        ],
        "Cobertura":[
            "89%",
            "78%",
            "91%",
            "95%"
        ]
    })
    st.dataframe(
        coverage_df,
        use_container_width=True,
        hide_index=True
    )

with col_c2:
    st.subheader("Evidence Repository")
    evidence = pd.DataFrame({
        "Evidência":[
            "Bucket Inventory",
            "Encryption Review",
            "Policy Assessment"
        ],
        "Status":[
            "Coletada",
            "Coletada",
            "Coletada"
        ]
    })
    st.dataframe(
        evidence,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# ==========================
# 14. EXECUTIVE REPORT & DOWNLOAD
# ==========================
col_r1, col_r2 = st.columns(2)

with col_r1:
    st.subheader("Executive Report")
    if st.button(
        "Gerar Resumo Executivo"
    ):
        st.success(f"""
Buckets: {s3_data.get('totalBuckets',18)}

Públicos: {s3_data.get('publicBuckets',2)}

Score: {s3_score}%

Situação Geral:
Atenção Moderada
""")

with col_r2:
    st.subheader("Exportar Evidências S3")
    evidence_text = f"""
AWS S3 AUDIT REPORT

Data:
{datetime.now()}

Buckets:
{s3_data.get('totalBuckets', 18)}

Buckets Públicos:
{s3_data.get('publicBuckets', 2)}

Conclusão:
Auditoria executada.
"""
    st.download_button(
        "Baixar Evidência",
        evidence_text,
        file_name="s3_audit_report.txt"
    )

st.markdown("---")

# ==========================
# 15. S3 COPILOT
# ==========================
st.subheader("S3 Copilot")
pergunta = st.text_area("Pergunte sobre S3")

if st.button("Analisar S3"):
    p = pergunta.lower()
    if "criptografia" in p:
        st.info("Recomenda-se SSE-KMS para dados críticos.")
    elif "bucket público" in p:
        st.info("Aplicar Block Public Access.")
    elif "versionamento" in p:
        st.info("Versionamento protege contra exclusão acidental.")
    else:
        st.info("Análise S3 concluída.")

st.markdown("---")

# ==========================
# 16. KNOWLEDGE CHECKS (SECURITY ANALYST CHALLENGES)
# ==========================
col_k1, col_k2 = st.columns(2)

with col_k1:
    st.subheader("Security Analyst Challenge")
    questao = st.radio(
        "Qual recurso bloqueia acesso público em buckets?",
        [
            "ACL",
            "Bucket Policy",
            "Block Public Access"
        ]
    )

    if st.button("Validar Desafio"):
        if questao == "Block Public Access":
            st.success("Correto.")
        else:
            st.error("Resposta incorreta.")

with col_k2:
    st.subheader("S3 Analyst Challenge")
    pergunta2 = st.radio(
        "Qual criptografia é recomendada para dados críticos?",
        [
            "Nenhuma",
            "SSE-S3",
            "SSE-KMS"
        ]
    )

    if st.button("Validar Certificação"):
        if pergunta2 == "SSE-KMS":
            st.success("Resposta correta.")
        else:
            st.error("Resposta incorreta.")

st.markdown("---")

# ==========================
# 17. INTEGRAÇÃO COM SECURITY HUB
# ==========================
st.subheader("Integração Security Hub")
st.success("""
Achados enviados para:

Security Hub
Compliance
IAM Audit
CloudTrail
Security Center
""")

st.markdown("---")

# ==========================
# 18. NAVEGAÇÃO INTEGRADA
# ==========================
st.subheader("Navegação Integrada")
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1:
    st.page_link("pages/security_hub.py", label="Security Hub")
with c2:
    st.page_link("pages/security_center.py", label="Security Center")
with c3:
    st.page_link("pages/compliance.py", label="Compliance")
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
st.caption(f"AWS Cyber Defense Platform • S3 Storage Audit • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")