# Guia Completo de Tkinter com Padrão MVC

## Índice

1. [Introdução ao Tkinter](#introdução-ao-tkinter)
2. [Padrão MVC](#padrão-mvc)
3. [Widgets Principais](#widgets-principais)
4. [Exemplos Práticos](#exemplos-práticos)

---

## Introdução ao Tkinter

Tkinter é a biblioteca padrão do Python para criação de interfaces gráficas (GUI). Ela é multiplataforma e vem instalada por padrão com o Python.

### Estrutura Básica

```python
import tkinter as tk

# Criar janela principal
root = tk.Tk()
root.title("Minha Aplicação")
root.geometry("400x300")

# Iniciar loop principal
root.mainloop()
```

---

## Padrão MVC

O padrão **Model-View-Controller (MVC)** separa a aplicação em três componentes:

| Componente     | Responsabilidade                 |
| -------------- | -------------------------------- |
| **Model**      | Lógica de negócio e dados        |
| **View**       | Interface gráfica (widgets)      |
| **Controller** | Intermediário entre Model e View |

### Diagrama de Fluxo

```
┌─────────┐    ┌────────────┐    ┌───────┐
│  View   │◄───│ Controller │───►│ Model │
│  (GUI)  │───►│  (Lógica)  │◄───│(Dados)│
└─────────┘    └────────────┘    └───────┘
```

---

## Widgets Principais

### 1. Label (Rótulo)

Exibe texto ou imagem estática.

```python
label = tk.Label(parent, text="Olá Mundo!", font=("Arial", 14))
label.pack()
```

**Propriedades principais:**

- `text`: Texto a ser exibido
- `font`: Fonte e tamanho
- `fg` / `bg`: Cor do texto / fundo
- `anchor`: Alinhamento (n, s, e, w, center)

---

### 2. Button (Botão)

Executa uma ação quando clicado.

```python
button = tk.Button(parent, text="Clique Aqui", command=minha_funcao)
button.pack()
```

**Propriedades principais:**

- `text`: Texto do botão
- `command`: Função a ser executada
- `state`: `normal`, `disabled`, `active`
- `width` / `height`: Dimensões

---

### 3. Entry (Campo de Texto)

Campo para entrada de texto em uma linha.

```python
entry = tk.Entry(parent, width=30)
entry.pack()

# Obter valor
valor = entry.get()

# Definir valor
entry.delete(0, tk.END)
entry.insert(0, "Novo texto")
```

**Propriedades principais:**

- `width`: Largura em caracteres
- `show`: Caractere para ocultar (ex: `"*"` para senhas)
- `textvariable`: Variável StringVar vinculada

---

### 4. Text (Área de Texto)

Campo para entrada de texto multilinha.

```python
text = tk.Text(parent, width=40, height=10)
text.pack()

# Obter valor
conteudo = text.get("1.0", tk.END)

# Inserir texto
text.insert(tk.END, "Novo texto\n")
```

---

### 5. Listbox (Lista)

Lista de itens selecionáveis.

```python
listbox = tk.Listbox(parent, selectmode=tk.SINGLE)
listbox.pack()

# Adicionar itens
listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")

# Obter seleção
indice = listbox.curselection()
valor = listbox.get(indice)
```

**Modos de seleção:**

- `tk.SINGLE` - Apenas um item
- `tk.MULTIPLE` - Vários itens com cliques
- `tk.EXTENDED` - Seleção com Shift/Ctrl

**Evento de mudança (onChange):**

```python
def ao_selecionar(event):
    # Obtém índice(s) selecionado(s)
    selecao = listbox.curselection()
    if selecao:
        indice = selecao[0]
        valor = listbox.get(indice)
        print(f"Selecionado: {valor}")

# Vincula o evento de seleção
listbox.bind("<<ListboxSelect>>", ao_selecionar)
```

**Exemplo prático - Filtrar produtos por categoria:**

```python
# View
class ProdutosView:
    def __init__(self, controller):
        self.controller = controller

        # Listbox de categorias
        self.listbox_categorias = tk.Listbox(parent, selectmode=tk.SINGLE)
        self.listbox_categorias.insert(tk.END, "Eletrônicos")
        self.listbox_categorias.insert(tk.END, "Roupas")
        self.listbox_categorias.insert(tk.END, "Alimentos")
        self.listbox_categorias.bind("<<ListboxSelect>>", controller.filtrarPorCategoria)
        self.listbox_categorias.pack()

# Controller
def filtrarPorCategoria(self, event):
    selecao = self.view.listbox_categorias.curselection()
    if selecao:
        categoria = self.view.listbox_categorias.get(selecao[0])
        produtos = [p for p in self.produtos if p.categoria == categoria]
        self.view.atualizarProdutos(produtos)
```

---

### 6. Combobox (Lista Suspensa)

Requer `ttk` (themed tkinter).

```python
from tkinter import ttk

combo = ttk.Combobox(parent, values=["Opção 1", "Opção 2", "Opção 3"])
combo.pack()
combo.set("Selecione...")

# Obter valor selecionado
valor = combo.get()
```

**Propriedades importantes:**

- `state="readonly"` - Impede digitação, apenas seleção
- `state="normal"` - Permite digitar valores customizados
- `values` - Lista de opções disponíveis

**Evento de mudança (onChange):**

```python
def ao_selecionar(event):
    valor_selecionado = combo.get()
    print(f"Você selecionou: {valor_selecionado}")

# Vincula o evento de seleção
combo.bind("<<ComboboxSelected>>", ao_selecionar)
```

**Exemplo prático - Filtrar vinhos por tipo:**

```python
# View
class VinhosView:
    def __init__(self, controller):
        self.controller = controller

        # Combobox de tipos
        self.combo_tipo = ttk.Combobox(
            parent,
            values=["Todos", "Tinto", "Branco", "Rosé", "Espumante"],
            state="readonly"  # Só permite seleção
        )
        self.combo_tipo.set("Todos")
        self.combo_tipo.bind("<<ComboboxSelected>>", controller.filtrarPorTipo)
        self.combo_tipo.pack()

        # Lista de vinhos
        self.lista_vinhos = tk.Listbox(parent)
        self.lista_vinhos.pack()

    def atualizarVinhos(self, vinhos):
        # Limpa a lista
        self.lista_vinhos.delete(0, tk.END)
        # Adiciona vinhos filtrados
        for vinho in vinhos:
            self.lista_vinhos.insert(tk.END, f"{vinho.nome} - R${vinho.preco}")

# Controller
class VinhosController:
    def __init__(self):
        self.vinhos = [...]  # Lista de vinhos

    def filtrarPorTipo(self, event):
        tipo_selecionado = self.view.combo_tipo.get()

        if tipo_selecionado == "Todos":
            vinhos_filtrados = self.vinhos
        else:
            vinhos_filtrados = [v for v in self.vinhos if v.tipo == tipo_selecionado]

        self.view.atualizarVinhos(vinhos_filtrados)
```

**Eventos úteis:**

- `<<ComboboxSelected>>` - Quando usuário seleciona da lista
- `<KeyRelease>` - Quando usuário digita (se state="normal")
- `<FocusOut>` - Quando combo perde o foco

---

### 7. Checkbutton (Caixa de Seleção)

```python
var = tk.BooleanVar()
check = tk.Checkbutton(parent, text="Aceito os termos", variable=var)
check.pack()

# Verificar estado
if var.get():
    print("Marcado!")
```

---

### 8. Radiobutton (Botão de Opção)

```python
var = tk.StringVar(value="opcao1")

radio1 = tk.Radiobutton(parent, text="Opção 1", variable=var, value="opcao1")
radio2 = tk.Radiobutton(parent, text="Opção 2", variable=var, value="opcao2")
radio1.pack()
radio2.pack()

# Obter valor selecionado
print(var.get())
```

---

### 9. Scale (Controle Deslizante)

```python
scale = tk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL)
scale.pack()

# Obter valor
valor = scale.get()
```

---

### 10. Frame (Container)

Agrupa widgets.

```python
frame = tk.Frame(parent, borderwidth=2, relief=tk.GROOVE)
frame.pack(padx=10, pady=10)

# Adicionar widgets ao frame
label = tk.Label(frame, text="Dentro do frame")
label.pack()
```

---

## Gerenciadores de Layout

### Pack

Organiza widgets em blocos.

```python
widget.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
```

### Grid

Organiza em grade (linhas e colunas).

```python
widget.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
```

### Place

Posicionamento absoluto.

```python
widget.place(x=100, y=50, width=200, height=30)
```

---

## Exemplos Práticos

Veja os arquivos de exemplo na pasta:

1. **`exemplo_mvc_calculadora/`** - Calculadora simples com MVC
2. **`exemplo_mvc_lista_tarefas/`** - Lista de tarefas com MVC
3. **`exemplo_widgets_demo.py`** - Demonstração de todos os widgets

---

## Boas Práticas

1. **Separação de responsabilidades**: Use MVC para organizar o código
2. **Use variáveis de controle**: `StringVar`, `IntVar`, `BooleanVar`
3. **Prefira ttk**: Widgets com visual moderno
4. **Evite lógica na View**: Mantenha a View apenas para exibição
5. **Use constantes**: Para configurações de estilo

---

## Referências

- [Documentação Oficial Tkinter](https://docs.python.org/3/library/tkinter.html)
- [TkDocs - Tutorial Moderno](https://tkdocs.com/)
