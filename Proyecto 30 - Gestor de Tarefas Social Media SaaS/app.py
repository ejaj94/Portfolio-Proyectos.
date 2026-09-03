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

# Initial Mock Task & Team Database for Social Media Agency
equipa_db = [
    {"id": "EMP-01", "nome": "Mariana Ramos", "cargo": "Social Media Manager", "avatar": "MR"},
    {"id": "EMP-02", "nome": "Diogo Vasconcelos", "cargo": "Motion & Video Editor", "avatar": "DV"},
    {"id": "EMP-03", "nome": "Carolina Mendes", "cargo": "Graphic & Brand Designer", "avatar": "CM"},
    {"id": "EMP-04", "nome": "Tiago Carvalhal", "cargo": "Copywriter & Content Creator", "avatar": "TC"}
]

tarefas_db = [
    {
        "id": "TSK-3001",
        "titulo": "Carrossel de Tendências AI no Instagram",
        "descricao": "Criar 6 slides informativos sobre ferramentas de IA para marketing digital.",
        "plataforma": "Instagram",      # Instagram, TikTok, LinkedIn, YouTube, Facebook
        "estagio": "briefing",          # briefing, producao, revisao, publicado
        "prioridade": "Alta",          # Alta, Média, Baixa
        "responsavel": "Mariana Ramos",
        "data_publicacao": "2026-09-05",
        "comentarios": 3
    },
    {
        "id": "TSK-3002",
        "titulo": "Vídeo Reel / TikTok: Bastidores do Projeto Marina Resort",
        "descricao": "Edição dinâmica de 30 segundos com transições modernas e música em tendência.",
        "plataforma": "TikTok",
        "estagio": "producao",
        "prioridade": "Alta",
        "responsavel": "Diogo Vasconcelos",
        "data_publicacao": "2026-09-04",
        "comentarios": 5
    },
    {
        "id": "TSK-3003",
        "titulo": "Artigo B2B LinkedIn: O Futuro dos Sistemas SaaS",
        "descricao": "Texto profundo de 800 palavras focado em decisores de empresas no setor imobiliário.",
        "plataforma": "LinkedIn",
        "estagio": "revisao",
        "prioridade": "Média",
        "responsavel": "Tiago Carvalhal",
        "data_publicacao": "2026-09-06",
        "comentarios": 2
    },
    {
        "id": "TSK-3004",
        "titulo": "Design de Stories & Banners para EJAJ TECH",
        "descricao": "Criativo gráfico promocional para o lançamento do novo produto de facturação.",
        "plataforma": "Instagram",
        "estagio": "publicado",
        "prioridade": "Média",
        "responsavel": "Carolina Mendes",
        "data_publicacao": "2026-09-02",
        "comentarios": 4
    },
    {
        "id": "TSK-3005",
        "titulo": "Tutorial YouTube: Como Funciona o CRM de Ventas",
        "descricao": "Gravação de ecrã com locução profissional demonstrando o fluxo de leads.",
        "plataforma": "YouTube",
        "estagio": "producao",
        "prioridade": "Baixa",
        "responsavel": "Diogo Vasconcelos",
        "data_publicacao": "2026-09-08",
        "comentarios": 1
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tarefas", methods=["GET"])
def get_tarefas():
    return jsonify(tarefas_db)

@app.route("/api/equipa", methods=["GET"])
def get_equipa():
    return jsonify(equipa_db)

@app.route("/api/tarefas/criar", methods=["POST"])
def criar_tarefa():
    data = request.json or {}
    new_id = f"TSK-{3000 + len(tarefas_db) + 1}"
    
    nova_tarefa = {
        "id": new_id,
        "titulo": data.get("titulo", "Nova Tarefa de Conteúdo"),
        "descricao": data.get("descricao", "Descrição do post para redes sociais."),
        "plataforma": data.get("plataforma", "Instagram"),
        "estagio": "briefing",
        "prioridade": data.get("prioridade", "Média"),
        "responsavel": data.get("responsavel", "Mariana Ramos"),
        "data_publicacao": data.get("data_publicacao", datetime.now().strftime("%Y-%m-%d")),
        "comentarios": 0
    }
    
    tarefas_db.insert(0, nova_tarefa)
    return jsonify({"success": True, "tarefa": nova_tarefa})

@app.route("/api/tarefas/mover/<tarefa_id>", methods=["POST"])
def mover_tarefa(tarefa_id):
    estagios = ["briefing", "producao", "revisao", "publicado"]
    for t in tarefas_db:
        if t["id"] == tarefa_id:
            curr_idx = estagios.index(t["estagio"]) if t["estagio"] in estagios else 0
            if curr_idx < len(estagios) - 1:
                next_stage = estagios[curr_idx + 1]
                t["estagio"] = next_stage
                return jsonify({"success": True, "tarefa": t})
                
    return jsonify({"success": False, "message": "Tarefa não encontrada"}), 404

@app.route("/api/stats", methods=["GET"])
def get_stats():
    total_tarefas = len(tarefas_db)
    em_producao = sum(1 for t in tarefas_db if t["estagio"] == "producao")
    publicados = sum(1 for t in tarefas_db if t["estagio"] == "publicado")
    alta_prioridade = sum(1 for t in tarefas_db if t["prioridade"] == "Alta" and t["estagio"] != "publicado")
    
    return jsonify({
        "total_tarefas": total_tarefas,
        "em_producao": em_producao,
        "publicados": publicados,
        "alta_prioridade": alta_prioridade
    })

if __name__ == "__main__":
    print("Iniciando GESTOR DE TAREFAS SOCIAL MEDIA SAAS em http://localhost:5450")
    app.run(host="0.0.0.0", port=5450, debug=False)
