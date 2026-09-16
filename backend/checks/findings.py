"""
backend/security/findings.py
"""

from backend.checks.mfa_check import MFACheck
from backend.checks.security_group_check import SecurityGroupCheck
from backend.checks.bucket_encryption_check import BucketEncryptionCheck
from backend.checks.access_key_check import AccessKeyAgeCheck


class FindingsEngine:

    def __init__(self, session=None):
        self.session = session

    def get_findings(self):
        all_findings = []

        # 1. Verificação de MFA
        try:
            # Tenta instanciar com session; se falhar, tenta sem parâmetros
            try:
                mfa = MFACheck(session=self.session)
            except TypeError:
                mfa = MFACheck()
                if hasattr(mfa, "session") and self.session:
                    mfa.session = self.session

            if hasattr(mfa, "check_mfa"):
                users = mfa.check_mfa() or []
            elif hasattr(mfa, "run_check"):
                users = mfa.run_check() or []
            else:
                users = []

            for user in users:
                if isinstance(user, dict) and "severity" in user:
                    all_findings.append(user)
                elif isinstance(user, dict) and not user.get("mfa_enabled", True):
                    username = (
                        user.get("user")
                        or user.get("UserName")
                        or "Usuário Desconhecido"
                    )
                    all_findings.append({
                        "severity": "HIGH",
                        "title": "MFA desabilitado",
                        "description": f"O usuário IAM '{username}' não possui MFA ativado.",
                        "resource": username,
                        "remediation": "Habilite MFA para todas as contas de usuário IAM com acesso ao console ou API."
                    })
        except Exception as e:
            print(f"Erro ao executar MFACheck: {e}")

        # 2. Security Groups (SSH e RDP abertos para 0.0.0.0/0)
        try:
            sg_check = SecurityGroupCheck(session=self.session)
            all_findings.extend(sg_check.run_check())
        except Exception as e:
            print(f"Erro ao executar SecurityGroupCheck: {e}")

        # 3. Criptografia de Buckets S3
        try:
            encryption_check = BucketEncryptionCheck(session=self.session)
            all_findings.extend(encryption_check.run_check())
        except Exception as e:
            print(f"Erro ao executar BucketEncryptionCheck: {e}")

        # 4. Rotação de Access Keys (> 90 dias)
        try:
            key_check = AccessKeyAgeCheck(session=self.session)
            all_findings.extend(key_check.run_check())
        except Exception as e:
            print(f"Erro ao executar AccessKeyAgeCheck: {e}")

        return all_findings