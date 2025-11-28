"""
Controller - Lista de Tarefas
Responsável por intermediar a comunicação entre Model e View.
"""

from model import ListaTarefasModel
from view import ListaTarefasView


class ListaTarefasController:
    """Controller da lista de tarefas."""

    ARQUIVO_DADOS = "tarefas.json"

    def __init__(self, model: ListaTarefasModel, view: ListaTarefasView):
        self.model = model
        self.view = view

        # Conectar callbacks da View ao Controller
        self.view.on_adicionar = self.adicionar_tarefa
        self.view.on_remover = self.remover_tarefa
        self.view.on_toggle_status = self.toggle_status
        self.view.on_editar = self.editar_tarefa
        self.view.on_filtrar = self.atualizar_lista
        self.view.on_salvar = self.salvar
        self.view.on_carregar = self.carregar

        # Observer: Model notifica Controller sobre mudanças
        self.model.adicionar_observer(self.atualizar_lista)

        # Tentar carregar dados salvos
        self.carregar(silencioso=True)

        # Atualização inicial
        self.atualizar_lista()

    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa."""
        titulo = self.view.get_titulo()
        descricao = self.view.get_descricao()

        if not titulo:
            self.view.mostrar_erro("Erro", "O título é obrigatório!")
            return

        self.model.adicionar_tarefa(titulo, descricao)
        self.view.limpar_entrada()
        self.view.mostrar_info("Sucesso", f"Tarefa '{titulo}' adicionada!")

    def remover_tarefa(self):
        """Remove a tarefa selecionada."""
        tarefa_id = self.view.get_tarefa_selecionada()

        if tarefa_id is None:
            self.view.mostrar_erro(
                "Erro", "Selecione uma tarefa para remover!")
            return

        tarefa = self.model.obter_tarefa(tarefa_id)
        if tarefa and self.view.confirmar("Confirmar", f"Remover a tarefa '{tarefa.titulo}'?"):
            self.model.remover_tarefa(tarefa_id)

    def toggle_status(self):
        """Alterna o status de conclusão da tarefa selecionada."""
        tarefa_id = self.view.get_tarefa_selecionada()

        if tarefa_id is None:
            self.view.mostrar_erro("Erro", "Selecione uma tarefa!")
            return

        tarefa = self.model.obter_tarefa(tarefa_id)
        if tarefa:
            if tarefa.concluida:
                self.model.desmarcar_concluida(tarefa_id)
            else:
                self.model.marcar_concluida(tarefa_id)

    def editar_tarefa(self):
        """Edita a tarefa selecionada."""
        tarefa_id = self.view.get_tarefa_selecionada()

        if tarefa_id is None:
            self.view.mostrar_erro("Erro", "Selecione uma tarefa para editar!")
            return

        tarefa = self.model.obter_tarefa(tarefa_id)
        if tarefa:
            resultado = self.view.mostrar_dialogo_edicao(
                tarefa.titulo, tarefa.descricao)
            if resultado:
                novo_titulo, nova_descricao = resultado
                if not novo_titulo:
                    self.view.mostrar_erro("Erro", "O título é obrigatório!")
                    return
                self.model.atualizar_tarefa(
                    tarefa_id, novo_titulo, nova_descricao)

    def atualizar_lista(self):
        """Atualiza a lista de tarefas na View baseado no filtro."""
        filtro = self.view.get_filtro()

        if filtro == "pendentes":
            tarefas = self.model.filtrar_por_status(concluidas=False)
        elif filtro == "concluidas":
            tarefas = self.model.filtrar_por_status(concluidas=True)
        else:
            tarefas = self.model.tarefas

        self.view.atualizar_lista(tarefas)
        self.view.atualizar_status(self.model.contar_tarefas())

    def salvar(self):
        """Salva as tarefas em arquivo."""
        if self.model.salvar_em_arquivo(self.ARQUIVO_DADOS):
            self.view.mostrar_info("Sucesso", "Tarefas salvas com sucesso!")
        else:
            self.view.mostrar_erro(
                "Erro", "Não foi possível salvar as tarefas.")

    def carregar(self, silencioso: bool = False):
        """Carrega as tarefas de arquivo."""
        sucesso = self.model.carregar_de_arquivo(self.ARQUIVO_DADOS)
        if not silencioso:
            if sucesso:
                self.view.mostrar_info(
                    "Sucesso", "Tarefas carregadas com sucesso!")
            else:
                self.view.mostrar_erro(
                    "Erro", "Não foi possível carregar as tarefas.")
