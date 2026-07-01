from src.conta.ContaRepository import ContaRepository
from src.conta.ContaService import ContaService


def main():
    repository = ContaRepository()
    service = ContaService(repository)

    while True:
        print("\n=== Sistema Bancario ===")
        print("1 - Criar conta")
        print("2 - Consultar saldo")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Transferencia")
        print("6 - Criar conta poupanca")
        print("7 - Render juros")
        print("8 - Criar conta bonus")
        print("9 - Consultar dados da conta")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            numero = input("Numero da conta: ")
            saldo_inicial = float(input("Saldo inicial: "))
            resultado = service.criar_conta(numero, saldo_inicial)

            print(resultado.mensagem)

        elif opcao == "2":
            numero = input("Numero da conta: ")
            resultado = service.consultar_saldo(numero)

            if resultado.sucesso:
                saldo = resultado.dados["saldo"]
                print(f"Saldo: R$ {saldo:.2f}")
            else:
                print(resultado.mensagem)

        elif opcao == "3":
            numero = input("Numero da conta: ")
            valor = float(input("Valor do credito: "))
            resultado = service.credito(numero, valor)

            print(resultado.mensagem)

        elif opcao == "4":
            numero = input("Numero da conta: ")
            valor = float(input("Valor do debito: "))
            resultado = service.debito(numero, valor)

            print(resultado.mensagem)

        elif opcao == "5":
            origem = input("Conta origem: ")
            destino = input("Conta destino: ")
            valor = float(input("Valor da transferencia: "))
            resultado = service.transferencia(origem, destino, valor)

            print(resultado.mensagem)

        elif opcao == "6":
            numero = input("Numero da conta poupanca: ")
            saldo_inicial = float(input("Saldo inicial: "))
            resultado = service.criar_poupanca(numero, saldo_inicial)

            print(resultado.mensagem)

        elif opcao == "7":
            try:
                taxa = float(input("Informe a taxa de juros (%): "))
                resultado = service.render_juros_total(taxa)
                print(resultado.mensagem)
            except ValueError:
                print("Erro: Informe um valor numerico para a taxa.")

        elif opcao == "8":
            numero = input("Numero da conta: ")
            resultado = service.criar_conta_bonus(numero)

            print(resultado.mensagem)

        elif opcao == "9":
            numero = input("Numero da conta: ")
            resultado = service.consultar_conta(numero)

            if resultado.sucesso:
                dados = resultado.dados
                print(f"Tipo: {dados['tipo']}")
                print(f"Numero: {dados['numero']}")
                print(f"Saldo: R$ {dados['saldo']:.2f}")
                if "bonus" in dados:
                    print(f"Bonus: {dados['bonus']}")
            else:
                print(resultado.mensagem)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
