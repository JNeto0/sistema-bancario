from src.conta.Conta import Conta

class ContaPoupanca(Conta):
    def __init__(self, numero, saldo=0.0):
        super().__init__(numero, saldo)

    def render_juros(self, taxa):
        if taxa > 0:
            juros = self.saldo * (taxa / 100)
            self.depositar(juros)
            return True
        return False