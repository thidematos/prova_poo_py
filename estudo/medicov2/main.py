# 2024016073 - Thiago Luiz de Matos
from tkinter import *
from medico import CtrlMedico
from consulta import CtrlConsulta


class LimitePrincipal:
    """View Principal - Menu da aplicação"""

    def __init__(self, root, controle):
        self.root = root
        self.controle = controle

        self.root.title('Sistema de Consultas Médicas')
        self.root.geometry('400x300')

        # Cria barra de menu
        self.menubar = Menu(self.root)

        # Menu Médico
        self.menuMedico = Menu(self.menubar, tearoff=0)
        self.menuMedico.add_command(
            label='Cadastrar', command=self.controle.cadastrarMedico)
        self.menubar.add_cascade(label='Médico', menu=self.menuMedico)

        # Menu Consulta
        self.menuConsulta = Menu(self.menubar, tearoff=0)
        self.menuConsulta.add_command(
            label='Cadastrar', command=self.controle.cadastrarConsulta)
        self.menuConsulta.add_command(
            label='Listar Consultas', command=self.controle.listarConsultas)
        self.menubar.add_cascade(label='Consulta', menu=self.menuConsulta)

        self.root.config(menu=self.menubar)


class ControlePrincipal:
    """Controller Principal - Coordena a aplicação"""

    def __init__(self):
        self.root = Tk()

        # Cria os controllers
        self.ctrlMedico = CtrlMedico()
        self.ctrlConsulta = CtrlConsulta(self.ctrlMedico)

        # Cria a view principal
        self.limite = LimitePrincipal(self.root, self)

        # Inicia o loop
        self.root.mainloop()

    def cadastrarMedico(self):
        """Delega para o controller de médico"""
        self.ctrlMedico.cadastraMedico()

    def cadastrarConsulta(self):
        """Delega para o controller de consulta"""
        self.ctrlConsulta.cadastraConsulta()

    def listarConsultas(self):
        """Delega para o controller de consulta"""
        self.ctrlConsulta.listaConsultas()


if __name__ == '__main__':
    app = ControlePrincipal()
