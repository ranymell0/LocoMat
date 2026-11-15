from contextlib import AbstractContextManager
from typing import Callable

from locomat.historico import HistoricoService
from locomat.materiais.modelo import Conservacao, EstadoMaterial, Material, TipoMaterial
from locomat.materiais.portas import RepositorioMateriais


class MaterialInvalido(ValueError):
    pass


class CodigoDuplicado(MaterialInvalido):
    pass


class MaterialService:
    """Interface oferecida: cadastrar(...) e listar(...) (H01)."""

    def __init__(self, repositorio: RepositorioMateriais, historico: HistoricoService,
                 transacao: Callable[[], AbstractContextManager]):
        self._repo = repositorio
        self._historico = historico
        self._transacao = transacao

    def cadastrar(self, codigo: str, nome: str, tipo: str, conservacao: str,
                  registrado_por: str = "sistema") -> Material:
        codigo, nome = (codigo or "").strip().upper(), (nome or "").strip()
        if not codigo:
            raise MaterialInvalido("Informe o código do material.")
        if not nome:
            raise MaterialInvalido("Informe o nome do material.")
        try:
            tipo_ = TipoMaterial(tipo)
            conservacao_ = Conservacao(conservacao)
        except ValueError as erro:
            raise MaterialInvalido("Tipo ou estado de conservação inválido.") from erro

        # Material e movimento de cadastro são gravados juntos ou não são gravados (C04).
        with self._transacao():
            if self._repo.buscar_por_codigo(codigo) is not None:
                raise CodigoDuplicado(f"Já existe um material com o código {codigo}.")
            material = self._repo.adicionar(Material(codigo, nome, tipo_, conservacao_))
            self._historico.registrar(codigo, "cadastro", registrado_por,
                                      EstadoMaterial.DISPONIVEL.value)
        return material

    def listar(self) -> list[Material]:
        return self._repo.listar()
