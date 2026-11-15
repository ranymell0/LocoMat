from dataclasses import dataclass
from enum import Enum


class TipoMaterial(str, Enum):
    ESPORTIVO = "esportivo"
    INSTRUMENTO_BATERIA = "instrumento_bateria"


class EstadoMaterial(str, Enum):
    DISPONIVEL = "disponivel"
    EMPRESTADO = "emprestado"
    RESERVADO = "reservado"
    EM_MANUTENCAO = "em_manutencao"


class Conservacao(str, Enum):
    BOM = "bom"
    REGULAR = "regular"
    RUIM = "ruim"


@dataclass
class Material:
    codigo: str
    nome: str
    tipo: TipoMaterial
    conservacao: Conservacao
    estado: EstadoMaterial = EstadoMaterial.DISPONIVEL
    id: int | None = None
