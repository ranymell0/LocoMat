"""Módulo historico.

Segredo: esconde como e onde os movimentos (retirada, devolução, dano...) são
gravados e consultados. Protege o cenário C04 (rastreabilidade).
"""
from locomat.historico.modelo import Movimento
from locomat.historico.portas import RepositorioHistorico
from locomat.historico.servico import HistoricoService

__all__ = ["Movimento", "RepositorioHistorico", "HistoricoService"]
