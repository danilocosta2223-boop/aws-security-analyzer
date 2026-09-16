"""
AWS Security Analyzer - Security Group Check
"""

import boto3


class SecurityGroupCheck:

    def __init__(self, ec2_client=None):
        self.ec2 = ec2_client or boto3.client('ec2')

    def run(self):
        findings = []
        try:
            response = self.ec2.describe_security_groups()
            for sg in response.get('SecurityGroups', []):
                sg_id = sg.get('GroupId')
                sg_name = sg.get('GroupName')

                for permission in sg.get('IpPermissions', []):
                    from_port = permission.get('FromPort')
                    to_port = permission.get('ToPort')
                    ip_ranges = permission.get('IpRanges', [])

                    is_public = any(ip_range.get('CidrIp') == '0.0.0.0/0' for ip_range in ip_ranges)

                    if is_public:
                        # Checagem de SSH (22)
                        if (from_port is None and to_port is None) or (from_port <= 22 <= to_port):
                            findings.append({
                                "severity": "CRITICAL",
                                "title": "Porta SSH (22) aberta para a Internet",
                                "resource": f"{sg_name} ({sg_id})",
                                "description": f"O Security Group {sg_id} permite tráfego de entrada na porta 22 vindo de 0.0.0.0/0.",
                                "remediation": "Restrinja o acesso SSH apenas aos IPs corporativos ou utilize AWS Systems Manager Session Manager."
                            })

                        # Checagem de RDP (3389)
                        if (from_port is None and to_port is None) or (from_port <= 3389 <= to_port):
                            findings.append({
                                "severity": "CRITICAL",
                                "title": "Porta RDP (3389) aberta para a Internet",
                                "resource": f"{sg_name} ({sg_id})",
                                "description": f"O Security Group {sg_id} permite tráfego de entrada na porta 3389 vindo de 0.0.0.0/0.",
                                "remediation": "Remova a regra de entrada para 0.0.0.0/0 e utilize VPN ou Bastion Host."
                            })
        except Exception as e:
            findings.append({
                "severity": "LOW",
                "title": "Erro ao checar Security Groups",
                "resource": "EC2 Service",
                "description": str(e),
                "remediation": "Garanta permissão ec2:DescribeSecurityGroups no IAM Role/User."
            })

        return findings