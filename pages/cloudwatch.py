import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="CloudWatch & Observability | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ESTILO CSS CORPORATIVO (Tags 100% limpas, sem entidades escapadas)
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
    <h1>CloudWatch & Observability Center</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Centro unificado de monitoramento de métricas, alarmes avançados, logs centralizados, telemetria de infraestrutura e correlação SOC.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. DASHBOARD EXECUTIVO, KPIS OPERACIONAIS & EXECUTIVE SUMMARY
# ==========================================
m1, m2, m3, m4 = st.columns(4)
m1.metric("Alarmes", "12")
m2.metric("Críticos", "3")
m3.metric("Logs", "25.4K")
m4.metric("Disponibilidade", "99.95%")

st.subheader("KPIs Operacionais")
k1, k2, k3 = st.columns(3)
k1.metric("MTTD", "12 min")
k2.metric("MTTR", "31 min")
k3.metric("Uptime", "99.95%")

st.subheader("Executive Summary")
st.success("""
Status Operacional: Normal

Disponibilidade: 99.95%

Alarmes Críticos: 3

Recomendação:
Monitorar pico de CPU e crescimento de logs.
""")

st.markdown("---")

# ==========================================
# 5. SLA DASHBOARD & PERFORMANCE
# ==========================================
st.subheader("SLA Dashboard")
sla1, sla2, sla3 = st.columns(3)
sla1.metric("SLA", "99.95%")
sla2.metric("Incidentes", "4")
sla3.metric("Disponibilidade", "99.99%")

st.subheader("Performance")
perf1, perf2, perf3 = st.columns(3)
perf1.metric("CPU Avg", "82%")
perf2.metric("Memória", "68%")
perf3.metric("Network", "120 Mbps")

st.markdown("---")

# ==========================================
# 6. HEALTH OVERVIEW & SECURITY HEALTH POR SERVIÇO
# ==========================================
st.subheader("Health Overview")
health = 94
st.progress(health / 100)
st.success(f"Health Score: {health}%")

