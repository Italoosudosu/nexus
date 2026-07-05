"""
NEXUM — routes/clientes.py
Rotas de Clientes: páginas (listagem, cadastro, edição) e API REST.
Nenhuma regra de negócio aqui — tudo delega para services/clientes_service.py.
"""

from flask import Blueprint, jsonify, render_template, request

from services import clientes_service as service
from services.clientes_service import ConflictError, NotFoundError, ValidationError

clientes_bp = Blueprint("clientes", __name__)


# ----------------------------------------------------------------------------
# Páginas (Server-Side Rendering via Jinja2)
# ----------------------------------------------------------------------------

@clientes_bp.route("/clientes")
def lista():
    clientes = service.listar_clientes()
    return render_template("clientes/lista.html", clientes=clientes)


@clientes_bp.route("/clientes/novo")
def novo():
    return render_template("clientes/form.html", cliente=None, modo="criar")


@clientes_bp.route("/clientes/<int:cliente_id>/editar")
def editar(cliente_id):
    try:
        cliente = service.obter_cliente(cliente_id)
    except NotFoundError:
        return render_template("erro_404.html"), 404
    return render_template("clientes/form.html", cliente=cliente.to_dict(), modo="editar")


# ----------------------------------------------------------------------------
# API REST — /api/clientes
# ----------------------------------------------------------------------------

@clientes_bp.route("/api/clientes", methods=["GET"])
def api_listar():
    busca = request.args.get("busca")
    return jsonify(service.listar_clientes(busca=busca))


@clientes_bp.route("/api/clientes/<int:cliente_id>", methods=["GET"])
def api_obter(cliente_id):
    try:
        cliente = service.obter_cliente(cliente_id)
    except NotFoundError as err:
        return jsonify({"mensagem": str(err)}), 404
    return jsonify(cliente.to_dict())


@clientes_bp.route("/api/clientes", methods=["POST"])
def api_criar():
    dados = request.get_json(silent=True) or {}
    try:
        cliente = service.criar_cliente(dados)
    except ValidationError as err:
        return jsonify({"mensagem": err.mensagem, "campo": err.campo}), 400
    except ConflictError as err:
        return jsonify({"mensagem": str(err)}), 409
    return jsonify(cliente.to_dict()), 201


@clientes_bp.route("/api/clientes/<int:cliente_id>", methods=["PUT"])
def api_atualizar(cliente_id):
    dados = request.get_json(silent=True) or {}
    try:
        cliente = service.atualizar_cliente(cliente_id, dados)
    except NotFoundError as err:
        return jsonify({"mensagem": str(err)}), 404
    except ValidationError as err:
        return jsonify({"mensagem": err.mensagem, "campo": err.campo}), 400
    except ConflictError as err:
        return jsonify({"mensagem": str(err)}), 409
    return jsonify(cliente.to_dict())


@clientes_bp.route("/api/clientes/<int:cliente_id>", methods=["DELETE"])
def api_excluir(cliente_id):
    try:
        service.excluir_cliente(cliente_id)
    except NotFoundError as err:
        return jsonify({"mensagem": str(err)}), 404
    return "", 204
