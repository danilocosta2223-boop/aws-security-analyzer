from backend.dashboard.dashboard import Dashboard
from backend.aws.account import AWSAccountAnalyzer


class AWSService:

    def __init__(self):
        self.dashboard = Dashboard()
        self.account = AWSAccountAnalyzer()

    def get_dashboard_data(self):
        return self.dashboard.get_dashboard_data()

    def get_account_context(self):
        return self.account.get_account_context()