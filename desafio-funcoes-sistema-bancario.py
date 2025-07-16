
def menu(): 
    menu = str(input("""
=============== MENU ================   
       Escolha a operação:
         [D] - Depósito
         [S] - Saque
         [E] - Extrato
         [N] - Nova Conta
         [L] - Listar Contas
        [NU] - Novo Usuário
=====================================
      => """))
    return menu
    

def nova_operacao(se_nova_operacao):
    while True:
        se_nova_operacao = str(input("""
=======================================
Deseja realizar uma nova operação?
        [1] - Sim
        [2] - Não 
=======================================
        => """).strip())
        
        if se_nova_operacao != "1" and se_nova_operacao != "2":
                print("\nComando inválido! Tente novamente!\n")
                continue
        if se_nova_operacao == "2":
            print("\nOperação Concluída! \nObrigado por utilizar nosso banco!\n")
            break
        
        return se_nova_operacao
    


def deposito(saldo, extrato, /):
    print("\n=============== DEPÓSITO ================")
    valor = float(input("Digite o valor a ser depositado:\nR$ "))
    if valor > 0:
        extrato += f"Depósito de: R$ {valor:.2f}.\n"
        saldo += valor
        print(f"\nVocê depositou R$ {valor:.2f}!\n")
    else:
        print("Valor inválido! Digite um valor positivo. \n")
        print("="*40,"\n")
    return saldo, extrato


def saque(*, saldo, extrato, limite_saque_diario, contador_saques):
    limite_valor_por_saque = 500
    print("\n=============== SAQUE ================")
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
        print("="*42,"\n")
    return saldo, extrato

                        
def exibe_extrato(saldo, /, *, extrato):
    print("\n=============== EXTRATO ================")
    print("\nNão foram realizadas movimentações!" if not extrato else extrato)                  
    print(f"\nSALDO ATUAL: R${saldo:.2f}.")
    print("="*42,"\n")


def novo_usuario(usuarios):
    print("\n=============== NOVO USUÁRIO ================")
    while True:
        cpf = input("Insira seu CPF: ").replace(".", "").replace("-", "").strip()
        if len(cpf) != 11:
            print("CPF inválido! Insira novamente.")
        elif any(cpf_existente[2] == cpf for cpf_existente in usuarios):
            print("CPF já cadastrado! Insira um CPF não usado anteriormente.")
            continue
            
        nome = input("Digite seu nome completo: ").strip().title()
        if not all( parte.isalpha() for parte in nome.split()):
            print("Nome inválido! Insira apenas letras.\n")
            continue
            
        data = input("Digite sua data de nascimento (apenas números): ").strip()
        dia, mes, ano = data[:2], data[2:4], data[4:]
        if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
            print("Data inválida! Tente novamente.")
            continue
        data_nascimento = "/".join([dia, mes, ano])
        
        endereco_digitado = input("Digite seu endereço (Logradouro - Bairro - Cidade - UF): ").split(" - ")
        if len(endereco_digitado) != 4:
            print("Endereço Inválido! Tente novamente.")
            continue
        logradouro, bairro, cidade, estado = [end.strip() for end in endereco_digitado]
        if len(estado) != 2 and not estado.isalpha():
            print("Formato de sigla do estado inválido! Tente novamente.(UF)\n")
            continue   
        endereco = ", ".join([logradouro.title(), bairro.title(), f"{cidade.title()}/{estado.upper()}"])
        
        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        print("\nNovo usuário cadastrado com sucesso!")
        print("="*42,"\n")
        break    
    return usuarios 


def nova_conta(n_conta, AGENCIA, usuarios):
    print("\n=============== NOVA CONTA ================")
    while True:
        cpf = input("Insira seu CPF: ").replace(".", "").replace("-", "").strip()
        if len(cpf) != 11:
            print("CPF inválido! Insira novamente.")
            continue
        
        for usuario in usuarios:
            if usuario["cpf"] == cpf:
                print(f"\nBem-vindo(a), {usuario["nome"].split()[0]}!")
                print("\nNova conta criada com sucesso!")
                print(F"Agência: {AGENCIA}   Conta: {n_conta}")
                print("="*42,"\n")
                return {"agencia": AGENCIA, "n_conta": n_conta, "usuario": usuario} 
        else:    
            print("\nUsuário não encontrado!")
           
        print("="*42,"\n")
        break


def listar_contas(contas):
    print("\n============= CENTRAL DE CONTAS ==============")
    if not contas:
        print("Nenhuma conta cadastrada.")

    for conta in contas:
        usuario = conta["usuario"]
        print(f"Titular: {usuario["nome"]} \nAgência: {conta["agencia"]}   Conta: {conta["n_conta"]}")
        print("="*46,"\n")


def main ():
    saldo = 500
    extrato = ""
    contador_saques = 0
    LIMITE_SAQUE_DIARIO = 3
    se_nova_operacao = "1"
    usuarios = []
    contas = []
    AGENCIA = "0001"
    n_conta = 0
    
    print("\n  BEM-VINDO AO SISTEMA BANCÁRIO\n".center(96,"="))
    while True:
        if se_nova_operacao == "1":
            opcao = menu()
            
            if opcao.upper() == "D":
                saldo, extrato = deposito(saldo, extrato)
                

            elif opcao.upper() == "S":
                saldo, extrato = saque(saldo=saldo, extrato=extrato, limite_saque_diario=LIMITE_SAQUE_DIARIO, contador_saques=contador_saques)
                

            elif opcao.upper() == "E":
                exibe_extrato(saldo, extrato=extrato)
                

            elif opcao.upper() == "N":
                n_conta = len(contas) + 1
                conta = nova_conta(n_conta, AGENCIA, usuarios)
                
                if conta:
                    contas.append(conta)
                

            elif opcao.upper() == "L":
                listar_contas(contas)
                

            elif opcao.upper() == "NU":
                usuarios = novo_usuario(usuarios)
                
            
            se_nova_operacao = nova_operacao(se_nova_operacao)
        
        else:
            break
        
               
main()