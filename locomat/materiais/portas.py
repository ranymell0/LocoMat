from typing import Protocol

from locomat.materiais.modelo import EstadoMaterial, Material, TipoMaterial


class RepositorioMateriais(Protocol):
    def adicionar(self, material: Material) -> Material: ...

    def buscar_por_codigo(self, codigo: str) -> Material | None: ...

    def listar(self, tipo: TipoMaterial | None = None,
               estado: EstadoMaterial | None = None) -> list[Material]: ...
