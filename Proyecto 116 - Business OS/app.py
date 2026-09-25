import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# Initialize database
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

# 1. Telemetry / Dashboard KPIs
@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    try:
        data = database.get_dashboard_telemetry()
        return jsonify({"success": True, "telemetry": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 2. Clientes
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
            city=data.get('city', 'Lisboa'),
            tax_id=data.get('tax_id', 'PT999999999'),
            tier=data.get('tier', 'Standard'),
            status=data.get('status', 'Ativo'),
            lifetime_value=float(data.get('lifetime_value', 0.0))
        )
        return jsonify({"success": True, "client_id": cid, "message": "Cliente cadastrado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 3. CRM Deals
@app.route('/api/crm', methods=['GET', 'POST'])
def handle_crm():
    if request.method == 'GET':
        deals = database.get_all_deals()
        return jsonify({"success": True, "deals": deals})

    data = request.json or {}
    try:
        did = database.add_deal(
            client_id=int(data.get('client_id')),
            title=data.get('title'),
            value=float(data.get('value')),
            stage=data.get('stage', 'Prospecto'),
            probability_pct=int(data.get('probability_pct', 50)),
            closing_date=data.get('closing_date'),
            notes=data.get('notes', '')
        )
        return jsonify({"success": True, "deal_id": did, "message": "Oportunidade criada no pipeline!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/crm/<int:did>/stage', methods=['POST'])
def update_deal(did):
    data = request.json or {}
    stage = data.get('stage')
    try:
        database.update_deal_stage(did, stage)
        return jsonify({"success": True, "message": f"Etapa do Deal atualizada para {stage}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 4. Invoices (Facturacao)
@app.route('/api/invoices', methods=['GET', 'POST'])
def handle_invoices():
    if request.method == 'GET':
        invoices = database.get_all_invoices()
        return jsonify({"success": True, "invoices": invoices})

    data = request.json or {}
    try:
        iid, inv_num = database.create_invoice(
            client_id=int(data.get('client_id')),
            due_days=int(data.get('due_days', 30)),
            subtotal=float(data.get('subtotal')),
            tax_rate=float(data.get('tax_rate', 23.0)),
            items_json=data.get('items_json', '[]')
        )
        return jsonify({"success": True, "invoice_id": iid, "invoice_number": inv_num, "message": f"Fatura {inv_num} emitida!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/invoices/<int:iid>/status', methods=['POST'])
def update_invoice(iid):
    data = request.json or {}
    status = data.get('status')
    try:
        database.update_invoice_status(iid, status)
        return jsonify({"success": True, "message": f"Fatura marcada como {status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 5. Quotes (Orcamentos)
@app.route('/api/quotes', methods=['GET', 'POST'])
def handle_quotes():
    if request.method == 'GET':
        quotes = database.get_all_quotes()
        return jsonify({"success": True, "quotes": quotes})

    data = request.json or {}
    try:
        qid, q_num = database.create_quote(
            client_id=int(data.get('client_id')),
            title=data.get('title'),
            subtotal=float(data.get('subtotal')),
            valid_days=int(data.get('valid_days', 30)),
            items_json=data.get('items_json', '[]')
        )
        return jsonify({"success": True, "quote_id": qid, "quote_number": q_num, "message": f"Orcamento {q_num} gerado!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/quotes/<int:qid>/convert', methods=['POST'])
def convert_quote(qid):
    try:
        res = database.convert_quote_to_invoice(qid)
        if res:
            new_inv_id, inv_num = res
            return jsonify({"success": True, "invoice_id": new_inv_id, "invoice_number": inv_num, "message": f"Orcamento convertido na Fatura {inv_num}!"})
        return jsonify({"success": False, "error": "Orcamento nao encontrado."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 6. Inventory
@app.route('/api/inventory', methods=['GET', 'POST'])
def handle_inventory():
    if request.method == 'GET':
        items = database.get_all_inventory()
        return jsonify({"success": True, "inventory": items})

    data = request.json or {}
    try:
        item_id = database.add_inventory_item(
            sku=data.get('sku'),
            name=data.get('name'),
            category=data.get('category', 'Hardware'),
            stock_qty=int(data.get('stock_quantity', 10)),
            min_threshold=int(data.get('min_threshold', 5)),
            cost_price=float(data.get('cost_price')),
            sale_price=float(data.get('sale_price')),
            unit=data.get('unit', 'Unid')
        )
        return jsonify({"success": True, "item_id": item_id, "message": "Artigo adicionado ao inventario!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/inventory/<int:item_id>/adjust', methods=['POST'])
def adjust_inventory_stock(item_id):
    data = request.json or {}
    delta = int(data.get('delta', 0))
    try:
        database.adjust_stock(item_id, delta)
        return jsonify({"success": True, "message": "Stock atualizado!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 7. Tasks
@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        tasks = database.get_all_tasks()
        return jsonify({"success": True, "tasks": tasks})

    data = request.json or {}
    try:
        tid = database.add_task(
            title=data.get('title'),
            client_id=int(data.get('client_id')) if data.get('client_id') else None,
            priority=data.get('priority', 'Media'),
            due_date=data.get('due_date'),
            assigned_to=data.get('assigned_to', 'Equipa')
        )
        return jsonify({"success": True, "task_id": tid, "message": "Tarefa criada com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/tasks/<int:tid>/status', methods=['POST'])
def update_task_state(tid):
    data = request.json or {}
    status = data.get('status', 'Concluida')
    try:
        database.update_task_status(tid, status)
        return jsonify({"success": True, "message": f"Tarefa marcada como {status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 8. Calendar
@app.route('/api/calendar', methods=['GET', 'POST'])
def handle_calendar():
    if request.method == 'GET':
        events = database.get_all_events()
        return jsonify({"success": True, "events": events})

    data = request.json or {}
    try:
        eid = database.add_calendar_event(
            title=data.get('title'),
            event_type=data.get('event_type', 'Reuniao'),
            event_date=data.get('event_date'),
            start_time=data.get('start_time', '10:00'),
            end_time=data.get('end_time', '11:00'),
            client_id=int(data.get('client_id')) if data.get('client_id') else None,
            location=data.get('location', 'Online')
        )
        return jsonify({"success": True, "event_id": eid, "message": "Evento agendado no calendario!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# 9. Support Tickets
@app.route('/api/tickets', methods=['GET', 'POST'])
def handle_tickets():
    if request.method == 'GET':
        tickets = database.get_all_tickets()
        return jsonify({"success": True, "tickets": tickets})

    data = request.json or {}
    try:
        tid, code = database.create_ticket(
            client_id=int(data.get('client_id')),
            subject=data.get('subject'),
            priority=data.get('priority', 'Media'),
            channel=data.get('channel', 'Email')
        )
        return jsonify({"success": True, "ticket_id": tid, "ticket_code": code, "message": f"Ticket {code} aberto!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/tickets/<int:tid>/status', methods=['POST'])
def update_ticket_state(tid):
    data = request.json or {}
    status = data.get('status', 'Resolvido')
    try:
        database.update_ticket_status(tid, status)
        return jsonify({"success": True, "message": f"Ticket marcado como {status}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 10. AI Brain & Copilot
@app.route('/api/ai/insights', methods=['GET'])
def get_insights():
    try:
        insights = database.get_ai_insights()
        return jsonify({"success": True, "insights": insights})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ai/query', methods=['POST'])
def ai_query():
    data = request.json or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({"success": False, "error": "Prompt vazio."}), 400
    try:
        reply = database.process_ai_copilot_query(prompt)
        return jsonify({"success": True, "reply": reply})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6969))
    print(f">> NEXUS Business OS rodando em http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
