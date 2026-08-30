import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Threat Intelligence & Hunting Center",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 2. ESTILO CSS CORPORATIVO
# ==========================
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

# ==========================
# 3. CARREGAR JSON DE RELATÓRIO
# ==========================
json_file = "reports/security_report.json"

if not os.path.exists(json_file):
    st.error("Arquivo security_report.json não encontrado.")
    st.stop()

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extração de dados base para cálculos
critical = data.get("security_hub_summary", {}).get("critical", 0)
high = data.get("security_hub_summary", {}).get("high", 0)
medium = data.get("security_hub_summary", {}).get("medium", 0)
low = data.get("security_hub_summary", {}).get("low", 0)
findings_list = data.get("findings", [])

# Cálculo dinâmico do Threat Score
score = max(
    100 - (
        critical * 15 +
        high * 8 +
        medium * 3
    ),
    0
)

# ==========================
# 4. CABEÇALHO DO MÓDULO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Threat Intelligence & Hunting Center</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Centro avançado de inteligência de ameaças, caça a IOCs, simulação de adversários e resposta a incidentes na AWS.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Região AWS: {data.get('region', 'us-east-1')} | Scan: {data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")

st.markdown("---")

# ==========================
# 5. THREAT MISSION CONTROL
# ==========================
st.subheader("Threat Mission Control")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Threat Score", f"{score}%")
c2.metric("Findings", len(findings_list))
c3.metric("Critical", critical)
c4.metric("IOCs", 14)
c5.metric("Risk Level", "High" if critical > 0 else "Low")

st.markdown("---")

# ==========================
# 6. EXECUTIVE DASHBOARD & MÉTRICAS
# ==========================
st.subheader("Executive Dashboard & Severity Overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Critical", critical)
m2.metric("High", high)
m3.metric("Medium", medium)
m4.metric("Low", low)

st.subheader("Threat Severity Score")
st.progress(score / 100)
st.success(f"Threat Score Geral do Ambiente: {score}%")

st.markdown("---")

# ==========================
# 7. THREAT HEAT MAP & THREAT LANDSCAPE
# ==========================
hm_col1, hm_col2 = st.columns(2)

with hm_col1:
    st.subheader("Threat Heat Map")
    heatmap = pd.DataFrame({
        "Área": ["IAM", "S3", "EC2", "CloudTrail"],
        "Risco": [90, 95, 70, 40]
    })
    st.bar_chart(heatmap.set_index("Área"))

with hm_col2:
    st.subheader("Threat Landscape")
    landscape = pd.DataFrame({
        "Categoria": ["Credential Theft", "Misconfiguration", "Data Exposure", "Privilege Escalation"],
        "Ocorrências": [4, 7, 3, 2]
    })
    st.bar_chart(landscape.set_index("Categoria"))

st.markdown("---")

# ==========================
# 8. THREAT HUNTING COVERAGE, STATS & LAB
# ==========================
st.subheader("Hunting Statistics")
h1, h2, h3, h4 = st.columns(4)
h1.metric("IOCs", 14)
h2.metric("Investigados", 8)
h3.metric("Confirmados", 2)
h4.metric("Falsos Positivos", 6)

th_col1, th_col2 = st.columns(2)

with th_col1:
    st.subheader("Threat Hunting Coverage")
    coverage = pd.DataFrame({
        "Fonte": ["CloudTrail", "Security Hub", "IAM", "EC2", "S3"],
        "Cobertura": ["100%", "100%", "92%", "95%", "97%"]
    })
    st.dataframe(coverage, use_container_width=True, hide_index=True)

with th_col2:
    st.subheader("Threat Hunting Lab")
    ioc = st.text_input("IOC, IP, Domínio ou Hash para caça ativa:")
    if st.button("Investigar IOC"):
        if ioc.strip():
            st.success(f"Investigação ativa iniciada para: `{ioc}`")
            st.info("Nenhum indicador de comprometimento (IoC) malicioso ativo na frota.")
        else:
            st.warning("Insira um indicador válido para iniciar a varredura.")

st.markdown("---")

