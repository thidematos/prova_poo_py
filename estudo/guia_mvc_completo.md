# Guia Completo: Padrão MVC em Python com Tkinter

## 📋 Índice

1. [O que é o Padrão MVC?](#o-que-é-o-padrão-mvc)
2. [Estrutura de Arquivos](#estrutura-de-arquivos)
3. [Etapa 1: Criando o Model](#etapa-1-criando-o-model)
4. [Etapa 2: Criando o Limite (View)](#etapa-2-criando-o-limite-view)
5. [Etapa 3: Criando o Controle (Controller)](#etapa-3-criando-o-controle-controller)
6. [Etapa 4: Integrando os Componentes](#etapa-4-integrando-os-componentes)
7. [Etapa 5: Comunicação entre Módulos](#etapa-5-comunicação-entre-módulos)
8. [Boas Práticas](#boas-práticas)
9. [Resumo Visual](#resumo-visual)

---

## O que é o Padrão MVC?

O **MVC (Model-View-Controller)** é um padrão de arquitetura de software que divide a aplicação em três componentes principais:

| Componente     | Nome no Código     | Responsabilidade                                         |
| -------------- | ------------------ | -------------------------------------------------------- |
| **Model**      | Classe de Entidade | Representa os dados e regras de negócio                  |
| **View**       | Limite (Limite\*)  | Interface gráfica com o usuário                          |
| **Controller** | Controle (Ctrl\*)  | Intermediário que processa eventos e atualiza Model/View |

### Por que usar MVC?

✅ **Separação de responsabilidades** - Cada classe tem uma função específica  
✅ **Manutenibilidade** - Fácil modificar uma parte sem afetar outras  
✅ **Testabilidade** - Componentes podem ser testados isoladamente  
✅ **Reutilização** - Models podem ser usados com diferentes Views

---

## Estrutura de Arquivos

No exemplo, cada **entidade do sistema** tem seu próprio arquivo contendo:

- A classe Model (entidade)
- A(s) classe(s) Limite (View)
- A classe Controle (Controller)

```
exemplo/
├── main.py           # Ponto de entrada + Controle Principal
├── estudante.py      # Model + Limite + Controle de Estudante
├── disciplina.py     # Model + Limite + Controle de Disciplina
└── turma.py          # Model + Limite + Controle de Turma
```

### Diagrama de Dependências

```
                    ┌─────────────────┐
                    │ ControlePrincipal│
                    │    (main.py)     │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  CtrlEstudante  │ │  CtrlDisciplina │ │    CtrlTurma    │
│ (estudante.py)  │ │ (disciplina.py) │ │   (turma.py)    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Etapa 1: Criando o Model

O **Model** é a classe mais simples. Ela representa uma **entidade do mundo real** com seus atributos.

### Regras para o Model:

1. ✅ Apenas atributos e propriedades
2. ✅ Getters e Setters quando necessário
3. ❌ **NÃO** deve conhecer a interface gráfica
4. ❌ **NÃO** deve importar tkinter

### Exemplo: Classe `Estudante`

```python
# estudante.py

class Estudante:
    """
    MODEL - Representa a entidade Estudante.
    Contém apenas dados e métodos de acesso.
    """

    def __init__(self, nroMatric, nome):
        self.__nroMatric = nroMatric  # Atributo privado
        self.__nome = nome            # Atributo privado

    @property
    def nroMatric(self):
        """Getter para número de matrícula."""
        return self.__nroMatric

    @property
    def nome(self):
        """Getter para nome."""
        return self.__nome
```

### Exemplo: Classe `Disciplina`

```python
# disciplina.py

class Disciplina:
    """MODEL - Representa a entidade Disciplina."""

    def __init__(self, codigo, nome):
        self.__codigo = codigo
        self.__nome = nome

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nome(self):
        return self.__nome
```

### Exemplo: Classe `Turma` (com relacionamentos)

```python
# turma.py

class Turma:
    """
    MODEL - Representa a entidade Turma.
    Possui relacionamento com Disciplina e Estudantes.
    """

    def __init__(self, codigo, disciplina, estudantes):
        self.__codigo = codigo
        self.__disciplina = disciplina      # Referência a um objeto Disciplina
        self.__estudantes = estudantes      # Lista de objetos Estudante

    @property
    def codigo(self):
        return self.__codigo

    @property
    def disciplina(self):
        return self.__disciplina

    @property
    def estudantes(self):
        return self.__estudantes
```

---

## Etapa 2: Criando o Limite (View)

O **Limite** é a camada de interface gráfica. Ela é responsável por:

- Exibir informações ao usuário
- Capturar entrada de dados
- Disparar eventos para o Controle

### Regras para o Limite:

1. ✅ Cria e organiza widgets (Label, Entry, Button, etc.)
2. ✅ Vincula eventos aos handlers do Controle
3. ✅ Recebe referência ao Controle no construtor
4. ❌ **NÃO** deve conter lógica de negócio
5. ❌ **NÃO** deve manipular dados diretamente

### Tipos de Limites

| Tipo              | Classe Base      | Uso                    |
| ----------------- | ---------------- | ---------------------- |
| Janela Principal  | `tk.Tk` ou Frame | Menu principal         |
| Janela Secundária | `tk.Toplevel`    | Formulários, cadastros |
| Diálogo Simples   | `messagebox`     | Mensagens, alertas     |

### Exemplo: Limite de Inserção

```python
# estudante.py

import tkinter as tk
from tkinter import messagebox

class LimiteInsereEstudantes(tk.Toplevel):
    """
    VIEW - Janela para inserir novos estudantes.
    Herda de Toplevel para criar uma janela secundária.
    """

    def __init__(self, controle):
        tk.Toplevel.__init__(self)
        self.geometry('250x100')
        self.title("Estudante")
        self.controle = controle  # Referência ao Controller

        # === CRIAÇÃO DOS FRAMES (containers) ===
        self.frameNro = tk.Frame(self)
        self.frameNome = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameNro.pack()
        self.frameNome.pack()
        self.frameButton.pack()

        # === LABELS ===
        self.labelNro = tk.Label(self.frameNro, text="Nro Matrícula: ")
        self.labelNome = tk.Label(self.frameNome, text="Nome: ")
        self.labelNro.pack(side="left")
        self.labelNome.pack(side="left")

        # === CAMPOS DE ENTRADA ===
        self.inputNro = tk.Entry(self.frameNro, width=20)
        self.inputNro.pack(side="left")
        self.inputNome = tk.Entry(self.frameNome, width=20)
        self.inputNome.pack(side="left")

        # === BOTÕES COM EVENTOS VINCULADOS AO CONTROLE ===
        self.buttonSubmit = tk.Button(self.frameButton, text="Enter")
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.enterHandler)  # Vincula ao Controller

        self.buttonClear = tk.Button(self.frameButton, text="Clear")
        self.buttonClear.pack(side="left")
        self.buttonClear.bind("<Button>", controle.clearHandler)   # Vincula ao Controller

        self.buttonFecha = tk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)   # Vincula ao Controller

    def mostraJanela(self, titulo, msg):
        """Método utilitário para exibir mensagens."""
        messagebox.showinfo(titulo, msg)
```

### Exemplo: Limite de Exibição Simples

```python
# estudante.py

class LimiteMostraEstudantes():
    """
    VIEW - Exibe lista de estudantes em um messagebox.
    Para exibições simples, não precisa de janela completa.
    """

    def __init__(self, str):
        messagebox.showinfo('Lista de alunos', str)
```

### Exemplo: Limite com Combobox e Listbox

```python
# turma.py

class LimiteInsereTurma(tk.Toplevel):
    """
    VIEW - Janela com widgets mais complexos.
    Demonstra uso de Combobox e Listbox.
    """

    def __init__(self, controle, listaCodDiscip, listaNroMatric):
        tk.Toplevel.__init__(self)
        self.geometry('300x250')
        self.title("Turma")
        self.controle = controle

        # ... frames ...

        # === COMBOBOX (lista suspensa) ===
        self.labelDiscip = tk.Label(self.frameDiscip, text="Escolha a disciplina: ")
        self.labelDiscip.pack(side="left")
        self.escolhaCombo = tk.StringVar()
        self.combobox = ttk.Combobox(self.frameDiscip, width=15, textvariable=self.escolhaCombo)
        self.combobox.pack(side="left")
        self.combobox['values'] = listaCodDiscip  # Popula com dados do Controller

        # === LISTBOX (lista de seleção) ===
        self.labelEst = tk.Label(self.frameEstudante, text="Escolha o estudante: ")
        self.labelEst.pack(side="left")
        self.listbox = tk.Listbox(self.frameEstudante)
        self.listbox.pack(side="left")
        for nro in listaNroMatric:
            self.listbox.insert(tk.END, nro)  # Popula a lista

        # === BOTÕES ===
        self.buttonInsere = tk.Button(self.frameButton, text="Insere Aluno")
        self.buttonInsere.pack(side="left")
        self.buttonInsere.bind("<Button>", controle.insereAluno)

        self.buttonCria = tk.Button(self.frameButton, text="Cria Turma")
        self.buttonCria.pack(side="left")
        self.buttonCria.bind("<Button>", controle.criaTurma)
```

---

## Etapa 3: Criando o Controle (Controller)

O **Controle** é o cérebro da aplicação. Ele:

- Mantém a lista de objetos (dados em memória)
- Processa eventos da View
- Atualiza Model e View

### Regras para o Controle:

1. ✅ Mantém coleções de objetos Model
2. ✅ Implementa handlers de eventos
3. ✅ Cria instâncias de Limite quando necessário
4. ✅ Valida dados antes de criar objetos
5. ❌ **NÃO** deve criar widgets diretamente

### Estrutura Padrão de um Controle

```python
class CtrlEntidade():
    def __init__(self):
        self.listaEntidades = []  # Armazena objetos Model

    # Métodos de acesso aos dados
    def getEntidade(self, id): ...
    def getListaIds(self): ...

    # Métodos que abrem janelas
    def insereEntidades(self): ...
    def mostraEntidades(self): ...

    # Handlers de eventos (chamados pela View)
    def enterHandler(self, event): ...
    def clearHandler(self, event): ...
    def fechaHandler(self, event): ...
```

### Exemplo Completo: `CtrlEstudante`

```python
# estudante.py

class CtrlEstudante():
    """
    CONTROLLER - Gerencia a lógica de Estudantes.
    """

    def __init__(self):
        # Inicializa com dados de exemplo
        self.listaEstudantes = [
            Estudante('1001', 'Joao Santos'),
            Estudante('1002', 'Marina Cintra'),
            Estudante('1003', 'Felipe Reis'),
            Estudante('1004', 'Ana Souza')
        ]

    # === MÉTODOS DE ACESSO AOS DADOS ===

    def getEstudante(self, nroMatric):
        """Busca estudante por matrícula."""
        estRet = None
        for est in self.listaEstudantes:
            if est.nroMatric == nroMatric:
                estRet = est
        return estRet

    def getListaNroMatric(self):
        """Retorna lista de matrículas (para preencher Listbox)."""
        listaNro = []
        for est in self.listaEstudantes:
            listaNro.append(est.nroMatric)
        return listaNro

    # === MÉTODOS QUE ABREM JANELAS ===

    def insereEstudantes(self):
        """Abre janela de inserção."""
        self.limiteIns = LimiteInsereEstudantes(self)  # Passa self como referência

    def mostraEstudantes(self):
        """Exibe lista de estudantes."""
        str = 'Nro Matric. -- Nome\n'
        for est in self.listaEstudantes:
            str += est.nroMatric + ' -- ' + est.nome + '\n'
        self.limiteLista = LimiteMostraEstudantes(str)

    # === HANDLERS DE EVENTOS ===

    def enterHandler(self, event):
        """
        Chamado quando o usuário clica em 'Enter'.
        1. Obtém dados da View
        2. Cria objeto Model
        3. Adiciona à lista
        4. Notifica o usuário
        """
        nroMatric = self.limiteIns.inputNro.get()  # Obtém dados da View
        nome = self.limiteIns.inputNome.get()

        estudante = Estudante(nroMatric, nome)     # Cria Model
        self.listaEstudantes.append(estudante)     # Adiciona à lista

        self.limiteIns.mostraJanela('Sucesso', 'Estudante cadastrado com sucesso')
        self.clearHandler(event)                    # Limpa campos

    def clearHandler(self, event):
        """Limpa os campos de entrada."""
        self.limiteIns.inputNro.delete(0, len(self.limiteIns.inputNro.get()))
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))

    def fechaHandler(self, event):
        """Fecha a janela de inserção."""
        self.limiteIns.destroy()
```

---

## Etapa 4: Integrando os Componentes

O arquivo `main.py` é o **ponto de entrada** da aplicação. Ele contém:

- O **Controle Principal** que coordena todos os outros controles
- O **Limite Principal** (menu da aplicação)

### Estrutura do main.py

```python
# main.py

import tkinter as tk
import estudante as est
import disciplina as disc
import turma as trm

class LimitePrincipal():
    """
    VIEW PRINCIPAL - Menu da aplicação.
    """

    def __init__(self, root, controle):
        self.controle = controle
        self.root = root
        self.root.geometry('300x250')

        # Cria barra de menu
        self.menubar = tk.Menu(self.root)

        # Menu Estudante
        self.estudanteMenu = tk.Menu(self.menubar)
        self.estudanteMenu.add_command(label="Insere",
                    command=self.controle.insereEstudantes)
        self.estudanteMenu.add_command(label="Mostra",
                    command=self.controle.mostraEstudantes)
        self.menubar.add_cascade(label="Estudante", menu=self.estudanteMenu)

        # Menu Disciplina
        self.discipMenu = tk.Menu(self.menubar)
        self.discipMenu.add_command(label="Insere",
                    command=self.controle.insereDisciplinas)
        self.discipMenu.add_command(label="Mostra",
                    command=self.controle.mostraDisciplinas)
        self.menubar.add_cascade(label="Disciplina", menu=self.discipMenu)

        # Menu Turma
        self.turmaMenu = tk.Menu(self.menubar)
        self.turmaMenu.add_command(label="Insere",
                    command=self.controle.insereTurmas)
        self.menubar.add_cascade(label="Turma", menu=self.turmaMenu)

        self.root.config(menu=self.menubar)
```

### Controle Principal

```python
# main.py

class ControlePrincipal():
    """
    CONTROLLER PRINCIPAL - Coordena todos os módulos.
    """

    def __init__(self):
        self.root = tk.Tk()

        # Cria os controles de cada módulo
        self.ctrlEstudante = est.CtrlEstudante()
        self.ctrlDisciplina = disc.CtrlDisciplina()
        self.ctrlTurma = trm.CtrlTurma(self)  # Passa referência a si mesmo

        # Cria o limite principal
        self.limite = LimitePrincipal(self.root, self)

        self.root.title("Exemplo MVC")
        self.root.mainloop()  # Inicia o loop de eventos

    # === MÉTODOS DELEGADORES ===
    # Delegam chamadas para os controles específicos

    def insereEstudantes(self):
        self.ctrlEstudante.insereEstudantes()

    def mostraEstudantes(self):
        self.ctrlEstudante.mostraEstudantes()

    def insereDisciplinas(self):
        self.ctrlDisciplina.insereDisciplinas()

    def mostraDisciplinas(self):
        self.ctrlDisciplina.mostraDisciplinas()

    def insereTurmas(self):
        self.ctrlTurma.insereTurmas()


# Ponto de entrada
if __name__ == '__main__':
    c = ControlePrincipal()
```

---

## Etapa 5: Comunicação entre Módulos

Quando um módulo precisa acessar dados de outro, usamos o **Controle Principal** como intermediário.

### Exemplo: Turma precisa de Disciplinas e Estudantes

```python
# turma.py

class CtrlTurma():
    def __init__(self, controlePrincipal):
        self.ctrlPrincipal = controlePrincipal  # Guarda referência
        self.listaTurmas = []

    def insereTurmas(self):
        self.listaAlunosTurma = []

        # Acessa dados de outros módulos via Controle Principal
        listaCodDisc = self.ctrlPrincipal.ctrlDisciplina.getListaCodDisciplinas()
        listaNroMatric = self.ctrlPrincipal.ctrlEstudante.getListaNroMatric()

        # Passa os dados para a View
        self.limiteIns = LimiteInsereTurma(self, listaCodDisc, listaNroMatric)

    def criaTurma(self, event):
        codTurma = self.limiteIns.inputCodTurma.get()
        discSel = self.limiteIns.escolhaCombo.get()

        # Busca objeto Disciplina via Controle Principal
        disc = self.ctrlPrincipal.ctrlDisciplina.getDisciplina(discSel)

        turma = Turma(codTurma, disc, self.listaAlunosTurma)
        self.listaTurmas.append(turma)
        # ...

    def insereAluno(self, event):
        alunoSel = self.limiteIns.listbox.get(tk.ACTIVE)

        # Busca objeto Estudante via Controle Principal
        aluno = self.ctrlPrincipal.ctrlEstudante.getEstudante(alunoSel)

        self.listaAlunosTurma.append(aluno)
        # ...
```

### Diagrama de Comunicação

```
┌────────────────────────────────────────────────────────────────┐
│                     ControlePrincipal                          │
│  ┌──────────────┐ ┌───────────────┐ ┌───────────────┐         │
│  │ctrlEstudante │ │ctrlDisciplina │ │   ctrlTurma   │         │
│  └──────────────┘ └───────────────┘ └───────┬───────┘         │
│                                             │                  │
│                                             │ getListaCodDisciplinas()
│                                             ▼                  │
│                                    ┌───────────────┐           │
│                                    │ctrlDisciplina │           │
│                                    └───────────────┘           │
└────────────────────────────────────────────────────────────────┘
```

---

## Boas Práticas

### ✅ Faça

| Prática                                     | Exemplo                                       |
| ------------------------------------------- | --------------------------------------------- |
| Encapsular atributos                        | `self.__nome` (privado)                       |
| Usar properties                             | `@property def nome(self):`                   |
| Separar arquivos por entidade               | `estudante.py`, `disciplina.py`               |
| Validar dados no Controller                 | Verificar campos vazios antes de criar objeto |
| Usar `tk.Toplevel` para janelas secundárias | Formulários de cadastro                       |

### ❌ Evite

| Anti-padrão                            | Por quê?                              |
| -------------------------------------- | ------------------------------------- |
| Model importando tkinter               | Quebra separação de responsabilidades |
| View processando dados                 | Lógica deve estar no Controller       |
| Acessar atributos privados diretamente | Usar getters/setters                  |
| Criar widgets no Controller            | Deve ser feito na View                |

---

## Resumo Visual

### Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                         USUÁRIO                              │
│                       (clica, digita)                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     LIMITE (View)                            │
│  • Captura eventos                                          │
│  • Exibe dados                                              │
│  • Chama handlers do Controle                               │
└─────────────────────────┬───────────────────────────────────┘
                          │ evento
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONTROLE (Controller)                      │
│  • Processa evento                                          │
│  • Valida dados                                             │
│  • Cria/atualiza objetos Model                              │
│  • Atualiza View                                            │
└─────────────────────────┬───────────────────────────────────┘
                          │ manipula
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      MODEL (Entidade)                        │
│  • Armazena dados                                           │
│  • Define regras de negócio                                 │
└─────────────────────────────────────────────────────────────┘
```

### Checklist para Nova Entidade

1. [ ] Criar classe **Model** com atributos e properties
2. [ ] Criar classe **LimiteInsere** (formulário de cadastro)
3. [ ] Criar classe **LimiteMostra** (exibição de dados)
4. [ ] Criar classe **Ctrl** com:
   - [ ] Lista de objetos
   - [ ] Métodos de acesso (getters)
   - [ ] Métodos que abrem janelas
   - [ ] Handlers de eventos
5. [ ] Adicionar ao **ControlePrincipal**:
   - [ ] Instância do novo Ctrl
   - [ ] Métodos delegadores
6. [ ] Adicionar ao **LimitePrincipal**:
   - [ ] Novo menu com comandos

---

## Conclusão

O padrão MVC permite criar aplicações organizadas, manuteníveis e extensíveis. Seguindo as etapas deste guia, você poderá:

1. **Adicionar novas entidades** facilmente
2. **Modificar a interface** sem afetar a lógica
3. **Testar componentes** isoladamente
4. **Trabalhar em equipe** com responsabilidades claras

> 💡 **Dica Final**: Comece sempre pelo Model, depois crie o Controller com dados de teste, e por último desenvolva a View.
