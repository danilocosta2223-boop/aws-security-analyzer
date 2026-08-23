import boto3
from botocore.exceptions import BotoCoreError, ClientError

def testar_conexao_aws():
    """Valida as credenciais atuais da AWS utilizando o serviço STS."""
    print("🔄 Conectando à AWS...")
    
    try:
        # Inicializa o client do STS (Security Token Service)
        sts = boto3.client("sts")

        # Obtém a identidade associada às credenciais ativas
        identity = sts.get_caller_identity()

        print("\n✅ Conectado com sucesso!\n")
        print(f"• **Account ID:** {identity.get('Account')}")
        print(f"• **User/Role ARN:** {identity.get('Arn')}")
        print(f"• **User ID:** {identity.get('UserId')}")

    except (BotoCoreError, ClientError) as e:
        print("\n❌ Erro de conexão ou credenciais inválidas na AWS:")
        print(f"Detalhes: {e}")
    except Exception as e:
        print(f"\n⚠️ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    testar_conexao_aws()