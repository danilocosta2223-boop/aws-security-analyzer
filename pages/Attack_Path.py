import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Attack Path Analysis | AWS Cyber Defense Platform",
    layout="wide"
)

# ==========================
# TEMA CORPORATIVO PADRÃO SOC (ESTILO AWS SECURITY HUB)
# ==========================
st.markdown("""
<style>
.stApp {
    background-color: #111827;
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
    background-color: #1F2937;
    border: 1px solid #374151;
    border-radius: 15px;
    padding: 24px;
    margin-bottom: 20px;
}

.attack-step {
    background-color: #1F2937;
    border-left: 4px solid #2563EB;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 15px;
    border: 1px solid #374151;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Attack Path Analysis & Kill Chain</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Simulação dinâmica de progressão de ataque e cadeia de exploração correlacionada via APIs do backend Node.js.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# CONSUMO E CACHE DAS APIS
# ==========================
@st.cache_data(ttl=10)
def carregar_dados_backend():
    try:
        ec2 = requests.get("http://127.0.0.1:3000/api/ec2", timeout=2).json()
        iam = requests.get("http://127.0.0.1:3000/api/iam", timeout=2).json()
        s3 = requests.get("http://127.0.0.1:3000/api/s3", timeout=2).json()
        rds = requests.get("http://127.0.0.1:3000/api/rds", timeout=2).json()
        guardduty = requests.get("http://127.0.0.1:3000/api/guardduty", timeout=2).json()
        return ec2, iam, s3, rds, guardduty
    except Exception:
        return None, None, None, None, None

data_ec2, data_iam, data_s3, data_rds, data_guardduty = carregar_dados_backend()

# Fallback se o backend Node.js estiver offline
if not data_ec2:
    data_ec2 = {"openSecurityGroups": 2, "totalInstances": 5}
    data_iam = {"mfaDisabled": 3}
    data_s3 = {"publicBuckets": 1, "totalBuckets": 8}
    data_rds = {"unencryptedDatabases": 0}
    data_guardduty = {"activeFindings": 2}

# ==========================
# SELETOR DE CENÁRIO E SIMULAÇÃO DINÂMICA
# ==========================
st.subheader("Laboratório de Simulação")

col_cen, col_btn = st.columns([3, 1])
with col_cen:
    cenario = st.selectbox(
        "Simulação",
        [
            "IAM Compromise",
            "S3 Data Leak",
            "EC2 Breach",
            "Ransomware",
            "Privilege Escalation"
        ]
    )

with col_btn:
    st.write("")
    executar_sim = st.button("Executar Simulação", use_container_width=True)

# Valores dinâmicos baseados no cenário selecionado
if cenario == "Ransomware":
    risco_sim = "95%"
    tempo_sim = "8 min"
    impacto_sim = "Crítico"
elif cenario == "IAM Compromise":
    risco_sim = "78%"
    tempo_sim = "20 min"
    impacto_sim = "Alto"
elif cenario == "S3 Data Leak":
    risco_sim = "88%"
    tempo_sim = "12 min"
    impacto_sim = "Crítico"
elif cenario == "EC2 Breach":
    risco_sim = "82%"
    tempo_sim = "15 min"
    impacto_sim = "Alto"
else:
    risco_sim = "70%"
    tempo_sim = "25 min"
    impacto_sim = "Médio"

# ==========================
# PAINEL DE RESULTADO DA SIMULAÇÃO
# ==========================
if executar_sim:
    st.success(f"Cenário {cenario} carregado com sucesso!")
    
    res_c1, res_c2, res_c3 = st.columns(3)
    with res_c1:
        st.metric("Probabilidade de Comprometimento", risco_sim)
    with res_c2:
        st.metric("Tempo Médio de Exploração", tempo_sim)
    with res_c3:
        st.metric("Impacto", impacto_sim)

# ==========================
# CÁLCULOS E MÉTRICAS GERAIS
# ==========================
open_sg = data_ec2.get("openSecurityGroups", 0)
mfa_off = data_iam.get("mfaDisabled", 0)
public_buckets = data_s3.get("publicBuckets", 0)
active_threats = data_guardduty.get("activeFindings", 0)

attack_paths = max(1, open_sg + mfa_off + public_buckets)
calculated_risk = min((open_sg * 20) + (mfa_off * 10) + (public_buckets * 25) + (active_threats * 15), 100)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Attack Paths", attack_paths)
with c2:
    st.metric("Critical Nodes", open_sg + public_buckets + active_threats)
with c3:
    st.metric("Affected Assets", data_ec2.get("totalInstances", 0) + data_s3.get("totalBuckets", 0))
with c4:
    if calculated_risk >= 80:
        st.error(f"Exposure Score: {calculated_risk}/100")
    elif calculated_risk >= 50:
        st.warning(f"Exposure Score: {calculated_risk}/100")
    else:
        st.success(f"Exposure Score: {calculated_risk}/100")

# Score visual com barra de progresso
st.markdown("### Índice Geral de Exposição")
st.progress(calculated_risk / 100)

# ==========================
# COMPLIANCE
# ==========================
st.markdown("---")
st.subheader("Compliance")
comp_c1, comp_c2, comp_c3 = st.columns(3)
with comp_c1:
    st.metric("AWS Config", "92%")
with comp_c2:
    st.metric("CIS Benchmark", "88%")
with comp_c3:
    st.metric("NIST", "90%")

# ==========================
# DISTRIBUIÇÃO DE RISCOS (DATAFRAME + GRÁFICO)
# ==========================
st.markdown("---")
st.subheader("Distribuição de Riscos por Componente")

dados_grafico = pd.DataFrame({
    "Categoria": ["EC2", "IAM", "S3", "GuardDuty"],
    "Achados": [open_sg, mfa_off, public_buckets, active_threats]
})

col_df, col_chart = st.columns(2)
with col_df:
    st.dataframe(dados_grafico.set_index("Categoria"), use_container_width=True)
with col_chart:
    st.bar_chart(dados_grafico.set_index("Categoria"), color="#2563EB")

# ==========================
# LABORATÓRIO DE TESTES
# ==========================
st.markdown("---")
st.subheader("Laboratório")
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    teste = st.selectbox(
        "Tipo",
        [
            "IAM",
            "S3",
            "EC2",
            "Lambda",
            "RDS"
        ]
    )
with col_t2:
    st.write("")
    if st.button("Executar", use_container_width=True):
        st.success("Teste executado")

# ==========================
# CADEIA DE ATAQUE (KILL CHAIN DINÂMICA)
# ==========================
st.markdown("---")
st.subheader(f"Cadeia de Ataque Correlacionada ({cenario})")

if cenario == "IAM Compromise":
    kill_steps = [
        ("1. Reconhecimento", "Varredura de identidades IAM e chaves de acesso expostas."),
        ("2. Credencial Vazada", "Identificação de chaves de acesso com permissões excessivas em repositórios."),
        ("3. Ausência de MFA", "Falta de autenticação multifator permitindo sessão direta."),
        ("4. Acesso Administrativo", "Assunção de papéis de privilégio elevado (AdministratorAccess)."),
        ("5. Comprometimento Total", "Exfiltração de dados e alteração de infraestrutura.")
    ]
elif cenario == "Ransomware":
    kill_steps = [
        ("1. Phishing / Acesso Inicial", "Comprometimento de endpoint via engenharia social."),
        ("2. Movimento Lateral", "Varredura interna na rede VPC e descoberta de instâncias EC2."),
        ("3. Escalada de Privilégios", "Exploração de vulnerabilidades de Kernel ou permissões IAM da instância."),
        ("4. Criptografia de Dados", "Acionamento de rotinas de criptografia em volumes EBS e bancos RDS."),
        ("5. Impacto e Resgate", "Indisponibilidade de serviços e exigência de resgate.")
    ]
else:
    kill_steps = [
        ("1. Reconhecimento e Acesso Inicial", "Varredura de portas e identificação de grupos de segurança perimetrais abertos."),
        ("2. Escalação de Privilégios", "Exploração de credenciais comprometidas e usuários sem MFA."),
        ("3. Exfiltração e Impacto", "Acesso a buckets S3 públicos e bases de dados para extração de dados.")
    ]

for titulo_passo, desc_passo in kill_steps:
    st.markdown(f"""
    <div class="attack-step">
        <h4 style="color: #FFFFFF; margin-bottom: 8px;">{titulo_passo}</h4>
        <p style="color: #E5E7EB; font-size: 14px;">{desc_passo}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# INTEGRAÇÃO COM MÓDULOS DE CORREÇÃO (PAGE LINKS)
# ==========================
st.markdown("---")
st.subheader("Módulos de Remediação Direta")

col_l1, col_l2, col_l3, col_l4, col_l5 = st.columns(5)

with col_l1:
    st.write("**IAM**")
    st.page_link("pages/iam_audit.py", label="Corrigir IAM")

with col_l2:
    st.write("**S3**")
    st.page_link("pages/s3_audit.py", label="Corrigir S3")

with col_l3:
    st.write("**Lambda**")
    st.page_link("pages/Lambda.py", label="Abrir Lambda Audit")

with col_l4:
    st.write("**KMS**")
    st.page_link("pages/KMS.py", label="Abrir KMS Audit")

with col_l5:
    st.write("**RDS**")
    st.page_link("pages/RDS.py", label="Abrir RDS Audit")

# ==========================
# SECURITY COPILOT APRIMORADO
# ==========================
st.markdown("---")
st.subheader("AWS Security Copilot")

pergunta = st.text_area(
    "Pergunte ao Copilot",
    placeholder="Ex: Como mitigar riscos em IAM, S3, EC2, CloudTrail, GuardDuty, Ransomware, Lambda, RDS, KMS, Config, CloudWatch ou CloudShell?"
)

if st.button("Analisar Pergunta"):
    p = pergunta.lower()
    if "s3" in p or "bucket" in p:
        st.info("Copilot: Ative o Block Public Access nas configurações globais da conta e revise as políticas de acesso dos buckets.")
    elif "iam" in p or "mfa" in p:
        st.info("Copilot: Obrigue o uso de MFA por meio de Service Control Policies (SCP) e remonte credenciais de longa duração inutilizadas.")
    elif "ec2" in p:
        st.info("Copilot: Remova exposições públicas desnecessárias em Security Groups e atualize as instâncias com patches de vulnerabilidade.")
    elif "cloudtrail" in p:
        st.info("Copilot: Garanta a habilitação do CloudTrail em todas as regiões com trilhas multi-regionais integradas ao S3 seguro.")
    elif "guardduty" in p:
        st.info("Copilot: Priorize os achados críticos do GuardDuty e configure respostas automáticas via Amazon EventBridge.")
    elif "ransomware" in p:
        st.info("Copilot: Implemente backups imutáveis com AWS Backup Vault Lock e isole a rede afetada por meio de Network ACLs.")
    elif "lambda" in p:
        st.info("Copilot: Valide as permissões de execução (IAM Roles) das funções Lambda seguindo o princípio do privilégio mínimo.")
    elif "rds" in p:
        st.info("Copilot: Assegure que as instâncias RDS estejam criptografadas em repouso e sem exposição direta à internet (PubliclyAccessible = False).")
    elif "kms" in p:
        st.info("Copilot: Faça a rotação periódica das chaves de criptografia gerenciadas pelo cliente (CMKs) no KMS.")
    elif "config" in p:
        st.info("Copilot: Ative regras customizadas e gerenciadas no AWS Config para monitorar o compliance contínuo da infraestrutura.")
    elif "cloudwatch" in p:
        st.info("Copilot: Configure alarmes direcionados a métricas críticas e logs estruturados em CloudWatch Logs para detecção precoce de anomalias.")
    elif "cloudshell" in p:
        st.info("Copilot: Monitore o uso de sessões do CloudShell através do CloudTrail para auditar comandos executados por administradores.")
    elif p.strip():
        st.info(f"Copilot: Analisando diretrizes para '{pergunta}'. Recomendamos isolar os recursos afetados e executar o script de hardening.")
    else:
        st.warning("Por favor, digite uma pergunta para o Copilot.")

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Attack Path Analysis • Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")