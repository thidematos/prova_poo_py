"""
View - Lista de Tarefas
Responsável pela interface gráfica.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional


class ListaTarefasView:
    """View da lista de tarefas."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Lista de Tarefas - MVC")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        # Variáveis de controle
        self.titulo_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.filtro_var = tk.StringVar(value="todas")

        # Callbacks do controller
        self.on_adicionar: Optional[Callable] = None
        self.on_remover: Optional[Callable] = None
        self.on_toggle_status: Optional[Callable] = None
        self.on_editar: Optional[Callable] = None
        self.on_filtrar: Optional[Callable] = None
        self.on_salvar: Optional[Callable] = None
        self.on_carregar: Optional[Callable] = None

        self._criar_widgets()
        self._configurar_bindings()

    def _criar_widgets(self):
        """Cria todos os widgets da interface."""

        # === BARRA DE MENU ===
        self._criar_menu()

        # === FRAME PRINCIPAL ===
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # === SEÇÃO DE ENTRADA ===
        self._criar_secao_entrada(main_frame)

        # === SEÇÃO DE FILTROS ===
        self._criar_secao_filtros(main_frame)

        # === SEÇÃO DA LISTA ===
        self._criar_secao_lista(main_frame)

        # === BARRA DE STATUS ===
        self._criar_barra_status()

    def _criar_menu(self):
        """Cria a barra de menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Salvar", command=self._executar_salvar)
        arquivo_menu.add_command(
            label="Carregar", command=self._executar_carregar)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)

    def _criar_secao_entrada(self, parent):
        """Cria a seção de entrada de nova tarefa."""
        input_frame = ttk.LabelFrame(parent, text="Nova Tarefa", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Grid para layout organizado
        input_frame.columnconfigure(1, weight=1)

        # Título
        ttk.Label(input_frame, text="Título:").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        self.entry_titulo = ttk.Entry(
            input_frame, textvariable=self.titulo_var)
        self.entry_titulo.grid(
            row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=2)

        # Descrição
        ttk.Label(input_frame, text="Descrição:").grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self.entry_descricao = ttk.Entry(
            input_frame, textvariable=self.descricao_var)
        self.entry_descricao.grid(
            row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=2)

        # Botão Adicionar
        self.btn_adicionar = ttk.Button(input_frame, text="Adicionar Tarefa",
                                        command=self._executar_adicionar)
        self.btn_adicionar.grid(row=2, column=0, columnspan=2, pady=(10, 0))

    def _criar_secao_filtros(self, parent):
        """Cria a seção de filtros."""
        filtro_frame = ttk.Frame(parent)
        filtro_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filtro_frame, text="Filtrar:").pack(side=tk.LEFT)

        filtros = [("Todas", "todas"), ("Pendentes", "pendentes"),
                   ("Concluídas", "concluidas")]
        for texto, valor in filtros:
            rb = ttk.Radiobutton(filtro_frame, text=texto, variable=self.filtro_var,
                                 value=valor, command=self._executar_filtrar)
            rb.pack(side=tk.LEFT, padx=(10, 0))

    def _criar_secao_lista(self, parent):
        """Cria a seção da lista de tarefas."""
        lista_frame = ttk.LabelFrame(parent, text="Tarefas", padding="10")
        lista_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview para exibir tarefas
        columns = ("id", "titulo", "status", "data")
        self.tree = ttk.Treeview(
            lista_frame, columns=columns, show="headings", selectmode="browse")

        # Configurar colunas
        self.tree.heading("id", text="ID")
        self.tree.heading("titulo", text="Título")
        self.tree.heading("status", text="Status")
        self.tree.heading("data", text="Data Criação")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("titulo", width=200)
        self.tree.column("status", width=80, anchor=tk.CENTER)
        self.tree.column("data", width=120, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame de botões de ação
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        self.btn_toggle = ttk.Button(btn_frame, text="✓ Marcar/Desmarcar",
                                     command=self._executar_toggle)
        self.btn_toggle.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_editar = ttk.Button(btn_frame, text="✎ Editar",
                                     command=self._executar_editar)
        self.btn_editar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_remover = ttk.Button(btn_frame, text="✕ Remover",
                                      command=self._executar_remover)
        self.btn_remover.pack(side=tk.LEFT)

    def _criar_barra_status(self):
        """Cria a barra de status."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.label_status = ttk.Label(self.status_frame, text="Total: 0 | Pendentes: 0 | Concluídas: 0",
                                      relief=tk.SUNKEN, padding=(5, 2))
        self.label_status.pack(fill=tk.X)

    def _configurar_bindings(self):
        """Configura atalhos de teclado."""
        self.entry_titulo.bind(
            "<Return>", lambda e: self._executar_adicionar())
        self.entry_descricao.bind(
            "<Return>", lambda e: self._executar_adicionar())
        self.tree.bind("<Double-1>", lambda e: self._executar_toggle())
        self.tree.bind("<Delete>", lambda e: self._executar_remover())

    # === MÉTODOS DE EXECUÇÃO (chamam callbacks) ===

    def _executar_adicionar(self):
        if self.on_adicionar:
            self.on_adicionar()

    def _executar_remover(self):
        if self.on_remover:
            self.on_remover()

    def _executar_toggle(self):
        if self.on_toggle_status:
            self.on_toggle_status()

    def _executar_editar(self):
        if self.on_editar:
            self.on_editar()

    def _executar_filtrar(self):
        if self.on_filtrar:
            self.on_filtrar()

    def _executar_salvar(self):
        if self.on_salvar:
            self.on_salvar()

    def _executar_carregar(self):
        if self.on_carregar:
            self.on_carregar()

    # === MÉTODOS PÚBLICOS PARA O CONTROLLER ===

    def get_titulo(self) -> str:
        """Retorna o título digitado."""
        return self.titulo_var.get().strip()

    def get_descricao(self) -> str:
        """Retorna a descrição digitada."""
        return self.descricao_var.get().strip()

    def get_filtro(self) -> str:
        """Retorna o filtro selecionado."""
        return self.filtro_var.get()

    def get_tarefa_selecionada(self) -> Optional[int]:
        """Retorna o ID da tarefa selecionada ou None."""
        selecao = self.tree.selection()
        if selecao:
            item = self.tree.item(selecao[0])
            return int(item["values"][0])
        return None

    def limpar_entrada(self):
        """Limpa os campos de entrada."""
        self.titulo_var.set("")
        self.descricao_var.set("")
        self.entry_titulo.focus()

    def atualizar_lista(self, tarefas: list):
        """Atualiza a lista de tarefas exibida."""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Adicionar tarefas
        for tarefa in tarefas:
            status = "✓ Concluída" if tarefa.concluida else "○ Pendente"
            tag = "concluida" if tarefa.concluida else "pendente"

            self.tree.insert("", tk.END, values=(
                tarefa.id,
                tarefa.titulo,
                status,
                tarefa.data_criacao
            ), tags=(tag,))

        # Configurar cores das tags
        self.tree.tag_configure("concluida", foreground="gray")
        self.tree.tag_configure("pendente", foreground="black")

    def atualizar_status(self, contagem: dict):
        """Atualiza a barra de status."""
        texto = f"Total: {contagem['total']} | Pendentes: {contagem['pendentes']} | Concluídas: {contagem['concluidas']}"
        self.label_status.config(text=texto)

    def mostrar_dialogo_edicao(self, titulo: str, descricao: str) -> Optional[tuple]:
        """Exibe diálogo para editar tarefa."""
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Editar Tarefa")
        dialogo.geometry("400x150")
        dialogo.transient(self.root)
        dialogo.grab_set()

        resultado = {"confirmado": False, "titulo": "", "descricao": ""}

        frame = ttk.Frame(dialogo, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Título:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        entry_titulo = ttk.Entry(frame, width=40)
        entry_titulo.insert(0, titulo)
        entry_titulo.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Descrição:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        entry_descricao = ttk.Entry(frame, width=40)
        entry_descricao.insert(0, descricao)
        entry_descricao.grid(row=1, column=1, pady=5)

        def confirmar():
            resultado["confirmado"] = True
            resultado["titulo"] = entry_titulo.get().strip()
            resultado["descricao"] = entry_descricao.get().strip()
            dialogo.destroy()

        def cancelar():
            dialogo.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(btn_frame, text="Salvar", command=confirmar).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar",
                   command=cancelar).pack(side=tk.LEFT, padx=5)

        dialogo.wait_window()

        if resultado["confirmado"]:
            return (resultado["titulo"], resultado["descricao"])
        return None

    def mostrar_erro(self, titulo: str, mensagem: str):
        """Exibe mensagem de erro."""
        messagebox.showerror(titulo, mensagem)

    def mostrar_info(self, titulo: str, mensagem: str):
        """Exibe mensagem informativa."""
        messagebox.showinfo(titulo, mensagem)

    def confirmar(self, titulo: str, mensagem: str) -> bool:
        """Exibe diálogo de confirmação."""
        return messagebox.askyesno(titulo, mensagem)
