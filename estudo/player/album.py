from tkinter import *


class Album:
    def __init__(self, titulo, ano):
        self.__titulo = titulo
        self.__ano = ano
        self.__musicas = []

    @property
    def titulo(self):
        return self.__titulo

    @property
    def ano(self):
        return self.__ano

    @property
    def musicas(self):
        return self.__musicas


class AddWindow(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.title('Adicionar album')
        self.geometry('400x600')

        self.frameHeader = Frame(self)
        self.title = Label(self.frameHeader, text='Adicionar Album')
        self.title.pack(pady=5)
        self.frameHeader.pack(pady=5)

        self.frameTituloEntry = Frame(self)
        self.labelTitulo = Label(self.frameTituloEntry, text='Título: ')
        self.labelTitulo.grid(row=0, column=0, padx=5)
        self.entryTitulo = Entry(self.frameTituloEntry, width=30)
        self.entryTitulo.grid(row=0, column=1, padx=5)
        self.frameTituloEntry.pack(pady=5)


class AlbumController:
    def __init__(self):
        self.albumList = []

    def showAddAlbum(self):
        self.addAlbumWindow = AddWindow(self)
