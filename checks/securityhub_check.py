import boto3
from botocore.exceptions import ClientError

def check_security_hub_findings(region="us-east-1"):
    """
    Consulta o AWS Security Hub para buscar falhas críticas de compliance.
    """
    findings_list = []
    summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    
    client = boto3.client('securityhub', region_name=region)
    
    try:
        # Verifica se o Security Hub está habilitado
        client.describe_hub()
        
        # Puxa os achados ativos e não resolvidos
        response = client.get_findings(
            Filters={
                'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}],
                'WorkflowStatus': [{'Value': 'NEW', 'Comparison': 'EQUALS'}]
            },
            MaxResults=10
        )
        
        for f in response.get('Findings', []):
            title = f.get('Title', 'Desvio de Compliance')
            sev_label = f.get('Severity', {}).get('Label', 'LOW').upper()
            
            if sev_label in summary:
                summary[sev_label] += 1
            else:
                summary["LOW"] += 1
                
            findings_list.append({
                "service": "Security Hub",
                "severity": sev_label if sev_label in ["CRITICAL", "HIGH", "MEDIUM"] else "LOW",
                "resource": f.get('Resources', [{}])[0].get('Id', 'AWS Resource'),
                "issue": f"[Security Hub] {title}",
                "code": "SECURITY_HUB_FINDING",
                "recommendation": f"Remediar padrão de compliance violado: {f.get('Compliance', {}).get('Status', 'WARNING')}"
            })

    except ClientError as e:
        code = e.response['Error']['Code']
        findings_list.append({
            "service": "Security Hub",
            "severity": "LOW",
            "resource": f"Region {region}",
            "issue": f"Security Hub não habilitado ou sem permissão ({code}).",
            "code": "SECURITY_HUB_INACTIVE",
            "recommendation": "Habilitar o AWS Security Hub via console ou CLI."
        })
        
    return findings_list, summary

if __name__ == "__main__":
    print(check_security_hub_findings())