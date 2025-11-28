from tkinter import *
from consulta import *
from medico import *


class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title('Consultas Médicas')
        self.root.geometry('400x300')

        self.menu = Menu(self.root)
        self.menu.add_command(label='Criar Médico',
                              command=self.controller.showCriarMedico)
        self.menu.add_command(
            label='Agendar', command=self.controller.showCriarConsulta)
        self.menu.add_command(
            label='Consultas', command=self.controller.showConsultas)

        self.root.config(menu=self.menu)


class MainController:
    def __init__(self):
        self.root = Tk()

        self.mainView = MainView(self.root, self)
        self.ConsultaController = ConsultaController()
        self.medicoController = MedicoController()
        self.root.mainloop()

    def showCriarConsulta(self):
        self.ConsultaController.showCriar(self.medicoController)

    def showCriarMedico(self):
        self.medicoController.showCriarMedicos()

    def showConsultas(self):
        self.ConsultaController.showConsultas(self.medicoController)


if __name__ == '__main__':
    app = MainController()
