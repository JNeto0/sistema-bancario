from src.conta.Conta import Conta
from src.conta.ContaRepository import ContaRepository
from src.conta.ContaService import ContaService

def main():
    contas = {} 
    repository = ContaRepository()
    service = ContaService(repository)

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

            conta = service.criar_conta(numero)

            if conta:
                print("Conta criada com sucesso!")
            else:
                print("Conta já existe.")

        
        elif opcao == "2":

            numero = input("Número da conta: ")

            saldo = service.consultar_saldo(numero)

            if saldo is not None:
                print(f"Saldo: R$ {saldo:.2f}")
            else:
                print("Conta não encontrada.")


        elif opcao == "3":

            numero = input("Número da conta: ")

            valor = float(input("Valor do crédito: "))

            mensagem = service.credito(numero, valor)

            print(mensagem)


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