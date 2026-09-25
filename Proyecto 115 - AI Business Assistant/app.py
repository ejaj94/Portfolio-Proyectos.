import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# Initialize DB on launch
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

# 1. Dashboard KPIs & Metrics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        kpis = database.get_dashboard_kpis()
        return jsonify({"success": True, "kpis": kpis})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 2. Clients (CRM)
@app.route('/api/clients', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'GET':
        clients = database.get_all_clients()
        return jsonify({"success": True, "clients": clients})

    data = request.json or {}
    try:
        cid = database.add_client(
            company_name=data.get('company_name'),
            contact_name=data.get('contact_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            industry=data.get('industry', 'Tecnologia'),
            status=data.get('status', 'Ativo'),
            monthly_value=float(data.get('monthly_value', 0.0)),
            notes=data.get('notes', '')
        )
        return jsonify({"success": True, "client_id": cid, "message": "Cliente adicionado ao CRM com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 3. Chat / Copilot
@app.route('/api/chat', methods=['GET', 'POST'])
def handle_chat():
    if request.method == 'GET':
        history = database.get_chat_history()
        return jsonify({"success": True, "messages": history})

    data = request.json or {}
    user_msg = data.get('message', '').strip()
    mode = data.get('mode', 'Estrategia')

    if not user_msg:
        return jsonify({"success": False, "error": "Mensagem vazia."}), 400

    try:
        reply, tokens = database.process_ai_chat(user_msg, mode)
        return jsonify({"success": True, "reply": reply, "tokens_used": tokens})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 4. Summaries
@app.route('/api/summaries', methods=['GET', 'POST'])
def handle_summaries():
    if request.method == 'GET':
        summaries = database.get_all_summaries()
        return jsonify({"success": True, "summaries": summaries})

    data = request.json or {}
    title = data.get('title', 'Resumo Sem Titulo')
    source_type = data.get('source_type', 'Reuniao')
    text = data.get('text', '').strip()

    if not text:
        return jsonify({"success": False, "error": "Texto para resumo e obrigatorio."}), 400

    try:
        sid, summary_text, action_points, sentiment = database.generate_ai_summary(title, source_type, text)
        return jsonify({
            "success": True,
            "summary_id": sid,
            "summary_text": summary_text,
            "action_points": action_points,
            "sentiment": sentiment,
            "message": "Resumo executivo processado pela IA!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 5. Email Generator
@app.route('/api/emails', methods=['GET', 'POST'])
def handle_emails():
    if request.method == 'GET':
        emails = database.get_all_emails()
        return jsonify({"success": True, "emails": emails})

    data = request.json or {}
    client_name = data.get('client_name', 'Cliente')
    email_type = data.get('email_type', 'Proposta Comercial')
    tone = data.get('tone', 'Profissional')
    key_points = data.get('key_points', '')

    try:
        eid, subject, body = database.generate_ai_email(client_name, email_type, tone, key_points)
        return jsonify({
            "success": True,
            "email_id": eid,
            "subject": subject,
            "body": body,
            "message": "Email corporativo gerado com sucesso!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 6. Tasks
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = database.get_all_tasks()
        return jsonify({"success": True, "tasks": tasks})

    data = request.json or {}
    try:
        tid = database.add_task(
            title=data.get('title'),
            client_name=data.get('client_name', ''),
            priority=data.get('priority', 'Media'),
            due_date=data.get('due_date')
        )
        return jsonify({"success": True, "task_id": tid, "message": "Tarefa criada!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/tasks/<int:tid>/status', methods=['POST'])
def update_task(tid):
    data = request.json or {}
    status = data.get('status', 'Concluida')
    try:
        database.update_task_status(tid, status)
        return jsonify({"success": True, "message": f"Tarefa marcada como {status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 7. Activity History
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = database.get_activity_history(limit=50)
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6968))
    print(f">> Nexa AI Business Assistant rodando em http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
