from datetime import datetime, timezone
from typing import Callable

from locomat.historico.modelo import Movimento
from locomat.historico.portas import RepositorioHistorico


class HistoricoService:
    """Interface oferecida: registrar(...) e listar(...). Só acrescenta; nunca altera nem apaga."""

    def __init__(self, repositorio: RepositorioHistorico,
                 relogio: Callable[[], datetime] = lambda: datetime.now(timezone.utc)):
        self._repo = repositorio
        self._relogio = relogio

    def registrar(self, material_codigo: str, tipo: str, registrado_por: str,
                  estado_resultante: str, responsavel: str | None = None) -> Movimento:
        movimento = Movimento(material_codigo=material_codigo, tipo=tipo,
                              registrado_por=registrado_por,
                              estado_resultante=estado_resultante,
                              registrado_em=self._relogio(), responsavel=responsavel)
        return self._repo.adicionar(movimento)
