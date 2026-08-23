import streamlit as st
import json
import os

# ==========================
# CONFIGURAÇÃO
# ==========================

st.set_page_config(
    page_title="Executive View",
    page_icon="📈",
    layout="wide"
)

# ==========================
# CARREGAR JSON
# ==========================

json_file = "reports/security_report.json"

if not os.path.exists(json_file):
    st.error("Arquivo security_report.json não encontrado.")
    st.stop()

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ==========================
# CÁLCULO DE SCORE
# ==========================

def calculate_score(summary):
    score = 100
    score -= summary.get("critical", 0) * 25
    score -= summary.get("high", 0) * 15
    score -= summary.get("medium", 0) * 5
    score -= summary.get("low", 0) * 1
    return max(score, 0)

score = calculate_score(
    data["security_hub_summary"]
)

# ==========================
# CABEÇALHO
# ==========================

st.title("📈 Executive Dashboard")

st.caption(
    f"Ambiente AWS | Região: {data['region']}"
)

# ==========================
# KPIs EXECUTIVOS
# ==========================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Security Score",
        f"{score}/100"
    )

with k2:
    st.metric(
        "Total Findings",
        data["total_findings"]
    )

with k3:
    st.metric(
        "Critical Risks",
        data["security_hub_summary"]["critical"]
    )

with k4:
    st.metric(
        "High Risks",
        data["security_hub_summary"]["high"]
    )

# ==========================
# RESUMO EXECUTIVO
# ==========================

st.markdown("---")

st.subheader("🎯 Executive Summary")

if score >= 90:
    risk = "BAIXO"
elif score >= 70:
    risk = "MODERADO"
else:
    risk = "ALTO"

st.info(f"""
A organização apresenta um Security Score de **{score}/100**.

O nível de risco atual é classificado como **{risk}**.

Foram identificados **{data['total_findings']} achados de segurança** durante a última avaliação.

Prioridade máxima para correção dos itens classificados como **CRITICAL** e **HIGH**.
""")

# ==========================
# FRAMEWORKS
# ==========================

st.markdown("---")

st.subheader("📚 Compliance Frameworks")

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.metric(
        "CIS Benchmark",
        "91%"
    )

with f2:
    st.metric(
        "NIST CSF",
        "94%"
    )

with f3:
    st.metric(
        "ISO 27001",
        "92%"
    )

with f4:
    st.metric(
        "LGPD",
        "96%"
    )

# ==========================
# RISCOS PRINCIPAIS
# ==========================

st.markdown("---")

st.subheader("🚨 Top Riscos Identificados")

for finding in data["findings"]:

    severity = finding["severity"]

    if severity in ["CRITICAL", "HIGH"]:
        st.warning(
            f"[{severity}] "
            f"{finding['service']} | "
            f"{finding['issue']}"
        )

# ==========================
# PLANO EXECUTIVO
# ==========================

st.markdown("---")

st.subheader("🛠️ Plano Estratégico")

st.markdown("""
### Curto Prazo

- Ativar MFA para contas administrativas
- Revisar Security Groups expostos
- Corrigir findings críticos

### Médio Prazo

- Expandir cobertura Security Hub
- Automatizar remediação
- Fortalecer trilhas CloudTrail

### Longo Prazo

- Atingir Security Score acima de 95
- Implementar Zero Trust
- Consolidar aderência NIST e ISO 27001
""")

# ==========================
# RODAPÉ
# ==========================

st.markdown("---")

st.caption(
    "AWS Cyber Defense Platform • Executive View"
)