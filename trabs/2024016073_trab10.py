# Thiago Luiz de Matos - 2024016073

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class ModelMusica():
    def __init__(self, titulo, nroFaixa, artista):
        self.__titulo = titulo
        self.__nroFaixa = nroFaixa
        self.__artista = artista

    @property
    def titulo(self):
        return self.__titulo

    @property
    def nroFaixa(self):
        return self.__nroFaixa

    @property
    def artista(self):
        return self.__artista


class ModelAlbum():
    def __init__(self, titulo, ano, artista):
        self.__titulo = titulo
        self.__ano = ano
        self.__artista = artista
        self.__musicas = []

    @property
    def titulo(self):
        return self.__titulo

    @property
    def ano(self):
        return self.__ano

    @property
    def artista(self):
        return self.__artista

    @property
    def musicas(self):
        return self.__musicas

    def addMusica(self, musica):
        self.__musicas.append(musica)


class ModelArtista():
    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome


class ModelPlaylist():
    def __init__(self, nome):
        self.__nome = nome
        self.__musicas = []

    @property
    def nome(self):
        return self.__nome

    @property
    def musicas(self):
        return self.__musicas

    def addMusica(self, musica):
        self.__musicas.append(musica)


class View():
    def __init__(self, master, controller):
        self.controller = controller
        self.menubar = tk.Menu(master)
        self.artistaMenu = tk.Menu(self.menubar, tearoff=0)
        self.albumMenu = tk.Menu(self.menubar, tearoff=0)
        self.playlistMenu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Artista", menu=self.artistaMenu)
        self.artistaMenu.add_command(
            label="Cadastrar", command=self.controller.cadastraArtista)
        self.artistaMenu.add_command(
            label="Consultar", command=self.controller.consultaArtista)

        self.menubar.add_cascade(label="Álbum", menu=self.albumMenu)
        self.albumMenu.add_command(
            label="Cadastrar", command=self.controller.cadastraAlbum)
        self.albumMenu.add_command(
            label="Consultar", command=self.controller.consultaAlbum)

        self.menubar.add_cascade(label="Playlist", menu=self.playlistMenu)
        self.playlistMenu.add_command(
            label="Cadastrar", command=self.controller.cadastraPlaylist)
        self.playlistMenu.add_command(
            label="Consultar", command=self.controller.consultaPlaylist)

        master.config(menu=self.menubar)

    def mostraJanela(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)


class ViewCadastraPlaylist():
    def __init__(self, controller):
        self.controller = controller
        self.janela = tk.Toplevel(self.controller.root)
        self.janela.geometry('400x400')
        self.janela.title("Cadastrar Playlist")

        self.frameNome = tk.Frame(self.janela)
        self.frameNome.pack()
        self.labelNome = tk.Label(self.frameNome, text="Nome:")
        self.labelNome.pack(side="left")
        self.entryNome = tk.Entry(self.frameNome, width=30)
        self.entryNome.pack(side="left")

        self.frameArtista = tk.Frame(self.janela)
        self.frameArtista.pack()
        self.labelArtista = tk.Label(self.frameArtista, text="Artista:")
        self.labelArtista.pack(side="left")
        self.comboArtista = ttk.Combobox(self.frameArtista, width=30)
        self.comboArtista.pack(side="left")
        self.comboArtista['values'] = [
            artista.nome for artista in self.controller.listaArtistas]
        self.comboArtista.bind("<<ComboboxSelected>>", self.populaMusicas)

        self.frameMusicas = tk.Frame(self.janela)
        self.frameMusicas.pack()
        self.labelMusicasArtista = tk.Label(
            self.frameMusicas, text="Músicas do Artista:")
        self.labelMusicasArtista.pack()
        self.listMusicasArtista = tk.Listbox(self.frameMusicas, width=50)
        self.listMusicasArtista.pack()
        self.listMusicasArtista.bind("<Button-1>", self.addMusica)

        self.labelMusicasPlaylist = tk.Label(
            self.frameMusicas, text="Músicas na Playlist:")
        self.labelMusicasPlaylist.pack()
        self.listMusicasPlaylist = tk.Listbox(self.frameMusicas, width=50)
        self.listMusicasPlaylist.pack()

        self.btnSalva = tk.Button(self.janela, text="Salvar Playlist")
        self.btnSalva.pack()
        self.btnSalva.bind("<Button>", self.salvaPlaylist)

        self.musicasDisponiveis = []
        self.musicasNaPlaylist = []

    def populaMusicas(self, event):
        self.listMusicasArtista.delete(0, tk.END)
        self.musicasDisponiveis.clear()
        nome_artista = self.comboArtista.get()

        artista_obj = None
        for artista in self.controller.listaArtistas:
            if artista.nome == nome_artista:
                artista_obj = artista
                break

        if artista_obj:
            for musica in self.controller.listaMusicas:
                if musica.artista == artista_obj:
                    self.listMusicasArtista.insert(tk.END, musica.titulo)
                    self.musicasDisponiveis.append(musica)

    def addMusica(self, event):
        try:
            idx = self.listMusicasArtista.curselection()[0]
            musica_obj = self.musicasDisponiveis[idx]
            self.musicasNaPlaylist.append(musica_obj)
            self.listMusicasPlaylist.insert(tk.END, musica_obj.titulo)
        except IndexError:
            pass

    def salvaPlaylist(self, event):
        nome = self.entryNome.get()
        if not nome:
            self.controller.view.mostraJanela(
                "Erro", "Nome da playlist é obrigatório")
            return

        playlist = ModelPlaylist(nome)
        for musica in self.musicasNaPlaylist:
            playlist.addMusica(musica)

        self.controller.listaPlaylists.append(playlist)
        self.controller.view.mostraJanela("Sucesso", "Playlist cadastrada")
        self.janela.destroy()


