import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'quotecraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Metrics Calculations
    cursor.execute("SELECT COUNT(*) as cnt FROM quotes")
    total_quotes = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM quotes WHERE status IN ('Aprovado', 'Faturado')")
    approved_count = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(total_amount) as sum_total FROM quotes")
    total_quoted_val = cursor.fetchone()['sum_total'] or 0.0

    cursor.execute("SELECT SUM(total_amount) as sum_approved FROM quotes WHERE status IN ('Aprovado', 'Faturado')")
    approved_val = cursor.fetchone()['sum_approved'] or 0.0

    cursor.execute("SELECT COUNT(*) as cnt FROM clients")
    total_clients = cursor.fetchone()['cnt']

    conversion_rate = round((approved_count / total_quotes * 100), 1) if total_quotes > 0 else 0.0

    # Recent Quotes List
    cursor.execute("""
    SELECT q.*, c.company_name, c.full_name as client_name
    FROM quotes q
    JOIN clients c ON q.client_id = c.id
    ORDER BY q.id DESC
    LIMIT 6
    """)
    recent_quotes = [dict(r) for r in cursor.fetchall()]

    # Catalog Items
    cursor.execute("SELECT * FROM items ORDER BY id ASC LIMIT 5")
    catalog_items = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        total_quotes=total_quotes,
        approved_count=approved_count,
        total_quoted_val=total_quoted_val,
        approved_val=approved_val,
        total_clients=total_clients,
        conversion_rate=conversion_rate,
        recent_quotes=recent_quotes,
        catalog_items=catalog_items
    )

@app.route('/quotes')
def quotes_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    query = """
    SELECT q.*, c.company_name, c.full_name as client_name, c.vat_nif
    FROM quotes q
    JOIN clients c ON q.client_id = c.id
    WHERE 1=1
    """
    params = []
    if status_filter:
        query += " AND q.status = ?"
        params.append(status_filter)

    query += " ORDER BY q.id DESC"
    cursor.execute(query, params)
    quotes = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, company_name, full_name FROM clients ORDER BY company_name ASC")
    clients = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM items ORDER BY item_name ASC")
    items = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('quotes.html', quotes=quotes, clients=clients, items=items, selected_status=status_filter)

@app.route('/quote/<int:quote_id>')
def quote_detail(quote_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT q.*, c.company_name, c.full_name as client_name, c.email as client_email, c.phone as client_phone, c.vat_nif, c.address
    FROM quotes q
    JOIN clients c ON q.client_id = c.id
    WHERE q.id = ?
    """, (quote_id,))
    q_row = cursor.fetchone()

    if not q_row:
        conn.close()
        return redirect(url_for('quotes_page'))

    quote = dict(q_row)

    # Quote Line Items
    cursor.execute("SELECT * FROM quote_items WHERE quote_id = ? ORDER BY id ASC", (quote_id,))
    quote_items = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('quote_detail.html', quote=quote, quote_items=quote_items)

@app.route('/clients')
def clients_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.*, COUNT(q.id) as quote_count, COALESCE(SUM(q.total_amount), 0) as total_spent
    FROM clients c
    LEFT JOIN quotes q ON c.id = q.client_id
    GROUP BY c.id
    ORDER BY c.id DESC
    """)
    clients = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('clients.html', clients=clients)

@app.route('/items')
def items_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items ORDER BY id ASC")
    items = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('items.html', items=items)

# API ENDPOINTS

