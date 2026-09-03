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

# Initial Real Estate Property Management Mock Database
propiedades_db = [
    {
        "id": "PROP-101",
        "titulo": "Apartamento Familiar T2 Parque Central",
        "tipo": "Apartamento",
        "morada": "Av. da República 142, 3º Dto, Lisboa",
        "renda": 850,
        "tipologia": "T2 • 1 WC • 85m²",
        "proprietario": "Carlos Silva",
        "estado": "Alugado",
        "foto": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": "PROP-102",
        "nome_curto": "Moradia Jardim T3",
        "titulo": "Moradia Geminada T3 com Jardim",
        "tipo": "Moradia",
        "morada": "Rua dos Pinheiros 28, Setúbal",
        "renda": 1150,
        "tipologia": "T3 • 2 WC • 140m²",
        "proprietario": "Ana Vasconcelos",
        "estado": "Alugado",
        "foto": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": "PROP-103",
        "titulo": "Estúdio Moderno T1 Centro Histórico",
        "tipo": "Estúdio",
        "morada": "Rua das Flores 15, 1º Esq, Porto",
        "renda": 650,
        "tipologia": "T1 • 1 WC • 48m²",
        "proprietario": "Ricardo Alvares",
        "estado": "Disponível",
        "foto": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": "PROP-104",
        "titulo": "Apartamento Residencial T3 Vista Rio",
        "tipo": "Apartamento",
        "morada": "Alameda dos Oceanos 88, 5º A, Parque das Nações",
        "renda": 1250,
        "tipologia": "T3 • 2 WC • 110m²",
        "proprietario": "Beatriz Lima",
        "estado": "Alugado",
        "foto": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": "PROP-105",
        "titulo": "Townhouse Conchegante T2 com Varanda",
        "tipo": "Moradia",
        "morada": "Rua de São José 44, Cascais",
        "renda": 950,
        "tipologia": "T2 • 1.5 WC • 95m²",
        "proprietario": "Dr. Fernando Siqueira",
        "estado": "Em Manutenção",
        "foto": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80"
    }
]

inquilinos_db = [
    {
        "id": "INQ-201",
        "nome": "João Pedro Mendonça",
        "unidade": "Apartamento T2 Parque Central",
        "contacto": "+351 912 345 678",
        "email": "joao.mendonca@gmail.com",
        "renda_mensal": 850,
        "data_inicio": "2023-09-01",
        "estado_pago": "Pago",
        "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "INQ-202",
        "nome": "Mariana Fonseca",
        "unidade": "Moradia Geminada T3 com Jardim",
        "contacto": "+351 965 432 109",
        "email": "mariana.fonseca@outlook.pt",
        "renda_mensal": 1150,
        "data_inicio": "2024-01-15",
        "estado_pago": "Pago",
        "foto": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80"
    },
    {
        "id": "INQ-203",
        "nome": "Diogo Carvalhal",
        "unidade": "Apartamento T3 Vista Rio",
        "contacto": "+351 933 778 990",
        "email": "diogo.carvalhal@sapo.pt",
        "renda_mensal": 1250,
        "data_inicio": "2023-11-01",
        "estado_pago": "Pendente",
        "foto": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80"
    }
]

pagos_db = [
    {
        "id": "PAG-801",
        "inquilino": "João Pedro Mendonça",
        "propriedade": "Apartamento T2 Parque Central",
        "valor": "850.00 €",
        "mes_referencia": "Setembro 2026",
        "data_pago": "2026-09-01",
        "metodo": "Transferência MBWay",
        "estado": "Concluído"
    },
    {
        "id": "PAG-802",
        "inquilino": "Mariana Fonseca",
        "propriedade": "Moradia Geminada T3 com Jardim",
        "valor": "1.150.00 €",
        "mes_referencia": "Setembro 2026",
        "data_pago": "2026-09-02",
        "metodo": "Débito Direto",
        "estado": "Concluído"
    },
    {
        "id": "PAG-803",
        "inquilino": "Diogo Carvalhal",
        "propriedade": "Apartamento T3 Vista Rio",
        "valor": "1.250.00 €",
        "mes_referencia": "Setembro 2026",
        "data_pago": "2026-09-05 (Previsto)",
        "metodo": "Transferência Bancária",
        "estado": "Pendente"
    }
]

