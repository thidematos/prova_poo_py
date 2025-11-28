"""
View - Calculadora
Responsável pela interface gráfica (GUI).
"""

import tkinter as tk
from tkinter import ttk, messagebox


class CalculadoraView:
    """View da calculadora - Interface gráfica."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora MVC")
        self.root.geometry("350x400")
        self.root.resizable(False, False)

        # Variáveis de controle do Tkinter
        self.numero1_var = tk.StringVar()
        self.numero2_var = tk.StringVar()
        self.resultado_var = tk.StringVar(value="0")

        # Callback para o controller (será definido pelo controller)
        self.on_calcular = None
        self.on_limpar = None

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria todos os widgets da interface."""

        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === SEÇÃO DE ENTRADA ===
        input_frame = ttk.LabelFrame(main_frame, text="Entrada", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Número 1
        ttk.Label(input_frame, text="Número 1:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.entry_num1 = ttk.Entry(
            input_frame, textvariable=self.numero1_var, width=20)
        self.entry_num1.grid(row=0, column=1, pady=5, padx=(10, 0))

        # Número 2
        ttk.Label(input_frame, text="Número 2:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.entry_num2 = ttk.Entry(
            input_frame, textvariable=self.numero2_var, width=20)
        self.entry_num2.grid(row=1, column=1, pady=5, padx=(10, 0))

        # === SEÇÃO DE OPERAÇÕES ===
        op_frame = ttk.LabelFrame(main_frame, text="Operações", padding="10")
        op_frame.pack(fill=tk.X, pady=(0, 10))

        # Botões de operação
        self.btn_somar = ttk.Button(op_frame, text="+", width=5,
                                    command=lambda: self._executar_operacao("somar"))
        self.btn_somar.grid(row=0, column=0, padx=5, pady=5)

        self.btn_subtrair = ttk.Button(op_frame, text="-", width=5,
                                       command=lambda: self._executar_operacao("subtrair"))
        self.btn_subtrair.grid(row=0, column=1, padx=5, pady=5)

        self.btn_multiplicar = ttk.Button(op_frame, text="×", width=5,
                                          command=lambda: self._executar_operacao("multiplicar"))
        self.btn_multiplicar.grid(row=0, column=2, padx=5, pady=5)

        self.btn_dividir = ttk.Button(op_frame, text="÷", width=5,
                                      command=lambda: self._executar_operacao("dividir"))
        self.btn_dividir.grid(row=0, column=3, padx=5, pady=5)

        self.btn_limpar = ttk.Button(op_frame, text="Limpar", width=10,
                                     command=self._executar_limpar)
        self.btn_limpar.grid(row=0, column=4, padx=5, pady=5)

        # === SEÇÃO DE RESULTADO ===
        result_frame = ttk.LabelFrame(
            main_frame, text="Resultado", padding="10")
        result_frame.pack(fill=tk.X, pady=(0, 10))

        self.label_resultado = ttk.Label(result_frame, textvariable=self.resultado_var,
                                         font=("Arial", 24, "bold"), anchor=tk.CENTER)
        self.label_resultado.pack(fill=tk.X)

        # === SEÇÃO DE HISTÓRICO ===
        hist_frame = ttk.LabelFrame(main_frame, text="Histórico", padding="10")
        hist_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox com scrollbar
        scrollbar = ttk.Scrollbar(hist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_historico = tk.Listbox(hist_frame, yscrollcommand=scrollbar.set,
                                            height=6, font=("Consolas", 10))
        self.listbox_historico.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_historico.yview)

    def _executar_operacao(self, operacao: str):
        """Chama o callback do controller para executar uma operação."""
        if self.on_calcular:
            self.on_calcular(operacao)

    def _executar_limpar(self):
        """Chama o callback do controller para limpar."""
        if self.on_limpar:
            self.on_limpar()

    # === MÉTODOS PÚBLICOS PARA O CONTROLLER ===

    def get_numero1(self) -> str:
        """Retorna o valor do campo número 1."""
        return self.numero1_var.get()

    def get_numero2(self) -> str:
        """Retorna o valor do campo número 2."""
        return self.numero2_var.get()

    def set_resultado(self, valor: str):
        """Define o valor do resultado."""
        self.resultado_var.set(valor)

    def limpar_campos(self):
        """Limpa todos os campos de entrada."""
        self.numero1_var.set("")
        self.numero2_var.set("")
        self.resultado_var.set("0")

    def atualizar_historico(self, historico: list):
        """Atualiza a listbox do histórico."""
        self.listbox_historico.delete(0, tk.END)
        for item in historico:
            self.listbox_historico.insert(tk.END, item)
        # Scroll para o último item
        self.listbox_historico.see(tk.END)

    def mostrar_erro(self, titulo: str, mensagem: str):
        """Exibe uma mensagem de erro."""
        messagebox.showerror(titulo, mensagem)

    def mostrar_info(self, titulo: str, mensagem: str):
        """Exibe uma mensagem informativa."""
        messagebox.showinfo(titulo, mensagem)
