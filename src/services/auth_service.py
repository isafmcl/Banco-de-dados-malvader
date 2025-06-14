from ..database.connection import get_db_connection
import random

class AuthService:
    """
    Serviço responsável pela autenticação de clientes e funcionários
    """
    def __init__(self):
        self.db = get_db_connection()

    def autenticar_cliente(self, cpf, senha):
        """Autentica um cliente no sistema"""
        try:
            cursor = self.db.get_cursor()
            
            query = """
                SELECT u.nome, u.cpf, c.id_cliente, co.numero_conta, co.saldo, 
                       COALESCE(cc.limite, 0) as limite
                FROM usuario u
                JOIN cliente c ON u.id_usuario = c.id_usuario
                JOIN conta co ON c.id_cliente = co.id_cliente
                LEFT JOIN conta_corrente cc ON co.id_conta = cc.id_conta
                WHERE u.cpf = %s AND u.senha_hash = %s AND u.tipo_usuario = 'CLIENTE'
            """
            
            cursor.execute(query, (cpf, senha))
            result = cursor.fetchone()
            
            if result:
                return {
                    'nome': result[0],
                    'cpf': result[1],
                    'id_cliente': result[2],
                    'numero_conta': result[3],
                    'saldo': float(result[4]),
                    'limite': float(result[5])
                }
            return None
                
        except Exception as e:
            print(f"Erro na autenticação do cliente: {e}")
            return None

    def autenticar_funcionario(self, cpf, senha, otp):
        """Autentica um funcionário no sistema"""
        try:
            cursor = self.db.get_cursor()
            
            query = """
                SELECT u.nome, u.cpf, f.codigo_funcionario, f.cargo
                FROM usuario u
                JOIN funcionario f ON u.id_usuario = f.id_usuario
                WHERE u.cpf = %s 
                AND u.senha_hash = %s 
                AND u.otp_ativo = %s
                AND u.tipo_usuario = 'FUNCIONARIO'
            """
            cursor.execute(query, (cpf, senha, otp))
            result = cursor.fetchone()
            
            if result:
                return {
                    'nome': result[0],
                    'cpf': result[1],
                    'codigo_funcionario': result[2],
                    'cargo': result[3]
                }
            return None
                
        except Exception as e:
            print(f"Erro na autenticação do funcionário: {e}")
            return None

    def consultar_otp_funcionario(self, cpf):
        """Consulta o OTP atual de um funcionário"""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT u.otp_ativo
                FROM usuario u
                WHERE u.cpf = %s AND u.tipo_usuario = 'FUNCIONARIO'
            """
            cursor.execute(query, (cpf,))
            result = cursor.fetchone()
            
            return result[0] if result else None
                
        except Exception as e:
            print(f"Erro ao consultar OTP: {e}")
            return None

def get_auth_service():
    """Retorna uma instância do serviço de autenticação"""
    return AuthService()
