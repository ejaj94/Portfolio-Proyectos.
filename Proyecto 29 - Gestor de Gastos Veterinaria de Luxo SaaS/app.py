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

# Initial Financial Mock Database for Luxury Veterinary Clinic
transacoes_db = [
    {
        "id": "TRX-7001",
        "tipo": "Receita",       # Receita / Despesa
        "descricao": "Cirurgia de Reconstrução Ortopédica VIP",
        "categoria": "Cirurgia & Especialidades",
        "montante": 3850.00,
        "data": "2026-09-02",
        "metodo": "Cartão de Crédito Executive",
        "notas": "Paciente: Caniche Toy 'Bella' (Família Vasconcelos)"
    },
    {
        "id": "TRX-7002",
        "tipo": "Despesa",
        "descricao": "Lote de Fórmulas & Anestésicos Importados (Suíça)",
        "categoria": "Farmácia & Medicamentos",
        "montante": 1250.00,
        "data": "2026-09-02",
        "metodo": "Transferência Bancária",
        "notas": "Fornecedor: SwissVet Pharma Direct"
    },
    {
        "id": "TRX-7003",
        "tipo": "Receita",
        "descricao": "Tratamento de Hidroterapia & Spa Grooming Deluxe",
        "categoria": "Spa & Estética Canina",
        "montante": 450.00,
        "data": "2026-09-03",
        "metodo": "MB WAY",
        "notas": "Paciente: Pastor Alemão 'Max' (Quinta do Lago)"
    },
    {
        "id": "TRX-7004",
        "tipo": "Despesa",
        "descricao": "Manutenção Preventiva Equipamento Laser & Ultrassom",
        "categoria": "Equipamento Clínico",
        "montante": 980.00,
        "data": "2026-09-03",
        "metodo": "Cartão Empresarial",
        "notas": "Assistência Técnica Autorizada TechVet"
    },
    {
        "id": "TRX-7005",
        "tipo": "Receita",
        "descricao": "Plano Anual de Saúde Holística & Suplementação",
        "categoria": "Consultas & Nutrição",
        "montante": 1890.00,
        "data": "2026-09-03",
        "metodo": "Transferência Bancária",
        "notas": "Assinatura Anual VIP Gold"
    }
]

graficos_dados = {
    "meses": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set"],
    "receitas": [42000, 48000, 51000, 58000, 64000, 69000, 75000, 82000, 88500],
    "despesas": [18000, 19500, 21000, 23000, 24500, 26000, 27500, 29000, 31200],
    "categorias_despesas": {
        "labels": ["Farmácia & Medicamentos", "Equipamento Clínico", "Salários Médicos", "Nutrição Premium", "Instalações & Spa"],
        "valores": [35, 25, 20, 12, 8]  # Percentagens
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/transacoes", methods=["GET"])
def get_transacoes():
    return jsonify(transacoes_db)

@app.route("/api/transacoes/criar", methods=["POST"])
def criar_transacao():
    data = request.json or {}
    new_id = f"TRX-{7000 + len(transacoes_db) + 1}"
    
    nova_trx = {
        "id": new_id,
        "tipo": data.get("tipo", "Receita"),
        "descricao": data.get("descricao", "Serviço Veterinário VIP"),
        "categoria": data.get("categoria", "Consultas & Nutrição"),
        "montante": float(data.get("montante", 100.0)),
        "data": datetime.now().strftime("%Y-%m-%d"),
        "metodo": data.get("metodo", "Cartão de Crédito"),
        "notas": data.get("notas", "Registo Financeiro")
    }
    
    transacoes_db.insert(0, nova_trx)
    return jsonify({"success": True, "transacao": nova_trx})

@app.route("/api/graficos", methods=["GET"])
def get_graficos():
    return jsonify(graficos_dados)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_ingresos = sum(t["montante"] for t in transacoes_db if t["tipo"] == "Receita")
    total_gastos = sum(t["montante"] for t in transacoes_db if t["tipo"] == "Despesa")
    balance_liquido = total_ingresos - total_gastos
    margem = round((balance_liquido / total_ingresos * 100) if total_ingresos > 0 else 0, 1)
    
    return jsonify({
        "total_ingresos": f"{total_ingresos:,.2f} €".replace(",", " ").replace(".", ","),
        "total_gastos": f"{total_gastos:,.2f} €".replace(",", " ").replace(".", ","),
        "balance_liquido": f"{balance_liquido:,.2f} €".replace(",", " ").replace(".", ","),
        "margem_operacional": f"{margem}%",
        "total_transacoes": len(transacoes_db)
    })

if __name__ == "__main__":
    print("Iniciando GESTOR DE GASTOS VETERINÁRIA DE LUXO SAAS em http://localhost:5400")
    app.run(host="0.0.0.0", port=5400, debug=False)
