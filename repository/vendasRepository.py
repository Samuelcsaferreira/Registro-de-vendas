import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime
import json

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class VendasRepository:
    def __init__(self, database=DATABASE_URL):
        self.connection = psycopg2.connect(database)
        self._criar_tabela()

    def _criar_tabela(self):
        with self.connection as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vendas_table(
                    id SERIAL PRIMARY KEY,
                    valor FLOAT NOT NULL,
                    form_pgt VARCHAR(20),
                    vd_date DATE,
                    rg_date TIMESTAMP)
            """)

    def criar_venda(self, valor, formpgt, data):
        agora = datetime.now()
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO vendas_table (valor, form_pgt, vd_date, rg_date) VALUES (%s, %s, %s, %s)",
                (valor, formpgt, data, agora),
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

#%%
    def somar_vendas(self, forma_pagamento):
        with self.connection as con:
            cur = con.cursor()
            cur.execute(
                "SELECT SUM(valor) FROM vendas_table WHERE form_pgt = %s",
                (forma_pagamento,),
            )

            dados = cur.fetchone()
            return dados


#%%