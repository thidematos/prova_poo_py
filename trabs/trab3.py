from abc import ABC, abstractmethod
import math



class FormaGeo(ABC):
    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def area():
        pass

    @abstractmethod
    def perimetro():
        pass

    @abstractmethod
    def printDados():
        pass

class Retangulo(FormaGeo):
    def __init__(self, nome, altura, base):
        super().__init__(nome)
        self.__altura = altura
        self.__base = base

    @property 
    def altura(self):
        return self.__altura
    
    def area(self):
        return self.__altura * self.__base
    
    def perimetro(self):
        return 2 * (self.__altura + self.__base)

    def printDados(self):
        print('Nome: {}'.format(self.nome))
        print('Area: {}'.format(self.area()))
        print('Perimetro: {}'.format(self.perimetro()))



class Circulo(FormaGeo):
    def __init__(self, nome, raio):
        super().__init__(nome)
        self.__raio = raio
       

    @property 
    def raio(self):
        return self.__raio
    
    def area(self):
        return math.pi *  math.pow(self.__raio, 2)
     
    def perimetro(self):
        return 2 * math.pi * self.__raio

    def printDados(self):
        print('Nome: {}'.format(self.nome))
        print('Area: {}'.format(self.area()))
        print('Perimetro: {}'.format(self.perimetro()))

class HexagonoRegular(FormaGeo):
    def __init__(self, nome, lado):
        super().__init__(nome)
        self.__lado = lado
       

    @property 
    def lado(self):
        return self.__lado

    def area(self):
        return (3 * (math.pow(self.__lado, 2)) * math.sqrt(3)) / 2
     
    def perimetro(self):
        return 6 * self.__lado

    def printDados(self):
        print('Nome: {}'.format(self.nome))
        print('Area: {}'.format(self.area()))
        print('Perimetro: {}'.format(self.perimetro()))

if __name__ == "__main__":
    hexagono = HexagonoRegular('HexReg1', 6)
    hexagono.printDados()

    circulo = Circulo('Circ', 2.5)
    circulo.printDados()

    retangulo = Retangulo('Ret', 4, 2)
    retangulo.printDados()

