from backend.aws.aws import AWSConnector

class EC2Manager:

    def __init__(self):
        self.aws = AWSConnector()
        self.session = self.aws.get_session()

    def list_instances(self):

        ec2 = self.session.client("ec2")

        response = ec2.describe_instances()

        return response["Reservations"]