import logging
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError

def check_s3_buckets(session: boto3.Session, region: str) -> List[Dict[str, Any]]:
    """
    Verifica a segurança dos buckets S3 na região especificada.
    Analisa configurações de acesso público e políticas de bucket.
    """
    findings: List[Dict[str, Any]] = []
    
    try:
        # Cria o cliente S3 na região informada
        s3_client = session.client('s3', region_name=region)
        
        # Lista os buckets da conta (S3 é global, mas podemos filtrar ou checar)
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            try:
                # 1. Verifica o Block Public Access do Bucket
                pub_access = s3_client.get_public_access_block(Bucket=bucket_name)
                config = pub_access.get('PublicAccessBlockConfiguration', {})
                
                is_public_exposed = not (
                    config.get('BlockPublicAcls') and
                    config.get('IgnorePublicAcls') and
                    config.get('BlockPublicPolicy') and
                    config.get('RestrictPublicBuckets')
                )
                
                if is_public_exposed:
                    findings.append({
                        "service": "S3",
                        "severity": "HIGH",
                        "resource": f"arn:aws:s3:::{bucket_name}",
                        "issue": f"O bucket S3 '{bucket_name}' possui configurações que permitem acesso público.",
                        "impact": "Exposição indesejada de dados confidenciais armazenados na nuvem para a internet.",
                        "recommendation": "Habilite todas as opções de 'Block Public Access' nas configurações do bucket.",
                        "compliance": "CIS AWS Benchmark 2.1.1",
                        "region": region
                    })
                    
            except ClientError as e:
                error_code = e.response['Error']['Code']
                # Se o bloco de acesso público não estiver configurado, é um risco crítico
                if error_code == 'NoSuchPublicAccessBlockConfiguration':
                    findings.append({
                        "service": "S3",
                        "severity": "CRITICAL",
                        "resource": f"arn:aws:s3:::{bucket_name}",
                        "issue": f"O bucket '{bucket_name}' não possui nenhuma configuração de Block Public Access ativa.",
                        "impact": "Alto risco de vazamento de dados caso alguma política permita leitura pública.",
                        "recommendation": "Configure imediatamente o Block Public Access para o bucket S3.",
                        "compliance": "CIS AWS Benchmark 2.1.2",
                        "region": region
                    })
                else:
                    logging.warning(f"Não foi possível verificar as políticas do bucket {bucket_name}: {e}")
                    
    except Exception as e:
        logging.error(f"Erro ao listar buckets S3 na região {region}: {e}")
        
    return findings