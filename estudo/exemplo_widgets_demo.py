"""
Demonstração de Todos os Widgets do Tkinter
Este arquivo mostra exemplos de uso de cada widget principal.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser


class WidgetsDemo:
    """Aplicação demonstrando todos os widgets principais do Tkinter."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Demo de Widgets Tkinter")
        self.root.geometry("800x600")

        # Criar notebook (abas) para organizar widgets
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Criar cada aba
        self._criar_aba_basicos()
        self._criar_aba_entrada()
        self._criar_aba_selecao()
        self._criar_aba_containers()
        self._criar_aba_dialogos()

    # =====================================================
    # ABA 1: WIDGETS BÁSICOS
    # =====================================================
    def _criar_aba_basicos(self):
        """Cria aba com widgets básicos."""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="Básicos")

        # ----- LABEL -----
        ttk.Label(frame, text="LABEL (Rótulo)", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        # Label simples
        label1 = ttk.Label(frame, text="Este é um Label simples")
        label1.pack(anchor=tk.W, pady=(5, 0))

        # Label com estilo
        label2 = tk.Label(frame, text="Label com cores personalizadas",
                          fg="white", bg="darkblue", font=("Arial", 10), padx=10, pady=5)
        label2.pack(anchor=tk.W, pady=(5, 15))

        # ----- BUTTON -----
        ttk.Label(frame, text="BUTTON (Botão)", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(anchor=tk.W, pady=5)

        # Botão normal
        btn1 = ttk.Button(btn_frame, text="Botão Normal",
                          command=lambda: messagebox.showinfo("Info", "Você clicou!"))
        btn1.pack(side=tk.LEFT, padx=(0, 10))

        # Botão desabilitado
        btn2 = ttk.Button(btn_frame, text="Desabilitado", state=tk.DISABLED)
        btn2.pack(side=tk.LEFT, padx=(0, 10))

        # Botão com estilo tk (cores)
        btn3 = tk.Button(btn_frame, text="Colorido", bg="green", fg="white",
                         activebackground="darkgreen", activeforeground="white")
        btn3.pack(side=tk.LEFT)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # ----- CANVAS -----
        ttk.Label(frame, text="CANVAS (Desenho)", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        canvas = tk.Canvas(frame, width=300, height=100, bg="white",
                           highlightthickness=1, highlightbackground="gray")
        canvas.pack(anchor=tk.W, pady=5)

        # Desenhar formas
        canvas.create_rectangle(10, 10, 60, 60, fill="red", outline="darkred")
        canvas.create_oval(70, 10, 130, 60, fill="blue", outline="darkblue")
        canvas.create_line(140, 35, 200, 10, 200, 60,
                           260, 35, fill="green", width=2)
        canvas.create_text(280, 35, text="Texto", font=("Arial", 12))

    # =====================================================
    # ABA 2: WIDGETS DE ENTRADA
    # =====================================================
    def _criar_aba_entrada(self):
        """Cria aba com widgets de entrada de dados."""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="Entrada")

        # ----- ENTRY -----
        ttk.Label(frame, text="ENTRY (Campo de Texto)",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W)

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(anchor=tk.W, pady=5)

        ttk.Label(entry_frame, text="Normal:").grid(
            row=0, column=0, sticky=tk.W)
        self.entry_normal = ttk.Entry(entry_frame, width=30)
        self.entry_normal.grid(row=0, column=1, padx=(10, 0))
        self.entry_normal.insert(0, "Digite aqui...")

        ttk.Label(entry_frame, text="Senha:").grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.entry_senha = ttk.Entry(entry_frame, width=30, show="•")
        self.entry_senha.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))

        ttk.Label(entry_frame, text="Somente leitura:").grid(
            row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.entry_readonly = ttk.Entry(
            entry_frame, width=30, state="readonly")
        self.entry_readonly.grid(row=2, column=1, padx=(10, 0), pady=(5, 0))

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # ----- TEXT -----
        ttk.Label(frame, text="TEXT (Área de Texto Multilinha)",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W)

        text_frame = ttk.Frame(frame)
        text_frame.pack(anchor=tk.W, pady=5, fill=tk.X)

        self.text_area = tk.Text(text_frame, width=50,
                                 height=6, wrap=tk.WORD, font=("Consolas", 10))
        self.text_area.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

        self.text_area.insert(tk.END, "Este é um widget Text.\n")
        self.text_area.insert(tk.END, "Permite múltiplas linhas de texto.\n")
        self.text_area.insert(tk.END, "Suporta formatação e tags.")

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # ----- SPINBOX -----
        ttk.Label(frame, text="SPINBOX (Campo Numérico)",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W)

        spin_frame = ttk.Frame(frame)
        spin_frame.pack(anchor=tk.W, pady=5)

        ttk.Label(spin_frame, text="Idade:").pack(side=tk.LEFT)
        self.spinbox = ttk.Spinbox(spin_frame, from_=0, to=120, width=10)
        self.spinbox.pack(side=tk.LEFT, padx=(10, 0))
        self.spinbox.set(25)

    # =====================================================
    # ABA 3: WIDGETS DE SELEÇÃO
    # =====================================================
    def _criar_aba_selecao(self):
        """Cria aba com widgets de seleção."""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="Seleção")

        # Layout em duas colunas
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 20))

        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.LEFT, anchor=tk.N)

        # ----- CHECKBUTTON -----
        ttk.Label(left_frame, text="CHECKBUTTON", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        self.check_vars = [tk.BooleanVar() for _ in range(3)]
        opcoes = ["Opção A", "Opção B", "Opção C"]

        for var, texto in zip(self.check_vars, opcoes):
            cb = ttk.Checkbutton(left_frame, text=texto, variable=var)
            cb.pack(anchor=tk.W)

        self.check_vars[0].set(True)  # Marcar primeira opção

        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=20)

        # ----- RADIOBUTTON -----
        ttk.Label(left_frame, text="RADIOBUTTON", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        self.radio_var = tk.StringVar(value="opcao1")
        opcoes_radio = [("Opção 1", "opcao1"), ("Opção 2",
                                                "opcao2"), ("Opção 3", "opcao3")]

        for texto, valor in opcoes_radio:
            rb = ttk.Radiobutton(left_frame, text=texto,
                                 variable=self.radio_var, value=valor)
            rb.pack(anchor=tk.W)

        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=20)

        # ----- SCALE -----
        ttk.Label(left_frame, text="SCALE (Slider)", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        self.scale_var = tk.IntVar(value=50)
        scale = ttk.Scale(left_frame, from_=0, to=100, variable=self.scale_var,
                          orient=tk.HORIZONTAL, length=200)
        scale.pack(anchor=tk.W, pady=5)

        self.scale_label = ttk.Label(left_frame, text="Valor: 50")
        self.scale_label.pack(anchor=tk.W)

        scale.config(command=lambda v: self.scale_label.config(
            text=f"Valor: {int(float(v))}"))

        # ----- LISTBOX -----
        ttk.Label(right_frame, text="LISTBOX", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        listbox_frame = ttk.Frame(right_frame)
        listbox_frame.pack(anchor=tk.W, pady=5)

        self.listbox = tk.Listbox(
            listbox_frame, width=25, height=6, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT)

        lb_scroll = ttk.Scrollbar(
            listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        lb_scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=lb_scroll.set)

        for i in range(1, 11):
            self.listbox.insert(tk.END, f"Item {i}")

        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=20)

        # ----- COMBOBOX -----
        ttk.Label(right_frame, text="COMBOBOX", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        self.combo = ttk.Combobox(right_frame, values=["Python", "Java", "C++", "JavaScript"],
                                  width=22, state="readonly")
        self.combo.pack(anchor=tk.W, pady=5)
        self.combo.set("Selecione uma linguagem")

    # =====================================================
    # ABA 4: CONTAINERS
    # =====================================================
    def _criar_aba_containers(self):
        """Cria aba demonstrando containers."""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="Containers")

        # ----- FRAME -----
        ttk.Label(frame, text="FRAME (Container básico)",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W)

        demo_frame = ttk.Frame(frame, borderwidth=2,
                               relief=tk.GROOVE, padding="10")
        demo_frame.pack(anchor=tk.W, pady=5, fill=tk.X)

        ttk.Label(demo_frame, text="Conteúdo dentro de um Frame").pack()
        ttk.Button(demo_frame, text="Botão no Frame").pack(pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # ----- LABELFRAME -----
        ttk.Label(frame, text="LABELFRAME (Frame com título)",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W)

        label_frame = ttk.LabelFrame(frame, text="Configurações", padding="10")
        label_frame.pack(anchor=tk.W, pady=5, fill=tk.X)

        ttk.Checkbutton(label_frame, text="Ativar recurso").pack(anchor=tk.W)
        ttk.Checkbutton(
            label_frame, text="Mostrar notificações").pack(anchor=tk.W)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # ----- PANEDWINDOW -----
        ttk.Label(frame, text="PANEDWINDOW (Painéis redimensionáveis)",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W)

        paned = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=5)

        pane1 = ttk.Frame(paned, borderwidth=2, relief=tk.SUNKEN)
        pane1.pack(fill=tk.BOTH, expand=True)
        ttk.Label(pane1, text="Painel 1", padding="20").pack()

        pane2 = ttk.Frame(paned, borderwidth=2, relief=tk.SUNKEN)
        pane2.pack(fill=tk.BOTH, expand=True)
        ttk.Label(pane2, text="Painel 2", padding="20").pack()

        paned.add(pane1, weight=1)
        paned.add(pane2, weight=1)

    # =====================================================
    # ABA 5: DIÁLOGOS
    # =====================================================
    def _criar_aba_dialogos(self):
        """Cria aba demonstrando diálogos."""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="Diálogos")

        ttk.Label(frame, text="DIÁLOGOS PADRÃO", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(frame, text="Clique nos botões para ver cada tipo de diálogo:").pack(
            anchor=tk.W, pady=(0, 10))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(anchor=tk.W)

        # Messagebox
        ttk.Button(btn_frame, text="Info",
                   command=lambda: messagebox.showinfo(
                       "Informação", "Esta é uma mensagem de informação.")
                   ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(btn_frame, text="Warning",
                   command=lambda: messagebox.showwarning(
                       "Aviso", "Esta é uma mensagem de aviso!")
                   ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(btn_frame, text="Error",
                   command=lambda: messagebox.showerror(
                       "Erro", "Esta é uma mensagem de erro!")
                   ).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(btn_frame, text="Yes/No",
                   command=lambda: messagebox.showinfo("Resultado",
                                                       "Você clicou: SIM" if messagebox.askyesno("Confirmar", "Deseja continuar?") else "Você clicou: NÃO")
                   ).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(btn_frame, text="Ok/Cancel",
                   command=lambda: messagebox.showinfo("Resultado",
                                                       "OK" if messagebox.askokcancel("Confirmar", "Continuar?") else "Cancelado")
                   ).grid(row=1, column=1, padx=5, pady=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # File dialogs
        ttk.Label(frame, text="DIÁLOGOS DE ARQUIVO", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        file_frame = ttk.Frame(frame)
        file_frame.pack(anchor=tk.W, pady=10)

        def abrir_arquivo():
            arquivo = filedialog.askopenfilename(
                title="Selecione um arquivo",
                filetypes=[("Arquivos Python", "*.py"),
                           ("Todos os arquivos", "*.*")]
            )
            if arquivo:
                messagebox.showinfo("Arquivo", f"Selecionado: {arquivo}")

        def salvar_arquivo():
            arquivo = filedialog.asksaveasfilename(
                title="Salvar como",
                defaultextension=".txt",
                filetypes=[("Arquivo de texto", "*.txt"),
                           ("Todos os arquivos", "*.*")]
            )
            if arquivo:
                messagebox.showinfo("Arquivo", f"Salvando em: {arquivo}")

        def selecionar_pasta():
            pasta = filedialog.askdirectory(title="Selecione uma pasta")
            if pasta:
                messagebox.showinfo("Pasta", f"Selecionada: {pasta}")

        ttk.Button(file_frame, text="Abrir Arquivo",
                   command=abrir_arquivo).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Salvar Arquivo",
                   command=salvar_arquivo).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Selecionar Pasta",
                   command=selecionar_pasta).pack(side=tk.LEFT, padx=5)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        # Color chooser
        ttk.Label(frame, text="SELETOR DE COR", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)

        color_frame = ttk.Frame(frame)
        color_frame.pack(anchor=tk.W, pady=10)

        self.color_label = tk.Label(color_frame, text="   Cor selecionada   ", bg="white",
                                    relief=tk.SUNKEN, width=20)
        self.color_label.pack(side=tk.LEFT, padx=(0, 10))

        def escolher_cor():
            cor = colorchooser.askcolor(title="Escolha uma cor")
            if cor[1]:
                self.color_label.config(bg=cor[1])

        ttk.Button(color_frame, text="Escolher Cor",
                   command=escolher_cor).pack(side=tk.LEFT)


def main():
    """Função principal."""
    root = tk.Tk()
    app = WidgetsDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
