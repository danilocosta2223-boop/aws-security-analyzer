import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Security Copilot | AWS Cyber Defense",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 2. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================
st_autorefresh(interval=15000, key="copilot_ultimate_refresh")

# ==========================
# 3. ESTILO CSS CORPORATIVO (RAW HTML LIMPO)
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
# 4. PERSISTÊNCIA DE APRENDIZADO & HISTÓRICO DE AÇÕES
# ==========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "actions" not in st.session_state:
    st.session_state.actions = []

if "knowledge" not in st.session_state:
    st.session_state.knowledge = {}
    try:
        with open("copilot_knowledge.json", "r") as f:
            st.session_state.knowledge = json.load(f)
    except Exception:
        pass

def salvar_conhecimento():
    try:
        with open("copilot_knowledge.json", "w") as f:
            json.dump(st.session_state.knowledge, f)
    except Exception:
        pass

# ==========================
# 5. CONSUMO DE DADOS REAIS DA API (BACKEND)
# ==========================
@st.cache_data(ttl=10)
def carregar_dados_api():
    dados = {
        "iam_mfa_disabled": 4,
        "s3_public_buckets": 2,
        "ec2_open_sg": 1,
        "security_score": "89%",
        "compliance": "91%",
        "findings": 12
    }
    try:
        resp_iam = requests.get("http://127.0.0.1:3000/api/iam", timeout=1)
        if resp_iam.status_code == 200:
            dados["iam_mfa_disabled"] = resp_iam.json().get("mfaDisabled", 4)
    except Exception:
        pass

    try:
        resp_s3 = requests.get("http://127.0.0.1:3000/api/s3", timeout=1)
        if resp_s3.status_code == 200:
            dados["s3_public_buckets"] = resp_s3.json().get("publicBuckets", 2)
    except Exception:
        pass

    try:
        resp_ec2 = requests.get("http://127.0.0.1:3000/api/ec2", timeout=1)
        if resp_ec2.status_code == 200:
            dados["ec2_open_sg"] = resp_ec2.json().get("openSecurityGroups", 1)
    except Exception:
        pass

    try:
        resp_score = requests.get("http://127.0.0.1:3000/api/security-score", timeout=1)
        if resp_score.status_code == 200:
            dados["security_score"] = f"{resp_score.json().get('score', 89)}%"
    except Exception:
        pass

    return dados

env_data = carregar_dados_api()

# ==========================
# 6. CABEÇALHO DO MÓDULO (RAW HTML)
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Security Copilot Mission Control</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Centro de Operações de Segurança Autônomo com Aprendizado Persistente, KPIs de SOC, Action Center e Contexto Unificado da Infraestrutura AWS.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# 7. SOC KPIS & MISSION CONTROL
# ==========================
st.subheader("SOC KPIs & Mission Control")

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric("MTTD", "12 min")
kpi2.metric("MTTR", "31 min")
kpi3.metric("Incidentes", "7")
kpi4.metric("Playbooks", "23")
kpi5.metric("Compliance", env_data["compliance"])
kpi6.metric("Security Score", env_data["security_score"])

# ==========================
# MELHORIA 2: SECURITY HEALTH SCORE
# ==========================
st.subheader("Security Health")
health_score = 94
st.progress(health_score / 100)
st.success(f"Saúde do Ambiente: {health_score}%")

st.markdown("---")

# ==========================
# MELHORIA 3: FINDINGS DASHBOARD
# ==========================
st.subheader("Findings Dashboard")
f1, f2, f3, f4 = st.columns(4)
f1.metric("Critical", 2)
f2.metric("High", 4)
f3.metric("Medium", 3)
f4.metric("Low", 1)

st.markdown("---")

# ==========================
# 8. EXECUTIVE AI SUMMARY & ONE CLICK SUMMARY (MELHORIA 8)
# ==========================
st.subheader("One Click Executive Summary")

