from flask import Blueprint, flash, redirect, render_template, request, url_for

from locomat.materiais import Conservacao, MaterialInvalido, MaterialService, TipoMaterial


def criar_blueprint(materiais: MaterialService) -> Blueprint:
    bp = Blueprint("web", __name__)

    @bp.get("/")
    def inicio():
        return redirect(url_for("web.listar_materiais"))

    @bp.get("/materiais")
    def listar_materiais():
        return render_template("materiais.html", itens=materiais.listar(), tipos=list(TipoMaterial),
                               conservacoes=list(Conservacao))

    @bp.post("/materiais")
    def cadastrar_material():
        try:
            m = materiais.cadastrar(request.form.get("codigo", ""), request.form.get("nome", ""),
                                    request.form.get("tipo", ""), request.form.get("conservacao", ""))
            flash(f"Material {m.codigo} cadastrado.", "ok")
        except MaterialInvalido as erro:  # inclui CodigoDuplicado
            flash(str(erro), "erro")
        return redirect(url_for("web.listar_materiais"))

    return bp
