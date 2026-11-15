from typing import Protocol

from locomat.historico.modelo import Movimento


class RepositorioHistorico(Protocol):
    def adicionar(self, movimento: Movimento) -> Movimento: ...
