"""
Model e Controller para Consulta
"""
from tkinter import *
from tkinter import ttk, messagebox
import os.path
import pickle


class Consulta:
    """Model - Representa uma consulta médica"""

    def __init__(self, paciente, dia, hora, medico):
        self.__paciente = paciente

        # Validação de dia (1-30)
        if not isinstance(dia, int) or dia < 1 or dia > 30:
            raise ValueError('Dia inválido! Informe um valor entre 1 e 30.')
        self.__dia = dia

        # Validação de hora (9-17)
        if not isinstance(hora, int) or hora < 9 or hora > 17:
            raise ValueError('Hora inválida! Informe um valor entre 9 e 17.')
        self.__hora = hora

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
    def medico(self):
        return self.__medico

    def __str__(self):
        return f"Dia {self.dia:02d} às {self.hora}h - {self.paciente}"


class LimiteCadastraConsulta(Toplevel):
    """View - Janela para cadastrar consulta"""

    def __init__(self, controller, ctrlMedico):
        Toplevel.__init__(self)
        self.title('Cadastrar Consulta')
        self.geometry('400x500')
        self.controller = controller
        self.ctrlMedico = ctrlMedico

        # Nome do Paciente
        self.frameNome = Frame(self)
        self.labelNome = Label(self.frameNome, text='Nome do paciente:')
        self.entryNome = Entry(self.frameNome, width=30)
        self.labelNome.pack(side='left')
        self.entryNome.pack(side='left', padx=5)
        self.frameNome.pack(pady=10)

        # Dia
        self.frameDia = Frame(self)
        self.labelDia = Label(self.frameDia, text='Informe o dia (1-30):')
        self.entryDia = Entry(self.frameDia, width=10)
        self.labelDia.pack(side='left')
        self.entryDia.pack(side='left', padx=5)
        self.frameDia.pack(pady=10)

        # Hora
        self.frameHora = Frame(self)
        self.labelHora = Label(
            self.frameHora, text='Informe o horário (9-17):')
        self.entryHora = Entry(self.frameHora, width=10)
        self.labelHora.pack(side='left')
        self.entryHora.pack(side='left', padx=5)
        self.frameHora.pack(pady=10)

        # Especialidade (Combobox)
        self.frameEspecialidade = Frame(self)
        self.labelEspecialidade = Label(
            self.frameEspecialidade, text='Escolha a especialidade:')
        self.labelEspecialidade.pack()

        especialidades = self.ctrlMedico.getEspecialidadesDisponiveis()
        self.comboEspecialidade = ttk.Combobox(
            self.frameEspecialidade,
            values=especialidades,
            state='readonly',
            width=30
        )
        self.comboEspecialidade.set('Selecione...')
        self.comboEspecialidade.bind(
            '<<ComboboxSelected>>', self.aoSelecionarEspecialidade)
        self.comboEspecialidade.pack(pady=5)
        self.frameEspecialidade.pack(pady=10)

        # Médicos (Listbox)
        self.frameMedicos = Frame(self)
        self.labelMedicos = Label(self.frameMedicos, text='Escolha o médico:')
        self.labelMedicos.pack()

        self.listboxMedicos = Listbox(
            self.frameMedicos, selectmode=SINGLE, width=40, height=6)
        self.listboxMedicos.pack(pady=5)
        self.frameMedicos.pack(pady=10)

        # Botões
        self.frameButtons = Frame(self)
        self.btnCadastrar = Button(self.frameButtons, text='Cadastrar Consulta',
                                   command=self.controller.cadastrarConsulta)
        self.btnLimpar = Button(
            self.frameButtons, text='Limpar', command=self.limparCampos)
        self.btnCadastrar.pack(side='left', padx=5)
        self.btnLimpar.pack(side='left', padx=5)
        self.frameButtons.pack(pady=15)

    def aoSelecionarEspecialidade(self, event):
        """Atualiza listbox de médicos quando especialidade é selecionada"""
        especialidade = self.comboEspecialidade.get()
        medicos = self.ctrlMedico.getMedicosPorEspecialidade(especialidade)

        # Limpa e preenche listbox
        self.listboxMedicos.delete(0, END)
        for medico in medicos:
            self.listboxMedicos.insert(END, medico.nome)

    def getMedicoSelecionado(self):
        """Retorna o objeto Medico selecionado"""
        selecao = self.listboxMedicos.curselection()
        if not selecao:
            return None

        nome_medico = self.listboxMedicos.get(selecao[0])
        especialidade = self.comboEspecialidade.get()
        medicos = self.ctrlMedico.getMedicosPorEspecialidade(especialidade)

        for medico in medicos:
            if medico.nome == nome_medico:
                return medico
        return None

    def limparCampos(self):
        """Limpa todos os campos do formulário"""
        self.entryNome.delete(0, END)
        self.entryDia.delete(0, END)
        self.entryHora.delete(0, END)
        self.comboEspecialidade.set('Selecione...')
        self.listboxMedicos.delete(0, END)

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

    def mostraErro(self, titulo, msg):
        messagebox.showerror(titulo, msg)


