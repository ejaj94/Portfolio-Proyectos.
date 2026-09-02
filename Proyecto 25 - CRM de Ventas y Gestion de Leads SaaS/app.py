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

# Initial CRM Mock Database
leads_db = [
    {
        "id": "LEAD-2001",
        "empresa": "TechAlgarve Solutions",
        "contacto": "Ricardo Santos",
        "email": "ricardo@techalgarve.pt",
        "telefone": "+351 912 998 877",
        "valor": 12500,
        "estagio": "lead",        # lead, contacto, negociacao, cliente
        "origem": "Website Organic",
        "notas": [
            {"data": "2026-09-01 10:30", "texto": "Lead criado a partir do formulário do site."},
            {"data": "2026-09-02 14:15", "texto": "Enviado e-mail de apresentação de serviços CRM."}
        ]
    },
    {
        "id": "LEAD-2002",
        "empresa": "Clínica Estética Quinta do Lago",
        "contacto": "Dra. Beatriz Vasconcelos",
        "email": "beatriz@clinicavip.pt",
        "telefone": "+351 965 123 456",
        "valor": 28000,
        "estagio": "contacto",
        "origem": "Referência VIP",
        "notas": [
            {"data": "2026-09-02 09:00", "texto": "Primeira reunião de apresentação realizada via Zoom."}
        ]
    },
    {
        "id": "LEAD-2003",
        "empresa": "Veloce Motors Concessionário",
        "contacto": "Gonçalo Mendonça",
        "email": "goncalo@velocemotors.pt",
        "telefone": "+351 931 445 566",
        "valor": 45000,
        "estagio": "negociacao",
        "origem": "Google Ads",
        "notas": [
            {"data": "2026-09-01 16:45", "texto": "Proposta comercial enviada. Cliente a analisar valores."},
            {"data": "2026-09-02 11:20", "texto": "Ajuste na cláusula de suporte anual solicitado."}
        ]
    },
    {
        "id": "LEAD-2004",
        "empresa": "Marina Resort & Spa Hotel",
        "contacto": "Sofia Carvalhal",
        "email": "sofia.c@marina-resort.pt",
        "telefone": "+351 918 223 344",
        "valor": 62000,
        "estagio": "cliente",
        "origem": "Evento Presencial",
        "notas": [
            {"data": "2026-08-28 15:00", "texto": "Contrato assinado! Negócio fechado com sucesso."}
        ]
    },
    {
        "id": "LEAD-2005",
        "empresa": "Algarve Real Estate Group",
        "contacto": "Alexandre Fontes",
        "email": "afontes@algarvere.pt",
        "telefone": "+351 922 556 677",
        "valor": 35000,
        "estagio": "negociacao",
        "origem": "LinkedIn B2B",
        "notas": [
            {"data": "2026-09-02 15:00", "texto": "Demonstração técnica do software SaaS agendada."}
        ]
    }
]

@app.route("/")
def index():
    return render_template("index.html")

# REST API Endpoints
@app.route("/api/leads", methods=["GET", "POST"])
def handle_leads():
    if request.method == "POST":
        data = request.json or {}
        new_id = f"LEAD-{2000 + len(leads_db) + 1}"
        new_lead = {
            "id": new_id,
            "empresa": data.get("empresa", "Empresa Exemplo"),
            "contacto": data.get("contacto", "Pessoa de Contacto"),
            "email": data.get("email", "contacto@empresa.com"),
            "telefone": data.get("telefone", "+351 900 000 000"),
            "valor": float(data.get("valor", 10000)),
            "estagio": "lead",
            "origem": data.get("origem", "Directo"),
            "notas": [
                {"data": datetime.now().strftime("%Y-%m-%d %H:%M"), "texto": "Nova oportunidade criada no CRM."}
            ]
        }
        leads_db.insert(0, new_lead)
        return jsonify({"success": True, "lead": new_lead})
        
    return jsonify(leads_db)

@app.route("/api/leads/advance/<lead_id>", methods=["POST"])
def advance_lead(lead_id):
    stages = ["lead", "contacto", "negociacao", "cliente"]
    for l in leads_db:
        if l["id"] == lead_id:
            curr_idx = stages.index(l["estagio"]) if l["estagio"] in stages else 0
            if curr_idx < len(stages) - 1:
                next_stage = stages[curr_idx + 1]
                l["estagio"] = next_stage
                l["notas"].append({
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "texto": f"Estágio avançado para: {next_stage.upper()}"
                })
                return jsonify({"success": True, "lead": l})
    return jsonify({"success": False, "message": "Lead não encontrado"}), 404

@app.route("/api/leads/notes/<lead_id>", methods=["POST"])
def add_lead_note(lead_id):
    data = request.json or {}
    texto_nota = data.get("texto", "").strip()
    if not texto_nota:
        return jsonify({"success": False, "message": "Texto vazio"}), 400
        
    for l in leads_db:
        if l["id"] == lead_id:
            nova_nota = {
                "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "texto": texto_nota
            }
            l["notas"].append(nova_nota)
            return jsonify({"success": True, "lead": l})
            
    return jsonify({"success": False, "message": "Lead não encontrado"}), 404

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_leads = len(leads_db)
    pipeline_val = sum(l["valor"] for l in leads_db if l["estagio"] != "cliente")
    ganhos_val = sum(l["valor"] for l in leads_db if l["estagio"] == "cliente")
    clientes_fechados = sum(1 for l in leads_db if l["estagio"] == "cliente")
    
    taxa_conversao = round((clientes_fechados / total_leads * 100) if total_leads > 0 else 0, 1)
    
    return jsonify({
        "total_leads": total_leads,
        "pipeline_val": f"{pipeline_val:,.0f} €".replace(",", "."),
        "ganhos_val": f"{ganhos_val:,.0f} €".replace(",", "."),
        "clientes_fechados": clientes_fechados,
        "taxa_conversao": f"{taxa_conversao}%"
    })

if __name__ == "__main__":
    print("Iniciando CRM DE VENDAS & GESTÃO DE LEADS SAAS em http://localhost:5200")
    app.run(host="0.0.0.0", port=5200, debug=False)
