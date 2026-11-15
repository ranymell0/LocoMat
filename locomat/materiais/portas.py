from typing import Protocol

from locomat.materiais.modelo import Material


class RepositorioMateriais(Protocol):
    def adicionar(self, material: Material) -> Material: ...

    def buscar_por_codigo(self, codigo: str) -> Material | None: ...

    def listar(self) -> list[Material]: ...
