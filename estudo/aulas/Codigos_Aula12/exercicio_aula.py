# Definir as exceptions

class UsernameDuplicado(Exception):
    pass

class IdadeMenorQuePermitida(Exception):
    pass

class IdadeInvalida(Exception):
    pass

class EmailInvalido(Exception):
    pass

class User:
    def __init__(self, username, email):
        self.__username = username
        self.__email = email

    def getUsername(self):
        return self.__username

    def getEmail(self):
        return self.__email

if __name__ == "__main__":

    listaExemplo = [
        ("paulo", "paulo@gmail.com", 21),
        ("maria", "maria@gmail.com", 19),
        ("antonio", "antonio@gmail.com", 25),
        ("pedro", "pedro@gmail.com", 15),
        ("marisa", "marisa@", 23),
        ("ana", "ana@gmail.com", -22),
        ("maria", "maria2@gmail.com", 27)
    ]

    cadastro = {}

    #completar
