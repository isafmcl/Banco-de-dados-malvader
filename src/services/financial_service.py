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

    def consultar_inadimplentes(self):
        """Consulta os clientes inadimplentes"""
        try:
            cursor = self.db.get_cursor()
            query = """
                WITH saldo_atual AS (
                    SELECT 
                        c.id_conta,
                        c.numero_conta,
                        c.saldo,
                        COALESCE(cc.limite, 0) as limite,
                        cli.nome as nome_cliente,
                        u.cpf,
                        CASE 
                            WHEN c.saldo < 0 THEN ABS(c.saldo)
                            ELSE 0 
                        END as valor_inadimplencia,
                        CASE 
                            WHEN c.saldo < 0 THEN 
                                EXTRACT(DAY FROM (CURRENT_DATE - (
                                    SELECT MAX(t.data_hora)::date 
                                    FROM transacao t 
                                    WHERE t.id_conta_origem = c.id_conta 
                                    AND t.valor > 0
                                )))
                            ELSE 0
                        END as dias_inadimplente
                    FROM conta c
                    LEFT JOIN conta_corrente cc ON c.id_conta = cc.id_conta
                    JOIN cliente cli ON c.id_cliente = cli.id_cliente
                    JOIN usuario u ON cli.id_usuario = u.id_usuario
                    WHERE c.status = 'ATIVA'
                )
                SELECT *
                FROM saldo_atual
                WHERE valor_inadimplencia > 0
                ORDER BY dias_inadimplente DESC, valor_inadimplencia DESC;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            inadimplentes = []
            for row in results:
                inadimplentes.append({
                    'numero_conta': row[1],
                    'nome': row[4],
                    'cpf': row[5],
                    'valor_inadimplencia': float(row[6]),
                    'dias_inadimplente': int(row[7]),
                    'limite': float(row[3]),
                    'saldo': float(row[2])
                })
            
            return inadimplentes
            
        except Exception as e:
            print(f"Erro ao consultar inadimplentes: {e}")
            return []

    def consultar_transacoes(self, numero_conta):
        """Consulta as transações de uma conta"""
        try:
            cursor = self.db.get_cursor()
            query = """
                WITH transacoes_completas AS (
                    -- Transações de saída (débitos)
                    SELECT 
                        t.id_transacao,
                        t.data_hora,
                        t.tipo_transacao,
                        t.valor * -1 as valor,
                        t.descricao,
                        cd.numero_conta as conta_destino,
                        cli_d.nome as nome_destino
                    FROM transacao t
                    JOIN conta c ON t.id_conta_origem = c.id_conta
                    LEFT JOIN conta cd ON t.id_conta_destino = cd.id_conta
                    LEFT JOIN cliente cli_d ON cd.id_cliente = cli_d.id_cliente
                    WHERE c.numero_conta = %s
                    
                    UNION ALL
                    
                    -- Transações de entrada (créditos)
                    SELECT 
                        t.id_transacao,
                        t.data_hora,
                        t.tipo_transacao,
                        t.valor,
                        t.descricao,
                        co.numero_conta as conta_origem,
                        cli_o.nome as nome_origem
                    FROM transacao t
                    JOIN conta c ON t.id_conta_destino = c.id_conta
                    LEFT JOIN conta co ON t.id_conta_origem = co.id_conta
                    LEFT JOIN cliente cli_o ON co.id_cliente = cli_o.id_cliente
                    WHERE c.numero_conta = %s
                )
                SELECT 
                    id_transacao,
                    data_hora,
                    tipo_transacao,
                    valor,
                    descricao,
                    CASE 
                        WHEN tipo_transacao = 'TRANSFERENCIA_ENTRADA' THEN conta_destino
                        WHEN tipo_transacao = 'TRANSFERENCIA_SAIDA' THEN conta_origem
                        ELSE NULL
                    END as conta_relacionada,
                    CASE 
                        WHEN tipo_transacao = 'TRANSFERENCIA_ENTRADA' THEN nome_destino
                        WHEN tipo_transacao = 'TRANSFERENCIA_SAIDA' THEN nome_origem
                        ELSE NULL
                    END as nome_relacionado
                FROM transacoes_completas
                ORDER BY data_hora DESC
            """
            cursor.execute(query, (numero_conta, numero_conta))
            results = cursor.fetchall()
            
            transacoes = []
            for row in results:
                transacao = {
                    'id': row[0],
                    'data_hora': row[1].isoformat(),
                    'tipo': row[2],
                    'valor': float(row[3]),
                    'descricao': row[4],
                    'conta_relacionada': row[5],
                    'nome_relacionado': row[6]
                }
                transacoes.append(transacao)
                
            return transacoes
            
        except Exception as e:
            print(f"Erro ao consultar transações: {e}")
            return []

def get_financial_service():
    """Retorna uma instância do serviço financeiro"""
    return FinancialService()
