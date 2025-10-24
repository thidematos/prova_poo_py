#Matricula: 2024016073

from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self,  codigo, nome, cargo):
        self.__codigo = codigo
        self.__nome = nome
        self.__cargo = cargo

    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def cargo(self):
        return self.__cargo 
    
    @property
    def nome(self):
        return self.__nome
    
    @abstractmethod
    def calcSalario(self):
        pass

    @abstractmethod
    def lancaFaltas(self, mes, ano, faltas):
        pass

    @abstractmethod
    def lancaAtrasos(self, mes, ano, atrasos):
        pass

    @abstractmethod
    def imprimeFolha(self, mes, ano): 
        pass

    @abstractmethod
    def adicionaPonto(self):
        pass



class Professor(Funcionario):
    def __init__(self, codigo, nome, cargo, salarioHora, nroAulas):
        super().__init__(codigo, nome, cargo)
        self.__salarioHora = salarioHora
        self.__nroAulas = nroAulas
        self.__fichas = []

    @property
    def salarioHora(self):
        return self.__salarioHora
    
    @property
    def nroAulas(self):
        return self.__nroAulas
    
    def adicionaPonto(self, mes, ano, faltas, atrasos):
        self.__fichas.append(PontoFunc(mes, ano, faltas, atrasos))
        

    def calcSalario(self, mes, ano):
        for ficha in self.__fichas:
            if(ficha.mes == mes and ficha.ano == ano):
                curFicha = ficha
            else:
                print('Ficha não encontrada')
                return                
        
        return self.salarioHora * self.nroAulas - self.salarioHora * ficha.faltas   
    
    def lancaAtrasos(self, mes, ano, atrasos):
        for ficha in self.__fichas:
            if(ficha.mes == mes and ficha.ano == ano):
                curFicha = ficha
            
        
        curFicha.addAtraso(atrasos)

    def lancaFaltas(self, mes, ano, faltas):
        for ficha in self.__fichas:
            if(ficha.mes == mes and ficha.ano == ano):
                curFicha = ficha
            
                
        
        curFicha.addFalta(faltas)

    def imprimeFolha(self, mes, ano):
        for ficha in self.__fichas:
            if(ficha.mes == mes and ficha.ano == ano):
                curFicha = ficha
            else:
                print('Ficha não encontrada')
                return
            
        salario = self.calcSalario(mes, ano)   
        if(curFicha.atrasos == 0):
            bonus = salario * 0.10
        else:
            numBonus = 10
            numBonus -= curFicha.atrasos
            if(numBonus > 0):
                bonus = salario * (numBonus / 100)
            else:
                bonus = 0
            
        print(f'Código: {self.codigo}')
        print(f'Nome: {self.nome}')
        print(f'Salário líquido: {salario:.2f}')
        print(f'Bonus: {bonus:.2f}')
    
class TecnicoAdmin(Funcionario):
        def __init__(self, codigo, nome, cargo, salarioMensal):
            super().__init__(codigo, nome, cargo)
            self.__salarioMensal = salarioMensal
            self.__fichas = []

        @property
        def salarioMensal(self):
            return self.__salarioMensal
        
        def adicionaPonto(self, mes, ano, faltas, atrasos):
            self.__fichas.append(PontoFunc(mes, ano, faltas, atrasos))
        
        def calcSalario(self, mes, ano):
            for ficha in self.__fichas:
                if(ficha.mes == mes and ficha.ano == ano):
                    curFicha = ficha
                else:
                    print('Ficha não encontrada')
                    return
            return self.__salarioMensal - ((self.__salarioMensal/30) * curFicha.faltas)
        
        def lancaAtrasos(self, mes, ano, atrasos):
            for ficha in self.__fichas:
                if(ficha.mes == mes and ficha.ano == ano):
                    curFicha = ficha
                curFicha.addAtraso(atrasos)

        def lancaFaltas(self, mes, ano, faltas):
            for ficha in self.__fichas:
                if(ficha.mes == mes and ficha.ano == ano):
                    curFicha = ficha                          
            curFicha.addFalta(faltas)
        
        def imprimeFolha(self, mes, ano):
            for ficha in self.__fichas:
                if(ficha.mes == mes and ficha.ano == ano):
                    curFicha = ficha
                else:
                    print('Ficha não encontrada')
                    return
            
            salario = self.calcSalario(mes, ano)   
            if(curFicha.atrasos == 0):
                bonus = salario * 0.08
            else:
                numBonus = 8
                numBonus -= curFicha.atrasos
                if(numBonus > 0):
                    bonus = salario * (numBonus / 100)
                else:
                    bonus = 0

            print(f'Código: {self.codigo}')
            print(f'Nome: {self.nome}')
            print(f'Salário líquido: {salario:.2f}')
            print(f'Bonus: {bonus:.2f}')

class PontoFunc() :
    def __init__(self, mes, ano, faltas, atrasos):
        self.__atrasos = atrasos
        self.__faltas = faltas
        self.__mes = mes
        self.__ano = ano
        

    @property
    def atrasos(self):
        return self.__atrasos
    
    @property
    def faltas(self):
        return self.__faltas
    
    @property 
    def mes(self):
        return self.__mes
    
    @property
    def ano(self):
        return self.__ano
    
    def addFalta(self, faltas):
        self.__faltas += faltas

    def addAtraso(self, atraso):
        self.__atrasos += atraso

if __name__ == '__main__':
    funcionarios = []

    prof = Professor(1, 'João', 'Doutor', 45.35, 32)
    prof.adicionaPonto(4, 2021, 0, 0)
    prof.lancaFaltas(4, 2021, 2)
    prof.lancaAtrasos(4, 2021, 3)
    funcionarios.append(prof)
    tec = TecnicoAdmin(2, "Pedro", "Analista Contábil", 3600)
    tec.adicionaPonto(4, 2021, 0, 0)
    tec.lancaFaltas(4, 2021, 3)
    tec.lancaAtrasos(4, 2021, 4)
    funcionarios.append(tec)
    for func in funcionarios:
        func.imprimeFolha(4, 2021)
        print()


    

        



