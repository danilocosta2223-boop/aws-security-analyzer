import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Audit History | AWS Cyber Defense Platform",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (30s)
# ==========================================
st_autorefresh(interval=30000, key="history_view_refresh")

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

    h1, h2, h3, h4 {
        color: #93c5fd;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HERO CARD - HISTÓRICO & AUDITORIA
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>Audit & Event History</h1>
    <p style="color:#9ca3af; margin: 0; font-size: 15px;">
        Registro imutável de eventos de segurança, alterações de compliance e execuções do Copilot.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 20px;">
    <b>Status do Log:</b> Ativo &nbsp;|&nbsp; 
    <b>Última varredura de auditoria:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# BASE DE DADOS DE HISTÓRICO (MOCK / SIMULADA)
# ==========================================
data_hoje = datetime.now()

history_df = pd.DataFrame({
    "Timestamp": [
        (data_hoje - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
        (data_hoje - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
        (data_hoje - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S'),
        (data_hoje - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        (data_hoje - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
        (data_hoje - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
    ],
    "Módulo": [
        "Security Hub",
        "IAM",
        "Compliance",
        "Threat Intelligence",
        "Security Copilot",
        "Security Hub"
    ],
    "Evento": [
        "Detecção de S3 Bucket público mitigada automaticamente",
        "Alerta de ausência de MFA para usuário IAM de suporte",
        "Varredura CIS Benchmark concluída (Score: 92%)",
        "Nova assinatura de ameaça detectada e isolada",
        "Consulta executiva realizada via Copilot sobre riscos",
        "Atualização de regras de Security Group no EC2"
    ],
    "Severidade": [
        "Critical",
        "High",
        "Medium",
        "High",
        "Info",
        "Medium"
    ],
    "Responsável / Origem": [
        "AWS GuardDuty / Auto-Remediation",
        "IAM Access Analyzer",
        "Compliance Engine",
        "Threat Feed Connector",
        "Executive User",
        "Admin DevOps"
    ]
})

# ==========================================
# 1. AUDIT MISSION CONTROL (Adicionado logo após o Hero)
# ==========================================
st.subheader("Audit Mission Control")

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Eventos", len(history_df))
m2.metric("Critical", len(history_df[history_df["Severidade"]=="Critical"]))
m3.metric("High", len(history_df[history_df["Severidade"]=="High"]))
m4.metric("Módulos", history_df["Módulo"].nunique())
m5.metric("Status", "Active")

st.markdown("---")

# ==========================================
# 5. FILTROS DE HISTÓRICO
# ==========================================
st.subheader("Filtros de Auditoria")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filtro_severidade = st.selectbox(
        "Filtrar por Severidade",
        ["Todas", "Critical", "High", "Medium", "Low", "Info"]
    )

with col_f2:
    filtro_modulo = st.selectbox(
        "Filtrar por Módulo",
        ["Todos", "Security Hub", "IAM", "Compliance", "Threat Intelligence", "Security Copilot"]
    )

with col_f3:
    dias_historico = st.slider("Período (Dias)", 1, 30, 7)

st.markdown("---")

# ==========================================
# 2. AUDIT HEALTH SCORE (Adicionado após os filtros)
# ==========================================
st.subheader("Audit Health Score")

audit_score = 96

st.progress(audit_score / 100)

st.success(
    f"Audit Health: {audit_score}%"
)

st.markdown("---")

# Aplicando Filtros
df_filtrado = history_df.copy()

if filtro_severidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Severidade"] == filtro_severidade]

if filtro_modulo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Módulo"] == filtro_modulo]

# ==========================================
# 7. EXIBIÇÃO DA TABELA DE HISTÓRICO
# ==========================================
st.subheader("Registro de Eventos")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 3. SECURITY EVENT DISTRIBUTION (Adicionado após a tabela principal)
# ==========================================
st.subheader("Security Event Distribution")

dist_df = pd.DataFrame({
    "Severidade": [
        "Critical",
        "High",
        "Medium",
        "Info"
    ],
    "Quantidade": [
        len(history_df[history_df["Severidade"]=="Critical"]),
        len(history_df[history_df["Severidade"]=="High"]),
        len(history_df[history_df["Severidade"]=="Medium"]),
        len(history_df[history_df["Severidade"]=="Info"])
    ]
})

st.bar_chart(
    dist_df.set_index("Severidade")
)

st.markdown("---")

# ==========================================
# 4. AUDIT INTELLIGENCE (Adicionado antes da Timeline)
# ==========================================
st.subheader("Audit Intelligence")

st.info("""
Resumo Executivo

• Eventos críticos auditados.

• Histórico íntegro.

• Nenhuma inconsistência detectada.

• Logs sincronizados.

• Compliance preservado.
""")

st.markdown("---")

# ==========================================
# 8. TIMELINE DE INCIDENTES RECENTES
# ==========================================
st.subheader("Timeline de Ocorrências Críticas")

for index, row in history_df[history_df["Severidade"].isin(["Critical", "High"])].iterrows():
    with st.expander(f"🚨 [{row['Timestamp']}] {row['Módulo']} - Severidade: {row['Severidade']}"):
        st.write(f"**Descrição do Evento:** {row['Evento']}")
        st.write(f"**Origem / Ação Tomada:** {row['Responsável / Origem']}")
        st.caption("Status: Resolvido / Auditado pelo sistema.")

st.markdown("---")

# ==========================================
# 7. COMPLIANCE TIMELINE (Adicionado após a Timeline)
# ==========================================
st.subheader("Compliance Timeline")

timeline_df = pd.DataFrame({
    "Evento": [
        "IAM Review",
        "CIS Scan",
        "NIST Validation",
        "Threat Review"
    ],
    "Status": [
        "Concluído",
        "Concluído",
        "Concluído",
        "Em andamento"
    ]
})

st.dataframe(
    timeline_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================
# 5. AUDIT COPILOT (Adicionado antes da exportação)
# ==========================================
st.subheader("Audit Copilot")

question = st.text_area(
    "Pergunte sobre o histórico."
)

if st.button("Analisar Histórico"):
    q = question.lower()
    
    if "critical" in q:
        st.info(
            "Foi identificado 1 evento crítico recente."
        )
    elif "iam" in q:
        st.info(
            "Existem registros relacionados ao IAM."
        )
    elif "compliance" in q:
        st.info(
            "Os eventos de compliance estão registrados."
        )
    else:
        st.info(
            "Análise de auditoria concluída."
        )

st.markdown("---")

# ==========================================
# 6. EVENT TREND (Adicionado antes da exportação)
# ==========================================
st.subheader("Audit Trend")

trend = pd.DataFrame({
    "Dia": [
        "Seg",
        "Ter",
        "Qua",
        "Qui",
        "Sex"
    ],
    "Eventos": [
        15,
        12,
        18,
        10,
        len(history_df)
    ]
})

st.line_chart(
    trend.set_index("Dia")
)

st.markdown("---")

# ==========================================
# 9. EXPORTAÇÃO DE RELATÓRIO DE AUDITORIA
# ==========================================
st.subheader("Exportar Relatório de Auditoria")

csv_data = history_df.to_csv(index=False).encode('utf-8')

st.download_button(
    "📥 Baixar Histórico Completo (CSV)",
    csv_data,
    file_name=f"audit_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

st.markdown("---")

# ==========================================
# 10. NAVEGAÇÃO INTEGRADA
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
st.caption(f"AWS Cyber Defense Platform • Audit History Module • Todos os direitos reservados © {datetime.now().year} • Sincronizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")