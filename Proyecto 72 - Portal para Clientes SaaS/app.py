import os
import sqlite3
import json
import csv
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clientportal_ejajtech_secret_key_2026'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'clientportal.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_current_client_id():
    return session.get('client_id', 1)

@app.before_request
def check_auth():
    # Public routes
    public_endpoints = ['login', 'do_login', 'static']
    if request.endpoint and request.endpoint not in public_endpoints:
        if 'client_id' not in session:
            session['client_id'] = 1  # Default auto-login as Aura Luxe Group for demo ease

@app.route('/login')
def login():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients ORDER BY id ASC")
    clients = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return render_template('login.html', clients=clients)

@app.route('/do_login', methods=['POST'])
def do_login():
    client_id = request.form.get('client_id', type=int)
    if client_id:
        session['client_id'] = client_id
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('client_id', None)
    return redirect(url_for('login'))

@app.route('/')
def dashboard():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    # Client Info
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    # Stats Metrics
    cursor.execute("SELECT COUNT(*) as cnt FROM projects WHERE client_id = ?", (client_id,))
    total_projects = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM projects WHERE client_id = ? AND status = 'Em Progresso'", (client_id,))
    active_projects = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM invoices WHERE client_id = ? AND status = 'Pendente'", (client_id,))
    pending_invoices_cnt = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(amount_total) as sum_pending FROM invoices WHERE client_id = ? AND status = 'Pendente'", (client_id,))
    pending_amount = cursor.fetchone()['sum_pending'] or 0.0

    cursor.execute("SELECT COUNT(*) as cnt FROM tickets WHERE client_id = ? AND status != 'Resolvido'", (client_id,))
    open_tickets_cnt = cursor.fetchone()['cnt']

    # Active Projects List
    cursor.execute("SELECT * FROM projects WHERE client_id = ? ORDER BY id DESC LIMIT 3", (client_id,))
    projects = [dict(r) for r in cursor.fetchall()]

    # Recent Invoices
    cursor.execute("SELECT * FROM invoices WHERE client_id = ? ORDER BY id DESC LIMIT 4", (client_id,))
    invoices = [dict(r) for r in cursor.fetchall()]

    # Recent Messages
    cursor.execute("SELECT * FROM messages WHERE client_id = ? ORDER BY id DESC LIMIT 5", (client_id,))
    messages = [dict(r) for r in cursor.fetchall()]
    messages.reverse()  # Chronological order for chat UI

    # Recent Documents
    cursor.execute("SELECT * FROM documents WHERE client_id = ? ORDER BY id DESC LIMIT 4", (client_id,))
    documents = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        client=client,
        total_projects=total_projects,
        active_projects=active_projects,
        pending_invoices_cnt=pending_invoices_cnt,
        pending_amount=pending_amount,
        open_tickets_cnt=open_tickets_cnt,
        projects=projects,
        invoices=invoices,
        messages=messages,
        documents=documents
    )

@app.route('/projects')
def projects_page():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    status_filter = request.args.get('status')
    query = "SELECT * FROM projects WHERE client_id = ?"
    params = [client_id]

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    projects = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('projects.html', client=client, projects=projects, selected_status=status_filter)

@app.route('/documents')
def documents_page():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    doc_type_filter = request.args.get('type')
    query = "SELECT d.*, p.project_name FROM documents d LEFT JOIN projects p ON d.project_id = p.id WHERE d.client_id = ?"
    params = [client_id]

    if doc_type_filter:
        query += " AND d.doc_type = ?"
        params.append(doc_type_filter)

    query += " ORDER BY d.id DESC"
    cursor.execute(query, params)
    documents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, project_name FROM projects WHERE client_id = ?", (client_id,))
    client_projects = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('documents.html', client=client, documents=documents, client_projects=client_projects, selected_type=doc_type_filter)

@app.route('/invoices')
def invoices_page():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    status_filter = request.args.get('status')
    query = "SELECT * FROM invoices WHERE client_id = ?"
    params = [client_id]

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    invoices = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT SUM(amount_total) as total_paid FROM invoices WHERE client_id = ? AND status = 'Paga'", (client_id,))
    total_paid = cursor.fetchone()['total_paid'] or 0.0

    cursor.execute("SELECT SUM(amount_total) as total_pending FROM invoices WHERE client_id = ? AND status = 'Pendente'", (client_id,))
    total_pending = cursor.fetchone()['total_pending'] or 0.0

    conn.close()
    return render_template('invoices.html', client=client, invoices=invoices, selected_status=status_filter, total_paid=total_paid, total_pending=total_pending)

