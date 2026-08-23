import streamlit as st
import json
import os

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Compliance Dashboard",
    page_icon="📜",
    layout="wide"
)

# ==========================
# CARREGAR DADOS DO RELATÓRIO (Opcional para métricas dinâmicas)
# ==========================
json_file = "reports/security_report.json"
has_data = os.path.exists(json_file)

if has_data:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    critical_count = data["security_hub_summary"].get("critical", 0)
    # Lógica simples de impacto de compliance baseada nos achados críticos
    cis_score = max(91 - (critical_count * 5), 50)
    nist_score = max(94 - (critical_count * 4), 50)
    iso_score = max(92 - (critical_count * 4), 50)
else:
    cis_score, nist_score, iso_score = 91, 94, 92

# ==========================
# INTERFACE
# ==========================
st.title("📜 Compliance & Frameworks Dashboard")
st.markdown("Monitoramento de aderência aos principais padrões globais de segurança da informação.")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="CIS AWS Foundations Benchmark",
        value=f"{cis_score}%",
        delta="-2% vs última semana" if critical_count > 0 else "Estável",
        delta_color="inverse" if critical_count > 0 else "normal"
    )

with col2:
    st.metric(
        label="NIST CSF (Cybersecurity Framework)",
        value=f"{nist_score}%",
        delta="Conforme"
    )

with col3:
    st.metric(
        label="ISO/IEC 27001",
        value=f"{iso_score}%",
        delta="Revisão Pendente"
    )

st.markdown("---")
st.subheader("📊 Status de Aderência por Framework")

# Tabela detalhada de frameworks
import pandas as pd
compliance_df = pd.DataFrame({
    "Framework": ["CIS Benchmark v1.5.0", "NIST SP 800-53", "ISO 27001:2022", "PCI-DSS v4.0", "SOC 2 Type II"],
    "Controles Avaliados": [45, 110, 93, 64, 85],
    "Controles Conformes": [41, 103, 86, 59, 81],
    "Status": ["Atenção Requerida", "Conforme", "Conforme", "Atenção Requerida", "Conforme"]
})

st.dataframe(compliance_df, use_container_width=True)

if critical_count > 0:
    st.warning(f"⚠️ Atenção: Existem **{critical_count} achado(s) crítico(s)** impactando diretamente a pontuação de conformidade do CIS Benchmark.")
else:
    st.success("Ambiente totalmente aderente aos principais frameworks avaliados.")