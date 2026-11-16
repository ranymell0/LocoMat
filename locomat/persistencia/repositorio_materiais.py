from dataclasses import replace

from locomat.materiais import Conservacao, EstadoMaterial, Material, TipoMaterial
from locomat.persistencia.banco import Banco


def _para_material(linha) -> Material:
    return Material(codigo=linha["codigo"], nome=linha["nome"], tipo=TipoMaterial(linha["tipo"]),
                    conservacao=Conservacao(linha["conservacao"]),
                    estado=EstadoMaterial(linha["estado"]), id=linha["id"])


class RepositorioMateriaisSQL:
    def __init__(self, banco: Banco):
        self._banco = banco

    def adicionar(self, material: Material) -> Material:
        cursor = self._banco.executar(
            "INSERT INTO material (codigo, nome, tipo, conservacao, estado) VALUES (?, ?, ?, ?, ?)",
            (material.codigo, material.nome, material.tipo.value,
             material.conservacao.value, material.estado.value))
        return replace(material, id=cursor.lastrowid)

    def buscar_por_codigo(self, codigo: str) -> Material | None:
        linha = self._banco.executar("SELECT * FROM material WHERE codigo = ?", (codigo,)).fetchone()
        return _para_material(linha) if linha else None

    def listar(self, tipo: TipoMaterial | None = None,
               estado: EstadoMaterial | None = None) -> list[Material]:
        sql, parametros = "SELECT * FROM material WHERE 1=1", []
        if tipo:
            sql += " AND tipo = ?"
            parametros.append(tipo.value)
        if estado:
            sql += " AND estado = ?"
            parametros.append(estado.value)
        sql += " ORDER BY codigo"
        return [_para_material(l) for l in self._banco.executar(sql, tuple(parametros)).fetchall()]
