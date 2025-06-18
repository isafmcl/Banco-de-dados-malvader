from ..database.connection import get_db_connection

class StatisticsService:
    """
    Serviço responsável por estatísticas e utilitários do banco
    """
    def __init__(self):
        self.db = get_db_connection()

    def obter_estatisticas_banco(self):
        """Retorna estatísticas gerais do banco para funcionários"""
        try:
            cursor = self.db.get_cursor()
            stats = {}
            
            # Total de clientes
            cursor.execute("SELECT COUNT(*) FROM cliente")
            stats['total_clientes'] = cursor.fetchone()[0]
            
            # Contas ativas
            cursor.execute("SELECT COUNT(*) FROM conta")
            stats['contas_ativas'] = cursor.fetchone()[0]
            
            # Transações hoje
            cursor.execute("SELECT COUNT(*) FROM transacao WHERE DATE(data_transacao) = CURDATE()")
            stats['transacoes_hoje'] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {
                'total_clientes': 0,
                'contas_ativas': 0,
                'transacoes_hoje': 0
            }

def get_statistics_service():
    """Retorna uma instância do serviço de estatísticas"""
    return StatisticsService()
