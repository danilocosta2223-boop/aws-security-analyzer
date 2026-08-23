import streamlit as st
import json
import os
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="IAM Security Center",
    page_icon="👤",
    layout="wide"
)

# ==========================
# ESTILO VISUAL CUSTOMIZADO (CSS)
# ==========================
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px; border-radius: 16px; border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4); margin-bottom: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# CARREGAR JSON
# ==========================
json_file = "reports/security_report.json"

if not os.path.exists(json_file):
    st.error(f"⚠️ O arquivo `{json_file}` não foi encontrado.")
    st.stop()

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
    <div class="hero-card">
        <h1>👤 IAM Security Center</h1>
        <p style="color: #94a3b8; margin: 0; font-size: 15px;">Gestão de identidade, autenticação, privilégios e credenciais AWS</p>
    </div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Usuários IAM", "18")
with col2:
    st.metric("MFA Ativado", "16")
with col3:
    st.metric("Sem MFA", "2", delta="Atenção", delta_color="inverse")
with col4:
    st.metric("Access Keys Antigas", "2", delta="Risco", delta_color="inverse")

# ==========================
# SCORE IAM
# ==========================
iam_score = 75

st.markdown("---")
st.subheader("📊 IAM Security Score")
st.progress(iam_score / 100)
st.metric("Pontuação IAM", f"{iam_score}/100")

# ==========================
# RESUMO EXECUTIVO
# ==========================
iam_findings = [
    item for item in data.get("findings", [])
    if item["service"].upper() == "IAM"
]

st.markdown("---")
st.subheader("📋 Executive Summary")

st.info(f"""
O módulo IAM identificou **{len(iam_findings)} achado(s)** relacionado(s) à gestão de identidade e acesso.

Principais riscos:

• Usuários sem MFA

• Access Keys antigas

• Possíveis permissões excessivas

Recomenda-se correção imediata dos itens classificados como críticos.
""")

# ==========================
# TABELA DE USUÁRIOS
# ==========================
st.markdown("---")
st.subheader("👥 Usuários IAM")

usuarios = pd.DataFrame({
    "Usuário": ["admin-user", "security-admin", "developer-user"],
    "MFA": ["Não", "Sim", "Sim"],
    "Access Key": ["Ativa", "Ativa", "Ativa"],
    "Status": ["Crítico", "OK", "OK"]
})

st.dataframe(usuarios, use_container_width=True)

# ==========================
# ACHADOS IAM (Filtrado do JSON)
# ==========================
st.markdown("---")
st.subheader("🚨 Achados de Segurança (IAM)")

if iam_findings:
    for finding in iam_findings:
        st.error(f"""
**Recurso Afetado:** `{finding['resource']}`  
**Problema:** {finding['issue']}  
**Recomendação:** {finding['recommendation']}
        """)
else:
    st.success("🟢 Nenhum problema crítico de IAM encontrado no relatório atual.")

# ==========================
# CHECKLIST
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Postura IAM")

st.checkbox("Conta Root protegida com MFA de Hardware", value=True, disabled=True)
st.checkbox("CloudTrail ativo globalmente", value=True, disabled=True)
st.checkbox("Política de senha forte habilitada", value=True, disabled=True)
st.checkbox("MFA obrigatório para todos os usuários IAM", value=False, disabled=True)

# ==========================
# RISCOS
# ==========================
st.markdown("---")
st.subheader("⚠️ Principais Riscos Identificados")

st.warning("🔒 **MFA desabilitado:** Aumenta significativamente o risco de comprometimento de credenciais em caso de vazamento de senhas.")
st.warning("🔑 **Access Keys antigas:** Chaves de acesso de longa duração sem rotação podem estar expostas ou comprometidas.")
st.warning("⚡ **Permissões excessivas:** Políticas com privilégios amplos abrem margem para escalação de privilégios na conta.")

# ==========================
# PLANO DE CORREÇÃO
# ==========================
st.markdown("---")
st.subheader("🛠️ Plano de Correção Recomendado")

st.markdown("""
1. **Forçar MFA:** Enviar notificação ou aplicar política SCP/IAM exigindo MFA para todos os usuários.
2. **Rotacionar Chaves:** Identificar e revogar `Access Keys` com mais de 90 dias de uso.
3. **Princípio do Menor Privilégio:** Auditar políticas do tipo `AdministratorAccess` associadas a usuários humanos e substituí-las por funções baseadas em tarefas (`IAM Roles`).
4. **Revisão Periódica:** Agendar varreduras semanais automatizadas com o pipeline de segurança.
""")

# ==========================
# EXEMPLO AWS CLI
# ==========================
st.markdown("---")
st.subheader("💻 Exemplo de Correção")

st.code(
    """
aws iam enable-mfa-device \\
    --user-name admin-user
    """,
    language="bash"
)

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>AWS Cyber Defense Platform • Módulo IAM</p>", unsafe_allow_html=True)