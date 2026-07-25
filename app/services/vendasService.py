from app.models.vendas import Vendas
from app.repository.SalesRepository import SalesRepository


class VendasService:
    """Serviço da classe vendas.
    
    Esse serviço é reponsável por executar ações e validações do usuário,
    através da comunicação entre o repositorio e a classe Vendas.
    """

    def __init__(self, repository=None):
        self.repository = repository or SalesRepository()


    def create_sales(self, price, pay_method, sales_dt):
        """
        Coleta os dados passados e cria uma instancia de vendas
        a ser registrado no repositorio.

        Args:
            price (float):
                Valor da venda.
            pay_method (string):
              Forma de pagamento registrada.
            sales_dt (string):
                Data em que foi realizada a venda.
        """

        sales = Vendas(price, pay_method, sales_dt)
        self.repository.register_sale(sales.price, sales.pay_method, sales.sales_dt)
        return sales


    def get_sales(self, start_dt=None, end_dt=None):
        """
        Coleta todos os dados da tabela sales.


        Retorna todas os dados do perido caso seja informado algum argumento.
        Args:
            start_dt (str):
                Data inicial da busca.
            end_dt (str):
                Data final da busca
            

        Permite coletar as vendas do banco, sendo possivel a coleta por período
        através dos argumentos .

        Caso os argumentos
        """

        # Coleta todos as vendas do repositorio sales.
        self.dados = self.repository.read_sales()

        # Verifica se a data de inicio e fim foram preenchidas.
        if start_dt and end_dt:
            # Coleta todas as vendas entre as datas selecionadas.
            self.dados = self.repository.read_sales(start_dt, end_dt)
            

        # Soma as vendas por forma de pagamento.
        self.resumo = self.dados.groupby(self.dados['pay_method'])['price'].sum().reset_index()

        self.dados = self.dados.to_dict(orient='records')

        self.resumo = self.resumo.to_dict(orient='records')

        return self.dados, self.resumo