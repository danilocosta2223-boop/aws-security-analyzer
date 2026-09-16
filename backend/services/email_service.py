# services/email_service.py

from datetime import datetime

class EmailService:
    def __init__(self, sender_email: str = "security@cloudanalyzer.io"):
        self.sender_email = sender_email

    def generate_security_report_html(self, account_context: dict, score: int, findings: list) -> str:
        """
        Gera um relatório executivo de segurança em HTML formatado para envio por e-mail.
        """
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        account_id = account_context.get("account_id", "--")
        region = account_context.get("region", "us-east-1")

        # Cor do score dinâmica
        score_color = "#10b981" if score >= 80 else ("#f97316" if score >= 50 else "#ef4444")

        # Linhas da tabela de achados
        rows_html = ""
        for f in findings:
            sev = f.get("severity", "LOW").upper()
            sev_color = {
                "CRITICAL": "#ef4444",
                "HIGH": "#f97316",
                "MEDIUM": "#eab308",
                "LOW": "#10b981"
            }.get(sev, "#6b7280")

            rows_html += f"""
            <tr style="border-bottom: 1px solid #374151;">
              <td style="padding: 12px; font-weight: bold; color: {sev_color};">{sev}</td>
              <td style="padding: 12px; color: #f9fafb;">{f.get('title', 'N/A')}</td>
              <td style="padding: 12px; color: #9ca3af; font-family: monospace;">{f.get('resource', 'N/A')}</td>
            </tr>
            """

        if not findings:
            rows_html = """
            <tr>
              <td colspan="3" style="padding: 16px; text-align: center; color: #10b981;">
                ✅ Nenhum problema de segurança detectado!
              </td>
            </tr>
            """

        # Template HTML final
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0b0f19; color: #f9fafb; margin: 0; padding: 20px; }}
            .container {{ max-width: 650px; margin: 0 auto; background-color: #111827; border: 1px solid #374151; border-radius: 10px; padding: 24px; }}
            .header {{ border-bottom: 1px solid #374151; padding-bottom: 16px; margin-bottom: 20px; }}
            .header h2 {{ margin: 0; color: #3b82f6; font-size: 20px; }}
            .meta {{ font-size: 13px; color: #9ca3af; margin-top: 6px; }}
            .score-box {{ text-align: center; background-color: #1f2937; padding: 20px; border-radius: 8px; margin-bottom: 24px; }}
            .score-val {{ font-size: 36px; font-weight: bold; color: {score_color}; }}
            table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }}
            th {{ background-color: #1f2937; color: #9ca3af; padding: 10px 12px; text-transform: uppercase; font-size: 12px; }}
            .footer {{ text-align: center; margin-top: 24px; font-size: 12px; color: #6b7280; border-top: 1px solid #374151; padding-top: 16px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h2>🛡️ AWS Security Analyzer — Relatório Executivo</h2>
              <div class="meta">
                Conta: <strong>{account_id}</strong> | Região: <strong>{region}</strong><br>
                Gerado em: {date_str}
              </div>
            </div>

            <div class="score-box">
              <div style="font-size: 14px; color: #9ca3af; margin-bottom: 4px;">Security Score</div>
              <div class="score-val">{score}/100</div>
            </div>

            <h3>Resumo de Achados</h3>
            <table>
              <thead>
                <tr>
                  <th>Severidade</th>
                  <th>Título / Problema</th>
                  <th>Recurso Afetado</th>
                </tr>
              </thead>
              <tbody>
                {rows_html}
              </tbody>
            </table>

            <div class="footer">
              AWS Security Analyzer © {datetime.now().year} — SecOps Platform
            </div>
          </div>
        </body>
        </html>
        """
        return html_content