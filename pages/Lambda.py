import streamlit as st
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Lambda Security Center",
    page_icon="⚡",
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
    <h1>⚡ Lambda Security Center</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Monitoramento de funções serverless, análise de permissões IAM (IAM Roles), variáveis de ambiente e segurança de runtime.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total de Funções", "5")

with c2:
    st.metric("Permissões Excessivas", "1", delta="Atenção", delta_color="inverse")

with c3:
    st.metric("VPC Conectada", "3/5")

with c4:
    st.metric("Lambda Security Score", "85/100")

# ==========================
# SCORE
# ==========================
st.markdown("---")
st.subheader("📊 Serverless Security Score")

lambda_score = 85
st.progress(lambda_score / 100)
st.metric("Pontuação Lambda", f"{lambda_score}/100")

# ==========================
# EXECUTIVE SUMMARY
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O ambiente possui **5 funções AWS Lambda** ativas monitoradas. 
Foi identificada uma função com políticas de execução (*IAM Role*) excessivamente permissivas (uso de wildcard `*`), além de variáveis de ambiente sem criptografia KMS dedicada.

Recomenda-se aplicar o princípio do privilégio mínimo nas funções e isolar o acesso a recursos sensíveis.
""")

# ==========================
# INVENTÁRIO DE FUNÇÕES
# ==========================
st.markdown("---")
st.subheader("⚡ Inventário de Funções Lambda")

lambda_df = pd.DataFrame({
    "Função": [
        "auth-api-prod",
        "process-payments",
        "data-sync-worker",
        "image-resizer",
        "legacy-webhook"
    ],
    "Runtime": [
        "Node.js 20.x",
        "Python 3.11",
        "Python 3.11",
        "Node.js 18.x",
        "Python 3.9"
    ],
    "IAM Role": [
        "role-auth-limited",
        "role-payments-admin ⚠️",
        "role-sync-s3",
        "role-resizer",
        "role-webhook"
    ],
    "VPC Config": [
        "Sim",
        "Sim",
        "Sim",
        "Não",
        "Não"
    ],
    "Risco": [
        "Baixo",
        "Alto",
        "Baixo",
        "Baixo",
        "Médio"
    ]
})

st.dataframe(
    lambda_df,
    use_container_width=True
)

# ==========================
# ALERTAS
# ==========================
st.markdown("---")
st.subheader("🚨 Alertas de Segurança")

st.error("""
**Função:** `process-payments`  
**Problema:** A política IAM associada (`role-payments-admin`) possui permissões globais excessivas (`AdministratorAccess` ou `*` em ações de DynamoDB/S3).  
**Impacto:** Comprometimento da função pode resultar em escalação de privilégios e vazamento generalizado de dados financeiros.  
**Correção:** Restringir a política IAM estritamente aos recursos necessários.
""")

st.warning("""
**Função:** `legacy-webhook`  
**Problema:** Runtime desatualizada (`Python 3.9`) e variáveis de ambiente contendo segredos em texto plano sem chave KMS dedicada.  
**Correção:** Atualizar o runtime para uma versão suportada e criptografar o payload de configuração.
""")

# ==========================
# CHECKLIST
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Segurança Serverless")

st.checkbox("Princípio do privilégio mínimo aplicado nas IAM Roles", value=False, disabled=True)
st.checkbox("Variáveis de ambiente confidenciais criptografadas com KMS", value=True, disabled=True)
st.checkbox("Funções sensíveis isoladas dentro de VPC Privada", value=True, disabled=True)
st.checkbox("Inspeção de dependências e vulnerabilidades ativa", value=True, disabled=True)

# ==========================
# AWS CLI
# ==========================
st.markdown("---")
st.subheader("💻 Exemplo de Correção via AWS CLI")

st.code("""
aws lambda update-function-configuration \\
    --function-name process-payments \\
    --role arn:aws:iam::123456789012:role/role-payments-least-privilege
""", language="bash")

# ==========================
# ROADMAP
# ==========================
st.markdown("---")
st.subheader("🛠️ Plano de Correção")

st.markdown("""
1. **Refatorar IAM Roles:** Eliminar permissões com coringa (`*`) nas funções críticas.
2. **Atualização de Runtimes:** Migrar funções legadas para versões LTS (Python 3.11+ / Node.js 20+).
3. **Criptografia de Segredos:** Integrar o AWS Secrets Manager ou KMS Parameter Store.
4. **Isolamento de Rede:** Conectar workers em subnets privadas com Network Security Groups ajustados.
5. **Monitoramento de Execução:** Habilitar logs estruturados e alertas no CloudWatch.
""")

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • Lambda Security Center")