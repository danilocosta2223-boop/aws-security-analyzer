import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="IAM Audit & Governance | AWS Cyber Defense Platform",
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
    <h1>IAM Audit & Governance Center</h1>
    <p style="color: #9CA3AF; margin: 0; font-size: 15px;">
        Auditoria avançada de Identidades, detecção de privilégios excessivos, conformidade com Least Privilege, caminhos de ataque, access analyzer e remediação automatizada.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. DASHBOARD EXECUTIVO, IAM SECURITY SCORE, MATURIDADE & DISTRIBUIÇÃO
# ==========================================
m1, m2, m3, m4 = st.columns(4)
m1.metric("Usuários", "42")
m2.metric("Sem MFA", "3")
m3.metric("Admins", "8")
m4.metric("Risco IAM", "High")

st.subheader("IAM Security Score")
score = 82
st.progress(score / 100)
st.success(f"Score IAM: {score}%")

st.subheader("IAM Maturity")
st.progress(0.87)
st.success("Maturidade IAM: Avançada")

st.subheader("Distribuição de Identidades")
id1, id2, id3 = st.columns(3)
id1.metric("Users", 42)
id2.metric("Roles", 15)
id3.metric("Groups", 8)

st.markdown("---")

# ==========================================
# 5. ALERTAS CRÍTICOS & RISK MATRIX
# ==========================================
st.subheader("Alertas Críticos")
st.error("3 usuários sem MFA")
st.warning("2 chaves com mais de 90 dias")
st.warning("1 usuário com AdministratorAccess")

