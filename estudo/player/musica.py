class Musica:
    def __init__(self, titulo, nroFaixa):
        self.__titulo = titulo
        self.__nroFaixa = nroFaixa

    @property
    def titulo(self):
        return self.__titulo

    @property
    def nroFaixa(self):
        return self.__nroFaixa
