import boto3


class AWSConnector:

    def __init__(self, region="us-east-1"):
        self.region = region

    def get_session(self):
        return boto3.Session(
            region_name=self.region
        )

    def get_account_info(self):

        session = self.get_session()

        sts = session.client("sts")

        return sts.get_caller_identity()