"""
Guia rápido de sintaxe básica do Python focado em construções úteis para POO.

Execute este arquivo diretamente para visualizar exemplos em funcionamento.
"""


# ================== Tipos básicos e variáveis ==================
inteiro = 42
flutuante = 3.14
texto = "Olá, Python!"
booleano = True
tupla = ("Ana", 29)

print(
    f"Tipos primitivos: {inteiro}, {flutuante}, {texto}, {booleano}, {tupla}")


# ================== Listas (arrays) e métodos ==================
linguagens = ["Python", "Java", "C#"]
linguagens.append("Go")  # Adiciona ao final
linguagens.extend(["Rust", "Kotlin"])  # Concatena outra sequência
linguagens.insert(1, "JavaScript")  # Insere em posição específica
linguagens.remove("C#")  # Remove primeira ocorrência do item

ultimo = linguagens.pop()  # Remove e retorna o último elemento
linguagens.sort()  # Ordena in place
linguagens_reversa = list(reversed(linguagens))  # Cria nova lista invertida

print(
    f"Listas em ação: {linguagens} | Último removido: {ultimo} | Reversa: {linguagens_reversa}")

# List comprehension gera listas a partir de iteráveis com sintaxe concisa
tamanhos = [len(nome) for nome in linguagens]
print(f"Tamanhos dos nomes: {tamanhos}")


# ================== Dicionários e métodos ==================
usuario = {"nome": "Ana", "cargo": "Dev", "ativo": True}
usuario["linguagens"] = linguagens  # Adiciona nova chave

usuario_atualizado = {"cargo": "Dev Sênior", "projetos": 3}

# Atualiza chaves/valores existentes e adiciona novos
usuario.update(usuario_atualizado)
chaves = list(usuario.keys())
valores = list(usuario.values())
itens = list(usuario.items())

print(f"Dicionário completo: {usuario}")
print(f"Chaves: {chaves}")
print(f"Valores: {valores}")
print(f"Itens: {itens}")
print(f"Acesso seguro com get: {usuario.get('cidade', 'Desconhecida')}")


# ================== Conjuntos (sets) ==================
conjunto_a = {"Python", "Java", "Go"}
conjunto_b = {"Python", "Rust", "C++"}

print(f"União: {conjunto_a | conjunto_b}")
print(f"Interseção: {conjunto_a & conjunto_b}")
print(f"Diferença: {conjunto_a - conjunto_b}")


# ================== Estruturas condicionais ==================
idade = 20

if idade < 18:
    status = "Menor de idade"
elif idade < 65:
    status = "Adulto"
else:
    status = "Idoso"

print(f"Status por idade ({idade}): {status}")

mensagem = "Pode dirigir" if idade >= 18 else "Não pode dirigir"
print(f"Operador ternário: {mensagem}")


# ================== Loops e controle de fluxo ==================
nomes = ["Ana", "Bruno", "Carla"]

for indice, nome in enumerate(nomes):
    print(f"for com enumerate -> {indice}: {nome}")

contador = 0
while contador < 3:
    print(f"while em execução: contador = {contador}")
    contador += 1
else:
    print("Bloco else executa quando o while termina sem break.")

for numero in range(5):
    if numero == 2:
        continue  # Pula para a próxima iteração
    if numero == 4:
        break  # Interrompe o loop
    print(f"Controle de fluxo em for: {numero}")


# ================== Funções ==================
def saudacao(nome: str, saudacao_inicial: str = "Olá") -> str:
    """Função com parâmetro padrão e anotação de tipo."""
    return f"{saudacao_inicial}, {nome}!"


def somar(*numeros: float) -> float:
    """Aceita quantidade variável de argumentos."""
    return sum(numeros)


def montar_usuario(**campos: str) -> dict[str, str]:
    """Recebe parâmetros nomeados variáveis e retorna dicionário."""
    return dict(campos)


print(saudacao("Clara"))
print(somar(1, 2, 3, 4.5))
print(montar_usuario(nome="Diego", cargo="Arquiteto"))


# ================== Iterators e diferentes formas de iterar ==================
projetos = ["API", "Web", "Mobile"]
duracoes_meses = [3, 4, 2]

print("Iteração direta com for:")
for projeto in projetos:
    print(f" - {projeto}")

print("Iteração com enumerate (índice e valor):")
for indice, projeto in enumerate(projetos, start=1):
    print(f" {indice}. {projeto}")

print("Iteração por índice com range:")
for indice in range(len(projetos)):
    print(f" Índice {indice} -> {projetos[indice]}")

print("Iteração paralela com zip:")
for projeto, duracao in zip(projetos, duracoes_meses):
    print(f" {projeto} dura {duracao} meses")
