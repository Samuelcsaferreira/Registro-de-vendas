from flask import Blueprint, request, render_template, redirect, jsonify
from services.vendasService import VendasService
from datetime import datetime
import json

# Declaração da classe Flask e rota para vendas
vendas_bp = Blueprint("vendas", __name__)


# Rota do blueprint de venas
@vendas_bp.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return listar_vendas()


# Listar todas as vendas na interface do lado do cliente
def listar_vendas():

    dados = VendasService()
    dados.mostrar_registros()
    with open("dados_json.json", "r", encoding="utf-8") as arquivo_json:
        dados.dados = json.load(arquivo_json)

    credito = dados.exibir_soma("Crédito")
    debito = dados.exibir_soma("Débito")
    dinheiro = dados.exibir_soma("Dinheiro")
    pix = dados.exibir_soma("PIX")

    return render_template(
        "vendas.html",
        dados=dados.dados,
        credito=credito,
        debito=debito,
        dinheiro=dinheiro,
        pix=pix,
    )



# Criar um novo registro de vendas
def criar_vendas():
    valor = request.form.get("valor") or request.json["valor"]
    pagamento = request.form.get("pgtform") or request.json["pgtform"]
    data = request.form.get("data-venda") or request.json["dt_registro"]

    if not data:
        data = datetime.now()
    venda = VendasService()
    venda.registrar_venda(valor, pagamento, data)
    return redirect("/")


# Rota para efetuar uma alteração ou deletar um registro já cadastrado
@vendas_bp.route("/vendas/<int:venda_id>", methods=["PUT", "DELETE"])
def atualizar_dados(venda_id):
    if request.method == "DELETE":
        return deletar_venda()

    def deletar_venda():
        venda = VendasService()
        venda.deletar_dado(venda_id)
        return jsonify({"message": "Deletado com sucesso"}), 200



@vendas_bp.route("/vendas", methods=["POST"])
def vendas():
    criar_vendas()
    return jsonify()