import streamlit as st
import pandas as pd
import json
import os

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Network Security Center",
    page_icon="🌐",
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
# CARREGAR JSON (Opcional para Findings)
# ==========================
json_file = "reports/security_report.json"
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    net_findings = [
        item for item in data.get("findings", [])
        if item["service"].upper() in ["EC2", "VPC", "NETWORK"]
    ]
else:
    net_findings = []

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>🌐 Network Security Center</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Monitoramento de VPCs, Security Groups, Network ACLs e rastreamento de exposição de portas globais.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("VPCs", "3")

with c2:
    st.metric("Security Groups", "8")

with c3:
    st.metric(
        "Portas Expostas",
        "1",
        delta="Atenção",
        delta_color="inverse"
    )

with c4:
    st.metric(
        "Network Score",
        "88/100"
    )

# ==========================
# RESUMO EXECUTIVO
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O ambiente possui **3 VPCs** ativas e monitoradas continuamente. 
Foi identificada uma regra crítica de exposição de rede na porta **SSH (22)** acessível publicamente para a internet através do bloco `0.0.0.0/0`.

Recomenda-se restringir os acessos externos de gerenciamento, validar o uso de Bastion Hosts ou AWS Systems Manager, e revisar o isolamento das subnets privadas.
""")

# ==========================
# INVENTÁRIO DE VPCS
# ==========================
st.markdown("---")
st.subheader("☁️ Inventário de VPCs e Subnets")

vpc_df = pd.DataFrame({
    "VPC": [
        "vpc-production",
        "vpc-development",
        "vpc-security"
    ],
    "CIDR Block": [
        "10.0.0.0/16",
        "172.16.0.0/16",
        "192.168.0.0/16"
    ],
    "Subnets Públicas": [
        "2 (Multi-AZ)",
        "1",
        "0 (Isolada)"
    ],
    "Subnets Privadas": [
        "4",
        "2",
        "2"
    ],
    "Status": [
        "Ativo",
        "Ativo",
        "Ativo"
    ]
})

st.dataframe(
    vpc_df,
    use_container_width=True
)

# ==========================
# ANÁLISE DE SECURITY GROUPS
# ==========================
st.markdown("---")
st.subheader("🛡️ Mapeamento de Portas e Security Groups")

sg_net_df = pd.DataFrame({
    "Security Group": [
        "sg-prod-web",
        "sg-public-ssh",
        "sg-rds-db",
        "sg-internal-app"
    ],
    "Porta(s)": [
        "443, 80",
        "22",
        "3306",
        "8080"
    ],
    "Origem / Destino": [
        "Internet (0.0.0.0/0)",
        "Internet (0.0.0.0/0)",
        "VPC Prod (10.0.0.0/16)",
        "VPC Internal"
    ],
    "Classificação de Risco": [
        "Baixo (Esperado)",
        "Alto (Crítico)",
        "Baixo",
        "Baixo"
    ]
})

st.dataframe(
    sg_net_df,
    use_container_width=True
)

# ==========================
# ALERTAS DE REDE
# ==========================
st.markdown("---")
st.subheader("🚨 Alertas de Exposição de Rede")

st.error("""
**Recurso:** `sg-public-ssh` (Porta 22)  
**Problema:** Acesso SSH aberto globalmente para `0.0.0.0/0`.  
**Impacto:** Permite que qualquer ator na internet realize varreduras e ataques automatizados de força bruta contra a infraestrutura.  
**Correção Recomendada:** Alterar o CIDR de origem para o IP corporativo ou desativar o acesso direto via porta 22 migrando para o AWS SSM Session Manager.
""")

# ==========================
# CHECKLIST DE CONFORMIDADE DE REDE
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Segurança de Perímetro")

st.checkbox("Fluxo de tráfego monitorado via VPC Flow Logs", value=True, disabled=True)
st.checkbox("Isolamento adequado entre subnets públicas e privadas", value=True, disabled=True)
st.checkbox("Nenhuma regra de Security Group permissiva (0.0.0.0/0 em portas sensíveis)", value=False, disabled=True)
st.checkbox("Network ACLs restritivas aplicadas nas subnets", value=True, disabled=True)

# ==========================
# EXEMPLO DE CORREÇÃO VIA CLI
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
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • Network Security Center")