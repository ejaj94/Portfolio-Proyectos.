import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'warrantycraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_days_remaining(expiration_date_str):
    try:
        exp_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
        today = date.today()
        diff = (exp_date - today).days
        return diff
    except Exception:
        return 0

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Metrics
    cursor.execute("SELECT COUNT(*) as cnt FROM warranties WHERE status = 'Ativa'")
    active_warranties = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM warranties WHERE status = 'Prestes a Expirar'")
    expiring_soon = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM incidents WHERE status IN ('Aberto', 'Em Reparação', 'Em Testes')")
    open_rma_claims = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM clients")
    total_clients = cursor.fetchone()['cnt']

    # Recent Warranties List
    cursor.execute("""
    SELECT w.*, c.company_name, c.contact_name, p.product_name, p.brand, p.model_code
    FROM warranties w
    JOIN clients c ON w.client_id = c.id
    JOIN products p ON w.product_id = p.id
    ORDER BY w.id DESC
    LIMIT 5
    """)
    recent_warranties = [dict(r) for r in cursor.fetchall()]
    for w in recent_warranties:
        w['days_left'] = calculate_days_remaining(w['expiration_date'])

    # Recent Incidents / RMA Claims
    cursor.execute("""
    SELECT i.*, w.warranty_code, w.serial_number, p.product_name, c.company_name
    FROM incidents i
    JOIN warranties w ON i.warranty_id = w.id
    JOIN products p ON w.product_id = p.id
    JOIN clients c ON w.client_id = c.id
    ORDER BY i.id DESC
    LIMIT 4
    """)
    recent_incidents = [dict(r) for r in cursor.fetchall()]

    # Dropdowns for Modal
    cursor.execute("SELECT id, company_name FROM clients ORDER BY company_name ASC")
    clients_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, product_name, brand, default_warranty_months FROM products ORDER BY product_name ASC")
    products_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT w.id, w.warranty_code, w.serial_number, p.product_name, c.company_name FROM warranties w JOIN products p ON w.product_id = p.id JOIN clients c ON w.client_id = c.id ORDER BY w.id DESC")
    warranties_list = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        active_warranties=active_warranties,
        expiring_soon=expiring_soon,
        open_rma_claims=open_rma_claims,
        total_clients=total_clients,
        recent_warranties=recent_warranties,
        recent_incidents=recent_incidents,
        clients_list=clients_list,
        products_list=products_list,
        warranties_list=warranties_list
    )

@app.route('/warranties')
def warranties_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT w.*, c.company_name, c.contact_name, p.product_name, p.brand, p.model_code
    FROM warranties w
    JOIN clients c ON w.client_id = c.id
    JOIN products p ON w.product_id = p.id
    WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND w.status = ?"
        params.append(status_filter)

    if search_q:
        query += " AND (w.warranty_code LIKE ? OR w.serial_number LIKE ? OR c.company_name LIKE ? OR p.product_name LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " ORDER BY w.id DESC"
    cursor.execute(query, params)
    warranties = [dict(r) for r in cursor.fetchall()]

    for w in warranties:
        w['days_left'] = calculate_days_remaining(w['expiration_date'])

    conn.close()
    return render_template('warranties.html', warranties=warranties, selected_status=status_filter, search_q=search_q)

@app.route('/warranty/<int:warranty_id>')
def warranty_detail(warranty_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT w.*, c.company_name, c.contact_name, c.email as client_email, c.phone as client_phone, c.nif_vat,
           p.product_name, p.brand, p.model_code, p.category
    FROM warranties w
    JOIN clients c ON w.client_id = c.id
    JOIN products p ON w.product_id = p.id
    WHERE w.id = ?
    """, (warranty_id,))
    w_row = cursor.fetchone()

    if not w_row:
        conn.close()
        return redirect(url_for('warranties_page'))

    warranty = dict(w_row)
    warranty['days_left'] = calculate_days_remaining(warranty['expiration_date'])

    # Linked RMA Incidents
    cursor.execute("SELECT * FROM incidents WHERE warranty_id = ? ORDER BY id DESC", (warranty_id,))
    incidents = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('warranty_detail.html', warranty=warranty, incidents=incidents)

@app.route('/products')
def products_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.*, COUNT(w.id) as registered_warranties
    FROM products p
    LEFT JOIN warranties w ON p.id = w.product_id
    GROUP BY p.id
    ORDER BY p.id DESC
    """)
    products = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('products.html', products=products)