class Controller():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x300')
        self.listaArtistas = []
        self.listaAlbuns = []
        self.listaMusicas = []
        self.listaPlaylists = []
        self.view = View(self.root, self)
        self.root.title("Gestor Musical")
        self.root.mainloop()

    def cadastraArtista(self):
        nome = simpledialog.askstring("Cadastrar Artista", "Nome:")
        if nome:
            artista = ModelArtista(nome)
            self.listaArtistas.append(artista)
            self.view.mostraJanela("Sucesso", "Artista cadastrado com sucesso")

    def consultaArtista(self):
        nome = simpledialog.askstring("Consultar Artista", "Nome:")
        if not nome:
            return

        artista_encontrado = None
        for artista in self.listaArtistas:
            if artista.nome == nome:
                artista_encontrado = artista
                break

        if artista_encontrado:
            output = f"Artista: {artista_encontrado.nome}\n\n"
            output += "Álbuns:\n"
            albuns_do_artista = [
                album for album in self.listaAlbuns if album.artista == artista_encontrado]
            if not albuns_do_artista:
                output += "  (Nenhum álbum cadastrado)\n"
            else:
                for album in albuns_do_artista:
                    output += f"  - {album.titulo} ({album.ano})\n"
                    output += "    Faixas:\n"
                    for musica in album.musicas:
                        output += f"      {musica.nroFaixa}. {musica.titulo}\n"
            self.view.mostraJanela("Consulta Artista", output)

    def cadastraAlbum(self):
        titulo = simpledialog.askstring("Cadastrar Álbum", "Título:")
        if not titulo:
            return
        ano = simpledialog.askinteger("Cadastrar Álbum", "Ano:")
        if not ano:
            return
        nome_artista = simpledialog.askstring(
            "Cadastrar Álbum", "Nome do Artista:")
        if not nome_artista:
            return

        artista_obj = None
        if nome_artista == "Vários artistas":
            artista_obj = ModelArtista("Vários artistas")
        else:
            for artista in self.listaArtistas:
                if artista.nome == nome_artista:
                    artista_obj = artista
                    break

        album = ModelAlbum(titulo, ano, artista_obj)

        while True:
            nroFaixa = simpledialog.askinteger(
                "Adicionar Faixa", f"Álbum: {titulo}\nNúmero da Faixa (ou 0 para parar):")
            if nroFaixa == 0 or nroFaixa is None:
                break
            tituloFaixa = simpledialog.askstring(
                "Adicionar Faixa", "Título da Faixa:")
            if not tituloFaixa:
                continue

            musica = ModelMusica(tituloFaixa, nroFaixa, artista_obj)
            album.addMusica(musica)
            self.listaMusicas.append(musica)

        self.listaAlbuns.append(album)
        self.view.mostraJanela("Sucesso", "Álbum cadastrado com sucesso")

    def consultaAlbum(self):
        titulo = simpledialog.askstring("Consultar Álbum", "Título:")
        if not titulo:
            return

        album_encontrado = None
        for album in self.listaAlbuns:
            if album.titulo == titulo:
                album_encontrado = album
                break

        if album_encontrado:
            output = f"Álbum: {album_encontrado.titulo} ({album_encontrado.ano})\n"
            output += f"Artista: {album_encontrado.artista.nome}\n\n"
            output += "Faixas:\n"
            if not album_encontrado.musicas:
                output += "  (Nenhuma faixa cadastrada)\n"
            else:
                for musica in sorted(album_encontrado.musicas, key=lambda m: m.nroFaixa):
                    output += f"  {musica.nroFaixa}. {musica.titulo}\n"
            self.view.mostraJanela("Consulta Álbum", output)

    def cadastraPlaylist(self):

        self.viewCadPlaylist = ViewCadastraPlaylist(self)

    def consultaPlaylist(self):
        nome = simpledialog.askstring("Consultar Playlist", "Nome:")
        if not nome:
            return

        playlist_encontrada = None
        for playlist in self.listaPlaylists:
            if playlist.nome == nome:
                playlist_encontrada = playlist
                break

        if playlist_encontrada:
            output = f"Playlist: {playlist_encontrada.nome}\n\n"
            output += "Músicas:\n"
            if not playlist_encontrada.musicas:
                output += "  (Nenhuma música na playlist)\n"
            else:
                for musica in playlist_encontrada.musicas:
                    output += f"  - {musica.titulo} ({musica.artista.nome})\n"
            self.view.mostraJanela("Consulta Playlist", output)


if __name__ == '__main__':
    c = Controller()
