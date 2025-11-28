"""
Controller - Calculadora
Responsável por intermediar a comunicação entre Model e View.
"""

from model import CalculadoraModel
from view import CalculadoraView


class CalculadoraController:
    """Controller da calculadora - Intermedia Model e View."""

    def __init__(self, model: CalculadoraModel, view: CalculadoraView):
        self.model = model
        self.view = view

        # Conectar os callbacks da View ao Controller
        self.view.on_calcular = self.calcular
        self.view.on_limpar = self.limpar

    def calcular(self, operacao: str):
        """
        Executa o cálculo baseado na operação selecionada.

        Args:
            operacao: Nome da operação ('somar', 'subtrair', 'multiplicar', 'dividir')
        """
        try:
            # Obter valores da View
            num1_str = self.view.get_numero1()
            num2_str = self.view.get_numero2()

            # Validar entrada
            if not num1_str or not num2_str:
                self.view.mostrar_erro(
                    "Erro", "Por favor, preencha ambos os números!")
                return

            # Converter para float
            try:
                num1 = float(num1_str.replace(",", "."))
                num2 = float(num2_str.replace(",", "."))
            except ValueError:
                self.view.mostrar_erro(
                    "Erro", "Por favor, insira números válidos!")
                return

            # Executar operação no Model
            resultado = self._executar_operacao(operacao, num1, num2)

            if resultado is not None:
                # Formatar resultado
                if resultado == int(resultado):
                    resultado_formatado = str(int(resultado))
                else:
                    resultado_formatado = f"{resultado:.4f}".rstrip(
                        '0').rstrip('.')

                # Atualizar View
                self.view.set_resultado(resultado_formatado)
                self.view.atualizar_historico(self.model.historico)

        except ValueError as e:
            self.view.mostrar_erro("Erro de Cálculo", str(e))
        except Exception as e:
            self.view.mostrar_erro(
                "Erro Inesperado", f"Ocorreu um erro: {str(e)}")

    def _executar_operacao(self, operacao: str, num1: float, num2: float) -> float:
        """
        Executa a operação matemática no Model.

        Args:
            operacao: Nome da operação
            num1: Primeiro número
            num2: Segundo número

        Returns:
            Resultado da operação
        """
        operacoes = {
            "somar": self.model.somar,
            "subtrair": self.model.subtrair,
            "multiplicar": self.model.multiplicar,
            "dividir": self.model.dividir
        }

        if operacao in operacoes:
            return operacoes[operacao](num1, num2)
        else:
            raise ValueError(f"Operação desconhecida: {operacao}")

    def limpar(self):
        """Limpa os campos e o histórico."""
        self.model.limpar()
        self.model.limpar_historico()
        self.view.limpar_campos()
        self.view.atualizar_historico([])