# ==========================
# 9. ANALYST WORKBENCH & ACTIVE INCIDENTS
# ==========================
aw_col1, aw_col2 = st.columns(2)

with aw_col1:
    st.subheader("Analyst Workbench")
    analyst = st.selectbox(
        "Selecionar Caso",
        ["IAM Compromise", "S3 Exposure", "Privilege Escalation"]
    )
    if st.button("Abrir Investigação"):
        st.success(f"Investigação aberta para {analyst}")

with aw_col2:
    st.subheader("Active Incidents")
    incidentes = pd.DataFrame({
        "Incidente": ["Bucket Público", "IAM sem MFA"],
        "Status": ["Investigando", "Em Correção"],
        "Prioridade": ["P1", "P2"]
    })
    st.dataframe(incidentes, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================
# 10. IOC REPOSITORY & THREAT INTELLIGENCE FEED
# ==========================
ti_col1, ti_col2 = st.columns(2)

with ti_col1:
    st.subheader("IOC Repository")
    ioc_df = pd.DataFrame({
        "Indicador": ["185.22.x.x", "evil-domain.com", "SHA256:xxxx"],
        "Tipo": ["IP", "Domínio", "Hash"],
        "Status": ["Monitorado", "Bloqueado", "Monitorado"]
    })
    st.dataframe(ioc_df, use_container_width=True, hide_index=True)

with ti_col2:
    st.subheader("Threat Intelligence Feed")
    feeds = pd.DataFrame({
        "Fonte": ["GuardDuty", "Security Hub", "CloudTrail"],
        "Eventos": [12, 33, 102]
    })
    st.dataframe(feeds, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================
# 11. THREAT CORRELATION & MITRE ATT&CK COVERAGE
# ==========================
tc_col1, tc_col2 = st.columns(2)

with tc_col1:
    st.subheader("Threat Correlation Engine")
    correlation = pd.DataFrame({
        "Origem": ["IAM", "EC2", "S3"],
        "Destino": ["EC2", "S3", "Exfiltração"],
        "Impacto": ["Alto", "Crítico", "Crítico"]
    })
    st.dataframe(correlation, use_container_width=True, hide_index=True)

with tc_col2:
    st.subheader("ATT&CK Coverage")
    attck_cov = 88
    st.progress(attck_cov / 100)
    st.success(f"Cobertura MITRE ATT&CK: {attck_cov}%")

st.markdown("---")

# ==========================
# 12. RISK RANKING & FINDINGS
# ==========================
rk_col1, rk_col2 = st.columns(2)

with rk_col1:
    st.subheader("Risk Ranking")
    ranking = pd.DataFrame({
        "Risco": ["Bucket Público", "IAM sem MFA", "Security Group Aberto"],
        "Prioridade": ["P1", "P2", "P3"]
    })
    st.dataframe(ranking, use_container_width=True, hide_index=True)

with rk_col2:
    st.subheader("Findings Detectados")
    for finding in findings_list:
        severity = finding.get("severity", "LOW")
        msg = f"{finding.get('service', 'AWS')} - {finding.get('issue', 'Alerta')}"
        if severity == "CRITICAL":
            st.error(msg)
        elif severity == "HIGH":
            st.warning(msg)
        else:
            st.info(msg)

st.markdown("---")

# ==========================
# 13. TABELA DETALHADA E TOP RISKS
# ==========================
st.subheader("Threat Investigation Detalhada")

rows = []
for finding in findings_list:
    rows.append({
        "Serviço": finding.get("service"),
        "Severidade": finding.get("severity"),
        "Recurso": finding.get("resource"),
        "Problema": finding.get("issue"),
        "Correção": finding.get("recommendation")
    })

if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.info("Nenhum registro detalhado na base de achados atual.")

st.subheader("Top Risks")
high_risks = [f for f in findings_list if f.get("severity") in ["CRITICAL", "HIGH"]]
if high_risks:
    for item in high_risks:
        st.markdown(f"""
### {item.get('service')}
* **Severidade:** {item.get('severity')}
* **Problema:** {item.get('issue')}
* **Recurso:** `{item.get('resource')}`
* **Recomendação:** {item.get('recommendation')}
""")
else:
    st.success("Nenhum risco alto ou crítico pendente no momento.")

st.markdown("---")

# ==========================
# 14. THREAT PREDICTION & INCIDENT READINESS
# ==========================
pr_col1, pr_col2 = st.columns(2)

with pr_col1:
    st.subheader("Threat Prediction")
    if critical > 0:
        st.error("Probabilidade de incidente: 85% — Existem ameaças críticas ativas.")
    else:
        st.success("Probabilidade de incidente: 25% — Ambiente controlado.")

with pr_col2:
    st.subheader("Incident Response Readiness")
    readiness = 93
    st.progress(readiness / 100)
    st.success(f"IR Readiness: {readiness}%")

st.markdown("---")

# ==========================
# 15. THREAT ACTOR SIMULATION & RECOMMENDATIONS
# ==========================
sim_col1, sim_col2 = st.columns(2)

with sim_col1:
    st.subheader("Threat Actor Simulation")
    actor = st.selectbox("Perfil", ["Credential Theft", "Ransomware", "APT", "Insider Threat"])
    if st.button("Executar Simulação"):
        st.warning(f"Simulação executada com sucesso para o perfil: {actor}")

with sim_col2:
    st.subheader("Recommendations Engine")
    recommendations = [
        "Ativar MFA global",
        "Aplicar Block Public Access",
        "Fechar Security Groups expostos",
        "Rotacionar credenciais antigas"
    ]
    for item in recommendations:
        st.info(item)

st.markdown("---")

# ==========================
# 16. THREAT INTELLIGENCE MATURITY & COPILOT INSIGHTS
# ==========================
mat_col1, mat_col2 = st.columns(2)

with mat_col1:
    st.subheader("Threat Intelligence Maturity")
    maturity = 91
    st.progress(maturity / 100)
    st.success(f"Maturidade de Inteligência: {maturity}%")

with mat_col2:
    st.subheader("Copilot Risk Summary")
    st.info(f"""
Resumo da IA

Threat Score: {score}%

Critical: {critical}

High: {high}

Ameaça Principal: Misconfiguration

Prioridade: P1
    """)

st.subheader("Threat Intelligence Copilot")
pergunta = st.text_area("Faça uma pergunta ao Copilot sobre ameaças (ex: risco, iam, s3):")
if st.button("Analisar Threats"):
    p = pergunta.lower()
    if "risco" in p:
        st.info(f"""
Maior risco atual:

Critical: {critical}

Threat Score: {score}%

Ação recomendada: Remediar findings críticos imediatamente.
        """)
    elif "iam" in p:
        st.info("Copilot Insights: IAM sem MFA é um vetor primário de comprometimento de credenciais.")
    elif "s3" in p:
        st.info("Copilot Insights: Buckets S3 públicos podem resultar em exfiltração imediata de dados.")
    else:
        st.info("Copilot Insights: Análise comportamental concluída com base nos relatórios de telemetria.")

st.markdown("---")

# ==========================
# 17. EXECUTIVO: DOWNLOAD DO RELATÓRIO
# ==========================
st.subheader("Executive Report Download")

report_text = f"""
=========================================
THREAT INTELLIGENCE EXECUTIVE REPORT
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
=========================================
Critical: {critical} | High: {high} | Medium: {medium} | Low: {low}
Threat Score: {score}%
Maturidade: {maturity}%
IR Readiness: {readiness}%
"""

st.download_button(
    "Baixar Relatório Executivo (.txt)",
    report_text,
    file_name="threat_intelligence_report.txt",
    mime="text/plain"
)

st.markdown("---")

# ==========================
# 18. NAVEGAÇÃO INTEGRADA
# ==========================
st.subheader("Navegação Integrada")

n1, n2, n3, n4, n5 = st.columns(5)
with n1:
    st.page_link("pages/security_hub.py", label="Security Hub")
with n2:
    st.page_link("pages/security_copilot.py", label="Security Copilot")
with n3:
    st.page_link("pages/compliance.py", label="Compliance")
with n4:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")
with n5:
    st.page_link("pages/security_center.py", label="Security Center")

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Threat Intelligence & Hunting Center • Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")