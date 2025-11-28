import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
import pickle

class Jogo:
    def __init__(self, codigo, titulo, console, genero, preco):
        self.__codigo = codigo
        self.__titulo = titulo
        self.__console = console
        self.__genero = genero
        self.__preco = float(preco)
        self.__avaliacoes = []

    @property
    def codigo(self):
        return self.__codigo

    @property
    def titulo(self):
        return self.__titulo

    @property
    def console(self):
        return self.__console

    @property
    def genero(self):
        return self.__genero

    @property
    def preco(self):
        return self.__preco

    @property
    def avaliacoes(self):
        return self.__avaliacoes

    def adicionar_avaliacao(self, nota):
        self.__avaliacoes.append(nota)

    def calcular_media_estrelas(self):
        if not self.__avaliacoes:
            return 0
        media = sum(self.__avaliacoes) / len(self.__avaliacoes)
        if 0 <= media <= 1:
            return 1
        elif 1 < media <= 2:
            return 2
        elif 2 < media <= 3:
            return 3
        elif 3 < media <= 4:
            return 4
        elif 4 < media <= 5:
            return 5
        return 0

class View:
    def __init__(self, master, controller):
        self.controller = controller
        self.master = master
        self.master.title("Trabalho 12")
        self.master.geometry("300x200")

        self.menu = tk.Menu(self.master)
        self.menu_jogo = tk.Menu(self.menu, tearoff=0)
        self.menu_jogo.add_command(label="Cadastrar", command=controller.iniciaCadastro)
        self.menu_jogo.add_command(label="Avaliar", command=controller.iniciaAvaliacao)
        self.menu_jogo.add_command(label="Consultar", command=controller.iniciaConsulta)
        self.menu.add_cascade(label="Jogo", menu=self.menu_jogo)
        self.master.config(menu=self.menu)

    def mostraJanela(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostraErro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def janelaCadastro(self):
        self.top_cadastro = tk.Toplevel(self.master)
        self.top_cadastro.title("Cadastrar Jogo")

        lbl1 = tk.Label(self.top_cadastro, text="Código:")
        lbl1.pack()
        self.ent_codigo = tk.Entry(self.top_cadastro)
        self.ent_codigo.pack()

        lbl2 = tk.Label(self.top_cadastro, text="Título:")
        lbl2.pack()
        self.ent_titulo = tk.Entry(self.top_cadastro)
        self.ent_titulo.pack()

        lbl3 = tk.Label(self.top_cadastro, text="Console:")
        lbl3.pack()
        self.ent_console = tk.Entry(self.top_cadastro)
        self.ent_console.pack()

        lbl4 = tk.Label(self.top_cadastro, text="Gênero:")
        lbl4.pack()
        self.ent_genero = tk.Entry(self.top_cadastro)
        self.ent_genero.pack()

        lbl5 = tk.Label(self.top_cadastro, text="Preço:")
        lbl5.pack()
        self.ent_preco = tk.Entry(self.top_cadastro)
        self.ent_preco.pack()

        btn = tk.Button(self.top_cadastro, text="Salvar")
        btn.pack(pady=5)
        btn.bind("<Button>", self.controller.salvaJogoHandler)

    def janelaAvaliacao(self):
        self.top_avaliacao = tk.Toplevel(self.master)
        self.top_avaliacao.title("Avaliar Jogo")

        lbl1 = tk.Label(self.top_avaliacao, text="Código do Jogo:")
        lbl1.pack()
        self.ent_cod_av = tk.Entry(self.top_avaliacao)
        self.ent_cod_av.pack()

        lbl2 = tk.Label(self.top_avaliacao, text="Nota (Estrelas):")
        lbl2.pack()
        self.combo_nota = ttk.Combobox(self.top_avaliacao, values=["1", "2", "3", "4", "5"])
        self.combo_nota.pack()

        btn = tk.Button(self.top_avaliacao, text="Avaliar")
        btn.pack(pady=5)
        btn.bind("<Button>", self.controller.salvaAvaliacaoHandler)

    def janelaConsulta(self):
        self.top_consulta = tk.Toplevel(self.master)
        self.top_consulta.title("Consultar Jogos")

        lbl1 = tk.Label(self.top_consulta, text="Filtrar por Estrelas:")
        lbl1.pack()
        self.combo_filtro = ttk.Combobox(self.top_consulta, values=["1", "2", "3", "4", "5"])
        self.combo_filtro.pack()

        btn = tk.Button(self.top_consulta, text="Consultar")
        btn.pack(pady=5)
        btn.bind("<Button>", self.controller.processaConsultaHandler)

class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.listaJogos = []
        self.carregar_dados()
        self.view = View(self.root, self)
        self.root.mainloop()

    def carregar_dados(self):
        if os.path.exists("games.pkl"):
            with open("games.pkl", "rb") as f:
                self.listaJogos = pickle.load(f)

    def salvar_dados(self):
        with open("games.pkl", "wb") as f:
            pickle.dump(self.listaJogos, f)

    def iniciaCadastro(self):
        self.view.janelaCadastro()

    def iniciaAvaliacao(self):
        self.view.janelaAvaliacao()

    def iniciaConsulta(self):
        self.view.janelaConsulta()

    def salvaJogoHandler(self, event):
        codigo = self.view.ent_codigo.get()
        titulo = self.view.ent_titulo.get()
        console = self.view.ent_console.get()
        genero = self.view.ent_genero.get()
        preco_str = self.view.ent_preco.get()

        consoles_validos = ["XBox", "PlayStation", "Switch", "PC"]
        generos_validos = ["Ação", "Aventura", "Estratégia", "RPG", "Esporte", "Simulação"]

        try:
            if console not in consoles_validos:
                raise ValueError("Console inválido. Use: XBox, PlayStation, Switch, PC")
            if genero not in generos_validos:
                raise ValueError("Gênero inválido.")
            
            preco = float(preco_str)
            if preco <= 0 or preco > 500:
                raise ValueError("Preço deve ser maior que 0 e até 500.")
            
            for jogo in self.listaJogos:
                if jogo.codigo == codigo:
                    raise ValueError("Código de jogo já cadastrado.")

            jogo = Jogo(codigo, titulo, console, genero, preco)
            self.listaJogos.append(jogo)
            self.salvar_dados()
            self.view.mostraJanela("Sucesso", "Jogo cadastrado com sucesso!")
            self.view.top_cadastro.destroy()

        except ValueError as error:
            self.view.mostraErro("Erro de Validação", str(error))
        except Exception as e:
            self.view.mostraErro("Erro", "Dados inválidos.")

    def salvaAvaliacaoHandler(self, event):
        codigo = self.view.ent_cod_av.get()
        nota_str = self.view.combo_nota.get()

        try:
            nota = int(nota_str)
            jogo_encontrado = None
            for jogo in self.listaJogos:
                if jogo.codigo == codigo:
                    jogo_encontrado = jogo
                    break
            
            if jogo_encontrado:
                jogo_encontrado.adicionar_avaliacao(nota)
                self.salvar_dados()
                self.view.mostraJanela("Sucesso", f"Avaliação de {nota} estrelas registrada para {jogo_encontrado.titulo}.")
                self.view.top_avaliacao.destroy()
            else:
                self.view.mostraErro("Erro", "Jogo não encontrado.")
        
        except ValueError:
            self.view.mostraErro("Erro", "Selecione uma nota válida.")

    def processaConsultaHandler(self, event):
        filtro_str = self.view.combo_filtro.get()
        resultado = ""
        
        try:
            filtro = int(filtro_str)
            for jogo in self.listaJogos:
                if not jogo.avaliacoes:
                    continue
                
                media_estrelas = jogo.calcular_media_estrelas()
                if media_estrelas == filtro:
                    resultado += f"Título: {jogo.titulo} - Console: {jogo.console} - Preço: {jogo.preco}\n"
            
            if not resultado:
                resultado = "Nenhum jogo encontrado com essa classificação."
            
            self.view.mostraJanela(f"Jogos com {filtro} Estrelas", resultado)
            self.view.top_consulta.destroy()

        except ValueError:
             self.view.mostraErro("Erro", "Selecione um filtro válido.")

if __name__ == '__main__':
    c = Controller()