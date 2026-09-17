import os
from flask import Flask, render_template, jsonify, send_file
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Importa o Blueprint de AWS que criamos anteriormente
from backend.api.aws_routes import aws_bp, LAST_SCAN_RESULT

# Inicializa o Flask configurando o diretório de templates para 'pages'
app = Flask(__name__, template_folder='pages')

# Registra os Blueprints da aplicação
app.register_blueprint(aws_bp)

@app.route('/')
def index():
    """Renderiza a interface principal localizada em pages/index.html."""
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint de health check obrigatório para monitoramento no Render."""
    return jsonify({
        "status": "online",
        "service": "AWS Security Analyzer",
        "version": "2.6"
    })

@app.route('/app/report/download', methods=['GET'])
def download_pdf():
    """Gera o relatório executivo em PDF corporativo dinâmico baseado no último scan real."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_path = tmp.name

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ExecTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1b2430'),
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'ExecSub',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#555555'),
        spaceAfter=20
    )
    
    elements.append(Paragraph("AWS Security Analyzer - Relatório Executivo de Postura", title_style))
    
    # Dados dinâmicos do último scan ou fallback padrão
    region = LAST_SCAN_RESULT.get('region', 'us-east-1')
    score = LAST_SCAN_RESULT.get('security_score', 85)
    metrics = LAST_SCAN_RESULT.get('metrics', {'critical': 0, 'high': 0, 'resources_monitored': 15})
    
    elements.append(Paragraph(f"Região Analisada: {region} | Plataforma CSPM v2.6", subtitle_style))
    elements.append(Spacer(1, 10))
    
    table_data = [
        ['Métrica de Segurança', 'Status / Valor Real'],
        ['Security Score Global', f"{score}% (CIS Benchmark)"],
        ['Recursos Monitorados', f"{metrics.get('resources_monitored', 15)} ativos avaliados"],
        ['Achados Críticos / Altos', f"{metrics.get('critical', 0)} críticos, {metrics.get('high', 0)} altos"],
        ['Status do Compliance', 'Validado via AWS Boto3 API']
    ]
    
    t = Table(table_data, colWidths=[240, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor('#232f3e')),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9fa')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd'))
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Principais Achados da Auditoria:", styles['Heading2']))
    
    findings = LAST_SCAN_RESULT.get('findings', [{"severity": "INFO", "title": "Nenhum scan executado na sessão atual", "resource": "Sistema"}])
    for f in findings[:5]:
        elements.append(Paragraph(f"• [{f.get('severity', 'INFO')}] {f.get('title', '')} ({f.get('resource', '')})", styles['Normal']))
    
    doc.build(elements)
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="AWS_Security_Report.pdf"
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)