import os
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'ejajtech_sunset_travel_secret_2026'

# Inicializar BD
database.init_db()

@app.route('/')
def index():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Buscar viagens ativas
    cursor.execute('''
        SELECT t.*, d.name as dest_name, d.country as dest_country, d.weather as dest_weather
        FROM trips t
        JOIN destinations d ON t.destination_id = d.id
        ORDER BY t.start_date ASC
    ''')
    trips = cursor.fetchall()

    # Buscar todos os destinos de verão
    cursor.execute('SELECT * FROM destinations ORDER BY name ASC')
    destinations = cursor.fetchall()

    # Totais Globais
    cursor.execute('SELECT SUM(total_budget), SUM(total_spent) FROM trips')
    totals = cursor.fetchone()
    sum_budget = totals[0] or 0
    sum_spent = totals[1] or 0

    conn.close()

    return render_template(
        'index.html',
        trips=trips,
        destinations=destinations,
        sum_budget=sum_budget,
        sum_spent=sum_spent
    )

@app.route('/trip/<int:trip_id>')
def trip_detail(trip_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.*, d.name as dest_name, d.country as dest_country, d.weather as dest_weather, d.currency, d.avg_daily_cost, d.visa_required
        FROM trips t
        JOIN destinations d ON t.destination_id = d.id
        WHERE t.id = ?
    ''', (trip_id,))
    trip = cursor.fetchone()

    if not trip:
        conn.close()
        flash('A viagem solicitada não foi encontrada.', 'danger')
        return redirect(url_for('index'))

    # Itinerário Dia a Dia
    cursor.execute('''
        SELECT * FROM itinerary_items
        WHERE trip_id = ?
        ORDER BY day_number ASC, time_slot ASC
    ''', (trip_id,))
    raw_itinerary = cursor.fetchall()

    # Agrupar itinerário por Dias
    days_dict = {}
    for item in raw_itinerary:
        day_num = item['day_number']
        if day_num not in days_dict:
            days_dict[day_num] = []
        days_dict[day_num].append(dict(item))

    # Hotéis do Destino
    cursor.execute('SELECT * FROM hotels WHERE destination_id = ?', (trip['destination_id'],))
    hotels = cursor.fetchall()

    conn.close()

    return render_template(
        'trip_detail.html',
        trip=trip,
        days_dict=days_dict,
        hotels=hotels
    )

@app.route('/destinations')
def destinations():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM destinations')
    dest_list = cursor.fetchall()
    conn.close()
    return render_template('destinations.html', destinations=dest_list)


# --- APIS REST ---

@app.route('/api/trips/create', methods=['POST'])
def api_create_trip():
    data = request.form if request.form else (request.json or {})
    title = data.get('title', '').strip()
    destination_id = data.get('destination_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    total_budget = float(data.get('total_budget', 2000.0))

    if not title or not destination_id or not start_date or not end_date:
        flash('Por favor preencha todos os campos obrigatórios da viagem.', 'danger')
        return redirect(url_for('index'))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT image_url FROM destinations WHERE id = ?', (destination_id,))
    dest = cursor.fetchone()
    cover_image = dest['image_url'] if dest else 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800'

    cursor.execute('''
        INSERT INTO trips (title, destination_id, start_date, end_date, total_budget, total_spent, status, cover_image)
        VALUES (?, ?, ?, ?, ?, 0.0, 'Planeada', ?)
    ''', (title, destination_id, start_date, end_date, total_budget, cover_image))

    new_trip_id = cursor.lastrowid
    conn.commit()
    conn.close()

    flash(f'¡Viagem "{title}" criada com sucesso!', 'success')
    return redirect(url_for('trip_detail', trip_id=new_trip_id))


@app.route('/api/trips/<int:trip_id>/add-item', methods=['POST'])
def api_add_itinerary_item(trip_id):
    data = request.form if request.form else (request.json or {})
    day_number = int(data.get('day_number', 1))
    time_slot = data.get('time_slot', '12:00').strip()
    title = data.get('title', '').strip()
    category = data.get('category', 'Atividade')
    location = data.get('location', '').strip()
    cost = float(data.get('cost', 0.0))
    notes = data.get('notes', '').strip()

    if not title:
        if request.is_json:
            return jsonify({'success': False, 'message': 'O título da atividade é obrigatório'}), 400
        flash('O título da atividade é obrigatório.', 'danger')
        return redirect(url_for('trip_detail', trip_id=trip_id))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO itinerary_items (trip_id, day_number, time_slot, title, category, location, cost, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (trip_id, day_number, time_slot, title, category, location, cost, notes))

    # Atualizar total_spent na viagem
    cursor.execute('UPDATE trips SET total_spent = total_spent + ? WHERE id = ?', (cost, trip_id))

    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({'success': True, 'message': 'Atividade adicionada com sucesso!'})

    flash('Atividade adicionada ao itinerário!', 'success')
    return redirect(url_for('trip_detail', trip_id=trip_id))


@app.route('/api/trips/<int:trip_id>/budget')
def api_trip_budget(trip_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT category, SUM(cost) as total
        FROM itinerary_items
        WHERE trip_id = ?
        GROUP BY category
    ''', (trip_id,))
    rows = cursor.fetchall()
    conn.close()

    categories = [{'category': r['category'], 'total': r['total']} for r in rows]
    return jsonify({'success': True, 'categories': categories})


if __name__ == '__main__':
    print("=" * 60)
    print(" [SUNSET TRAVEL SaaS] EJAJ TECH Summer Trip Planner")
    print(" Servidor Flask a correr em http://127.0.0.1:6100")
    print("=" * 60)
    app.run(host='0.0.0.0', port=6100, debug=True)
