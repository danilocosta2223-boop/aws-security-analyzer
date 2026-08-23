import streamlit as st
import pandas as pd
import json
import os

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="EC2 Security Center",
    page_icon="🖥️",
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
</style>
""", unsafe_allow_html=True)

# ==========================
# CARREGAR JSON
# ==========================
json_file = "reports/security_report.json"

if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ec2_findings = [
        item
        for item in data.get("findings", [])
        if item["service"].upper() == "EC2"
    ]
else:
    ec2_findings = []

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>🖥️ EC2 Security Center</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Auditoria de instâncias EC2, Security Groups, análise de vulnerabilidades e boas práticas de hardening.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Instâncias", "6")

with c2:
    st.metric("Security Groups", "8")

with c3:
    st.metric(
        "SSH Exposto",
        "1",
        delta="Atenção",
        delta_color="inverse"
    )

with c4:
    st.metric(
        "Instâncias Críticas",
        "1",
        delta="Risco"
    )

# ==========================
# EC2 SECURITY SCORE (MELHORIA)
# ==========================
st.markdown("---")
st.subheader("📊 EC2 Security Score")

ec2_score = 88

st.progress(ec2_score / 100)

st.metric(
    "Pontuação EC2",
    f"{ec2_score}/100"
)

# ==========================
# EXECUTIVE SUMMARY
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O ambiente possui instâncias EC2 monitoradas continuamente. 
Foi identificado um Security Group com a porta **SSH (22)** exposta globalmente para toda a Internet (`0.0.0.0/0`), representando um risco iminente de ataques de força bruta. 

Recomenda-se restringir imediatamente o acesso por IP de origem e validar os padrões de hardening das máquinas.
""")

# ==========================
# INVENTÁRIO EC2
# ==========================
st.markdown("---")
st.subheader("🖥️ Inventário de Instâncias")

ec2_df = pd.DataFrame({
    "Instância": [
        "i-0123456789abcdef0",
        "i-0987654321fedcba0",
        "i-11111111111111111"
    ],
    "Sistema": [
        "Amazon Linux",
        "Ubuntu 22.04",
        "Windows Server"
    ],
    "Status": [
        "Running",
        "Running",
        "Stopped"
    ],
    "Security Group": [
        "sg-web",
        "sg-public-ssh",
        "sg-internal"
    ],
    "Risco": [
        "Baixo",
        "Alto",
        "Baixo"
    ]
})

st.dataframe(
    ec2_df,
    use_container_width=True
)

# ==========================
# DISTRIBUIÇÃO DE RISCOS (MELHORIA)
# ==========================
st.markdown("---")
st.subheader("📈 Distribuição de Riscos")

risk_df = pd.DataFrame({
    "Risco": ["Baixo", "Médio", "Alto"],
    "Quantidade": [2, 0, 1]
})

st.bar_chart(
    risk_df.set_index("Risco")
)

# ==========================
# SECURITY GROUPS
# ==========================
st.markdown("---")
st.subheader("🌐 Análise de Security Groups")

sg_df = pd.DataFrame({
    "Security Group": [
        "sg-web",
        "sg-public-ssh",
        "sg-internal"
    ],
    "Porta": [
        "443",
        "22",
        "3306"
    ],
    "Origem": [
        "Internet",
        "0.0.0.0/0",
        "VPC Interna"
    ],
    "Status": [
        "OK",
        "Risco",
        "OK"
    ]
})

st.dataframe(
    sg_df,
    use_container_width=True
)

# ==========================
# FINDINGS EC2
# ==========================
st.markdown("---")
st.subheader("🚨 Findings Encontrados no Security Hub")

if ec2_findings:
    for finding in ec2_findings:
        st.error(f"""
**Recurso:** `{finding['resource']}`  
**Problema:** {finding['issue']}  
**Recomendação:** {finding['recommendation']}
""")
else:
    st.error("""
**Recurso:** `sg-public-ssh` / `i-0987654321fedcba0`  
**Problema:** Porta SSH (22) aberta para a Internet (`0.0.0.0/0`).  
**Impacto:** Exposição a varreduras de portas e tentativas de invasão por força bruta.  
**Recomendação:** Restringir o CIDR de origem para um IP corporativo seguro ou utilizar o AWS Systems Manager (SSM) Session Manager.
""")

# ==========================
# HARDENING
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Hardening")

st.checkbox("CloudWatch Agent instalado para coleta de logs", value=True, disabled=True)
st.checkbox("SSM Agent habilitado (gerenciamento sem SSH direto)", value=True, disabled=True)
st.checkbox("Porta SSH restrita a IPs confiáveis", value=False, disabled=True)
st.checkbox("Patches de segurança atualizados", value=True, disabled=True)
st.checkbox("Políticas de Backup configuradas (AWS Backup)", value=True, disabled=True)

# ==========================
# AWS CLI
# ==========================
st.markdown("---")
st.subheader("💻 Exemplo de Correção via AWS CLI")

st.code("""
aws ec2 revoke-security-group-ingress \\
    --group-id sg-public-ssh \\
    --protocol tcp \\
    --port 22 \\
    --cidr 0.0.0.0/0
""", language="bash")

# ==========================
# ROADMAP
# ==========================
st.markdown("---")
st.subheader("🛠️ Plano de Ação e Correção")

st.markdown("""
1. **Restringir Portas Críticas:** Ajustar as regras de entrada (*Inbound Rules*) dos Security Groups afetados.
2. **Adoção do SSM Session Manager:** Eliminar a necessidade de portas abertas para acesso administrativo remoto.
3. **Gestão de Vulnerabilidades:** Integrar e programar varreduras periódicas com o Amazon Inspector.
4. **Hardening de SO:** Validar o compliance das instâncias com benchmarks corporativos de segurança.
5. **Monitoramento Contínuo:** Configurar alertas automáticos para alterações suspeitas em Security Groups.
""")

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • EC2 Security Center")