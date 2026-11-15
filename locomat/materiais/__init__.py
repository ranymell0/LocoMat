"""Módulo materiais.

Segredo: esconde como o ciclo de vida do material é controlado (quais estados
existem e quais transições são permitidas, RN03 e RN05).
"""
from locomat.materiais.ciclo import TransicaoInvalida, pode_transitar
from locomat.materiais.modelo import Conservacao, EstadoMaterial, Material, TipoMaterial
from locomat.materiais.portas import RepositorioMateriais
from locomat.materiais.servico import CodigoDuplicado, MaterialInvalido, MaterialService

__all__ = ["Conservacao", "EstadoMaterial", "Material", "TipoMaterial", "RepositorioMateriais",
           "MaterialService", "MaterialInvalido", "CodigoDuplicado",
           "TransicaoInvalida", "pode_transitar"]
