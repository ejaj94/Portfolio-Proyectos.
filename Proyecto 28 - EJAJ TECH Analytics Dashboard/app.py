import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Strict anti-cache headers
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Initial Mock Financial & Analytics Database for EJAJ TECH
analytics_db = {
    "faturacao_total": 348500.00,
    "mrr": 28400.00,
    "arr": 340800.00,
    "lucro_liquido": 243950.00,
    "margem_operacional": "70.0%",
    "clientes_ativos": 48,
    "taxa_retencao": "95.8%",
    "projetos_concluidos": 124,
    "comparativa_yoy": "+34.2%",
    "comparativa_mom": "+14.8%"
}

projetos_recentes_db = [
    {"id": "PRJ-901", "nome": "Marina Resort & Spa Hotel SaaS", "categoria": "Web Development", "cliente": "Marina Albufeira Group", "valor": 38500, "estado": "Entregue", "progresso": 100},
    {"id": "PRJ-902", "nome": "Veloce Motors Telemetry App", "categoria": "Apps Development", "cliente": "Veloce Motors", "valor": 45000, "estado": "Em Desenvolvimento", "progresso": 85},
    {"id": "PRJ-903", "nome": "EJAJ Billing & Certified Invoicing", "categoria": "Software Solutions", "cliente": "EJAJ Enterprise", "valor": 28000, "estado": "Entregue", "progresso": 100},
    {"id": "PRJ-904", "nome": "Algarve Health & Aesthetics Portal", "categoria": "Web Development", "cliente": "Quinta do Lago Clinic", "valor": 22000, "estado": "Em Testes QA", "progresso": 92},
    {"id": "PRJ-905", "nome": "AutoParts Industrial Inventory System", "categoria": "Software Solutions", "cliente": "AUTODOC Logistics", "valor": 62000, "estado": "Entregue", "progresso": 100}
]

graficos_dados = {
    "meses": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set"],
    "receita": [28000, 32000, 31000, 39000, 42000, 48000, 51000, 54000, 62000],
    "custos": [9000, 10500, 10000, 12000, 13000, 14500, 15000, 16000, 17500],
    "unidades_negocio": {
        "labels": ["Web Development", "Apps Development", "Software Solutions"],
        "valores": [42, 33, 25]  # Percentagens
    },
    "leads_vs_projetos": {
        "leads": [14, 18, 22, 26, 30, 34, 38, 42, 45],
        "projetos": [8, 11, 14, 17, 21, 25, 29, 32, 36]
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    return jsonify(analytics_db)

@app.route("/api/graficos", methods=["GET"])
def get_graficos():
    return jsonify(graficos_dados)

@app.route("/api/projetos", methods=["GET"])
def get_projetos():
    return jsonify(projetos_recentes_db)

if __name__ == "__main__":
    print("Iniciando EJAJ TECH ANALYTICS DASHBOARD em http://localhost:5350")
    app.run(host="0.0.0.0", port=5350, debug=False)
