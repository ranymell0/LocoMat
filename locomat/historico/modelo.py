from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Movimento:
    material_codigo: str
    tipo: str  # cadastro, emprestimo, devolucao, reserva, dano, conclusao_manutencao
    registrado_por: str
    estado_resultante: str
    registrado_em: datetime
    responsavel: str | None = None  # quem ficou com o material, quando houver
    id: int | None = None
