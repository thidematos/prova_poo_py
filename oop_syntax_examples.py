"""
Guia de sintaxe de Programação Orientada a Objetos (POO) em Python.

Cada bloco demonstra um conceito central da POO no Python com exemplos concisos.
Execute este arquivo diretamente para ver a saída de cada exemplo.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol


class Pessoa:
    """Classe base com atributos de instância, atributo de classe e métodos."""

    especie = "Homo sapiens"  # Atributo de classe compartilhado por todas as instâncias

    def __init__(self, nome: str, idade: int) -> None:
        self.nome = nome  # Atributo de instância público
        self._idade = idade  # Convenção de atributo "protegido" (uso interno)

    @property
    def idade(self) -> int:
        """Propriedade (getter) para controlar acesso ao atributo."""
        return self._idade

    @idade.setter
    def idade(self, nova_idade: int) -> None:
        """Setter com validação simples."""
        if nova_idade < 0:
            raise ValueError("Idade não pode ser negativa.")
        self._idade = nova_idade

    def apresentar(self) -> str:
        """Método de instância que usa dados do objeto."""
        return f"Olá, eu sou {self.nome} e tenho {self.idade} anos."

    @classmethod
    def definir_especie(cls, especie: str) -> None:
        """Método de classe que altera atributo compartilhado."""
        cls.especie = especie

    @staticmethod
    def eh_adulto(idade: int) -> bool:
        """Método estático independe de estado da classe/instância."""
        return idade >= 18

    def __repr__(self) -> str:
        """Representação formal útil para debugging."""
        return f"Pessoa(nome={self.nome!r}, idade={self.idade!r})"


class Trabalhavel(Protocol):
    """Protocol (similar a interface) descreve métodos esperados."""

    def trabalhar(self) -> str:
        ...


class Funcionario(Pessoa):
    """Exemplo de herança simples com polimorfismo via sobrescrita."""

    def __init__(self, nome: str, idade: int, cargo: str, salario: float) -> None:
        super().__init__(nome, idade)  # Reaproveita lógica da classe base
        self.cargo = cargo
        self.salario = salario

    def apresentar(self) -> str:
        """Polimorfismo: sobrescreve comportamento da classe base."""
        base = super().apresentar()
        return f"{base} Trabalho como {self.cargo}."

    def trabalhar(self) -> str:
        return f"{self.nome} está trabalhando como {self.cargo}."

    def receber_aumento(self, percentual: float) -> None:
        if percentual <= 0:
            raise ValueError("Percentual deve ser positivo.")
        self.salario *= 1 + (percentual / 100)


class LiderancaMixin:
    """Mixin: fornece funcionalidades opcionais para classes que herdarem."""

    def delegar(self, tarefa: str, pessoa: Pessoa) -> str:
        return f"{self.nome} delegou '{tarefa}' para {pessoa.nome}."


class Gerente(Funcionario, LiderancaMixin):
    """Herança múltipla: combina Funcionario com capacidades de liderança."""

    def __init__(self, nome: str, idade: int, salario: float, equipe: list[Funcionario]) -> None:
        super().__init__(nome, idade, cargo="Gerente", salario=salario)
        self.equipe = equipe

    def apresentar(self) -> str:
        """Mais polimorfismo com super() para reutilizar implementações em cascata."""
        base = super().apresentar()
        return f"{base} Lidero uma equipe com {len(self.equipe)} pessoas."


class Documento(ABC):
    """Classe abstrata: define interface obrigatória."""

    @property
    @abstractmethod
    def titulo(self) -> str:
        ...

    @abstractmethod
    def imprimir(self) -> str:
        ...


class Relatorio(Documento):
    """Implementa todos os membros abstratos definidos em Documento."""

    def __init__(self, titulo: str, conteudo: str) -> None:
        self._titulo = titulo
        self.conteudo = conteudo

    @property
    def titulo(self) -> str:
        return self._titulo

    def imprimir(self) -> str:
        return f"=== {self.titulo} ===\n{self.conteudo}"


class Singleton:
    """Exemplo de controle de instanciamento via método especial __new__."""

    _instancia: Singleton | None = None

    def __new__(cls) -> Singleton:
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self) -> None:
        self.configuracoes = {}


def usar_polimorfismo(objetos: list[Trabalhavel]) -> list[str]:
    """Função que aceita qualquer objeto que siga o protocolo Trabalhavel."""
    return [obj.trabalhar() for obj in objetos]


if __name__ == "__main__":
    pessoa = Pessoa("Ana", 25)
    funcionario = Funcionario("Bruno", 30, "Desenvolvedor", 8000.0)
    gerente = Gerente("Clara", 40, 12000.0, equipe=[funcionario])

    print(pessoa.apresentar())
    print(funcionario.apresentar())
    print(gerente.apresentar())

    Pessoa.definir_especie("Humana 2.0")
    print(f"Espécie redefinida: {Pessoa.especie}")

    funcionario.receber_aumento(10)
    print(f"Novo salário: {funcionario.salario:.2f}")

    print(gerente.delegar("Relatório mensal", funcionario))

    relatorio = Relatorio("Resultados Q1", "Lucro líquido cresceu 12%.")
    print(relatorio.imprimir())

    mensagens = usar_polimorfismo([funcionario, gerente])
    print("\n".join(mensagens))

    s1 = Singleton()
    s2 = Singleton()
    print(f"Singleton único? {s1 is s2}")
