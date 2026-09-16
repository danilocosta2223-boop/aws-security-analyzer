from backend.aws.aws import AWSConnector

class S3Manager:

    def __init__(self):
        self.aws = AWSConnector()
        self.session = self.aws.get_session()

    def list_buckets(self):
        s3 = self.session.client("s3")

        response = s3.list_buckets()

        return response["Buckets"]