@app.route('/api/quote/save', methods=['POST'])
def api_save_quote():
    try:
        data = request.get_json() or {}
        client_id = data.get('client_id')
        discount_percent = float(data.get('discount_percent', 0.0))
        vat_rate = float(data.get('vat_rate', 23.0))
        notes = data.get('notes', '').strip()
        items_data = data.get('items', [])

        if not client_id or not items_data:
            return jsonify({'success': False, 'message': 'Selecione o cliente e adicione pelo menos um item.'}), 400

        subtotal = 0.0
        line_items = []
        for it in items_data:
            name = it.get('item_name', '').strip()
            qty = int(it.get('quantity', 1))
            price = float(it.get('unit_price', 0.0))
            l_total = round(qty * price, 2)
            subtotal += l_total
            line_items.append((name, qty, price, l_total))

        # Calculate discount and tax
        discount_val = round(subtotal * (discount_percent / 100.0), 2)
        discounted_subtotal = subtotal - discount_val
        tax_amount = round(discounted_subtotal * (vat_rate / 100.0), 2)
        total_amount = round(discounted_subtotal + tax_amount, 2)

        today_str = date.today().strftime("%Y-%m-%d")
        valid_date = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = get_db()
        cursor = conn.cursor()

        # Generate quote number
        cursor.execute("SELECT COUNT(*) as cnt FROM quotes")
        cnt = cursor.fetchone()['cnt'] + 1
        quote_number = f"ORC-2026-{cnt:03d}"

        cursor.execute("""
        INSERT INTO quotes (quote_number, client_id, status, issue_date, valid_until, discount_percent, vat_rate, subtotal, tax_amount, total_amount, notes, created_at)
        VALUES (?, ?, 'Enviado', ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (quote_number, client_id, today_str, valid_date, discount_percent, vat_rate, subtotal, tax_amount, total_amount, notes, now_str))

        quote_id = cursor.lastrowid

        for li in line_items:
            cursor.execute("""
            INSERT INTO quote_items (quote_id, item_name, quantity, unit_price, line_total)
            VALUES (?, ?, ?, ?, ?)
            """, (quote_id, li[0], li[1], li[2], li[3]))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'quote_id': quote_id, 'message': f'Orçamento "{quote_number}" gerado com sucesso! Total: {total_amount:.2f} €'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/quote/status/<int:quote_id>', methods=['POST'])
def api_update_quote_status(quote_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Aprovado')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE quotes SET status = ? WHERE id = ?", (new_status, quote_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Estado do orçamento alterado para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/client/save', methods=['POST'])
def api_save_client():
    try:
        data = request.get_json() or {}
        company_name = data.get('company_name', '').strip()
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        vat_nif = data.get('vat_nif', '').strip()
        address = data.get('address', '').strip()

        if not all([company_name, email, vat_nif]):
            return jsonify({'success': False, 'message': 'Preencha a empresa, e-mail e NIF.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clients (company_name, full_name, email, phone, vat_nif, address, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company_name, full_name, email, phone, vat_nif, address, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Cliente "{company_name}" registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/item/save', methods=['POST'])
def api_save_item():
    try:
        data = request.get_json() or {}
        item_name = data.get('item_name', '').strip()
        category = data.get('category', 'Serviço')
        unit_price = float(data.get('unit_price', 0.0))
        description = data.get('description', '').strip()

        if not item_name or unit_price <= 0:
            return jsonify({'success': False, 'message': 'Preencha o nome do item e o preço unitário.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO items (item_name, category, unit_price, description, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (item_name, category, unit_price, description, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Item "{item_name}" adicionado ao catálogo!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_quotes(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT q.quote_number, c.company_name, c.vat_nif, q.issue_date, q.valid_until, q.subtotal, q.vat_rate, q.tax_amount, q.total_amount, q.status
    FROM quotes q
    JOIN clients c ON q.client_id = c.id
    ORDER BY q.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=relatorio_orcamentos_quotecraft.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Nº Orçamento', 'Cliente / Empresa', 'NIF / VAT', 'Data Emissão', 'Validade', 'Subtotal (€)', 'Taxa IVA (%)', 'Valor IVA (€)', 'Total (€)', 'Estado'])

        for r in rows:
            writer.writerow([r['quote_number'], r['company_name'], r['vat_nif'], r['issue_date'], r['valid_until'], f"{r['subtotal']:.2f}", f"{r['vat_rate']:.1f}", f"{r['tax_amount']:.2f}", f"{r['total_amount']:.2f}", r['status']])

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=relatorio_orcamentos_quotecraft.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - QuoteCraft AI SaaS na porta 6924...")
    app.run(host='127.0.0.1', port=6924, debug=False, use_reloader=False)
