#!/usr/env python3
import json
import logging
from datetime import datetime

# Importações dos módulos de checagem AWS
from guardduty_check import check_guardduty_threats
from securityhub_check import check_security_hub_findings
from cloudtrail_check import check_cloudtrail_status

# Configuração básica de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def aggregate_all_security_data(region="us-east-1"):
    findings = []
    sh_summary = {}
    
    logger.info(f"Iniciando coleta de dados de segurança na região: {region}")
    
    try:
        logger.info("Coletando alertas do GuardDuty...")
        findings.extend(check_guardduty_threats(region))
    except Exception as e:
        logger.error(f"Erro ao executar check_guardduty_threats: {e}")

    try:
        logger.info("Coletando findings e sumário do Security Hub...")
        sh_findings, sh_summary = check_security_hub_findings(region)
        findings.extend(sh_findings)
    except Exception as e:
        logger.error(f"Erro ao executar check_security_hub_findings: {e}")

    try:
        logger.info("Verificando status do CloudTrail...")
        findings.extend(check_cloudtrail_status(region))
    except Exception as e:
        logger.error(f"Erro ao executar check_cloudtrail_status: {e}")
    
    return findings, sh_summary

def generate_security_report(region="us-east-1", output_file="security_report.json"):
    """
    Função principal que agrega os dados e exporta um relatório consolidado.
    """
    findings, sh_summary = aggregate_all_security_data(region)
    
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "region": region,
        "total_findings": len(findings),
        "security_hub_summary": sh_summary,
        "findings": findings
    }
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        logger.info(f"Relatório gerado com sucesso em: {output_file}")
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo de relatório: {e}")
        
    return report

if __name__ == "__main__":
    generate_security_report(region="us-east-1")