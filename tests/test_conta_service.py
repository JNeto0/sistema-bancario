import unittest

from src.conta.Conta import Conta
from src.conta.ContaBonus import ContaBonus
from src.conta.ContaPoupanca import ContaPoupanca
from src.conta.ContaRepository import ContaRepository
from src.conta.ContaService import ContaService


class TestContaService(unittest.TestCase):
    def setUp(self):
        self.repository = ContaRepository()
        self.service = ContaService(self.repository)

    def test_criar_conta_comum(self):
        resultado = self.service.criar_conta("12345678", 100.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.mensagem, "Conta criada com sucesso!")
        self.assertEqual(resultado.dados["tipo"], "Conta Simples")
        self.assertEqual(resultado.dados["numero"], "12345678")
        self.assertEqual(resultado.dados["saldo"], 100.0)

    def test_criar_conta_poupanca(self):
        resultado = self.service.criar_poupanca("12345678", 200.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["tipo"], "Conta Poupanca")
        self.assertEqual(resultado.dados["saldo"], 200.0)

    def test_criar_conta_bonus(self):
        resultado = self.service.criar_conta_bonus("12345678")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["tipo"], "Conta Bonus")
        self.assertEqual(resultado.dados["bonus"], 10)

    def test_consultar_conta_simples(self):
        self.repository.adicionar(Conta("12345678", 100.0))

        resultado = self.service.consultar_conta("12345678")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["tipo"], "Conta Simples")
        self.assertEqual(resultado.dados["numero"], "12345678")

    def test_consultar_conta_poupanca(self):
        self.repository.adicionar(ContaPoupanca("12345678", 200.0))

        resultado = self.service.consultar_conta("12345678")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["tipo"], "Conta Poupanca")
        self.assertEqual(resultado.dados["saldo"], 200.0)

    def test_consultar_conta_bonus(self):
        self.repository.adicionar(ContaBonus("12345678", 300.0))

        resultado = self.service.consultar_conta("12345678")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["tipo"], "Conta Bonus")
        self.assertEqual(resultado.dados["bonus"], 10)

    def test_consultar_saldo(self):
        self.repository.adicionar(Conta("12345678", 100.0))

        resultado = self.service.consultar_saldo("12345678")

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["saldo"], 100.0)

    def test_credito_normal(self):
        self.repository.adicionar(Conta("12345678", 100.0))

        resultado = self.service.credito("12345678", 50.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["saldo"], 150.0)

    def test_credito_negativo(self):
        self.repository.adicionar(Conta("12345678", 100.0))

        resultado = self.service.credito("12345678", -10.0)

        self.assertFalse(resultado.sucesso)
        self.assertEqual(resultado.erro, "VALOR_INVALIDO")

    def test_credito_bonus_aplica_pontuacao(self):
        self.repository.adicionar(ContaBonus("12345678", 100.0))

        resultado = self.service.credito("12345678", 200.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["saldo"], 300.0)
        self.assertEqual(resultado.dados["bonus"], 12)

    def test_debito_normal(self):
        self.repository.adicionar(Conta("12345678", 100.0))

        resultado = self.service.debito("12345678", 50.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["saldo"], 50.0)

    def test_debito_negativo(self):
        self.repository.adicionar(Conta("12345678", 100.0))

        resultado = self.service.debito("12345678", -10.0)

        self.assertFalse(resultado.sucesso)
        self.assertEqual(resultado.erro, "VALOR_INVALIDO")

    def test_debito_saldo_insuficiente(self):
        self.repository.adicionar(ContaPoupanca("12345678", 100.0))

        resultado = self.service.debito("12345678", 150.0)

        self.assertFalse(resultado.sucesso)
        self.assertEqual(resultado.erro, "SALDO_INSUFICIENTE")

    def test_transferencia_negativa(self):
        self.repository.adicionar(Conta("12345678", 100.0))
        self.repository.adicionar(Conta("87654321", 100.0))

        resultado = self.service.transferencia("12345678", "87654321", -10.0)

        self.assertFalse(resultado.sucesso)
        self.assertEqual(resultado.erro, "VALOR_INVALIDO")

    def test_transferencia_saldo_insuficiente(self):
        self.repository.adicionar(Conta("12345678", 100.0))
        self.repository.adicionar(Conta("87654321", 100.0))

        resultado = self.service.transferencia("12345678", "87654321", 1200.0)

        self.assertFalse(resultado.sucesso)
        self.assertEqual(resultado.erro, "SALDO_INSUFICIENTE")

    def test_transferencia_bonus_aplica_pontuacao(self):
        self.repository.adicionar(Conta("12345678", 500.0))
        self.repository.adicionar(ContaBonus("87654321", 0.0))

        resultado = self.service.transferencia("12345678", "87654321", 300.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.dados["origem"]["saldo"], 200.0)
        self.assertEqual(resultado.dados["destino"]["saldo"], 300.0)
        self.assertEqual(resultado.dados["destino"]["bonus"], 12)

    def test_render_juros_total(self):
        self.repository.adicionar(ContaPoupanca("12345678", 100.0))
        self.repository.adicionar(ContaPoupanca("87654321", 200.0))
        self.repository.adicionar(Conta("11223344", 300.0))

        resultado = self.service.render_juros_total(10.0)

        self.assertTrue(resultado.sucesso)
        self.assertEqual(len(resultado.dados["contas"]), 2)
        self.assertEqual(self.repository.buscar_por_numero("12345678").consultar_saldo(), 110.0)
        self.assertEqual(self.repository.buscar_por_numero("87654321").consultar_saldo(), 220.0)
        self.assertEqual(self.repository.buscar_por_numero("11223344").consultar_saldo(), 300.0)


if __name__ == "__main__":
    unittest.main()