@app.route('/clients')
def clients_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.*, COUNT(w.id) as warranty_count
    FROM clients c
    LEFT JOIN warranties w ON c.id = w.client_id
    GROUP BY c.id
    ORDER BY c.id DESC
    """)
    clients = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('clients.html', clients=clients)

@app.route('/incidents')
def incidents_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    query = """
    SELECT i.*, w.warranty_code, w.serial_number, p.product_name, c.company_name
    FROM incidents i
    JOIN warranties w ON i.warranty_id = w.id
    JOIN products p ON w.product_id = p.id
    JOIN clients c ON w.client_id = c.id
    WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND i.status = ?"
        params.append(status_filter)

    query += " ORDER BY i.id DESC"
    cursor.execute(query, params)
    incidents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT w.id, w.warranty_code, w.serial_number, p.product_name, c.company_name FROM warranties w JOIN products p ON w.product_id = p.id JOIN clients c ON w.client_id = c.id ORDER BY w.id DESC")
    warranties_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('incidents.html', incidents=incidents, selected_status=status_filter, warranties_list=warranties_list)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT l.*, i.incident_code, w.warranty_code, p.product_name
    FROM intervention_logs l
    JOIN incidents i ON l.incident_id = i.id
    JOIN warranties w ON i.warranty_id = w.id
    JOIN products p ON w.product_id = p.id
    ORDER BY l.id DESC
    """)
    logs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('history.html', logs=logs)

# API ENDPOINTS

@app.route('/api/warranty/register', methods=['POST'])
def api_register_warranty():
    try:
        data = request.get_json() or {}
        client_id = data.get('client_id')
        product_id = data.get('product_id')
        serial_number = data.get('serial_number', '').strip().upper()
        purchase_date_str = data.get('purchase_date', '').strip()
        months = int(data.get('warranty_months', 24))
        notes = data.get('notes', '').strip()

        if not client_id or not product_id or not serial_number or not purchase_date_str:
            return jsonify({'success': False, 'message': 'Preencha o cliente, produto, número de série e data de compra.'}), 400

        p_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()
        exp_date = p_date + timedelta(days=months * 30.4375)
        exp_date_str = exp_date.strftime("%Y-%m-%d")

        today = date.today()
        days_left = (exp_date - today).days

        if days_left <= 0:
            status = 'Expirada'
        elif days_left <= 60:
            status = 'Prestes a Expirar'
        else:
            status = 'Ativa'

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM warranties")
        code_num = cursor.fetchone()['cnt'] + 105
        warranty_code = f"GAR-2026-{code_num}"

        cursor.execute("""
        INSERT INTO warranties (warranty_code, client_id, product_id, serial_number, purchase_date, expiration_date, warranty_months, status, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (warranty_code, client_id, product_id, serial_number, purchase_date_str, exp_date_str, months, status, notes, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Garantia "{warranty_code}" registada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/incident/create', methods=['POST'])
def api_create_incident():
    try:
        data = request.get_json() or {}
        warranty_id = data.get('warranty_id')
        fault_description = data.get('fault_description', '').strip()
        severity = data.get('severity', 'Média')
        technician = data.get('assigned_technician', 'Enmanuel Jimenez').strip()

        if not warranty_id or not fault_description:
            return jsonify({'success': False, 'message': 'Selecione a garantia e descreva a avaria.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM incidents")
        code_num = cursor.fetchone()['cnt'] + 8804
        incident_code = f"RMA-{code_num}"

        cursor.execute("""
        INSERT INTO incidents (incident_code, warranty_id, fault_description, severity, status, assigned_technician, opened_date, resolved_date)
        VALUES (?, ?, ?, ?, 'Em Reparação', ?, ?, NULL)
        """, (incident_code, warranty_id, fault_description, severity, technician, now_str))

        incident_id = cursor.lastrowid

        # Add initial intervention log
        cursor.execute("""
        INSERT INTO intervention_logs (incident_id, action, technician, timestamp, notes)
        VALUES (?, 'Abertura de Chamado RMA & Atribuição de Técnico', ?, ?, ?)
        """, (incident_id, technician, now_str, f"Incidência iniciada com severidade {severity}."))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Incidência RMA "{incident_code}" aberta com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/incident/status/<int:incident_id>', methods=['POST'])
def api_update_incident_status(incident_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Concluído')
        technician = data.get('technician', 'Enmanuel Jimenez')
        notes = data.get('notes', 'Atualização de estado técnica.').strip()

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        resolved_date = now_str if new_status in ['Concluído', 'Substituído'] else None

        cursor.execute("""
        UPDATE incidents SET status = ?, resolved_date = COALESCE(?, resolved_date) WHERE id = ?
        """, (new_status, resolved_date, incident_id))

        cursor.execute("""
        INSERT INTO intervention_logs (incident_id, action, technician, timestamp, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (incident_id, f"Estado Alterado para '{new_status}'", technician, now_str, notes))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Incidência alterada para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT w.warranty_code, c.company_name, p.product_name, p.brand, w.serial_number, w.purchase_date, w.expiration_date, w.status
    FROM warranties w
    JOIN clients c ON w.client_id = c.id
    JOIN products p ON w.product_id = p.id
    ORDER BY w.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        return Response(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=warrantycraft_export.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Código Garantia', 'Empresa / Cliente', 'Produto', 'Marca', 'Nº Série', 'Data Compra', 'Expiração', 'Estado'])
        for r in rows:
            writer.writerow([r['warranty_code'], r['company_name'], r['product_name'], r['brand'], r['serial_number'], r['purchase_date'], r['expiration_date'], r['status']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=warrantycraft_export.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6928, debug=True)
