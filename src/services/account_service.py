from ..database.connection import get_db_connection
import random

class AccountService:
    """
    Serviço responsável pela gestão de contas de clientes e funcionários
    """
    def __init__(self):
        self.db = get_db_connection()

    def criar_conta_cliente(self, nome, cpf, data_nascimento, telefone, senha, saldo_inicial=0):
        """Cria uma nova conta de cliente"""
        try:
            cursor = self.db.get_cursor()
            
            # Inserir usuário
            query_usuario = """
                INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
                VALUES (%s, %s, %s, %s, 'CLIENTE', %s)
            """
            cursor.execute(query_usuario, (nome, cpf, data_nascimento, telefone, senha))
            id_usuario = cursor.lastrowid
            
            # Inserir cliente
            query_cliente = """
                INSERT INTO cliente (id_usuario)
                VALUES (%s)
            """
            cursor.execute(query_cliente, (id_usuario,))
            id_cliente = cursor.lastrowid
            
            # Gerar número da conta
            numero_conta = self._gerar_numero_conta()
            
            # Inserir conta
            query_conta = """
                INSERT INTO conta (id_cliente, numero_conta, saldo)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_conta, (id_cliente, numero_conta, saldo_inicial))
            
            self.db.commit()
            return numero_conta
            
        except Exception as e:
            print(f"Erro ao criar conta: {e}")
            self.db.rollback()
            return None

    def criar_funcionario(self, nome, cpf, senha, cargo, codigo_funcionario):
        """Cria um novo funcionário"""
        try:
            cursor = self.db.get_cursor()
            
            # Gerar um OTP inicial
            otp_inicial = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Inserir usuário
            query_usuario = """
                INSERT INTO usuario (nome, cpf, tipo_usuario, senha_hash, otp_ativo)
                VALUES (%s, %s, 'FUNCIONARIO', %s, %s)
            """
            cursor.execute(query_usuario, (nome, cpf, senha, otp_inicial))
            id_usuario = cursor.lastrowid
            
            # Inserir funcionário
            query_funcionario = """
                INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_funcionario, (id_usuario, codigo_funcionario, cargo))
            
            self.db.commit()
            return otp_inicial
            
        except Exception as e:
            print(f"Erro ao criar funcionário: {e}")
            self.db.rollback()
            return None

    def _gerar_numero_conta(self):
        """Gera um número de conta único"""
        return f"{random.randint(10000, 99999)}-{random.randint(0, 9)}"

def get_account_service():
    """Retorna uma instância do serviço de contas"""
    return AccountService()
