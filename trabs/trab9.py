# Thiago Luiz de Matos - 2024016073

import tkinter as tk
from tkinter import messagebox, simpledialog


class ModelCliente():
    def __init__(self, codigo, nome, email):
        self.__codigo = codigo
        self.__nome = nome
        self.__email = email

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email


class View():
    def __init__(self, master, controller):
        self.controller = controller
        self.janela = tk.Frame(master)
        self.janela.pack()
        self.frame1 = tk.Frame(self.janela)
        self.frame2 = tk.Frame(self.janela)
        self.frame3 = tk.Frame(self.janela)
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        self.labelInfo0 = tk.Label(self.frame1, text="Código: ")
        self.labelInfo1 = tk.Label(self.frame2, text="Nome: ")
        self.labelInfo2 = tk.Label(self.frame3, text="Email: ")
        self.labelInfo0.pack(side="left")
        self.labelInfo1.pack(side="left")
        self.labelInfo2.pack(side="left")

        self.inputText0 = tk.Entry(self.frame1, width=20)
        self.inputText0.pack(side="left")
        self.inputText1 = tk.Entry(self.frame2, width=20)
        self.inputText1.pack(side="left")
        self.inputText2 = tk.Entry(self.frame3, width=20)
        self.inputText2.pack(side="left")

        self.buttonSubmit = tk.Button(self.janela, text="Salva")
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controller.salvaHandler)

        self.buttonClear = tk.Button(self.janela, text="Limpa")
        self.buttonClear.pack(side="left")
        self.buttonClear.bind("<Button>", controller.clearHandler)

        self.buttonConsulta = tk.Button(self.janela, text="Consulta")
        self.buttonConsulta.pack(side="left")
        self.buttonConsulta.bind("<Button>", controller.consultaHandler)

    def mostraJanela(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)


class Controller():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x130')
        self.listaClientes = []
        self.view = View(self.root, self)
        self.root.title("Exemplo MVC")
        self.root.mainloop()

    def salvaHandler(self, event):
        codigoCli = self.view.inputText0.get()
        nomeCli = self.view.inputText1.get()
        emailCli = self.view.inputText2.get()
        cliente = ModelCliente(codigoCli, nomeCli, emailCli)
        self.listaClientes.append(cliente)
        self.view.mostraJanela('Sucesso', 'Cliente cadastrado com sucesso')
        self.clearHandler(event)

    def clearHandler(self, event):
        self.view.inputText0.delete(0, len(self.view.inputText0.get()))
        self.view.inputText1.delete(0, len(self.view.inputText1.get()))
        self.view.inputText2.delete(0, len(self.view.inputText2.get()))

    def consultaHandler(self, event):
        codigo = simpledialog.askstring(
            "Consulta", "Digite o código do cliente:")
        for cliente in self.listaClientes:
            if cliente.codigo == codigo:
                self.view.mostraJanela(
                    "Cliente encontrado", f"Nome: {cliente.nome}\nEmail: {cliente.email}")
                return
        self.view.mostraJanela("Erro", "Código não cadastrado")


if __name__ == '__main__':
    c = Controller()
