import datetime
from abc import ABC, abstractmethod


class Vendedor(ABC):
    def __init__(self, codigo, nome):
        self.__codigo = codigo
        self.__nome = nome
        self.__vendas = []

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nome(self):
        return self.__nome

    @property
    def vendas(self):
        return self.__vendas

    def getCodigo(self):
        return self.codigo

    def getVendas(self):
        return self.vendas

    def getNome(self):
        return self.nome

    def adicionaVenda(self, pCodImovel, pMes, pAno, pValor):
        venda = Venda(pCodImovel, pMes, pAno, pValor)
        self.__vendas.append(venda)

    @abstractmethod
    def getDados(self):
        pass

    @abstractmethod
    def calculaRenda(pMes, pAno):
        pass


class Contratado(Vendedor):
    def __init__(self, codigo, nome, nroCartTrabalho, salarioFixo):
        super().__init__(codigo, nome)
        self.__nroCartTrabalho = nroCartTrabalho
        self.__salarioFixo = salarioFixo

    def getNroCartTrabalho(self):
        return self.__nroCartTrabalho

    def getSalarioFixo(self):
        return self.__salarioFixo

    def getDados(self):
        print(
            f"Nome: {self.getNome()} - Nro Carteira: {self.getNroCartTrabalho()}")

    def calculaRenda(self, pMes, pAno):
        valorTotal = self.__salarioFixo
        for venda in self.vendas:
            if venda.getMesVenda() == pMes and venda.getAnoVenda() == pAno:
                valorTotal += venda.getValorVenda() * 1.001

        return valorTotal


class Comissionado(Vendedor):
    def __init__(self, codigo, nome, nroCPF, comissao):
        super().__init__(codigo, nome)
        self.__nroCPF = nroCPF
        self.__comissao = comissao

    def getNroCPF(self):
        return self.__nroCPF

    def getComissao(self):
        return self.__comissao

    def getDados(self):
        print(f'Nome: {self.getNome()} - Nro CPF: {self.getNroCPF()}')

    def calculaRenda(self, pMes, pAno):
        valorTotal = 0
        for venda in self.vendas:
            if venda.getMesVenda() == pMes and venda.getAnoVenda() == pAno:
                valorTotal += venda.getValorVenda() * (1 + (self.getComissao() / 100))

        return valorTotal


class Venda:
    def __init__(self, codImovel, mesVenda, anoVenda, valorVenda):
        self.__codImovel = codImovel
        self.__mesVenda = mesVenda
        self.__anoVenda = anoVenda
        self.__valorVenda = valorVenda

    def getCodImovel(self):
        return self.__codImovel

    def getMesVenda(self):
        return self.__mesVenda

    def getAnoVenda(self):
        return self.__anoVenda

    def getValorVenda(self):
        return self.__valorVenda


if __name__ == "__main__":
    funcContratado = Contratado(1001, 'João da Silva', 2000, 1234)
    funcContratado.adicionaVenda(100, 3, 2022, 200000)
    funcContratado.adicionaVenda(101, 3, 2022, 300000)
    funcContratado.adicionaVenda(102, 4, 2022, 600000)
    funcComissionado = Comissionado(1002, 'José Santos', 4321, 5)
    funcComissionado.adicionaVenda(200, 3, 2022, 200000)
    funcComissionado.adicionaVenda(201, 3, 2022, 400000)
    funcComissionado.adicionaVenda(202, 4, 2022, 500000)
    listaFunc = [funcContratado, funcComissionado]
    for func in listaFunc:
        print(func.getDados())
        print("Renda no mês 3 de 2022: ")
        print(func.calculaRenda(3, 2022))
