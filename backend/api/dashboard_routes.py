"""
==============================================================================
         AWS Security Analyzer - Dashboard & Audit Routes Blueprint         
               Desenvolvido por Danilo Rafael da Silva Costa              
==============================================================================
"""

from flask import Blueprint, jsonify, send_file

from backend.dashboard.dashboard import Dashboard
from backend.security.findings import FindingsEngine
from backend.reports.pdf_report import PDFReportGenerator

# Definição do Blueprint
dashboard_bp = Blueprint("dashboard", __name__)

# Print de rastreio para confirmar no terminal que o arquivo foi lido pelo Python
print(">>> DASHBOARD_ROUTES CARREGADO COM SUCESSO <<<")


@dashboard_bp.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """
    Retorna os dados consolidados do painel de segurança.
    """
    try:
        dashboard = Dashboard()
        data = dashboard.get_dashboard_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao carregar dados do dashboard: {str(e)}"
        }), 500


@dashboard_bp.route("/api/audit-history", methods=["GET"])
def api_audit_history():
    """
    Retorna o histórico de auditorias para o gráfico de evolução.
    """
    try:
        engine = FindingsEngine()
        history = engine.get_audit_history()
        return jsonify({
            "status": "success",
            "history": history
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao carregar histórico: {str(e)}"
        }), 500


@dashboard_bp.route("/api/report", methods=["GET"])
def generate_report():
    """
    Gera e retorna o relatório executivo em PDF formatado.
    """
    try:
        dashboard = Dashboard()
        data = dashboard.get_dashboard_data()
        
        report = PDFReportGenerator()
        pdf_buffer = report.generate(data)
        
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="aws-security-report.pdf"
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar relatório PDF: {str(e)}"
        }), 500


@dashboard_bp.route("/teste", methods=["GET"])
def teste_rota():
    """
    Rota de diagnóstico rápido para testar o Blueprint.
    """
    return "ROTA TESTE OK"