class LimiteMostraConsultas(Toplevel):
    """View - Janela para listar consultas por médico"""

    def __init__(self, controller, ctrlMedico):
        Toplevel.__init__(self)
        self.title('Consultas Marcadas')
        self.geometry('500x400')
        self.controller = controller
        self.ctrlMedico = ctrlMedico

        # Título
        self.labelTitulo = Label(
            self, text='Consultas por Médico', font=('Arial', 14, 'bold'))
        self.labelTitulo.pack(pady=10)

        # Combobox de médicos
        self.frameMedico = Frame(self)
        self.labelMedico = Label(self.frameMedico, text='Selecione o médico:')
        self.labelMedico.pack()

        medicos = self.ctrlMedico.getTodosMedicos()
        nomes_medicos = [medico.nome for medico in medicos]

        self.comboMedico = ttk.Combobox(
            self.frameMedico,
            values=nomes_medicos,
            state='readonly',
            width=40
        )
        self.comboMedico.set('Selecione um médico...')
        self.comboMedico.bind('<<ComboboxSelected>>', self.aoSelecionarMedico)
        self.comboMedico.pack(pady=5)
        self.frameMedico.pack(pady=10)

        # Listbox de consultas
        self.frameConsultas = Frame(self)
        self.labelConsultas = Label(
            self.frameConsultas, text='Consultas marcadas:', font=('Arial', 10, 'bold'))
        self.labelConsultas.pack()

        scrollbar = Scrollbar(self.frameConsultas)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.listboxConsultas = Listbox(self.frameConsultas, width=60, height=15,
                                        yscrollcommand=scrollbar.set, font=('Courier', 10))
        self.listboxConsultas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listboxConsultas.yview)

        self.frameConsultas.pack(pady=10, padx=20, fill=BOTH, expand=True)

    def aoSelecionarMedico(self, event):
        """Atualiza lista de consultas quando médico é selecionado"""
        nome_medico = self.comboMedico.get()

        # Encontra o médico
        medico = None
        for med in self.ctrlMedico.getTodosMedicos():
            if med.nome == nome_medico:
                medico = med
                break

        if medico:
            consultas = self.controller.getConsultasPorMedico(medico)
            self.atualizarConsultas(consultas)

    def atualizarConsultas(self, consultas):
        """Atualiza a listbox com as consultas"""
        self.listboxConsultas.delete(0, END)

        if not consultas:
            self.listboxConsultas.insert(
                END, "Nenhuma consulta agendada para este médico.")
        else:
            # Cabeçalho
            self.listboxConsultas.insert(END, "Dia / Hora / Nome do Paciente")
            self.listboxConsultas.insert(END, "-" * 50)

            # Ordena por dia e hora
            consultas_ordenadas = sorted(
                consultas, key=lambda c: (c.dia, c.hora))

            for consulta in consultas_ordenadas:
                linha = f"{consulta.dia:02d}   /  {consulta.hora:02d}h  / {consulta.paciente}"
                self.listboxConsultas.insert(END, linha)


class CtrlConsulta:
    """Controller - Gerencia consultas"""

    def __init__(self, ctrlMedico):
        self.ctrlMedico = ctrlMedico

        if os.path.isfile('consultas.pickle'):
            with open('consultas.pickle', 'rb') as file:
                self.consultas = pickle.load(file)
        else:
            self.consultas = []

    def salvaConsultas(self):
        """Persiste consultas em arquivo pickle"""
        with open('consultas.pickle', 'wb') as file:
            pickle.dump(self.consultas, file)

    def cadastraConsulta(self):
        """Abre janela de cadastro de consulta"""
        self.limiteCadastro = LimiteCadastraConsulta(self, self.ctrlMedico)

    def cadastrarConsulta(self):
        """Handler do botão cadastrar consulta"""
        paciente = self.limiteCadastro.entryNome.get().strip()
        dia_str = self.limiteCadastro.entryDia.get().strip()
        hora_str = self.limiteCadastro.entryHora.get().strip()
        medico = self.limiteCadastro.getMedicoSelecionado()

        # Validações de preenchimento
        if not paciente:
            self.limiteCadastro.mostraErro(
                'Erro', 'Nome do paciente é obrigatório!')
            return

        if not dia_str or not hora_str:
            self.limiteCadastro.mostraErro(
                'Erro', 'Dia e hora são obrigatórios!')
            return

        if not medico:
            self.limiteCadastro.mostraErro('Erro', 'Selecione um médico!')
            return

        # Conversão para inteiro
        try:
            dia = int(dia_str)
            hora = int(hora_str)
        except ValueError:
            self.limiteCadastro.mostraErro(
                'Erro', 'Dia e hora devem ser números inteiros!')
            return

        # Verifica conflito de horário
        if self.verificaConflito(medico, dia, hora):
            self.limiteCadastro.mostraErro(
                'Conflito', 'Já existe consulta agendada nesta data, escolha outra.')
            return

        # Cria a consulta
        try:
            consulta = Consulta(paciente, dia, hora, medico)
            self.consultas.append(consulta)
            self.salvaConsultas()
            self.limiteCadastro.mostraJanela('Sucesso',
                                             f'Consulta agendada com sucesso!\nPaciente: {paciente}\nDia: {dia}\nHora: {hora}h\nMédico: {medico.nome}')
            self.limiteCadastro.destroy()
        except ValueError as err:
            self.limiteCadastro.mostraErro('Erro de Validação', str(err))

    def verificaConflito(self, medico, dia, hora):
        """Verifica se já existe consulta para o médico no dia/hora"""
        for consulta in self.consultas:
            if (consulta.medico.crm == medico.crm and
                consulta.dia == dia and
                    consulta.hora == hora):
                return True
        return False

    def getConsultasPorMedico(self, medico):
        """Retorna lista de consultas de um médico específico"""
        return [c for c in self.consultas if c.medico.crm == medico.crm]

    def listaConsultas(self):
        """Abre janela de listagem de consultas"""
        self.limiteLista = LimiteMostraConsultas(self, self.ctrlMedico)
