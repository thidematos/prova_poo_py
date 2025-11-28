"""
Model - Lista de Tarefas
Responsável pelos dados e lógica de negócio.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class Tarefa:
    """Representa uma tarefa individual."""
    id: int
    titulo: str
    descricao: str
    concluida: bool
    data_criacao: str
    data_conclusao: Optional[str] = None

    def to_dict(self) -> dict:
        """Converte a tarefa para dicionário."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "concluida": self.concluida,
            "data_criacao": self.data_criacao,
            "data_conclusao": self.data_conclusao
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Tarefa":
        """Cria uma tarefa a partir de um dicionário."""
        return cls(**dados)


class ListaTarefasModel:
    """Model da lista de tarefas."""

    def __init__(self):
        self._tarefas: List[Tarefa] = []
        self._proximo_id = 1
        self._observers = []  # Padrão Observer para notificar mudanças

    def adicionar_observer(self, callback):
        """Adiciona um observer para ser notificado de mudanças."""
        self._observers.append(callback)

    def _notificar_observers(self):
        """Notifica todos os observers sobre mudanças."""
        for callback in self._observers:
            callback()

    @property
    def tarefas(self) -> List[Tarefa]:
        """Retorna a lista de tarefas."""
        return self._tarefas.copy()

    def adicionar_tarefa(self, titulo: str, descricao: str = "") -> Tarefa:
        """Adiciona uma nova tarefa."""
        tarefa = Tarefa(
            id=self._proximo_id,
            titulo=titulo,
            descricao=descricao,
            concluida=False,
            data_criacao=datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        self._tarefas.append(tarefa)
        self._proximo_id += 1
        self._notificar_observers()
        return tarefa

    def remover_tarefa(self, tarefa_id: int) -> bool:
        """Remove uma tarefa pelo ID."""
        for i, tarefa in enumerate(self._tarefas):
            if tarefa.id == tarefa_id:
                del self._tarefas[i]
                self._notificar_observers()
                return True
        return False

    def marcar_concluida(self, tarefa_id: int) -> bool:
        """Marca uma tarefa como concluída."""
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                tarefa.concluida = True
                tarefa.data_conclusao = datetime.now().strftime("%d/%m/%Y %H:%M")
                self._notificar_observers()
                return True
        return False

    def desmarcar_concluida(self, tarefa_id: int) -> bool:
        """Desmarca uma tarefa como concluída."""
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                tarefa.concluida = False
                tarefa.data_conclusao = None
                self._notificar_observers()
                return True
        return False

    def obter_tarefa(self, tarefa_id: int) -> Optional[Tarefa]:
        """Obtém uma tarefa pelo ID."""
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                return tarefa
        return None

    def atualizar_tarefa(self, tarefa_id: int, titulo: str, descricao: str) -> bool:
        """Atualiza o título e descrição de uma tarefa."""
        for tarefa in self._tarefas:
            if tarefa.id == tarefa_id:
                tarefa.titulo = titulo
                tarefa.descricao = descricao
                self._notificar_observers()
                return True
        return False

    def filtrar_por_status(self, concluidas: bool) -> List[Tarefa]:
        """Filtra tarefas por status de conclusão."""
        return [t for t in self._tarefas if t.concluida == concluidas]

    def contar_tarefas(self) -> dict:
        """Retorna contagem de tarefas."""
        total = len(self._tarefas)
        concluidas = len([t for t in self._tarefas if t.concluida])
        return {
            "total": total,
            "concluidas": concluidas,
            "pendentes": total - concluidas
        }

    def salvar_em_arquivo(self, caminho: str) -> bool:
        """Salva as tarefas em um arquivo JSON."""
        try:
            dados = {
                "proximo_id": self._proximo_id,
                "tarefas": [t.to_dict() for t in self._tarefas]
            }
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def carregar_de_arquivo(self, caminho: str) -> bool:
        """Carrega as tarefas de um arquivo JSON."""
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            self._proximo_id = dados.get("proximo_id", 1)
            self._tarefas = [Tarefa.from_dict(t)
                             for t in dados.get("tarefas", [])]
            self._notificar_observers()
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
