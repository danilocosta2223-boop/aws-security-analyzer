"""
AWS Security Analyzer - PDF Report Generator
"""

import io
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFReportGenerator:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura estilos de tipografia personalizados."""
        self.styles.add(ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=4
        ))
        
        self.styles.add(ParagraphStyle(
            'ReportSubTitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        ))

        self.styles.add(ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1e293b'),
            spaceBefore=12,
            spaceAfter=8
        ))

        self.styles.add(ParagraphStyle(
            'FindingTitle',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0f172a')
        ))

        self.styles.add(ParagraphStyle(
            'FindingBody',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155')
        ))

        self.styles.add(ParagraphStyle(
            'RemediationText',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor('#475569')
        ))

    def _get_severity_color(self, severity):
        """Retorna a cor associada à severidade do achado."""
        sev_map = {
            'CRITICAL': colors.HexColor('#dc2626'),
            'HIGH': colors.HexColor('#ef4444'),
            'MEDIUM': colors.HexColor('#f59e0b'),
            'LOW': colors.HexColor('#3b82f6')
        }
        return sev_map.get(severity.upper(), colors.HexColor('#64748b'))

    def generate(self, data):
        """Gera o buffer binário do relatório em PDF a partir dos dados do dashboard."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        story = []

        # 1. Cabeçalho Principal
        story.append(Paragraph("AWS Security Analyzer", self.styles['ReportTitle']))
        story.append(Paragraph("Relatorio Executivo de Auditoria e Conformidade de Seguranca", self.styles['ReportSubTitle']))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#cbd5e1'), spaceAfter=15))

        # 2. Metadados do Relatório (Ajustado para ler diretamente de data)
        account_id = data.get("account_id", "N/A")
        region = data.get("region", "N/A")
        iam_user = data.get("iam_user", "N/A")
        gen_date = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
        
        meta_data = [
            [
                Paragraph(f"<b>Account ID:</b> {account_id}", self.styles['FindingBody']),
                Paragraph(f"<b>Data:</b> {gen_date}", self.styles['FindingBody'])
            ],
            [
                Paragraph(f"<b>Regiao:</b> {region}", self.styles['FindingBody']),
                Paragraph(f"<b>Autor:</b> Danilo Rafael da Silva Costa", self.styles['FindingBody'])
            ],
            [
                Paragraph(f"<b>IAM User:</b> {iam_user}", self.styles['FindingBody']),
                ""
            ]
        ]
        
        meta_table = Table(meta_data, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 2), (1, 2)),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # 3. Resumo de Métricas (Security Score + Resumo de Vulnerabilidades)
        score = data.get("security_score", 0)
        findings = data.get("findings", [])

        crit_count = sum(1 for f in findings if f.get("severity", "").upper() == "CRITICAL")
        high_count = sum(1 for f in findings if f.get("severity", "").upper() == "HIGH")
        med_count = sum(1 for f in findings if f.get("severity", "").upper() == "MEDIUM")
        low_count = sum(1 for f in findings if f.get("severity", "").upper() == "LOW")

        summary_data = [
            ["Security Score", "Criticos", "Altos", "Medios", "Baixos"],
            [f"{score}%", str(crit_count), str(high_count), str(med_count), str(low_count)]
        ]

        summary_table = Table(summary_data, colWidths=[110, 107, 107, 107, 107])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 12),
            ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#10b981') if score >= 80 else colors.HexColor('#dc2626')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))

        # 4. Detalhamento dos Achados (Findings)
        story.append(Paragraph("Vulnerabilidades Encontradas e Recomendacoes", self.styles['SectionHeading']))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

        if not findings:
            story.append(Paragraph("Nenhuma vulnerabilidade detectada na conta auditada.", self.styles['FindingBody']))
        else:
            for finding in findings:
                severity = finding.get("severity", "LOW").upper()
                sev_color = self._get_severity_color(severity)
                title = finding.get("title", "Vulnerabilidade Detectada")
                resource = finding.get("resource", "N/A")
                desc = finding.get("description", "")
                remediation = finding.get("remediation", "")

                finding_content = [
                    [
                        Paragraph(f"<b>[{severity}]</b> {title}", self.styles['FindingTitle']),
                        Paragraph(f"<b>Recurso:</b> {resource}", self.styles['FindingBody'])
                    ],
                    [
                        Paragraph(desc, self.styles['FindingBody']),
                        ""
                    ]
                ]

                if remediation:
                    finding_content.append([
                        Paragraph(f"<b>Remediacao:</b> {remediation}", self.styles['RemediationText']),
                        ""
                    ])

                finding_table = Table(finding_content, colWidths=[380, 157])
                
                table_styles = [
                    ('SPAN', (0, 1), (1, 1)),
                    ('LINELEFT', (0, 0), (0, -1), 3.5, sev_color),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
                    ('PADDING', (0, 0), (-1, -1), 5),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]
                
                if remediation:
                    table_styles.append(('SPAN', (0, 2), (1, 2)))

                finding_table.setStyle(TableStyle(table_styles))
                story.append(finding_table)
                story.append(Spacer(1, 8))

        # Construção final do documento PDF
        doc.build(story)
        buffer.seek(0)
        return buffer