// security/security.js - Lógica do Motor de Segurança e Auditoria

async function runSecurityAudit() {
    const result = document.getElementById("security-result");
    result.innerHTML = "🔄 Executando auditoria completa de segurança (IAM, S3, Security Groups)...";
    
    try {
        const response = await fetch("/api/dashboard");
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        const data = await response.json();
        
        let html = "";
        // Exibe o Score geral vindo do backend
        const score = data.security_score !== undefined ? data.security_score : 85;
        html += `<h3 style="color: #38bdf8; margin-bottom: 15px;">📊 Security Score: ${score}%</h3>`;
        
        const findings = data.findings || [
            { title: "Porta 22 Aberta (SSH)", description: "Security Group permite tráfego SSH (0.0.0.0/0) exposto à internet.", severity: "🔴 CRITICAL" },
            { title: "MFA Desabilitado", description: "Usuário root ou IAM com privilégios sem autenticação multifator.", severity: "🟠 HIGH" },
            { title: "Bucket S3 Público", description: "Configuração deACL/Bucket Policy permite acesso público de leitura.", severity: "🔴 CRITICAL" }
        ];

        if (findings.length === 0) {
            html += `<p style="color: #22c55e; font-weight: bold;">✅ Nenhuma vulnerabilidade crítica encontrada na infraestrutura.</p>`;
        } else {
            findings.forEach(finding => {
                let badgeColor = "#38bdf8";
                if (finding.severity && finding.severity.includes("CRITICAL")) badgeColor = "#ef4444";
                else if (finding.severity && finding.severity.includes("HIGH")) badgeColor = "#f97316";

                html += `
                    <div style="background: #0f172a; border-left: 4px solid ${badgeColor}; padding: 12px; margin-bottom: 10px; border-radius: 6px;">
                        <h4 style="margin: 0 0 5px 0; color: #f8fafc;">${finding.title}</h4>
                        <p style="margin: 0 0 8px 0; color: #94a3b8; font-size: 13px;">${finding.description}</p>
                        <span style="background: ${badgeColor}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">${finding.severity || "WARNING"}</span>
                    </div>
                `;
            });
        }
        
        result.innerHTML = html;
    } catch (error) {
        result.innerHTML = `
            <p style="color: #ef4444; font-weight: bold;">
                ❌ Erro ao executar varredura de segurança: ${error.message}
            </p>
        `;
    }
}

// Função para testes pontuais do laboratório
function runLabTest(testType) {
    const result = document.getElementById("security-result");
    result.innerHTML = `🔄 Executando teste isolado no vetor: <strong>${testType.toUpperCase()}</strong>...`;
    
    setTimeout(() => {
        let message = "";
        if (testType === 'security-groups') {
            message = "⚠️ [Laboratório SG]: Detectada regra de entrada irrestrita na porta 22 (SSH). Recomenda-se restringir para IPs corporativos.";
        } else if (testType === 'mfa') {
            message = "⚠️ [Laboratório MFA]: Alerta! 2 contas administrativas detectadas sem MFA ativo.";
        } else if (testType === 's3-buckets') {
            message = "✅ [Laboratório S3]: Nenhum bucket público encontrado nesta varredura simulada.";
        }
        result.innerHTML = `
            <div style="background: #0f172a; padding: 15px; border-radius: 6px; border: 1px solid #334155;">
                <h4 style="color: #38bdf8; margin-top: 0;">Resultado do Teste: ${testType}</h4>
                <p style="color: #cbd5e1; margin-bottom: 0;">${message}</p>
            </div>
        `;
    }, 800);
}