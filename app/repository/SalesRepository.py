# =======================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =======================================
# Bibliotecas externas
from sqlalchemy import create_engine, text
import pandas as pd

# Bibliotecas internas
from app.settings import DATABASE_URL


# =======================================
# DEFINIÇÃO DE CLASSES
# =======================================
class SalesRepository:
    """
    Repositório responsável pela persistência dos dados de vendas.

    Centraliza as operações de acesso ao banco de dados, incluindo
    criação da tabela e manipulação dos registros.
    
    Attributes:
        connection (psycopg2.extensions.connection):
            Conexão ativa com o banco de dados PostgreSQL.
    """

    def __init__(self, database: str = DATABASE_URL) -> None:
        self.engine = create_engine(database, pool_size=10, max_overflow=20)
        # self.connection: psycopg2.extensions.connection = (
        #     psycopg2.connect(database)
        # )
        self._create_table()


    def _create_table(self) -> None:
        """
        Cria a tabela principal da aplicação no banco de dados, caso ainda não exista.

        A função executa um comando SQL utilizando `CREATE TABLE IF NOT EXISTS`,
        garantindo que a estrutura necessária para o armazenamento dos registros
        seja criada apenas na primeira execução da aplicação.

        Estrutura da tabela:
        - id (SERIAL): Identificador único do registro.
        - price (NUMERIC (10, 2)): Valor monetário registrado.
        - pay_method (VARCHAR): Forma de pagamento registrada.
        - sales_dt (DATE): Data em que a venda foi realizada.
        - created_at (TIMESTAMP): Data e hora em que foi criado.
        """

        # Comando SQL.
        sql ="""
            CREATE TABLE IF NOT EXISTS sales(
                id SERIAL PRIMARY KEY,
                price NUMERIC(10,2) NOT NULL,
                pay_method VARCHAR(20),
                sales_dt DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        # Cria a tabela, caso ela ainda não exista.
        with self.engine.connect() as con:
            con.execute(text(sql))
            con.commit()


    def register_sale(self, price: float, pay_method: str, sales_dt) -> None:
        """
        Insere os dados na tabela do banco de dados.
            Args:
            - price (float)
            - pay_method(str)
            - date (str)
        """

        # Comando SQL.
        sql = """
            INSERT INTO sales (price, pay_method, sales_dt)
                VALUES (:price, :pay_method, :sales_dt)"""
        
        # Rregistra uma venda no banco de dados.
        with self.engine.connect() as con:
            con.execute(text(sql), {"price": price, "pay_method": pay_method, "sales_dt": sales_dt})
            con.commit()


    def read_sales(self, start_date: str = None, end_date: str = None):
        """Executa a leitura da tabela de vendas e retorna os dados do banco em uma DataFrame (Pandas)
        """

        # Comando SQL.
        sql="""
            SELECT price, pay_method, sales_dt 
                FROM sales
            """
        
        # Faz a leitura de todos os dados da tabela.
        with self.engine.connect() as con:
            sales = pd.read_sql(text(sql), con=con)

            # Formata a coluna da data da venda para string.
            sales['sales_dt'] = pd.to_datetime(sales['sales_dt']).dt.strftime('%d/%m/%Y')
        
        # Verifica se foi repassado a data de inicio e fim do periodo.
        if start_date and end_date:
            sql = """
                SELECT price, pay_method, sales_dt 
                    FROM sales
                    WHERE sales_dt BETWEEN :start AND :end
                """
            # Faz a leitura dos dados dentro da data selecionada.
            with self.engine.connect() as con:
                sales = pd.read_sql(text(sql), params={"start": start_date, "end": end_date}, con=con)

                # Formata a coluna da data da venda para string.
                sales['sales_dt'] = pd.to_datetime(sales['sales_dt']).dt.strftime('%d/%m/%Y')
                

        return sales