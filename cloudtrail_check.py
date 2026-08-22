import boto3
from botocore.exceptions import ClientError

def check_cloudtrail_status(region="us-east-1"):
    """
    Verifica se o CloudTrail possui trilhas ativas de auditoria e multi-região.
    """
    findings_list = []
    client = boto3.client('cloudtrail', region_name=region)
    
    try:
        trails = client.describe_trails(includeShadowTrails=True)
        trail_list = trails.get('trailList', [])
        
        if not trail_list:
            return [{
                "service": "CloudTrail",
                "severity": "HIGH",
                "resource": "AWS CloudTrail",
                "issue": "Nenhuma trilha (Trail) do CloudTrail configurada na conta.",
                "code": "CLOUDTRAIL_NOT_FOUND",
                "recommendation": "Criar e habilitar uma trilha global do CloudTrail para auditoria forense."
            }]
            
        active_global_trail = False
        for trail in trail_list:
            status = client.get_trail_status(Name=trail['Name'])
            if status.get('IsLogging', False) and trail.get('IsMultiRegionTrail', False):
                active_global_trail = True
                break
                
        if not active_global_trail:
            findings_list.append({
                "service": "CloudTrail",
                "severity": "MEDIUM",
                "resource": "CloudTrail Multi-Region",
                "issue": "CloudTrail ativo, mas sem cobertura Multi-Região ou desativado.",
                "code": "CLOUDTRAIL_NOT_GLOBAL",
                "recommendation": "Habilitar gravação multi-região e log file validation no CloudTrail."
            })
        else:
            findings_list.append({
                "service": "CloudTrail",
                "severity": "LOW",
                "resource": "CloudTrail Global",
                "issue": "Trilha multi-região ativa e validando integridade de logs.",
                "code": "CLOUDTRAIL_SECURE",
                "recommendation": "Manter monitoramento de eventos via CloudWatch/SIEM."
            })

    except ClientError as e:
        findings_list.append({
            "service": "CloudTrail",
            "severity": "LOW",
            "resource": region,
            "issue": f"Erro ao auditar CloudTrail: {e.response['Error']['Code']}",
            "code": "CLOUDTRAIL_ERROR",
            "recommendation": "Revisar políticas de permissão IAM."
        })
        
    return findings_list

if __name__ == "__main__":
    print(check_cloudtrail_status())