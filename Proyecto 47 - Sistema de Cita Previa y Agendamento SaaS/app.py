import os
import sqlite3
import json
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import DB_PATH, init_db

app = Flask(__name__)
app.secret_key = 'ejajtech_appointment_booking_saas_secret_key'

# Custom Filters
@app.template_filter('currency')
def currency_filter(value):
    if value is None:
        return ""
    try:
        val = float(value)
        return f"€ {val:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
    except Exception:
        return f"€ {value}"

@app.template_filter('escapejs')
def escapejs_filter(val):
    if not val:
        return ""
    return json.dumps(str(val))[1:-1]

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Ensure DB exists
if not os.path.exists(DB_PATH):
    init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    professionals = [dict(r) for r in conn.execute('SELECT * FROM professionals ORDER BY name ASC').fetchall()]
    services = [dict(r) for r in conn.execute('''
        SELECT s.*, p.name as professional_name
        FROM services s
        JOIN professionals p ON s.professional_id = p.id
        ORDER BY s.category ASC, s.title ASC
    ''').fetchall()]
    conn.close()
    return render_template('index.html', professionals=professionals, services=services)

@app.route('/professional/<int:prof_id>')
def professional_profile(prof_id):
    conn = get_db_connection()
    prof_row = conn.execute('SELECT * FROM professionals WHERE id = ?', (prof_id,)).fetchone()
    if not prof_row:
        conn.close()
        return "Profissional não encontrado", 404
        
    professional = dict(prof_row)
    services = [dict(r) for r in conn.execute('SELECT * FROM services WHERE professional_id = ? ORDER BY title ASC', (prof_id,)).fetchall()]
    conn.close()
    return render_template('professional.html', professional=professional, services=services)

@app.route('/admin')

@app.route('/admin/<int:prof_id>')
def admin_dashboard(prof_id=1):
    conn = get_db_connection()
    professionals = [dict(r) for r in conn.execute('SELECT * FROM professionals ORDER BY name ASC').fetchall()]
    
    prof_row = conn.execute('SELECT * FROM professionals WHERE id = ?', (prof_id,)).fetchone()
    if not prof_row:
        prof_row = conn.execute('SELECT * FROM professionals LIMIT 1').fetchone()
        
    professional = dict(prof_row)
    
    # Appointments for this professional
    appointments = [dict(r) for r in conn.execute('''
        SELECT a.*, s.title as service_title, s.duration_minutes, s.price
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.professional_id = ?
        ORDER BY a.appointment_date DESC, a.start_time ASC
    ''', (professional['id'],)).fetchall()]
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_appointments = [a for a in appointments if a['appointment_date'] == today_str and a['status'] == 'Confirmada']
    confirmed_count = len([a for a in appointments if a['status'] == 'Confirmada'])
    cancelled_count = len([a for a in appointments if a['status'] == 'Cancelada'])
    
    services = [dict(r) for r in conn.execute('SELECT * FROM services WHERE professional_id = ?', (professional['id'],)).fetchall()]
    
    conn.close()
    return render_template('admin.html', professionals=professionals, professional=professional, appointments=appointments, today_appointments=today_appointments, confirmed_count=confirmed_count, cancelled_count=cancelled_count, services=services, today_str=today_str)

@app.route('/appointments')
def view_appointments():
    q = request.args.get('code', '').strip()
    conn = get_db_connection()
    found_appointment = None
    
    if q:
        row = conn.execute('''
            SELECT a.*, s.title as service_title, s.duration_minutes, s.price, p.name as professional_name, p.specialty as professional_specialty, p.avatar_url as professional_avatar
            FROM appointments a
            JOIN services s ON a.service_id = s.id
            JOIN professionals p ON a.professional_id = p.id
            WHERE a.code = ? OR a.client_email = ? OR a.client_phone = ?
        ''', (q, q, q)).fetchone()
        if row:
            found_appointment = dict(row)
            
    recent_list = [dict(r) for r in conn.execute('''
        SELECT a.*, s.title as service_title, p.name as professional_name
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        JOIN professionals p ON a.professional_id = p.id
        ORDER BY a.id DESC LIMIT 10
    ''').fetchall()]
    
    conn.close()
    return render_template('appointments.html', found_appointment=found_appointment, recent_list=recent_list, q=q)

