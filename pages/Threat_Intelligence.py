import streamlit as st
import json
import os
import pandas as pd

# ==========================
# CONFIGURAÇÃO
# ==========================

st.set_page_config(
    page_title="Threat Intelligence",
    page_icon="🚨",
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
# CABEÇALHO
# ==========================

st.title("🚨 Threat Intelligence Center")

st.caption(
    f"Região AWS: {data['region']} | Scan: {data['timestamp']}"
)

# ==========================
# MÉTRICAS
# ==========================

critical = data["security_hub_summary"]["critical"]
high = data["security_hub_summary"]["high"]
medium = data["security_hub_summary"]["medium"]
low = data["security_hub_summary"]["low"]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("🔴 Critical", critical)

with c2:
    st.metric("🟠 High", high)

with c3:
    st.metric("🟡 Medium", medium)

with c4:
    st.metric("🟢 Low", low)

# ==========================
# DISTRIBUIÇÃO
# ==========================

st.subheader("📊 Distribuição de Ameaças")

chart_data = pd.DataFrame(
    {
        "Quantidade": [
            critical,
            high,
            medium,
            low
        ]
    },
    index=[
        "Critical",
        "High",
        "Medium",
        "Low"
    ]
)

st.bar_chart(chart_data)

# ==========================
# ACHADOS
# ==========================

st.subheader("🚨 Findings Detectados")

for finding in data["findings"]:

    severity = finding["severity"]

    if severity == "CRITICAL":
        st.error(
            f"{finding['service']} - {finding['issue']}"
        )

    elif severity == "HIGH":
        st.warning(
            f"{finding['service']} - {finding['issue']}"
        )

    else:
        st.info(
            f"{finding['service']} - {finding['issue']}"
        )

# ==========================
# TABELA DETALHADA
# ==========================

st.subheader("📋 Threat Investigation")

rows = []

for finding in data["findings"]:

    rows.append(
        {
            "Serviço": finding["service"],
            "Severidade": finding["severity"],
            "Recurso": finding["resource"],
            "Problema": finding["issue"],
            "Correção": finding["recommendation"]
        }
    )

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True
)

# ==========================
# AMEAÇAS MAIS PERIGOSAS
# ==========================

st.subheader("🎯 Top Risks")

high_risks = [
    f for f in data["findings"]
    if f["severity"] in ["CRITICAL", "HIGH"]
]

for item in high_risks:

    st.markdown(
        f"""
### {item['service']}

**Severidade:** {item['severity']}

**Problema:** {item['issue']}

**Recurso:** `{item['resource']}`

**Recomendação:** {item['recommendation']}
"""
    )

# ==========================
# INTELIGÊNCIA
# ==========================

st.subheader("🧠 Threat Intelligence Assessment")

if critical > 0:
    st.error(
        "Existem riscos críticos que exigem correção imediata."
    )
elif high > 0:
    st.warning(
        "Existem riscos elevados que devem ser priorizados."
    )
else:
    st.success(
        "Nenhuma ameaça crítica identificada."
    )

# ==========================
# RODAPÉ
# ==========================

st.markdown("---")

st.caption(
    "AWS Cyber Defense Platform • Threat Intelligence Center"
)