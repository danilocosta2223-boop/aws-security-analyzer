from enum import Enum

class Severity(Enum):
    """
    Enumeração para classificar a severidade das falhas de segurança
    e definir o peso de desconto no Score Geral de Segurança.
    """
    CRITICAL = 15
    HIGH = 10
    MEDIUM = 5
    LOW = 2