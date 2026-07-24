# =======================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =======================================
# Bibliotecas padrão
from datetime import datetime
import json

# Bibliotecas externas
import psycopg2

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
        self.connection: psycopg2.extensions.connection = (
            psycopg2.connect(database)
        )
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
        
        with self.connection as con:
            cur = con.cursor()

            # Cria a tabela caso ela ainda não exista.
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sales(
                    id SERIAL PRIMARY KEY,
                    price NUMERIC(10,2) NOT NULL,
                    pay_method VARCHAR(20),
                    sales_dt DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)


    # Registra uma venda no bano de dados.
    def register_sale(self, price: float, pay_method: str, date: str):
        """
        Insere dados dentro do banco de dados.

        **`INSERT INTO...`:**
        - dasda
        """
        with self.connection as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO vendas_table (price, pay_method, sales_dt)
                    VALUES (%s, %s, %s)""",
                (price, pay_method, date),
            )
            return cur.lastrowid

    def ler_registros(self):
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "SELECT id, valor, form_pgt, vd_date FROM vendas_table")
            coluna = [descricao[0] for descricao in cur.description]
            dados = cur.fetchall()

            dados_json = [dict(zip(coluna, linha)) for linha in dados]
            # transformar coluna vd_date em string
            dados_json = [
                {**linha, "vd_date": linha["vd_date"].strftime("%d-%m-%y")}
                for linha in dados_json
            ]

            with open("dados_json.json", "w", encoding="utf-8") as arquivo_json:
                json.dump(dados_json, arquivo_json,
                          indent=4, ensure_ascii=False)
            return dados_json

    def selecioar_dados_periodo(self, data_inicio, data_final):
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "SELECT id, valor, form_pgt, vd_date FROM vendas_table WHERE vd_date BETWEEN %s AND %s",
                (data_inicio, data_final),
            )

            dados = cur.fetchall()
            return dados

    def atualizar_venda(self, id, valor, pagamento, data):
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE vendas_table SET valor = %s, form_pgt = %s, vd_date = %s WHERE id = %s",
                (valor, pagamento, data, id),
            )
            return cur.rowcount

    def deletar_registro(self, venda_id):
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "DELETE FROM vendas_table WHERE id = %s",
                (venda_id,))
            return cur.rowcount


    def somar_vendas(self, forma_pagamento):
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "SELECT SUM(valor) FROM vendas_table WHERE form_pgt = %s",
                (forma_pagamento,),
            )

            dados = cur.fetchone()
            return dados