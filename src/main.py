from conta.conta import Conta

def main():
    contas = {}

    while True:
        print("\n=== Sistema Bancário ===")
        print("1 - Criar conta")
        print("2 - Consultar saldo")
        print("3 - Depositar")
        print("4 - Sacar")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            numero = input("Número da conta: ")
            contas[numero] = Conta(numero)
            print("Conta criada com sucesso!")

        elif opcao == "2":
            numero = input("Número da conta: ")
            conta = contas.get(numero)

            if conta:
                print(f"Saldo: {conta.consultar_saldo()}")
            else:
                print("Conta não encontrada.")

        elif opcao == "3":
            numero = input("Número da conta: ")
            valor = float(input("Valor: "))
            conta = contas.get(numero)

            if conta:
                conta.depositar(valor)
                print("Depósito realizado.")
            else:
                print("Conta não encontrada.")

        elif opcao == "4":
            numero = input("Número da conta: ")
            valor = float(input("Valor: "))
            conta = contas.get(numero)

            if conta:
                conta.sacar(valor)
                print("Saque realizado.")
            else:
                print("Conta não encontrada.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()