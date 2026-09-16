document.addEventListener("DOMContentLoaded", () => {
    // Insere a data atual formatada no rodapé
    const now = new Date();
    document.getElementById("report-date").textContent = now.toLocaleDateString("pt-BR");

    // Consome a API do Backend
    fetch("/api/dashboard")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao carregar dados do relatório");
            }
            return response.json();
        })
        .then(data => {
            renderReport(data);
        })
        .catch(error => {
            console.error("Erro:", error);
            document.getElementById("findings-container").innerHTML = `
                <p style="color: var(--color-high);">Erro ao conectar com a API para gerar o relatório.</p>
            `;
        });
});

function renderReport(data) {
    // 1. Preenche Contexto da Conta AWS
    document.getElementById("account-id").textContent = data.account_info?.account_id || "N/A";
    document.getElementById("account-region").textContent = data.account_info?.region || "N/A";
    document.getElementById("account-user").textContent = data.account_info?.user_arn?.split("/").pop() || "N/A";

    // 2. Preenche o Security Score e ajusta a cor
    const scoreElem = document.getElementById("security-score");
    const score = data.security_score || 0;
    scoreElem.textContent = `${score}%`;

    if (score >= 80) {
        scoreElem.style.color = "var(--color-success)";
    } else if (score >= 50) {
        scoreElem.style.color = "var(--color-medium)";
    } else {
        scoreElem.style.color = "var(--color-high)";
    }

    // 3. Contagem de Severidades
    const findings = data.findings || [];
    let criticals = 0, highs = 0, mediums = 0, lows = 0;

    findings.forEach(item => {
        const sev = (item.severity || "").toUpperCase();
        if (sev === "CRITICAL") criticals++;
        else if (sev === "HIGH") highs++;
        else if (sev === "MEDIUM") mediums++;
        else if (sev === "LOW") lows++;
    });

    document.getElementById("count-critical").textContent = criticals;
    document.getElementById("count-high").textContent = highs;
    document.getElementById("count-medium").textContent = mediums;
    document.getElementById("count-low").textContent = lows;

    // 4. Renderiza a Lista de Findings
    const container = document.getElementById("findings-container");
    container.innerHTML = "";

    if (findings.length === 0) {
        container.innerHTML = "<p>Nenhuma vulnerabilidade foi detectada na conta.</p>";
        return;
    }

    findings.forEach(finding => {
        const item = document.createElement("div");
        const severityClass = (finding.severity || "LOW").toUpperCase();
        item.className = `report-finding-item severity-${severityClass}`;

        item.innerHTML = `
            <div class="finding-title-row">
                <h3>${finding.title || "Vulnerabilidade Detectada"}</h3>
                <span class="badge ${severityClass}">${severityClass}</span>
            </div>
            <div class="finding-details">
                <p><strong>Recurso:</strong> ${finding.resource || "N/A"}</p>
                <p>${finding.description || ""}</p>
            </div>
            ${finding.remediation ? `
                <div class="finding-remediation">
                    <strong>🔧 Recomendação de Correção:</strong> ${finding.remediation}
                </div>
            ` : ""}
        `;

        container.appendChild(item);
    });
}