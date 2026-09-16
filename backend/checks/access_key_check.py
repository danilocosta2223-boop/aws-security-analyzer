"""
AWS Security Analyzer - IAM Access Key Age Check
"""

import boto3
from datetime import datetime, timezone


class AccessKeyCheck:

    def __init__(self, iam_client=None):
        self.iam = iam_client or boto3.client('iam')

    def run(self):
        findings = []
        now = datetime.now(timezone.utc)

        try:
            users_response = self.iam.list_users()
            for user in users_response.get('Users', []):
                username = user.get('UserName')
                keys_response = self.iam.list_access_keys(UserName=username)

                for key in keys_response.get('AccessKeyMetadata', []):
                    key_id = key.get('AccessKeyId')
                    status = key.get('Status')
                    created_date = key.get('CreateDate')

                    if status == 'Active':
                        age_days = (now - created_date).days

                        if age_days > 180:
                            findings.append({
                                "severity": "CRITICAL",
                                "title": f"Access Key ativa há mais de 180 dias ({age_days} dias)",
                                "resource": f"{username} / {key_id}",
                                "description": f"A chave de acesso {key_id} do usuário {username} tem {age_days} dias sem rotação.",
                                "remediation": "Desative e exclua a chave antiga, gerando uma nova credencial com rotatividade programada."
                            })
                        elif age_days > 90:
                            findings.append({
                                "severity": "HIGH",
                                "title": f"Access Key ativa há mais de 90 dias ({age_days} dias)",
                                "resource": f"{username} / {key_id}",
                                "description": f"A chave de acesso {key_id} do usuário {username} ultrapassou o limite recomendado de 90 dias.",
                                "remediation": "Planeje a rotação da chave de acesso para manter a conformidade com as boas práticas."
                            })
        except Exception as e:
            findings.append({
                "severity": "LOW",
                "title": "Erro ao checar idade das Access Keys",
                "resource": "IAM Service",
                "description": str(e),
                "remediation": "Garanta permissões iam:ListUsers e iam:ListAccessKeys no perfil da AWS."
            })

        return findings