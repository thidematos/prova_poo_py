"""
Model e Controller para Médico
"""
from tkinter import *
from tkinter import messagebox
import os.path
import pickle


class Medico:
    """Model - Representa um médico"""

    ESPECIALIDADES = [
        'Pediatria', 'Cardiologia', 'Neurologia',
        'Oftalmologia', 'Ortopedia', 'Gastroenterologia',
        'Psiquiatria', 'Pneumologia'
    ]

    def __init__(self, nome, crm, especialidade):
        self.__nome = nome
        self.__crm = crm

        if especialidade not in self.ESPECIALIDADES:
            raise ValueError(
                f'Especialidade inválida. Opções válidas: {", ".join(self.ESPECIALIDADES)}')

        self.__especialidade = especialidade

    @property
    def especialidade(self):
        return self.__especialidade

    @property
    def nome(self):
        return self.__nome

    @property
    def crm(self):
        return self.__crm

    def __str__(self):
        return f"{self.nome} - {self.especialidade} (CRM: {self.crm})"


class LimiteCadastraMedico(Toplevel):
    """View - Janela para cadastrar médico"""

    def __init__(self, controller):
        Toplevel.__init__(self)
        self.title('Cadastrar Médico')
        self.geometry('400x200')
        self.controller = controller

        # Frame Nome
        self.nomeFrame = Frame(self)
        self.nomeLabel = Label(self.nomeFrame, text='Nome: ')
        self.nomeEntry = Entry(self.nomeFrame, width=30)
        self.nomeLabel.pack(side='left')
        self.nomeEntry.pack(side='left', padx=5)
        self.nomeFrame.pack(pady=10)

        # Frame CRM
        self.crmFrame = Frame(self)
        self.crmLabel = Label(self.crmFrame, text='CRM: ')
        self.crmEntry = Entry(self.crmFrame, width=30)
        self.crmLabel.pack(side='left')
        self.crmEntry.pack(side='left', padx=5)
        self.crmFrame.pack(pady=10)

        # Frame Especialidade
        self.especialidadeFrame = Frame(self)
        self.especialidadeLabel = Label(
            self.especialidadeFrame, text='Especialidade: ')
        self.especialidadeEntry = Entry(self.especialidadeFrame, width=30)
        self.especialidadeLabel.pack(side='left')
        self.especialidadeEntry.pack(side='left', padx=5)
        self.especialidadeFrame.pack(pady=10)

        # Dica de especialidades
        self.dicaLabel = Label(self, text='Especialidades: Pediatria, Cardiologia, Neurologia, Oftalmologia,\nOrtopedia, Gastroenterologia, Psiquiatria, Pneumologia',
                               font=('Arial', 8), fg='gray')
        self.dicaLabel.pack(pady=5)

        # Botão Cadastrar
        self.btnCadastrar = Button(
            self, text='Cadastrar', command=self.controller.cadastrarMedico)
        self.btnCadastrar.pack(pady=10)

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

    def mostraErro(self, titulo, msg):
        messagebox.showerror(titulo, msg)


class CtrlMedico:
    """Controller - Gerencia médicos"""

    def __init__(self):
        if os.path.isfile('medicos.pickle'):
            with open('medicos.pickle', 'rb') as file:
                self.medicos = pickle.load(file)
        else:
            # Dados iniciais para teste
            self.medicos = [
                Medico('Dr. João Silva', '12345-SP', 'Pediatria'),
                Medico('Dra. Maria Santos', '23456-RJ', 'Pediatria'),
                Medico('Dr. Carlos Souza', '34567-MG', 'Cardiologia'),
                Medico('Dra. Ana Paula', '45678-SP', 'Cardiologia'),
                Medico('Dr. Pedro Lima', '56789-RS', 'Neurologia'),
                Medico('Dra. Fernanda Costa', '67890-BA', 'Neurologia'),
            ]
            self.salvaMedicos()

    def salvaMedicos(self):
        """Persiste médicos em arquivo pickle"""
        with open('medicos.pickle', 'wb') as file:
            pickle.dump(self.medicos, file)

    def getMedicosPorEspecialidade(self, especialidade):
        """Retorna lista de médicos de uma especialidade"""
        return [med for med in self.medicos if med.especialidade == especialidade]

    def getEspecialidadesDisponiveis(self):
        """Retorna lista de especialidades que possuem médicos cadastrados"""
        especialidades = set()
        for medico in self.medicos:
            especialidades.add(medico.especialidade)
        return sorted(list(especialidades))

    def getTodosMedicos(self):
        """Retorna lista de todos os médicos"""
        return self.medicos

    def cadastraMedico(self):
        """Abre janela de cadastro"""
        self.limiteCadastro = LimiteCadastraMedico(self)

    def cadastrarMedico(self):
        """Handler do botão cadastrar"""
        nome = self.limiteCadastro.nomeEntry.get().strip()
        crm = self.limiteCadastro.crmEntry.get().strip()
        especialidade = self.limiteCadastro.especialidadeEntry.get().strip()

        if not nome or not crm or not especialidade:
            self.limiteCadastro.mostraErro(
                'Erro', 'Todos os campos são obrigatórios!')
            return

        try:
            medico = Medico(nome, crm, especialidade)
            self.medicos.append(medico)
            self.salvaMedicos()
            self.limiteCadastro.mostraJanela(
                'Sucesso', f'Médico {nome} cadastrado com sucesso!')
            self.limiteCadastro.destroy()
        except ValueError as err:
            self.limiteCadastro.mostraErro('Erro de Validação', str(err))
