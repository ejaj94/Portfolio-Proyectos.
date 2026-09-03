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

# Enterprise Auto Parts Catalog Mock Database (AUTODOC Inventory)
produtos_db = [
    {
        "sku": "PAR-9001",
        "oem": "OEM-13717597586",
        "nome": "Filtro de Ar de Alta Performance",
        "categoria": "Filtros & Motor",
        "compatibilidade": "BMW Série 3 (F30) / Série 5 (F10)",
        "marca": "BOSCH",
        "stock": 42,
        "stock_min": 15,
        "preco_custo": 12.50,
        "preco_venda": 28.90,
        "localizacao": "Corredor A-04-02",
        "estado": "OK"
    },
    {
        "sku": "PAR-9002",
        "oem": "OEM-1K0698151",
        "nome": "Jogo de Pastilhas de Travão Dianteiras",
        "categoria": "Sistema de Travões",
        "compatibilidade": "VW Golf VII / Audi A3 (8V) / Seat Leon",
        "marca": "BREMBO",
        "stock": 6,
        "stock_min": 10,
        "preco_custo": 24.00,
        "preco_venda": 54.90,
        "localizacao": "Corredor B-12-01",
        "estado": "Alerta Crítico"
    },
    {
        "sku": "PAR-9003",
        "oem": "OEM-51717065919",
        "nome": "Amortecedor de Suspensão a Gás",
        "categoria": "Suspensão & Direção",
        "compatibilidade": "BMW X5 (E70) / X6 (E71)",
        "marca": "SACHS",
        "stock": 18,
        "stock_min": 8,
        "preco_custo": 75.00,
        "preco_venda": 169.00,
        "localizacao": "Corredor C-02-04",
        "estado": "OK"
    },
    {
        "sku": "PAR-9004",
        "oem": "OEM-03L903023",
        "nome": "Alternador Trifásico 140A",
        "categoria": "Sistema Elétrico",
        "compatibilidade": "VW Passat (3C) / Skoda Octavia II",
        "marca": "VALEO",
        "stock": 0,
        "stock_min": 5,
        "preco_custo": 110.00,
        "preco_venda": 245.00,
        "localizacao": "Corredor D-01-03",
        "estado": "Fora de Stock"
    },
    {
        "sku": "PAR-9005",
        "oem": "OEM-63117419630",
        "nome": "Farol Principal Full LED (Esquerdo)",
        "categoria": "Iluminação",
        "compatibilidade": "BMW Série 4 (F32/F36)",
        "marca": "HELLA",
        "stock": 8,
        "stock_min": 4,
        "preco_custo": 280.00,
        "preco_venda": 590.00,
        "localizacao": "Corredor A-08-01",
        "estado": "OK"
    },
    {
        "sku": "PAR-9006",
        "oem": "OEM-11287628652",
        "nome": "Kit de Correia de Distribuição + Bomba de Água",
        "categoria": "Filtros & Motor",
        "compatibilidade": "Peugeot 308 II / Citroën C4 Picasso 2.0 HDi",
        "marca": "SKF",
        "stock": 4,
        "stock_min": 8,
        "preco_custo": 85.00,
        "preco_venda": 189.00,
        "localizacao": "Corredor B-06-03",
        "estado": "Alerta Crítico"
    }
]

movimentos_db = [
    {
        "id": "MOV-8001",
        "sku": "PAR-9001",
        "nome": "Filtro de Ar de Alta Performance",
        "tipo": "Entrada",
        "quantidade": 20,
        "motivo": "Recebimento de Fornecedor (BOSCH Direct)",
        "operador": "Armazém Almancil",
        "data": "2026-09-03 08:30"
    },
    {
        "id": "MOV-8002",
        "sku": "PAR-9002",
        "nome": "Jogo de Pastilhas de Travão Dianteiras",
        "tipo": "Saída",
        "quantidade": 4,
        "motivo": "Expedição de Encomenda #ENC-5541",
        "operador": "Expedição AutoDoc",
        "data": "2026-09-03 09:15"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/produtos", methods=["GET", "POST"])
def handle_produtos():
    if request.method == "POST":
        data = request.json or {}
        new_sku = f"PAR-{9000 + len(produtos_db) + 1}"
        stock_val = int(data.get("stock", 10))
        stock_min_val = int(data.get("stock_min", 5))
        
        estado = "OK"
        if stock_val == 0:
            estado = "Fora de Stock"
        elif stock_val < stock_min_val:
            estado = "Alerta Crítico"
            
        new_prod = {
            "sku": new_sku,
            "oem": data.get("oem", "OEM-00000000"),
            "nome": data.get("nome", "Peça Automóvel"),
            "categoria": data.get("categoria", "Filtros & Motor"),
            "compatibilidade": data.get("compatibilidade", "Universal"),
            "marca": data.get("marca", "AUTODOC Select"),
            "stock": stock_val,
            "stock_min": stock_min_val,
            "preco_custo": float(data.get("preco_custo", 20.0)),
            "preco_venda": float(data.get("preco_venda", 45.0)),
            "localizacao": data.get("localizacao", "Corredor A-01-01"),
            "estado": estado
        }
        produtos_db.insert(0, new_prod)
        return jsonify({"success": True, "produto": new_prod})
        
    return jsonify(produtos_db)

@app.route("/api/produtos/movimento", methods=["POST"])
def registar_movimento():
    data = request.json or {}
    sku = data.get("sku")
    tipo = data.get("tipo")  # Entrada ou Saída
    qtd = int(data.get("quantidade", 1))
    motivo = data.get("motivo", "Ajuste de Stock")
    
    prod = next((p for p in produtos_db if p["sku"] == sku), None)
    if not prod:
        return jsonify({"success": False, "message": "Peça não encontrada"}), 404
        
    if tipo == "Entrada":
        prod["stock"] += qtd
    elif tipo == "Saída":
        if prod["stock"] < qtd:
            return jsonify({"success": False, "message": "Stock insuficiente para expedição"}), 400
        prod["stock"] -= qtd
        
    # Recalculate status
    if prod["stock"] == 0:
        prod["estado"] = "Fora de Stock"
    elif prod["stock"] < prod["stock_min"]:
        prod["estado"] = "Alerta Crítico"
    else:
        prod["estado"] = "OK"
        
    new_mov = {
        "id": f"MOV-{8000 + len(movimentos_db) + 1}",
        "sku": prod["sku"],
        "nome": prod["nome"],
        "tipo": tipo,
        "quantidade": qtd,
        "motivo": motivo,
        "operador": "Operador Sistema",
        "data": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    movimentos_db.insert(0, new_mov)
    
    return jsonify({"success": True, "produto": prod, "movimento": new_mov})

@app.route("/api/movimentos", methods=["GET"])
def get_movimentos():
    return jsonify(movimentos_db)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_pecas = len(produtos_db)
    valor_stock = sum(p["stock"] * p["preco_venda"] for p in produtos_db)
    alertas_criticos = sum(1 for p in produtos_db if p["estado"] in ["Alerta Crítico", "Fora de Stock"])
    total_movimentos = len(movimentos_db)
    
    return jsonify({
        "total_pecas": total_pecas,
        "valor_stock": f"{valor_stock:,.2f} €".replace(",", " ").replace(".", ","),
        "alertas_criticos": alertas_criticos,
        "movimentos_hoje": total_movimentos
    })

if __name__ == "__main__":
    print("Iniciando SISTEMA DE INVENTÁRIO ENTERPRISE PEÇAS AUTO em http://localhost:5250")
    app.run(host="0.0.0.0", port=5250, debug=False)
