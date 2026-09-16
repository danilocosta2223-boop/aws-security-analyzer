from backend.dashboard.dashboard import Dashboard
from backend.security.findings import FindingsEngine


class ReportGenerator:

    def generate(self):

        dashboard = Dashboard()

        summary = dashboard.get_summary()

        findings = FindingsEngine().get_findings()

        return {
            "summary": summary,
            "findings": findings
        }