from backend.aws.iam import IAMManager


class IAMCheck:

    def __init__(self):
        self.iam = IAMManager()

    def check_users(self):

        users = self.iam.list_users()

        results = []

        for user in users:

            results.append({
                "username": user["UserName"],
                "arn": user["Arn"],
                "created": str(user["CreateDate"])
            })

        return results