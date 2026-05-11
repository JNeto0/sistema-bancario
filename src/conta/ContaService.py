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

        if conta.sacar(valor):
            return "Débito realizado com sucesso."
        else:
            return "Erro: Saldo insuficiente."

    def transferencia(self, numero_origem, numero_destino, valor):
        conta_origem = self.repository.buscar_por_numero(numero_origem)
        conta_destino = self.repository.buscar_por_numero(numero_destino)

        if not conta_origem or not conta_destino:
            return "Conta não encontrada, verifique o código."

        if conta_origem.sacar(valor):
            conta_destino.depositar(valor)
            return "Transferência realizada com sucesso."
        else:
            return "Erro: Saldo insuficiente na conta de origem."