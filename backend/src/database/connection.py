import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Gerenciador de conexão com o banco de dados MySQL
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance

    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="banco_malvader",
                user="root",
                password="Isinha009*"
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conexão com MySQL estabelecida com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            self.connection = None
            self.cursor = None

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão fechada com sucesso!")

    def get_cursor(self):
        """Retorna o cursor para executar queries"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.cursor

    def commit(self):
        """Confirma as alterações no banco de dados"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Desfaz as alterações no banco de dados"""
        if self.connection:
            self.connection.rollback()

    def __del__(self):
        """Destrutor - fecha conexão automaticamente"""
        self.close()

def get_db_connection():
    """Retorna uma instância única da conexão com o banco de dados"""
    return DatabaseConnection()
