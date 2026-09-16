from backend.aws.aws import AWSConnector
from botocore.exceptions import ClientError


class SecurityHubManager:

    def __init__(self):
        self.aws = AWSConnector()
        self.session = self.aws.get_session()

    def get_findings(self):

        try:

            securityhub = self.session.client("securityhub")

            response = securityhub.get_findings()

            return response["Findings"]

        except ClientError as error:

            print(f"Erro Security Hub: {error}")

            return []