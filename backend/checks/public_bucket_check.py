"""
AWS Security Analyzer - Public Bucket Check
Desenvolvido por Danilo Rafael da Silva Costa
"""

import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PublicBucketCheck:
    def __init__(self, session=None):
        self.session = session or boto3.Session()
        self.s3_client = self.session.client("s3")

    def is_public_block_active(self, bucket_name: str) -> bool:
        """
        Verifica se o recurso 'Block Public Access' está totalmente ativado no bucket.
        """
        try:
            response = self.s3_client.get_public_access_block(Bucket=bucket_name)
            config = response.get("PublicAccessBlockConfiguration", {})
            
            return all([
                config.get("BlockPublicAcls", False),
                config.get("IgnorePublicAcls", False),
                config.get("BlockPublicPolicy", False),
                config.get("RestrictPublicBuckets", False)
            ])
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "NoSuchPublicAccessBlockConfiguration":
                return False
            logger.error(f"Erro ao verificar Public Access Block no bucket {bucket_name}: {e}")
            return False

    def has_public_acl(self, bucket_name: str) -> bool:
        """
        Verifica se a ACL do bucket concede acesso público a AllUsers ou AuthenticatedUsers.
        """
        public_grants = [
            "http://acs.amazonaws.com/groups/global/AllUsers",
            "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
        ]
        try:
            acl = self.s3_client.get_bucket_acl(Bucket=bucket_name)
            for grant in acl.get("Grants", []):
                grantee = grant.get("Grantee", {})
                if grantee.get("Type") == "Group" and grantee.get("URI") in public_grants:
                    return True
            return False
        except ClientError as e:
            logger.error(f"Erro ao verificar ACL do bucket {bucket_name}: {e}")
            return False

    def run_check(self) -> list:
        """
        Executa a verificação em todos os buckets S3 e retorna achados estruturados.
        """
        findings = []

        try:
            buckets_resp = self.s3_client.list_buckets()
            buckets = buckets_resp.get("Buckets", [])
        except ClientError as e:
            logger.error(f"Erro ao listar buckets S3: {e}")
            return findings

        for bucket in buckets:
            bucket_name = bucket.get("Name")
            is_block_active = self.is_public_block_active(bucket_name)
            is_acl_public = self.has_public_acl(bucket_name)

            if not is_block_active or is_acl_public:
                findings.append({
                    "id": f"S3-PUBLIC-{bucket_name}",
                    "severity": "HIGH",
                    "title": "Bucket S3 público ou sem restrição total de acesso público",
                    "description": (
                        f"O bucket S3 '{bucket_name}' possui o 'Block Public Access' desativado "
                        f"ou possui ACL com permissões públicas configuradas."
                    ),
                    "resource": bucket_name,
                    "remediation": (
                        f"Ative todas as opções do 'Block Public Access' no bucket '{bucket_name}' "
                        f"e revogue concessões de ACL públicas."
                    )
                })

        return findings