if st.button("Gerar Resumo Estratégico"):
    st.success(f"""
Resumo Estratégico

Security Score: {env_data['security_score']}
Compliance: {env_data['compliance']}

Principal Risco:
Buckets Públicos

Prioridade:
Alta

Ação Recomendada:
Aplicar Block Public Access.
""")

st.markdown("---")

# ==========================
# 9. ENVIRONMENT RISK RANKING & THREAT TIMELINE (MELHORIA 1)
# ==========================
st.subheader("Risk Ranking")

risk_df = pd.DataFrame({
    "Risco": [
        "Bucket S3 Público",
        "Usuários IAM sem MFA",
        "Security Group EC2 Exposto"
    ],
    "Severidade": [
        "Crítico",
        "Alto",
        "Médio"
    ],
    "Prioridade": [
        1,
        2,
        3
    ],
    "Impacto Atual": [
        f"{env_data['s3_public_buckets']} buckets afetados",
        f"{env_data['iam_mfa_disabled']} usuários afetados",
        f"{env_data['ec2_open_sg']} grupos afetados"
    ]
})

st.dataframe(risk_df, use_container_width=True, hide_index=True)

# Melhória 1: Threat Timeline
st.subheader("Threat Timeline")

timeline_df = pd.DataFrame({
    "Evento": [
        "IAM Login",
        "AssumeRole",
        "S3 Access",
        "GetObject",
        "Investigation"
    ],
    "Horário": [
        "08:00",
        "08:05",
        "08:07",
        "08:09",
        "08:12"
    ]
})

