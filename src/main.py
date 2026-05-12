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
        print("5 - Transferência")
        print("6 - Criar conta poupança")
        print("7 - Render juros")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            numero = input("Número da conta: ")
            
            # Chamamos o service, que agora faz a validação de 8 dígitos
            # e retorna uma string com a mensagem de sucesso ou erro.
            mensagem = service.criar_conta(numero)
            
            # Exibimos a mensagem diretamente para o usuário
            print(mensagem)

        
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

            valor = float(input("Valor do débito: "))

            mensagem = service.debito(numero, valor)

            print(mensagem)

        elif opcao == "5":

            origem = input("Conta origem: ")

            destino = input("Conta destino: ")

            valor = float(input("Valor da transferência: "))

            mensagem = service.transferencia(origem, destino, valor)

            print(mensagem)

        elif opcao == "6":
            numero = input("Número da conta poupança: ")
            print(service.criar_poupanca(numero))

        elif opcao == "7":
            try:
                taxa = float(input("Informe a taxa de juros (%): "))
                print(service.render_juros_total(taxa))
            except ValueError:
                print("Erro: Informe um valor numérico para a taxa.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()