from tkinter import *
from vinho import *


class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.root.title('Adega')
        self.root.geometry('400x400')
        self.controller = controller

        self.menu = Menu(self.root)
        self.menu.add_command(label='Adicionar vinho',
                              command=self.controller.showCreateVinho)
        self.menu.add_command(label='Consultar vinhos',
                              command=self.controller.showListVinhos)

        self.root.config(menu=self.menu)


class MainController:
    def __init__(self):
        self.root = Tk()

        self.mainView = MainView(self.root, self)
        self.vinhoController = VinhoController()

        self.root.mainloop()

    def showCreateVinho(self):
        self.vinhoController.showCreateView()

    def showListVinhos(self):
        self.vinhoController.showListView()


if __name__ == '__main__':
    app = MainController()
