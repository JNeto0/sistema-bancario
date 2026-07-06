from src.conta.Conta import Conta
from src.conta.ContaPoupanca import ContaPoupanca
from src.conta.ContaBonus import ContaBonus
from src.conta.ResultadoService import ResultadoService


class ContaService:

    def __init__(self, repository):
        self.repository = repository

    def _sucesso(self, mensagem, dados=None):
        return ResultadoService(True, mensagem, dados=dados)

    def _erro(self, mensagem, codigo):
        return ResultadoService(False, mensagem, erro=codigo)

    def _numero_invalido(self, numero):
        return len(numero) != 8 or not numero.isdigit()

    def _dados_conta(self, conta):
        dados = {
            "tipo": "Conta Simples",
            "numero": conta.numero,
            "saldo": conta.consultar_saldo(),
        }

        if isinstance(conta, ContaPoupanca):
            dados["tipo"] = "Conta Poupanca"

        if isinstance(conta, ContaBonus):
            dados["tipo"] = "Conta Bonus"
            dados["bonus"] = conta.pontuacao

        return dados

    def criar_conta(self, numero, saldo_inicial):
        if self._numero_invalido(numero):
            return self._erro(
                "Erro: O numero da conta deve ter exatamente 8 digitos numericos.",
                "NUMERO_CONTA_INVALIDO",
            )

        if self.repository.buscar_por_numero(numero):
            return self._erro("Erro: Conta ja existe.", "CONTA_JA_EXISTE")

        conta = Conta(numero, saldo_inicial)
        self.repository.adicionar(conta)
        return self._sucesso("Conta criada com sucesso!", self._dados_conta(conta))

    def criar_conta_bonus(self, numero):
        if self._numero_invalido(numero):
            return self._erro(
                "Erro: O numero da conta deve ter exatamente 8 digitos numericos.",
                "NUMERO_CONTA_INVALIDO",
            )

        conta_existente = self.repository.buscar_por_numero(numero)

        if conta_existente:
            return self._erro("Erro: Ja existe uma conta com esse numero.", "CONTA_JA_EXISTE")

        conta = ContaBonus(numero)
        self.repository.adicionar(conta)

        return self._sucesso("Conta bonus criada com sucesso.", self._dados_conta(conta))

    def consultar_saldo(self, numero):
        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return self._erro("Conta nao encontrada.", "CONTA_NAO_ENCONTRADA")

        return self._sucesso(
            "Saldo consultado com sucesso.",
            {"numero": conta.numero, "saldo": conta.consultar_saldo()},
        )

    def consultar_conta(self, numero):
        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return self._erro("Conta nao encontrada.", "CONTA_NAO_ENCONTRADA")

        return self._sucesso("Conta consultada com sucesso.", self._dados_conta(conta))

    def credito(self, numero, valor):
        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return self._erro(
                "Conta nao encontrada, verifique o codigo.",
                "CONTA_NAO_ENCONTRADA",
            )

        if valor < 0:
            return self._erro("Erro: Valor do credito deve ser positivo.", "VALOR_INVALIDO")

        conta.depositar(valor)

        return self._sucesso("Credito realizado.", self._dados_conta(conta))

    def debito(self, numero, valor):
        conta = self.repository.buscar_por_numero(numero)

        if not conta:
            return self._erro(
                "Conta nao encontrada, verifique o codigo.",
                "CONTA_NAO_ENCONTRADA",
            )

        if valor < 0:
            return self._erro("Erro: Valor do debito deve ser positivo.", "VALOR_INVALIDO")

        if conta.sacar(valor):
            return self._sucesso("Debito realizado com sucesso.", self._dados_conta(conta))

        return self._erro("Erro: Saldo insuficiente.", "SALDO_INSUFICIENTE")

    def transferencia(self, numero_origem, numero_destino, valor):
        conta_origem = self.repository.buscar_por_numero(numero_origem)
        conta_destino = self.repository.buscar_por_numero(numero_destino)

        if not conta_origem or not conta_destino:
            return self._erro(
                "Conta nao encontrada, verifique o codigo.",
                "CONTA_NAO_ENCONTRADA",
            )

        if valor < 0:
            return self._erro("Erro: Valor da transferencia deve ser positivo.", "VALOR_INVALIDO")

        if conta_origem.sacar(valor):
            if hasattr(conta_destino, "receber_transferencia"):
                conta_destino.receber_transferencia(valor+10)
            else:
                conta_destino.depositar(valor + 10)

            return self._sucesso(
                "Transferencia realizada com sucesso.",
                {
                    "origem": self._dados_conta(conta_origem),
                    "destino": self._dados_conta(conta_destino),
                },
            )

        return self._erro(
            "Erro: Saldo insuficiente na conta de origem.",
            "SALDO_INSUFICIENTE",
        )

    def criar_poupanca(self, numero, saldo_inicial):
        if self._numero_invalido(numero):
            return self._erro(
                "Erro: O numero da conta deve ter exatamente 8 digitos numericos.",
                "NUMERO_CONTA_INVALIDO",
            )

        if self.repository.buscar_por_numero(numero):
            return self._erro("Erro: Conta ja existe.", "CONTA_JA_EXISTE")

        conta = ContaPoupanca(numero, saldo_inicial)
        self.repository.adicionar(conta)

        return self._sucesso("Conta Poupanca criada com sucesso!", self._dados_conta(conta))

    def render_juros_total(self, taxa):
        contas = self.repository.listar_todas()
        poupancas = []

        for conta in contas:
            if isinstance(conta, ContaPoupanca):
                conta.render_juros(taxa)
                poupancas.append(self._dados_conta(conta))

        if poupancas:
            return self._sucesso(
                f"Juros de {taxa}% aplicados com sucesso.",
                {"contas": poupancas},
            )

        return self._erro(
            "Nenhuma conta poupanca encontrada.",
            "NENHUMA_POUPANCA_ENCONTRADA",
        )
