import argparse
import concurrent.futures
import json
import logging
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

import boto3
import pandas as pd
from botocore.exceptions import BotoCoreError, ClientError

from enums import Severity
from s3_check import check_s3_buckets
from iam_check import check_iam_users
from ec2_check import check_security_groups
from report import generate_pdf_report, generate_html_dashboard

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AWS Security Analyzer - Ferramenta de Auditoria")
    parser.add_argument("--profile", type=str, default=None, help="Perfil da AWS CLI")
    parser.add_argument("--region", type=str, default="us-east-1", help="Região padrão da AWS")
    parser.add_argument("--all-regions", action="store_true", help="Varre todas as regiões habilitadas da AWS")
    return parser.parse_args()

def validate_aws_session(profile: str, region: str) -> boto3.Session:
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        logging.info(f"Sessão ativa. Conta: {identity['Account']} | IAM: {identity['Arn'].split('/')[-1]}")
        return session
    except (ClientError, BotoCoreError) as e:
        logging.error(f"Erro de autenticação AWS: {e}")
        sys.exit(1)

def get_target_regions(session: boto3.Session, all_regions: bool, default_region: str) -> List[str]:
    """Retorna a lista de regiões a serem auditadas."""
    if not all_regions:
        return [default_region]
    
    try:
        ec2 = session.client('ec2')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        logging.info(f"Modo multi-região ativado. Regiões encontradas: {len(regions)}")
        return regions
    except Exception as e:
        logging.warning(f"Não foi possível listar regiões automaticamente ({e}). Usando padrão: {default_region}")
        return [default_region]

def calculate_score(findings: List[Dict[str, Any]]) -> int:
    score = 100
    # Mapeamento dinâmico utilizando diretamente os pesos do Enum
    weights = {
        "CRITICAL": Severity.CRITICAL.value,
        "HIGH": Severity.HIGH.value,
        "MEDIUM": Severity.MEDIUM.value,
        "LOW": Severity.LOW.value
    }
    
    for finding in findings:
        severity = finding.get("severity", "LOW")
        score -= weights.get(severity, 2)
            
    return max(score, 0)

def print_executive_summary(findings: List[Dict[str, Any]], score: int) -> None:
    """Exibe um resumo executivo formatado no terminal por severidade e serviço."""
    summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    service_summary: Dict[str, Dict[str, int]] = {}
    
    for finding in findings:
        sev = finding.get("severity", "LOW").upper()
        srv = finding.get("service", "UNKNOWN").upper()
        
        if sev in summary:
            summary[sev] += 1
            
        if srv not in service_summary:
            service_summary[srv] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        if sev in service_summary[srv]:
            service_summary[srv][sev] += 1

    print("\n" + "="*45)
    print("           RESUMO EXECUTIVO - AWS SECURITY")
    print("="*45)
    print(f"🎯 Score Geral de Segurança: {score}/100")
    print("-" * 45)
    print(f"🚨 Críticos : {summary['CRITICAL']}")
    print(f"⚠️  Altos    : {summary['HIGH']}")
    print(f"⚡ Médios   : {summary['MEDIUM']}")
    print(f"ℹ️  Baixos   : {summary['LOW']}")
    print(f"📊 Total    : {len(findings)} achados")
    print("-" * 45)
    
    if service_summary:
        print("📌 Breakdown por Serviço:")
        for srv, counts in service_summary.items():
            total_srv = sum(counts.values())
            print(f"   • {srv} (Total: {total_srv}) -> C: {counts['CRITICAL']} | H: {counts['HIGH']} | M: {counts['MEDIUM']} | L: {counts['LOW']}")
            
    print("="*45 + "\n")

def main() -> None:
    args = parse_arguments()
    session = validate_aws_session(args.profile, args.region)
    
    regions = get_target_regions(session, args.all_regions, args.region)
    
    findings: List[Dict[str, Any]] = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Cria diretório versionado para os relatórios
    output_dir = f"reports/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    audit_tasks = [
        ("S3", lambda r: check_s3_buckets(session, r)),
        ("IAM", lambda r: check_iam_users(session, r)),
        ("Security Groups", lambda r: check_security_groups(session, r))
    ]

    logging.info("Iniciando varredura paralela do ambiente AWS...")

    # ThreadPool dimensionado dinamicamente de forma segura
    max_workers = min(32, max(1, len(regions) * len(audit_tasks)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {}
        
        for region in regions:
            for name, func in audit_tasks:
                future = executor.submit(func, region)
                future_to_task[future] = f"{name} ({region})"

        for future in concurrent.futures.as_completed(future_to_task):
            task_name = future_to_task[future]
            try:
                results = future.result()
                if results:
                    findings.extend(results)
                logging.info(f"Módulo {task_name} finalizado.")
            except Exception as e:
                logging.error(f"Erro crítico no módulo {task_name}: {e}")

    # Calcula o score geral e exibe o resumo executivo detalhado
    security_score = calculate_score(findings)
    print_executive_summary(findings, security_score)
    
    # 1. Exporta resultados em JSON dentro da pasta de relatórios
    json_filename = os.path.join(output_dir, "security_findings.json")
    try:
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump({"score": security_score, "timestamp": timestamp, "findings": findings}, f, indent=4, ensure_ascii=False)
        logging.info(f"Relatório JSON gerado: {json_filename}")
    except Exception as e:
        logging.error(f"Falha ao salvar o JSON: {e}")

    # 2. Exporta resultados em Excel (.xlsx) usando Pandas
    excel_filename = os.path.join(output_dir, "security_report.xlsx")
    try:
        if findings:
            df = pd.DataFrame(findings)
            df.to_excel(excel_filename, index=False)
            logging.info(f"Relatório Excel gerado: {excel_filename}")
        else:
            logging.info("Nenhum achado para exportar no Excel.")
    except Exception as e:
        logging.error(f"Falha ao gerar o Excel: {e}")

    # 3. Gera os relatórios visuais (PDF e Dashboard HTML)
    try:
        generate_pdf_report(findings, security_score, timestamp, output_dir)
        generate_html_dashboard(findings, security_score, timestamp, output_dir)
        print(f"🚀 Relatórios organizados e salvos com sucesso em: {output_dir}/")
    except Exception as e:
        logging.error(f"Falha ao gerar relatórios finais: {e}")

if __name__ == "__main__":
    main()