incidencias_db = [
    {
        "id": "INC-401",
        "propriedade": "Townhouse T2 com Varanda",
        "inquilino": "Sem Inquilino (Em Manutenção)",
        "descricao": "Reparação de canalização de esquentador e pintura de parede da sala",
        "prioridade": "Alta",
        "data_abertura": "2026-09-01",
        "custo_estimado": "320.00 €",
        "estado": "Em Resolução"
    },
    {
        "id": "INC-402",
        "propriedade": "Apartamento T3 Vista Rio",
        "inquilino": "Diogo Carvalhal",
        "descricao": "Ajuste de fechadura de segurança da porta principal",
        "prioridade": "Média",
        "data_abertura": "2026-09-03",
        "custo_estimado": "85.00 €",
        "estado": "Aberto"
    },
    {
        "id": "INC-403",
        "propriedade": "Apartamento T2 Parque Central",
        "inquilino": "João Pedro Mendonça",
        "descricao": "Substituição de correia de estor da janela do quarto principal",
        "prioridade": "Baixa",
        "data_abertura": "2026-08-28",
        "custo_estimado": "45.00 €",
        "estado": "Resolvido"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/propiedades", methods=["GET"])
def get_propiedades():
    return jsonify(propiedades_db)

@app.route("/api/propiedades/criar", methods=["POST"])
def criar_propriedade():
    data = request.json or {}
    new_id = f"PROP-{100 + len(propiedades_db) + 1}"
    
    nova_propriedade = {
        "id": new_id,
        "titulo": data.get("titulo", "Nova Propriedade Residencial"),
        "tipo": data.get("tipo", "Apartamento"),
        "morada": data.get("morada", "Av. Principal, Lisboa"),
        "renda": float(data.get("renda", 800)),
        "tipologia": f"{data.get('tipologia', 'T2')} • 1 WC • 80m²",
        "proprietario": data.get("proprietario", "Proprietário Registado"),
        "estado": "Disponível",
        "foto": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"
    }
    
    propiedades_db.insert(0, nova_propriedade)
    return jsonify({"success": True, "propriedade": nova_propriedade})

@app.route("/api/inquilinos", methods=["GET"])
def get_inquilinos():
    return jsonify(inquilinos_db)

@app.route("/api/pagos", methods=["GET"])
def get_pagos():
    return jsonify(pagos_db)

@app.route("/api/incidencias", methods=["GET"])
def get_incidencias():
    return jsonify(incidencias_db)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_propriedades = len(propiedades_db)
    renda_total = sum(p["renda"] for p in propiedades_db if p["estado"] == "Alugado")
    alugadas = sum(1 for p in propiedades_db if p["estado"] == "Alugado")
    taxa_ocupacao = f"{int((alugadas / total_propriedades) * 100)}%" if total_propriedades > 0 else "0%"
    incidencias_abertas = sum(1 for i in incidencias_db if i["estado"] in ["Aberto", "Em Resolução"])
    total_inquilinos = len(inquilinos_db)
    
    return jsonify({
        "total_propriedades": total_propriedades,
        "renda_total": f"{renda_total:,.2f} €",
        "taxa_ocupacao": taxa_ocupacao,
        "incidencias_abertas": incidencias_abertas,
        "total_inquilinos": total_inquilinos
    })

if __name__ == "__main__":
    print("Iniciando GESTOR DE PROPRIEDADES INMOBILIARIAS SAAS em http://localhost:5850")
    app.run(host="0.0.0.0", port=5850, debug=False)
