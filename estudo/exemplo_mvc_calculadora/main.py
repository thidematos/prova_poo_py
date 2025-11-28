"""
Aplicação Principal - Calculadora MVC
Este arquivo inicializa todos os componentes e inicia a aplicação.
"""

import tkinter as tk
from model import CalculadoraModel
from view import CalculadoraView
from controller import CalculadoraController


def main():
    """Função principal que inicializa a aplicação."""

    # Criar a janela principal do Tkinter
    root = tk.Tk()

    # Criar as instâncias do MVC
    model = CalculadoraModel()      # 1. Model - Lógica de negócio
    view = CalculadoraView(root)    # 2. View - Interface gráfica
    controller = CalculadoraController(
        model, view)  # 3. Controller - Intermedia

    # Iniciar o loop principal do Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
