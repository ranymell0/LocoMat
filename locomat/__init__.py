"""LocoMat: controle de empréstimo, reserva e manutenção de materiais da Atlética Loucomotiva.

Este arquivo é a raiz de composição: o único lugar que conhece, ao mesmo tempo,
a interface web, os módulos de domínio e a persistência concreta.
"""
import os

from flask import Flask


def create_app(caminho_banco: str | None = None) -> Flask:
    app = Flask(__name__, template_folder="web/templates")
    app.config["SECRET_KEY"] = os.environ.get("LOCOMAT_SECRET", "dev-apenas-para-desenvolvimento")
    return app
