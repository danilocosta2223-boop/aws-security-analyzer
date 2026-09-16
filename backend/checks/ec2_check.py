from backend.aws.ec2 import EC2Manager


class EC2Check:

    def __init__(self):
        self.ec2 = EC2Manager()

    def check_instances(self):

        instances = self.ec2.list_instances()

        results = []

        for reservation in instances:

            for instance in reservation["Instances"]:

                results.append({
                    "id": instance["InstanceId"],
                    "type": instance["InstanceType"],
                    "state": instance["State"]["Name"]
                })

        return results