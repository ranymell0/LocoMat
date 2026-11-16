from dataclasses import replace
from datetime import datetime

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

    def listar_por_material(self, material_codigo: str) -> list[Movimento]:
        linhas = self._banco.executar(
            "SELECT * FROM movimento WHERE material_codigo = ? ORDER BY id", (material_codigo,)
        ).fetchall()
        return [Movimento(material_codigo=l["material_codigo"], tipo=l["tipo"],
                          responsavel=l["responsavel"], registrado_por=l["registrado_por"],
                          estado_resultante=l["estado_resultante"],
                          registrado_em=datetime.fromisoformat(l["registrado_em"]), id=l["id"])
                for l in linhas]
