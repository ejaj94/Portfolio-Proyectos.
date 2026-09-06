import os
import sqlite3
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import DB_PATH, init_db

app = Flask(__name__)
app.secret_key = 'ejajtech_commercial_proposals_saas_secret_key'

# Custom Filters
@app.template_filter('currency')
def currency_filter(value):
    if value is None:
        return "€ 0,00"
    try:
        val = float(value)
        return f"€ {val:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
    except Exception:
        return f"€ {value}"

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if not os.path.exists(DB_PATH):
    init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proposals')
def proposals_list():
    conn = get_db_connection()
    proposals = [dict(r) for r in conn.execute('SELECT * FROM proposals ORDER BY created_at DESC').fetchall()]
    conn.close()
    return render_template('proposals.html', proposals=proposals)

@app.route('/proposal/<code_str>')
def proposal_view(code_str):
    conn = get_db_connection()
    prop_row = conn.execute('SELECT * FROM proposals WHERE code = ?', (code_str,)).fetchone()
    if not prop_row:
        conn.close()
        return "Proposta Comercial não encontrada", 404
        
    prop = dict(prop_row)
    items = [dict(r) for r in conn.execute('SELECT * FROM proposal_items WHERE proposal_id = ? ORDER BY id ASC', (prop['id'],)).fetchall()]
    timeline = [dict(r) for r in conn.execute('SELECT * FROM proposal_timeline WHERE proposal_id = ? ORDER BY id ASC', (prop['id'],)).fetchall()]
    conn.close()
    
    return render_template('proposal_view.html', prop=prop, items=items, timeline=timeline)

@app.route('/proposal/<code_str>/pdf')
def proposal_pdf(code_str):
    conn = get_db_connection()
    prop_row = conn.execute('SELECT * FROM proposals WHERE code = ?', (code_str,)).fetchone()
    if not prop_row:
        conn.close()
        return "Proposta Comercial não encontrada", 404
        
    prop = dict(prop_row)
    items = [dict(r) for r in conn.execute('SELECT * FROM proposal_items WHERE proposal_id = ? ORDER BY id ASC', (prop['id'],)).fetchall()]
    timeline = [dict(r) for r in conn.execute('SELECT * FROM proposal_timeline WHERE proposal_id = ? ORDER BY id ASC', (prop['id'],)).fetchall()]
    conn.close()
    
    return render_template('proposal_pdf.html', prop=prop, items=items, timeline=timeline)

# API ENDPOINTS
@app.route('/api/proposals/create', methods=['POST'])
def api_proposal_create():
    data = request.json or {}
    
    client_name = data.get('client_name', '').strip()
    client_company = data.get('client_company', '').strip()
    client_email = data.get('client_email', '').strip()
    client_phone = data.get('client_phone', '').strip()
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    validity_days = int(data.get('validity_days', 30))
    vat_rate = float(data.get('vat_rate', 23.0))
    payment_terms = data.get('payment_terms', '').strip()
    
    items = data.get('items', [])
    timeline = data.get('timeline', [])
    
    if not client_name or not client_company or not title or not items:
        return jsonify({'success': False, 'message': 'Por favor preencha os dados do cliente, título e adicione pelo menos um serviço.'}), 400
        
    subtotal = 0.0
    for item in items:
        qty = int(item.get('quantity', 1))
        price = float(item.get('unit_price', 0))
        subtotal += (qty * price)
        
    vat_amount = round(subtotal * (vat_rate / 100.0), 2)
    total_amount = round(subtotal + vat_amount, 2)
    
    code = f"PROP-2026-{random.randint(1000, 9999)}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO proposals (
            code, client_name, client_company, client_email, client_phone,
            title, description, validity_days, subtotal, vat_rate, vat_amount,
            total_amount, payment_terms, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Enviada')
    ''', (
        code, client_name, client_company, client_email, client_phone,
        title, description, validity_days, subtotal, vat_rate, vat_amount,
        total_amount, payment_terms
    ))
    
    prop_id = cursor.lastrowid
    
    # Insert items
    for item in items:
        qty = int(item.get('quantity', 1))
        price = float(item.get('unit_price', 0))
        tot = qty * price
        cursor.execute('''
            INSERT INTO proposal_items (proposal_id, service_title, description, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (prop_id, item.get('service_title', ''), item.get('description', ''), qty, price, tot))
        
    # Insert timeline
    for phase in timeline:
        cursor.execute('''
            INSERT INTO proposal_timeline (proposal_id, phase_name, duration_text, deliverables)
            VALUES (?, ?, ?, ?)
        ''', (prop_id, phase.get('phase_name', ''), phase.get('duration_text', ''), phase.get('deliverables', '')))
        
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'code': code,
        'prop_id': prop_id,
        'url': f'/proposal/{code}',
        'message': f'Proposta comercial {code} criada com sucesso!'
    })

@app.route('/api/proposals/sign', methods=['POST'])
def api_proposal_sign():
    data = request.json or {}
    code = data.get('code', '').strip()
    signed_by_name = data.get('signed_by_name', '').strip()
    signature_data = data.get('signature_data', '').strip()
    
    if not code or not signed_by_name or not signature_data:
        return jsonify({'success': False, 'message': 'Nome do assinante e assinatura digital são obrigatórios.'}), 400
        
    conn = get_db_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE proposals
        SET status = 'Aceite / Assinada', signature_data = ?, signed_at = ?, signed_by_name = ?
        WHERE code = ?
    ''', (signature_data, now_str, signed_by_name, code))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': f'Proposta {code} aceite e assinada digitalmente com sucesso por {signed_by_name}!'
    })

@app.route('/api/proposals/delete/<int:prop_id>', methods=['POST', 'DELETE'])
def api_proposal_delete(prop_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM proposals WHERE id = ?', (prop_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Proposta eliminada com sucesso.'})

if __name__ == '__main__':
    print("[SERVER] Generador de Propuestas Comerciales SaaS a iniciar na porta 6902...")
    app.run(host='0.0.0.0', port=6902, debug=False)
