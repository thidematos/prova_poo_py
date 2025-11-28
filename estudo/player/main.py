from tkinter import *

from artista import *
from album import *


class MainView():
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title('Musicfier')
        self.root.geometry('700x500')

        self.menu = Menu(self.root)

        self.menuArtistas = Menu(self.menu)
        self.menuArtistas.add_command(
            label='Cadastrar', command=self.controller.addArtista)
        self.menuArtistas.add_command(
            label='Consultar', command=self.controller.showArtista)
        self.menu.add_cascade(label='Artistas', menu=self.menuArtistas)

        self.menuAlbuns = Menu(self.menu)
        self.menuAlbuns.add_command(
            label='Cadastrar', command=self.controller.addAlbum)
        self.menu.add_cascade(label='Albuns', menu=self.menuAlbuns)

        self.root.config(menu=self.menu)

        pass


class MainController:
    def __init__(self):
        self.root = Tk()

        self.artistaController = ArtistaController()
        self.albumController = AlbumController()

        self.mainView = MainView(self.root, self)

        self.root.mainloop()

    def addArtista(self):
        self.artistaController.showAddArtista()

    def showArtista(self):
        self.artistaController.showListArtistas()

    def addAlbum(self):
        self.albumController.showAddAlbum()


if __name__ == '__main__':
    app = MainController()
