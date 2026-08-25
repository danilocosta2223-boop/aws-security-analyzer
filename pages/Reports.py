import streamlit as st
from datetime import datetime
import time
import pandas as pd

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Relatórios & Exportação | AWS Cyber Defense",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ESTILO CSS CUSTOMIZADO
# ==========================================
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    .badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background-color: #1e3a8a;
        color: #93c5fd;
        border: 1px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CABEÇALHO DO MÓDULO
# ==========================================
st.title("📄 Reports & Export Center")

st.info("""
Central de geração de relatórios executivos,
compliance, vulnerabilidades e auditoria AWS.
""")

st.markdown(f"""
<div style="font-size: 13px; color: #94a3b8; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional &nbsp;|&nbsp; 
    <b>Última varredura consolidada:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')} &nbsp;|&nbsp;
    <b>Formato padrão:</b> PDF / JSON / CSV
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 4. PAINEL DE CONFIGURAÇÃO DE RELATÓRIO
# ==========================================
st.subheader("⚙️ Configurar Novo Relatório")

col_cfg1, col_cfg2, col_cfg3 = st.columns(3)

with col_cfg1:
    report_type = st.selectbox(
        "Tipo de Relatório",
        ["Executive Summary (CSOC)", "Compliance CIS Benchmark", "Vulnerability & Inspector Audit", "Attack Path & Threat Intel"]
    )

with col_cfg2:
    report_format = st.selectbox(
        "Formato de Saída",
        ["PDF (Enterprise Layout)", "JSON (Raw Data)", "CSV (Spreadsheet)", "HTML Report"]
    )

with col_cfg3:
    scope = st.selectbox(
        "Escopo da Conta AWS",
        ["Conta Completa (Global)", "IAM & S3 Services", "Compute (EC2/Lambda/RDS)", "Security Hub Findings"]
    )

st.markdown("<br>", unsafe_allow_html=True)

# Botão de Ação para Gerar Relatório
if st.button("🚀 Gerar e Baixar Relatório", type="primary"):
    with st.spinner("Processando dados de segurança, compilar métricas e gerando documento..."):
        time.sleep(2)
    
    st.success(f"✅ Relatório **{report_type}** gerado com sucesso no formato **{report_format}**!")
    
    # Simulação de Download
    st.download_button(
        label="📥 Clique aqui para baixar o arquivo gerado",
        data=f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Tipo: {report_type} - Escopo: {scope}",
        file_name=f"aws_security_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

# ==========================================
# 5. HISTÓRICO DE RELATÓRIOS RECENTES
# ==========================================
st.markdown("---")
st.subheader("📂 Relatórios Recentes Disponíveis")

df_reports = pd.DataFrame([
    {"Data/Hora": "23/08/2026 14:30", "Nome do Relatório": "Executive_Summary_Q3.pdf", "Tipo": "Executive", "Status": "Pronto"},
    {"Data/Hora": "22/08/2026 09:15", "Nome do Relatório": "Compliance_CIS_AWS.pdf", "Tipo": "Compliance", "Status": "Pronto"},
    {"Data/Hora": "20/08/2026 18:40", "Nome do Relatório": "Inspector_Vulnerabilities.csv", "Tipo": "Vulnerabilidade", "Status": "Pronto"}
])

st.dataframe(df_reports, use_container_width=True, hide_index=True)

# ==========================================
# RODAPÉ DA PÁGINA
# ==========================================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • Módulo de Relatórios • Desenvolvido por Danilo Rafael da Silva Costa")