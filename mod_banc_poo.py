from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
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
    
    
    def sacar(self, *, valor, limite, numero_saques, limite_saques):
        if valor <= 0:
            print("\n Operação falhou! O valor informado é inválido. ")
            return False

        if valor > self._saldo:
            print("\n Operação falhou! Você não tem saldo suficiente. ")
            return False

        if valor > limite:
            print("\n Operação falhou! O valor do saque excede o limite. ")
            return False

        if numero_saques >= limite_saques:
            print("\n Operação falhou! Número máximo de saques excedido. ")
            return False

        self._saldo -= valor
        self._historico.adicionar_transacao(Saque(valor))
        print("\n=== Saque realizado com sucesso! ===")
        return True


    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            
            return False
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")


    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor, /):
        if valor <= 0:
            print("\n Operação falhou! O valor informado é inválido. ")
            return

        if valor > self.saldo:
            print("\n Operação falhou! Você não tem saldo suficiente. ")
            return

        if valor > self.limite:
            print("\n Operação falhou! O valor do saque excede o limite. ")
            return

        if self.numero_saques >= self.limite_saques:
            print("\n Operação falhou! Número máximo de saques excedido. ")
            return

        self.saldo -= valor
        self.historico.adicionar_lancamento("Saque", valor)
        self.numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
        
    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            C/C: {self.numero}
            Titular: {self.cliente.nome}
        """
        
        
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def __str__(self):
        return "\n".join(
            f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}"
            for transacao in self.transacoes
        )


class Transacao(ABC):
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


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


def menu():
    opcoes = {
        'd': 'Depositar',
        's': 'Sacar',
        'e': 'Extrato',
        'nc': 'Nova conta',
        'lc': 'Listar contas',
        'nu': 'Novo usuário',
        'q': 'Sair'
    }

    menu_str = "\n" + "============== MENU ==============\n"
    for opcao, descricao in opcoes.items():
        menu_str += f"[{opcao}]\t{descricao}\n"
    menu_str += "=> "

    return input(textwrap.dedent(menu_str))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas.")
        return None
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

    
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
        
        
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n=== Extrato da Conta ===")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação realizada."
    else:
        extrato = "\n".join(f"{t.data} - {t.tipo}: R$ {t.valor:.2f}" for t in transacoes)

    print(extrato)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("=" * 30)
    
    
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já existe.")
        return cliente

    nome = input("Informe o nome do cliente: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Informe o endereço do cliente: ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)
    
    print(f"Cliente {cliente.nome} criado com sucesso!")
    print(f"CPF: {cliente.cpf}, Data de Nascimento: {cliente.data_nascimento}, Endereço: {cliente.endereco}")
    print("=" * 30)
    


def criar_conta(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta= ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f"Conta criada com sucesso! Número da conta: {conta.numero}")
    
    
    
def listar_contas(clientes):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    print("=" * 100)    


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            
            valor = float(input("Informe o valor do depósito: "))
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                conta.depositar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == 's':
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            
            valor = float(input("Informe o valor do saque: "))
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                conta.sacar(valor)
            else:
                print("Conta não encontrada.")

        elif opcao == 'e':
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if not cliente:
                print("Cliente não encontrado.")
                continue
            
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                print(conta.historico)
            else:
                print("Conta não encontrada.")

        elif opcao == 'nc':
            nome = input("Informe o nome do cliente: ")
            data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy): ")
            cpf = input("Informe o CPF do cliente: ")
            endereco = input("Informe o endereço do cliente: ")
            
            novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
            clientes.append(novo_cliente)
            
            numero_conta = len(contas) + 1
            nova_conta = ContaCorrente.nova_conta(novo_cliente, numero_conta)
            contas.append(nova_conta)

        elif opcao == 'lc':
            for conta in contas:
                print(conta)

        elif opcao == 'nu':
            nome = input("Informe o nome do novo usuário: ")
            data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy): ")
            cpf = input