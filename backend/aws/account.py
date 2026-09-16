import boto3
from botocore.exceptions import BotoCoreError, ClientError


class AWSAccountAnalyzer:

    def __init__(self, session=None):
        self.session = session or boto3.Session()
        self.sts_client = self.session.client("sts")

    def get_account_context(self) -> dict:

        try:

            identity = self.sts_client.get_caller_identity()

            region = self.session.region_name or "us-east-1"

            arn = identity.get("Arn", "")

            user_or_role = (
                arn.split("/")[-1]
                if "/" in arn
                else arn
            )

            return {
                "account_id": identity.get(
                    "Account",
                    "Desconhecido"
                ),
                "region": region,
                "iam_user": user_or_role,
                "arn": arn,
                "status": "success"
            }

        except (BotoCoreError, ClientError) as e:

            return {
                "account_id": "Erro de Conexão",
                "region": self.session.region_name
                          or "us-east-1",
                "iam_user": "Não Autenticado",
                "arn": "",
                "status": "error",
                "message": str(e)
            }