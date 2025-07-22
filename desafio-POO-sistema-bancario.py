from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        pass

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        pass


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico


    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("\nSaldo insuficiente para saque!\n")
        elif valor > 0:
            print(f"Saque no valor de R${valor:.2f} realizado com sucesso!\n")
            self._saldo -= valor
            return True
        else:
            print("\nValor inválido! Tente Novamente.\n")
        return False


    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nVocê depositou R$ {valor:.2f}!\n")
        else:
            print("Valor inválido! Digite um valor positivo. \n")
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        contador_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if contador_saques > self.limite_saques:
            print("\nLimite de saque diário atingido! \nPara alteração de limite entre em contato com seu gerente!\n")
        elif valor > self.limite:
            print(
                f"\nValor não permitido! \nSeu limite por saque é de R${self.limite :.2f}.\nPara alteração de limite entre em contato com seu gerente!\n")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
        Titular: {self.cliente.nome}
        Agência: {self.agencia}   Conta: {self.numero}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


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

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def conta_existe(cliente):
    if not cliente.contas:
        print("\nCliente não possui uma conta!")
        return
    return cliente.contas[0]

def deposito(clientes):
    print("\n=============== DEPÓSITO ================")
    cpf = input("Insira seu CPF: ").replace(".", "").replace("-", "").strip()
    if len(cpf) != 11:
        print("CPF inválido! Insira novamente.")
        return
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n## Cliente não encontrado! ##")
        return

    conta = conta_existe(cliente)
    if not conta:
        return

    valor = float(input("Digite o valor a ser depositado:\nR$ "))
    transacao = Deposito(valor)


    cliente.realizar_transacao(conta,transacao)

def saque(clientes):
    print("\n=============== SAQUE ================")
    cpf = input("Insira seu CPF: ").replace(".", "").replace("-", "").strip()
    if len(cpf) != 11:
        print("CPF inválido! Insira novamente.")
        return
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n## Cliente não encontrado!##")
        return

    conta = conta_existe(cliente)
    if not conta:
        return

    valor = float(input("Digite o valor a ser sacado:\nR$ "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)


def exibe_extrato(clientes):
    cpf = input("\nInsira seu CPF: ").replace(".", "").replace("-", "").strip()
    if len(cpf) != 11:
        print("CPF inválido! Insira novamente.")
        return
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n## Cliente não encontrado! ##")
        return

    conta = conta_existe(cliente)
    if not conta:
        return

    print("\n=============== EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\nNão foram realizadas movimentações!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSALDO ATUAL: R$ {conta.saldo:.2f}")
    print("=" * 42, "\n")

def novo_usuario(clientes):
    print("\n=============== NOVO USUÁRIO ================")
    cpf = input("Insira seu CPF: ").replace(".", "").replace("-", "").strip()
    if len(cpf) != 11:
        print("CPF inválido! Insira novamente.")
        return
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\nCliente já cadastrado!")
        return

    nome = input("Digite seu nome completo: ").strip().title()
    if not all(parte.isalpha() for parte in nome.split()):
        print("Nome inválido! Insira apenas letras.\n")
        return

    data = input("Digite sua data de nascimento (ddmmaaaa): ").strip()
    dia, mes, ano = data[:2], data[2:4], data[4:]
    if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
        print("Data inválida! Tente novamente.")
        return
    data_nascimento = "/".join([dia, mes, ano])

    endereco_digitado = input("Digite seu endereço (Logradouro - Bairro - Cidade - UF): ").split(" - ")
    if len(endereco_digitado) != 4:
        print("Endereço Inválido! Tente novamente.")
        return
    logradouro, bairro, cidade, estado = [end.strip() for end in endereco_digitado]
    if len(estado) != 2 and not estado.isalpha():
        print("Formato de sigla do estado inválido! Tente novamente.(UF)\n")
        return
    endereco = ", ".join([logradouro.title(), bairro.title(), f"{cidade.title()}/{estado.upper()}"])

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\nNovo usuário cadastrado com sucesso!")
    print("=" * 42, "\n")

def criar_conta(n_conta, clientes, contas):
    print("\n=============== NOVA CONTA ================")
    cpf = input("Insira seu CPF: ").replace(".", "").replace("-", "").strip()
    if len(cpf) != 11:
        print("\nCPF inválido! Tente novamente.")
        return
    cliente = filtrar_cliente(cpf,clientes)
    if not cliente:
        print("\n## Cliente não encontrado! ##")
        return

    print(f"\nBem-vindo(a), {cliente.nome.split()[0]}!")

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=n_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\nNova conta criada com sucesso!")
    print(F"Agência: {conta.agencia}   Conta: {n_conta}")
    print("=" * 42, "\n")

def listar_contas(contas):
    print("\n============ CENTRAL DE CONTAS =============")
    for conta in contas:
        print(str(conta))
        print("=" * 48, "\n")

def main():
    clientes = []
    contas = []
    se_nova_operacao = "1"

    print("\n  BEM-VINDO AO SISTEMA BANCÁRIO\n".center(96, "="))
    while True:
        if se_nova_operacao == "1":
            opcao = menu()

            if opcao.upper() == "D":
                deposito(clientes)

            elif opcao.upper() == "S":
                saque(clientes)

            elif opcao.upper() == "E":
                exibe_extrato(clientes)

            elif opcao.upper() == "N":
                n_conta = len(contas) + 1
                criar_conta(n_conta, clientes, contas)

            elif opcao.upper() == "L":
                listar_contas(contas)

            elif opcao.upper() == "NU":
                novo_usuario(clientes)

            se_nova_operacao = nova_operacao(se_nova_operacao)

        else:
            break


main()