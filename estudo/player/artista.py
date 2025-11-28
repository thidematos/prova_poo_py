from tkinter import *
from tkinter import messagebox


class ArtistaController:
    def __init__(self):
        self.artistaList = []

    def showListArtistas(self):
        self.showWindow = AddArtistaList(self)

    def showAddArtista(self):
        self.addWindow = AddArtistaView(self)

    def getArtistas(self):
        return self.artistaList

    def addArtistaHandler(self, event):
        nome = self.addWindow.entry.get()
        self.artistaList.append(Artista(nome))
        self.addWindow.destroy()
        for art in self.artistaList:
            print(f'artista: {art.nome}')


class AddArtistaList(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.geometry('300x250')
        self.title('Artistas')
        self.controller = controller

        self.frame = Frame(self)

        self.mainLabel = Label(self, text='ARTISTAS')
        self.mainLabel.pack()
        self.mainDivider = Label(self, text='-------------------')
        self.mainDivider.pack()

        for art in self.controller.getArtistas():
            label = Label(self.frame, text=art.nome)
            label.pack(pady=5)

        self.frame.pack()


class AddArtistaView(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.geometry('400x150')
        self.title('Adicionar artista')
        self.controller = controller

        self.frameEntry = Frame(self)

        self.label = Label(self.frameEntry, text='Artista: ')
        self.label.pack(side='left')

        self.entry = Entry(self.frameEntry, width=40)
        self.entry.pack(side='right')

        self.frameButton = Frame(self)

        self.button = Button(self.frameButton, text='Adicionar')
        self.button.pack(pady=10)
        self.button.bind('<Button>', self.controller.addArtistaHandler)

        self.frameEntry.pack()
        self.frameButton.pack()

    def showSuccess(self):
        messagebox.showinfo(title='Artista adicionado', message='Successo!')


class Artista:
    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome
