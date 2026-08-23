import streamlit as st
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="AWS Config Center",
    page_icon="⚙️",
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
    <h1>⚙️ AWS Config Center</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Governança de configuração, auditoria de recursos, monitoramento de mudanças de estado e conformidade contínua com frameworks de segurança.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Regras Avaliadas", "12")

with c2:
    st.metric("Não Conformes", "2", delta="Atenção", delta_color="inverse")

with c3:
    st.metric("Recursos Monitorados", "148")

with c4:
    st.metric("Config Compliance Score", "83/100")

# ==========================
# SCORE
# ==========================
st.markdown("---")
st.subheader("📊 Configuration Compliance Score")

config_score = 83
st.progress(config_score / 100)
st.metric("Pontuação de Conformidade", f"{config_score}/100")

# ==========================
# EXECUTIVE SUMMARY
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O **AWS Config** está ativo monitorando o histórico de alterações e avaliando o ambiente corporativo com base em **12 regras de conformidade** automatizadas. 

Foram identificadas duas violações críticas relacionadas a buckets S3 sem criptografia padrão obrigatória e grupos de segurança permitindo tráfego indevido na porta SSH (22) globalmente (`0.0.0.0/0`). Recomenda-se a remediação imediata através dos playbooks automatizados de correção.
""")

# ==========================
# INVENTÁRIO DE REGRAS AWS CONFIG
# ==========================
st.markdown("---")
st.subheader("⚙️ Inventário de Regras do AWS Config")

config_df = pd.DataFrame({
    "Nome da Regra": [
        "s3-bucket-server-side-encryption-enabled",
        "ec2-security-group-ssh-restricted",
        "iam-root-access-key-check",
        "rds-instance-public-access-check",
        "cloudtrail-enabled",
        "iam-password-policy"
    ],
    "Serviço Alvo": [
        "S3",
        "EC2 / VPC",
        "IAM",
        "RDS",
        "CloudTrail",
        "IAM"
    ],
    "Status": [
        "Não Conforme ⚠️",
        "Não Conforme ⚠️",
        "Conforme",
        "Conforme",
        "Conforme",
        "Conforme"
    ],
    "Recursos Afetados": [
        "1 Bucket",
        "1 Security Group",
        "0",
        "0",
        "0",
        "0"
    ],
    "Severidade": [
        "Alto",
        "Alto",
        "Baixo",
        "Baixo",
        "Baixo",
        "Baixo"
    ]
})

st.dataframe(
    config_df,
    use_container_width=True
)

# ==========================
# ALERTAS
# ==========================
st.markdown("---")
st.subheader("🚨 Alertas de Não Conformidade")

st.error("""
**Regra:** `s3-bucket-server-side-encryption-enabled`  
**Problema:** O bucket `corp-backup-temp-logs` foi detectado sem criptografia do lado do servidor ativada por padrão.  
**Impacto:** Risco de exposição de dados brutos armazenados em repouso.  
**Correção:** Aplicar configuração de criptografia SSE-S3 ou SSE-KMS mandatória.
""")

st.error("""
**Regra:** `ec2-security-group-ssh-restricted`  
**Problema:** O Security Group `sg-0192834756` permite acesso irrestrito na porta 22 a partir do bloco IP `0.0.0.0/0`.  
**Impacto:** Superfície de ataque exposta a tentativas de força bruta e invasão externa.  
**Correção:** Restringir as regras de entrada (Ingress) para IPs corporativos ou VPN confiável.
""")

# ==========================
# CHECKLIST
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Governança e Configuração")

st.checkbox("Gravador de Configuração ativo em todas as regiões ativas", value=True, disabled=True)
st.checkbox("Agregação multi-região/multi-conta configurada", value=True, disabled=True)
st.checkbox("Remediação automática habilitada para regras críticas via SSM", value=False, disabled=True)
st.checkbox("Notificações do Amazon SNS integradas para eventos de não conformidade", value=True, disabled=True)

# ==========================
# AWS CLI
# ==========================
st.markdown("---")
st.subheader("💻 Exemplo de Consulta via AWS CLI")

st.code("""
aws configservice get-compliance-details-by-config-rule \
    --config-rule-name s3-bucket-server-side-encryption-enabled \
    --compliance-types NON_COMPLIANT
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
        10,
        0,
        2
    ]
})

st.bar_chart(
    risk_df.set_index("Risco")
)

# ==========================
# COMPLIANCE OVERVIEW
# ==========================
st.markdown("---")

st.subheader("📊 Compliance Overview")

compliance_df = pd.DataFrame({
    "Status": [
        "Conforme",
        "Não Conforme"
    ],
    "Quantidade": [
        10,
        2
    ]
})

st.bar_chart(
    compliance_df.set_index("Status")
)

# ==========================
# AUTOMATED REMEDIATION
# ==========================
st.markdown("---")

st.subheader("🤖 Automated Remediation")

st.success("""
Playbooks automáticos disponíveis:

✅ Habilitar SSE-KMS em buckets

✅ Corrigir Security Groups

✅ Aplicar políticas IAM

✅ Corrigir configurações RDS
""")

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • AWS Config Center")