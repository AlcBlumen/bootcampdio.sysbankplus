import re
from datetime import datetime

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class ContaBancaria:
    numero_conta_sequencial = 1
    
    def __init__(self, agencia, usuario):
        self.agencia = agencia
        self.numero_conta = ContaBancaria.numero_conta_sequencial
        ContaBancaria.numero_conta_sequencial += 1
        self.usuario = usuario
        self.saldo = 0
        self.extrato = []
        self.numero_saques = 0

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.saldo += valor
        self.extrato.append(f"Depósito: R$ {valor:.2f}")
    
    def sacar(self, valor, limite=500, limite_saques=3):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        if valor > limite:
            raise ValueError("O valor do saque excede o limite permitido.")
        if self.numero_saques >= limite_saques:
            raise ValueError("Número máximo de saques excedido.")
        
        self.saldo -= valor
        self.extrato.append(f"Saque: R$ {valor:.2f}")
        self.numero_saques += 1

    def visualizar_extrato(self):
        print("\n================ EXTRATO ================")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            for item in self.extrato:
                print(item)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
    
    def cadastrar_usuario(self, nome, data_nascimento, cpf, endereco):
        if not self.validar_cpf(cpf):
            raise ValueError("CPF inválido ou já cadastrado.")
        if not self.validar_data_nascimento(data_nascimento):
            raise ValueError("Data de nascimento inválida.")
        
        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print(f"Usuário {nome} cadastrado com sucesso.")
        return usuario

    def cadastrar_conta(self, agencia, cpf):
        usuario = self.obter_usuario_por_cpf(cpf)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        
        conta = ContaBancaria(agencia, usuario)
        usuario.adicionar_conta(conta)
        self.contas.append(conta)
        print(f"Conta bancária {conta.numero_conta} criada com sucesso para o usuário {usuario.nome}.")
        return conta

    def obter_usuario_por_cpf(self, cpf):
        return next((u for u in self.usuarios if u.cpf == cpf), None)
    
    @staticmethod
    def validar_cpf(cpf):
        padrao_cpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'  # Exemplo de formato: 123.456.789-10
        if not re.match(padrao_cpf, cpf):
            return False
        return True
    
    @staticmethod
    def validar_data_nascimento(data):
        try:
            datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            return False



def menu_principal():
    banco = Banco()
    
    menu = """
    [1] Cadastrar Usuário
    [2] Cadastrar Conta Bancária
    [3] Depositar
    [4] Sacar
    [5] Visualizar Extrato
    [6] Sair

    => """
    
    while True:
        opcao = input(menu)
        
        try:
            if opcao == "1":
                nome = input("Nome: ")
                data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
                cpf = input("CPF (xxx.xxx.xxx-xx): ")
                endereco = input("Endereço: ")
                banco.cadastrar_usuario(nome, data_nascimento, cpf, endereco)

            elif opcao == "2":
                agencia = input("Agência: ")
                cpf = input("CPF do usuário: ")
                banco.cadastrar_conta(agencia, cpf)

            elif opcao == "3":
                cpf = input("CPF do usuário: ")
                usuario = banco.obter_usuario_por_cpf(cpf)
                if usuario and usuario.contas:
                    conta = usuario.contas[0]  # Seleciona a primeira conta para simplificação
                    valor = float(input("Informe o valor do depósito: "))
                    conta.depositar(valor)
                    print("Depósito realizado com sucesso!")
                else:
                    print("Usuário ou conta não encontrados.")

            elif opcao == "4":
                cpf = input("CPF do usuário: ")
                usuario = banco.obter_usuario_por_cpf(cpf)
                if usuario and usuario.contas:
                    conta = usuario.contas[0]
                    valor = float(input("Informe o valor do saque: "))
                    conta.sacar(valor=valor)
                    print("Saque realizado com sucesso!")
                else:
                    print("Usuário ou conta não encontrados.")

            elif opcao == "5":
                cpf = input("CPF do usuário: ")
                usuario = banco.obter_usuario_por_cpf(cpf)
                if usuario and usuario.contas:
                    conta = usuario.contas[0]
                    conta.visualizar_extrato()
                else:
                    print("Usuário ou conta não encontrados.")

            elif opcao == "6":
                print("Saindo do sistema. Obrigado!")
                break

            else:
                print("Opção inválida.")
        
        except ValueError as e:
            print(f"Erro: {e}")



menu_principal()
