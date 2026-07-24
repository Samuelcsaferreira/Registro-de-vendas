class Vendas:
    """
    Representa uma venda cadastrada no sistema.
    
    Responsável por cada registro e seus dados registrados no sistema.

    Atributos:
        Valor (float): preço da venda.
        forma_pgt (str): Forma de pagamento.
        venda_dt (str): Data da venda.
    """
    def __init__(self, valor: int, pagamento: str, data: str):
        self.valor = valor
        self.pagamento = pagamento
        self.venda_dt = data
        