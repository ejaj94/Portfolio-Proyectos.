import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'realtycraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/showcase')
def showcase():
    return render_template('showcase.html')

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()


    # Metrics Calculations
    cursor.execute("SELECT COUNT(*) as cnt FROM properties WHERE status = 'Disponível'")
    active_properties = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(price) as total_val FROM properties WHERE status != 'Vendido'")
    total_portfolio_value = cursor.fetchone()['total_val'] or 0.0

    cursor.execute("SELECT COUNT(*) as cnt FROM clients")
    total_clients = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM leads WHERE status != 'Fechado' AND status != 'Cancelado'")
    active_leads = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM visits WHERE status = 'Agendada'")
    scheduled_visits = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM offers WHERE status = 'Pendente'")
    pending_offers = cursor.fetchone()['cnt']

    # Recent Leads
    cursor.execute("""
    SELECT l.*, p.title as property_title
    FROM leads l
    LEFT JOIN properties p ON l.property_id = p.id
    ORDER BY l.id DESC
    LIMIT 5
    """)
    recent_leads = [dict(r) for r in cursor.fetchall()]

    # Featured Properties
    cursor.execute("SELECT * FROM properties ORDER BY price DESC LIMIT 4")
    featured_properties = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        active_properties=active_properties,
        total_portfolio_value=total_portfolio_value,
        total_clients=total_clients,
        active_leads=active_leads,
        scheduled_visits=scheduled_visits,
        pending_offers=pending_offers,
        recent_leads=recent_leads,
        featured_properties=featured_properties
    )

@app.route('/properties')
def properties_page():
    conn = get_db()
    cursor = conn.cursor()

    type_filter = request.args.get('type')
    status_filter = request.args.get('status')
    search_q = request.args.get('q', '').strip()

    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if type_filter:
        query += " AND property_type = ?"
        params.append(type_filter)
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
    if search_q:
        query += " AND (title LIKE ? OR city LIKE ? OR address LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    properties = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('properties.html', properties=properties, selected_type=type_filter, selected_status=status_filter, search_q=search_q)

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties WHERE id = ?", (property_id,))
    p_row = cursor.fetchone()
    if not p_row:
        conn.close()
        return redirect(url_for('properties_page'))

    prop = dict(p_row)

    # Leads for this property
    cursor.execute("SELECT * FROM leads WHERE property_id = ? ORDER BY id DESC", (property_id,))
    leads = [dict(r) for r in cursor.fetchall()]

    # Visits for this property
    cursor.execute("""
    SELECT v.*, c.full_name as client_name
    FROM visits v
    JOIN clients c ON v.client_id = c.id
    WHERE v.property_id = ?
    ORDER BY v.visit_date DESC
    """, (property_id,))
    visits = [dict(r) for r in cursor.fetchall()]

    # Offers for this property
    cursor.execute("""
    SELECT o.*, c.full_name as client_name, c.phone as client_phone
    FROM offers o
    JOIN clients c ON o.client_id = c.id
    WHERE o.property_id = ?
    ORDER BY o.offer_date DESC
    """, (property_id,))
    offers = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, full_name FROM clients ORDER BY full_name ASC")
    clients = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('property_detail.html', property=prop, leads=leads, visits=visits, offers=offers, clients=clients)

@app.route('/clients')
def clients_page():
    conn = get_db()
    cursor = conn.cursor()

    type_filter = request.args.get('type')
    query = "SELECT * FROM clients WHERE 1=1"
    params = []
    if type_filter:
        query += " AND client_type = ?"
        params.append(type_filter)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    clients = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('clients.html', clients=clients, selected_type=type_filter)

@app.route('/pipeline')
def pipeline_page():
    conn = get_db()
    cursor = conn.cursor()

    stages = ['Novo Lead', 'Em Contacto', 'Visita Agendada', 'Proposta', 'Fechado']
    pipeline_data = {}

    for stage in stages:
        cursor.execute("""
        SELECT l.*, p.title as property_title
        FROM leads l
        LEFT JOIN properties p ON l.property_id = p.id
        WHERE l.status = ?
        ORDER BY l.id DESC
        """, (stage,))
        pipeline_data[stage] = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('pipeline.html', pipeline_data=pipeline_data, stages=stages)

@app.route('/visits')
def visits_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT v.*, p.title as property_title, p.address as property_address, c.full_name as client_name, c.phone as client_phone
    FROM visits v
    JOIN properties p ON v.property_id = p.id
    JOIN clients c ON v.client_id = c.id
    ORDER BY v.visit_date DESC, v.visit_time ASC
    """)
    visits = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, title FROM properties WHERE status = 'Disponível' ORDER BY title ASC")
    properties = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, full_name FROM clients ORDER BY full_name ASC")
    clients = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('visits.html', visits=visits, properties=properties, clients=clients)

@app.route('/offers')
def offers_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT o.*, p.title as property_title, p.price as property_price, c.full_name as client_name, c.email as client_email, c.phone as client_phone
    FROM offers o
    JOIN properties p ON o.property_id = p.id
    JOIN clients c ON o.client_id = c.id
    ORDER BY o.offer_date DESC
    """)
    offers = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, title, price FROM properties WHERE status != 'Vendido' ORDER BY title ASC")
    properties = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, full_name FROM clients ORDER BY full_name ASC")
    clients = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('offers.html', offers=offers, properties=properties, clients=clients)

# API ENDPOINTS

