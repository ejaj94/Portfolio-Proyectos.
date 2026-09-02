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

# Initial mock database for SaaS Software demonstration
reservas_db = [
    {
        "id": "RES-1001",
        "cliente": "Guilherme Siqueira",
        "email": "guilherme@domain.pt",
        "telefone": "+351 912 345 678",
        "servico": "Consultoria de Software SaaS",
        "data": "2026-09-03",
        "hora": "10:00",
        "duracao": "60 min",
        "estado": "Confirmada",
        "preco": "150 €"
    },
    {
        "id": "RES-1002",
        "cliente": "Sofia Carvalhal",
        "email": "sofia.c@domain.pt",
        "telefone": "+351 965 432 109",
        "servico": "Sessão de Diagnóstico Clínico",
        "data": "2026-09-03",
        "hora": "11:30",
        "duracao": "45 min",
        "estado": "Pendente",
        "preco": "95 €"
    },
    {
        "id": "RES-1003",
        "cliente": "Marcos Andrade",
        "email": "marcos.andrade@company.com",
        "telefone": "+351 931 112 233",
        "servico": "Reserva de Estadia Executive",
        "data": "2026-09-04",
        "hora": "14:00",
        "duracao": "120 min",
        "estado": "Confirmada",
        "preco": "320 €"
    },
    {
        "id": "RES-1004",
        "cliente": "Beatriz Mendonça",
        "email": "beatriz@designstudio.pt",
        "telefone": "+351 918 776 554",
        "servico": "Reunião de Alinhamento Técnico",
        "data": "2026-09-04",
        "hora": "16:00",
        "duracao": "60 min",
        "estado": "Cancelada",
        "preco": "120 €"
    },
    {
        "id": "RES-1005",
        "cliente": "Alexandre Fontes",
        "email": "afontes@investments.eu",
        "telefone": "+351 922 889 900",
        "servico": "Avaliação VIP de Projeto",
        "data": "2026-09-05",
        "hora": "09:00",
        "duracao": "90 min",
        "estado": "Confirmada",
        "preco": "250 €"
    }
]

clientes_db = [
    {"id": "CLI-01", "nome": "Guilherme Siqueira", "email": "guilherme@domain.pt", "telefone": "+351 912 345 678", "reservas": 4, "tipo": "VIP"},
    {"id": "CLI-02", "nome": "Sofia Carvalhal", "email": "sofia.c@domain.pt", "telefone": "+351 965 432 109", "reservas": 2, "tipo": "Regular"},
    {"id": "CLI-03", "nome": "Marcos Andrade", "email": "marcos.andrade@company.com", "telefone": "+351 931 112 233", "reservas": 6, "tipo": "VIP Corp"},
    {"id": "CLI-04", "nome": "Beatriz Mendonça", "email": "beatriz@designstudio.pt", "telefone": "+351 918 776 554", "reservas": 1, "tipo": "Regular"},
    {"id": "CLI-05", "nome": "Alexandre Fontes", "email": "afontes@investments.eu", "telefone": "+351 922 889 900", "reservas": 8, "tipo": "VIP Platinum"}
]

@app.route("/")
def index():
    return render_template("index.html")

# API Endpoints
@app.route("/api/reservas", methods=["GET", "POST"])
def handle_reservas():
    if request.method == "POST":
        data = request.json or {}
        new_id = f"RES-{1000 + len(reservas_db) + 1}"
        new_reserva = {
            "id": new_id,
            "cliente": data.get("cliente", "Cliente Anónimo"),
            "email": data.get("email", "contacto@domain.pt"),
            "telefone": data.get("telefone", "+351 900 000 000"),
            "servico": data.get("servico", "Consulta Geral"),
            "data": data.get("data", str(datetime.now().date())),
            "hora": data.get("hora", "10:00"),
            "duracao": data.get("duracao", "60 min"),
            "estado": "Confirmada",
            "preco": data.get("preco", "150 €")
        }
        reservas_db.insert(0, new_reserva)
        
        # Sync client if not existing
        if not any(c["email"] == new_reserva["email"] for c in clientes_db):
            clientes_db.append({
                "id": f"CLI-0{len(clientes_db)+1}",
                "nome": new_reserva["cliente"],
                "email": new_reserva["email"],
                "telefone": new_reserva["telefone"],
                "reservas": 1,
                "tipo": "Regular"
            })
            
        return jsonify({"success": True, "reserva": new_reserva})
    
    return jsonify(reservas_db)

@app.route("/api/cancelar/<reserva_id>", methods=["POST"])
def cancelar_reserva(reserva_id):
    for r in reservas_db:
        if r["id"] == reserva_id:
            r["estado"] = "Cancelada"
            return jsonify({"success": True, "reserva": r})
    return jsonify({"success": False, "message": "Reserva não encontrada"}), 404

@app.route("/api/clientes", methods=["GET"])
def get_clientes():
    return jsonify(clientes_db)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total = len(reservas_db)
    confirmadas = sum(1 for r in reservas_db if r["estado"] == "Confirmada")
    pendentes = sum(1 for r in reservas_db if r["estado"] == "Pendente")
    canceladas = sum(1 for r in reservas_db if r["estado"] == "Cancelada")
    taxa_ocupacao = round((confirmadas / total * 100) if total > 0 else 0, 1)
    
    return jsonify({
        "total_reservas": total,
        "confirmadas": confirmadas,
        "pendentes": pendentes,
        "canceladas": canceladas,
        "taxa_ocupacao": f"{taxa_ocupacao}%",
        "clientes_ativos": len(clientes_db),
        "receita_estimada": "1.435 €"
    })

if __name__ == "__main__":
    print("Iniciando SISTEMA DE RESERVAS & GESTÃO SAAS em http://localhost:5150")
    app.run(host="0.0.0.0", port=5150, debug=False)
