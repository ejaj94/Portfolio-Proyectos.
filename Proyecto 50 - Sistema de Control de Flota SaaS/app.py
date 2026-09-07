import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import DB_PATH, init_db

app = Flask(__name__)
app.secret_key = 'ejajtech_fleet_management_saas_secret_key'

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

@app.template_filter('km')
def km_filter(value):
    if value is None:
        return "0 km"
    try:
        val = int(value)
        return f"{val:,} km".replace(',', ' ')
    except Exception:
        return f"{value} km"

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
    conn = get_db_connection()
    vehicles = [dict(r) for r in conn.execute('SELECT * FROM vehicles ORDER BY id DESC').fetchall()]
    drivers = [dict(r) for r in conn.execute('SELECT * FROM drivers').fetchall()]
    fuel_logs = [dict(r) for r in conn.execute('SELECT * FROM fuel_logs ORDER BY fill_date DESC LIMIT 5').fetchall()]
    alerts = [dict(r) for r in conn.execute('SELECT * FROM alerts WHERE is_resolved = 0 ORDER BY id DESC').fetchall()]
    
    total_vehicles = len(vehicles)
    operational_count = len([v for v in vehicles if v['status'] == 'Operacional'])
    maintenance_count = len([v for v in vehicles if v['status'] == 'Em Manutenção'])
    total_fuel_cost = sum([f['total_cost'] for f in fuel_logs])
    
    conn.close()
    return render_template(
        'index.html', 
        vehicles=vehicles, 
        drivers=drivers, 
        fuel_logs=fuel_logs, 
        alerts=alerts,
        total_vehicles=total_vehicles,
        operational_count=operational_count,
        maintenance_count=maintenance_count,
        total_fuel_cost=total_fuel_cost
    )

@app.route('/vehicles')
def vehicles_page():
    conn = get_db_connection()
    vehicles = [dict(r) for r in conn.execute('SELECT * FROM vehicles ORDER BY id DESC').fetchall()]
    drivers = [dict(r) for r in conn.execute('SELECT * FROM drivers').fetchall()]
    conn.close()
    return render_template('vehicles.html', vehicles=vehicles, drivers=drivers)

@app.route('/drivers')
def drivers_page():
    conn = get_db_connection()
    drivers = [dict(r) for r in conn.execute('SELECT * FROM drivers ORDER BY id DESC').fetchall()]
    conn.close()
    return render_template('drivers.html', drivers=drivers)

@app.route('/fuel')
def fuel_page():
    conn = get_db_connection()
    fuel_logs = [dict(r) for r in conn.execute('SELECT * FROM fuel_logs ORDER BY fill_date DESC').fetchall()]
    vehicles = [dict(r) for r in conn.execute('SELECT * FROM vehicles ORDER BY plate ASC').fetchall()]
    conn.close()
    return render_template('fuel.html', fuel_logs=fuel_logs, vehicles=vehicles)

@app.route('/maintenance')
def maintenance_page():
    conn = get_db_connection()
    maintenances = [dict(r) for r in conn.execute('SELECT * FROM maintenances ORDER BY maint_date DESC').fetchall()]
    vehicles = [dict(r) for r in conn.execute('SELECT * FROM vehicles ORDER BY plate ASC').fetchall()]
    conn.close()
    return render_template('maintenance.html', maintenances=maintenances, vehicles=vehicles)

@app.route('/alerts')
def alerts_page():
    conn = get_db_connection()
    alerts = [dict(r) for r in conn.execute('SELECT * FROM alerts ORDER BY is_resolved ASC, id DESC').fetchall()]
    conn.close()
    return render_template('alerts.html', alerts=alerts)

