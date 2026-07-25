from flask import Blueprint, request, render_template, redirect, jsonify
from app.services.vendasService import VendasService
from datetime import datetime
import json

# Declaração da classe Flask e rota para vendas
vendas_bp = Blueprint("vendas", __name__)


# Rota do blueprint de venas
@vendas_bp.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        vendas = VendasService()
        sales, resumo = vendas.get_sales()
        return jsonify(sales, resumo)

