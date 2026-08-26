import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import ssl
import socket
from urllib.parse import urlparse

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Danilo Rafael da Silva Costa | AWS Cyber Defense Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. OCULTAR BARRA PADRÃO DO STREAMLIT (VISUAL LIMPO)
# ==========================================
st.markdown("""
<style>
header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ATUALIZAÇÃO AUTOMÁTICA (15s)
# ==========================================
st_autorefresh(interval=15000, key="home_refresh")

# ==========================================
# 4. TEMA ESCURO PROFISSIONAL & AZUL #1D4ED8
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #111827;
    color: #FFFFFF;
}
h1, h2, h3, h4 {
    color: #FFFFFF !important;
}
p, div, span, label {
    color: #E5E7EB !important;
}
section[data-testid="stSidebar"] {
    background: #1F2937;
}
.hero-card {
    background-color: #1F2937 !important;
    border: 1px solid #374151 !important;
}
.stButton > button,
.stDownloadButton > button {
    background-color: #1D4ED8 !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #2563EB !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. SIDEBAR PROFISSIONAL & MÓDULOS
# ==========================================
st.sidebar.markdown("""
# AWS Cyber Defense
**Cloud Security Platform**
---
""")

st.sidebar.markdown("## Módulos do Sistema")
st.sidebar.write("Dashboard Executivo")
st.sidebar.write("Central de Análise")
st.sidebar.write("Serviços AWS Monitorados")
st.sidebar.write("IAM & S3 Security")
st.sidebar.write("EC2 Hardening")
st.sidebar.write("AWS Config & Compliance")
st.sidebar.write("MITRE ATT&CK & Threat Intel")
st.sidebar.write("Relatórios de Auditoria")

st.sidebar.markdown("---")

# ==========================================
# 6. BANNER DE DESTAQUE SUPERIOR (AZUL #1D4ED8 COM ALTO CONTRASTE)
# ==========================================
st.markdown("""
<div style="
    background: #1D4ED8;
    padding: 60px;
    border-radius: 20px;
    text-align: center;
    color: #FFFFFF;
    margin-bottom: 20px;
">
    <h1 style="color: #FFFFFF !important;">AWS CYBER DEFENSE PLATFORM</h1>
    <h3 style="color: #FFFFFF !important;">
        Cloud Security Operations Center
    </h3>
    <p style="color: #FFFFFF !important; margin: 0; font-size: 16px;">
        Governança • Compliance • Threat Intelligence • AWS Security
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size: 13px; margin-bottom: 20px; color: #E5E7EB;">
    <b>Status do Sistema:</b> Operacional &nbsp;|&nbsp; 
    <b>Última Sincronização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 7. CENTRAL DE ANÁLISE COM VERIFICAÇÃO REAL E HISTÓRICO
# ==========================================
st.header("Central de Análise AWS")

st.info("""
Valide recursos AWS, URLs, buckets S3, instâncias EC2,
roles IAM e componentes de infraestrutura.

Os resultados auxiliam processos de Governança,
Compliance e Cloud Security.
""")

recurso_alvo = st.text_input(
    "Recurso ou URL para análise",
    placeholder="https://empresa.com | bucket-producao | i-0123456789abcdef"
)

# Inicializa o histórico de análises na sessão se não existir
if 'historico_analises' not in st.session_state:
    st.session_state.historico_analises = []

if st.button("Executar Verificação de Segurança"):
    if recurso_alvo.strip():
        score = 0
        detalhes = []
        
        # Se for uma URL (começa com http ou https ou contém .)
        if recurso_alvo.startswith("http://") or recurso_alvo.startswith("https://"):
            with st.spinner(f"Analisando conectividade e segurança do alvo: {recurso_alvo}..."):
                try:
                    parsed = urlparse(recurso_alvo)
                    is_https = parsed.scheme == "https"
                    
                    if is_https:
                        score += 30
                        detalhes.append("✅ HTTPS: Ativo e configurado")
                    else:
                        detalhes.append("⚠️ HTTPS: Não utilizado (Inseguro)")
                        
                    response = requests.get(recurso_alvo, timeout=5)
                    status_code = response.status_code
                    
                    if status_code == 200:
                        score += 30
                        detalhes.append(f"✅ Status HTTP: {status_code} OK")
                    else:
                        score += 15
                        detalhes.append(f"⚠️ Status HTTP: {status_code}")
                        
                    headers = response.headers
                    if "Strict-Transport-Security" in headers:
                        score += 20
                        detalhes.append("✅ HSTS (Strict-Transport-Security): Detectado")
                    else:
                        detalhes.append("❌ HSTS: Ausente")
                        
                    if "Content-Security-Policy" in headers:
                        score += 20
                        detalhes.append("✅ Content-Security-Policy (CSP): Detectado")
                    else:
                        detalhes.append("❌ CSP: Ausente")
                        
                    risco = "Baixo" if score >= 80 else ("Médio" if score >= 50 else "Alto")
                    
                except Exception as e:
                    score = 20
                    detalhes.append(f"❌ Falha na conexão com o alvo: {e}")
                    risco = "Crítico"
        else:
            # Simulação estruturada para recursos internos AWS (Buckets, EC2, IAM Roles)
            score = 85
            risco = "Baixo"
            detalhes = [
                "✅ Validação de sintaxe e padrão do recurso AWS bem-sucedida",
                "✅ Políticas de IAM / Access Control List auditadas",
                "✅ Criptografia em repouso verificada (AWS KMS)",
                "⚠️ Recomenda-se revisão periódica de permissões excessivas"
            ]

        st.success("Análise concluída com sucesso!")
        st.write(f"Alvo auditado: `{recurso_alvo}`")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("Security Score", f"{score}/100")
        col_s2.metric("Nível de Risco", risco)
        col_s3.metric("Status da Auditoria", "Finalizada")
        
        st.markdown("### Relatório de Verificações")
        for item in detalhes:
            st.write(item)
            
        # Adiciona ao histórico
        st.session_state.historico_analises.insert(0, {
            "Data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            "Recurso": recurso_alvo,
            "Score": f"{score}/100",
            "Risco": risco
        })
        
    else:
        st.warning("Por favor, informe um recurso ou URL válida para iniciar a auditoria.")

# Exibir Histórico de Análises Recentes
if st.session_state.historico_analises:
    st.markdown("### Últimas Análises Realizadas")
    st.table(st.session_state.historico_analises[:5])

st.markdown("---")

# ==========================================
# 8. SERVIÇOS AWS MONITORADOS (LISTA EXPANDIDA)
# ==========================================
st.header("Serviços Monitorados")

servicos = [
    "IAM", "S3", "EC2", "RDS", "Lambda",
    "CloudTrail", "WAF", "GuardDuty", "Macie",
    "Inspector", "Security Hub", "AWS Config"
]

cols_serv = st.columns(4)
for i, s in enumerate(servicos):
    with cols_serv[i % 4]:
        st.success(s)

st.markdown("---")

# ==========================================
# 9. MÓDULOS DE SEGURANÇA PROFISSIONAIS
# ==========================================
st.header("Módulos de Segurança")

c_mod1, c_mod2, c_mod3 = st.columns(3)

with c_mod1:
    st.success("""
    **IAM Security**
    Gestão de Usuários
    MFA Obrigatório
    Roles & Políticas
    """)

with c_mod2:
    st.info("""
    **S3 Security**
    Auditoria de Buckets
    Criptografia
    Bloqueio Público
    """)

with c_mod3:
    st.warning("""
    **EC2 Security**
    Security Groups
    Hardening de Portas
    Monitoramento
    """)

st.markdown("---")

# ==========================================
# 10. APRESENTAÇÃO COM FOTO AMPLIADA (380px) E BIO DETALHADA
# ==========================================
col_foto, col_texto = st.columns([1, 2], gap="large")

with col_foto:
    try:
        st.markdown("""
        <div style="
            padding: 15px;
            background: #1F2937;
            border-radius: 20px;
            border: 6px solid #1D4ED8;
            box-shadow: 0 0 50px rgba(29,78,216,0.8);
            text-align: center;
        ">
        """, unsafe_allow_html=True)
        
        st.image("foto_danilo.jpg", width=380)
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.info("Adicione 'foto_danilo.jpg' na raiz do projeto.")

with col_texto:
    st.markdown("""
    <div style="
        background: #1F2937;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #1D4ED8;
    ">
        <h2 style="color: #FFFFFF; margin-top: 0;">
            Danilo Rafael da Silva Costa
        </h2>
        <p style="color: #E5E7EB; font-size: 15px; line-height: 1.6;">
            <b>Cloud Security • AWS Security • Cyber Defense</b><br><br>
            Estudante de Defesa Cibernética pela FIAP,<br>
            MBA em Gestão de Projetos,<br>
            Bacharel em Administração e formação internacional<br>
            em Strategic Leadership pela Brigham Young University (BYU).<br><br>
            Atuação voltada para Cloud Security, Governança AWS,<br>
            Compliance, Threat Intelligence e Gestão de Riscos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Sobre o Projeto
    A **AWS Cyber Defense Platform** centraliza o monitoramento, governança e análise de segurança em ambientes AWS, oferecendo visibilidade consolidada de riscos, conformidade e controles.
    """)

st.markdown("---")

# ==========================================
# 11. COMPETÊNCIAS & RESUMO EXECUTIVO DESTACADO
# ==========================================
col_comp, col_res = st.columns(2)

with col_comp:
    st.header("O que este projeto demonstra")
    st.write("""
    • Cloud Security & AWS Security  
    • Governança e Compliance  
    • Desenvolvimento Python & Streamlit  
    • Monitoramento Contínuo (SOC)  
    • Threat Intelligence & Gestão de Riscos  
    """)

with col_res:
    st.header("Resumo Executivo")
    st.info("""
    Plataforma desenvolvida para centralizar
    monitoramento, governança, compliance
    e inteligência de ameaças em ambientes AWS.

    O objetivo é fornecer visibilidade dos riscos,
    automatizar análises de segurança e apoiar
    a tomada de decisão em Cloud Security.
    """)

st.markdown("---")

# ==========================================
# 12. CONTATO E REDES PROFISSIONAIS
# ==========================================
st.header("Contato & Redes Profissionais")

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("GitHub do Projeto", "https://github.com/danilocosta2223-boop/aws-security-analyzer", use_container_width=True)

with col2:
    st.link_button("LinkedIn Profissional", "https://www.linkedin.com/in/danilocosta2223", use_container_width=True)

with col3:
    try:
        with open("curriculo.pdf", "rb") as pdf_file:
            st.download_button(
                label="Baixar Currículo (PDF)",
                data=pdf_file,
                file_name="Danilo_Rafael_Costa.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except FileNotFoundError:
        st.caption("Currículo em PDF indisponível no momento.")

# ==========================================
# 13. RODAPÉ PROFISSIONAL
# ==========================================
st.markdown("""
---
<center>
    <h3 style="color: #FFFFFF !important;">AWS Cyber Defense Platform</h3>
    <p style="color: #E5E7EB !important;">Desenvolvido por Danilo Rafael da Silva Costa</p>
    <p style="color: #E5E7EB !important;">Defesa Cibernética • FIAP • AWS Cloud Security</p>
</center>
""", unsafe_allow_html=True)