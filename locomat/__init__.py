"""LocoMat: controle de empréstimo, reserva e manutenção de materiais da Atlética Loucomotiva.

Este arquivo é a raiz de composição: o único lugar que conhece, ao mesmo tempo,
a interface web, os módulos de domínio e a persistência concreta.
"""
import os

from flask import Flask

from locomat.historico import HistoricoService
from locomat.materiais import MaterialService
from locomat.persistencia import Banco, RepositorioHistoricoSQL, RepositorioMateriaisSQL
from locomat.web import criar_blueprint


def create_app(caminho_banco: str | None = None) -> Flask:
    caminho = caminho_banco or os.environ.get("LOCOMAT_DB", "locomat.db")
    banco = Banco(caminho)
    banco.criar_esquema()

    historico = HistoricoService(RepositorioHistoricoSQL(banco))
    materiais = MaterialService(RepositorioMateriaisSQL(banco), historico, banco.transacao)

    app = Flask(__name__, template_folder="web/templates")
    app.config["SECRET_KEY"] = os.environ.get("LOCOMAT_SECRET", "dev-apenas-para-desenvolvimento")
    app.register_blueprint(criar_blueprint(materiais))
    app.extensions["locomat_banco"] = banco
    return app
