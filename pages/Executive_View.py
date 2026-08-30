import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Executive View | AWS Cyber Defense Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="executive_view_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO (DARK THEME)
# ==========================================
st.markdown("""
<style>
    .stApp {
        background: #111827;
        color: #E5E7EB;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1F2937;
    }
    
    .hero-card {
        background: #1F2937;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background-color: #1F2937;
        color: #93c5fd;
        border: 1px solid #374151;
    }

    h1, h2, h3, h4 {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. HERO CARD
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>Executive View</h1>
    <p style="color:#9ca3af; margin: 0; font-size: 15px;">
        Painel executivo consolidado para tomada de decisão estratégica e visibilidade global de segurança.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status da Plataforma:</b> Operacional (High Availability) &nbsp;|&nbsp; 
    <b>Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 2. EXECUTIVE MISSION CONTROL
# ==========================================
st.subheader("Executive Mission Control")

m1, m2, m3, m4, m5, m6 = st.columns(6)

m1.metric("Security Score", "92%", delta="+2.1%")
m2.metric("Compliance", "94%", delta="Estável")
m3.metric("Threats", 3, delta="Alerta", delta_color="inverse")
m4.metric("Critical Risks", 1, delta="Atenção", delta_color="inverse")
m5.metric("Assets", 1240, delta="+12")
m6.metric("Status", "Protected")

st.markdown("---")

# ==========================================
# EXECUTIVE RISK MATRIX (Adicionado)
# ==========================================
st.subheader("Executive Risk Matrix")

r1, r2, r3, r4 = st.columns(4)

r1.metric("Critical", 1)
r2.metric("High", 3)
r3.metric("Medium", 5)
r4.metric("Low", 8)

st.markdown("---")

# ==========================================
# 3. GLOBAL SECURITY POSTURE
# ==========================================
st.subheader("Global Security Posture")

security_posture = 92

st.progress(
    security_posture / 100
)

st.success(
    f"Postura Global de Segurança: {security_posture}%"
)

st.markdown("---")

# ==========================================
# SECURITY MATURITY (Adicionado)
# ==========================================
st.subheader("Security Maturity")

maturity = 94

st.progress(maturity / 100)

st.success(
    f"Maturidade Global: {maturity}%"
)

st.markdown("---")

# ==========================================
# 4. EXECUTIVE KPIS
# ==========================================
st.subheader("Executive KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric("IAM Coverage", "96%")
k2.metric("Encryption", "99%")
k3.metric("MFA", "95%")
k4.metric("Monitoring", "100%")

st.markdown("---")

# ==========================================
# 5. RISK EXPOSURE & 6. COMPLIANCE OVERVIEW (2 COLUNAS)
# ==========================================
col_r, col_c = st.columns(2)

with col_r:
    st.subheader("Risk Exposure")
    risk_df = pd.DataFrame({
        "Categoria": [
            "IAM",
            "S3",
            "EC2",
            "Threats"
        ],
        "Riscos": [
            2,
            1,
            3,
            1
        ]
    })
    st.bar_chart(
        risk_df.set_index("Categoria")
    )

with col_c:
    st.subheader("Compliance Overview")
    compliance_df = pd.DataFrame({
        "Framework": [
            "CIS",
            "NIST",
            "ISO 27001",
            "PCI-DSS",
            "SOC2"
        ],
        "Score": [
            92,
            94,
            96,
            98,
            97
        ]
    })
    st.dataframe(
        compliance_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# ==========================================
# EXECUTIVE HEAT MAP (Adicionado)
# ==========================================
st.subheader("Executive Heat Map")

heatmap_df = pd.DataFrame({
    "Domínio": [
        "IAM",
        "Cloud",
        "Network",
        "Threats"
    ],
    "Exposição": [
        20,
        10,
        25,
        15
    ]
})

st.bar_chart(
    heatmap_df.set_index("Domínio")
)

st.markdown("---")

# ==========================================
# 7. THREAT OVERVIEW & 8. FINANCIAL OVERVIEW
# ==========================================
col_t, col_f = st.columns(2)

with col_t:
    st.subheader("Threat Overview")
    threat_df = pd.DataFrame({
        "Threat": [
            "Public Bucket",
            "No MFA",
            "Open SG"
        ],
        "Severity": [
            "Critical",
            "High",
            "Medium"
        ]
    })
    st.dataframe(
        threat_df,
        use_container_width=True,
        hide_index=True
    )

with col_f:
    st.subheader("Financial Overview")
    f1, f2, f3 = st.columns(3)
    f1.metric("AWS Cost", "$12,800")
    f2.metric("Security Tools", "$2,100")
    f3.metric("Projected Savings", "$1,500")

st.markdown("---")

# ==========================================
# 9. PLATFORM HEALTH
# ==========================================
st.subheader("Platform Health")

health = pd.DataFrame({
    "Módulo": [
        "Security Hub",
        "Threat Intelligence",
        "Compliance",
        "VM Dashboard"
    ],
    "Status": [
        "Online",
        "Online",
        "Online",
        "Online"
    ]
})

st.dataframe(
    health,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 10. EXECUTIVE INSIGHTS & 11. EXECUTIVE COPILOT (Com melhorias)
# ==========================================
col_in, col_co = st.columns(2)

with col_in:
    st.subheader("Executive Insights")
    st.info("""
    **Resumo Executivo**
    
    • Ambiente estável e monitorado.<br>
    • Compliance global acima de 90%.<br>
    • Nenhum incidente crítico em andamento.<br>
    • Threat Score adequado.<br>
    • Necessário revisar recursos sem MFA.
    """)

with col_co:
    st.subheader("Executive Copilot")
    question = st.text_area(
        "Pergunte sobre riscos, compliance ou segurança:"
    )
    
    if st.button("Executar Análise"):
        q = question.lower()
        if "risco" in q:
            st.info("O principal risco atual é a ausência de MFA em identidades periféricas.")
        elif "compliance" in q:
            st.info("A conformidade global atual é superior a 90% nos frameworks CIS e NIST.")
        elif "custo" in q:
            st.info("Existem oportunidades de otimização financeira em instâncias subutilizadas.")
        elif "ameaça" in q:
            st.info("Existem 3 ameaças monitoradas atualmente.")
        elif "mfa" in q:
            st.info("O principal desvio identificado é MFA não habilitado.")
        elif "segurança" in q:
            st.info("O ambiente possui postura de segurança de 92%.")
        else:
            st.info("Análise executiva concluída com sucesso.")

st.markdown("---")

# ==========================================
# EXECUTIVE INTELLIGENCE SCORE (Adicionado)
# ==========================================
st.subheader("Executive Intelligence Score")

intel_score = 96

st.progress(
    intel_score / 100
)

st.success(
    f"Executive Intelligence: {intel_score}%"
)

st.markdown("---")

# ==========================================
# 12. STRATEGIC RECOMMENDATIONS
# ==========================================
st.subheader("Strategic Recommendations")

recommendations = [
    "Expandir MFA obrigatório",
    "Reduzir exposição pública",
    "Automatizar remediações",
    "Fortalecer monitoramento contínuo",
    "Revisar permissões críticas"
]

for item in recommendations:
    st.success(item)

st.markdown("---")

# ==========================================
# STRATEGIC ROADMAP (Adicionado)
# ==========================================
st.subheader("Strategic Roadmap")

roadmap = pd.DataFrame({
    "Iniciativa": [
        "Expandir MFA",
        "Automação de Resposta",
        "Zero Trust",
        "Hardening EC2"
    ],
    "Prioridade": [
        "Alta",
        "Alta",
        "Média",
        "Média"
    ]
})

st.dataframe(
    roadmap,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# PLATFORM MODULES OVERVIEW (Adicionado)
# ==========================================
st.subheader("Platform Modules Overview")

module_df = pd.DataFrame({
    "Módulo": [
        "Security Center",
        "Security Hub",
        "Threat Intelligence",
        "Compliance",
        "VM Dashboard",
        "Security Copilot"
    ],
    "Status": [
        "Online",
        "Online",
        "Online",
        "Online",
        "Online",
        "Online"
    ]
})

st.dataframe(
    module_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 13. EXECUTIVE REPORT
# ==========================================
st.subheader("Executive Report")

report = """AWS CYBER DEFENSE PLATFORM - EXECUTIVE REPORT

Security Score: 92%
Compliance: 94%
Threat Score: 96%
Intelligence Score: 96%

Status: Operational
"""

st.download_button(
    "📥 Baixar Relatório Executivo",
    report,
    file_name="executive_report.txt"
)

st.markdown("---")

# ==========================================
# 14. NAVEGAÇÃO INTEGRADA
# ==========================================
st.subheader("Navegação Integrada")

n1, n2, n3, n4, n5, n6 = st.columns(6)

with n1:
    st.page_link("pages/security_center.py", label="Security Center")

with n2:
    st.page_link("pages/security_hub.py", label="Security Hub")

with n3:
    st.page_link("pages/security_copilot.py", label="Security Copilot")

with n4:
    st.page_link("pages/threat_intelligence.py", label="Threat Intelligence")

with n5:
    st.page_link("pages/compliance.py", label="Compliance")

with n6:
    st.page_link("pages/vm_dashboard.py", label="VM Dashboard")

# ==========================================
# RODAPÉ DO MÓDULO
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Executive View • Todos os direitos reservados © {datetime.now().year} • Sincronizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")