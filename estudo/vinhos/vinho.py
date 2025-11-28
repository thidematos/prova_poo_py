from tkinter import *
import os.path
import pickle
from tkinter import messagebox
from tkinter import ttk


class Vinho:
    allowed_tipos = ['Branco', 'Tinto', 'Rose', 'Espumante']
    allowed_var = ['Cabernet Sauvignon', 'Carmenere',
                   'Merlot', 'Malbec', 'Sauvignon Blanc', 'Pinot Grigio']
    allowed_origem = ['Brasil', 'Argentina', 'Chile',
                      'Itália', 'França', 'Portugal', 'África do Sul']

    def __init__(self, cod, nome, tipo, var, origem, preco):
        self.__cod = cod
        self.__nome = nome
        if tipo not in self.allowed_tipos:
            raise ValueError('Tipo inválido')
        self.__tipo = tipo

        if var not in self.allowed_var:
            raise ValueError('Variedade inválida')
        self.__var = var

        if origem not in self.allowed_origem:
            raise ValueError('Origem inválida')
        self.__origem = origem

        self.__preco = preco

    @property
    def cod(self):
        return self.__cod

    @property
    def nome(self):
        return self.__nome

    @property
    def tipo(self):
        return self.__tipo

    @property
    def var(self):
        return self.__var

    @property
    def origem(self):
        return self.__origem

    @property
    def preco(self):
        return self.__preco


class CreateView(Toplevel):
    def __init__(self,  controller):
        Toplevel.__init__(self)
        self.title('Adicionar vinhos')
        self.geometry('400x400')
        self.controller = controller

        self.codFrame = Frame(self)
        self.codLabel = Label(self.codFrame, text='Código: ')
        self.codEntry = Entry(self.codFrame, width=20)
        self.codLabel.pack(side='left')
        self.codEntry.pack(side='right')
        self.codFrame.pack(pady=10)

        self.nomeFrame = Frame(self)
        self.nomeLabel = Label(self.nomeFrame, text='Nome: ')
        self.nomeEntry = Entry(self.nomeFrame, width=20)
        self.nomeLabel.pack(side='left')
        self.nomeEntry.pack(side='right')
        self.nomeFrame.pack(pady=10)

        self.tipoFrame = Frame(self)
        self.tipoLabel = Label(self.tipoFrame, text='Tipo: ')
        self.tipoEntry = Entry(self.tipoFrame, width=20)
        self.tipoLabel.pack(side='left')
        self.tipoEntry.pack(side='right')
        self.tipoFrame.pack(pady=10)

        self.varFrame = Frame(self)
        self.varLabel = Label(self.varFrame, text='Variedade: ')
        self.varEntry = Entry(self.varFrame, width=20)
        self.varLabel.pack(side='left')
        self.varEntry.pack(side='right')
        self.varFrame.pack(pady=10)

        self.origemFrame = Frame(self)
        self.origemLabel = Label(self.origemFrame, text='Origem: ')
        self.origemEntry = Entry(self.origemFrame, width=20)
        self.origemLabel.pack(side='left')
        self.origemEntry.pack(side='right')
        self.origemFrame.pack(pady=10)

        self.precoFrame = Frame(self)
        self.precoLabel = Label(self.precoFrame, text='Preço: ')
        self.precoEntry = Entry(self.precoFrame, width=20)
        self.precoLabel.pack(side='left')
        self.precoEntry.pack(side='right')
        self.precoFrame.pack(pady=10)

        self.submit = Button(self, text='Adicionar',
                             command=self.controller.createVinho)
        self.submit.pack()

    def showErr(self, err):
        messagebox.showerror(title='Falha', message=err)

    def showSuccess(self, message):
        messagebox.showinfo(title='Sucesso!', message=message)


class ListView(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.title('Consultar vinhos')
        self.geometry('400x400')
        self.controller = controller

        tipos = self.controller.getTipos()
        vars = self.controller.getVars()

        self.resultFrame = Frame()

        self.filterFrame = Frame(self)
        self.tipo = ttk.Combobox(self.filterFrame, values=tipos)
        self.tipo.set('------')
        self.tipo.bind('<<ComboboxSelected>>', self.controller.showTipoFilter)
        self.tipo.pack(side='left')

        self.var = ttk.Combobox(self.filterFrame, values=vars)
        self.var.set('------')
        self.var.bind('<<ComboboxSelected>>', self.controller.showVarFilter)
        self.var.pack(side='right')

        self.filterFrame.pack()

        self.resultFrame.pack()

    def mountResults(self, results, isTipo):

        self.resultFrame.destroy()

        self.resultFrame = Frame(self)

        for result in results:
            cod = Label(self.resultFrame, text=result.cod)
            cod.pack()
            nome = Label(self.resultFrame, text=result.nome)
            nome.pack()
            tipo = Label(self.resultFrame, text=result.tipo)
            tipo.pack()
            var = Label(self.resultFrame, text=result.var)
            var.pack()
            origem = Label(self.resultFrame, text=result.origem)
            origem.pack()
            preco = Label(self.resultFrame, text=result.preco)
            preco.pack()
        self.resultFrame.pack()
        if isTipo:
            self.var.set('------')
        else:
            self.tipo.set('------')


class VinhoController:
    def __init__(self):
        if not os.path.isfile('vinhos.pickle'):
            self.vinhos = []
        else:
            with open('vinhos.pickle', 'rb') as file:
                self.vinhos = pickle.load(file)

    def salvaVinhos(self):
        if len(self.vinhos) != 0:
            with open('vinhos.pickle', 'wb') as file:
                pickle.dump(self.vinhos, file)

    def showCreateView(self):
        self.createView = CreateView(self)

    def showListView(self):
        self.listView = ListView(self)

    def showTipoFilter(self, event):
        vinhos = self.vinhos
        filtered = []
        selected = self.listView.tipo.get()

        for vinho in vinhos:
            if vinho.tipo == selected:
                filtered.append(vinho)
        self.listView.mountTipoResults(filtered)

    def showTipoFilter(self, event):
        vinhos = self.vinhos
        filtered = []
        selected = self.listView.tipo.get()

        for vinho in vinhos:
            if vinho.tipo == selected:
                filtered.append(vinho)
        self.listView.mountResults(filtered, True)

    def showVarFilter(self, event):
        vinhos = self.vinhos
        filtered = []
        selected = self.listView.var.get()

        for vinho in vinhos:
            if vinho.var == selected:
                filtered.append(vinho)
        self.listView.mountResults(filtered, False)

    def getTipos(self):
        vinhos = self.vinhos
        tipos = []

        for vinho in vinhos:
            if vinho.tipo not in tipos:
                tipos.append(vinho.tipo)
        return tipos

    def getVars(self):
        vinhos = self.vinhos
        vars = []

        for vinho in vinhos:
            if vinho.var not in vars:
                vars.append(vinho.var)
        return vars

    def createVinho(self):
        nome = self.createView.nomeEntry.get()
        cod = self.createView.codEntry.get()
        tipo = self.createView.tipoEntry.get()
        var = self.createView.varEntry.get()
        origem = self.createView.origemEntry.get()
        preco = self.createView.precoEntry.get()

        try:
            vinho = Vinho(cod, nome, tipo, var, origem, preco)
            self.vinhos.append(vinho)
            self.salvaVinhos()
            self.createView.showSuccess(f'Vinho {nome} criado!')
            self.createView.destroy()
        except ValueError as err:
            self.createView.showErr(str(err))