st.subheader("Risk Matrix")
risk = pd.DataFrame({
    "Achado": ["Sem MFA", "Admin Excessivo", "Key Antiga"],
    "Impacto": ["Crítico", "Alto", "Médio"]
})
st.dataframe(risk, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 6. INVENTÁRIO IAM, CHAVES, ROLES & INATIVOS
# ==========================================
col_i1, col_i2 = st.columns(2)

with col_i1:
    st.subheader("Inventário de Usuários")
    usuarios = pd.DataFrame({
        "Usuário": ["admin", "auditor", "analista"],
        "MFA": ["Não", "Sim", "Sim"],
        "Último Login": ["1 dia", "5 dias", "Hoje"]
    })
    st.dataframe(usuarios, use_container_width=True, hide_index=True)

with col_i2:
    st.subheader("Chaves de Acesso")
    access_keys = pd.DataFrame({
        "Usuário": ["admin", "backup-user"],
        "Idade": ["120 dias", "15 dias"],
        "Status": ["Rotacionar", "OK"]
    })
    st.dataframe(access_keys, use_container_width=True, hide_index=True)

col_i3, col_i4 = st.columns(2)

with col_i3:
    st.subheader("IAM Roles")
    roles = pd.DataFrame({
        "Role": ["EC2-Role", "Lambda-Role", "Admin-Role"],
        "Risco": ["Baixo", "Médio", "Alto"]
    })
    st.dataframe(roles, use_container_width=True, hide_index=True)

with col_i4:
    st.subheader("Usuários Inativos")
    inactive = pd.DataFrame({
        "Usuário": ["backup-user", "old-admin"],
        "Dias": [95, 180]
    })
    st.dataframe(inactive, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 7. DASHBOARD DE PRIVILÉGIOS, ACCESS ANALYZER & ROTAÇÃO DE CHAVES
# ==========================================
st.subheader("Privilégios")
p1, p2, p3 = st.columns(3)
p1.metric("Admins", 8)
p2.metric("Power Users", 12)
p3.metric("Read Only", 22)

st.subheader("Access Analyzer")
st.warning("""
2 permissões excessivas detectadas

1 política com '*'

1 trust policy exposta
""")

st.subheader("Key Rotation Status")
rotation = pd.DataFrame({
    "Faixa": ["0-30", "31-60", "61-90", "90+"],
    "Quantidade": [15, 8, 4, 2]
})
st.dataframe(rotation, use_container_width=True, hide_index=True)

st.markdown("---")

# ==========================================
# 8. COMPLIANCE IAM & COMPLIANCE FRAMEWORKS
# ==========================================
st.subheader("Compliance IAM")
c1, c2, c3 = st.columns(3)
c1.metric("MFA", "92%")
c2.metric("Least Privilege", "88%")
c3.metric("Key Rotation", "80%")

st.subheader("IAM Compliance")
f1, f2, f3 = st.columns(3)
f1.metric("NIST", "92%")
f2.metric("CIS", "89%")
f3.metric("ISO 27001", "90%")

st.markdown("---")

# ==========================================
# 9. IAM ATTACK PATH, FORENSE IAM, RISK TREND & COVERAGE
# ==========================================
col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader("Attack Path IAM")
    st.warning("""
    Usuário sem MFA
    ↓
    Comprometimento de Credencial
    ↓
    Privilégio Administrativo
    ↓
    Acesso EC2
    ↓
    Bucket S3
    """)

with col_t2:
    st.subheader("Timeline IAM")
    timeline = pd.DataFrame({
        "Hora": ["14:01", "14:05", "14:10"],
        "Evento": ["Login", "CreateUser", "AttachPolicy"]
    })
    st.dataframe(timeline, use_container_width=True, hide_index=True)

st.subheader("Eventos Suspeitos")
forense = pd.DataFrame({
    "Hora": ["14:01", "14:05", "14:08"],
    "Evento": ["ConsoleLogin", "CreateAccessKey", "AttachAdministratorAccess"],
    "Severidade": ["Baixa", "Alta", "Crítica"]
})
st.dataframe(forense, use_container_width=True, hide_index=True)

st.subheader("IAM Risk Trend")
risk_trend = pd.DataFrame({
    "Score": [95, 92, 88, 85, 82]
})
st.line_chart(risk_trend)

st.subheader("IAM Coverage")
st.progress(0.94)
st.success("94% das identidades auditadas")

st.markdown("---")

# ==========================================
# 10. IAM EXECUTIVE SUMMARY
# ==========================================
st.subheader("IAM Executive Summary")
st.success("""
Status Geral: Requer Atenção

Score IAM: 82%

Usuários sem MFA: 3

Chaves para rotação: 2

Privilégios excessivos: 2

Maturidade IAM: Avançada

Recomendação:
Executar plano de remediação para MFA, revisar AdministratorAccess e rotacionar as Access Keys antigas.
""")

st.markdown("---")

# ==========================================
# 11. REMEDIAÇÃO AUTOMATIZADA
# ==========================================
st.subheader("Remediação")

r1, r2, r3 = st.columns(3)
with r1:
    if st.button("Habilitar MFA"):
        st.success("Plano de remediação gerado com sucesso.")
with r2:
    if st.button("Rotacionar Chaves"):
        st.success("Plano de rotação de chaves criado.")
with r3:
    if st.button("Revisar Permissões"):
        st.success("Análise detalhada de privilégios iniciada.")

st.markdown("---")

# ==========================================
# 12. CENTRO EDUCACIONAL (EXPANDERS)
# ==========================================
st.subheader("Centro Educacional")

with st.expander("O que é MFA?"):
    st.write("A Autenticação Multifator (MFA) adiciona uma camada extra de proteção aos logins do IAM, exigindo um fator de autenticação adicional além de senha e usuário.")

with st.expander("O que é Least Privilege?"):
    st.write("O princípio do Menor Privilégio garante que identidades tenham apenas as permissões estritamente necessárias para realizar suas tarefas operacionais.")

with st.expander("O que é Access Key?"):
    st.write("Chaves de acesso (Access Keys ID e Secret) são credenciais de longo prazo usadas para assinar solicitações programáticas à API da AWS.")

with st.expander("O que é IAM Role?"):
    st.write("Uma IAM Role é uma identidade AWS com permissões específicas que pode ser assumida temporariamente por usuários, aplicações ou serviços autorizados.")

st.markdown("---")

# ==========================================
# 13. IAM COPILOT & INTEGRAÇÃO CLOUDTRAIL
# ==========================================
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("IAM Copilot")
    pergunta = st.text_area("Pergunte sobre IAM, Políticas ou Governança de Identidade")

    if st.button("Analisar IAM"):
        p = pergunta.lower()
        if "mfa" in p:
            st.info("Ative MFA para todos os usuários com acesso ao console e políticas restritivas para chaves.")
        elif "admin" in p:
            st.info("Revise permissões AdministratorAccess. Aplique escopos granulares e conditions em políticas customizadas.")
        elif "key" in p:
            st.info("Rotacione Access Keys periodicamente a cada 90 dias e utilize roles sempre que possível para evitar chaves de longa duração.")
        elif "least privilege" in p:
            st.info("Inspecione políticas em busca de ações curinga (*) e utilize o IAM Access Analyzer para validar exposição.")
        else:
            st.info("Análise IAM concluída com sucesso com base nas melhores práticas do AWS Well-Architected Framework.")

with col_c2:
    st.subheader("Integração CloudTrail")
    st.success("""
    Eventos IAM correlacionados:
    ✓ Login
    ✓ CreateUser
    ✓ CreateAccessKey
    ✓ AttachPolicy
    ✓ AssumeRole
    """)

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
    st.page_link("pages/pdf_reports.py", label="PDF Reports")
with c_link6:
    st.page_link("pages/cloudwatch.py", label="CloudWatch")

# ==========================================
# 15. RODAPÉ
# ==========================================
st.markdown("---")
st.caption(f"AWS Cyber Defense Platform • IAM Audit & Governance Center • Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")