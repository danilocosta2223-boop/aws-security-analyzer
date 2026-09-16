# services/notification_service.py

class NotificationService:
    def __init__(self):
        # Mapeamento de emojis / prefixos visuais por severidade
        self.severity_icons = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "⚡",
            "LOW": "ℹ️"
        }

    def build_alert(self, finding: dict) -> dict:
        """
        Formata um achado individual em um objeto de alerta pronto para exibição.
        """
        severity = finding.get("severity", "LOW").upper()
        icon = self.severity_icons.get(severity, "ℹ️")
        title = finding.get("title", "Alerta Sem Título")
        resource = finding.get("resource", "Recurso Não Especificado")

        return {
            "severity": severity,
            "icon": icon,
            "message": f"{icon} [{severity}] {title}",
            "detail": f"Recurso afetado: {resource}",
            "timestamp": finding.get("timestamp")
        }

    def get_all_alerts(self, findings: list) -> list:
        """
        Processa uma lista de achados e retorna alertas ordenados por severidade.
        """
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        
        alerts = [self.build_alert(f) for f in findings]
        
        # Ordena para garantir que o que for CRITICAL e HIGH apareça no topo
        alerts.sort(key=lambda x: severity_order.get(x["severity"], 4))
        return alerts