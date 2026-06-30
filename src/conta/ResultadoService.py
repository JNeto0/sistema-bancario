from dataclasses import dataclass


@dataclass
class ResultadoService:
    sucesso: bool
    mensagem: str
    dados: dict | None = None
    erro: str | None = None

    def para_dict(self):
        return {
            "sucesso": self.sucesso,
            "mensagem": self.mensagem,
            "dados": self.dados,
            "erro": self.erro,
        }
