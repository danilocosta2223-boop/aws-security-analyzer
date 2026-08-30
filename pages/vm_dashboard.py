import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="VM Dashboard | AWS Cyber Defense",
    page_icon=None,
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
# 3. CABEÇALHO DO MÓDULO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>Executive VM Dashboard</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Painel executivo central de monitoramento, governança, postura de segurança, custos e inteligência operacional da frota AWS EC2.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# 4. EXECUTIVE SUMMARY
# ==========================
st.subheader("Executive Summary")

st.info("""
Ambiente EC2 monitorado em tempo real.

• 12 instâncias registradas na frota global  
• 9 instâncias em execução (Running)  
• 3 instâncias paradas (Stopped)  
• Compliance geral médio de 94%  
• Nenhum incidente crítico ativo no momento  
""")

st.markdown("---")

# ==========================
# 5. VM FLEET OVERVIEW
# ==========================
st.subheader("VM Fleet Overview")

v1, v2, v3, v4 = st.columns(4)

v1.metric("Total VMs", 12)
v2.metric("Running", 9)
v3.metric("Stopped", 3)
v4.metric("Security Score", "92%")

st.markdown("---")

# ==========================
# 6. SCORES (SECURITY & HEALTH)
# ==========================
st.subheader("VM Security Score")

score = 92
st.progress(score / 100)
st.success(f"Score Geral do Ambiente EC2: {score}%")

st.subheader("Fleet Health Score")

health = 95
st.progress(health / 100)
st.success(f"Saúde Geral da Frota: {health}%")

st.markdown("---")

# ==========================
# 7. DISTRIBUIÇÃO E RECURSOS
# ==========================
st.subheader("Operating System Distribution")

os_df = pd.DataFrame({
    "Sistema": [
        "Ubuntu",
        "Amazon Linux",
        "Windows"
    ],
    "Quantidade": [
        5,
        4,
        3
    ]
})

st.bar_chart(
    os_df.set_index("Sistema")
)

st.subheader("Resource Utilization")

resource_df = pd.DataFrame({
    "Dia": [
        "Seg",
        "Ter",
        "Qua",
        "Qui",
        "Sex"
    ],
    "CPU": [
        52,
        61,
        57,
        65,
        59
    ]
})

st.line_chart(
    resource_df.set_index("Dia")
)

st.markdown("---")

# ==========================
# 8. SECURITY POSTURE
# ==========================
st.subheader("Security Posture")

p1, p2, p3, p4 = st.columns(4)
p1.metric("Criptografadas", "10/12")
p2.metric("MFA", "100%")
p3.metric("SSM", "11/12")
p4.metric("CloudWatch", "12/12")

st.markdown("---")

# ==========================
# 9. INVENTÁRIO, PATCH & VULNERABILIDADES
# ==========================
st.subheader("EC2 Inventory")

inventory = pd.DataFrame({
    "Nome": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01"
    ],
    "SO": [
        "Ubuntu",
        "Amazon Linux",
        "Windows"
    ],
    "Status": [
        "Running",
        "Running",
        "Stopped"
    ],
    "Risco": [
        "Baixo",
        "Baixo",
        "Médio"
    ]
})

st.dataframe(
    inventory,
    use_container_width=True,
    hide_index=True
)

st.subheader("Patch Management")

patch_df = pd.DataFrame({
    "Instância": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01"
    ],
    "Status": [
        "Atualizada",
        "Atualizada",
        "Pendente"
    ]
})

