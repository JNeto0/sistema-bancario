from src.conta.ContaRepository import ContaRepository
from src.conta.ContaService import ContaService
from src.conta.ResultadoService import ResultadoService


class ContaController:
    def __init__(self, service=None):
        if service is None:
            repository = ContaRepository()
            service = ContaService(repository)

        self.service = service

    def _erro(self, mensagem, codigo):
        return ResultadoService(False, mensagem, erro=codigo)

    def _texto(self, payload, campo, erro_codigo):
        valor = payload.get(campo)

        if valor is None:
            return None, self._erro(f"Campo obrigatorio ausente: {campo}.", erro_codigo)

        texto = str(valor).strip()
        if not texto:
            return None, self._erro(f"Campo obrigatorio ausente: {campo}.", erro_codigo)

        return texto, None

    def _numero(self, payload, campo="numero"):
        return self._texto(payload, campo, "CAMPO_OBRIGATORIO")

    def _valor(self, payload, campo="valor"):
        valor = payload.get(campo)
        if valor is None:
            return None, self._erro(f"Campo obrigatorio ausente: {campo}.", "CAMPO_OBRIGATORIO")

        try:
            return float(valor), None
        except (TypeError, ValueError):
            return None, self._erro(f"Campo invalido: {campo}.", "VALOR_INVALIDO")

    def _saldo_inicial(self, payload):
        if "saldo_inicial" not in payload:
            return None, self._erro(
                "Campo obrigatorio ausente: saldo_inicial.",
                "CAMPO_OBRIGATORIO",
            )

        try:
            return float(payload["saldo_inicial"]), None
        except (TypeError, ValueError):
            return None, self._erro("Campo invalido: saldo_inicial.", "VALOR_INVALIDO")

    def criar_conta(self, payload):
        numero, erro = self._numero(payload)
        if erro:
            return erro

        tipo = str(payload.get("tipo", "simples")).strip().lower()

        if tipo in ("simples", "comum", "conta_simples"):
            saldo_inicial, erro = self._saldo_inicial(payload)
            if erro:
                return erro
            return self.service.criar_conta(numero, saldo_inicial)

        if tipo in ("poupanca", "poupança", "conta_poupanca"):
            saldo_inicial, erro = self._saldo_inicial(payload)
            if erro:
                return erro
            return self.service.criar_poupanca(numero, saldo_inicial)

        if tipo in ("bonus", "bônus", "conta_bonus"):
            return self.service.criar_conta_bonus(numero)

        return self._erro("Tipo de conta invalido.", "TIPO_CONTA_INVALIDO")

    def consultar_conta(self, numero):
        return self.service.consultar_conta(numero)

    def consultar_saldo(self, numero):
        return self.service.consultar_saldo(numero)

    def credito(self, numero, payload):
        valor, erro = self._valor(payload)
        if erro:
            return erro

        return self.service.credito(numero, valor)

    def debito(self, numero, payload):
        valor, erro = self._valor(payload)
        if erro:
            return erro

        return self.service.debito(numero, valor)

    def transferencia(self, payload):
        numero_origem, erro = self._texto(payload, "origem", "CAMPO_OBRIGATORIO")
        if erro:
            return erro

        numero_destino, erro = self._texto(payload, "destino", "CAMPO_OBRIGATORIO")
        if erro:
            return erro

        valor, erro = self._valor(payload)
        if erro:
            return erro

        return self.service.transferencia(numero_origem, numero_destino, valor)

    def rendimento(self, payload):
        taxa, erro = self._valor(payload, "taxa")
        if erro:
            return erro

        return self.service.render_juros_total(taxa)
