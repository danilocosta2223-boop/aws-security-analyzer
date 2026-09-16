"""
backend/checks/bucket_encryption_check.py
"""

import boto3
from botocore.exceptions import ClientError


class BucketEncryptionCheck:

    def __init__(self, session=None):
        self.session = session or boto3.Session()
        self.s3_client = self.session.client("s3")

    def run_check(self):
        findings = []

        try:
            buckets = self.s3_client.list_buckets().get("Buckets", [])
        except ClientError as e:
            print(f"Erro ao listar buckets para criptografia: {e}")
            return findings

        for bucket in buckets:
            bucket_name = bucket["Name"]

            try:
                # Tenta obter a configuração de criptografia
                self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code")

                # Se o código for ServerSideEncryptionConfigurationNotFoundError, o bucket não tem criptografia
                if error_code == "ServerSideEncryptionConfigurationNotFoundError":
                    findings.append({
                        "severity": "HIGH",
                        "title": "Bucket S3 sem criptografia habilitada",
                        "description": (
                            f"O bucket '{bucket_name}' não possui criptografia padrão "
                            "em repouso (Server-Side Encryption) configurada."
                        ),
                        "resource": bucket_name,
                        "remediation": (
                            "Habilite a criptografia padrão SSE-S3 ou SSE-KMS "
                            "nas propriedades do bucket."
                        )
                    })
                else:
                    print(f"Erro ao verificar criptografia do bucket {bucket_name}: {e}")

        return findings