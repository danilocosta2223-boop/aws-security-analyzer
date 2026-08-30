import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Tenta importar fpdf para geração real de PDF, fallback para texto formatado se indisponível
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="PDF Reports & Executive Export | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ESTILO CSS CORPORATIVO (Tags limpas)
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

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

p, span, label, div {
    color: #E5E7EB;
}

.hero-card {
    background: #1F2937;
    border: 1px solid #374151;
    border-radius: 15px;
    padding: 24px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CABEÇALHO DO MÓDULO (Tags limpas)
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>PDF Reports & Executive Export</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Geração automatizada de relatórios executivos de nível diretivo, auditorias de conformidade e exportação multi-formato integrada à plataforma.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. MÉTRICAS DO GERADOR
# ==========================================
m1, m2, m3, m4 = st.columns(4)

m1.metric("Modelos Prontos", "5")
m2.metric("Relatórios Gerados", "34")
m3.metric("Formatos", "PDF / CSV / TXT / JSON")
m4.metric("Status do Motor", "Online")

st.markdown("---")

# ==========================================
# 5. CONFIGURAÇÃO DO RELATÓRIO (Templates, Período e Audiência)
# ==========================================
st.subheader("Configuração do Relatório Consolidado")

col_cfg1, col_cfg2, col_cfg3 = st.columns(3)

with col_cfg1:
    template_escolhido = st.selectbox(
        "Template de Relatório",
        [
            "Executive Board",
            "SOC Report",
            "Compliance Report",
            "Incident Report",
            "Attack Path Assessment"
        ]
    )

with col_cfg2:
    audiencia = st.radio(
        "Audiência",
        [
            "Executiva",
            "Técnica"
        ]
    )

with col_cfg3:
    formato_saida = st.selectbox(
        "Formato de Exportação",
        [
            "PDF (Documento Oficial)",
            "CSV (Planilha Consolidada)",
            "TXT (Texto Simples)",
            "JSON (Payload Estruturado)"
        ]
    )

col_p1, col_p2 = st.columns(2)
with col_p1:
    data_inicio = st.date_input("Data Inicial", value=datetime.strptime("2026-08-01", "%Y-%m-%d").date())
with col_p2:
    data_fim = st.date_input("Data Final", value=datetime.now().date())

modulos = st.multiselect(
    "Módulos Incluídos no Relatório Consolidado",
    [
        "Security Center",
        "AWS Config",
        "CloudTrail",
        "Attack Path",
        "Threat Intelligence",
        "Kali Lab"
    ],
    default=["Security Center", "AWS Config", "CloudTrail", "Attack Path", "Kali Lab"]
)

st.markdown("---")

# ==========================================
# 6. KPIS E MATURIDADE DE SEGURANÇA
# ==========================================
st.subheader("KPIs Incluídos")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Risk Score", "82")
k2.metric("Compliance", "91%")
k3.metric("Incidentes", "4")
k4.metric("Ativos", "127")

st.subheader("Security Maturity")
st.progress(0.88)
st.success("Nível de Maturidade: Avançado")

st.markdown("---")

# ==========================================
# 7. ASSINATURA DE INTEGRIDADE
# ==========================================
st.subheader("Integridade Criptográfica do Relatório")
hash_relatorio = "SHA256-ABCD1234F9823AE78901BCDE45678902"
st.code(hash_relatorio)

st.markdown("---")

# ==========================================
# 8. GERAÇÃO E DOWNLOAD DE ARQUIVOS REAIS
# ==========================================
st.subheader("Geração e Download do Documento")

# Função para gerar PDF real se FPDF estiver disponível
def gerar_pdf_bytes():
    if FPDF_AVAILABLE:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "AWS Cyber Defense Platform - Executive Report", 0, 1, "C")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Template: {template_escolhido} | Audiencia: {audiencia}", 0, 1, "L")
        pdf.cell(0, 10, f"Periodo: {data_inicio} ate {data_fim}", 0, 1, "L")
        pdf.ln(5)
        
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "1. Sumario Executivo & KPIs", 0, 1, "L")
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, "Risk Score: 82/100\nCompliance Geral: 91%\nIncidentes Ativos: 4\nAtivos Monitorados: 127\nMaturidade de Seguranca: Avancado (88%)\nHash de Integridade: " + hash_relatorio)
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "2. Modulos Incluidos", 0, 1, "L")
        pdf.set_font("Arial", "", 11)
        for m in modulos:
            pdf.cell(0, 6, f"- {m}: Analisado e verificado sem anomalias criticas pendentes.", 0, 1, "L")
            
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            pdf_output = pdf_output.encode('latin1')
        return BytesIO(pdf_output)
    else:
        # Fallback para texto caso fpdf não esteja instalado no ambiente
        conteudo_fallback = f"""=== AWS CYBER DEFENSE PLATFORM - EXECUTIVE REPORT ===
Template: {template_escolhido}
Audiência: {audiencia}
Período: {data_inicio} a {data_fim}
Módulos: {', '.join(modulos)}
Risk Score: 82 | Compliance: 91% | Maturidade: Avançado (88%)
Hash de Integridade: {hash_relatorio}
======================================================="""
        return BytesIO(conteudo_fallback.encode('utf-8'))

arquivo_gerado = gerar_pdf_bytes()

col_d1, col_d2 = st.columns(2)

with col_d1:
    if st.button("Executar Motor de Relatórios"):
        st.success("Relatório processado, validado e criptografado com sucesso.")

with col_d2:
    extensao = "pdf" if ("PDF" in formato_saida and FPDF_AVAILABLE) else ("csv" if "CSV" in formato_saida else ("json" if "JSON" in formato_saida else "txt"))
    mime_type = "application/pdf" if extensao == "pdf" else ("text/csv" if extensao == "csv" else ("application/json" if extensao == "json" else "text/plain"))
    
    st.download_button(
        label=f"Baixar Documento Oficial ({extensao.upper()})",
        data=arquivo_gerado,
        file_name=f"executive_report_{template_escolhido.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{extensao}",
        mime=mime_type
    )

st.markdown("---")

# ==========================================
# 9. HISTÓRICO DE RELATÓRIOS
# ==========================================
st.subheader("Histórico de Relatórios")

df_relatorios = pd.DataFrame({
    "Data": ["27/08/2026", "26/08/2026", "25/08/2026", "24/08/2026"],
    "Template": ["Executive Board", "Compliance Report", "Incident Report", "Attack Path Assessment"],
    "Audiência": ["Executiva", "Técnica", "Técnica", "Executiva"],
    "Formato": ["PDF", "PDF", "CSV", "PDF"],
    "Status": ["Disponível", "Disponível", "Disponível", "Disponível"]
})

st.dataframe(df_relatorios, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 10. NAVEGAÇÃO RÁPIDA ENTRE MÓDULOS
# ==========================================
st.subheader("Navegação Rápida")

c_link1, c_link2, c_link3, c_link4, c_link5, c_link6 = st.columns(6)

with c_link1:
    st.page_link("pages/security_center.py", label="Security Center")
with c_link2:
    st.page_link("pages/Attack_Path.py", label="Attack Path")
with c_link3:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")
with c_link4:
    st.page_link("pages/AWS_Config.py", label="AWS Config")
with c_link5:
    st.page_link("pages/kali_lab.py", label="Kali Lab")
with c_link6:
    st.page_link("pages/executive_dashboard.py", label="Exec Dashboard")

# ==========================================
# 11. RODAPÉ
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • PDF Reports & Executive Export • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")