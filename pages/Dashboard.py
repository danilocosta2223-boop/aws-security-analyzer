import streamlit as st
import json
import os

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================

st.set_page_config(
    page_title="AWS Cyber Defense Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ==========================
# ESTILO VISUAL CUSTOMIZADO (CSS)
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
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
        margin-bottom: 24px;
    }
    .badge-critical { background-color: #7f1d1d; color: #fca5a5; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-high { background-color: #78350f; color: #fde68a; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-medium { background-color: #1e3a8a; color: #93c5fd; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    .badge-low { background-color: #065f46; color: #34d399; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# ==========================
# CARREGAR JSON
# ==========================

json_file = "reports/security_report.json"

if not os.path.exists(json_file):
    st.error(f"⚠️ O arquivo de relatório `{json_file}` não foi encontrado. Execute o pipeline de geração de dados primeiro.")
    st.stop()

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ==========================
# SECURITY SCORE
# ==========================

def calculate_score(summary):
    score = 100
    score -= summary.get("critical", 0) * 25
    score -= summary.get("high", 0) * 15
    score -= summary.get("medium", 0) * 5
    score -= summary.get("low", 0) * 1
    return max(score, 0)

score = calculate_score(data["security_hub_summary"])

# ==========================
# CABEÇALHO & HERO CARD
# ==========================

st.markdown("""
    <div class="hero-card">
        <h1>🛡️ Cloud Security Operations Center (CSOC)</h1>
        <p style="color: #94a3b8; margin: 0; font-size: 15px;">Monitoramento contínuo de postura de segurança e conformidade em nuvem</p>
    </div>
""", unsafe_allow_html=True)

st.caption(
    f"🌐 **Região AWS:** `{data['region']}` | "
    f"🕒 **Último Scan:** `{data['timestamp']}`"
)
st.markdown("---")

# ==========================
# MÉTRICAS
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Security Score", f"{score}/100", delta="Postura Atual")

with col2:
    st.metric("Total Findings", data["total_findings"], delta="Security Hub")

with col3:
    st.metric("Critical", data["security_hub_summary"]["critical"], delta="Requer Ação", delta_color="inverse")

with col4:
    st.metric("High", data["security_hub_summary"]["high"], delta="Atenção", delta_color="inverse")

# ==========================
# SCORE VISUAL
# ==========================

st.subheader("📈 Postura de Segurança Global")
st.progress(score / 100)

# ==========================
# SUMMARY
# ==========================

st.subheader("📋 Executive Summary")

st.info(f"""
* **Security Score Atual:** **{score}/100**
* **Total de Vulnerabilidades Detectadas:** **{data['total_findings']}**
* **Região AWS Monitorada:** **{data['region']}**
* **Achados Críticos Prioritários:** **{data['security_hub_summary']['critical']}**
""")

# ==========================
# FINDINGS
# ==========================

st.subheader("🚨 Principais Achados (Findings)")

for finding in data["findings"]:
    sev = finding['severity'].upper()
    badge_class = "badge-critical" if sev == "CRITICAL" else ("badge-high" if sev == "HIGH" else ("badge-medium" if sev == "MEDIUM" else "badge-low"))
    
    with st.expander(f"[{sev}] {finding['service']} — Recurso: {finding['resource']}"):
        st.markdown(f'<span class="{badge_class}">{sev}</span>', unsafe_allow_html=True)
        st.write("")
        st.write(f"**🔍 Problema Identificado:** {finding['issue']}")
        st.write(f"**💡 Recomendação de Correção:** {finding['recommendation']}")

# ==========================
# ROADMAP
# ==========================

st.subheader("🛠️ Roadmap de Correção Recomendado")

st.markdown("""
1. **Ativar MFA** obrigatoriamente para todos os usuários IAM administrativos.
2. **Revisar Security Groups** para fechar portas de acesso remoto desprotegidas (ex: SSH/22).
3. **Habilitar Criptografia SSE-KMS** em todos os buckets de armazenamento S3.
4. **Auditar permissões excessivas** em papéis e políticas de acesso.
5. **Executar novo ciclo de varredura** após a aplicação das correções.
""")

# ==========================
# RODAPÉ
# ==========================

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>AWS Cyber Defense Platform • CSOC Enterprise Edition</p>", unsafe_allow_html=True)