from abc import ABC, abstractmethod
from datetime import date


class Conta:
    def __init__(self, nroConta, nome, limite, senha):
        self.__nroConta = nroConta
        self.__nome = nome
        self.__limite = limite
        self.__senha = senha
        self.__transacoes = []

    @property
    def nroConta(self):
        return self.__nroConta

    @property
    def nome(self):
        return self.__nome

    @property
    def limite(self):
        return self.__limite

    @property
    def senha(self):
        return self.__senha

    @property
    def transacoes(self):
        return self.__transacoes

    def getNroConta(self):
        return self.nroConta

    def getNome(self):
        return self.nome

    def getLimite(self):
        return self.limite

    def getSenha(self):
        return self.senha

    def getTransacoes(self):
        return self.transacoes

    def adicionaDeposito(self, valor, data, nomeDepositante):
        deposito = Deposito(valor, data, nomeDepositante)
        self.transacoes.append(deposito)

    def adicionaSaque(self, valor, data, senha):
        saque = Saque(valor, data, senha)
        if (saque.senha != self.senha or self.calculaSaldo() < saque.getValor()):
            return False
        self.transacoes.append(saque)

    def adicionaTransf(self, valor, data, senha, contaFavorecido):
        transf = Transferencia(valor, data, senha, 'D')

        if (transf.getSenha() != self.senha or valor > self.calculaSaldo()):
            return False

        self.transacoes.append(transf)

        transfCredito = Transferencia(valor, data, senha, 'C')

        contaFavorecido.transacoes.append(transfCredito)

    def calculaSaldo(self):
        saldo = self.getLimite()
        for transacao in self.transacoes:
            saldo += transacao.getValor()

        return saldo


class Transacao(ABC):
    def __init__(self, valor, data):
        self.__valor = valor
        self.__data = data

    @property
    def data(self):
        return self.__data

    @property
    def valor(self):
        return self.__valor

    @abstractmethod
    def getValor(self):
        pass

    @abstractmethod
    def getData(self):
        pass


class Saque(Transacao):
    def __init__(self, valor, data, senha):
        super().__init__(valor, data)
        self.__senha = senha

    @property
    def senha(self):
        return self.__senha

    def getSenha(self):
        return self.__senha

    def getValor(self):
        return -self.valor

    def getData(self):
        return self.data


class Deposito(Transacao):
    def __init__(self, valor, data, nomeDepositante):
        super().__init__(valor, data)
        self.__nomeDepositante = nomeDepositante

    @property
    def nomeDepositante(self):
        return self.__nomeDepositante

    def getNomeDepositante(self):
        return self.__nomeDepositante

    def getValor(self):
        return self.valor

    def getData(self):
        return self.data


class Transferencia(Transacao):
    def __init__(self, valor, data, senha, tipoTransf):
        super().__init__(valor, data)
        self.__senha = senha
        self.__tipoTransf = tipoTransf

    @property
    def senha(self):
        return self.__senha

    @property
    def tipoTransf(self):
        return self.__tipoTransf

    def getSenha(self):
        return self.senha

    def getTipoTransf(self):
        return self.tipoTransf

    def getValor(self):
        if (self.getTipoTransf() == 'D'):
            return -self.valor
        elif (self.getTipoTransf() == 'C'):
            return self.valor

    def getData(self):
        return self.data


if __name__ == "__main__":
    c1 = Conta(1234, 'Jose da Silva', 1000, 'senha1')
    c1.adicionaDeposito(5000, date.today(), 'Antonio Maia')
    if c1.adicionaSaque(2000, date.today(), 'senha1') == False:
        print('Não foi possível realizar o saque no valor de 2000')
    if c1.adicionaSaque(1000, date.today(), 'senha-errada') == False:  # deve falhar
        print('Não foi possível realizar o saque no valor de 1000')

    c2 = Conta(4321, 'Joao Souza', 1000, 'senha2')
    c2.adicionaDeposito(3000, date.today(), 'Maria da Cruz')
    if c2.adicionaSaque(1500, date.today(), 'senha2') == False:
        print('Não foi possível realizar o saque no valor de 1500')
    if c2.adicionaTransf(5000, date.today(), 'senha2', c1) == False:  # deve falhar
        print('Não foi possível realizar a transf no valor de 5000')
    if c2.adicionaTransf(800, date.today(), 'senha2', c1) == False:
        print('Não foi possível realizar a transf no valor de 800')

    print('--------')
    print('Saldo de c1: {}'.format(c1.calculaSaldo()))  # deve imprimir 4800
    print('Saldo de c2: {}'.format(c2.calculaSaldo()))  # deve imprimir 1700
