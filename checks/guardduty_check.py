import boto3
from botocore.exceptions import ClientError

def check_guardduty_threats(region="us-east-1"):
    """
    Verifica o status do Amazon GuardDuty e puxa findings de ameaças ativas.
    """
    findings_list = []
    client = boto3.client('guardduty', region_name=region)
    
    try:
        # Lista detectors ativos na região
        detectors = client.list_detectors()
        detector_ids = detectors.get('DetectorIds', [])
        
        if not detector_ids:
            return [{
                "service": "GuardDuty",
                "severity": "MEDIUM",
                "resource": f"Region {region}",
                "issue": "Nenhum GuardDuty Detector habilitado nesta região.",
                "code": "GUARDDUTY_DISABLED",
                "recommendation": "Habilitar o Amazon GuardDuty para monitoramento contínuo de ameaças."
            }]
        
        for det_id in detector_ids:
            # Puxa findings ativos (não arquivados)
            findings_response = client.list_findings(
                DetectorId=det_id,
                FindingCriteria={
                    'Criterion': {
                        'service.archived': {'Eq': ['false']}
                    }
                },
                MaxResults=5
            )
            finding_ids = findings_response.get('FindingIds', [])
            
            if finding_ids:
                details = client.get_findings(DetectorId=det_id, FindingIds=finding_ids)
                for f in details.get('Findings', []):
                    title = f.get('Title', 'Atividade Suspeita Detectada')
                    sev_num = f.get('Severity', 1)
                    
                    # Normaliza severidade do GuardDuty para o padrão CSOC
                    sev_str = "HIGH" if sev_num >= 7.0 else ("MEDIUM" if sev_num >= 4.0 else "LOW")
                    
                    findings_list.append({
                        "service": "GuardDuty Threat Intel",
                        "severity": sev_str,
                        "resource": f.get('Resource', {}).get('ResourceType', 'AWS Resource'),
                        "issue": f"Ameaça detectada: {title}",
                        "code": "GUARDDUTY_THREAT",
                        "recommendation": "Investigar imediatamente o IP/credencial comprometida isolando o recurso."
                    })
        
        if not findings_list:
            findings_list.append({
                "service": "GuardDuty Threat Intel",
                "severity": "LOW",
                "resource": f"Detector {detector_ids[0]}",
                "issue": "Nenhuma ameaça ativa detectada pelo GuardDuty.",
                "code": "GUARDDUTY_CLEAN",
                "recommendation": "Manter postura de monitoramento ativo."
            })

    except ClientError as e:
        code = e.response['Error']['Code']
        findings_list.append({
            "service": "GuardDuty",
            "severity": "LOW",
            "resource": f"Region {region}",
            "issue": f"Erro ao acessar GuardDuty ({code}). Verifique permissões IAM.",
            "code": "GUARDDUTY_ERROR",
            "recommendation": "Conceder a política AmazonGuardDutyReadOnlyAccess."
        })
        
    return findings_list

if __name__ == "__main__":
    print(check_guardduty_threats())