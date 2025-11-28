#Thiago Luiz de Matos - 2024016073

from abc import ABC, abstractmethod

class IdadeException(Exception):
    def __init__(self, message="Idade inválida"):
        super().__init__(message)

class TitulacaoException(Exception):
    def __init__(self, message="Titulação inválida"):
        super().__init__(message)

class CursoException(Exception):
    def __init__(self, message="Curso inválido"):
        super().__init__(message)

class CpfException(Exception):
    def __init__(self, message="CPF já existe"):
        super().__init__(message)

class Pessoa(ABC):
    def __init__(self, nome, endereco, idade, cpf):
        self.__nome = nome
        self.__endereco = endereco
        self.__idade = idade
        self.__cpf = cpf
        
    def getNome(self):
        return self.__nome

    def getCpf(self):
        return self.__cpf

    def getEndereco(self):
        return self.__endereco

    def getIdade(self):
        return self.__idade
    
    @abstractmethod
    def printDescricao(self): 
        pass

class Professor(Pessoa):
    def __init__(self, nome, endereco, idade, cpf, titulacao):
        if idade < 30:
            raise IdadeException('Professor deve ter no mínimo 30 anos.')
        if titulacao != 'Doutor':
            raise TitulacaoException('Professor deve ter titulação "Doutor".') 
            
        super().__init__(nome, endereco, idade, cpf) 
        self.__titulacao = titulacao

    def getTitulacao(self):
        return self.__titulacao
    
    def printDescricao(self):
        print(f'Professor: {self.getNome()} | Idade: {self.getIdade()} | CPF: {self.getCpf()} | Titulação: {self.getTitulacao()} ')

        
class Aluno(Pessoa):
    def __init__(self, nome, endereco, idade, cpf, curso):  
        
        if idade < 18:
            raise IdadeException('Aluno deve ter no mínimo 18 anos.')      
        
        if curso != 'SIN' and curso != 'CCO':
            raise CursoException('Curso deve ser "SIN" ou "CCO".')

        super().__init__(nome, endereco, idade, cpf)
        self.__curso = curso

    def getCurso(self):
        return self.__curso  
    
    def printDescricao(self):
        print(f'Aluno: {self.getNome()} | Idade: {self.getIdade()} | CPF: {self.getCpf()} | Curso: {self.getCurso()} ')

if __name__ == "__main__":
    lista = [
        Aluno('Thiago', 'xxxxx', 25, 1111, 'SIN'), 
        Aluno('Maria', 'xxxxx', 20, 2222, 'ECO'), 
        Aluno('Joao', 'xxxxx', 21, 3333, 'CCO'), 
        Professor('Rodrigo', 'xxxx', 43, 4444, 'Doutor'),
        Professor('Isabela', 'xxxx', 28, 5555, 'Doutor'), 
        Aluno('Thiago', 'xxxxx', 25, 1111, 'SIN') 
    ]
    
    lista_cpf_duplicado = [
        Aluno('Thiago', 'xxxxx', 25, 1111, 'SIN'), 
        Aluno('Pedro', 'xxxxx', 22, 2222, 'CCO'),
        Aluno('Maria', 'xxxxx', 20, 1111, 'SIN') 
    ]

    lista_a_usar = lista_cpf_duplicado
    
    listaVerificada = []
    listaCpfs = []
    
    try:
        for el in lista_a_usar:
            if el.getCpf() in listaCpfs:
                raise CpfException()
                
            el.printDescricao()
            listaCpfs.append(el.getCpf())
            listaVerificada.append(el)
            
    except Exception as e:
        print(f"ERRO: {e}")
        print(f"CPFs processados com sucesso: {listaCpfs}")