/**
 * AWS Security Analyzer - Dashboard Core Script
 * Desenvolvido por Danilo Rafael da Silva Costa
 */

// Configurações Globais
const API_URL = "http://127.0.0.1:5000/api/dashboard";
const REFRESH_INTERVAL = 60000; // 60 segundos

// Trava para evitar requisições simultâneas
let isLoading = false;

document.addEventListener("DOMContentLoaded", () => {
  initDashboard();
});

function initDashboard() {
  const refreshBtn = document.getElementById("refresh-btn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", loadDashboardData);
  }

  // Carga inicial dos dados
  loadDashboardData();

  // Auto-refresh automático
  setInterval(loadDashboardData, REFRESH_INTERVAL);
}

/**
 * Função principal para buscar dados da API Flask
 */
function loadDashboardData() {
  if (isLoading) return;
  isLoading = true;

  setLoadingState();

  fetch(API_URL)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.status} ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      updateLastTimestamp();
      renderScoreAndStatus(data.security_score ?? 0);

      const findings = data.findings ?? [];
      renderSeverityAndSummary(data.security_score ?? 0, findings, data);
      renderAccountContext(data);
      renderResources(data);
      renderFindings(findings);
    })
    .catch(error => {
      console.error("Falha ao carregar dados do dashboard AWS:", error);
      setErrorState();
    })
    .finally(() => {
      isLoading = false;
    });
}

/**
 * Helper para padronizar o texto de severidade em CAIXA ALTA
 */
function formatSeverity(severity) {
  if (!severity) return "LOW";
  return severity.toUpperCase();
}

/**
 * Atualiza o indicador visual da última atualização
 */
