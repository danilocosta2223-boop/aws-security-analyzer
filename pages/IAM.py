import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="IAM Security | AWS Cyber Defense Platform",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (30s)
# ==========================================
st_autorefresh(interval=30000, key="iam_view_refresh")

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

    h1, h2, h3, h4 {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HERO CARD - GESTÃO DE IAM
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>IAM Security & Access Governance</h1>
    <p style="color:#9ca3af; margin: 0; font-size: 15px;">
        Auditoria contínua de identidades, usuários, políticas de privilégios e rotação de credenciais na AWS.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Ativo &nbsp;|&nbsp; 
    <b>Última varredura IAM:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 5. IAM MISSION CONTROL (Métricas Principais)
# ==========================================
st.subheader("IAM Mission Control")

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Usuários Totais", "42")
m2.metric("Sem MFA Ativo", "3", delta="-1", delta_color="inverse")
m3.metric("Chaves > 90 Dias", "5", delta="+2", delta_color="inverse")
m4.metric("Políticas Admin", "8")
m5.metric("Compliance Score", "89%")

st.markdown("---")

# ==========================================
# 6. IAM HEALTH SCORE & IAM RISK SCORE
# ==========================================
st.subheader("IAM Health Score")

iam_score = 89
st.progress(iam_score / 100)
st.success(f"Nível de Saúde de Acessos: {iam_score}%")

st.markdown("---")

st.subheader("IAM Risk Score")

risk_score = 82

st.progress(risk_score / 100)
st.error(
f"IAM Risk Score: {risk_score}%"
)

st.markdown("---")

# ==========================================
# 7. FILTROS DE ANÁLISE DE IDENTIDADES
# ==========================================
st.subheader("Filtros de Identidades")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filtro_mfa = st.selectbox("Status de MFA", ["Todos", "Ativo", "Inativo (Risco)"])
with col_f2:
    filtro_tipo = st.selectbox("Tipo de Credencial", ["Todos", "Usuário IAM", "Role / Service Account", "Access Key"])
with col_f3:
    filtro_status_chave = st.selectbox("Idade da Chave", ["Todos", "Recente (< 30 dias)", "Alerta (> 90 dias)"])

st.markdown("---")

# ==========================================
# 8. BASE DE DADOS DE USUÁRIOS E CREDENCIAIS (MOCK)
# ==========================================
iam_df = pd.DataFrame({
    "Usuário / Entidade": [
        "admin-devops",
        "suporte-sistema",
        "pipeline-ci-cd",
        "joao.silva",
        "maria.costa",
        "lambda-executor-role"
    ],
    "Tipo": [
        "Usuário IAM",
        "Usuário IAM",
        "Access Key",
        "Usuário IAM",
        "Usuário IAM",
        "Role / Service Account"
    ],
    "MFA": [
        "Ativo",
        "Inativo",
        "N/A",
        "Ativo",
        "Inativo",
        "N/A"
    ],
    "Último Acesso": [
        "Há 10 minutos",
        "Há 2 dias",
        "Há 1 hora",
        "Há 5 dias",
        "Há 45 dias",
        "Em tempo real"
    ],
    "Risco": [
        "Baixo",
        "Critical",
        "Medium",
        "Baixo",
        "High",
        "Baixo"
    ]
})

# Aplicando Filtros Básicos
df_iam_filtrado = iam_df.copy()
if filtro_mfa == "Ativo":
    df_iam_filtrado = df_iam_filtrado[df_iam_filtrado["MFA"] == "Ativo"]
elif filtro_mfa == "Inativo (Risco)":
    df_iam_filtrado = df_iam_filtrado[df_iam_filtrado["MFA"] == "Inativo"]

# ==========================================
# 9. TABELA PRINCIPAL DE IDENTIDADES
# ==========================================
st.subheader("Auditoria de Identidades e Contas")

st.dataframe(
    df_iam_filtrado,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 10. IAM COMPLIANCE CENTER
# ==========================================
st.subheader("IAM Compliance Center")

compliance_df = pd.DataFrame({
"Controle": [
"MFA",
"Password Policy",
"Access Keys",
"Least Privilege"
],
"Compliance": [
"92%",
"100%",
"85%",
"88%"
]
})

st.dataframe(
compliance_df,
use_container_width=True,
hide_index=True
)

st.markdown("---")

# ==========================================
# 11. PRIVILEGED ACCESS REVIEW
# ==========================================
st.subheader("Privileged Access Review")

admin_df = pd.DataFrame({
"Conta": [
"admin-devops",
"root-account",
"cloud-admin"
],
"Permissão": [
"AdministratorAccess",
"Full Access",
"AdministratorAccess"
]
})

st.dataframe(
admin_df,
use_container_width=True,
hide_index=True
)

st.markdown("---")

# ==========================================
# 12. IAM THREAT EXPOSURE
# ==========================================
st.subheader("IAM Threat Exposure")

exposure_df = pd.DataFrame({
"Risco": [
"Sem MFA",
"Access Key Antiga",
"Admin Excessivo"
],
"Quantidade": [
3,
5,
8
]
})

st.bar_chart(
exposure_df.set_index("Risco")
)

st.markdown("---")

# ==========================================
# 13. IDENTITY INTELLIGENCE
# ==========================================
st.subheader("Identity Intelligence")

st.info("""
Resumo Executivo

• 3 usuários sem MFA.

• 5 chaves acima de 90 dias.

• 8 permissões administrativas.

• Recomenda-se aplicar menor privilégio.
""")

st.markdown("---")

# ==========================================
# 14. ACCESS KEY MANAGEMENT
# ==========================================
st.subheader("Access Key Management")

keys_df = pd.DataFrame({
"Usuário": [
"pipeline-ci-cd",
"backup-service",
"integration-api"
],
"Idade": [
"120 dias",
"15 dias",
"95 dias"
],
"Status": [
"Rotacionar",
"OK",
"Rotacionar"
]
})

st.dataframe(
keys_df,
use_container_width=True,
hide_index=True
)

st.markdown("---")

# ==========================================
# 15. IAM EXECUTIVE REPORT
# ==========================================
st.subheader("IAM Executive Report")

report = f"""
IAM SECURITY REPORT

Usuários:
42

Sem MFA:
3

Access Keys >90 dias:
5

Políticas Admin:
8

IAM Health:
89%
"""

st.download_button(
"📥 Baixar Relatório IAM",
report,
file_name="iam_report.txt"
)

st.markdown("---")

# ==========================================
# 16. IAM COPILOT (Assistente Inteligente)
# ==========================================
st.subheader("IAM Copilot")

iam_question = st.text_area("Pergunte sobre políticas, acessos ou remediação de usuários IAM:")

if st.button("Analisar Acessos via Copilot"):
    q = iam_question.lower()
    if "mfa" in q:
        st.info(
        "Existem 3 contas sem MFA ativo."
        )
    elif "risco" in q:
        st.info(
        "O principal risco é MFA ausente e excesso de privilégios."
        )
    elif "key" in q or "chave" in q:
        st.info(
        "Existem chaves acima de 90 dias que precisam de rotação."
        )
    elif "privilegio" in q or "admin" in q:
        st.info("Foram detectadas 8 políticas com privilégios de AdministratorAccess. Considere aplicar o princípio do menor privilégio (PoLP).")
    else:
        st.info("Análise de segurança IAM concluída. Nenhuma anomalia severa fora do padrão mapeado foi encontrada.")

st.markdown("---")

# ==========================================
# 17. NAVEGAÇÃO INTEGRADA
# ==========================================
st.subheader("Navegação Integrada")

n1, n2, n3, n4, n5, n6 = st.columns(6)

with n1:
    st.page_link("pages/security_center.py", label="Security Center")
with n2:
    st.page_link("pages/security_hub.py", label="Security Hub")
with n3:
    st.page_link("pages/security_copilot.py", label="Security Copilot")
with n4:
    st.page_link("pages/threat_intelligence.py", label="Threat Intelligence")
with n5:
    st.page_link("pages/compliance.py", label="Compliance")
with n6:
    st.page_link("pages/history.py", label="Audit History")

# ==========================================
# RODAPÉ DO MÓDULO
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • IAM Security Module • Todos os direitos reservados © {datetime.now().year} • Sincronizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")