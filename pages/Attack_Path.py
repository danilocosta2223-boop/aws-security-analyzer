import streamlit as st

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Attack Path Analysis",
    page_icon="🧠",
    layout="wide"
)

# ==========================
# ESTILO VISUAL
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
    margin-bottom: 20px;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);
}

.attack-step {
    background-color: #1e293b;
    padding: 18px;
    border-radius: 10px;
    border-left: 5px solid #ef4444;
    margin-bottom: 12px;
    border-top: 1px solid #334155;
    border-right: 1px solid #334155;
    border-bottom: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>🧠 Attack Path Analysis</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Simulação de progressão de ataque e cadeia de exploração (Kill Chain) baseada nas vulnerabilidades correlacionadas na AWS.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Attack Paths", "1")

with c2:
    st.metric("Critical Nodes", "2")

with c3:
    st.metric("Affected Assets", "3")

with c4:
    st.metric("Risk Score", "92/100", delta="Crítico", delta_color="inverse")

# ==========================
# RESUMO EXECUTIVO
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
Foi mapeado um **caminho crítico de ataque (Attack Path)** que conecta brechas de configuração e permissões excessivas entre serviços da AWS. 

Um invasor externo pode explorar a exposição inicial de uma instância EC2, realizar escalação de privilégios via papéis IAM mal configurados e atingir os dados confidenciais armazenados em buckets S3 sem criptografia adequada.
""")

# ==========================
# CADEIA DE ATAQUE (ATTACK PATH)
# ==========================
st.markdown("---")
st.subheader("🎯 Attack Path Simulation (Kill Chain)")

st.markdown("""
<div class="attack-step">
    <h4 style="margin: 0 0 8px 0; color: #ef4444;">1. Initial Access & Reconnaissance</h4>
    <p style="margin: 0; color: #94a3b8; font-size: 14px;">
        <b>Vetor:</b> Instância EC2 (<code>db-test</code> ou worker legado) com porta SSH (22) exposta publicamente a partir de <code>0.0.0.0/0</code>.<br>
        <b>Impacto:</b> Tentativas de força bruta bem-sucedidas ou exploração de serviço desatualizado.
    </p>
</div>

<div class="attack-step">
    <h4 style="margin: 0 0 8px 0; color: #f59e0b;">2. Privilege Escalation & IAM Abuse</h4>
    <p style="margin: 0; color: #94a3b8; font-size: 14px;">
        <b>Vetor:</b> A instância comprometida possui uma <b>IAM Role excessivamente permissiva</b> (contendo coringa <code>*</code> em ações de gerenciamento).<br>
        <b>Impacto:</b> O atacante assume permissões administrativas temporárias no ambiente de nuvem.
    </p>
</div>

<div class="attack-step">
    <h4 style="margin: 0 0 8px 0; color: #ef4444;">3. Lateral Movement & Discovery</h4>
    <p style="margin: 0; color: #94a3b8; font-size: 14px;">
        <b>Vetor:</b> Uso das credenciais roubadas para listar recursos adjacentes (RDS, Lambdas e demais chaves no KMS).<br>
        <b>Impacto:</b> Mapeamento completo da infraestrutura interna e descoberta de segredos desprotegidos.
    </p>
</div>

<div class="attack-step" style="border-left-color: #dc2626;">
    <h4 style="margin: 0 0 8px 0; color: #dc2626;">4. Data Exfiltration / Impact</h4>
    <p style="margin: 0; color: #94a3b8; font-size: 14px;">
        <b>Vetor:</b> Acesso direto a buckets S3 e bases RDS sem criptografia adequada ou com políticas públicas resquiciosas.<br>
        <b>Impacto:</b> Vazamento em massa de dados corporativos confidenciais e credenciais de clientes.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MITRE CORRELATION
# ==========================
st.markdown("---")
st.subheader("🎯 MITRE ATT&CK Correlation")

st.markdown("""
| Técnica | Nome |
|----------|----------|
| T1078 | Valid Accounts |
| T1110 | Brute Force |
| T1087 | Account Discovery |
| T1098 | Account Manipulation |
| T1530 | Data from Cloud Storage |
| T1020 | Automated Exfiltration |
""")

# ==========================
# RECOMENDAÇÃO DE CORREÇÃO
# ==========================
st.markdown("---")
st.subheader("🛠️ Plano de Interrupção do Attack Path")

st.markdown("""
1. **Fechar o Acesso Perimetral:** Remover imediatamente a regra de entrada global na porta 22 dos Security Groups da EC2.
2. **Aplicar Menor Privilégio:** Substituir as IAM Roles com permissões globais por políticas granulares e restritas aos recursos necessários.
3. **Isolamento de Dados:** Habilitar criptografia mandatória (SSE-KMS) e bloqueio de acesso público (Block Public Access) nos buckets S3.
""")

# ==========================
# ATTACK SURFACE SCORE
# ==========================
st.markdown("---")
st.subheader("📊 Attack Surface Score")

surface_score = 92

st.progress(surface_score / 100)

st.metric(
    "Attack Exposure",
    f"{surface_score}/100"
)

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • Attack Path Analysis Center")