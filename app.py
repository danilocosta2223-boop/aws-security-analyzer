"""
==============================================================================
                AWS Security Analyzer v2.0                       
                Backend Engine & Security Posture                    
                Autor: Danilo Rafael da Silva Costa                  
==============================================================================
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env local se existir
load_dotenv()

# Configuração do Sistema de Logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AWS-Security-Analyzer")


def create_app():
    # Cria a instância do Flask apontando para a pasta 'pages'
    app = Flask(__name__, template_folder="pages")

    # Configurações Centralizadas
    app.config.update(
        JSON_SORT_KEYS=False,
        TEMPLATES_AUTO_RELOAD=True,
        APP_NAME=os.getenv("APP_NAME", "AWS Security Analyzer"),
        APP_VERSION=os.getenv("APP_VERSION", "2.0"),
        AWS_REGION=os.getenv("AWS_REGION", "us-east-1"),
        SECRET_KEY=os.getenv("SECRET_KEY", "chave-secreta-padrao-desenvolvimento"),
        DEBUG=os.getenv("DEBUG", "False").lower() == "true"
    )

    logger.info("Aplicação inicializada com sucesso no ambiente: %s", os.getenv("FLASK_ENV", "production"))

    # ---------------------------------------------------------------------------
    # ROTAS DE MONITORAMENTO E SAÚDE DO SISTEMA
    # ---------------------------------------------------------------------------

    @app.route("/health")
    def health():
        return jsonify({
            "status": "online",
            "service": app.config["APP_NAME"],
            "version": app.config["APP_VERSION"],
            "environment": os.getenv("FLASK_ENV", "production"),
            "timestamp": datetime.now().isoformat()
        }), 200

    @app.route("/status")
    def status_page():
        return jsonify({
            "status": "online",
            "version": app.config["APP_VERSION"],
            "uptime": "99.9%",
            "author": "Danilo Rafael da Silva Costa",
            "region": app.config["AWS_REGION"],
            "timestamp": datetime.now().isoformat()
        }), 200

    # ---------------------------------------------------------------------------
    # ROTAS AMIGÁVEIS DE NAVEGAÇÃO SPA (Frontend)
    # ---------------------------------------------------------------------------

    @app.route("/")
    @app.route("/dashboard")
    @app.route("/security")
    @app.route("/aws")
    @app.route("/labs")
    @app.route("/reports")
    def render_spa_routes():
        """Renderiza a interface principal para todas as rotas limpas do portfólio."""
        return render_template("index.html")

    # ---------------------------------------------------------------------------
    # APIS DE DADOS E AUDITORIA DE SEGURANÇA CLOUD
    # ---------------------------------------------------------------------------

    @app.route("/api/info")
    def api_info():
        return jsonify({
            "project": app.config["APP_NAME"],
            "version": app.config["APP_VERSION"],
            "author": "Danilo Rafael da Silva Costa",
            "region": app.config["AWS_REGION"],
            "modules": [
                "Dashboard",
                "AWS Management Center",
                "Security Center",
                "Executive Reports",
                "Settings",
                "Labs & Tests"
            ]
        })

    @app.route("/api/version")
    def api_version():
        return jsonify({
            "version": app.config["APP_VERSION"],
            "author": "Danilo Rafael da Silva Costa"
        })

    @app.route("/api/aws-status")
    def aws_status():
        return jsonify({
            "ec2": 14,
            "s3": 5,
            "vpc": 3,
            "lambda": 7,
            "rds": 2,
            "cloudtrail": True,
            "security_hub": True
        })

    @app.route("/api/labs")
    def api_labs():
        return jsonify({
            "status": "success",
            "available_tests": [
                "IAM Audit",
                "MFA Audit",
                "S3 Audit",
                "Security Group Audit",
                "CloudTrail Audit",
                "Encryption Audit",
                "Root Account Audit",
                "Access Key Rotation Audit"
            ]
        })

    @app.route("/api/security-center")
    def security_center():
        return jsonify({
            "status": "success",
            "controls": {
                "mfa": True,
                "iam": False,
                "s3_security": True,
                "cloudtrail": True,
                "encryption": True,
                "security_groups": False
            },
            "summary": "6 controles avaliados. 2 requerem atenção imediata."
        })

    @app.route("/api/logs")
    def api_logs():
        return jsonify({
            "status": "success",
            "events": [
                {
                    "date": datetime.now().isoformat(),
                    "event": "AWS Security Posture Scan executed successfully."
                },
                {
                    "date": "2026-09-16T10:30:00",
                    "event": "IAM Compliance Verification initialized."
                }
            ]
        })

    @app.route('/api/dashboard')
    def api_dashboard():
        audit_data = {
            "security_score": 85,
            "account_id": "123456789012",
            "region": app.config["AWS_REGION"],
            "iam_user": "admin-security",
            "metrics": {
                "total_findings": 12,
                "critical": 1,
                "high": 3,
                "medium": 5,
                "low": 3,
                "secure_resources_percent": 98,
                "audits_executed": 150,
                "resources_monitored": 321,
                "aws_services": 12,
                "risk_score": 15,
                "last_scan": datetime.now().strftime("%Y-%m-%d")
            },
            "security_controls": {
                "mfa": "HABILITADO",
                "iam_policies": "ATENÇÃO",
                "security_groups": "CRÍTICO",
                "s3_public": "SEGURO",
                "cloudtrail": "HABILITADO",
                "encryption": "HABILITADO"
            },
            "findings": [
                {
                    "severity": "CRITICAL",
                    "title": "Security Group com porta 22 aberta para a internet",
                    "description": "O Security Group sg-012345 permitiu acesso SSH (porta 22) de 0.0.0.0/0.",
                    "resource": "sg-0123456789abcdef0",
                    "remediation": "Restrinque o acesso SSH para IPs confiáveis."
                },
                {
                    "severity": "HIGH",
                    "title": "MFA Desabilitado em Conta Privilegiada",
                    "description": "A conta root ou administrador IAM não possui autenticação multifator ativa.",
                    "resource": "arn:aws:iam::123456789012:root",
                    "remediation": "Ative o MFA obrigatório para todos os usuários com privilégios."
                }
            ]
        }
        return jsonify(audit_data)

    @app.route('/api/audit-history')
    def api_audit_history():
        return jsonify({
            "status": "success",
            "history": [
                {"date": "2026-09-12", "score": 78},
                {"date": "2026-09-13", "score": 80},
                {"date": "2026-09-14", "score": 82},
                {"date": "2026-09-15", "score": 84},
                {"date": "2026-09-16", "score": 85}
            ]
        })

    @app.route('/api/report', methods=['GET'])
    def api_report():
        return jsonify({
            "status": "success",
            "message": "Relatório executivo de segurança gerado com sucesso.",
            "download_url": "/app/report/download"
        }), 200

    @app.route('/app/report/download', methods=['GET'])
    def download_report():
        return jsonify({
            "status": "error",
            "message": "Exportação binária de relatório PDF via ReportLab em processamento."
        }), 501

    # ---------------------------------------------------------------------------
    # TRATAMENTO DE ERROS E SEGURANÇA HTTP
    # ---------------------------------------------------------------------------

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"status": "error", "code": 404, "message": "Recurso não encontrado."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.exception(error)
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Erro interno no motor de auditoria.",
            "details": str(error)
        }), 500

    @app.after_request
    def apply_security_headers(response):
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.headers["Server"] = "AWS-Security-Analyzer/2.0"
        return response

    return app


# Execução local direta via python app.py
if __name__ == "__main__":
    app_instance = create_app()
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 70)
    print("AWS SECURITY ANALYZER v2.0")
    print("Autor: Danilo Rafael da Silva Costa")
    print(f"Server running on http://127.0.0.1:{port}")
    print("=" * 70 + "\n")
    app_instance.run(host="0.0.0.0", port=port, debug=True)