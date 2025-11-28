"""
Model - Calculadora
Responsável pela lógica de cálculo e armazenamento de dados.
"""


class CalculadoraModel:
    """Modelo da calculadora que contém a lógica de negócio."""

    def __init__(self):
        self._resultado = 0
        self._historico = []

    @property
    def resultado(self):
        """Retorna o resultado atual."""
        return self._resultado

    @property
    def historico(self):
        """Retorna o histórico de operações."""
        return self._historico.copy()

    def somar(self, a: float, b: float) -> float:
        """Realiza a soma de dois números."""
        self._resultado = a + b
        self._registrar_operacao(f"{a} + {b} = {self._resultado}")
        return self._resultado

    def subtrair(self, a: float, b: float) -> float:
        """Realiza a subtração de dois números."""
        self._resultado = a - b
        self._registrar_operacao(f"{a} - {b} = {self._resultado}")
        return self._resultado

    def multiplicar(self, a: float, b: float) -> float:
        """Realiza a multiplicação de dois números."""
        self._resultado = a * b
        self._registrar_operacao(f"{a} × {b} = {self._resultado}")
        return self._resultado

    def dividir(self, a: float, b: float) -> float:
        """Realiza a divisão de dois números."""
        if b == 0:
            raise ValueError("Divisão por zero não é permitida!")
        self._resultado = a / b
        self._registrar_operacao(f"{a} ÷ {b} = {self._resultado}")
        return self._resultado

    def limpar(self):
        """Limpa o resultado atual."""
        self._resultado = 0

    def limpar_historico(self):
        """Limpa o histórico de operações."""
        self._historico.clear()

    def _registrar_operacao(self, operacao: str):
        """Registra uma operação no histórico."""
        self._historico.append(operacao)
