import psycopg

class DataBaseConexao:
    def __init__(self):
        self.__conexao = psycopg.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='12345',
            dbname='produtos_api',
            autocommit=True
        )
        self.cursor = self.__conexao.cursor()