@app.route('/api/property/save', methods=['POST'])
def api_save_property():
    try:
        data = request.get_json() or {}
        p_id = data.get('id')
        title = data.get('title', '').strip()
        property_type = data.get('property_type', 'Apartamento')
        address = data.get('address', '').strip()
        city = data.get('city', '').strip()
        price = float(data.get('price', 0.0))
        bedrooms = int(data.get('bedrooms', 1))
        bathrooms = int(data.get('bathrooms', 1))
        area_sqm = float(data.get('area_sqm', 0.0))
        status = data.get('status', 'Disponível')
        agent_name = data.get('agent_name', 'Enmanuel Jimenez').strip()

        icon_map = {
            'Apartamento': 'fa-building',
            'Moradia': 'fa-house-chimney',
            'Escritório': 'fa-briefcase',
            'Loja': 'fa-store',
            'Terreno': 'fa-mountain-sun'
        }
        image_icon = icon_map.get(property_type, 'fa-building')

        if not all([title, address, city, price]):
            return jsonify({'success': False, 'message': 'Por favor preencha todos os campos obrigatórios.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        if p_id:
            cursor.execute("""
            UPDATE properties
            SET title = ?, property_type = ?, address = ?, city = ?, price = ?, bedrooms = ?, bathrooms = ?, area_sqm = ?, status = ?, image_icon = ?, agent_name = ?
            WHERE id = ?
            """, (title, property_type, address, city, price, bedrooms, bathrooms, area_sqm, status, image_icon, agent_name, p_id))
        else:
            cursor.execute("""
            INSERT INTO properties (title, property_type, address, city, price, bedrooms, bathrooms, area_sqm, status, image_icon, agent_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, property_type, address, city, price, bedrooms, bathrooms, area_sqm, status, image_icon, agent_name, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Imóvel "{title}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/client/save', methods=['POST'])
def api_save_client():
    try:
        data = request.get_json() or {}
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        client_type = data.get('client_type', 'Comprador')
        budget_max = float(data.get('budget_max', 0.0))
        preferred_type = data.get('preferred_type', 'Apartamento')

        if not all([full_name, email, phone]):
            return jsonify({'success': False, 'message': 'Preencha o nome, e-mail e telefone do cliente.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clients (full_name, email, phone, client_type, budget_max, preferred_type, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'Ativo', ?)
        """, (full_name, email, phone, client_type, budget_max, preferred_type, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Cliente "{full_name}" cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/lead/save', methods=['POST'])
def api_save_lead():
    try:
        data = request.get_json() or {}
        client_name = data.get('client_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        property_id = data.get('property_id')
        source = data.get('source', 'Website')
        notes = data.get('notes', '').strip()

        if not all([client_name, email, phone]):
            return jsonify({'success': False, 'message': 'Preencha os dados do potencial comprador.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO leads (client_name, email, phone, property_id, source, status, notes, created_at)
        VALUES (?, ?, ?, ?, ?, 'Novo Lead', ?, ?)
        """, (client_name, email, phone, property_id, source, notes, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Lead imobiliário registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/lead/status/<int:lead_id>', methods=['POST'])
def api_update_lead_status(lead_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Em Contacto')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (new_status, lead_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Etapa do lead alterada para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/visit/save', methods=['POST'])
def api_save_visit():
    try:
        data = request.get_json() or {}
        property_id = data.get('property_id')
        client_id = data.get('client_id')
        visit_date = data.get('visit_date')
        visit_time = data.get('visit_time')
        agent_name = data.get('agent_name', 'Enmanuel Jimenez').strip()
        notes = data.get('notes', '').strip()

        if not all([property_id, client_id, visit_date, visit_time]):
            return jsonify({'success': False, 'message': 'Selecione o imóvel, cliente, data e hora da visita.'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO visits (property_id, client_id, visit_date, visit_time, agent_name, status, notes)
        VALUES (?, ?, ?, ?, ?, 'Agendada', ?)
        """, (property_id, client_id, visit_date, visit_time, agent_name, notes))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Visita ao imóvel agendada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/offer/save', methods=['POST'])
def api_save_offer():
    try:
        data = request.get_json() or {}
        property_id = data.get('property_id')
        client_id = data.get('client_id')
        offer_amount = float(data.get('offer_amount', 0.0))
        notes = data.get('notes', '').strip()

        if not all([property_id, client_id, offer_amount]):
            return jsonify({'success': False, 'message': 'Selecione o imóvel, cliente e valor da proposta.'}), 400

        today_str = date.today().strftime("%Y-%m-%d")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO offers (property_id, client_id, offer_amount, status, offer_date, notes)
        VALUES (?, ?, ?, 'Pendente', ?, ?)
        """, (property_id, client_id, offer_amount, today_str, notes))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Proposta de compra registada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/offer/status/<int:offer_id>', methods=['POST'])
def api_update_offer_status(offer_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Aceita')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE offers SET status = ? WHERE id = ?", (new_status, offer_id))

        if new_status == 'Aceita':
            cursor.execute("SELECT property_id FROM offers WHERE id = ?", (offer_id,))
            o = cursor.fetchone()
            if o:
                cursor.execute("UPDATE properties SET status = 'Reservado' WHERE id = ?", (o['property_id'],))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Proposta alterada para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_realty(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.id, p.title, p.property_type, p.address, p.city, p.price, p.status, p.agent_name
    FROM properties p
    ORDER BY p.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=portafolio_imoveis_realtycraft.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID Imóvel', 'Título', 'Tipo', 'Morada', 'Cidade', 'Preço (€)', 'Estado', 'Consultor'])

        for r in rows:
            writer.writerow([r['id'], r['title'], r['property_type'], r['address'], r['city'], f"{r['price']:.2f}", r['status'], r['agent_name']])

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=portafolio_imoveis_realtycraft.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - RealtyCraft AI SaaS na porta 6970...")
    app.run(host='127.0.0.1', port=6970, debug=False, use_reloader=False)

