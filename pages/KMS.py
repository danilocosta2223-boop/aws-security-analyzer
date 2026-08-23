import streamlit as st
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="KMS & Encryption Center",
    page_icon="🔑",
    layout="wide"
)

# ==========================
# ESTILO VISUAL
# ==========================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #f8fafc;
}

.hero-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 20px;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>🔑 KMS & Encryption Center</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Gestão centralizada de chaves criptográficas, rotação automática, políticas de acesso e proteção de dados para S3, RDS, Lambda, EBS e Secrets Manager.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total de Chaves (CMKs)", "6")

with c2:
    st.metric("Rotação Desativada", "1", delta="Atenção", delta_color="inverse")

with c3:
    st.metric("Integrações Ativas", "S3 / RDS / Secrets")

with c4:
    st.metric("KMS Security Score", "94/100")

# ==========================
# SCORE
# ==========================
st.markdown("---")
st.subheader("📊 Encryption Security Score")

kms_score = 94
st.progress(kms_score / 100)
st.metric("Pontuação KMS", f"{kms_score}/100")

# ==========================
# EXECUTIVE SUMMARY
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O ambiente gerencia **6 Customer Master Keys (CMKs)** no AWS KMS. 
A maioria das chaves críticas de produção possui rotação automática habilitada e políticas restritas. 

Foi identificada uma chave legada utilizada pelo **Secrets Manager** sem rotação ativa há mais de 365 dias, o que representa um risco de conformidade. Recomenda-se ativar a política de rotação automática e auditar as permissões de decriptação (`kms:Decrypt`).
""")

# ==========================
# INVENTÁRIO DE CHAVES KMS
# ==========================
st.markdown("---")
st.subheader("🔑 Inventário de Chaves (CMKs)")

kms_df = pd.DataFrame({
    "Alias / Chave": [
        "alias/prod-database-key",
        "alias/prod-s3-vault",
        "alias/lambda-env-key",
        "alias/secrets-manager-prod",
        "alias/ebs-volumes-key",
        "alias/legacy-app-key"
    ],
    "Serviço Vinculado": [
        "RDS",
        "S3",
        "Lambda",
        "Secrets Manager",
        "EC2 / EBS",
        "Legado / Custom"
    ],
    "Rotação Automática": [
        "Ativada",
        "Ativada",
        "Ativada",
        "Desativada ⚠️",
        "Ativada",
        "Desativada"
    ],
    "Origem": [
        "AWS KMS",
        "AWS KMS",
        "AWS KMS",
        "AWS KMS",
        "AWS KMS",
        "Importada"
    ],
    "Risco": [
        "Baixo",
        "Baixo",
        "Baixo",
        "Alto",
        "Baixo",
        "Médio"
    ]
})

st.dataframe(
    kms_df,
    use_container_width=True
)

# ==========================
# ALERTAS
# ==========================
st.markdown("---")
st.subheader("🚨 Alertas de Segurança")

st.error("""
**Chave KMS:** `alias/secrets-manager-prod`  
**Problema:** A rotação automática de chaves está desativada para uma CMK que protege segredos críticos de produção.  
**Impacto:** Em caso de comprometimento prolongado do material da chave, dados sensíveis armazenados no Secrets Manager ficam vulneráveis a ataques de descriptografia em lote.  
**Correção:** Habilitar imediatamente a rotação anual automática via AWS KMS.
""")

st.warning("""
**Chave KMS:** `alias/legacy-app-key`  
**Problema:** Utiliza chave com material importado cuja validade de expiração não está configurada.  
**Correção:** Definir política de expiração do material ou migrar para chaves gerenciadas nativamente pelo AWS KMS.
""")

# ==========================
# CHECKLIST
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Criptografia e Governança")

st.checkbox("Rotação automática anual habilitada para todas as CMKs de produção", value=False, disabled=True)
st.checkbox("Políticas de chave restritas ao menor privilégio (sem wildcard '*')", value=True, disabled=True)
st.checkbox("Integração ativa e auditada com AWS Secrets Manager", value=True, disabled=True)
st.checkbox("Logs do CloudTrail habilitados para eventos do KMS (`Decrypt`/`Encrypt`)", value=True, disabled=True)

# ==========================
# AWS CLI
# ==========================
st.markdown("---")
st.subheader("💻 Exemplo de Correção via AWS CLI")

st.code("""
aws kms enable-key-rotation \
    --key-id alias/secrets-manager-prod
""", language="bash")

# ==========================
# DISTRIBUIÇÃO DE RISCO
# ==========================
st.markdown("---")
st.subheader("📈 Distribuição de Risco")

risk_df = pd.DataFrame({
    "Risco": [
        "Baixo",
        "Médio",
        "Alto"
    ],
    "Quantidade": [
        4,
        1,
        1
    ]
})

st.bar_chart(
    risk_df.set_index("Risco")
)

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • KMS & Encryption Center")