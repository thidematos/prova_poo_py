from tkinter import *
import os.path
import pickle
from tkinter import messagebox


class Medico:
    allowed_especialidades = ['Pediatria', 'Cardiologia', 'Neurologia',
                              'Oftalmologia', 'Ortopedia', 'Gastroenterologia', 'Psiquiatria', 'Pneumologia']

    def __init__(self, nome, crm, especialidade):
        self.__nome = nome
        self.__crm = crm

        if especialidade not in self.allowed_especialidades:
            raise ValueError('Especialidade inválida')

        self.__especialidade = especialidade

    @property
    def especialidade(self):
        return self.__especialidade

    @property
    def nome(self):
        return self.__nome


class CreateMedicoView(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.title('Cadastrar Médico')
        self.geometry('400x400')
        self.controller = controller

        self.nomeFrame = Frame(self)
        self.nomeLabel = Label(self.nomeFrame, text='Nome: ')
        self.nomeEntry = Entry(self.nomeFrame, width=15)
        self.nomeLabel.pack(side='left')
        self.nomeEntry.pack(side='right')
        self.nomeFrame.pack(pady=5)

        self.crmFrame = Frame(self)
        self.crmLabel = Label(self.crmFrame, text='CRM: ')
        self.crmEntry = Entry(self.crmFrame, width=15)
        self.crmLabel.pack(side='left')
        self.crmEntry.pack(side='right')
        self.crmFrame.pack(pady=5)

        self.especialidadeFrame = Frame(self)
        self.especialidadeLabel = Label(
            self.especialidadeFrame, text='Especialidade: ')
        self.especialidadeEntry = Entry(self.especialidadeFrame, width=15)
        self.especialidadeLabel.pack(side='left')
        self.especialidadeEntry.pack(side='right')
        self.especialidadeFrame.pack()

        self.criar = Button(self, text='Cadastrar',
                            command=self.controller.createMedico)
        self.criar.pack(pady=5)

    def showSuccess(self, message):
        messagebox.showinfo(title='Sucesso!', message=message)

    def showError(self, error):
        messagebox.showerror(title='Médico inválido!', message=error)


class MedicoController:

    def __init__(self):
        if not os.path.isfile('medicos.pickle'):
            self.medicos = []
        else:
            with open('medicos.pickle', 'rb') as file:
                self.medicos = pickle.load(file)

    def getMedicos(self, especialidade=False):
        if especialidade == False:
            return self.medicos

        medicos = []

        for med in self.medicos:
            if med.especialidade == especialidade:
                medicos.append(med)
        return medicos

    def getEspecialidades(self):
        esps = []

        for medico in self.medicos:
            if medico.especialidade not in esps:
                esps.append(medico.especialidade)

        return esps

    def salvaMedicos(self):
        if len(self.medicos) != 0:
            with open('medicos.pickle', 'wb') as file:
                pickle.dump(self.medicos, file)

    def showCriarMedicos(self):
        self.criarMedicoView = CreateMedicoView(self)

    def createMedico(self):
        nome = self.criarMedicoView.nomeEntry.get()
        crm = self.criarMedicoView.crmEntry.get()
        especialidade = self.criarMedicoView.especialidadeEntry.get()

        try:
            medico = Medico(nome, crm, especialidade)
            self.medicos.append(medico)
            self.salvaMedicos()
            self.criarMedicoView.showSuccess(
                f'Médico {nome} criado com sucesso')
            self.criarMedicoView.destroy()
        except ValueError as err:
            self.criarMedicoView.showError(str(err))
