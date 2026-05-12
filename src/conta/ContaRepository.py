class ContaRepository:

    def __init__(self):
        self.contas = []

    def adicionar(self, conta):
        self.contas.append(conta)

    def buscar_por_numero(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None