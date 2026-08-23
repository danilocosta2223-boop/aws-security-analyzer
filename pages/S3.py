import streamlit as st
import pandas as pd
import json
import os

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="S3 Security Center",
    page_icon="☁️",
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
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ==========================
# CARREGAR DADOS DO RELATÓRIO (Opcional para sincronização com JSON geral)
# ==========================
json_file = "reports/security_report.json"
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    s3_findings = [item for item in data.get("findings", []) if item["service"].upper() == "S3"]
else:
    s3_findings = []

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>☁️ S3 Security Center</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Monitoramento de Buckets S3, criptografia, exposição pública e conformidade na nuvem.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Buckets", "4")

with c2:
    st.metric("Criptografados", "3")

with c3:
    st.metric(
        "Buckets Públicos",
        "1",
        delta="Atenção",
        delta_color="inverse"
    )

with c4:
    st.metric("Versionamento", "75%")

# ==========================
# RESUMO EXECUTIVO
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O ambiente possui **4 buckets S3** monitorados.

Foi identificado **1 bucket** com configuração pública inadequada e ausência de criptografia padrão.

Recomenda-se correção imediata para garantir aderência aos controles de mercado (CIS AWS Foundations Benchmark e boas práticas de segurança).
""")

# ==========================
# DADOS DOS BUCKETS
# ==========================
bucket_df = pd.DataFrame({
    "Bucket": [
        "backup-clientes",
        "logs-prod",
        "financeiro-2026",
        "website-publico"
    ],
    "Público": [
        "Não",
        "Não",
        "Não",
        "Sim"
    ],
    "Criptografia": [
        "SSE-KMS",
        "SSE-KMS",
        "SSE-S3",
        "Desabilitada"
    ],
    "Versionamento": [
        "Ativo",
        "Ativo",
        "Ativo",
        "Inativo"
    ],
    "Risco": [
        "Baixo",
        "Baixo",
        "Baixo",
        "Alto"
    ]
})

st.markdown("---")
st.subheader("📦 Inventário de Buckets S3")
st.dataframe(
    bucket_df,
    use_container_width=True
)

# ==========================
# ALERTAS
# ==========================
st.markdown("---")
st.subheader("🚨 Alertas de Segurança")

st.error("""
**Bucket:** `website-publico`  
**Problema:** Bucket com acesso público habilitado.  
**Impacto:** Exposição indevida de dados sensíveis na internet.  
**Correção:** Ativar o recurso *Block Public Access* imediatamente.
""")

st.warning("""
**Bucket:** `website-publico`  
**Problema:** Criptografia em repouso desabilitada.  
**Correção:** Habilitar SSE-KMS para criptografar os objetos armazenados.
""")

# ==========================
# CHECKLIST
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Postura S3")

st.checkbox("Block Public Access habilitado em todos os buckets", value=False, disabled=True)
st.checkbox("Criptografia SSE-KMS habilitada", value=True, disabled=True)
st.checkbox("Versionamento de objetos ativo", value=True, disabled=True)
st.checkbox("Logs de auditoria e acesso configurados", value=True, disabled=True)

# ==========================
# ROADMAP
# ==========================
st.markdown("---")
st.subheader("🛠️ Plano de Correção")

st.markdown("""
1. **Bloquear Acesso Público:** Ativar o *Block Public Access* global e específico no bucket `website-publico`.
2. **Aplicar Criptografia:** Habilitar SSE-KMS no bucket em conformidade com as diretrizes corporativas.
3. **Revisar Políticas:** Auditar ACLs e políticas de bucket (*Bucket Policies*).
4. **Habilitar Versionamento:** Garantir proteção contra exclusão acidental em 100% dos buckets críticos.
5. **Monitoramento Contínuo:** Integrar alertas automáticos via AWS Security Hub e GuardDuty.
""")

# ==========================
# EXEMPLO AWS CLI
# ==========================
st.markdown("---")
st.subheader("💻 Exemplo de Correção (AWS CLI)")

st.code(
    """
aws s3api put-public-access-block \\
    --bucket website-publico \\
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    """,
    language="bash"
)

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • S3 Security Center")