st.dataframe(
    patch_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("Vulnerability Dashboard")

vuln_df = pd.DataFrame({
    "Vulnerabilidade": [
        "Open SSH",
        "RDP Exposure",
        "Outdated Package"
    ],
    "Severidade": [
        "High",
        "Critical",
        "Medium"
    ]
})

st.dataframe(
    vuln_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 10. VM SECURITY RANKING
# ==========================
st.subheader("VM Security Ranking")

ranking = pd.DataFrame({
    "VM": [
        "prod-db-01",
        "prod-web-01",
        "dev-app-01"
    ],
    "Score": [
        98,
        94,
        81
    ]
})

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 11. COMPLIANCE & ATTACK SURFACE
# ==========================
st.subheader("Compliance Status")

c1, c2, c3, c4 = st.columns(4)
c1.metric("CIS AWS", "96%")
c2.metric("ISO 27001", "94%")
c3.metric("NIST", "92%")
c4.metric("PCI-DSS", "88%")

st.subheader("Attack Surface")

attack = pd.DataFrame({
    "Controle": [
        "SSH",
        "RDP",
        "EBS Encryption"
    ],
    "Status": [
        "2 Expostos",
        "1 Exposto",
        "10/12 Habilitado"
    ]
})

st.dataframe(
    attack,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 12. SECURITY HUB FINDINGS
# ==========================
st.subheader("Security Hub Findings")

findings = pd.DataFrame({
    "Finding": [
        "SSH Open",
        "EBS Unencrypted",
        "RDP Open"
    ],
    "Severidade": [
        "High",
        "Critical",
        "Critical"
    ]
})

st.dataframe(
    findings,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 13. COST OVERVIEW & ANALYTICS
# ==========================
st.subheader("Cost Overview")

cost_df = pd.DataFrame({
    "Instância": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01"
    ],
    "Custo Mensal": [
        "$18",
        "$70",
        "$8"
    ]
})

st.dataframe(
    cost_df,
    use_container_width=True,
    hide_index=True
)

total_cost = 18 + 70 + 8
st.metric(
    "Custo Total Mensal",
    f"${total_cost}"
)

st.markdown("---")

# ==========================
# 14. DEPLOYMENT & INCIDENT TIMELINE
# ==========================
st.subheader("Deployment History")

deploys = pd.DataFrame({
    "Data": [
        "29/08/2026",
        "28/08/2026",
        "27/08/2026"
    ],
    "VM": [
        "prod-web-01",
        "prod-db-01",
        "dev-app-01"
    ],
    "Status": [
        "Sucesso",
        "Sucesso",
        "Sucesso"
    ]
})

st.dataframe(
    deploys,
    use_container_width=True,
    hide_index=True
)

st.subheader("Incident Timeline")

timeline = pd.DataFrame({
    "Horário": [
        "08:00",
        "09:15",
        "10:30"
    ],
    "Evento": [
        "SSH Open Detectado",
        "Análise Security Hub",
        "Remediação Aplicada"
    ]
})

st.dataframe(
    timeline,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 15. EC2 COPILOT & INSIGHTS
# ==========================
st.subheader("EC2 Copilot")

pergunta = st.text_area("Pergunte sobre a frota de instâncias EC2, segurança ou custos:")

if st.button("Analisar Ambiente"):
    p = pergunta.lower()
    if "custo" in p:
        st.info("💡 **Análise do Copilot:** A instância `prod-db-01` (`m5.large`) possui o maior custo mensal atual ($70/mês), recomendando-se avaliar instâncias reserved ou otimização de volume.")
    elif "ssh" in p:
        st.info("💡 **Análise do Copilot:** Foram identificadas instâncias com porta SSH exposta. Recomenda-se migrar o acesso administrativo para o AWS Systems Manager Session Manager.")
    elif "compliance" in p:
        st.info("💡 **Análise do Copilot:** O ambiente possui compliance médio de 94%, com destaque para CIS AWS e ISO 27001 em níveis saudáveis.")
    else:
        st.info("💡 **Análise geral concluída:** A frota encontra-se estável, com monitoramento ativo e postura de segurança adequada.")

st.subheader("Copilot Insights")

st.info("""
A IA identificou:

• SSH exposto em 2 instâncias  
• 1 VM sem criptografia  
• Compliance geral de 94%  
• Nenhum incidente ativo  
""")

st.markdown("---")

# ==========================
# 16. NAVEGAÇÃO INTEGRADA
# ==========================
st.subheader("Navegação Integrada")

ic1, ic2, ic3, ic4, ic5 = st.columns(5)
with ic1:
    st.page_link("pages/vm_creator.py", label="VM Creator")
with ic2:
    st.page_link("pages/security_hub.py", label="Security Hub")
with ic3:
    st.page_link("pages/security_copilot.py", label="Security Copilot")
with ic4:
    st.page_link("pages/compliance.py", label="Compliance")
with ic5:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")

# ==========================
# RODAPÉ DA PÁGINA
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • Executive VM Dashboard Module • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")