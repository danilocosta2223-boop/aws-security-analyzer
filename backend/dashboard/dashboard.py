"""
AWS Security Analyzer - Dashboard Aggregator Service
Desenvolvido por Danilo Rafael da Silva Costa
"""

from backend.aws.account import AWSAccountAnalyzer
from backend.checks.iam_check import IAMCheck
from backend.checks.s3_check import S3Check
from backend.checks.ec2_check import EC2Check
from backend.security.security import SecurityAnalyzer
from backend.security.findings import FindingsEngine
from backend.services.notification_service import NotificationService


class Dashboard:

    def __init__(self, session=None):
        self.session = session
        self.notification_service = NotificationService()

    def get_dashboard_data(self) -> dict:
        """
        Consolida todas as métricas de segurança,
        recursos e contexto da conta AWS.
        """

        # Contexto AWS
        account_analyzer = AWSAccountAnalyzer(session=self.session)
        account_data = account_analyzer.get_account_context()

        # Recursos AWS
        iam_users = len(IAMCheck().check_users())
        s3_buckets = len(S3Check().check_buckets())
        ec2_instances = len(EC2Check().check_instances())

        # Motor de Achados de Segurança (Executa todos os checks e grava histórico)
        findings_engine = FindingsEngine()
        raw_findings = findings_engine.get_findings()
        audit_history = findings_engine.get_audit_history()

        # Cálculo de Score dinâmico baseado nos achados reais
        security = SecurityAnalyzer()
        score = security.calculate_score(raw_findings)

        # Salva o histórico com o score atual e quantidade de achados
        findings_engine._save_audit_history(score, len(raw_findings))

        # Alertas
        alerts = self.notification_service.get_all_alerts(raw_findings)

        return {
            "account_id": account_data.get("account_id", "--"),
            "region": account_data.get("region", "us-east-1"),
            "iam_user": account_data.get("iam_user", "--"),
            "iam_users": iam_users,
            "s3_buckets": s3_buckets,
            "ec2_instances": ec2_instances,
            "security_score": score,
            "findings": raw_findings,
            "audit_history": audit_history,
            "alerts": alerts
        }