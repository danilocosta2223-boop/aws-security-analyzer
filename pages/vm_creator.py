import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="VM Creator | AWS Cyber Defense",
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
    <h1>AWS EC2 VM Creator</h1>
    <p style="color: #9ca3af; margin: 0; font-size: 15px;">
        Plataforma enterprise de provisionamento seguro de máquinas virtuais com validações de compliance, hardening e modelagem de ameaças.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# 4. EXECUTIVE DASHBOARD
# ==========================
st.subheader("Executive Dashboard")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Instâncias", 12)
c2.metric("Running", 9)
c3.metric("Stopped", 3)
c4.metric("Compliance", "94%")

st.markdown("---")

# ==========================
# 5. EC2 PROVISIONING WIZARD
# ==========================
st.subheader("EC2 Provisioning Wizard")

col_w1, col_w2 = st.columns(2)
with col_w1:
    nome_vm = st.text_input("Nome da VM", value="prod-web-server-01")
    sistema = st.selectbox(
        "Sistema Operacional",
        [
            "Amazon Linux 2023",
            "Ubuntu 24.04 LTS",
            "Windows Server 2025",
            "Red Hat Enterprise Linux"
        ]
    )
with col_w2:
    tipo = st.selectbox(
        "Tipo da Instância",
        [
            "t2.micro",
            "t3.small",
            "t3.medium",
            "m5.large"
        ]
    )

# ==========================
# 6. NETWORK CONFIGURATION
# ==========================
st.subheader("Network Configuration")

col_n1, col_n2 = st.columns(2)
with col_n1:
    vpc = st.selectbox(
        "VPC",
        [
            "prod-vpc",
            "dev-vpc",
            "security-vpc"
        ]
    )
with col_n2:
    subnet = st.selectbox(
        "Subnet",
        [
            "private-subnet-a",
            "private-subnet-b",
            "public-subnet-a"
        ]
    )

st.markdown("---")

# ==========================
# 7. SECURITY CONFIGURATION
# ==========================
st.subheader("Security Configuration")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    mfa = st.checkbox("Exigir MFA Administrativo", value=True)
with col_s2:
    encrypted = st.checkbox("Criptografia EBS", value=True)
with col_s3:
    ssm = st.checkbox("AWS Systems Manager", value=True)
with col_s4:
    cloudwatch = st.checkbox("CloudWatch Agent", value=True)

st.markdown("---")

# ==========================
# 8. COMPLIANCE VALIDATION & SECURITY SCORE
# ==========================
st.subheader("Compliance Validation")

if encrypted:
    st.success("Criptografia EBS habilitada de acordo com os padrões corporativos.")
else:
    st.error("Alerta de Compliance: Criptografia EBS não habilitada.")

st.subheader("VM Security Score")

score = 100
if not encrypted:
    score -= 25
if not mfa:
    score -= 20

# ==========================
# 9. ATTACK SURFACE ANALYSIS & RISK ASSESSMENT
# ==========================
st.subheader("Attack Surface Analysis")

col_as1, col_as2 = st.columns(2)
with col_as1:
    porta22 = st.checkbox("Porta SSH (22)", value=False)
with col_as2:
    porta3389 = st.checkbox("RDP (3389)", value=False)

if porta22:
    st.warning("Atenção: Porta SSH (22) exposta diretamente para a internet aumenta significativamente a superfície de ataque.")
    score -= 15

if porta3389:
    st.warning("Atenção: Porta RDP (3389) exposta representa alto risco de brute-force.")
    score -= 20

score = max(0, score)

st.progress(score / 100)
st.metric("Score de Segurança", f"{score}%")

# Executive Risk Rating
st.subheader("Executive Risk Rating")

if score >= 90:
    st.success("Risco Baixo")
elif score >= 70:
    st.warning("Risco Moderado")
else:
    st.error("Risco Alto")

st.subheader("Risk Assessment")

risk = []
if porta22:
    risk.append("SSH exposto")
if porta3389:
    risk.append("RDP exposto")
if not encrypted:
    risk.append("Sem criptografia")

if risk:
    for item in risk:
        st.warning(f"Risco Detectado: {item}")
else:
    st.success("Nenhum risco crítico identificado na configuração atual.")

st.markdown("---")

# ==========================
# 10. COMPLIANCE FRAMEWORKS
# ==========================
st.subheader("Compliance Frameworks")

frameworks = pd.DataFrame({
    "Framework": [
        "CIS AWS",
        "ISO 27001",
        "NIST",
        "PCI-DSS"
    ],
    "Status": [
        "Conforme" if score >= 80 else "Atenção",
        "Conforme" if encrypted else "Não Conforme",
        "Conforme" if ssm else "Atenção",
        "Conforme" if (encrypted and not porta22 and not porta3389) else "Atenção"
    ]
})

