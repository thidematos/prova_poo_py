import os.path
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Consulta:

    def __init__(self, paciente, dia, hora, especialidade, medico):
        self.__paciente = paciente
        if int(dia) < 1 or int(dia) > 30:
            raise ValueError('Dia inválido')
        self.__dia = dia

        if int(hora) < 9 or int(hora) > 17:
            raise ValueError('Hora inválida')
        self.__hora = hora

        self.__especialidade = especialidade
        self.__medico = medico

    @property
    def paciente(self):
        return self.__paciente

    @property
    def dia(self):
        return self.__dia

    @property
    def hora(self):
        return self.__hora

    @property
    def especialidade(self):
        return self.__especialidade

    @property
    def medico(self):
        return self.__medico


class CreateConsultaView(Toplevel):
    def __init__(self, controller, medicoController):
        Toplevel.__init__(self)
        self.title('Consulta')
        self.geometry('400x600')
        self.controller = controller
        self.medicoController = medicoController

        self.frameNome = Frame(self)
        self.labelNome = Label(self.frameNome, text='Nome do paciente:')
        self.entryNome = Entry(self.frameNome, width=20)
        self.labelNome.pack(side='left')
        self.entryNome.pack(side='right')
        self.frameNome.pack(pady=5)

        self.frameDia = Frame(self)
        self.labelDia = Label(self.frameDia, text='Informe o dia:')
        self.entryDia = Entry(self.frameDia, width=5)
        self.labelDia.pack(side='left')
        self.entryDia.pack(side='right')
        self.frameDia.pack(pady=5)

        self.frameHora = Frame(self)
        self.labelHora = Label(self.frameHora, text='Informe o horário:')
        self.entryHora = Entry(self.frameHora, width=5)
        self.labelHora.pack(side='left')
        self.entryHora.pack(side='right')
        self.frameHora.pack(pady=5)

        especialidades = medicoController.getEspecialidades()
        self.frameMedicos = Frame(self)

        self.frameEspecialidade = Frame(self)
        self.espLabel = Label(self.frameEspecialidade,
                              text='Escolha a especialidade')
        self.espDropdown = ttk.Combobox(
            self.frameEspecialidade, values=especialidades)
        self.espDropdown.set('------')
        self.espDropdown.bind('<<ComboboxSelected>>',
                              func=self.showMedicosList)
        self.espDropdown.pack(side='right')
        self.espLabel.pack(side='left')
        self.frameEspecialidade.pack(pady=5)

        self.frameMedicos.pack()

        self.frameCommands = Frame(self)
        self.cadastrar = Button(
            self.frameCommands, text='Cadastrar consulta', command=self.save)
        self.limpar = Button(self.frameCommands, text='Limpar')
        self.cadastrar.pack(side='left')
        self.limpar.pack(side='right')
        self.frameCommands.pack(pady=5)

    def showMedicosList(self, event):
        medicos = self.medicoController.getMedicos(self.espDropdown.get())
        self.medicosLabel = Label(self.frameMedicos, text='Escolha o médico: ')
        self.listMedicos = Listbox(self.frameMedicos, selectmode=SINGLE)
        for med in medicos:
            self.listMedicos.insert(END, med.nome)
        self.listMedicos.pack(side='right')
        self.medicosLabel.pack(side='left')

    def save(self):
        self.controller.createConsulta()

    def showError(self, err):
        messagebox.showerror(title='Consulta inválida', message=err)

    def showSuccess(self, message):
        messagebox.showinfo(title='Sucesso!', message=message)


class ConsultasView(Toplevel):
    def __init__(self, controller,  medicoController):
        Toplevel.__init__(self)
        self.medicoController = medicoController
        self.controller = controller
        self.title('Consultas Agendadas')
        self.geometry('400x600')

        medicos = self.medicoController.getMedicos()

        medicosNomes = []

        for med in medicos:
            medicosNomes.append(med.nome)

        self.consultasFrame = Frame(self)

        self.searchFrame = Frame(self)
        self.searchLabel = Label(self.searchFrame, text='Médico: ')
        self.searchDrop = ttk.Combobox(self.searchFrame, values=medicosNomes)

        self.searchDrop.bind('<<ComboboxSelected>>', func=self.showConsultas)

        self.searchLabel.pack(side='left')
        self.searchDrop.pack(side='right')
        self.searchFrame.pack()

        self.consultasFrame.pack()

    def showConsultas(self, event):
        consultas = self.controller.consultas

        for consulta in consultas:
            consulta = Label(
                self.consultasFrame, text=f'Dia: {consulta.dia} | Hora: {consulta.hora} | Paciente: {consulta.paciente}')
            divider = Label(self.consultasFrame, text='-----------------')
            consulta.pack(pady=10)
            divider.pack(pady=5)


class ConsultaController:
    def __init__(self):
        if not os.path.isfile('consultas.pickle'):
            self.consultas = []
        else:
            with open('consultas.pickle', 'rb') as file:
                self.consultas = pickle.load(file)

    def salvaConsultas(self):
        if len(self.consultas) != 0:
            with open('consultas.pickle', 'wb') as file:
                pickle.dump(self.consultas, file)

    def verifyConsultas(self, medico, dia, hora):
        status = True
        for consulta in self.consultas:
            if consulta.medico == medico and str(consulta.dia) == str(dia) and str(consulta.hora) == str(hora):
                status = False
        try:
            if status == False:
                raise ValueError(
                    'Já existe consulta agendada nesta data, escolha outra.')
        except ValueError as err:
            self.criarView.showError(str(err))

        return status

    def showCriar(self, medicoController):
        self.criarView = CreateConsultaView(self, medicoController)

    def showConsultas(self, medicoController):
        self.consultasView = ConsultasView(self, medicoController)

    def createConsulta(self):
        nomePaciente = self.criarView.entryNome.get()
        dia = self.criarView.entryDia.get()
        hora = self.criarView.entryHora.get()
        especialidade = self.criarView.espDropdown.get()
        index = self.criarView.listMedicos.curselection()
        medico = self.criarView.listMedicos.get(index[0])

        try:
            consulta = Consulta(nomePaciente, dia, hora, especialidade, medico)
            status = self.verifyConsultas(medico, dia, hora)
            if status == False:
                return

            self.consultas.append(consulta)
            self.salvaConsultas()
            self.criarView.showSuccess('Consulta criada com sucesso!')
            self.criarView.destroy()
        except ValueError as err:
            self.criarView.showError(str(err))
