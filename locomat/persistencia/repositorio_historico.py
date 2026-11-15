from dataclasses import replace

from locomat.historico import Movimento
from locomat.persistencia.banco import Banco


class RepositorioHistoricoSQL:
    def __init__(self, banco: Banco):
        self._banco = banco

    def adicionar(self, movimento: Movimento) -> Movimento:
        cursor = self._banco.executar(
            "INSERT INTO movimento (material_codigo, tipo, responsavel, registrado_por,"
            " estado_resultante, registrado_em) VALUES (?, ?, ?, ?, ?, ?)",
            (movimento.material_codigo, movimento.tipo, movimento.responsavel,
             movimento.registrado_por, movimento.estado_resultante,
             movimento.registrado_em.isoformat()))
        return replace(movimento, id=cursor.lastrowid)
