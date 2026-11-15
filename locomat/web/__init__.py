"""Módulo web.

Segredo: esconde o framework web (Flask) e como as telas são montadas.
Só conversa com os serviços dos módulos de domínio.
"""
from locomat.web.rotas import criar_blueprint

__all__ = ["criar_blueprint"]
