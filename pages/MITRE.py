import streamlit as st
import pandas as pd

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="MITRE ATT&CK Center",
    page_icon="🎯",
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

.tech-card {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 4px solid #ef4444;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# CABEÇALHO
# ==========================
st.markdown("""
<div class="hero-card">
    <h1>🎯 MITRE ATT&CK Cloud Matrix</h1>
    <p style="color:#94a3b8; margin: 0; font-size: 15px;">
        Correlação de ameaças e vulnerabilidades AWS com técnicas e táticas da matriz MITRE ATT&CK for Cloud.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================
# MÉTRICAS
# ==========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Técnicas Mapeadas", "8")

with c2:
    st.metric("Critical Risks", "1")

with c3:
    st.metric("High Risks", "2")

with c4:
    st.metric("MITRE Coverage", "87%")

# ==========================
# SCORE
# ==========================
st.markdown("---")
st.subheader("📊 ATT&CK Coverage Score")

score = 87
st.progress(score / 100)
st.metric("Cobertura MITRE", f"{score}%")

# ==========================
# EXECUTIVE SUMMARY
# ==========================
st.markdown("---")
st.subheader("📋 Executive Summary")

st.info("""
O ambiente possui cobertura para as principais táticas de ataque em nuvem alinhadas ao framework MITRE ATT&CK.

Foram identificadas técnicas ativas ou expostas relacionadas a:
• **Initial Access** (T1078 - Valid Accounts)
• **Credential Access** (T1110 - Brute Force)
• **Persistence** (T1098 - Account Manipulation)
• **Discovery** (T1087 - Account Discovery)
• **Data from Cloud Storage Object** (T1530)

Recomenda-se ampliar os controles de detecção para as táticas de *Privilege Escalation* e *Defense Evasion*.
""")

# ==========================
# MATRIZ MITRE
# ==========================
st.markdown("---")
st.subheader("🎯 MITRE ATT&CK Mapping")

mitre_df = pd.DataFrame({
    "ID": [
        "T1078",
        "T1110",
        "T1098",
        "T1087",
        "T1530",
        "T1562",
        "T1498",
        "T1531"
    ],
    "Técnica": [
        "Valid Accounts",
        "Brute Force",
        "Account Manipulation",
        "Account Discovery",
        "Data from Cloud Storage Object",
        "Impair Defenses",
        "Network Denial of Service",
        "Access Account Removal"
    ],
    "Tática": [
        "Initial Access",
        "Credential Access",
        "Persistence",
        "Discovery",
        "Collection",
        "Defense Evasion",
        "Impact",
        "Impact"
    ],
    "Severidade": [
        "Alto",
        "Médio",
        "Alto",
        "Baixo",
        "Crítico ⚠️",
        "Médio",
        "Baixo",
        "Médio"
    ],
    "Status de Detecção": [
        "Monitorado",
        "Alerta Ativo",
        "Monitorado",
        "Monitorado",
        "Alerta Ativo",
        "Parcial",
        "Monitorado",
        "Monitorado"
    ]
})

st.dataframe(
    mitre_df,
    use_container_width=True
)

# ==========================
# ALERTAS
# ==========================
st.markdown("---")
st.subheader("🚨 Alertas de Simulação e Ameaças")

st.error("""
**Técnica:** `T1530` - Data from Cloud Storage Object  
**Problema:** Buckets S3 com políticas permissivas permitiram consultas não autorizadas correlacionadas com varreduras externas.  
**Mitigação:** Aplicar Block Public Access globalmente e restringir políticas baseadas em recursos.
""")

st.warning("""
**Técnica:** `T1110` - Brute Force / Tentativas de Acesso  
**Problema:** Múltiplas tentativas de login com falha detectadas na console AWS (IAM) originadas de IPs suspeitos.  
**Mitigação:** Exigir MFA obrigatório para todos os perfis e habilitar AWS GuardDuty.
""")

# ==========================
# CHECKLIST
# ==========================
st.markdown("---")
st.subheader("✅ Checklist de Defesa MITRE ATT&CK")

st.checkbox("GuardDuty ativado para detecção comportamental baseada em MITRE", value=True, disabled=True)
st.checkbox("Políticas SCP (Service Control Policies) ativas no AWS Organizations", value=True, disabled=True)
st.checkbox("MFA corporativo imposto para acessos administrativos", value=False, disabled=True)
st.checkbox("Simulação periódica de ataques (Purple Teaming) integrada", value=True, disabled=True)

# ==========================
# DISTRIBUIÇÃO DE TÁTICAS (GRÁFICO)
# ==========================
st.markdown("---")
st.subheader("📈 Distribuição de Riscos por Tática")

tactic_risk_df = pd.DataFrame({
    "Tática": [
        "Initial Access",
        "Credential Access",
        "Persistence",
        "Discovery",
        "Collection",
        "Impact"
    ],
    "Quantidade": [
        1,
        1,
        1,
        1,
        1,
        2
    ]
})

st.bar_chart(
    tactic_risk_df.set_index("Tática")
)

# ==========================
# RODAPÉ
# ==========================
st.markdown("---")
st.caption("AWS Cyber Defense Platform • MITRE ATT&CK Center")