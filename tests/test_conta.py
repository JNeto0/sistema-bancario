import unittest

from src.conta.Conta import Conta
from src.conta.ContaBonus import ContaBonus
from src.conta.ContaPoupanca import ContaPoupanca


class TestConta(unittest.TestCase):
    def test_depositar_valor_positivo(self):
        conta = Conta("12345678", 100.0)

        resultado = conta.depositar(50.0)

        self.assertTrue(resultado)
        self.assertEqual(conta.consultar_saldo(), 150.0)

    def test_depositar_valor_nao_positivo(self):
        conta = Conta("12345678", 100.0)

        resultado = conta.depositar(0)

        self.assertFalse(resultado)
        self.assertEqual(conta.consultar_saldo(), 100.0)

    def test_sacar_respeita_limite_negativo(self):
        conta = Conta("12345678", 100.0)

        resultado = conta.sacar(1050.0)

        self.assertTrue(resultado)
        self.assertEqual(conta.consultar_saldo(), -950.0)

    def test_sacar_bloqueia_abaixo_do_limite(self):
        conta = Conta("12345678", 100.0)

        resultado = conta.sacar(1201.0)

        self.assertFalse(resultado)
        self.assertEqual(conta.consultar_saldo(), 100.0)

    def test_conta_poupanca_render_juros(self):
        conta = ContaPoupanca("12345678", 200.0)

        resultado = conta.render_juros(10.0)

        self.assertTrue(resultado)
        self.assertEqual(conta.consultar_saldo(), 220.0)

    def test_conta_poupanca_bloqueia_saldo_negativo(self):
        conta = ContaPoupanca("12345678", 100.0)

        resultado = conta.sacar(150.0)

        self.assertFalse(resultado)
        self.assertEqual(conta.consultar_saldo(), 100.0)

    def test_conta_bonus_depositar_soma_pontos(self):
        conta = ContaBonus("12345678", 0.0)

        conta.depositar(250.0)

        self.assertEqual(conta.consultar_saldo(), 250.0)
        self.assertEqual(conta.pontuacao, 12)

    def test_conta_bonus_transferencia_soma_pontos(self):
        conta = ContaBonus("12345678", 0.0)

        conta.receber_transferencia(300.0)

        self.assertEqual(conta.consultar_saldo(), 300.0)
        self.assertEqual(conta.pontuacao, 12)

    def test_consultar_dados_por_tipo(self):
        conta_simples = Conta("12345678", 100.0)
        conta_poupanca = ContaPoupanca("87654321", 200.0)
        conta_bonus = ContaBonus("11223344", 300.0)

        self.assertEqual(
            conta_simples.consultar_dados(),
            {"tipo": "Conta Simples", "numero": "12345678", "saldo": 100.0},
        )
        self.assertEqual(
            conta_poupanca.consultar_dados(),
            {"tipo": "Conta Poupanca", "numero": "87654321", "saldo": 200.0},
        )
        self.assertEqual(
            conta_bonus.consultar_dados(),
            {
                "tipo": "Conta Bonus",
                "numero": "11223344",
                "saldo": 300.0,
                "bonus": 10,
            },
        )


if __name__ == "__main__":
    unittest.main()