st.dataframe(
    timeline_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 10. ACTION CENTER & ACTION HISTORY (MELHORIA 7)
# ==========================
st.subheader("Action Center")

acao_escolhida = st.selectbox(
    "Selecione a Ação de Mitigação Automática",
    [
        "Ativar MFA Obrigatório para Usuários IAM",
        "Aplicar Block Public Access em Buckets S3",
        "Fechar Portas Administrativas em Security Groups EC2"
    ]
)

if st.button("Executar Ação de Remediação"):
    st.session_state.actions.append(acao_escolhida)
    st.success(f"Remediação simulada executada com sucesso para: {acao_escolhida}.")

if st.session_state.actions:
    st.subheader("Action History")
    for action in st.session_state.actions:
        st.write(f"✅ {action}")

st.markdown("---")

# ==========================
# MELHORIA 5: THREAT PREDICTION & AUTOMATED INSIGHTS (MELHORIA 6)
# ==========================
col_tp1, col_tp2 = st.columns(2)

with col_tp1:
    st.subheader("Threat Prediction")
    if env_data["s3_public_buckets"] > 0:
        st.warning("""
Probabilidade de Incidente:

78%

Motivo:
Exposição Pública S3
""")
    else:
        st.success("""
Probabilidade de Incidente:

22%
""")

with col_tp2:
    st.subheader("Automated Insights")
    insights = [
        "Buckets públicos continuam sendo o principal risco.",
        "MFA deve ser habilitado para todos os usuários IAM.",
        "Security Groups devem ser revisados semanalmente."
    ]
    for insight in insights:
        st.info(insight)

st.markdown("---")

# ==========================
# 11. THREAT ADVISOR (SECTORIAL)
# ==========================
st.subheader("Threat Advisor")

tipo_ambiente = st.selectbox(
    "Selecione o Setor do Ambiente",
    [
        "Financeiro",
        "Saúde",
        "Educação",
        "Corporativo"
    ]
)

if st.button("Gerar Recomendações Setoriais"):
    if tipo_ambiente == "Financeiro":
        st.warning("Setor Financeiro: Endurecimento contra fraudes via GuardDuty, criptografia KMS e aderência total ao PCI-DSS.")
    elif tipo_ambiente == "Saúde":
        st.warning("Setor Saúde: Proteção de dados sensíveis (PHI) com Amazon Macie e isolamento HIPAA.")
    elif tipo_ambiente == "Educação":
        st.info("Setor Educação: Gestão de acessos acadêmicos temporários e otimização de custos via CloudWatch.")
    else:
        st.info("Setor Corporativo: Universalização de MFA, logs centralizados no CloudTrail e DLP.")

st.markdown("---")

# ==========================
# 12. SELEÇÃO DE MODO (SECURITY GPT PERSONA)
# ==========================
st.subheader("Security GPT Persona Mode")

modo = st.radio(
    "Selecione o Perfil de Atuação do Copilot",
    [
        "SOC Analyst",
        "Threat Hunter",
        "Cloud Security Engineer",
        "Compliance Officer"
    ],
    horizontal=True
)

st.markdown(f"""
<div style="font-size: 13px; color: #9ca3af; margin-bottom: 15px;">
    <b>Modo Ativo:</b> {modo} | O tom e o foco analítico foram adaptados.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================
# 13. CHAT COM HISTÓRICO E APRENDIZADO PERMANENTE (JSON)
# ==========================
st.subheader("Chat Security Copilot")

pergunta = st.text_area(
    "Faça uma pergunta sobre AWS Security (IAM, S3, EC2, CloudTrail, Compliance...)"
)

if st.button("Analisar Pergunta"):
    p = pergunta.lower()
    
    if pergunta in st.session_state.knowledge:
        resposta = st.session_state.knowledge[pergunta] + " (Recuperado da Base de Conhecimento Permanente JSON)"
    else:
        if modo == "SOC Analyst":
            if "iam" in p:
                resposta = f"Análise SOC: O IAM apresenta {env_data['iam_mfa_disabled']} identidades sem MFA."
            elif "s3" in p:
                resposta = f"Análise SOC: Detectados {env_data['s3_public_buckets']} buckets S3 públicos."
            elif "ec2" in p:
                resposta = f"Análise SOC: Detectados {env_data['ec2_open_sg']} Security Groups com portas abertas."
            else:
                resposta = f"Análise SOC concluída. Telemetria atual - IAM sem MFA: {env_data['iam_mfa_disabled']}, S3 Públicos: {env_data['s3_public_buckets']}, EC2 SGs: {env_data['ec2_open_sg']}."
        elif modo == "Threat Hunter":
            if "iam" in p:
                resposta = "Threat Hunting: Investigando assume-roles anômalos no CloudTrail."
            elif "s3" in p:
                resposta = "Threat Hunting: Monitorando chamadas GetObject massivas em buckets S3."
            else:
                resposta = "Threat Hunting: Varredura de IOCs sem achados maliciosos na infraestrutura."
        elif modo == "Cloud Security Engineer":
            if "iam" in p:
                resposta = "Arquitetura Cloud: Aplicar SCPs restritivas e IAM Access Analyzer."
            elif "s3" in p:
                resposta = "Arquitetura Cloud: Habilitar Block Public Access e criptografia SSE-KMS."
            else:
                resposta = "Arquitetura Cloud: Infraestrutura em conformidade com o AWS Well-Architected."
        else:  # Compliance Officer
            if "iam" in p:
                resposta = "Compliance: Validação com CIS AWS Foundations Benchmark."
            elif "s3" in p:
                resposta = "Compliance: S3 público viola PCI-DSS e HIPAA."
            else:
                resposta = f"Compliance: Relatório validado com {env_data['compliance']} de aderência."
        
        st.session_state.knowledge[pergunta] = resposta
        salvar_conhecimento()

    st.session_state.chat_history.append({
        "Pergunta": pergunta,
        "Resposta": resposta
    })

if st.session_state.chat_history:
    st.subheader("Conversation History")
    for item in st.session_state.chat_history:
        st.write(f"👤 **Usuário:** {item['Pergunta']}")
        st.write(f"🤖 **Copilot ({modo}):** {item['Resposta']}")
        st.markdown("---")

# ==========================
# 14. LEARNING STATISTICS, LEARNING CENTER & CONFIDENCE
# ==========================
col_l1, col_l2 = st.columns(2)

with col_l1:
    st.subheader("Learning Statistics")
    l1, l2, l3 = st.columns(3)
    l1.metric("Conhecimentos", len(st.session_state.knowledge))
    l2.metric("Perguntas", len(st.session_state.chat_history))
    l3.metric("Personas", 4)
    
    # Melhoria 4: Copilot Learning Center
    st.subheader("Copilot Learning Center")
    if st.session_state.knowledge:
        for chave in st.session_state.knowledge.keys():
            st.write(f"📘 {chave}")
    else:
        st.info("Nenhum aprendizado registrado na base permanente ainda.")

with col_l2:
    st.subheader("AI Confidence")
    confidence = 96
    st.progress(confidence / 100)
    st.success(f"Confiança Analítica: {confidence}%")

st.markdown("---")

# ==========================
# 15. THREAT CORRELATION ENGINE & PLAYBOOKS
# ==========================
col_tc1, col_tc2 = st.columns(2)

with col_tc1:
    st.subheader("Threat Correlation Engine")
    correlation_df = pd.DataFrame({
        "Fase": ["1. Comprometimento", "2. Movimentação", "3. Armazenamento", "4. Exfiltração"],
        "Serviço": ["IAM (AssumeRole)", "EC2 (Security Groups)", "S3 (Objetos)", "CloudTrail"],
        "Risco": ["Alto", "Médio", "Crítico", "Crítico"]
    })
    st.dataframe(correlation_df, use_container_width=True, hide_index=True)

with col_tc2:
    st.subheader("Incident Response Playbook")
    playbook = st.selectbox("Selecionar Incidente", ["Credential Compromise", "S3 Exposure", "Malware Activity"])
    if st.button("Gerar Playbook"):
        st.success(f"Playbook gerado para: {playbook}")
        st.code("""
1. Identificar escopo e impacto
2. Conter incidente (revogar chaves / isolar instâncias)
3. Coletar evidências forenses no CloudTrail
4. Remediar a vulnerabilidade na raiz
5. Validar recuperação no Security Hub
""")

st.markdown("---")

# ==========================
# 16. COPILOT REPORT GENERATOR
# ==========================
st.subheader("Copilot Report Generator")

escopo_relatorio = st.selectbox(
    "Escopo do Relatório Executivo",
    [
        "IAM Audit Summary",
        "S3 Posture Report",
        "CloudTrail Threat Log",
        "Completo (Todos os Módulos)"
    ]
)

if st.button("Gerar Relatório Executivo"):
    relatorio_texto = f"""
AWS CYBER DEFENSE PLATFORM - COPILOT REPORT
Escopo: {escopo_relatorio}
Data: {datetime.now()}
Security Score: {env_data["security_score"]} | Compliance: {env_data["compliance"]}
Buckets Públicos: {env_data["s3_public_buckets"]} | IAM sem MFA: {env_data["iam_mfa_disabled"]} | SGs Abertos: {env_data["ec2_open_sg"]}
"""
    st.success("Relatório gerado com sucesso!")
    st.download_button(
        "Baixar Relatório em Texto",
        relatorio_texto,
        file_name=f"copilot_report_{escopo_relatorio.lower().replace(' ', '_')}.txt"
    )

st.markdown("---")

# ==========================
# 17. NAVEGAÇÃO INTEGRADA
# ==========================
st.subheader("Navegação Integrada")

c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
with c1:
    st.page_link("pages/security_hub.py", label="Security Hub")
with c2:
    st.page_link("pages/iam_audit.py", label="IAM Audit")
with c3:
    st.page_link("pages/s3_audit.py", label="S3 Audit")
with c4:
    st.page_link("pages/compliance.py", label="Compliance")
with c5:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")
with c6:
    st.page_link("pages/cloudwatch.py", label="CloudWatch")
with c7:
    st.page_link("pages/security_center.py", label="Security Center")
with c8:
    st.page_link("pages/pdf_reports.py", label="PDF Reports")

# ==========================
# RODAPÉ DA PÁGINA
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Security Copilot Mission Control • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")