st.dataframe(
    frameworks,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 11. AMI INTELLIGENCE & SIZING ADVISOR
# ==========================
st.subheader("AMI Intelligence")

if "Ubuntu" in sistema:
    st.info("Ubuntu 24.04 LTS selecionado: Imagem base moderna com suporte a AppArmor e atualizações automáticas de segurança ativadas.")
elif "Windows" in sistema:
    st.warning("Windows Server selecionado: Requer hardening adicional de políticas de grupo (GPO) e desativação de protocolos legados (SMBv1).")
elif "Amazon Linux" in sistema:
    st.info("Amazon Linux 2023 selecionado: Otimizado para performance na AWS com kernel minimalista e pacotes atualizados.")
else:
    st.info("Red Hat Enterprise Linux selecionado: Suporte corporativo de longa duração (LTS) habilitado.")

st.subheader("Resource Sizing Advisor")

if tipo == "t2.micro":
    st.info("Ideal para laboratórios e ambientes leves.")
elif tipo == "t3.small":
    st.info("Indicado para ambientes de desenvolvimento e homologação.")
elif tipo == "t3.medium":
    st.info("Indicado para aplicações corporativas padrão.")
elif tipo == "m5.large":
    st.warning("Maior custo operacional, validar necessidade de capacidade computacional dedicada.")

st.markdown("---")

# ==========================
# 12. DISASTER RECOVERY READINESS
# ==========================
st.subheader("Disaster Recovery")

backup_score = 100
if not encrypted:
    backup_score -= 30

st.progress(backup_score / 100)
st.metric("DR Readiness", f"{backup_score}%")

st.markdown("---")

# ==========================
# 13. AWS WELL-ARCHITECTED REVIEW
# ==========================
st.subheader("Well-Architected Review")

wa_df = pd.DataFrame({
    "Pilar": [
        "Security",
        "Reliability",
        "Performance",
        "Cost Optimization"
    ],
    "Status": [
        "OK" if score >= 80 else "Atenção",
        "OK" if backup_score >= 80 else "Atenção",
        "OK",
        "Atenção" if tipo == "m5.large" else "OK"
    ]
})

st.dataframe(
    wa_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 14. HARDENING RECOMMENDATIONS
# ==========================
st.subheader("Hardening Recommendations")

recomendacoes = pd.DataFrame({
    "Controle": [
        "MFA",
        "CloudWatch",
        "SSM",
        "Criptografia"
    ],
    "Status": [
        "OK" if mfa else "Pendente",
        "OK" if cloudwatch else "Pendente",
        "OK" if ssm else "Pendente",
        "OK" if encrypted else "Pendente"
    ]
})

st.dataframe(
    recomendacoes,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 15. COST ESTIMATOR
# ==========================
st.subheader("Cost Estimator")

custos = {
    "t2.micro": 8,
    "t3.small": 18,
    "t3.medium": 35,
    "m5.large": 70
}

st.info(f"Custo estimado mensal para a instância {tipo} na VPC `{vpc}`: **US$ {custos[tipo]} / mês**")

st.markdown("---")

# ==========================
# 16. DEPLOYMENT APPROVAL & SIMULATION
# ==========================
st.subheader("Deployment Approval")

aprovador = st.selectbox(
    "Aprovador",
    [
        "Cloud Team",
        "Security Team",
        "Infrastructure Team"
    ]
)

if st.button("Solicitar Aprovação"):
    st.success(f"Deploy enviado para validação de {aprovador}!")

st.markdown("---")

st.subheader("Deploy Simulation")

if st.button("Provisionar VM e Integrar com Plataforma"):
    st.success(f"Instância **{nome_vm}** criada com sucesso na subnet `{subnet}` (`{vpc}`)!")
    st.info("Deploy registrado com sucesso no CloudTrail, gerando telemetria para o Security Copilot e avaliando os findings abaixo no Security Hub:")

    finding_list = []
    severity_list = []
    
    if porta22:
        finding_list.append("SSH Open (Port 22)")
        severity_list.append("High")
    if porta3389:
        finding_list.append("RDP Open (Port 3389)")
        severity_list.append("Critical")
    if not encrypted:
        finding_list.append("No Encryption (EBS unencrypted)")
        severity_list.append("Critical")
    
    if not finding_list:
        finding_list.append("Nenhum finding gerado - Posture excelente")
        severity_list.append("Low")

    finding_df = pd.DataFrame({
        "Finding": finding_list,
        "Severity": severity_list
    })

    st.dataframe(
        finding_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# ==========================
# 17. SECURITY HUB INTEGRATION SCORE
# ==========================
st.subheader("Security Hub Integration")

hub_score = 100
if porta22:
    hub_score -= 15
if porta3389:
    hub_score -= 25
if not encrypted:
    hub_score -= 30

hub_score = max(0, hub_score)
st.metric("Security Hub Readiness", f"{hub_score}%")

st.markdown("---")

# ==========================
# 18. DEPLOYMENT TIMELINE
# ==========================
st.subheader("Deployment Timeline")

timeline = pd.DataFrame({
    "Etapa": [
        "Provisionamento",
        "Hardening",
        "CloudWatch",
        "CloudTrail",
        "Security Hub"
    ],
    "Status": [
        "OK",
        "OK",
        "OK" if cloudwatch else "Pendente",
        "OK",
        "OK"
    ]
})

st.dataframe(
    timeline,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 19. EC2 COPILOT (ASSISTENTE DE IA)
# ==========================
st.subheader("EC2 Copilot")

question = st.text_area("Pergunte sobre arquitetura, segurança ou otimização de instâncias EC2:")

if st.button("Analisar EC2 com IA"):
    p = question.lower()
    if "ssh" in p:
        st.info("💡 **Recomendação do Copilot:** Recomenda-se fortemente utilizar o AWS Systems Manager (SSM Session Manager) ao invés de manter a porta SSH (22) aberta no Security Group, eliminando a necessidade de bastion hosts.")
    elif "criptografia" in p or "ebs" in p:
        st.info("💡 **Recomendação do Copilot:** Utilize sempre EBS Encryption com chaves gerenciadas pelo AWS KMS (Customer Managed Keys) para atender a critérios rigorosos de auditoria da ISO 27001 e PCI-DSS.")
    elif "custo" in p:
        st.info("💡 **Recomendação do Copilot:** Para cargas de trabalho previsíveis, considere adquirir instâncias Reserved Instances ou Savings Plans para reduzir o custo da {tipo} em até 40%.")
    else:
        st.info("💡 **Análise EC2 concluída:** A configuração da instância está alinhada às melhores práticas gerais de arquitetura bem estruturada da AWS (Well-Architected Framework).")

st.markdown("---")

# ==========================
# 20. INFRASTRUCTURE REPORT
# ==========================
st.subheader("Infrastructure Report")

relatorio = f"""
AWS CYBER DEFENSE PLATFORM - VM PROVISIONING REPORT
Data: {datetime.now()}
--------------------------------------------------
Nome da VM: {nome_vm}
Sistema Operacional: {sistema}
Tipo de Instância: {tipo}
VPC: {vpc} | Subnet: {subnet}
Security Score: {score}%
Executive Risk: {"Baixo" if score >= 90 else ("Moderado" if score >= 70 else "Alto")}

Configurações de Segurança:
- Criptografia EBS: {encrypted}
- MFA Administrativo: {mfa}
- AWS Systems Manager: {ssm}
- CloudWatch Agent: {cloudwatch}
- Porta 22 Aberta: {porta22}
- Porta 3389 Aberta: {porta3389}
"""

st.download_button(
    "Baixar Relatório de Infraestrutura",
    relatorio,
    file_name="vm_report.txt"
)

st.markdown("---")

# ==========================
# 21. KNOWLEDGE CENTER
# ==========================
st.subheader("EC2 Knowledge Center")

with st.expander("O que é EBS Encryption?"):
    st.write("Protege seus volumes de dados em repouso na AWS, utilizando chaves gerenciadas pelo KMS para garantir confidencialidade e integridade.")

with st.expander("O que é AWS Systems Manager?"):
    st.write("Permite o gerenciamento seguro e remoto de instâncias sem a necessidade de abrir portas administrativas como SSH (22) ou RDP (3389).")

st.markdown("---")

# ==========================
# 22. INTEGRAÇÃO COM A PLATAFORMA
# ==========================
st.subheader("Integração com a Plataforma")

ic1, ic2, ic3, ic4 = st.columns(4)
with ic1:
    st.page_link("pages/security_hub.py", label="Security Hub")
with ic2:
    st.page_link("pages/security_copilot.py", label="Security Copilot")
with ic3:
    st.page_link("pages/compliance.py", label="Compliance")
with ic4:
    st.page_link("pages/cloudtrail.py", label="CloudTrail")

# ==========================
# RODAPÉ DA PÁGINA
# ==========================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • VM Creator Module • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")