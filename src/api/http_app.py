import json
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from src.api.conta_controller import ContaController
from src.conta.ContaRepository import ContaRepository
from src.conta.ContaService import ContaService


class BancoHTTPRequestHandler(BaseHTTPRequestHandler):
    controller = None

    def log_message(self, format, *args):
        return

    def _path(self):
        return urlparse(self.path).path.rstrip("/") or "/"

    def _ler_json(self):
        tamanho = int(self.headers.get("Content-Length", "0"))
        if tamanho == 0:
            return {}

        corpo = self.rfile.read(tamanho).decode("utf-8")
        if not corpo.strip():
            return {}

        try:
            dados = json.loads(corpo)
        except json.JSONDecodeError:
            return None

        return dados if isinstance(dados, dict) else None

    def _responder_json(self, status, payload):
        corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _responder_resultado(self, resultado, status_ok=HTTPStatus.OK, status_erro=HTTPStatus.BAD_REQUEST):
        status = status_ok if resultado.sucesso else status_erro
        if resultado.erro == "CONTA_NAO_ENCONTRADA":
            status = HTTPStatus.NOT_FOUND
        elif resultado.erro == "CONTA_JA_EXISTE":
            status = HTTPStatus.CONFLICT
        elif resultado.erro == "TIPO_CONTA_INVALIDO":
            status = HTTPStatus.BAD_REQUEST
        elif resultado.erro == "NENHUMA_POUPANCA_ENCONTRADA":
            status = HTTPStatus.NOT_FOUND

        self._responder_json(status, resultado.para_dict())

    def _not_found(self):
        self._responder_json(
            HTTPStatus.NOT_FOUND,
            {
                "sucesso": False,
                "mensagem": "Rota nao encontrada.",
                "dados": None,
                "erro": "ROTA_NAO_ENCONTRADA",
            },
        )

    def _metodo_nao_permitido(self):
        self._responder_json(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {
                "sucesso": False,
                "mensagem": "Metodo nao permitido.",
                "dados": None,
                "erro": "METODO_NAO_PERMITIDO",
            },
        )

    def _responder_json_invalido(self):
        self._responder_json(
            HTTPStatus.BAD_REQUEST,
            {
                "sucesso": False,
                "mensagem": "JSON invalido.",
                "dados": None,
                "erro": "JSON_INVALIDO",
            },
        )

    def do_POST(self):
        caminho = self._path()
        if caminho != "/banco/conta":
            return self._not_found()

        payload = self._ler_json()
        if payload is None:
            return self._responder_json_invalido()

        resultado = self.controller.criar_conta(payload)
        self._responder_resultado(resultado, status_ok=HTTPStatus.CREATED)

    def do_GET(self):
        caminho = self._path()

        match_saldo = re.fullmatch(r"/banco/conta/([^/]+)/saldo", caminho)
        if match_saldo:
            resultado = self.controller.consultar_saldo(match_saldo.group(1))
            return self._responder_resultado(resultado)

        match_conta = re.fullmatch(r"/banco/conta/([^/]+)", caminho)
        if match_conta:
            resultado = self.controller.consultar_conta(match_conta.group(1))
            return self._responder_resultado(resultado)

        return self._not_found()

    def do_PUT(self):
        caminho = self._path()
        payload = self._ler_json()
        if payload is None:
            return self._responder_json_invalido()

        match_credito = re.fullmatch(r"/banco/conta/([^/]+)/credito", caminho)
        if match_credito:
            resultado = self.controller.credito(match_credito.group(1), payload)
            return self._responder_resultado(resultado)

        match_debito = re.fullmatch(r"/banco/conta/([^/]+)/debito", caminho)
        if match_debito:
            resultado = self.controller.debito(match_debito.group(1), payload)
            return self._responder_resultado(resultado)

        if caminho == "/banco/conta/transferencia":
            resultado = self.controller.transferencia(payload)
            return self._responder_resultado(resultado)

        if caminho == "/banco/conta/rendimento":
            resultado = self.controller.rendimento(payload)
            return self._responder_resultado(resultado)

        return self._not_found()

    def do_PATCH(self):
        return self._metodo_nao_permitido()

    def do_DELETE(self):
        return self._metodo_nao_permitido()


def criar_servidor(host="0.0.0.0", port=8080):
    repository = ContaRepository()
    service = ContaService(repository)
    BancoHTTPRequestHandler.controller = ContaController(service)
    return ThreadingHTTPServer((host, port), BancoHTTPRequestHandler)


def run(host="0.0.0.0", port=8080):
    servidor = criar_servidor(host, port)
    endereco_exibicao = "127.0.0.1" if host == "0.0.0.0" else host
    print(f"API REST disponivel em http://{endereco_exibicao}:{port}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
    finally:
        servidor.server_close()
