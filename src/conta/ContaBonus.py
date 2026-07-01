from src.conta.Conta import Conta

class ContaBonus(Conta):

    def __init__(self, numero, saldo=0):
        super().__init__(numero, saldo)
        self.pontuacao = 10

    def depositar(self, valor):
        self.saldo += valor

        pontos = valor // 100
        self.pontuacao += int(pontos)

    def receber_transferencia(self, valor):
        self.saldo += valor

        pontos = valor // 150
        self.pontuacao += int(pontos)

    def consultar_dados(self):
        dados = super().consultar_dados()
        dados["tipo"] = "Conta Bonus"
        dados["bonus"] = self.pontuacao
        return dados
