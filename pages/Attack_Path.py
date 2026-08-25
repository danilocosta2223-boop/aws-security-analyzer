import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Attack Path Analysis | AWS Cyber Defense Platform",
    page_icon=None,
    layout="wide"
)

# ==========================
# ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================
st_autorefresh(interval=15000, key="attack_path_refresh")

# ==========================
# ESTILO VISUAL CORPORATIVO
# ==========================
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

.attack-step {
    background-color: #f8f9fa;
    border-left: 5px solid #1e3a8a;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    border-top: 1px solid #e5e7eb;
    border-right: 1px solid #e5e7eb;
    border-bottom: 1px solid #e5e7eb;
}

h1, h2, h3, h4 {
    color: #1e3a8a;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Attack Path Analysis</h1>
    <p style="color: #4b5563; margin: 0; font-size: 15px;">
        Simulação dinâmica de progressão de ataque e cadeia de exploração correlacionada via APIs do backend Node.js.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# CONSUMO E CACHE DAS APIS
# ==========================
@st.cache_data(ttl=10)
def carregar_dados_backend():
    ec2 = requests.get("http://127.0.0.1:3000/api/ec2").json()
    iam = requests.get("http://127.0.0.1:3000/api/iam").json()
    s3 = requests.get("http://127.0.0.1:3000/api/s3").json()
    rds = requests.get("http://127.0.0.1:3000/api/rds").json()
    kms = requests.get("http://127.0.0.1:3000/api/kms").json()
    lambda_data = requests.get("http://127.0.0.1:3000/api/lambda").json()
    guardduty = requests.get("http://127.0.0.1:3000/api/guardduty").json()
    config = requests.get("http://127.0.0.1:3000/api/config").json()
    return ec2, iam, s3, rds, kms, lambda_data, guardduty, config

# Tratamento de Erro caso o Backend esteja desligado
try:
    data_ec2, data_iam, data_s3, data_rds, data_kms, data_lambda, data_guardduty, data_config = carregar_dados_backend()
except Exception:
    st.error("Backend indisponível. Execute node server.js.")
    st.stop()

# ==========================
# CÁLCULOS E MÉTRICAS DINÂMICAS
# ==========================
open_sg = data_ec2.get("openSecurityGroups", 0)
mfa_off = data_iam.get("mfaDisabled", 0)
public_buckets = data_s3.get("publicBuckets", 0)
unencrypted_rds = data_rds.get("unencryptedDatabases", 0)
outdated_lambdas = data_lambda.get("outdatedRuntimes", 0)
active_threats = data_guardduty.get("activeFindings", 0)

# Contagem dinâmica de Attack Paths
attack_paths = 0
if open_sg > 0: attack_paths += 1
if mfa_off > 0: attack_paths += 1
if public_buckets > 0: attack_paths += 1
if attack_paths == 0: attack_paths = 1

# Cálculo dinâmico do Exposure Score
calculated_risk = min((open_sg * 20) + (mfa_off * 10) + (public_buckets * 25) + (active_threats * 15), 100)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Attack Paths Identificados", attack_paths)
with c2:
    st.metric("Critical Nodes", open_sg + public_buckets + active_threats)
with c3:
    st.metric("Affected Assets", data_ec2.get("totalInstances", 0) + data_s3.get("totalBuckets", 0) + data_rds.get("totalDatabases", 0))
with c4:
    st.metric("Attack Exposure Score", f"{calculated_risk}/100")

# ==========================
# RESUMO EXECUTIVO DINÂMICO
# ==========================
st.markdown("---")
st.subheader("Executive Summary")

summary_items = []
if open_sg > 0:
    summary_items.append(f"Detectadas {open_sg} instâncias EC2 com grupos de segurança perimetrais expostos.")
if mfa_off > 0:
    summary_items.append(f"Identificados {mfa_off} usuários IAM operando sem autenticação multifator (MFA).")
if public_buckets > 0:
    summary_items.append(f"Encontrados {public_buckets} buckets S3 com políticas de acesso público.")
if active_threats > 0:
    summary_items.append(f"GuardDuty reportou {active_threats} ameaças ativas no perímetro de nuvem.")

if summary_items:
    st.write("Foram correlacionadas vulnerabilidades ativas no ambiente que formam um vetor crítico de exploração:")
    for item in summary_items:
        st.write(f"- {item}")
else:
    st.success("Nenhum caminho crítico de ataque ativo detectado no momento com base nas APIs monitoradas.")

# ==========================
# ATIVOS AFETADOS REAIS
# ==========================
st.markdown("---")
st.subheader("Ativos Afetados")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Instâncias EC2 em Risco:**")
    for vm in data_ec2.get("instances", []):
        st.write(f"- {vm.get('name')} (SG: {vm.get('securityGroup')}) - Risco: {vm.get('risk')}")

with col_b:
    st.markdown("**Buckets S3 Críticos:**")
    for bucket in data_s3.get("buckets", []):
        if bucket.get('publicAccess'):
            st.write(f"- {bucket.get('name')} - Status: {bucket.get('status')}")

# ==========================
# CADEIA DE ATAQUE (ATTACK PATH)
# ==========================
st.markdown("---")
st.subheader("Attack Path Simulation (Kill Chain)")

st.markdown(f"""
<div class="attack-step">
    <h4 style="margin: 0 0 8px 0; color: #1e3a8a;">1. Initial Access & Reconnaissance</h4>
    <p style="margin: 0; color: #4b5563; font-size: 14px;">
        <b>Vetor:</b> {open_sg} Instância(s) EC2 com portas administrativas abertas ao público e {active_threats} alerta(s) do GuardDuty.<br>
        <b>Origem da API:</b> <code>/api/ec2</code> & <code>/api/guardduty</code>
    </p>
</div>

<div class="attack-step">
    <h4 style="margin: 0 0 8px 0; color: #1e3a8a;">2. Privilege Escalation & IAM Abuse</h4>
    <p style="margin: 0; color: #4b5563; font-size: 14px;">
        <b>Vetor:</b> {mfa_off} Usuário(s) IAM sem MFA ativo e chaves de acesso vulneráveis.<br>
        <b>Origem da API:</b> <code>/api/iam</code>
    </p>
</div>

<div class="attack-step">
    <h4 style="margin: 0 0 8px 0; color: #1e3a8a;">3. Data Exposure & Impact</h4>
    <p style="margin: 0; color: #4b5563; font-size: 14px;">
        <b>Vetor:</b> {public_buckets} Bucket(s) S3 expostos e {unencrypted_rds} banco(s) RDS sem criptografia adequada.<br>
        <b>Origem da API:</b> <code>/api/s3</code> & <code>/api/rds</code>
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# CORRELAÇÃO MITRE ATT&CK
# ==========================
st.markdown("---")
st.subheader("MITRE ATT&CK Correlation")

st.markdown("""
| Técnica ID | Tática | Nome da Técnica |
|------------|--------|-----------------|
| T1078 | Initial Access | Valid Accounts |
| T1133 | Persistence | External Remote Services |
| T1098 | Privilege Escalation | Account Manipulation |
| T1530 | Collection | Data from Cloud Storage |
""")

# ==========================
# ACHADOS CRÍTICOS & PLANO DE CORREÇÃO
# ==========================
st.markdown("---")
st.subheader("Plano de Interrupção do Attack Path")

st.markdown("""
1. **Remoção de Regras Perimetrais Inseguras:** Restringir o tráfego de entrada nas instâncias EC2 mapeadas na API `/api/ec2`.
2. **Imposição de MFA Corporativo:** Obrigar o uso de MFA para todos os perfis listados na auditoria de `/api/iam`.
3. **Bloqueio de Acesso Público no S3:** Ativar o recurso *S3 Block Public Access* nos buckets retornados em `/api/s3`.
""")

# ==========================
# RODAPÉ COM TIMESTAMP
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Attack Path Analysis Center • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")