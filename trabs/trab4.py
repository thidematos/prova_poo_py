from abc import ABC, abstractmethod

class EmpDomestica(ABC):
    def __init__(self, nome, telefone):
        self.__nome = nome
        self.__telefone = telefone

    @property
    def nome(self):
        return self.__nome
    
    @property
    def telefone(self):
        return self.__telefone
    
    @abstractmethod
    def getSalario(self):
        pass

class Horista(EmpDomestica):
    def __init__(self, nome, telefone, horasTrabalhadas, valorPorHora):
        self.__horasTrabalhadas = horasTrabalhadas
        self.__valorPorHora = valorPorHora
        super().__init__(nome, telefone)

    def getSalario(self):
        return self.__valorPorHora * self.__horasTrabalhadas
    
class Diarista(EmpDomestica):
    def __init__(self, nome, telefone, diasTrabalhados, valorPorDia):
        self.__diasTrabalhados = diasTrabalhados
        self.__valorPorDia = valorPorDia
        super().__init__(nome, telefone)

    def getSalario(self):
        return self.__diasTrabalhados * self.__valorPorDia
    
class Mensalista(EmpDomestica):
    def __init__(self, nome, telefone, valorMensal):
        self.__valorMensal = valorMensal
        super().__init__(nome, telefone)

    def getSalario(self):
        return self.__valorMensal
    
def findMostRentable():
    employes = [Horista('Thigas', 11112222, 160, 12), Diarista('Thugas', 11112222, 20, 65), Mensalista('Thogas', 11112222, 1200)]

    mostRentable = employes[0]

    for employ in employes:
        print('Salário: {}'.format(employ.getSalario()))
        if(employ.getSalario() > mostRentable.getSalario()):
            mostRentable = employ

    print('Opção mais barata:')
    print(f'Nome: {mostRentable.nome}, Tel.: {mostRentable.telefone}, Salário: {mostRentable.getSalario()}')


findMostRentable()
        