# API ENDPOINTS
@app.route('/api/availability')
def api_availability():
    prof_id = request.args.get('professional_id', type=int)
    service_id = request.args.get('service_id', type=int)
    date_str = request.args.get('date', '').strip()
    
    if not prof_id or not date_str:
        return jsonify({'success': False, 'message': 'ID do profissional e data são obrigatórios.'}), 400
        
    try:
        req_date = datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return jsonify({'success': False, 'message': 'Formato de data inválido (Use AAAA-MM-DD).'}), 400
        
    day_of_week = req_date.weekday() # 0 = Monday, 6 = Sunday
    
    conn = get_db_connection()
    
    # Check Schedule
    sched_row = conn.execute('''
        SELECT * FROM schedules 
        WHERE professional_id = ? AND day_of_week = ? AND is_active = 1
    ''', (prof_id, day_of_week)).fetchone()
    
    if not sched_row:
        conn.close()
        return jsonify({
            'success': True, 
            'available': False, 
            'message': 'O profissional não atende neste dia da semana.', 
            'slots': []
        })
        
    sched = dict(sched_row)
    
    # Get service duration
    duration = 45 # default
    if service_id:
        srv_row = conn.execute('SELECT duration_minutes FROM services WHERE id = ?', (service_id,)).fetchone()
        if srv_row:
            duration = srv_row['duration_minutes']
            
    # Get booked appointments for that date
    booked_rows = conn.execute('''
        SELECT start_time, end_time FROM appointments 
        WHERE professional_id = ? AND appointment_date = ? AND status != 'Cancelada'
    ''', (prof_id, date_str)).fetchall()
    
    booked_slots = [(r['start_time'], r['end_time']) for r in booked_rows]
    
    # Generate Time Slots
    def time_to_min(t_str):
        parts = t_str.split(':')
        return int(parts[0]) * 60 + int(parts[1])
        
    def min_to_time(m):
        hh = m // 60
        mm = m % 60
        return f"{hh:02d}:{mm:02d}"
        
    start_m = time_to_min(sched['start_time'])
    end_m = time_to_min(sched['end_time'])
    lunch_s_m = time_to_min(sched['lunch_start'])
    lunch_e_m = time_to_min(sched['lunch_end'])
    
    available_slots = []
    curr_m = start_m
    
    while curr_m + duration <= end_m:
        slot_start_t = min_to_time(curr_m)
        slot_end_t = min_to_time(curr_m + duration)
        
        # Check lunch overlap
        is_lunch = not (curr_m + duration <= lunch_s_m or curr_m >= lunch_e_m)
        
        # Check booked overlap
        is_booked = False
        for b_start, b_end in booked_slots:
            b_s_m = time_to_min(b_start)
            b_e_m = time_to_min(b_end)
            if not (curr_m + duration <= b_s_m or curr_m >= b_e_m):
                is_booked = True
                break
                
        if not is_lunch and not is_booked:
            available_slots.append(slot_start_t)
            
        curr_m += 30 # 30 min step
        
    conn.close()
    return jsonify({
        'success': True,
        'available': len(available_slots) > 0,
        'slots': available_slots,
        'duration_minutes': duration
    })

@app.route('/api/appointments/create', methods=['POST'])
def api_appointment_create():
    data = request.json or {}
    prof_id = data.get('professional_id')
    service_id = data.get('service_id')
    date_str = data.get('date', '').strip()
    start_time = data.get('start_time', '').strip()
    client_name = data.get('client_name', '').strip()
    client_email = data.get('client_email', '').strip()
    client_phone = data.get('client_phone', '').strip()
    client_notes = data.get('client_notes', '').strip()
    
    if not prof_id or not service_id or not date_str or not start_time or not client_name or not client_phone:
        return jsonify({'success': False, 'message': 'Por favor preencha todos os campos obrigatórios.'}), 400
        
    conn = get_db_connection()
    srv_row = conn.execute('SELECT duration_minutes, title FROM services WHERE id = ?', (service_id,)).fetchone()
    if not srv_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Serviço inválido.'}), 400
        
    duration = srv_row['duration_minutes']
    
    # Calculate end time
    start_min = int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])
    end_min = start_min + duration
    end_time = f"{end_min // 60:02d}:{end_min % 60:02d}"
    
    # Generate unique code
    code = f"AG-2026-{random.randint(1000, 9999)}"
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (code, professional_id, service_id, appointment_date, start_time, end_time, client_name, client_email, client_phone, client_notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmada')
    ''', (code, prof_id, service_id, date_str, start_time, end_time, client_name, client_email, client_phone, client_notes))
    
    appointment_id = cursor.lastrowid
    
    # Create initial reminder log
    reminder_msg = f"Lembrete EJAJ TECH: Marcação {code} confirmada para {date_str} às {start_time}. Serviço: {srv_row['title']}."
    cursor.execute('INSERT INTO reminders (appointment_id, type, message) VALUES (?, ?, ?)', (appointment_id, 'SMS & E-mail', reminder_msg))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'code': code,
        'appointment_id': appointment_id,
        'message': f'Agendamento {code} efetuado com sucesso! Enviámos a confirmação por SMS e E-mail.'
    })

@app.route('/api/appointments/cancel', methods=['POST'])
def api_appointment_cancel():
    data = request.json or {}
    code_or_id = data.get('code_or_id')
    reason = data.get('reason', 'Cancelamento solicitado pelo cliente.').strip()
    
    if not code_or_id:
        return jsonify({'success': False, 'message': 'Código ou ID de agendamento é obrigatório.'}), 400
        
    conn = get_db_connection()
    conn.execute('''
        UPDATE appointments 
        SET status = 'Cancelada', cancel_reason = ? 
        WHERE code = ? OR id = ?
    ''', (reason, code_or_id, code_or_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Agendamento cancelado com sucesso. A vaga ficou disponível na agenda.'})

@app.route('/api/reminders/send', methods=['POST'])
def api_reminder_send():
    data = request.json or {}
    appointment_id = data.get('appointment_id')
    
    if not appointment_id:
        return jsonify({'success': False, 'message': 'ID de agendamento é obrigatório.'}), 400
        
    conn = get_db_connection()
    appt = conn.execute('SELECT a.*, s.title as service_title FROM appointments a JOIN services s ON a.service_id = s.id WHERE a.id = ?', (appointment_id,)).fetchone()
    
    if not appt:
        conn.close()
        return jsonify({'success': False, 'message': 'Agendamento não encontrado.'}), 400
        
    msg = f"LEMBRETE CONSULTA: Olá {appt['client_name']}, lembramos da sua marcação ({appt['code']}) amanhã {appt['appointment_date']} às {appt['start_time']} para {appt['service_title']}."
    conn.execute('INSERT INTO reminders (appointment_id, type, message) VALUES (?, ?, ?)', (appointment_id, 'SMS & E-mail Instantâneo', msg))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Lembrete por SMS e E-mail enviado com sucesso para {appt["client_phone"]}!'})

if __name__ == '__main__':
    print("[SERVER] Sistema de Cita Previa & Agendamento SaaS a iniciar na porta 6900...")
    app.run(host='0.0.0.0', port=6900, debug=False)
