from src.conta.Conta import Conta
from src.conta.ContaPoupanca import ContaPoupanca
from src.conta.ContaBonus import ContaBonus

class ContaService:

    def __init__(self, repository):
        self.repository = repository

    def criar_conta(self, numero, saldo_inicial):
        # Validação de 8 dígitos numéricos
        if len(numero) != 8 or not numero.isdigit():
            return "Erro: O número da conta deve ter exatamente 8 dígitos numéricos."

        if self.repository.buscar_por_numero(numero):
            return "Erro: Conta já existe."

        conta = Conta(numero, saldo_inicial)
        self.repository.adicionar(conta)
        return "Conta criada com sucesso!"
    
    def criar_conta_bonus(self, numero):

        conta_existente = self.repository.buscar_por_numero(numero)

        if conta_existente:
            return "Erro: Já existe uma conta com esse número."

        conta = ContaBonus(numero)

        self.repository.adicionar(conta)

        return "Conta bônus criada com sucesso."
    
    def consultar_saldo(self, numero):

        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return None

        return conta.consultar_saldo()

    def consultar_conta(self, numero):
        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return None

        return conta.consultar_dados()
    
    def credito(self, numero, valor):

        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return "Conta não encontrada, verifique o código."

        if valor < 0:
            return "Erro: Valor do crédito deve ser positivo."

        conta.depositar(valor)

        return "Crédito realizado."
    
    def debito(self, numero, valor):
        conta = self.repository.buscar_por_numero(numero)
        if not conta:
            return "Conta não encontrada, verifique o código."

        if valor < 0:
            return "Erro: Valor do débito deve ser positivo."

        if conta.sacar(valor):
            return "Débito realizado com sucesso."
        else:
            return "Erro: Saldo insuficiente."

    def transferencia(self, numero_origem, numero_destino, valor):
        conta_origem = self.repository.buscar_por_numero(numero_origem)
        conta_destino = self.repository.buscar_por_numero(numero_destino)

        if not conta_origem or not conta_destino:
            return "Conta não encontrada, verifique o código."

        if valor < 0:
            return "Erro: Valor da transferência deve ser positivo."
        
        if conta_origem.sacar(valor):

            if hasattr(conta_destino, "receber_transferencia"):
                conta_destino.receber_transferencia(valor)
            else:
                conta_destino.depositar(valor)

            return "Transferência realizada com sucesso."

        else:
            return "Erro: Saldo insuficiente na conta de origem."
        
    def criar_poupanca(self, numero):
        if len(numero) != 8 or not numero.isdigit():
            return "Erro: O número da conta deve ter exatamente 8 dígitos numéricos."
        if self.repository.buscar_por_numero(numero):
            return "Erro: Conta já existe."
        
        conta = ContaPoupanca(numero)
        self.repository.adicionar(conta)
        return "Conta Poupança criada com sucesso!"

    def render_juros_total(self, taxa):
        contas = self.repository.contas
        encontrou_poupanca = False
        for conta in contas:
            if isinstance(conta, ContaPoupanca):
                conta.render_juros(taxa)
                encontrou_poupanca = True
        
        if encontrou_poupanca:
            return f"Juros de {taxa}% aplicados com sucesso."
        else:
            return "Nenhuma conta poupança encontrada."
