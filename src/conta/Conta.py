class Conta:

    def __init__(self, numero, saldo=0.0):
        self.numero = numero
        self.saldo = saldo

    def depositar(self, valor):
        if valor < 0:
            self.saldo += valor
            return True
        else:
            return False
        
    def sacar(self, valor):
        if valor > 0 :
            self.saldo -= valor
            return True
        else:
            return False
        
    def consultar_saldo(self):
        return self.saldo


        

