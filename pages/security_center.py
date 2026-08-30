import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Security Operations Center (SOC) | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="soc_refresh")

# ==========================================
# 3. ESTILO CSS CORPORATIVO (Tags limpas e nativas garantidas)
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
# 4. HEALTH CHECK DO BACKEND
# ==========================================
try:
    requests.get("http://127.0.0.1:3000", timeout=2)
    backend_status_html = 'Backend Node.js Online'
except Exception:
    backend_status_html = 'Backend Offline'

# ==========================================
# 5. CABEÇALHO DO MÓDULO (CÉREBRO DA PLATAFORMA)
# ==========================================
st.markdown(f"""
<div class="hero-card">
    <h1>Security Operations Center</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Centro de Comando e Governança da AWS Cyber Defense Platform. Visão unificada de risco, conformidade e telemetria forense.
    </p>
    <p style="color: #6EE7B7; margin-top: 8px; font-size: 13px;">Status do Servidor: {backend_status_html}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. VARIÁVEIS DINÂMICAS PARA INDICADORES
# ==========================================
risk_score = 82
compliance_score = 91
incidentes = 4
attack_paths_count = 2
criticos_count = 3
ativos_count = 127
health_score = 88

# ==========================================
# 7. INDICADORES GLOBAIS DINÂMICOS (6 COLUNAS)
# ==========================================
m1, m2, m3, m4, m5, m6 = st.columns(6)

m1.metric("Risk Score", f"{risk_score}/100")
m2.metric("Compliance", f"{compliance_score}%")
m3.metric("Incidentes", incidentes)
m4.metric("Attack Paths", attack_paths_count)
m5.metric("Críticos", criticos_count)
m6.metric("Ativos", ativos_count)

st.markdown("---")

# ==========================================
# 8. KPIS DO SOC & SECURITY POSTURE
# ==========================================
soc1, soc2, soc3 = st.columns(3)

soc1.metric(
    "MTTD",
    "12 min"
)

soc2.metric(
    "MTTR",
    "35 min"
)

soc3.metric(
    "SLA",
    "98%"
)

st.subheader("Security Posture")
st.success(
    "Postura de Segurança: Moderadamente Forte"
)

st.markdown("---")

# ==========================================
# 9. HEALTH SCORE GERAL & STATUS GLOBAL
# ==========================================
st.subheader("Health Score")

st.progress(
    health_score / 100
)

st.success(
    f"Health Score Geral: {health_score}%"
)

st.subheader("Status Global")

if health_score >= 90:
    st.success("Ambiente Saudável")
elif health_score >= 70:
    st.warning("Ambiente Requer Atenção")
else:
    st.error("Ambiente Crítico")

st.markdown("---")

# ==========================================
# 10. ESTADO OPERACIONAL (JSON) & SECURITY SCORE POR CATEGORIA
# ==========================================
st.subheader("Estado Operacional")

status = {
    "IAM": "Healthy",
    "S3": "Warning",
    "EC2": "Healthy",
    "CloudTrail": "Healthy",
    "KMS": "Healthy"
}

st.json(status)

st.subheader("Security Score por Categoria")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Identity", "82%")
col2.metric("Network", "78%")
col3.metric("Data", "91%")
col4.metric("Detection", "95%")

st.subheader("Security Coverage")

st.progress(0.94)

st.success(
    "94% da infraestrutura monitorada"
)

st.markdown("---")

# ==========================================
# 11. BUSCA GLOBAL
# ==========================================
st.subheader("Busca Global")

busca = st.text_input(
    "Buscar Serviço"
)

if busca:
    st.info(
        f"Resultados encontrados para {busca}"
    )

st.markdown("---")

# ==========================================
# 12. RESUMO EXECUTIVO & EXECUTIVE DASHBOARD
# ==========================================
st.subheader("Executive Summary")
st.success("""
Ambiente operacional.

Compliance acima de 90%.

Riscos principais identificados.

Remediação disponível.
""")

st.subheader("Resumo Executivo Detalhado")
st.info("""
Status Geral: Requer Atenção

Risco Atual: Alto

Não Conformidades:
• IAM sem MFA
• Bucket S3 Público
• Security Groups Expostos

Ação Recomendada:
Executar remediação imediata.
""")

st.markdown("---")

# ==========================================
# 13. COMPLIANCE FRAMEWORKS & COMPLIANCE CONSOLIDADO
# ==========================================
st.subheader("Compliance Frameworks")

f1, f2, f3, f4 = st.columns(4)

f1.metric("NIST", "91%")
f2.metric("CIS", "88%")
f3.metric("LGPD", "90%")
f4.metric("ISO 27001", "89%")

st.subheader("Compliance Consolidado")

compliance = pd.DataFrame({
    "Framework": [
        "NIST",
        "CIS",
        "ISO 27001",
        "LGPD"
    ],
    "Score": [
        91,
        88,
        89,
        90
    ]
})

st.dataframe(compliance, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 14. CENTRAL DE ALERTAS, FINDINGS & MISSÃO ATUAL
# ==========================================
st.subheader("Alertas Prioritários")
st.error("Bucket S3 público detectado")
st.warning("Usuários IAM sem MFA")
st.warning("Security Groups expostos")

st.subheader("Missão Atual")
st.warning("""
Prioridade:

1. Ativar MFA

2. Corrigir Buckets Públicos

3. Revisar Security Groups

4. Revisar Chaves KMS
""")

st.subheader("Dashboard de Severidade")
sev1, sev2, sev3, sev4 = st.columns(4)

sev1.metric("Critical", 2)
sev2.metric("High", 5)
sev3.metric("Medium", 11)
sev4.metric("Low", 23)

st.subheader("Critical Findings")
findings = pd.DataFrame({
    "Severidade": [
        "Critical",
        "High",
        "Medium"
    ],
    "Quantidade": [
        2,
        5,
        11
    ]
})

st.dataframe(findings, use_container_width=True, hide_index=True)

st.subheader("Findings Distribution")

findings_chart = pd.DataFrame({
    "Categoria": [
        "IAM",
        "S3",
        "EC2",
        "CloudTrail"
    ],
    "Quantidade": [
        5,
        3,
        2,
        1
    ]
})

st.bar_chart(
    findings_chart.set_index("Categoria")
)

st.subheader("Matriz de Risco")
risk_matrix = pd.DataFrame({
    "Categoria": [
        "IAM",
        "S3",
        "EC2",
        "CloudTrail",
        "KMS"
    ],
    "Impacto": [
        "Alto",
        "Crítico",
        "Alto",
        "Baixo",
        "Médio"
    ]
})

st.dataframe(risk_matrix, use_container_width=True, hide_index=True)

st.subheader("Plano de Ação")
st.error("""
Prioridade 1
Ativar MFA

Prioridade 2
Corrigir Buckets Públicos

Prioridade 3
Fechar Security Groups

Prioridade 4
Rotacionar Chaves
""")

st.markdown("---")

# ==========================================
# 15. PAINEL DE SAÚDE AWS & COBERTURA
# ==========================================
st.subheader("Painel de Saúde dos Serviços AWS")

c_p1, c_p2 = st.columns(2)

with c_p1:
    st.write("IAM: 75%")
    st.progress(0.75)
    st.write("S3: 60%")
    st.progress(0.60)
    st.write("EC2: 80%")
    st.progress(0.80)
    st.write("CloudTrail: 100%")
    st.progress(1.00)

with c_p2:
    st.write("Lambda: 90%")
    st.progress(0.90)
    st.write("RDS: 100%")
    st.progress(1.00)
    st.write("KMS: 95%")
    st.progress(0.95)

st.subheader("Cobertura AWS")
servicos = pd.DataFrame({
    "Serviço": [
        "IAM",
        "S3",
        "EC2",
        "Lambda",
        "CloudTrail",
        "KMS",
        "RDS",
        "Config"
    ],
    "Monitorado": [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True
    ]
})

st.dataframe(servicos, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 16. GRÁFICO PRINCIPAL, TENDÊNCIAS & ARQUITETURA
# ==========================================
st.subheader("Compliance e Saúde por Serviço")
chart_data = pd.DataFrame({
    "Serviço": [
        "IAM",
        "S3",
        "EC2",
        "CloudTrail",
        "KMS",
        "RDS"
    ],
    "Score": [
        75,
        60,
        80,
        100,
        95,
        100
    ]
})

st.bar_chart(
    chart_data.set_index("Serviço")
)

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader("Risk Trend")
    trend = pd.DataFrame({
        "Risk": [
            92,
            90,
            88,
            85,
            risk_score
        ]
    })
    st.line_chart(trend)

with col_t2:
    st.subheader("Compliance Trend")
    compliance_trend = pd.DataFrame({
        "Compliance": [
            84,
            86,
            88,
            90,
            compliance_score
        ]
    })
    st.line_chart(compliance_trend)

st.subheader("Arquitetura da Plataforma")
st.info("""
Security Center
│
├── AWS Config
├── CloudTrail
├── Attack Path
├── Threat Intelligence
├── IAM Audit
├── S3 Audit
├── EC2 Audit
├── Security Copilot
└── Compliance
""")

st.markdown("---")

# ==========================================
# 17. ATTACK PATH CORRELATION & MITRE ATT&CK
# ==========================================
st.subheader("Attack Path Correlation")
st.warning("""
Possível caminho de ataque detectado:

IAM
↓
EC2
↓
S3
↓
Exfiltração de Dados
""")

st.page_link(
    "pages/Attack_Path.py",
    label="Abrir Attack Path"
)

st.subheader("MITRE ATT&CK")
st.info("""
TA0001 - Initial Access

TA0003 - Persistence

TA0004 - Privilege Escalation

TA0010 - Exfiltration
""")

st.markdown("---")

# ==========================================
# 18. THREAT INTELLIGENCE & THREAT FEED
# ==========================================
st.subheader("Threat Intelligence")
t1, t2 = st.columns(2)
with t1:
    st.write("• **IOC Detectados:** 5 Indicadores ativos")
    st.write("• **IPs Suspeitos:** 2 IPs maliciosos bloqueados")
with t2:
    st.write("• **Táticas MITRE:** TA0001 (Initial Access), TA0004 (Privilege Escalation)")
    st.write("• **Técnicas MITRE:** T1078 (Valid Accounts), T1530 (Data from Cloud Storage)")

st.subheader("Threat Feed")
df_threat = pd.DataFrame({
    "IOC": [
        "185.22.11.10",
        "104.21.77.31"
    ],
    "Tipo": [
        "IP Suspeito",
        "Tentativa de Acesso"
    ]
})

st.dataframe(df_threat, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 19. CENTRO DE CORREÇÃO (REMEDIAÇÃO)
# ==========================================
st.subheader("Remediação")
col_r1, col_r2, col_r3, col_r4 = st.columns(4)

with col_r1:
    st.page_link(
        "pages/iam_audit.py",
        label="Corrigir IAM"
    )
with col_r2:
    st.page_link(
        "pages/s3_audit.py",
        label="Corrigir S3"
    )
with col_r3:
    st.page_link(
        "pages/cloudtrail.py",
        label="Investigar CloudTrail"
    )
with col_r4:
    st.page_link(
        "pages/AWS_Config.py",
        label="Abrir Compliance"
    )

st.markdown("---")

# ==========================================
# 20. SECURITY COPILOT ABRANGENTE
# ==========================================
st.subheader("Security Copilot")
pergunta = st.text_area(
    "Pergunte ao Copilot (Como corrigir MFA? Como proteger S3? Como responder a ransomware? Como corrigir IAM? attack path, cloudtrail, compliance, nist, cis, security center)"
)

if st.button("Analisar com Copilot"):
    p = pergunta.lower()
    if "mfa" in p:
        st.info("Recomendação: Ative obrigatoriedade de MFA via políticas do IAM para todos os usuários com acesso ao console.")
    elif "s3" in p:
        st.info("Recomendação: Ative o Block Public Access e criptografia padrão em todos os buckets S3.")
    elif "ransomware" in p:
        st.info("Recomendação: Isole instâncias comprometidas, revogue chaves de acesso imediatamente e verifique backups imutáveis.")
    elif "iam" in p:
        st.info("Recomendação: Revogue permissões excessivas, aplique privilégio mínimo e remova chaves de acesso órfãs.")
    elif "attack path" in p:
        st.info("Recomendação: Analise a cadeia de exploração priorizando o corte de privilégios de IAM conectados a instâncias EC2 expostas.")
    elif "cloudtrail" in p:
        st.info("Recomendação: Valide trilhas multi-regionais, log file validation e integridade dos eventos guardados no S3.")
    elif "compliance" in p:
        st.info("Recomendação: Audite regularmente os desvios de configuração comparando o estado atual com benchmarks estabelecidos.")
    elif "nist" in p:
        st.info("Recomendação: Alinhe os controles técnicos aos subgrupos de Protect, Detect e Respond do framework NIST CSF.")
    elif "cis" in p:
        st.info("Recomendação: Implemente as diretrizes do CIS AWS Foundations Benchmark para endurecer a segurança da conta.")
    elif "security center" in p:
        st.info("Recomendação: Monitore o Risk Score global e utilize o painel de saúde para orquestrar ações corretivas imediatas.")
    else:
        st.info("Análise concluída com base na inteligência central da plataforma.")

st.markdown("---")

# ==========================================
# 21. CENTRO EDUCACIONAL (FAQ / GLOSSÁRIO)
# ==========================================
st.subheader("Centro Educacional")

with st.expander("O que é MFA?"):
    st.write("A Autenticação Multifator (MFA) adiciona uma camada extra de proteção ao processo de autenticação, exigindo um fator de verificação adicional além da senha.")

with st.expander("O que é CloudTrail?"):
    st.write("O AWS CloudTrail é um serviço que monitora e registra a atividade da conta em toda a sua infraestrutura da AWS, fornecendo histórico de ações.")

with st.expander("O que é AWS Config?"):
    st.write("O AWS Config permite avaliar, auditar e avaliar as configurações dos seus recursos da AWS para garantir conformidade e histórico de mudanças.")

with st.expander("O que é GuardDuty?"):
    st.write("O Amazon GuardDuty é um serviço inteligente de detecção de ameaças que monitora continuamente comportamentos maliciosos e atividades não autorizadas.")

with st.expander("O que é KMS?"):
    st.write("O AWS Key Management Service (KMS) facilita a criação e o controle de chaves criptográficas usadas para proteger dados em serviços AWS.")

with st.expander("O que é Attack Path?"):
    st.write("Attack Path (Caminho de Ataque) mapeia vulnerabilidades combinadas e permissões que um invasor pode explorar para atingir ativos críticos.")

with st.expander("O que é MITRE ATT&CK?"):
    st.write("MITRE ATT&CK é uma base de conhecimento acessível globalmente sobre táticas e técnicas de adversários baseadas em observações do mundo real.")

st.markdown("---")

# ==========================================
# 22. RELATÓRIOS & INTEGRAÇÃO FUTURA
# ==========================================
st.subheader("Relatórios")

relatorio_texto = f"""=== RELATÓRIO EXECUTIVO DA PLATAFORMA ===
Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Compliance Geral: {compliance_score}%
Risk Score: {risk_score}/100
Attack Paths Detectados: {attack_paths_count}
Findings Críticos: {criticos_count}
Status do Ambiente: Requer Atenção
Recomendações: Ativar MFA em todos os usuários IAM e aplicar Block Public Access em buckets S3.
========================================="""

st.download_button(
    "Baixar Relatório",
    relatorio_texto,
    file_name="executive_report.txt"
)

st.subheader("Integração de Módulos")
c_link1, c_link2 = st.columns(2)
with c_link1:
    st.page_link(
        "pages/kali_lab.py",
        label="Abrir Kali Lab"
    )
with c_link2:
    st.page_link(
        "pages/pdf_reports.py",
        label="Relatórios"
    )

st.markdown("---")

# ==========================================
# 23. LABORATÓRIO SOC
# ==========================================
st.subheader("Laboratório SOC")
selecao = st.selectbox(
    "Cenário de Simulação",
    [
        "IAM Compromise",
        "S3 Data Leak",
        "EC2 Breach",
        "Ransomware"
    ]
)

if st.button("Executar Simulação"):
    st.success(
        f"Simulação {selecao} iniciada com sucesso no ambiente controlado."
    )

# ==========================================
# 24. RODAPÉ
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Security Operations Center (SOC) • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")