import streamlit as st
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================

st.set_page_config(
    page_title="RDS Security Center",
    page_icon="🗄️",
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
    <h1>🗄️ RDS Security Center</h1>
    <p style="color:#94a3b8;">
        Monitoramento de bancos de dados, criptografia,
        backups e exposição de acesso.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Instâncias RDS", "4")

with c2:
    st.metric("Criptografadas", "3")

with c3:
    st.metric(
        "Expostas Publicamente",
        "1",
        delta="Risco",
        delta_color="inverse"
    )

with c4:
    st.metric(
        "RDS Security Score",
        "91/100"
    )

# ==========================
# SCORE
# ==========================

st.markdown("---")

st.subheader("📊 Database Security Score")

score = 91

st.progress(score / 100)

# ==========================
# EXECUTIVE SUMMARY
# ==========================

st.markdown("---")

st.subheader("📋 Executive Summary")

st.info("""
O ambiente possui 4 instâncias RDS monitoradas.

Foi identificada uma instância com acesso
público habilitado, aumentando a superfície
de ataque da organização.

A recomendação é manter bancos de dados
em sub-redes privadas e criptografados.
""")

# ==========================
# INVENTÁRIO
# ==========================

st.markdown("---")

st.subheader("🗄️ Inventário RDS")

rds_df = pd.DataFrame({
    "Instância": [
        "db-production",
        "db-finance",
        "db-analytics",
        "db-test"
    ],
    "Engine": [
        "PostgreSQL",
        "MySQL",
        "PostgreSQL",
        "MySQL"
    ],
    "Criptografia": [
        "KMS",
        "KMS",
        "KMS",
        "Desabilitada"
    ],
    "Public Access": [
        "Não",
        "Não",
        "Não",
        "Sim"
    ],
    "Risco": [
        "Baixo",
        "Baixo",
        "Baixo",
        "Alto"
    ]
})

st.dataframe(
    rds_df,
    use_container_width=True
)

# ==========================
# ALERTAS
# ==========================

st.markdown("---")

st.subheader("🚨 Alertas de Segurança")

st.error("""
Instância: db-test

Problema:
Acesso público habilitado.

Impacto:
Maior exposição a tentativas de acesso indevido.

Correção:
Mover para subnet privada e desabilitar Public Access.
""")

st.warning("""
Instância: db-test

Problema:
Criptografia desabilitada.

Correção:
Utilizar AWS KMS.
""")

# ==========================
# BACKUP E RECOVERY
# ==========================

st.markdown("---")

st.subheader("💾 Backup & Recovery")

backup_df = pd.DataFrame({
    "Instância": [
        "db-production",
        "db-finance",
        "db-analytics",
        "db-test"
    ],
    "Backup": [
        "Ativo",
        "Ativo",
        "Ativo",
        "Ativo"
    ],
    "Retenção": [
        "30 dias",
        "30 dias",
        "15 dias",
        "7 dias"
    ]
})

st.dataframe(
    backup_df,
    use_container_width=True
)

# ==========================
# CHECKLIST
# ==========================

st.markdown("---")

st.subheader("✅ Checklist RDS")

st.checkbox(
    "Criptografia KMS habilitada",
    value=False,
    disabled=True
)

st.checkbox(
    "Backups automáticos",
    value=True,
    disabled=True
)

st.checkbox(
    "Instâncias privadas",
    value=False,
    disabled=True
)

st.checkbox(
    "Logs habilitados",
    value=True,
    disabled=True
)

# ==========================
# AWS CLI
# ==========================

st.markdown("---")

st.subheader("💻 Exemplo AWS CLI")

st.code("""
aws rds modify-db-instance \
--db-instance-identifier db-test \
--no-publicly-accessible
""", language="bash")

# ==========================
# ROADMAP
# ==========================

st.markdown("---")

st.subheader("🛠️ Plano de Correção")

st.markdown("""
1. Desabilitar acesso público.

2. Habilitar criptografia KMS.

3. Revisar Security Groups.

4. Aumentar retenção de backups.

5. Habilitar monitoramento avançado.
""")

# ==========================
# RODAPÉ
# ==========================

st.markdown("---")

st.caption(
    "AWS Cyber Defense Platform • RDS Security Center"
)