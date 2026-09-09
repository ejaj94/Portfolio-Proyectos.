import os
import sqlite3
import json
import csv
import io
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'bookings.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def slugify(text):
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text or 'servico-sem-titulo'

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all bookings joined with service data
    cursor.execute("""
    SELECT b.*, s.name as service_name, s.duration_min, s.price, s.color as service_color
    FROM bookings b
    JOIN services s ON b.service_id = s.id
    ORDER BY b.booking_date DESC, b.booking_time ASC
    """)
    bookings_raw = cursor.fetchall()

    bookings = [dict(r) for r in bookings_raw]

    # Calculate metrics
    total_bookings = len(bookings)
    confirmed_bookings = sum(1 for b in bookings if b['status'] == 'Confirmado')
    total_revenue = sum(b['price'] for b in bookings if b['status'] == 'Confirmado')

    # Get services count
    cursor.execute("SELECT COUNT(*) as cnt FROM services")
    total_services = cursor.fetchone()['cnt']

    conn.close()

    return render_template(
        'dashboard.html',
        bookings=bookings,
        total_bookings=total_bookings,
        confirmed_bookings=confirmed_bookings,
        total_revenue=total_revenue,
        total_services=total_services
    )

@app.route('/services')
def services_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services ORDER BY id ASC")
    services = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return render_template('services.html', services=services)

@app.route('/book/<slug>')
def public_booking_page(slug):
    conn = get_db()
    cursor = conn.cursor()
    
    # Selected main service or service list
    cursor.execute("SELECT * FROM services WHERE slug = ?", (slug,))
    service_row = cursor.fetchone()

    cursor.execute("SELECT * FROM services ORDER BY id ASC")
    all_services = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not service_row and all_services:
        service_row = all_services[0]

    if not service_row:
        return render_template('public_booking.html', error="Nenhum serviço disponível."), 404

    service_dict = dict(service_row)
    today_str = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        'public_booking.html',
        current_service=service_dict,
        all_services=all_services,
        today_date=today_str
    )

@app.route('/api/available-slots')
def api_available_slots():
    service_id = request.args.get('service_id')
    date_str = request.args.get('date')

    if not service_id or not date_str:
        return jsonify({'slots': []})

    conn = get_db()
    cursor = conn.cursor()

    # Get service duration
    cursor.execute("SELECT duration_min FROM services WHERE id = ?", (service_id,))
    s_row = cursor.fetchone()
    if not s_row:
        conn.close()
        return jsonify({'slots': []})

    duration = s_row['duration_min']

    # Get existing booked times for this date
    cursor.execute("""
    SELECT booking_time FROM bookings
    WHERE service_id = ? AND booking_date = ? AND status != 'Cancelado'
    """, (service_id, date_str))
    booked_times = set(r['booking_time'] for r in cursor.fetchall())
    conn.close()

    # Generate slots between 09:00 and 18:00
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    current = start_time

    available_slots = []
    while current + timedelta(minutes=duration) <= end_time:
        slot_str = current.strftime("%H:%M")
        available_slots.append({
            'time': slot_str,
            'available': slot_str not in booked_times
        })
        current += timedelta(minutes=30 if duration <= 30 else 45 if duration == 45 else 60)

    return jsonify({'slots': available_slots})

@app.route('/book/<slug>/submit', methods=['POST'])
def public_booking_submit(slug):
    try:
        service_id = request.form.get('service_id')
        client_name = request.form.get('client_name', '').strip()
        client_email = request.form.get('client_email', '').strip()
        client_phone = request.form.get('client_phone', '').strip()
        booking_date = request.form.get('booking_date', '').strip()
        booking_time = request.form.get('booking_time', '').strip()
        notes = request.form.get('notes', '').strip()

        if not all([service_id, client_name, client_email, client_phone, booking_date, booking_time]):
            return jsonify({'success': False, 'message': 'Por favor preencha todos os campos obrigatórios.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = get_db()
        cursor = conn.cursor()

        # Check collision
        cursor.execute("""
        SELECT id FROM bookings
        WHERE service_id = ? AND booking_date = ? AND booking_time = ? AND status != 'Cancelado'
        """, (service_id, booking_date, booking_time))

        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Este horário já se encontra reservado. Por favor escolha outro.'}), 400

        cursor.execute("""
        INSERT INTO bookings (service_id, client_name, client_email, client_phone, booking_date, booking_time, status, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'Confirmado', ?, ?)
        """, (service_id, client_name, client_email, client_phone, booking_date, booking_time, notes, now_str))

        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'message': f'Reserva confirmada com sucesso para {booking_date} às {booking_time}!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/booking/status/<int:booking_id>', methods=['POST'])
def api_update_booking_status(booking_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Confirmado')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (new_status, booking_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Estado alterado para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/booking/export/<fmt>')
def api_export_bookings(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT b.*, s.name as service_name, s.price
    FROM bookings b
    JOIN services s ON b.service_id = s.id
    ORDER BY b.booking_date ASC, b.booking_time ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=agenda_agendamentos.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID Reserva', 'Serviço', 'Preço (€)', 'Cliente', 'E-mail', 'Telefone', 'Data', 'Hora', 'Estado', 'Notas'])

        for r in rows:
            writer.writerow([r['id'], r['service_name'], f"{r['price']:.2f}", r['client_name'], r['client_email'], r['client_phone'], r['booking_date'], r['booking_time'], r['status'], r['notes']])

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=agenda_agendamentos.csv'}
        )

@app.route('/api/service/save', methods=['POST'])
def api_save_service():
    try:
        data = request.get_json() or {}
        s_id = data.get('id')
        name = data.get('name', 'Novo Serviço').strip()
        description = data.get('description', '').strip()
        duration_min = int(data.get('duration_min', 45))
        price = float(data.get('price', 0.0))
        category = data.get('category', 'Geral').strip()
        color = data.get('color', '#DC2626').strip()

        if not name:
            return jsonify({'success': False, 'message': 'O nome do serviço é obrigatório.'}), 400

        base_slug = slugify(name)
        conn = get_db()
        cursor = conn.cursor()

        if s_id:
            cursor.execute("""
            UPDATE services
            SET name = ?, description = ?, duration_min = ?, price = ?, category = ?, color = ?
            WHERE id = ?
            """, (name, description, duration_min, price, category, color, s_id))
        else:
            slug = base_slug
            counter = 1
            while True:
                cursor.execute("SELECT id FROM services WHERE slug = ?", (slug,))
                if not cursor.fetchone():
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1

            cursor.execute("""
            INSERT INTO services (name, slug, description, duration_min, price, category, color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, slug, description, duration_min, price, category, color))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Serviço "{name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/service/delete/<int:service_id>', methods=['POST', 'DELETE'])
def api_delete_service(service_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
        cursor.execute("DELETE FROM bookings WHERE service_id = ?", (service_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Serviço e agendamentos associados eliminados.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - BookCraft AI SaaS na porta 6919...")
    app.run(host='127.0.0.1', port=6919, debug=False, use_reloader=False)
