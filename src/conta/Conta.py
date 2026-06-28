class Conta:

    def __init__(self, numero, saldo):
        self.numero = numero
        self.saldo = saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        else:
            return False
        
    def sacar(self, valor):
        # Correção Issue #17: Adicionada verificação de saldo suficiente
        if self.saldo - valor >= self.limite_negativo():
            self.saldo -= valor
            return True
        else:
            return False
               
    def consultar_saldo(self):
        return self.saldo
    
    def limite_negativo(self):
        return -1000


        

