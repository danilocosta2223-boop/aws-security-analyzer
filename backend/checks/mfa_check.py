from backend.aws.iam import IAMManager


class MFACheck:

    def __init__(self):
        self.iam = IAMManager()

    def check_mfa(self):

        users = self.iam.list_users()

        results = []

        iam_client = self.iam.session.client("iam")

        for user in users:

            mfa = iam_client.list_mfa_devices(
                UserName=user["UserName"]
            )

            enabled = len(mfa["MFADevices"]) > 0

            results.append({
                "user": user["UserName"],
                "mfa_enabled": enabled
            })

        return results