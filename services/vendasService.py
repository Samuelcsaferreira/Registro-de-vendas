from models.vendas import Vendas
from repository.vendasRepository import VendasRepository


class VendasService:
    """Classe de Serviço para vendas. Responsável por instanciar
    a classe Vendas e Registrar suas informações no banco através
    da clase de VendasRepository"""

    def __init__(self, repository=None):
        self.dados = None
        self.repository = repository or VendasRepository()

    def registrar_venda(self, valor, pagamento, data):
        registro = Vendas(valor, pagamento, data)
        self.repository.criar_venda(registro.valor, registro.pagamento, registro.data)
        return registro

    def mostrar_registros(self, data_inicio=None, data_final=None):
        self.dados = self.repository.ler_registros()
        return self.dados

    def deletar_dado(self, venda_id):
        self.id = venda_id
        self.repository.deletar_registro(self.id)
        return "Dado deletado"

    def exibir_soma(self, forma_pagamento):
        self.forma_pagamento = self.repository.somar_vendas(forma_pagamento)
        soma = self.forma_pagamento[0]
        if soma is None:
            soma = float(0)
        return soma
