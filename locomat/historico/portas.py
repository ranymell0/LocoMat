from typing import Protocol

from locomat.historico.modelo import Movimento


class RepositorioHistorico(Protocol):
    def adicionar(self, movimento: Movimento) -> Movimento: ...

    def listar_por_material(self, material_codigo: str) -> list[Movimento]: ...