# API ENDPOINTS
@app.route('/api/vehicles/add', methods=['POST'])
def api_vehicle_add():
    data = request.json or {}
    plate = data.get('plate', '').strip().upper()
    brand = data.get('brand', '').strip()
    model = data.get('model', '').strip()
    category = data.get('category', 'Carrinha Comercial').strip()
    year = int(data.get('year', 2024))
    fuel_type = data.get('fuel_type', 'Diesel').strip()
    current_km = int(data.get('current_km', 0))
    driver_name = data.get('driver_name', 'Não Atribuído').strip()
    insurance_expiry = data.get('insurance_expiry', '').strip()
    itv_expiry = data.get('itv_expiry', '').strip()
    
    if not plate or not brand or not model:
        return jsonify({'success': False, 'message': 'Matrícula, marca e modelo são obrigatórios.'}), 400
        
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO vehicles (plate, brand, model, category, year, fuel_type, current_km, status, driver_name, insurance_expiry, itv_expiry)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Operacional', ?, ?, ?)
        ''', (plate, brand, model, category, year, fuel_type, current_km, driver_name, insurance_expiry, itv_expiry))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Veículo {plate} adicionado à frota com sucesso!'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Esta matrícula já se encontra registada na frota.'}), 400

@app.route('/api/fuel/log', methods=['POST'])
def api_fuel_log():
    data = request.json or {}
    vehicle_id = int(data.get('vehicle_id', 0))
    fill_date = data.get('fill_date', '').strip()
    liters = float(data.get('liters', 0))
    total_cost = float(data.get('total_cost', 0))
    km_at_fill = int(data.get('km_at_fill', 0))
    
    if not vehicle_id or liters <= 0 or total_cost <= 0 or km_at_fill <= 0:
        return jsonify({'success': False, 'message': 'Por favor preencha todos os campos do abastecimento.'}), 400
        
    conn = get_db_connection()
    v_row = conn.execute('SELECT plate, current_km FROM vehicles WHERE id = ?', (vehicle_id,)).fetchone()
    if not v_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Veículo não encontrado.'}), 400
        
    vehicle_plate = v_row['plate']
    prev_km = v_row['current_km']
    
    # Calculate avg consumption (L/100km)
    distance = max(km_at_fill - prev_km, 100)
    avg_consumption = round((liters / distance) * 100.0, 1) if distance > 0 else 0.0
    
    conn.execute('''
        INSERT INTO fuel_logs (vehicle_id, vehicle_plate, fill_date, liters, total_cost, km_at_fill, avg_consumption)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (vehicle_id, vehicle_plate, fill_date, liters, total_cost, km_at_fill, avg_consumption))
    
    # Update current km on vehicle
    if km_at_fill > prev_km:
        conn.execute('UPDATE vehicles SET current_km = ? WHERE id = ?', (km_at_fill, vehicle_id))
        
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Abastecimento registado para a viatura {vehicle_plate}! Consumo estimado: {avg_consumption} L/100km.'})

@app.route('/api/maintenance/add', methods=['POST'])
def api_maintenance_add():
    data = request.json or {}
    vehicle_id = int(data.get('vehicle_id', 0))
    maint_type = data.get('maint_type', '').strip()
    description = data.get('description', '').strip()
    maint_date = data.get('maint_date', '').strip()
    km_at_maint = int(data.get('km_at_maint', 0))
    cost = float(data.get('cost', 0))
    next_due_date = data.get('next_due_date', '').strip()
    
    if not vehicle_id or not maint_type or not maint_date or cost <= 0:
        return jsonify({'success': False, 'message': 'Por favor preencha os dados da manutenção.'}), 400
        
    conn = get_db_connection()
    v_row = conn.execute('SELECT plate FROM vehicles WHERE id = ?', (vehicle_id,)).fetchone()
    if not v_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Veículo não encontrado.'}), 400
        
    vehicle_plate = v_row['plate']
    conn.execute('''
        INSERT INTO maintenances (vehicle_id, vehicle_plate, maint_type, description, maint_date, km_at_maint, cost, next_due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (vehicle_id, vehicle_plate, maint_type, description, maint_date, km_at_maint, cost, next_due_date))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Manutenção registada com sucesso para a viatura {vehicle_plate}!'})

@app.route('/api/alerts/resolve/<int:alert_id>', methods=['POST'])
def api_alert_resolve(alert_id):
    conn = get_db_connection()
    conn.execute('UPDATE alerts SET is_resolved = 1 WHERE id = ?', (alert_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Alerta marcado como resolvido.'})

if __name__ == '__main__':
    print("[SERVER] Sistema de Controlo de Frota SaaS a iniciar na porta 6903...")
    app.run(host='0.0.0.0', port=6903, debug=False)
