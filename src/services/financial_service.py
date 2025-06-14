from ..database.connection import get_db_connection

class FinancialService:
    """
    Serviço responsável pelas operações financeiras do banco
    """
    def __init__(self):
        self.db = get_db_connection()

    def consultar_saldo(self, cpf):
        """Consulta o saldo de um cliente"""
        try:
            cursor = self.db.get_cursor()
            query = """
                SELECT co.saldo
                FROM conta co
                JOIN cliente c ON co.id_cliente = c.id_cliente
                JOIN usuario u ON c.id_usuario = u.id_usuario
                WHERE u.cpf = %s
            """
            cursor.execute(query, (cpf,))
            result = cursor.fetchone()
            return float(result[0]) if result else 0.0
        except Exception as e:
            print(f"Erro ao consultar saldo: {e}")
            return 0.0

    def realizar_deposito(self, numero_conta, valor):
        """Realiza um depósito na conta"""
        try:
            cursor = self.db.get_cursor()
            query = """
                INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
                SELECT id_conta, 'DEPOSITO', %s, 'Depósito via internet banking'
                FROM conta WHERE numero_conta = %s
            """
            cursor.execute(query, (valor, numero_conta))
            self.db.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao realizar depósito: {e}")
            self.db.rollback()
            return False

    def realizar_saque(self, numero_conta, valor):
        """Realiza um saque da conta"""
        try:
            cursor = self.db.get_cursor()
            query_saldo = """
                SELECT c.saldo, COALESCE(cc.limite, 0) as limite
                FROM conta c
                LEFT JOIN conta_corrente cc ON c.id_conta = cc.id_conta
                WHERE c.numero_conta = %s
            """
            cursor.execute(query_saldo, (numero_conta,))
            result = cursor.fetchone()
            
            if result:
                saldo_atual = float(result[0])
                limite = float(result[1])
                saldo_disponivel = saldo_atual + limite
                
                if valor <= saldo_disponivel:
                    query = """
                        INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
                        SELECT id_conta, 'SAQUE', %s, 'Saque via internet banking'
                        FROM conta WHERE numero_conta = %s
                    """
                    cursor.execute(query, (valor, numero_conta))
                    self.db.commit()
                    return True
                else:
                    print("Saldo insuficiente para o saque")
                    return False
            return False
            
        except Exception as e:
            print(f"Erro ao realizar saque: {e}")
            self.db.rollback()
            return False

    def realizar_transferencia(self, conta_origem, conta_destino, valor, descricao="Transferência"):
        """Realiza transferência entre contas"""
        try:
            cursor = self.db.get_cursor()
            
            # Verificar se conta destino existe
            cursor.execute("SELECT id_conta FROM conta WHERE numero_conta = %s", (conta_destino,))
            if not cursor.fetchone():
                print("Conta destino não encontrada")
                return False

            # Verificar saldo da conta origem
            query_saldo = """
                SELECT c.saldo, COALESCE(cc.limite, 0) as limite
                FROM conta c
                LEFT JOIN conta_corrente cc ON c.id_conta = cc.id_conta
                WHERE c.numero_conta = %s
            """
            cursor.execute(query_saldo, (conta_origem,))
            result = cursor.fetchone()
            
            if result:
                saldo_atual = float(result[0])
                limite = float(result[1])
                saldo_disponivel = saldo_atual + limite
                
                if valor <= saldo_disponivel:
                    # Debitar da conta origem
                    query_debito = """
                        INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
                        SELECT id_conta, 'TRANSFERENCIA_SAIDA', %s, %s
                        FROM conta WHERE numero_conta = %s
                    """
                    cursor.execute(query_debito, (valor, descricao, conta_origem))
                    
                    # Creditar na conta destino
                    query_credito = """
                        INSERT INTO transacao (id_conta_destino, tipo_transacao, valor, descricao)
                        SELECT id_conta, 'TRANSFERENCIA_ENTRADA', %s, %s
                        FROM conta WHERE numero_conta = %s
                    """
                    cursor.execute(query_credito, (valor, descricao, conta_destino))
                    
                    self.db.commit()
                    return True
                else:
                    print("Saldo insuficiente para transferência")
                    return False
            return False
            
        except Exception as e:
            print(f"Erro ao realizar transferência: {e}")
            self.db.rollback()
            return False

def get_financial_service():
    """Retorna uma instância do serviço financeiro"""
    return FinancialService()
