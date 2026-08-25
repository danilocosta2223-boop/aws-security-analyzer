import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EC2 Security Center | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="ec2_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO (FUNDO BRANCO)
# ==========================================
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #1e3a5f;
    }
    
    .hero-card {
        background-color: #f3f4f6;
        border: 1px solid #d1d5db;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }

    h1, h2, h3, h4 {
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. CONSUMO ROBUSTO DA API EC2 (TIMEOUT=5)
# ==========================================
@st.cache_data(ttl=10)
def carregar_dados_ec2():
    response = requests.get("http://127.0.0.1:3000/api/ec2", timeout=5)
    return response.json()

try:
    ec2_data = carregar_dados_ec2()
    backend_online = True
except Exception:
    backend_online = False
    st.error("Backend indisponível. Certifique-se de que o servidor Node.js está em execução.")
    st.stop()

# ==========================================
# 5. EXTRACÃO DE MÉTRICAS E CÁLCULOS DINÂMICOS
# ==========================================
total_instances = ec2_data.get("totalInstances", 0)
open_sg = ec2_data.get("openSecurityGroups", 0)
unpatched = ec2_data.get("unpatchedVulnerabilities", 0)
instances_list = ec2_data.get("instances", [])

ec2_score = max(100 - (open_sg * 10) - (unpatched * 5), 0)

critical_risk = open_sg
high_risk = unpatched
medium_risk = 0
low_risk = max(total_instances - critical_risk - high_risk, 0)

# ==========================================
# 6. CABEÇALHO DO MÓDULO (HERO CARD)
# ==========================================
st.markdown("""
<div class="hero-card">
    <h1>EC2 Security Center</h1>
    <p style="color: #4b5563; margin: 0; font-size: 15px;">
        Auditoria de instâncias EC2, análise de Security Groups, conformidade de hardening e gerenciamento de exposição de ativos.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; color: #4b5563; margin-bottom: 20px;">
    <b>Status do Módulo:</b> Operacional &nbsp;|&nbsp; 
    <b>Última Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} &nbsp;|&nbsp;
    <b>Total de Instâncias:</b> {total_instances}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 7. EXECUTIVE DASHBOARD
# ==========================================
st.subheader("Executive Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Instâncias Monitoradas", total_instances)

with c2:
    st.metric(
        "Security Groups Expostos",
        open_sg,
        delta="Crítico" if open_sg > 0 else "Normal",
        delta_color="inverse" if open_sg > 0 else "normal"
    )

with c3:
    st.metric("Vulnerabilidades Não Corrigidas", unpatched)

with c4:
    st.metric(
        "Risco Geral",
        "Alto" if open_sg > 0 or unpatched > 0 else "Baixo",
        delta="Atenção Necessária" if open_sg > 0 else "Estável",
        delta_color="inverse" if open_sg > 0 else "normal"
    )

st.markdown("---")

# ==========================================
# 8. EC2 SECURITY SCORE
# ==========================================
st.subheader("EC2 Security Score")
st.progress(ec2_score / 100)
st.metric("Pontuação de Segurança EC2", f"{ec2_score}/100")

st.markdown("---")

# ==========================================
# 9. EXECUTIVE SUMMARY
# ==========================================
st.subheader("Executive Summary")

summary_items = []
if open_sg > 0:
    summary_items.append(f"Identificados {open_sg} Security Groups com portas críticas abertas globalmente para a Internet.")
if unpatched > 0:
    summary_items.append(f"Existem {unpatched} vulnerabilidades pendentes de correção nas instâncias avaliadas.")

if summary_items:
    for item in summary_items:
        st.warning(item)
else:
    st.success("O ambiente EC2 encontra-se alinhado às melhores práticas corporativas de segurança e hardening.")

st.markdown("---")

# ==========================================
# 10. COMPLIANCE EC2
# ==========================================
st.subheader("Compliance EC2")
st.metric("Nível de Aderência às Políticas", f"{ec2_score}%")

st.markdown("---")

# ==========================================
# 11. INVENTÁRIO DE INSTÂNCIAS
# ==========================================
st.subheader("Inventário de Instâncias")

if instances_list:
    df_instances = pd.DataFrame(instances_list)
    st.dataframe(df_instances, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma instância registrada na resposta da API.")

st.markdown("---")

# ==========================================
# 12. FINDINGS EC2
# ==========================================
st.subheader("Findings e Alertas")

has_findings = False
for instance in instances_list:
    if instance.get("risk") in ["High", "Crítico", "Alto"]:
        has_findings = True
        st.error(f"Instância `{instance.get('name', 'Desconhecida')}` catalogada com risco elevado. Recomenda-se revisão imediata das regras de acesso.")

if not has_findings and open_sg > 0:
    st.warning("Existem regras de entrada permissivas em Security Groups que exigem remediação.")
elif not has_findings:
    st.write("Nenhum finding crítico registrado para as instâncias atuais.")

st.markdown("---")

# ==========================================
# 13. RISK MATRIX
# ==========================================
st.subheader("Risk Matrix")

r1, r2, r3, r4 = st.columns(4)
r1.metric("Crítico", critical_risk)
r2.metric("Alto", high_risk)
r3.metric("Médio", medium_risk)
r4.metric("Baixo", low_risk)

st.markdown("---")

# ==========================================
# 14. TIMELINE DE EVENTOS
# ==========================================
st.subheader("Timeline")

timeline = []
if open_sg > 0:
    timeline.append(f"Detecção de {open_sg} Security Groups com portas desprotegidas")
if unpatched > 0:
    timeline.append(f"Identificação de {unpatched} pacotes desatualizados")

if not timeline:
    timeline.append("Nenhum evento adverso reportado na última varredura do ciclo.")

for evento in timeline:
    st.write(f"{datetime.now().strftime('%H:%M:%S')} - {evento}")

st.markdown("---")

# ==========================================
# 15. HEALTH CHECK
# ==========================================
st.subheader("Health Check")

health_df = pd.DataFrame([
    ["EC2 API Service", "Online" if backend_online else "Offline"],
    ["Backend Node.js", "Online" if backend_online else "Offline"],
    ["AWS EC2 Endpoint", "Online" if backend_online else "Offline"]
], columns=["Serviço", "Status"])

st.dataframe(health_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 16. PLANO DE CORREÇÃO
# ==========================================
st.subheader("Plano de Correção")

if open_sg > 0:
    st.write("- Restringir imediatamente as regras de entrada (Inbound Rules) dos Security Groups para IPs corporativos confiáveis.")
if unpatched > 0:
    st.write("- Executar o processo de atualização de patches de segurança e pacotes nas instâncias afetadas.")
st.write("- Validar a adoção do AWS Systems Manager (SSM) Session Manager para auditoria e acesso remoto seguro.")

# ==========================================
# RODAPÉ DA PÁGINA
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • EC2 Security Center • Última Atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")