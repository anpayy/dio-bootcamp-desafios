from abc import ABC,abstractmethod

from datetime import datetime

class Cliente:
    def __init__ (self,endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
   
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        saldo = self._saldo
        saldo_excedido = valor > self._saldo
        
        if saldo_excedido:
            print("Erro - o saldo excede o saldo disponível.")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Erro - Valor inválido")
            return False
        
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        
        else:
            print("Erro - impossível depositar valor.")
            return False

class Historico():
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data" :datetime.now().strtime("%d-%m-%Y %H:%M:%s"),            
            })

class Transacao(ABC):
    @property
    @abstractmethod 
    def valor(self):
        pass

    @abstractmethod
    def registrar (self,conta):
        pass

class Saque(Transacao):
    
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            print("Saque realizado.")

class Deposito (Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite = 500,limite_saques = 3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self,valor):
        numero_saques = len(transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__)
        limite_excedido = valor > self.limite
        saque_excedido = numero_saques > self.limite_saques

        if limite_excedido:
            print("Erro - limite de saque excedido.")
        
        elif saque_excedido:
            print("Erro")
        
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""
            Agência: {self.agencia}
            Conta Corrente: {self.numero}
            Titular: {self.cliente.nome}
        """
