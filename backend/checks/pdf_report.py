from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFReportGenerator:

    def generate(self, dashboard_data):

        buffer = BytesIO()

        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "AWS Security Analyzer",
                styles["Title"]
            )
        )

        content.append(
            Paragraph(
                "Relatório Executivo de Segurança",
                styles["Heading2"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                f"Conta AWS: {dashboard_data['account_id']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Região: {dashboard_data['region']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"IAM User: {dashboard_data['iam_user']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Security Score: {dashboard_data['security_score']}%",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                "Achados de Segurança",
                styles["Heading2"]
            )
        )

        for finding in dashboard_data["findings"]:

            content.append(
                Paragraph(
                    f"<b>{finding['severity']}</b> - {finding['title']}",
                    styles["Normal"]
                )
            )

            if "description" in finding:

                content.append(
                    Paragraph(
                        finding["description"],
                        styles["Normal"]
                    )
                )

            content.append(
                Spacer(1, 10)
            )

        pdf.build(content)

        buffer.seek(0)

        return buffer