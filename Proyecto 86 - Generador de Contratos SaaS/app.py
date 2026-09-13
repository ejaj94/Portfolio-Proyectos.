import os
import sqlite3
import csv
import io
import datetime
import hashlib
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/templates')
def templates_page():
    return render_template('templates_page.html', active_page='templates')

@app.route('/clients')
def clients():
    return render_template('clients.html', active_page='clients')

@app.route('/generate')
def generate():
    return render_template('generate.html', active_page='generate')

@app.route('/history')
def history():
    return render_template('history.html', active_page='history')

@app.route('/stats')
def stats():
    return render_template('stats.html', active_page='stats')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html', active_page='showcase')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM contracts')
    total_contracts = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM contracts WHERE status = "Assinado & Válido"')
    signed_contracts = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM templates')
    total_templates = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM clients')
    total_clients = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'total_contracts': total_contracts,
        'signed_contracts': signed_contracts,
        'total_templates': total_templates,
        'total_clients': total_clients
    })

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        category = data.get('category', 'Geral').strip()
        description = data.get('description', '').strip()
        variable_tags = data.get('variable_tags', '').strip()
        content_text = data.get('content_text', '').strip()

        if not title or not content_text:
            return jsonify({'success': False, 'message': 'Preencha o título e o texto do contrato!'}), 400

        cursor.execute('''
            INSERT INTO templates (title, category, description, variable_tags, content_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, description, variable_tags, content_text))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Modelo de contrato criado com sucesso!'})

    cursor.execute('SELECT * FROM templates ORDER BY id DESC')
    templates = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(templates)

@app.route('/api/clients', methods=['GET', 'POST'])
def handle_clients():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        nif_tax = data.get('nif_tax', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        address = data.get('address', '').strip()
        company_name = data.get('company_name', '').strip()

        if not name or not nif_tax:
            return jsonify({'success': False, 'message': 'Preencha o nome e o NIF!'}), 400

        try:
            cursor.execute('''
                INSERT INTO clients (name, nif_tax, email, phone, address, company_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, nif_tax, email, phone, address, company_name))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Cliente registado com sucesso!'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'NIF já se encontra registado!'}), 400

    cursor.execute('SELECT * FROM clients ORDER BY id DESC')
    clients = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(clients)

@app.route('/api/contracts', methods=['GET', 'POST'])
def handle_contracts():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        template_id = data.get('template_id')
        client_id = data.get('client_id')
        custom_title = data.get('title', '').strip()

        if not template_id or not client_id:
            return jsonify({'success': False, 'message': 'Selecione o modelo e o cliente!'}), 400

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        contract_code = f"CTR-2026-{int(datetime.datetime.now().timestamp()) % 10000:04d}"
        raw_hash = f"{contract_code}-{template_id}-{client_id}-{now_str}"
        hash_signature = f"HASH-SHA256-{hashlib.sha256(raw_hash.encode()).hexdigest()[:12].upper()}"

        cursor.execute('''
            INSERT INTO contracts (contract_code, title, template_id, client_id, status, hash_signature, created_at, pdf_url)
            VALUES (?, ?, ?, ?, 'Assinado & Válido', ?, ?, ?)
        ''', (contract_code, custom_title or f"Contrato {contract_code}", template_id, client_id, hash_signature, now_str, f"/export/pdf/{contract_code}"))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Contrato gerado e assinado com sucesso!', 'code': contract_code, 'hash': hash_signature})

    cursor.execute('''
        SELECT contracts.*, templates.title as template_title, clients.name as client_name, clients.nif_tax
        FROM contracts
        JOIN templates ON contracts.template_id = templates.id
        JOIN clients ON contracts.client_id = clients.id
        ORDER BY contracts.id DESC
    ''')
    contracts = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(contracts)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT contracts.contract_code, contracts.title as Titulo_Contrato, clients.name as Cliente,
               clients.nif_tax as NIF, contracts.status as Estado, contracts.hash_signature as Hash_Assinatura,
               contracts.created_at as Data_Criacao
        FROM contracts
        JOIN clients ON contracts.client_id = clients.id
    ''')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if fmt == 'json':
        return jsonify(rows)
    elif fmt == 'csv':
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_contracts.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando ContractCraft AI SaaS no servidor local porta 6939...")
    app.run(host='0.0.0.0', port=6939, debug=True)
