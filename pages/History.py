import streamlit as st
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================

st.set_page_config(
    page_title="Security History",
    page_icon="📈",
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
    <h1>📈 Security History Center</h1>
    <p style="color:#94a3b8;">
        Histórico da postura de segurança,
        conformidade e evolução dos riscos.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# DADOS HISTÓRICOS
# ==========================

history_df = pd.DataFrame({
    "Mês": [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago"
    ],
    "Security Score": [
        72,
        75,
        78,
        82,
        85,
        88,
        90,
        92
    ],
    "Critical Findings": [
        6,
        5,
        5,
        4,
        3,
        2,
        1,
        1
    ]
})

# ==========================
# MÉTRICAS
# ==========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Score Atual",
        "92/100",
        "+20"
    )

with c2:
    st.metric(
        "Achados Críticos",
        "1",
        "-5"
    )

with c3:
    st.metric(
        "Compliance",
        "91%"
    )

with c4:
    st.metric(
        "Tendência",
        "Positiva ✅"
    )

# ==========================
# EXECUTIVE SUMMARY
# ==========================

st.markdown("---")

st.subheader("📋 Executive Summary")

st.info("""
A postura de segurança apresentou evolução
consistente ao longo dos últimos meses.

O Security Score aumentou de 72 para 92 pontos,
enquanto os achados críticos foram reduzidos
de 6 para apenas 1 ocorrência.
""")

# ==========================
# EVOLUÇÃO DO SCORE
# ==========================

st.markdown("---")

st.subheader("📊 Evolução do Security Score")

score_chart = history_df.set_index("Mês")[
    "Security Score"
]

st.line_chart(score_chart)

# ==========================
# EVOLUÇÃO DOS RISCOS
# ==========================

st.markdown("---")

st.subheader("🚨 Evolução dos Achados Críticos")

risk_chart = history_df.set_index("Mês")[
    "Critical Findings"
]

st.bar_chart(risk_chart)

# ==========================
# HISTÓRICO DETALHADO
# ==========================

st.markdown("---")

st.subheader("📑 Histórico Consolidado")

st.dataframe(
    history_df,
    use_container_width=True
)

# ==========================
# MARCOS DE SEGURANÇA
# ==========================

st.markdown("---")

st.subheader("🏆 Principais Marcos")

st.success("""
✅ MFA habilitado para contas administrativas.
""")

st.success("""
✅ Integração do AWS GuardDuty.
""")

st.success("""
✅ Criptografia KMS implementada.
""")

st.success("""
✅ Buckets S3 protegidos com Block Public Access.
""")

st.success("""
✅ Monitoramento contínuo via AWS Config.
""")

# ==========================
# PREVISÃO
# ==========================

st.markdown("---")

st.subheader("🔮 Tendência")

st.info("""
Mantendo o ritmo atual de correções,
a projeção é atingir um Security Score
acima de 95/100 nos próximos ciclos
de auditoria.
""")

# ==========================
# RODAPÉ
# ==========================

st.markdown("---")

st.caption(
    "AWS Cyber Defense Platform • Security History Center"
)