from flask import Blueprint, flash, redirect, render_template, request, url_for

from locomat.historico import HistoricoService
from locomat.materiais import (Conservacao, EstadoMaterial, MaterialInvalido, MaterialService,
                               TipoMaterial)


def criar_blueprint(materiais: MaterialService, historico: HistoricoService) -> Blueprint:
    bp = Blueprint("web", __name__)

    @bp.get("/")
    def inicio():
        return redirect(url_for("web.listar_materiais"))

    @bp.get("/materiais")
    def listar_materiais():
        tipo, estado = request.args.get("tipo") or None, request.args.get("estado") or None
        try:
            itens = materiais.listar(tipo, estado)
        except ValueError:
            itens = []
            flash("Filtro inválido.", "erro")
        return render_template("materiais.html", itens=itens, tipos=list(TipoMaterial),
                               estados=list(EstadoMaterial), conservacoes=list(Conservacao),
                               filtro_tipo=tipo, filtro_estado=estado)

    @bp.post("/materiais")
    def cadastrar_material():
        try:
            m = materiais.cadastrar(request.form.get("codigo", ""), request.form.get("nome", ""),
                                    request.form.get("tipo", ""), request.form.get("conservacao", ""))
            flash(f"Material {m.codigo} cadastrado.", "ok")
        except MaterialInvalido as erro:  # inclui CodigoDuplicado
            flash(str(erro), "erro")
        return redirect(url_for("web.listar_materiais"))

    @bp.get("/materiais/<codigo>/historico")
    def ver_historico(codigo: str):
        return render_template("historico.html", codigo=codigo, movimentos=historico.listar(codigo))

    return bp
