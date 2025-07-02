
menu = """
   Escolha a operação:
     [D] - Depósito
     [S] - Saque
     [E] - Extrato
   
      => """

saldo = 500
extrato = ""
contador_saques = 0
contador_depositos = 0
limite_saque_diario = 3
limite_valor_por_saque = 500
se_nova_operacao = "1"

print("\n BEM-VINDO AO SISTEMA BANCÁRIO\n".center(96,"#"))

while True:
    if se_nova_operacao == "1":
        opcao = input(menu)
        
        if opcao.upper() == "D":
            print("\n           DEPÓSITO \n".center(87,"="))
            valor = float(input("Digite o valor a ser depositado:\nR$ "))
            if valor > 0:
                extrato += f"Depósito de: R$ {valor:.2f}.\n"
                contador_depositos += 1 
                saldo += valor
                print(f"\nParabéns! Você depositou R$ {valor:.2f}!\n")
            else:
                print("Valor inválido! Digite um valor positivo. \n")
                        

        elif opcao.upper() == "S":
            print("\n            SAQUE \n".center(88,"="))
            if contador_saques > limite_saque_diario:
                print("\nLimite de saque diário atingido! \nPara alteração de limite entre em contato com seu gerente!\n")
            else:
                valor = float(input("Digite o valor do saque: \nR$ "))
                if valor > 0:
                    if valor > limite_valor_por_saque:
                        print(f"\nValor não permitido! \nSeu limite por saque é de R${limite_valor_por_saque:.2f}.\nPara alteração de limite entre em contato com seu gerente!\n")
                    elif valor > saldo:
                        print("\nSaldo insuficiente para saque!\n")
                    else:
                        extrato += f"Saque de: R$ {valor:.2f}.\n"
                        contador_saques += 1
                        saldo -= valor
                        print(f"Saque no valor de R${valor:.2f} realizado com sucesso!\n") 
                else:
                    print("\nValor inválido! Tente Novamente.\n")

                    
        elif opcao.upper() == "E":
            print("============= EXTRATO ==============")
            print("\nNão foram realizadas movimentações!" if not extrato else extrato)                  
            print(f"\nSALDO ATUAL: R${saldo:.2f}.")
            print("="*36)
        
        else:
            print("Comando inválido! Tente novamente.\n")

        print("="*36)
        se_nova_operacao = str(input(f""" Deseja realizar uma nova operação?
         [1] - Sim
         [2] - Não 
====================================
        => """).strip())
        
        
    elif se_nova_operacao == "2":
        print("\nOperação Concluída! \nObrigado por utilizar nosso banco!\n")
        break
    else:
        print("\nComando inválido! Tente novamente!\n")
        se_nova_operacao = str(input(f""" Deseja realizar uma nova operação?
         [1] - Sim
         [2] - Não 
====================================
        => """).strip())