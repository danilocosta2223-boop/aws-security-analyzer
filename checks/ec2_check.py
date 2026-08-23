import logging
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError

def check_security_groups(session: boto3.Session, region: str) -> List[Dict[str, Any]]:
    """
    Verifica a segurança dos Security Groups da EC2 na região especificada.
    Identifica regras de entrada (Inbound) permitindo acesso público (0.0.0.0/0) 
    em portas sensíveis como SSH (22) e RDP (3389).
    """
    findings: List[Dict[str, Any]] = []
    
    try:
        # Cria o cliente EC2 na região informada
        ec2_client = session.client('ec2', region_name=region)
        
        # Descreve todos os Security Groups da VPC/região
        response = ec2_client.describe_security_groups()
        security_groups = response.get('SecurityGroups', [])
        
        for sg in security_groups:
            sg_id = sg['GroupId']
            sg_name = sg['GroupName']
            vpc_id = sg.get('VpcId', 'N/A')
            
            # Analisa as regras de entrada (Ingress)
            for rule in sg.get('IpPermissions', []):
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                ip_protocol = rule.get('IpProtocol', '')
                
                # Verifica se a regra permite tráfego de qualquer IP (-1 significa todas as portas/protocolos)
                for ip_range in rule.get('IpRanges', []):
                    cidr_ip = ip_range.get('CidrIp', '')
                    
                    if cidr_ip == '0.0.0.0/0':
                        # Caso 1: Acesso total livre (-1 ou porta 0 a 65535)
                        if ip_protocol == '-1' or (from_port is not None and from_port <= 0 and to_port >= 65535):
                            findings.append({
                                "service": "EC2",
                                "severity": "CRITICAL",
                                "resource": f"arn:aws:ec2:{region}:{sg_id}",
                                "issue": f"O Security Group '{sg_name}' ({sg_id}) permite acesso total de qualquer IP (0.0.0.0/0) em todas as portas.",
                                "impact": "Exposição crítica de toda a infraestrutura associada a este grupo para a internet.",
                                "recommendation": "Restrinque as regras de entrada para IPs corporativos ou VPNs confiáveis.",
                                "compliance": "CIS AWS Benchmark 5.2",
                                "region": region
                            })
                        
                        # Caso 2: Porta SSH (22) aberta para o mundo
                        elif from_port is not None and from_port <= 22 <= to_port:
                            findings.append({
                                "service": "EC2",
                                "severity": "CRITICAL",
                                "resource": f"arn:aws:ec2:{region}:{sg_id}",
                                "issue": f"O Security Group '{sg_name}' ({sg_id}) expõe a porta SSH (22) diretamente para a internet (0.0.0.0/0).",
                                "impact": "Alto risco de ataques de força bruta e invasão direta aos servidores Linux.",
                                "recommendation": "Altere a regra para permitir SSH apenas a partir de um IP específico ou use AWS Systems Manager Session Manager.",
                                "compliance": "CIS AWS Benchmark 5.3",
                                "region": region
                            })
                            
                        # Caso 3: Porta RDP (3389) aberta para o mundo
                        elif from_port is not None and from_port <= 3389 <= to_port:
                            findings.append({
                                "service": "EC2",
                                "severity": "CRITICAL",
                                "resource": f"arn:aws:ec2:{region}:{sg_id}",
                                "issue": f"O Security Group '{sg_name}' ({sg_id}) expõe a porta RDP (3389) diretamente para a internet (0.0.0.0/0).",
                                "impact": "Alto risco de invasão e sequestro de instâncias Windows via Remote Desktop.",
                                "recommendation": "Restrinque o acesso à porta RDP para faixas de IP seguras ou utilize Bastion Hosts.",
                                "compliance": "CIS AWS Benchmark 5.4",
                                "region": region
                            })
                            
                # Verifica também blocos IPv6 públicos (::/0)
                for ipv6_range in rule.get('Ipv6Ranges', []):
                    cidr_ipv6 = ipv6_range.get('CidrIpv6', '')
                    if cidr_ipv6 == '::/0' and (from_port == 22 or from_port == 3389 or ip_protocol == '-1'):
                        findings.append({
                            "service": "EC2",
                            "severity": "HIGH",
                            "resource": f"arn:aws:ec2:{region}:{sg_id}",
                            "issue": f"O Security Group '{sg_name}' ({sg_id}) expõe portas sensíveis publicamente via IPv6 (::/0).",
                            "impact": "Exposição de serviços internos para a rede IPv6 global.",
                            "recommendation": "Remova regras permissivas de IPv6 em portas administrativas.",
                            "compliance": "CIS AWS Benchmark 5.5",
                            "region": region
                        })
                        
    except Exception as e:
        logging.error(f"Erro ao listar Security Groups na região {region}: {e}")
        
    return findings