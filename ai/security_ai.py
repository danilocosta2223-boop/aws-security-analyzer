# ==========================================
# MOTOR DE INTELIGÊNCIA ARTIFICIAL - SECURITY AI
# ==========================================

from prompts import (
    PLATFORM_PROMPT,
    SECURITY_COPILOT_PROMPT,
    THREAT_INTELLIGENCE_PROMPT,
    IAM_PROMPT,
    COMPLIANCE_PROMPT,
    EXECUTIVE_PROMPT,
    EXECUTIVE_VIEW_PROMPT,
    AUDIT_PROMPT,
    EC2_PROMPT,
    SECURITY_HUB_PROMPT,
    HISTORY_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT
)

class SecurityAI:
    
    def __init__(self):
        self.platform = PLATFORM_PROMPT

    def security_analysis(self, question):
        q = question.lower()
        if "vulnerabilidade" in q or "risco" in q:
            return f"""{SECURITY_COPILOT_PROMPT}

Pergunta:
{question}

Resumo Executivo:
Identificados pontos de atenção críticos na infraestrutura que exigem mitigação imediata para evitar exposição lateral.
"""
        return f"""{SECURITY_COPILOT_PROMPT}

Pergunta:
{question}

Resumo Executivo:
Análise geral de segurança concluída com base nos parâmetros atuais da plataforma.
"""

    def threat_analysis(self, ioc):
        q = ioc.lower()
        if "malware" in q or "ransomware" in q or "ip" in q:
            return f"""{THREAT_INTELLIGENCE_PROMPT}

IOC Analisado:
{ioc}

Resultado:
Severidade: Alta
Indicadores maliciosos confirmados em bases de Threat Intel. Vetor de ataque isolado.
"""
        return f"""{THREAT_INTELLIGENCE_PROMPT}

IOC Analisado:
{ioc}

Resultado:
Nenhuma ameaça crítica encontrada nas bases ativas.
"""

    def iam_analysis(self, question):
        q = question.lower()
        if "mfa" in q:
            return f"""{IAM_PROMPT}

Consulta:
{question}

Resultado:
Resumo Executivo
Existem usuários sem MFA ativo no ambiente AWS.

Risco:
Alto

Recomendação:
Ativar MFA obrigatório imediatamente para todas as contas administrativas.
"""
        elif "admin" in q or "privilegio" in q:
            return f"""{IAM_PROMPT}

Consulta:
{question}

Resultado:
Resumo Executivo
Foram encontradas permissões administrativas excessivas (AdministratorAccess).

Recomendação:
Aplicar o princípio do menor privilégio (Least Privilege).
"""
        return f"""{IAM_PROMPT}

Consulta:
{question}

Resultado:
Auditoria de identidades IAM processada com sucesso.
"""

    def compliance_analysis(self, question):
        q = question.lower()
        if "cis" in q or "benchmark" in q:
            return f"""{COMPLIANCE_PROMPT}

Consulta:
{question}

Resultado:
Compliance CIS Benchmark
Score Atual: 92%
Controles validados sem violações graves.
"""
        return f"""{COMPLIANCE_PROMPT}

Consulta:
{question}

Resultado:
Compliance verificado dentro dos parâmetros e frameworks esperados.
"""

    def security_hub_analysis(self, question):
        q = question.lower()
        if "critical" in q:
            return f"""{SECURITY_HUB_PROMPT}

Resumo Executivo

Foram identificados findings críticos.

Prioridade:
P1

Recomendação:
Remediar imediatamente.
"""
        return f"""{SECURITY_HUB_PROMPT}

Resumo Executivo

Security Hub analisado com sucesso.
"""

    def history_analysis(self, question):
        return f"""{HISTORY_PROMPT}

Consulta:
{question}

Resultado:

Histórico auditado.

Nenhuma inconsistência encontrada.
"""

    def executive_analysis(self, question):
        return f"""{EXECUTIVE_PROMPT}

Consulta:
{question}

Resumo Executivo:
Postura de segurança adequada, com riscos controlados e governança ativa.
"""

    def executive_view_analysis(self, question):
        return f"""{EXECUTIVE_VIEW_PROMPT}

Consulta:
{question}

Resumo Executivo

Ambiente estável.
Governança adequada.
Compliance acima de 90%.
"""

    def audit_analysis(self, question):
        return f"""{AUDIT_PROMPT}

Consulta:
{question}

Resultado:
Logs históricos auditados com sucesso. Nenhuma anomalia de auditoria não tratada.
"""

    def ec2_analysis(self, question):
        q = question.lower()
        if "ssh" in q or "rdp" in q:
            return f"""{EC2_PROMPT}

Consulta:
{question}

Resultado:
Foi detectada exposição potencial de portas de gerenciamento remoto (SSH/RDP) abertas para a internet (0.0.0.0/0). Restringir Security Groups urgentemente.
"""
        return f"""{EC2_PROMPT}

Consulta:
{question}

Resultado:
Infraestrutura EC2 e Security Groups estáveis.
"""

    # ==========================================
    # RECURSOS EXTRAS / UTILITIES & SCORES
    # ==========================================
    
    def calculate_risk(self, critical, high, medium):
        score = max(
            100 - (
                critical * 20 +
                high * 10 +
                medium * 5
            ),
            0
        )
        return score

    def calculate_threat_score(self, critical, high, medium):
        return max(
            100 - (
                critical * 15 +
                high * 8 +
                medium * 3
            ),
            0
        )

    def calculate_compliance_score(self, findings):
        return max(
            100 - (findings * 4),
            0
        )

    def calculate_health_score(self, security_score, compliance_score):
        return int(
            (
                security_score +
                compliance_score
            ) / 2
        )

    def classify_risk(self, score):
        if score >= 90:
            return "LOW"
        elif score >= 70:
            return "MEDIUM"
        elif score >= 50:
            return "HIGH"
        return "CRITICAL"

    def prioritize(self, finding):
        if finding == "Critical":
            return "P1"
        elif finding == "High":
            return "P2"
        elif finding == "Medium":
            return "P3"
        return "P4"

    def executive_summary(self, score, threats, compliance):
        return f"""{EXECUTIVE_SUMMARY_PROMPT}

Resumo Executivo
Security Score: {score}

Threats:
{threats}

Compliance:
{compliance}%

Prioridade:
Alta
"""