@app.route('/invoice/<int:invoice_id>')
def invoice_detail(invoice_id):
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    cursor.execute("SELECT * FROM invoices WHERE id = ? AND client_id = ?", (invoice_id, client_id))
    inv_row = cursor.fetchone()

    if not inv_row:
        conn.close()
        return redirect(url_for('invoices_page'))

    invoice = dict(inv_row)
    conn.close()
    return render_template('invoice_detail.html', client=client, invoice=invoice)

@app.route('/messages')
def messages_page():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    cursor.execute("SELECT * FROM messages WHERE client_id = ? ORDER BY id ASC", (client_id,))
    messages = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('messages.html', client=client, messages=messages)

@app.route('/tickets')
def tickets_page():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    status_filter = request.args.get('status')
    query = "SELECT * FROM tickets WHERE client_id = ?"
    params = [client_id]

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    tickets = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('tickets.html', client=client, tickets=tickets, selected_status=status_filter)

@app.route('/profile')
def profile_page():
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = dict(cursor.fetchone() or {})

    conn.close()
    return render_template('profile.html', client=client)

# API ENDPOINTS

@app.route('/api/message/send', methods=['POST'])
def api_send_message():
    try:
        client_id = get_current_client_id()
        data = request.get_json() or {}
        content = data.get('content', '').strip()

        if not content:
            return jsonify({'success': False, 'message': 'Escreva uma mensagem antes de enviar.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT contact_name FROM clients WHERE id = ?", (client_id,))
        client_name = cursor.fetchone()['contact_name']

        cursor.execute("""
        INSERT INTO messages (client_id, sender_type, sender_name, content, sent_at)
        VALUES (?, 'Cliente', ?, ?, ?)
        """, (client_id, client_name, content, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Mensagem enviada para o seu Gestor de Conta!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/ticket/create', methods=['POST'])
def api_create_ticket():
    try:
        client_id = get_current_client_id()
        data = request.get_json() or {}
        subject = data.get('subject', '').strip()
        category = data.get('category', 'Técnico')
        priority = data.get('priority', 'Média')

        if not subject:
            return jsonify({'success': False, 'message': 'Preencha o assunto do ticket.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM tickets")
        code_num = cursor.fetchone()['cnt'] + 8891
        ticket_code = f"TCK-{code_num}"

        cursor.execute("""
        INSERT INTO tickets (client_id, ticket_code, subject, category, priority, status, created_at, last_update)
        VALUES (?, ?, ?, ?, ?, 'Aberto', ?, ?)
        """, (client_id, ticket_code, subject, category, priority, now_str, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Ticket "{ticket_code}" aberto com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/document/upload', methods=['POST'])
def api_upload_document():
    try:
        client_id = get_current_client_id()
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        doc_type = data.get('doc_type', 'Especificação')
        project_id = data.get('project_id')

        if not title:
            return jsonify({'success': False, 'message': 'Nomeie o documento a carregar.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO documents (client_id, project_id, title, doc_type, file_size, upload_date, file_url)
        VALUES (?, ?, ?, ?, '1.5 MB', ?, '#')
        """, (client_id, project_id, title, doc_type, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Documento "{title}" carregado para o portal!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    client_id = get_current_client_id()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects WHERE client_id = ?", (client_id,))
    projects = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM invoices WHERE client_id = ?", (client_id,))
    invoices = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM tickets WHERE client_id = ?", (client_id,))
    tickets = [dict(r) for r in cursor.fetchall()]

    conn.close()

    export_payload = {
        'client_id': client_id,
        'projects': projects,
        'invoices': invoices,
        'tickets': tickets,
        'exported_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if fmt.lower() == 'json':
        return Response(
            json.dumps(export_payload, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment;filename=clientportal_export_{client_id}.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Tipo', 'ID / Código', 'Nome / Assunto', 'Estado', 'Valor (€) / Progresso (%)', 'Data'])

        for p in projects:
            writer.writerow(['Projeto', p['id'], p['project_name'], p['status'], f"{p['progress_percent']}%", p['deadline']])
        for inv in invoices:
            writer.writerow(['Fatura', inv['invoice_number'], inv['description'], inv['status'], f"{inv['amount_total']:.2f} €", inv['issue_date']])
        for t in tickets:
            writer.writerow(['Ticket', t['ticket_code'], t['subject'], t['status'], t['priority'], t['created_at']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment;filename=clientportal_export_{client_id}.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6925, debug=True)
