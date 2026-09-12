import os
import sqlite3
import csv
import io
import uuid
import datetime
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/events')
def events():
    return render_template('events.html', active_page='events')

@app.route('/tickets')
def tickets():
    return render_template('tickets.html', active_page='tickets')

@app.route('/users')
def users():
    return render_template('users.html', active_page='users')

@app.route('/checkin')
def checkin():
    return render_template('checkin.html', active_page='checkin')

@app.route('/organizers')
def organizers():
    return render_template('organizers.html', active_page='organizers')

@app.route('/stats')
def stats():
    return render_template('stats.html', active_page='stats')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM events WHERE status = "Ativo"')
    active_events = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets')
    total_tickets_sold = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM tickets WHERE checkin_status LIKE "%Validado%"')
    total_checkins = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(price_paid) FROM tickets')
    total_revenue = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT COUNT(*) FROM organizers')
    total_organizers = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    conn.close()
    return jsonify({
        'active_events': active_events,
        'total_tickets_sold': total_tickets_sold,
        'total_checkins': total_checkins,
        'total_revenue': total_revenue,
        'total_organizers': total_organizers,
        'total_users': total_users
    })

# Events API
@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT events.*, organizers.company_name as organizer_company, organizers.name as organizer_name
        FROM events
        JOIN organizers ON events.organizer_id = organizers.id
        ORDER BY events.event_date ASC, events.event_time ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/events/create', methods=['POST'])
def create_event():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cap = int(data.get('total_capacity', 100))
    cursor.execute('''
        INSERT INTO events (title, category, organizer_id, venue_name, city, event_date, event_time, total_capacity, available_tickets, ticket_price, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'), data.get('category'), data.get('organizer_id'),
        data.get('venue_name'), data.get('city'), data.get('event_date'),
        data.get('event_time'), cap, cap, float(data.get('ticket_price', 0)), data.get('status', 'Ativo')
    ))
    conn.commit()
    eid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': eid, 'message': 'Evento publicado com sucesso!'}), 201

@app.route('/api/events/<int:eid>', methods=['DELETE'])
def delete_event(eid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (eid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Evento cancelado/eliminado.'})

# Organizers API
@app.route('/api/organizers', methods=['GET'])
def get_organizers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM organizers ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/organizers/create', methods=['POST'])
def create_organizer():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO organizers (name, company_name, email, phone, nif, verified_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('company_name'), data.get('email'),
            data.get('phone'), data.get('nif'), data.get('verified_status', 'Verificado')
        ))
        conn.commit()
        oid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': oid, 'message': 'Organizador/Promotor cadastrado!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: Email ou NIF já registado.'}), 400

@app.route('/api/organizers/<int:oid>', methods=['DELETE'])
def delete_organizer(oid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM organizers WHERE id = ?', (oid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Organizador removido.'})

# Users API
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/users/create', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, phone, nif)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('email'), data.get('phone'), data.get('nif')
        ))
        conn.commit()
        uid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': uid, 'message': 'Participante registado!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: Email ou NIF já registado.'}), 400

@app.route('/api/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (uid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Participante eliminado.'})

# Tickets API
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tickets.*, events.title as event_title, events.event_date, events.venue_name, users.name as user_name, users.phone as user_phone, users.nif as user_nif
        FROM tickets
        JOIN events ON tickets.event_id = events.id
        JOIN users ON tickets.user_id = users.id
        ORDER BY tickets.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/tickets/create', methods=['POST'])
def create_ticket():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    event_id = data.get('event_id')
    cursor.execute('SELECT ticket_price, available_tickets FROM events WHERE id = ?', (event_id,))
    erow = cursor.fetchone()
    if not erow or erow['available_tickets'] <= 0:
        conn.close()
        return jsonify({'success': False, 'message': 'Lotação esgotada ou evento inválido.'}), 400
    
    price = erow['ticket_price']
    code = f"TCK-EVT-{uuid.uuid4().hex[:6].upper()}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={code}"
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO tickets (event_id, user_id, ticket_code, qr_code_url, seat_category, price_paid, purchase_date, checkin_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pendente')
    ''', (
        event_id, data.get('user_id'), code, qr_url,
        data.get('seat_category', 'Geral / Plateia'), price, today
    ))
    
    # Update available tickets count
    cursor.execute('UPDATE events SET available_tickets = available_tickets - 1 WHERE id = ?', (event_id,))
    conn.commit()
    t_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': t_id, 'code': code, 'qr_url': qr_url, 'message': 'Bilhete emitido com sucesso!'}), 201

# Check-in API
@app.route('/api/tickets/checkin/<code>', methods=['POST'])
def process_checkin(code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tickets.*, events.title as event_title, users.name as user_name
        FROM tickets
        JOIN events ON tickets.event_id = events.id
        JOIN users ON tickets.user_id = users.id
        WHERE tickets.ticket_code = ? OR tickets.id = ?
    ''', (code, code))
    ticket = cursor.fetchone()

    if not ticket:
        conn.close()
        return jsonify({'success': False, 'message': 'Bilhete INVÁLIDO ou inexistente.'}), 404

    if ticket['checkin_status'].startswith('Validado'):
        conn.close()
        return jsonify({'success': False, 'message': f'AVISO: Bilhete JÁ UTILIZADO em {ticket["checkin_time"]}. Entrada Recusada!'}), 400

    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE tickets SET checkin_status = "Validado (Check-in Efetuado)", checkin_time = ? WHERE id = ?', (now_str, ticket['id']))
    
    # Log check-in entry
    cursor.execute('''
        INSERT INTO checkin_logs (ticket_id, gate_number, validator_name, status_result)
        VALUES (?, 'Porta Principal A1', 'Staff EventCraft', 'VÁLIDO - Entrada Autorizada')
    ''', (ticket['id'],))
    conn.commit()
    conn.close()
    return jsonify({
        'success': True,
        'ticket': dict(ticket),
        'message': f'✅ CHECK-IN CONFIRMADO! Bem-vindo, {ticket["user_name"]} ({ticket["event_title"]})!'
    })

@app.route('/api/tickets/<int:tid>', methods=['DELETE'])
def delete_ticket(tid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tickets WHERE id = ?', (tid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Bilhete cancelado.'})

# Checkin Logs API
@app.route('/api/checkin_logs', methods=['GET'])
def get_checkin_logs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT checkin_logs.*, tickets.ticket_code, events.title as event_title, users.name as user_name
        FROM checkin_logs
        JOIN tickets ON checkin_logs.ticket_id = tickets.id
        JOIN events ON tickets.event_id = events.id
        JOIN users ON tickets.user_id = users.id
        ORDER BY checkin_logs.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Export API
@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tickets.ticket_code as Codigo_Bilhete, users.name as Participante, users.nif as NIF,
               events.title as Evento, tickets.seat_category as Categoria, tickets.price_paid as Valor_EUR,
               tickets.checkin_status as Estado_Checkin
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        JOIN events ON tickets.event_id = events.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_eventcraft.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando EventCraft AI SaaS no servidor local porta 6936...")
    app.run(host='0.0.0.0', port=6936, debug=True)
