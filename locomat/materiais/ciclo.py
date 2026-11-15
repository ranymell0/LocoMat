"""Ciclo do material (RN03): disponível, emprestado, reservado, em manutenção."""
from locomat.materiais.modelo import EstadoMaterial as E

_TRANSICOES: dict[E, set[E]] = {
    E.DISPONIVEL: {E.EMPRESTADO, E.RESERVADO, E.EM_MANUTENCAO},
    E.RESERVADO: {E.EMPRESTADO, E.DISPONIVEL, E.EM_MANUTENCAO},
    E.EMPRESTADO: {E.DISPONIVEL, E.EM_MANUTENCAO},
    E.EM_MANUTENCAO: {E.DISPONIVEL},  # RN05: só sai da manutenção quando o reparo termina
}


class TransicaoInvalida(Exception):
    pass


def pode_transitar(origem: E, destino: E) -> bool:
    return destino in _TRANSICOES[origem]
