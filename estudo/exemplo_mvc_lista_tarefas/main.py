"""
Aplicação Principal - Lista de Tarefas MVC
Este arquivo inicializa todos os componentes e inicia a aplicação.
"""

import tkinter as tk
from model import ListaTarefasModel
from view import ListaTarefasView
from controller import ListaTarefasController


def main():
    """Função principal que inicializa a aplicação."""

    # Criar a janela principal do Tkinter
    root = tk.Tk()

    # Aplicar tema (opcional - melhora aparência)
    try:
        root.tk.call("source", "azure.tcl")  # Se tiver tema Azure instalado
    except tk.TclError:
        pass  # Usar tema padrão

    # Criar as instâncias do MVC
    model = ListaTarefasModel()          # 1. Model - Dados e lógica
    view = ListaTarefasView(root)        # 2. View - Interface gráfica
    controller = ListaTarefasController(
        model, view)  # 3. Controller - Intermedia

    # Salvar automaticamente ao fechar
    def ao_fechar():
        model.salvar_em_arquivo("tarefas.json")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)

    # Iniciar o loop principal do Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