function updateLastTimestamp() {
  const lastUpdateEl = document.getElementById("last-update");
  if (lastUpdateEl) {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString("pt-BR", { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    lastUpdateEl.innerText = `Última atualização: ${formattedTime}`;
  }
}

/**
 * Define estado de carregamento visual
 */
function setLoadingState() {
  document.getElementById("score").innerHTML = `<span class="loading-spinner"></span>`;
  document.getElementById("security-status").innerText = "Status: Atualizando...";
  document.getElementById("executive-summary").innerHTML = `<p class="loading-text">Analisando dados da AWS...</p>`;
  document.getElementById("findings").innerHTML = `<p class="loading-text">Carregando achados de segurança...</p>`;
}

/**
 * Define o estado de erro caso a API Flask falhe
 */
function setErrorState() {
  document.getElementById("score").innerHTML = `<span class="error-score">--</span>`;
  document.getElementById("security-status").innerText = "Status: Indisponível";
  document.getElementById("executive-summary").innerHTML = `
    <p class="error-text">
      <i class="fa-solid fa-triangle-exclamation"></i>
      Não foi possível conectar ao backend da API (${API_URL}).
    </p>
  `;
  document.getElementById("findings").innerHTML = `
    <div class="empty-state-error">
      <p>Erro ao carregar os achados. Verifique se o serviço Flask está ativo.</p>
    </div>
  `;
}

/**
 * Renderiza o Score de Segurança e a Badge de Status Geral
 */
function renderScoreAndStatus(score) {
  const scoreContainer = document.getElementById("score");
  const statusBadge = document.getElementById("security-status");

  let colorClass = "score-low";
  let statusText = "🚨 Crítico";

  if (score >= 80) {
    colorClass = "score-high";
    statusText = "✅ Excelente";
  } else if (score >= 60) {
    colorClass = "score-medium";
    statusText = "⚠️ Atenção";
  } else if (score >= 40) {
    colorClass = "score-warning";
    statusText = "⚡ Risco Moderado";
  }

  scoreContainer.innerHTML = `
    <div class="score-circle ${colorClass}">
      <h2>${score}%</h2>
    </div>
  `;

  if (statusBadge) {
    statusBadge.innerText = `Status: ${statusText}`;
    statusBadge.className = `security-status-badge status-${colorClass}`;
  }
}

/**
 * Calcula distribuição de severidades e gera o texto do Resumo Executivo
 */
function renderSeverityAndSummary(score, findings, data) {
  const counts = { critical: 0, high: 0, medium: 0, low: 0 };

  findings.forEach(finding => {
    const sev = (finding.severity || "").toLowerCase();
    if (sev.includes("critical") || sev.includes("crítico")) counts.critical++;
    else if (sev.includes("high") || sev.includes("alto")) counts.high++;
    else if (sev.includes("medium") || sev.includes("médio")) counts.medium++;
    else counts.low++;
  });

  const totalRisk = counts.critical + counts.high + counts.medium + counts.low;
  const totalResources = (data.iam_users ?? 0) + (data.s3_buckets ?? 0) + (data.ec2_instances ?? 0);

  // Atualizar Pills de Severidade
  document.getElementById("sev-critical-count").innerText = counts.critical;
  document.getElementById("sev-high-count").innerText = counts.high;
  document.getElementById("sev-medium-count").innerText = counts.medium;
  document.getElementById("sev-low-count").innerText = counts.low;

  // Gerar Resumo Executivo Dinâmico
  const summaryContainer = document.getElementById("executive-summary");
  if (summaryContainer) {
    let summaryHtml = "";
    if (findings.length === 0) {
      summaryHtml = `
        <p class="summary-good">
          <i class="fa-solid fa-circle-check"></i> Nenhum problema de segurança foi identificado na infraestrutura.
        </p>
        <p class="summary-info"><i class="fa-solid fa-cubes"></i> Total de Recursos AWS Analisados: <strong>${totalResources}</strong></p>
      `;
    } else {
      summaryHtml = `
        <ul class="summary-list">
          <li>Compliance estimado: <strong>${score}%</strong></li>
          <li>Total de Recursos AWS: <strong>${totalResources}</strong></li>
          <li>Total de Achados (Risco): <strong>${totalRisk}</strong></li>
          ${counts.critical > 0 ? `<li class="text-critical"><i class="fa-solid fa-triangle-exclamation"></i> <strong>${counts.critical}</strong> problema(s) crítico(s) exigem ação imediata.</li>` : ''}
          ${counts.high > 0 ? `<li class="text-high"><i class="fa-solid fa-circle-exclamation"></i> <strong>${counts.high}</strong> vulnerabilidade(s) de alta severidade detectada(s).</li>` : ''}
        </ul>
      `;
    }
    summaryContainer.innerHTML = summaryHtml;
  }
}

/**
 * Renderiza informações contextuais da conta AWS
 */
function renderAccountContext(data) {
  const accIdEl = document.getElementById("acc-id");
  const accRegionEl = document.getElementById("acc-region");
  const accUserEl = document.getElementById("acc-user");

  if (accIdEl) accIdEl.innerText = data.account_id ?? "--";
  if (accRegionEl) accRegionEl.innerText = data.region ?? "us-east-1";
  if (accUserEl) accUserEl.innerText = data.iam_user ?? "--";
}

/**
 * Renderiza a contagem dos cartões de Recursos
 */
function renderResources(data) {
  document.getElementById("iam-users-count").innerText = data.iam_users ?? 0;
  document.getElementById("s3-buckets-count").innerText = data.s3_buckets ?? 0;
  document.getElementById("ec2-instances-count").innerText = data.ec2_instances ?? 0;
}

/**
 * Renderiza a lista detalhada de Achados (Findings)
 */
function renderFindings(findings) {
  const findingsContainer = document.getElementById("findings");
  const findingsCountBadge = document.getElementById("findings-count");

  if (findingsCountBadge) {
    findingsCountBadge.innerText = `${findings.length} ${findings.length === 1 ? 'achado' : 'achados'}`;
  }

  if (findings.length === 0) {
    findingsContainer.innerHTML = `
      <div class="empty-state">
        <i class="fa-solid fa-shield-cat"></i>
        <p>Nenhum achado de segurança. Sua conta está em conformidade!</p>
      </div>
    `;
    return;
  }

  let findingsHtml = "";
  findings.forEach(finding => {
    const severityClass = getSeverityClass(finding.severity);
    const formattedSev = formatSeverity(finding.severity);

    findingsHtml += `
      <div class="finding-item ${severityClass}">
        <span class="badge ${severityClass}">${formattedSev}</span>
        <div class="finding-content">
          <h4>${finding.title}</h4>
          <p class="finding-severity-text">Severidade: <strong>${formattedSev}</strong></p>
          ${finding.resource ? `<p class="resource-affected"><i class="fa-solid fa-cube"></i> ${finding.resource}</p>` : ''}
        </div>
      </div>
    `;
  });

  findingsContainer.innerHTML = findingsHtml;
}

/**
 * Helper para padronizar classes CSS baseadas em severidade
 */
function getSeverityClass(severity) {
  if (!severity) return "severity-low";
  const sev = severity.toLowerCase();
  if (sev.includes("critical") || sev.includes("crítico")) return "severity-critical";
  if (sev.includes("high") || sev.includes("alto")) return "severity-high";
  if (sev.includes("medium") || sev.includes("médio")) return "severity-medium";
  return "severity-low";
}