st.subheader("Security Health")
health_df = pd.DataFrame({
    "Serviço": ["EC2", "Lambda", "RDS", "S3", "CloudTrail"],
    "Health": [82, 95, 90, 76, 100]
})
st.dataframe(health_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 7. ALARMES ATIVOS, ALARMES POR SEVERIDADE & ANOMALY DETECTION
# ==========================================
st.subheader("Alarmes Ativos")
st.error("CPU EC2 acima de 90%")
st.warning("Pico de tráfego detectado")
st.warning("Volume de logs elevado")

st.subheader("Alarmes por Severidade")
a1, a2, a3 = st.columns(3)
a1.metric("Critical", 3)
a2.metric("High", 5)
a3.metric("Medium", 4)

st.subheader("Anomaly Detection")
st.warning("""
Anomalia detectada:

CPU acima da média histórica.

Horário: 14:08

Impacto: Médio
""")

st.markdown("---")

# ==========================================
# 8. MÉTRICAS E TENDÊNCIAS (CPU & LOGS)
# ==========================================
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.subheader("CloudWatch Metrics (Utilização %)")
    metrics = pd.DataFrame({
        "Serviço": ["EC2", "Lambda", "RDS", "S3"],
        "Utilização": [82, 45, 61, 38]
    })
    st.dataframe(metrics, use_container_width=True, hide_index=True)

with col_m2:
    st.subheader("Tendência Temporal de CPU (%)")
    trend = pd.DataFrame({
        "CPU": [60, 65, 70, 78, 82]
    })
    st.line_chart(trend)

st.subheader("Tendência de Logs")
logs_trend = pd.DataFrame({
    "Logs": [8000, 12000, 15000, 22000, 25400]
})
st.line_chart(logs_trend)

st.markdown("---")

# ==========================================
# 9. LOGS CENTRALIZADOS, TOP EVENTOS, STATUS DA INFRAESTRUTURA & CUSTOS
# ==========================================
col_l1, col_l2 = st.columns(2)

with col_l1:
    st.subheader("Logs Centralizados")
    logs = pd.DataFrame({
        "Hora": ["14:01", "14:04", "14:08"],
        "Evento": ["Login IAM", "CreateUser", "PutBucketPolicy"],
        "Severidade": ["Low", "Medium", "Critical"]
    })
    st.dataframe(logs, use_container_width=True, hide_index=True)

with col_l2:
    st.subheader("Top Eventos")
    top_events = pd.DataFrame({
        "Evento": ["ConsoleLogin", "CreateUser", "PutBucketPolicy", "RunInstances"],
        "Quantidade": [95, 12, 6, 9]
    })
    st.dataframe(top_events, use_container_width=True, hide_index=True)

st.subheader("Status da Infraestrutura")
infra = pd.DataFrame({
    "Componente": ["IAM", "S3", "EC2", "Lambda", "RDS", "CloudTrail"],
    "Status": ["Healthy", "Warning", "Healthy", "Healthy", "Healthy", "Healthy"]
})
st.dataframe(infra, use_container_width=True, hide_index=True)

st.subheader("Cloud Cost Monitoring")
costs = pd.DataFrame({
    "Serviço": ["EC2", "S3", "RDS", "CloudWatch"],
    "Custo ($)": [240, 50, 170, 25]
})
st.dataframe(costs, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 10. EXPORTAÇÃO DE RELATÓRIOS E LOGS
# ==========================================
st.subheader("Exportação")
st.download_button(
    "Exportar Logs (CSV)",
    logs.to_csv(index=False),
    file_name="cloudwatch_logs.csv",
    mime="text/csv"
)

relatorio_cloudwatch = f"""AWS CYBER DEFENSE PLATFORM - RELATÓRIO CLOUDWATCH
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Status: Normal | Disponibilidade: 99.95% | Alarmes Críticos: 3
--------------------------------------------------
Resumo de Métricas, Logs e Integridade Operacional consolidados com sucesso.
"""

st.download_button(
    "Exportar Relatório CloudWatch",
    relatorio_cloudwatch,
    file_name="relatorio_cloudwatch.txt",
    mime="text/plain"
)

st.markdown("---")

# ==========================================
# 11. MAPA DE MONITORAMENTO & CORRELAÇÃO DE SEGURANÇA
# ==========================================
st.subheader("Mapa de Monitoramento")
st.text("""
CloudWatch
│
├── EC2
├── RDS
├── Lambda
├── S3
├── CloudTrail
└── Security Center
""")

st.subheader("Observabilidade")
o1, o2, o3 = st.columns(3)
o1.metric("Logs", "25.4K")
o2.metric("Eventos", "4.2K")
o3.metric("Alarmes", "12")

st.subheader("Security Correlation & SOC Integration")
st.warning("""
CloudWatch
↓
CloudTrail
↓
GuardDuty
↓
IAM
↓
Attack Path
↓
Security Center
""")

st.success("""
Eventos enviados para:
✓ Security Center
✓ CloudTrail
✓ AWS Config
✓ Threat Intelligence
""")

st.markdown("---")

# ==========================================
# 12. CENTRO EDUCACIONAL (EXPENDABLES)
# ==========================================
st.subheader("Centro Educacional")

with st.expander("O que é CloudWatch?"):
    st.write("O Amazon CloudWatch é um serviço de monitoramento e observabilidade voltado para recursos da AWS e aplicativos executados na nuvem, coletando logs, métricas e eventos em tempo real.")

with st.expander("O que é Observabilidade?"):
    st.write("A observabilidade mede a capacidade de inferir o estado interno de um sistema complexo analisando suas saídas externas (métricas, logs e traces).")

with st.expander("O que é um Alarme?"):
    st.write("Um alarme do CloudWatch monitora uma única métrica ou o resultado de uma expressão matemática baseada em métricas, acionando ações automatizadas quando limites configurados são violados.")

st.markdown("---")

# ==========================================
# 13. CLOUDWATCH COPILOT & LABORATÓRIO DE SIMULAÇÕES AVANÇADAS
# ==========================================
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("CloudWatch Copilot")
    pergunta = st.text_area("Pergunte ao CloudWatch Copilot")
    if st.button("Analisar Métricas"):
        p = pergunta.lower()
        if "cpu" in p:
            st.info("CPU elevada detectada. Avalie Auto Scaling.")
        elif "autoscaling" in p:
            st.info("O Auto Scaling pode reduzir impactos de picos de CPU e tráfego.")
        elif "cloudtrail" in p:
            st.info("CloudTrail ativo gravando eventos na região com integridade validada.")
        elif "guardduty" in p:
            st.info("GuardDuty monitorando achados de ameaça e comportamentos anômalos.")
        elif "latência" in p:
            st.info("Latência média dentro dos limites operacionais tolerados.")
        elif "network" in p:
            st.info("Tráfego de rede estável sem indícios de exfiltração ativa.")
        elif "storage" in p:
            st.info("Utilização de S3 e EBS dentro da capacidade contratada.")
        elif "rds" in p:
            st.info("Conexões e IOPS do RDS em patamares normais.")
        elif "ec2" in p:
            st.info("Instâncias EC2 respondendo aos health checks com resiliência.")
        elif "lambda" in p:
            st.info("Tempo de execução Lambda e concorrência monitorados sem timeouts críticos.")
        elif "logs" in p:
            st.info("Volume de logs crescendo conforme o padrão analítico da plataforma.")
        else:
            st.info("Monitoramento e métricas analisadas com sucesso.")

with col_c2:
    st.subheader("Laboratório de Monitoramento")
    cenario = st.selectbox(
        "Simular",
        [
            "CPU Spike",
            "Memory Leak",
            "Lambda Timeout",
            "Network Surge",
            "Ransomware Activity",
            "DDoS Event"
        ]
    )
    if st.button("Executar Simulação"):
        st.success(f"Simulação avançada '{cenario}' iniciada com sucesso no ambiente.")

st.markdown("---")

# ==========================================
# 14. INTEGRAÇÃO COM A PLATAFORMA
# ==========================================
st.subheader("Integração com a Plataforma")

c_link1, c_link2, c_link3, c_link4, c_link5, c_link6 = st.columns(6)

with c_link1:
    st.page_link("pages/security_center.py", label="Security Center")
with c_link2:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")
with c_link3:
    st.page_link("pages/AWS_Config.py", label="AWS Config")
with c_link4:
    st.page_link("pages/Attack_Path.py", label="Attack Path")
with c_link5:
    st.page_link("pages/kali_lab.py", label="Kali Lab")
with c_link6:
    st.page_link("pages/pdf_reports.py", label="PDF Reports")

# ==========================================
# 15. RODAPÉ
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • CloudWatch & Observability Center • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")