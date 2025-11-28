# Guia Completo: Desenvolvendo Sistema de Consultas Médicas do Zero

## 📚 Sumário

1. [Análise do Problema](#análise-do-problema)
2. [Planejamento da Arquitetura](#planejamento-da-arquitetura)
3. [Etapa 1: Estrutura Básica](#etapa-1-estrutura-básica)
4. [Etapa 2: Model de Médico](#etapa-2-model-de-médico)
5. [Etapa 3: Controller e Persistência de Médico](#etapa-3-controller-e-persistência-de-médico)
6. [Etapa 4: View de Cadastro de Médico](#etapa-4-view-de-cadastro-de-médico)
7. [Etapa 5: Model de Consulta](#etapa-5-model-de-consulta)
8. [Etapa 6: View de Cadastro de Consulta](#etapa-6-view-de-cadastro-de-consulta)
9. [Etapa 7: Controller de Consulta](#etapa-7-controller-de-consulta)
10. [Etapa 8: View de Listagem](#etapa-8-view-de-listagem)
11. [Etapa 9: Integração Final](#etapa-9-integração-final)
12. [Etapa 10: Testes e Validações](#etapa-10-testes-e-validações)

---

## Análise do Problema

### 📋 Requisitos Extraídos

#### Questão 1 - Médicos

**Dados:**

- Nome (texto livre)
- CRM (texto livre)
- Especialidade (lista fechada com 8 opções)

**Especialidades válidas:**

- Pediatria
- Cardiologia
- Neurologia
- Oftalmologia
- Ortopedia
- Gastroenterologia
- Psiquiatria
- Pneumologia

**Regras:**

- Validar especialidade usando Exceptions
- Formulário com 3 campos de texto

#### Questão 2 - Consultas

**Dados:**

- Nome do paciente (texto livre)
- Dia (número 1-30)
- Hora (número 9-17)
- Especialidade (Combobox)
- Médico (Listbox filtrada)

**Regras de Negócio:**

- Dia: 1 a 30 (mês seguinte, sempre 30 dias)
- Hora: 9 a 17 (atendimento de 1h, início de cada hora)
- Validar dia e hora
- Ao selecionar especialidade → filtrar médicos no Listbox
- Verificar conflito de horário (mesmo médico, mesmo dia/hora)
- Mensagem de erro específica para conflitos

#### Questão 3 - Listagem

**Interface:**

- Combobox com todos os médicos
- Ao selecionar médico → mostrar suas consultas
- Formato: Dia / Hora / Nome do Paciente

**Persistência:**

- Todos os dados em arquivos
- Pré-cadastrar 2 médicos de 3 especialidades (6 total)

---

## Planejamento da Arquitetura

### 🏗️ Estrutura de Arquivos

```
medicov2/
├── main.py          # Ponto de entrada + Controller Principal + View Principal
├── medico.py        # Model Medico + Views + Controller de Médico
├── consulta.py      # Model Consulta + Views + Controller de Consulta
├── medicos.pickle   # Persistência de médicos (gerado automaticamente)
└── consultas.pickle # Persistência de consultas (gerado automaticamente)
```

### 🎯 Padrão MVC Aplicado

**Por que MVC?**

- Separação de responsabilidades
- Facilita manutenção
- Segue o padrão do curso

**Divisão:**

- **Model**: Classes Medico e Consulta (dados + validações)
- **View**: Janelas Tkinter (formulários e listagens)
- **Controller**: Lógica de negócio, persistência, coordenação

### 📊 Diagrama de Classes

```
┌─────────────────────┐
│   ControlePrincipal │
│   (main.py)         │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────┐   ┌───▼────┐
│CtrlMed │   │CtrlCon │
│        │◄──│        │ (precisa de médicos)
└───┬────┘   └───┬────┘
    │            │
┌───▼────┐   ┌───▼────┐
│ Medico │   │Consulta│
│(Model) │   │(Model) │
└────────┘   └───┬────┘
                 │
                 │ referência
                 ▼
             ┌────────┐
             │ Medico │
             └────────┘
```

---

## Etapa 1: Estrutura Básica

### 🎯 Objetivo

Criar o esqueleto da aplicação com janela principal e menu.

### 📝 Passo 1.1: Criar arquivo main.py

**O que fazer:**

1. Criar pasta `medicov2`
2. Criar arquivo `main.py`
3. Importar Tkinter

```python
from tkinter import *
```

**Por que começar pelo main.py?**

- É o ponto de entrada da aplicação
- Define a estrutura geral
- Facilita visualizar o que precisa ser implementado

### 📝 Passo 1.2: Criar classe LimitePrincipal (View)

**Responsabilidades:**

- Criar janela principal
- Criar menu com opções
- Conectar menu ao controller

```python
class LimitePrincipal:
    def __init__(self, root, controle):
        self.root = root
        self.controle = controle

        # Configurar janela
        self.root.title('Sistema de Consultas Médicas')
        self.root.geometry('400x300')

        # Criar menu
        self.menubar = Menu(self.root)

        # Menu Médico
        self.menuMedico = Menu(self.menubar, tearoff=0)
        self.menuMedico.add_command(label='Cadastrar',
                                     command=self.controle.cadastrarMedico)
        self.menubar.add_cascade(label='Médico', menu=self.menuMedico)

        # Menu Consulta
        self.menuConsulta = Menu(self.menubar, tearoff=0)
        self.menuConsulta.add_command(label='Cadastrar',
                                       command=self.controle.cadastrarConsulta)
        self.menuConsulta.add_command(label='Listar Consultas',
                                       command=self.controle.listarConsultas)
        self.menubar.add_cascade(label='Consulta', menu=self.menuConsulta)

        self.root.config(menu=self.menubar)
```

**Detalhes importantes:**

- `tearoff=0`: Remove linha pontilhada do menu
- `command=`: Conecta item do menu a método do controller
- Passar `self.controle` para chamar métodos do controller

### 📝 Passo 1.3: Criar classe ControlePrincipal

**Responsabilidades:**

- Criar janela Tk()
- Instanciar controllers específicos
- Delegar chamadas do menu

```python
class ControlePrincipal:
    def __init__(self):
        self.root = Tk()

        # TODO: Criar controllers
        # self.ctrlMedico = CtrlMedico()
        # self.ctrlConsulta = CtrlConsulta(self.ctrlMedico)

        self.limite = LimitePrincipal(self.root, self)

        self.root.mainloop()

    def cadastrarMedico(self):
        # TODO: Implementar
        print("Cadastrar médico")

    def cadastrarConsulta(self):
        # TODO: Implementar
        print("Cadastrar consulta")

    def listarConsultas(self):
        # TODO: Implementar
        print("Listar consultas")
```

### 📝 Passo 1.4: Criar ponto de entrada

```python
if __name__ == '__main__':
    app = ControlePrincipal()
```

### ✅ Teste da Etapa 1

Execute: `python main.py`

**Deve aparecer:**

- Janela com título "Sistema de Consultas Médicas"
- Menu "Médico" com opção "Cadastrar"
- Menu "Consulta" com "Cadastrar" e "Listar Consultas"
- Ao clicar nos menus → print no console (por enquanto)

---

## Etapa 2: Model de Médico

### 🎯 Objetivo

Criar a classe Medico com validações.

### 📝 Passo 2.1: Criar arquivo medico.py

```python
class Medico:
    """Model - Representa um médico"""

    # Constante de classe com especialidades válidas
    ESPECIALIDADES = [
        'Pediatria', 'Cardiologia', 'Neurologia',
        'Oftalmologia', 'Ortopedia', 'Gastroenterologia',
        'Psiquiatria', 'Pneumologia'
    ]
```

**Por que usar constante de classe?**

- Centraliza valores válidos
- Facilita manutenção
- Pode ser reutilizada em outras partes do código

### 📝 Passo 2.2: Implementar **init** com validação

```python
    def __init__(self, nome, crm, especialidade):
        self.__nome = nome
        self.__crm = crm

        # VALIDAÇÃO COM EXCEPTION (Requisito da Questão 1)
        if especialidade not in self.ESPECIALIDADES:
            raise ValueError(
                f'Especialidade inválida. Opções válidas: {", ".join(self.ESPECIALIDADES)}'
            )

        self.__especialidade = especialidade
```

**Detalhes importantes:**

- Atributos privados: `__nome`, `__crm`, `__especialidade`
- Validação ANTES de atribuir o valor
- `raise ValueError`: Lança exceção (requisito do exercício)
- Mensagem clara mostrando opções válidas

### 📝 Passo 2.3: Criar properties (getters)

```python
    @property
    def nome(self):
        return self.__nome

    @property
    def crm(self):
        return self.__crm

    @property
    def especialidade(self):
        return self.__especialidade
```

**Por que properties?**

- Encapsulamento: acesso controlado aos atributos
- Boas práticas de OO
- Padrão esperado no curso

### 📝 Passo 2.4: Método **str** (opcional, mas útil)

```python
    def __str__(self):
        return f"{self.nome} - {self.especialidade} (CRM: {self.crm})"
```

**Utilidade:**

- Facilita debug
- Representação legível do objeto

### ✅ Teste da Etapa 2

Adicione ao final de `medico.py`:

```python
if __name__ == '__main__':
    # Teste válido
    try:
        m1 = Medico('Dr. João', '12345', 'Pediatria')
        print(f"✓ Médico criado: {m1}")
    except ValueError as e:
        print(f"✗ Erro: {e}")

    # Teste inválido
    try:
        m2 = Medico('Dr. Maria', '67890', 'Dermatologia')
        print(f"✓ Médico criado: {m2}")
    except ValueError as e:
        print(f"✗ Erro esperado: {e}")
```

Execute: `python medico.py`

**Resultado esperado:**

```
✓ Médico criado: Dr. João - Pediatria (CRM: 12345)
✗ Erro esperado: Especialidade inválida. Opções válidas: Pediatria, ...
```

---

## Etapa 3: Controller e Persistência de Médico

### 🎯 Objetivo

Gerenciar lista de médicos e salvar em arquivo.

### 📝 Passo 3.1: Importar bibliotecas necessárias

No início de `medico.py`:

```python
from tkinter import *
from tkinter import messagebox
import os.path
import pickle
```

**O que cada uma faz:**

- `tkinter`: Widgets para Views
- `messagebox`: Diálogos de sucesso/erro
- `os.path`: Verificar se arquivo existe
- `pickle`: Serialização de objetos Python

### 📝 Passo 3.2: Criar classe CtrlMedico

```python
class CtrlMedico:
    """Controller - Gerencia médicos"""

    def __init__(self):
        # Carrega dados do arquivo ou cria lista vazia
        if os.path.isfile('medicos.pickle'):
            with open('medicos.pickle', 'rb') as file:
                self.medicos = pickle.load(file)
        else:
            self.medicos = []
```

**Lógica de carregamento:**

1. Verifica se arquivo existe
2. Se existe → carrega (deserializa)
3. Se não → cria lista vazia

**Por que pickle?**

- Serializa objetos Python diretamente
- Simples de usar
- Mantém estrutura de objetos

### 📝 Passo 3.3: Método para salvar dados

```python
    def salvaMedicos(self):
        """Persiste médicos em arquivo pickle"""
        with open('medicos.pickle', 'wb') as file:
            pickle.dump(self.medicos, file)
```

**Detalhes:**

- `'wb'`: Write Binary (necessário para pickle)
- `pickle.dump()`: Serializa e salva
- Chamado após adicionar/modificar médicos

### 📝 Passo 3.4: Métodos de consulta

```python
    def getMedicosPorEspecialidade(self, especialidade):
        """Retorna lista de médicos de uma especialidade"""
        return [med for med in self.medicos if med.especialidade == especialidade]

    def getEspecialidadesDisponiveis(self):
        """Retorna especialidades que têm médicos cadastrados"""
        especialidades = set()
        for medico in self.medicos:
            especialidades.add(medico.especialidade)
        return sorted(list(especialidades))

    def getTodosMedicos(self):
        """Retorna lista de todos os médicos"""
        return self.medicos
```

**Por que esses métodos?**

- `getMedicosPorEspecialidade`: Usado no Combobox de consultas (Questão 2)
- `getEspecialidadesDisponiveis`: Popular Combobox
- `getTodosMedicos`: Listagem de consultas (Questão 3)

### 📝 Passo 3.5: Criar dados iniciais

```python
    def __init__(self):
        if os.path.isfile('medicos.pickle'):
            with open('medicos.pickle', 'rb') as file:
                self.medicos = pickle.load(file)
        else:
            # DADOS INICIAIS (requisito: 2 médicos de 3 especialidades)
            self.medicos = [
                Medico('Dr. João Silva', '12345-SP', 'Pediatria'),
                Medico('Dra. Maria Santos', '23456-RJ', 'Pediatria'),
                Medico('Dr. Carlos Souza', '34567-MG', 'Cardiologia'),
                Medico('Dra. Ana Paula', '45678-SP', 'Cardiologia'),
                Medico('Dr. Pedro Lima', '56789-RS', 'Neurologia'),
                Medico('Dra. Fernanda Costa', '67890-BA', 'Neurologia'),
            ]
            self.salvaMedicos()  # Salva dados iniciais
```

**Atende requisito:**

- 2 médicos × 3 especialidades = 6 médicos total
- Dados já persistidos para correção

---

## Etapa 4: View de Cadastro de Médico

### 🎯 Objetivo

Criar formulário para cadastrar médicos.

### 📝 Passo 4.1: Criar classe LimiteCadastraMedico

```python
class LimiteCadastraMedico(Toplevel):
    """View - Janela para cadastrar médico"""

    def __init__(self, controller):
        Toplevel.__init__(self)
        self.title('Cadastrar Médico')
        self.geometry('400x200')
        self.controller = controller
```

**Por que Toplevel?**

- Cria janela secundária (não fecha a principal)
- Permite múltiplas janelas abertas
- Padrão para formulários

### 📝 Passo 4.2: Criar campo Nome

```python
        # Frame Nome
        self.nomeFrame = Frame(self)
        self.nomeLabel = Label(self.nomeFrame, text='Nome: ')
        self.nomeEntry = Entry(self.nomeFrame, width=30)
        self.nomeLabel.pack(side='left')
        self.nomeEntry.pack(side='left', padx=5)
        self.nomeFrame.pack(pady=10)
```

**Padrão Frame + Label + Entry:**

1. Frame: Container para agrupar widgets
2. Label: Descrição do campo
3. Entry: Campo de entrada
4. `pack(side='left')`: Organiza horizontalmente
5. `pack(pady=10)`: Espaçamento vertical

### 📝 Passo 4.3: Criar campos CRM e Especialidade

```python
        # Frame CRM
        self.crmFrame = Frame(self)
        self.crmLabel = Label(self.crmFrame, text='CRM: ')
        self.crmEntry = Entry(self.crmFrame, width=30)
        self.crmLabel.pack(side='left')
        self.crmEntry.pack(side='left', padx=5)
        self.crmFrame.pack(pady=10)

        # Frame Especialidade
        self.especialidadeFrame = Frame(self)
        self.especialidadeLabel = Label(self.especialidadeFrame, text='Especialidade: ')
        self.especialidadeEntry = Entry(self.especialidadeFrame, width=30)
        self.especialidadeLabel.pack(side='left')
        self.especialidadeEntry.pack(side='left', padx=5)
        self.especialidadeFrame.pack(pady=10)
```

**Nota:** Requisito pede 3 campos de texto (não Combobox)

### 📝 Passo 4.4: Adicionar dica de especialidades

```python
        # Dica de especialidades válidas
        self.dicaLabel = Label(
            self,
            text='Especialidades: Pediatria, Cardiologia, Neurologia, Oftalmologia,\n' +
                 'Ortopedia, Gastroenterologia, Psiquiatria, Pneumologia',
            font=('Arial', 8),
            fg='gray'
        )
        self.dicaLabel.pack(pady=5)
```

**Por que adicionar dica?**

- Melhora UX
- Usuário sabe opções válidas
- Reduz erros de digitação

### 📝 Passo 4.5: Criar botão Cadastrar

```python
        # Botão Cadastrar
        self.btnCadastrar = Button(
            self,
            text='Cadastrar',
            command=self.controller.cadastrarMedico
        )
        self.btnCadastrar.pack(pady=10)
```

**Conexão com Controller:**

- `command=self.controller.cadastrarMedico`
- Quando clicado → chama método do controller

### 📝 Passo 4.6: Métodos auxiliares

```python
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

    def mostraErro(self, titulo, msg):
        messagebox.showerror(titulo, msg)
```

**Por que na View?**

- View é responsável por exibir mensagens
- Controller chama esses métodos
- Separação de responsabilidades

### 📝 Passo 4.7: Implementar handler no Controller

```python
class CtrlMedico:
    # ... código anterior ...

    def cadastraMedico(self):
        """Abre janela de cadastro"""
        self.limiteCadastro = LimiteCadastraMedico(self)

    def cadastrarMedico(self):
        """Handler do botão cadastrar"""
        # 1. Obter dados da View
        nome = self.limiteCadastro.nomeEntry.get().strip()
        crm = self.limiteCadastro.crmEntry.get().strip()
        especialidade = self.limiteCadastro.especialidadeEntry.get().strip()

        # 2. Validar preenchimento
        if not nome or not crm or not especialidade:
            self.limiteCadastro.mostraErro('Erro', 'Todos os campos são obrigatórios!')
            return

        # 3. Tentar criar objeto (validação de especialidade)
        try:
            medico = Medico(nome, crm, especialidade)
            self.medicos.append(medico)
            self.salvaMedicos()
            self.limiteCadastro.mostraJanela('Sucesso', f'Médico {nome} cadastrado com sucesso!')
            self.limiteCadastro.destroy()  # Fecha janela
        except ValueError as err:
            self.limiteCadastro.mostraErro('Erro de Validação', str(err))
```

**Fluxo completo:**

1. Obter dados dos campos Entry
2. `.strip()`: Remove espaços em branco
3. Validar campos vazios
4. `try/except`: Captura erro de validação do Model
5. Se sucesso: salva, mostra mensagem, fecha janela
6. Se erro: mostra mensagem de erro

### 📝 Passo 4.8: Conectar ao main.py

```python
# No início de main.py
from medico import CtrlMedico

class ControlePrincipal:
    def __init__(self):
        self.root = Tk()

        # Criar controller de médico
        self.ctrlMedico = CtrlMedico()

        self.limite = LimitePrincipal(self.root, self)
        self.root.mainloop()

    def cadastrarMedico(self):
        self.ctrlMedico.cadastraMedico()
```

### ✅ Teste da Etapa 4

Execute: `python main.py`

**Testar:**

1. Menu Médico → Cadastrar
2. Preencher nome e CRM
3. Testar especialidade inválida ("Dermatologia") → deve dar erro
4. Testar especialidade válida ("Pediatria") → deve salvar
5. Fechar e reabrir programa → médico deve estar persistido

---

## Etapa 5: Model de Consulta

### 🎯 Objetivo

Criar classe Consulta com validações de dia e hora.

### 📝 Passo 5.1: Criar arquivo consulta.py

```python
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

        self.__medico = medico  # Objeto Medico
```

**Validações importantes:**

- `isinstance(dia, int)`: Garante que é número
- `dia < 1 or dia > 30`: Range válido
- Mesma lógica para hora
- `medico`: Referência ao objeto Medico (composição)

### 📝 Passo 5.2: Criar properties

```python
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
```

**Formato `{self.dia:02d}`:**

- `:02d`: Formata número com 2 dígitos (ex: 01, 02, ..., 30)

---

## Etapa 6: View de Cadastro de Consulta

### 🎯 Objetivo

Criar formulário complexo com Combobox e Listbox dinâmica.

### 📝 Passo 6.1: Estrutura básica da classe

```python
class LimiteCadastraConsulta(Toplevel):
    """View - Janela para cadastrar consulta"""

    def __init__(self, controller, ctrlMedico):
        Toplevel.__init__(self)
        self.title('Cadastrar Consulta')
        self.geometry('400x500')
        self.controller = controller
        self.ctrlMedico = ctrlMedico  # Precisa acessar médicos
```

**Por que recebe ctrlMedico?**

- Precisa buscar especialidades
- Precisa buscar médicos por especialidade
- Comunicação entre módulos

### 📝 Passo 6.2: Campos simples (Nome, Dia, Hora)

```python
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
        self.labelHora = Label(self.frameHora, text='Informe o horário (9-17):')
        self.entryHora = Entry(self.frameHora, width=10)
        self.labelHora.pack(side='left')
        self.entryHora.pack(side='left', padx=5)
        self.frameHora.pack(pady=10)
```

### 📝 Passo 6.3: Combobox de Especialidades

```python
        # Especialidade (Combobox)
        self.frameEspecialidade = Frame(self)
        self.labelEspecialidade = Label(self.frameEspecialidade,
                                         text='Escolha a especialidade:')
        self.labelEspecialidade.pack()

        # Buscar especialidades disponíveis do controller
        especialidades = self.ctrlMedico.getEspecialidadesDisponiveis()

        self.comboEspecialidade = ttk.Combobox(
            self.frameEspecialidade,
            values=especialidades,
            state='readonly',  # Só permite seleção, não digitação
            width=30
        )
        self.comboEspecialidade.set('Selecione...')
        self.comboEspecialidade.bind('<<ComboboxSelected>>',
                                      self.aoSelecionarEspecialidade)
        self.comboEspecialidade.pack(pady=5)
        self.frameEspecialidade.pack(pady=10)
```

**Pontos-chave:**

- `ttk.Combobox`: Precisa importar ttk
- `values=especialidades`: Lista de opções
- `state='readonly'`: Impede digitação
- `bind('<<ComboboxSelected>>', ...)`: Evento onChange

### 📝 Passo 6.4: Listbox de Médicos

```python
        # Médicos (Listbox)
        self.frameMedicos = Frame(self)
        self.labelMedicos = Label(self.frameMedicos, text='Escolha o médico:')
        self.labelMedicos.pack()

        self.listboxMedicos = Listbox(self.frameMedicos,
                                       selectmode=SINGLE,
                                       width=40,
                                       height=6)
        self.listboxMedicos.pack(pady=5)
        self.frameMedicos.pack(pady=10)
```

**Configurações:**

- `selectmode=SINGLE`: Só permite selecionar um item
- `width=40, height=6`: Dimensões em caracteres/linhas
- Inicialmente vazio (preenchido ao selecionar especialidade)

### 📝 Passo 6.5: Implementar evento de seleção

```python
    def aoSelecionarEspecialidade(self, event):
        """Atualiza listbox de médicos quando especialidade é selecionada"""
        especialidade = self.comboEspecialidade.get()
        medicos = self.ctrlMedico.getMedicosPorEspecialidade(especialidade)

        # Limpa listbox
        self.listboxMedicos.delete(0, END)

        # Preenche com médicos da especialidade
        for medico in medicos:
            self.listboxMedicos.insert(END, medico.nome)
```

**Fluxo:**

1. Usuário seleciona especialidade no Combobox
2. Evento `<<ComboboxSelected>>` dispara
3. Chama `aoSelecionarEspecialidade`
4. Busca médicos da especialidade no controller
5. Limpa Listbox anterior
6. Insere nomes dos médicos

### 📝 Passo 6.6: Método para obter médico selecionado

```python
    def getMedicoSelecionado(self):
        """Retorna o objeto Medico selecionado"""
        selecao = self.listboxMedicos.curselection()
        if not selecao:
            return None

        nome_medico = self.listboxMedicos.get(selecao[0])
        especialidade = self.comboEspecialidade.get()
        medicos = self.ctrlMedico.getMedicosPorEspecialidade(especialidade)

        # Busca objeto Medico pelo nome
        for medico in medicos:
            if medico.nome == nome_medico:
                return medico
        return None
```

**Por que esse método?**

- Listbox só guarda strings (nomes)
- Precisamos do objeto Medico completo
- Controller usa esse método

### 📝 Passo 6.7: Botões

```python
        # Botões
        self.frameButtons = Frame(self)
        self.btnCadastrar = Button(self.frameButtons,
                                    text='Cadastrar Consulta',
                                    command=self.controller.cadastrarConsulta)
        self.btnLimpar = Button(self.frameButtons,
                                text='Limpar',
                                command=self.limparCampos)
        self.btnCadastrar.pack(side='left', padx=5)
        self.btnLimpar.pack(side='left', padx=5)
        self.frameButtons.pack(pady=15)
```

### 📝 Passo 6.8: Método limpar campos

```python
    def limparCampos(self):
        """Limpa todos os campos do formulário"""
        self.entryNome.delete(0, END)
        self.entryDia.delete(0, END)
        self.entryHora.delete(0, END)
        self.comboEspecialidade.set('Selecione...')
        self.listboxMedicos.delete(0, END)
```

---

## Etapa 7: Controller de Consulta

### 🎯 Objetivo

Implementar lógica de cadastro com validações e verificação de conflitos.

### 📝 Passo 7.1: Estrutura básica do Controller

```python
class CtrlConsulta:
    """Controller - Gerencia consultas"""

    def __init__(self, ctrlMedico):
        self.ctrlMedico = ctrlMedico  # Referência ao controller de médicos

        # Carregar consultas do arquivo
        if os.path.isfile('consultas.pickle'):
            with open('consultas.pickle', 'rb') as file:
                self.consultas = pickle.load(file)
        else:
            self.consultas = []
```

**Por que recebe ctrlMedico?**

- Precisa acessar lista de médicos
- Precisa passar para a View
- Comunicação entre módulos

### 📝 Passo 7.2: Persistência

```python
    def salvaConsultas(self):
        """Persiste consultas em arquivo pickle"""
        with open('consultas.pickle', 'wb') as file:
            pickle.dump(self.consultas, file)
```

### 📝 Passo 7.3: Abrir janela de cadastro

```python
    def cadastraConsulta(self):
        """Abre janela de cadastro de consulta"""
        self.limiteCadastro = LimiteCadastraConsulta(self, self.ctrlMedico)
```

**Passa dois parâmetros:**

- `self`: Controller de consulta
- `self.ctrlMedico`: Controller de médico

### 📝 Passo 7.4: Verificar conflito de horário

```python
    def verificaConflito(self, medico, dia, hora):
        """Verifica se já existe consulta para o médico no dia/hora"""
        for consulta in self.consultas:
            if (consulta.medico.crm == medico.crm and
                consulta.dia == dia and
                consulta.hora == hora):
                return True
        return False
```

**Lógica:**

- Percorre todas as consultas
- Compara CRM do médico (único)
- Compara dia e hora
- Se encontrar igual → conflito!

### 📝 Passo 7.5: Handler de cadastro (parte 1: validações)

```python
    def cadastrarConsulta(self):
        """Handler do botão cadastrar consulta"""
        # 1. Obter dados da View
        paciente = self.limiteCadastro.entryNome.get().strip()
        dia_str = self.limiteCadastro.entryDia.get().strip()
        hora_str = self.limiteCadastro.entryHora.get().strip()
        medico = self.limiteCadastro.getMedicoSelecionado()

        # 2. Validar preenchimento
        if not paciente:
            self.limiteCadastro.mostraErro('Erro', 'Nome do paciente é obrigatório!')
            return

        if not dia_str or not hora_str:
            self.limiteCadastro.mostraErro('Erro', 'Dia e hora são obrigatórios!')
            return

        if not medico:
            self.limiteCadastro.mostraErro('Erro', 'Selecione um médico!')
            return
```

**Validações básicas:**

- Campos não podem estar vazios
- Médico deve ser selecionado

### 📝 Passo 7.6: Handler de cadastro (parte 2: conversão)

```python
        # 3. Converter para inteiro
        try:
            dia = int(dia_str)
            hora = int(hora_str)
        except ValueError:
            self.limiteCadastro.mostraErro('Erro',
                'Dia e hora devem ser números inteiros!')
            return
```

**Por que try/except?**

- Usuário pode digitar texto em vez de número
- `int()` lança ValueError se não for número
- Mensagem clara de erro

### 📝 Passo 7.7: Handler de cadastro (parte 3: verificações finais)

```python
        # 4. Verificar conflito de horário
        if self.verificaConflito(medico, dia, hora):
            self.limiteCadastro.mostraErro('Conflito',
                'Já existe consulta agendada nesta data, escolha outra.')
            return

        # 5. Criar consulta
        try:
            consulta = Consulta(paciente, dia, hora, medico)
            self.consultas.append(consulta)
            self.salvaConsultas()

            mensagem = (f'Consulta agendada com sucesso!\n'
                       f'Paciente: {paciente}\n'
                       f'Dia: {dia}\n'
                       f'Hora: {hora}h\n'
                       f'Médico: {medico.nome}')

            self.limiteCadastro.mostraJanela('Sucesso', mensagem)
            self.limiteCadastro.destroy()

        except ValueError as err:
            self.limiteCadastro.mostraErro('Erro de Validação', str(err))
```

**Fluxo completo:**

1. Verifica conflito (requisito da questão)
2. Tenta criar objeto Consulta (valida dia/hora)
3. Se sucesso: salva, mostra mensagem detalhada, fecha janela
4. Se erro: mostra erro de validação do Model

---

## Etapa 8: View de Listagem

### 🎯 Objetivo

Criar tela para listar consultas por médico.

### 📝 Passo 8.1: Estrutura da classe

```python
class LimiteMostraConsultas(Toplevel):
    """View - Janela para listar consultas por médico"""

    def __init__(self, controller, ctrlMedico):
        Toplevel.__init__(self)
        self.title('Consultas Marcadas')
        self.geometry('500x400')
        self.controller = controller
        self.ctrlMedico = ctrlMedico
```

### 📝 Passo 8.2: Título

```python
        # Título
        self.labelTitulo = Label(self,
                                 text='Consultas por Médico',
                                 font=('Arial', 14, 'bold'))
        self.labelTitulo.pack(pady=10)
```

### 📝 Passo 8.3: Combobox de médicos

```python
        # Combobox de médicos
        self.frameMedico = Frame(self)
        self.labelMedico = Label(self.frameMedico, text='Selecione o médico:')
        self.labelMedico.pack()

        # Buscar TODOS os médicos
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
```

**Diferença da tela de cadastro:**

- Aqui lista TODOS os médicos (não filtra por especialidade)
- List comprehension: `[medico.nome for medico in medicos]`

### 📝 Passo 8.4: Listbox de consultas com scrollbar

```python
        # Listbox de consultas
        self.frameConsultas = Frame(self)
        self.labelConsultas = Label(self.frameConsultas,
                                     text='Consultas marcadas:',
                                     font=('Arial', 10, 'bold'))
        self.labelConsultas.pack()

        # Scrollbar
        scrollbar = Scrollbar(self.frameConsultas)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Listbox conectada à scrollbar
        self.listboxConsultas = Listbox(
            self.frameConsultas,
            width=60,
            height=15,
            yscrollcommand=scrollbar.set,
            font=('Courier', 10)  # Fonte monoespaçada para alinhamento
        )
        self.listboxConsultas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listboxConsultas.yview)

        self.frameConsultas.pack(pady=10, padx=20, fill=BOTH, expand=True)
```

**Por que Courier (fonte monoespaçada)?**

- Todos os caracteres têm mesma largura
- Facilita alinhamento de colunas
- Formato tabular fica visualmente melhor

### 📝 Passo 8.5: Evento de seleção

```python
    def aoSelecionarMedico(self, event):
        """Atualiza lista de consultas quando médico é selecionado"""
        nome_medico = self.comboMedico.get()

        # Encontrar objeto Medico
        medico = None
        for med in self.ctrlMedico.getTodosMedicos():
            if med.nome == nome_medico:
                medico = med
                break

        if medico:
            consultas = self.controller.getConsultasPorMedico(medico)
            self.atualizarConsultas(consultas)
```

### 📝 Passo 8.6: Atualizar listbox

```python
    def atualizarConsultas(self, consultas):
        """Atualiza a listbox com as consultas"""
        self.listboxConsultas.delete(0, END)

        if not consultas:
            self.listboxConsultas.insert(END,
                "Nenhuma consulta agendada para este médico.")
        else:
            # Cabeçalho (formato do requisito)
            self.listboxConsultas.insert(END, "Dia / Hora / Nome do Paciente")
            self.listboxConsultas.insert(END, "-" * 50)

            # Ordenar por dia e hora
            consultas_ordenadas = sorted(consultas, key=lambda c: (c.dia, c.hora))

            # Inserir consultas formatadas
            for consulta in consultas_ordenadas:
                linha = f"{consulta.dia:02d}   /  {consulta.hora:02d}h  / {consulta.paciente}"
                self.listboxConsultas.insert(END, linha)
```

**Detalhes importantes:**

- Formato exato do requisito: "Dia / Hora / Nome do Paciente"
- Linha de separação com "-"
- Ordenação por dia e hora
- Formatação com 2 dígitos: `:02d`

### 📝 Passo 8.7: Métodos no Controller

```python
class CtrlConsulta:
    # ... código anterior ...

    def getConsultasPorMedico(self, medico):
        """Retorna lista de consultas de um médico específico"""
        return [c for c in self.consultas if c.medico.crm == medico.crm]

    def listaConsultas(self):
        """Abre janela de listagem de consultas"""
        self.limiteLista = LimiteMostraConsultas(self, self.ctrlMedico)
```

---

## Etapa 9: Integração Final

### 🎯 Objetivo

Conectar todos os componentes no main.py.

### 📝 Passo 9.1: Imports completos

```python
from tkinter import *
from medico import CtrlMedico
from consulta import CtrlConsulta
```

### 📝 Passo 9.2: Criar controllers na ordem correta

```python
class ControlePrincipal:
    def __init__(self):
        self.root = Tk()

        # 1. Criar controller de médico primeiro
        self.ctrlMedico = CtrlMedico()

        # 2. Criar controller de consulta (precisa do ctrlMedico)
        self.ctrlConsulta = CtrlConsulta(self.ctrlMedico)

        # 3. Criar view principal
        self.limite = LimitePrincipal(self.root, self)

        self.root.mainloop()
```

**Ordem importa!**

- CtrlConsulta depende de CtrlMedico
- Passar como parâmetro

### 📝 Passo 9.3: Implementar métodos delegadores

```python
    def cadastrarMedico(self):
        """Delega para o controller de médico"""
        self.ctrlMedico.cadastraMedico()

    def cadastrarConsulta(self):
        """Delega para o controller de consulta"""
        self.ctrlConsulta.cadastraConsulta()

    def listarConsultas(self):
        """Delega para o controller de consulta"""
        self.ctrlConsulta.listaConsultas()
```

**Padrão de delegação:**

- Menu chama método do ControlePrincipal
- ControlePrincipal delega para controller específico
- Controller específico abre View correspondente

### 📝 Passo 9.4: Melhorar tela inicial (opcional)

```python
class LimitePrincipal:
    def __init__(self, root, controle):
        # ... código do menu ...

        # Tela inicial com instruções
        self.frameInicial = Frame(self.root)

        self.labelTitulo = Label(self.frameInicial,
                                 text='Sistema de Consultas Médicas',
                                 font=('Arial', 16, 'bold'))
        self.labelTitulo.pack(pady=20)

        self.labelInstrucoes = Label(self.frameInicial,
                                      text='Use o menu acima para:\n\n' +
                                           '• Cadastrar médicos\n' +
                                           '• Agendar consultas\n' +
                                           '• Listar consultas por médico',
                                      font=('Arial', 11),
                                      justify=LEFT)
        self.labelInstrucoes.pack(pady=20)

        self.frameInicial.pack(expand=True)
```

---

## Etapa 10: Testes e Validações

### 🎯 Objetivo

Garantir que todos os requisitos foram atendidos.

### ✅ Teste 1: Cadastro de Médico

**Cenários:**

1. **Sucesso:**

   - Nome: Dr. Carlos Lima
   - CRM: 99999-SP
   - Especialidade: Ortopedia
   - ✓ Deve salvar e fechar janela

2. **Especialidade inválida:**

   - Especialidade: Dermatologia
   - ✗ Deve mostrar erro com lista de especialidades válidas

3. **Campo vazio:**

   - Deixar campo Nome vazio
   - ✗ Deve mostrar erro "Todos os campos são obrigatórios"

4. **Persistência:**
   - Cadastrar médico
   - Fechar programa
   - Reabrir programa
   - Menu Consulta → Cadastrar
   - ✓ Médico deve aparecer no Combobox

### ✅ Teste 2: Cadastro de Consulta

**Cenários:**

1. **Sucesso completo:**

   - Paciente: Maria Silva
   - Dia: 15
   - Hora: 14
   - Especialidade: Pediatria (selecionar no Combobox)
   - Médico: Dr. João Silva (selecionar no Listbox)
   - ✓ Deve salvar e mostrar mensagem de sucesso

2. **Dia inválido:**

   - Dia: 35
   - ✗ Deve mostrar "Dia inválido! Informe um valor entre 1 e 30."

3. **Hora inválida:**

   - Hora: 20
   - ✗ Deve mostrar "Hora inválida! Informe um valor entre 9 e 17."

4. **Conflito de horário:**

   - Cadastrar consulta: Dia 15, Hora 14, Dr. João Silva
   - Tentar cadastrar outra: Dia 15, Hora 14, Dr. João Silva
   - ✗ Deve mostrar "Já existe consulta agendada nesta data, escolha outra"

5. **Sem médico selecionado:**

   - Preencher todos os campos exceto médico
   - ✗ Deve mostrar erro "Selecione um médico!"

6. **Filtro de médicos:**
   - Selecionar Pediatria → deve mostrar só pediatras
   - Selecionar Cardiologia → deve mostrar só cardiologistas
   - ✓ Listbox atualiza dinamicamente

### ✅ Teste 3: Listagem de Consultas

**Cenários:**

1. **Listagem básica:**

   - Cadastrar 3 consultas para Dr. João Silva
   - Abrir Menu Consulta → Listar Consultas
   - Selecionar Dr. João Silva
   - ✓ Deve mostrar 3 consultas ordenadas

2. **Formato correto:**

   - Verificar cabeçalho: "Dia / Hora / Nome do Paciente"
   - Verificar linha de separação
   - Verificar formato: "15 / 14h / Maria Silva"
   - ✓ Alinhamento correto

3. **Médico sem consultas:**

   - Selecionar médico que não tem consultas
   - ✓ Deve mostrar "Nenhuma consulta agendada para este médico."

4. **Ordenação:**
   - Cadastrar consultas fora de ordem:
     - Dia 20, Hora 10
     - Dia 15, Hora 14
     - Dia 20, Hora 9
   - ✓ Deve listar ordenado por dia, depois hora:
     - 15 / 14h
     - 20 / 09h
     - 20 / 10h

### ✅ Teste 4: Persistência

**Cenários:**

1. **Médicos:**

   - Cadastrar 2 médicos
   - Fechar programa
   - Reabrir
   - ✓ Médicos devem estar lá

2. **Consultas:**

   - Cadastrar 3 consultas
   - Fechar programa
   - Reabrir
   - Menu Consulta → Listar
   - ✓ Consultas devem estar lá

3. **Dados iniciais:**
   - Deletar medicos.pickle
   - Executar programa
   - ✓ Deve criar 6 médicos automaticamente

### ✅ Checklist Final dos Requisitos

**Questão 1:**

- [x] Formulário com 3 campos de texto
- [x] Validação de especialidade com Exception
- [x] Lista de 8 especialidades válidas
- [x] Mensagem de erro clara

**Questão 2:**

- [x] Campo nome do paciente
- [x] Campo dia (1-30)
- [x] Campo hora (9-17)
- [x] Combobox de especialidades
- [x] Listbox de médicos
- [x] Filtro: Combobox → Listbox
- [x] Validação de dia e hora
- [x] Verificação de conflito
- [x] Mensagem específica de conflito
- [x] Botão Cadastra Consulta

**Questão 3:**

- [x] Combobox com todos os médicos
- [x] Ao selecionar → mostrar consultas
- [x] Formato: Dia / Hora / Nome Paciente
- [x] Linha de separação

**Geral:**

- [x] Persistência em arquivo
- [x] 2 médicos de 3 especialidades (6 total)
- [x] Menu Médico → Cadastra
- [x] Menu Consulta → Cadastra, Lista Consultas

---

## 💡 Dicas e Boas Práticas

### 🔍 Debug

**Adicionar prints temporários:**

```python
def aoSelecionarEspecialidade(self, event):
    especialidade = self.comboEspecialidade.get()
    print(f"DEBUG: Especialidade selecionada: {especialidade}")
    medicos = self.ctrlMedico.getMedicosPorEspecialidade(especialidade)
    print(f"DEBUG: {len(medicos)} médicos encontrados")
```

### 🐛 Erros Comuns

1. **AttributeError: 'X' object has no attribute 'tk'**

   - Causa: Passar objeto errado para widget
   - Solução: Passar `self.root` em vez de `self`

2. **NameError: name 'ttk' is not defined**

   - Causa: Não importou ttk
   - Solução: `from tkinter import ttk`

3. **Combobox não filtra Listbox**

   - Causa: Esqueceu de fazer `bind`
   - Solução: Verificar `bind('<<ComboboxSelected>>', ...)`

4. **Dados não persistem**

   - Causa: Não chamou `salvaMedicos()` ou `salvaConsultas()`
   - Solução: Chamar após adicionar/modificar

5. **ValueError ao criar Consulta**
   - Causa: Passou string em vez de int
   - Solução: Converter com `int(dia_str)`

### 📚 Referências Rápidas

**Eventos Tkinter:**

- Botão: `command=metodo`
- Combobox: `bind('<<ComboboxSelected>>', metodo)`
- Listbox: `bind('<<ListboxSelect>>', metodo)`
- Entry: `bind('<Return>', metodo)` (Enter)

**Obter valores:**

- Entry: `entry.get()`
- Combobox: `combo.get()`
- Listbox: `listbox.get(listbox.curselection()[0])`

**Limpar widgets:**

- Entry: `entry.delete(0, END)`
- Listbox: `listbox.delete(0, END)`
- Combobox: `combo.set('')`

---

## 🎓 Conceitos Aprendidos

### Padrão MVC

- Separação de responsabilidades
- Model: dados + validações
- View: interface gráfica
- Controller: lógica + coordenação

### Tkinter Avançado

- Toplevel para janelas secundárias
- Combobox do ttk
- Listbox com seleção
- Eventos de mudança
- Menu com submenus

### Python

- Exceptions customizadas
- Properties
- List comprehensions
- Pickle para persistência
- Composição de objetos

### Validações

- Validação no Model (especialidade, dia, hora)
- Validação no Controller (campos vazios, conflitos)
- Mensagens de erro claras

---

## 🚀 Próximos Passos (Melhorias Opcionais)

1. **Edição de consultas:**

   - Botão para editar consulta existente
   - Alterar data/hora

2. **Cancelamento:**

   - Botão para cancelar consulta
   - Remover da lista

3. **Relatórios:**

   - Consultas por período
   - Consultas por especialidade

4. **Interface melhorada:**

   - Usar ttk.Entry, ttk.Label
   - Temas
   - Ícones

5. **Validações adicionais:**

   - CRM com formato específico
   - Nome com mínimo de caracteres

6. **Banco de dados:**
   - Substituir pickle por SQLite
   - Queries mais eficientes

---

## ✅ Conclusão

Este guia cobriu TODOS os aspectos do desenvolvimento:

1. ✅ Análise detalhada dos requisitos
2. ✅ Planejamento da arquitetura
3. ✅ Implementação passo a passo
4. ✅ Testes completos
5. ✅ Boas práticas
6. ✅ Tratamento de erros

Seguindo este guia, você consegue:

- Entender o PORQUÊ de cada decisão
- Implementar sozinho projetos similares
- Aplicar padrão MVC corretamente
- Validar dados adequadamente
- Criar interfaces complexas com Tkinter

**Boa sorte no desenvolvimento! 🎉**
