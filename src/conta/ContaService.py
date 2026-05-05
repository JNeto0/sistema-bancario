from src.conta.Conta import Conta

class ContaService:

    def __init__(self, repository):
        self.repository = repository

    def criar_conta(self, numero):
        # verifica se já existe
        if self.repository.buscar_por_numero(numero):
            return None

        conta = Conta(numero)
        self.repository.adicionar(conta)
        return conta
    
    def consultar_saldo(self, numero):

        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return None

        return conta.consultar_saldo()
    
    def credito(self, numero, valor):

        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return "Conta não encontrada, verifique o código."

        conta.depositar(valor)

        return "Crédito realizado."
    
    def debito(self, numero, valor):

        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return "Conta não encontrada, verifique o código."

        conta.sacar(valor)

        return "Débito realizado com sucesso."
    
    