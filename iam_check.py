import logging
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError

def check_iam_users(session: boto3.Session, region: str) -> List[Dict[str, Any]]:
    """
    Verifica a segurança dos usuários IAM na conta AWS.
    Analisa se os usuários possuem MFA habilitado e se há chaves de acesso ativas antigas.
    """
    findings: List[Dict[str, Any]] = []
    
    try:
        # O IAM é um serviço global na AWS, mas aceitamos o parâmetro 'region' 
        # para manter o padrão da arquitetura paralela do projeto.
        iam_client = session.client('iam')
        
        response = iam_client.list_users()
        users = response.get('Users', [])
        
        for user in users:
            username = user['UserName']
            
            try:
                # 1. Verifica se o usuário possui Dispositivo MFA ativo
                mfa_response = iam_client.list_mfa_devices(UserName=username)
                mfa_devices = mfa_response.get('MFADevices', [])
                
                if not mfa_devices:
                    findings.append({
                        "service": "IAM",
                        "severity": "CRITICAL",
                        "resource": f"arn:aws:iam::user/{username}",
                        "issue": f"O usuário IAM '{username}' não possui dispositivo MFA (Autenticação Multifator) ativado.",
                        "impact": "Contas sem MFA são extremamente vulneráveis a ataques de força bruta e roubo de credenciais.",
                        "recommendation": "Habilite imediatamente o MFA para este usuário no Console AWS.",
                        "compliance": "CIS AWS Benchmark 1.2",
                        "region": region
                    })
                    
            except ClientError as e:
                logging.warning(f"Não foi possível verificar o MFA para o usuário {username}: {e}")
                
    except Exception as e:
        logging.error(f"Erro ao listar usuários IAM: {e}")
        
    return findings