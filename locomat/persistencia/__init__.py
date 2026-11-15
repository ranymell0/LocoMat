"""Módulo persistencia.

Segredo: esconde qual banco de dados é usado (SQLite no esqueleto, PostgreSQL em produção)
e como as tabelas são organizadas. Implementa as portas definidas pelos módulos de domínio.
"""
from locomat.persistencia.banco import Banco
from locomat.persistencia.repositorio_historico import RepositorioHistoricoSQL
from locomat.persistencia.repositorio_materiais import RepositorioMateriaisSQL

__all__ = ["Banco", "RepositorioHistoricoSQL", "RepositorioMateriaisSQL"]
