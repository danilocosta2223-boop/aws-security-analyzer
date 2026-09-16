from backend.aws.aws import AWSConnector

class IAMManager:

    def __init__(self):
        self.aws = AWSConnector()
        self.session = self.aws.get_session()

    def list_users(self):

        iam = self.session.client("iam")

        response = iam.list_users()

        return response["Users"]