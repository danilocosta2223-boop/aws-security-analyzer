"""
AWS Security Analyzer - Security Score Calculator
"""

class SecurityAnalyzer:

    def calculate_score(self, findings: list) -> int:
        """
        Calcula o score de segurança com base nas severidades dos achados.
        """
        deductions = {
            'CRITICAL': 25,
            'HIGH': 15,
            'MEDIUM': 10,
            'LOW': 5
        }
        score = 100
        for f in findings:
            sev = f.get('severity', 'LOW').upper()
            score -= deductions.get(sev, 5)

        return max(0, score)