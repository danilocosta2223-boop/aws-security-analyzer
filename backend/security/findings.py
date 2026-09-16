"""
AWS Security Analyzer - Findings Engine
Centraliza a execução de todas as verificações de segurança e o histórico.
"""

import os
import json
from datetime import datetime

# Imports seguros para evitar quebra caso algum arquivo de check falte
try:
    from backend.checks.mfa_check import MFACheck
except ImportError:
    MFACheck = None

try:
    from backend.checks.public_bucket_check import PublicBucketCheck
except ImportError:
    PublicBucketCheck = None

try:
    from backend.checks.bucket_encryption_check import BucketEncryptionCheck
except ImportError:
    BucketEncryptionCheck = None

try:
    from backend.checks.security_group_check import SecurityGroupCheck
except ImportError:
    SecurityGroupCheck = None

try:
    from backend.checks.access_key_check import AccessKeyCheck
except ImportError:
    try:
        from backend.checks.access_key_check import AccessKeyAgeCheck as AccessKeyCheck
    except ImportError:
        AccessKeyCheck = None


class FindingsEngine:

    def __init__(self, session=None):
        self.session = session
        self.history_file = os.path.join("backend", "data", "audit_history.json")

    def _get_mfa_findings(self):
        mfa_findings = []
        if MFACheck is None:
            return mfa_findings
        
        try:
            mfa = MFACheck()
            if hasattr(mfa, "session") and self.session:
                mfa.session = self.session

            if hasattr(mfa, "run_check"):
                users = mfa.run_check() or []
            elif hasattr(mfa, "check_mfa"):
                users = mfa.check_mfa() or []
            else:
                users = []

            for user in users:
                if isinstance(user, dict) and "severity" in user:
                    mfa_findings.append(user)
                elif isinstance(user, dict) and not user.get("mfa_enabled", True):
                    username = (
                        user.get("user")
                        or user.get("UserName")
                        or "Usuário Desconhecido"
                    )
                    mfa_findings.append({
                        "severity": "HIGH",
                        "title": "MFA desabilitado no usuário IAM",
                        "description": f"O usuário IAM '{username}' não possui MFA ativado.",
                        "resource": username,
                        "remediation": "Habilite MFA virtual ou físico para a conta IAM."
                    })
        except Exception as e:
            print(f"Erro MFACheck: {e}")
        return mfa_findings

    def _save_audit_history(self, score, findings_count):
        """
        Salva o snapshot da auditoria no arquivo audit_history.json
        """
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            history = []
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    try:
                        history = json.load(f)
                    except json.JSONDecodeError:
                        history = []

            record = {
                "timestamp": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": score,
                "total_findings": findings_count
            }
            history.append(record)
            history = history[-50:]  # Mantém os últimos 50 registros

            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"Erro ao salvar histórico de auditoria: {e}")

    def get_findings(self) -> list:
        """
        Executa todos os checks de segurança de forma resiliente e retorna a lista de achados.
        """
        findings = []

        # 1. MFA Check
        findings.extend(self._get_mfa_findings())

        # 2. Public Bucket Check
        if PublicBucketCheck is not None:
            try:
                pb = PublicBucketCheck()
                if hasattr(pb, "session") and self.session:
                    pb.session = self.session
                findings.extend(pb.run_check())
            except Exception as e:
                print(f"Erro PublicBucketCheck: {e}")

        # 3. Bucket Encryption Check
        if BucketEncryptionCheck is not None:
            try:
                be = BucketEncryptionCheck()
                if hasattr(be, "session") and self.session:
                    be.session = self.session
                findings.extend(be.run_check())
            except Exception as e:
                print(f"Erro BucketEncryptionCheck: {e}")

        # 4. Security Group Check
        if SecurityGroupCheck is not None:
            try:
                sg = SecurityGroupCheck()
                if hasattr(sg, "session") and self.session:
                    sg.session = self.session
                findings.extend(sg.run_check())
            except Exception as e:
                print(f"SecurityGroupCheck: {e}")

        # 5. Access Key Age Check
        if AccessKeyCheck is not None:
            try:
                ak = AccessKeyCheck()
                if hasattr(ak, "session") and self.session:
                    ak.session = self.session
                
                if hasattr(ak, "run"):
                    findings.extend(ak.run())
                elif hasattr(ak, "run_check"):
                    findings.extend(ak.run_check())
            except Exception as e:
                print(f"AccessKeyCheck: {e}")

        return findings

    def get_audit_history(self) -> list:
        """
        Carrega o histórico de auditorias gravado em disco.
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao ler histórico de auditoria: {e}")
        return []