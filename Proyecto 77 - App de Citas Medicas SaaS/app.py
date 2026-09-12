import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'medicare.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Unread notifications count
    cursor.execute("SELECT COUNT(*) as cnt FROM notifications WHERE is_read = 0")
    unread_notifications = cursor.fetchone()['cnt']

    # Next Upcoming Appointment
    cursor.execute("""
    SELECT a.*, p.name as patient_name, d.name as doctor_name, d.location, s.name as specialty_name, s.icon as specialty_icon
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    JOIN specialties s ON a.specialty_id = s.id
    WHERE a.status = 'Confirmada' AND a.appointment_date >= ?
    ORDER BY a.appointment_date ASC, a.appointment_time ASC
    LIMIT 1
    """, (date.today().strftime("%Y-%m-%d"),))
    next_appt_row = cursor.fetchone()
    next_appt = dict(next_appt_row) if next_appt_row else None

    # Specialties List
    cursor.execute("SELECT * FROM specialties ORDER BY id ASC LIMIT 6")
    specialties = [dict(r) for r in cursor.fetchall()]

    # Top Doctors
    cursor.execute("""
    SELECT d.*, s.name as specialty_name
    FROM doctors d
    JOIN specialties s ON d.specialty_id = s.id
    ORDER BY d.rating DESC
    LIMIT 4
    """)
    top_doctors = [dict(r) for r in cursor.fetchall()]

    # Recent Appointments
    cursor.execute("""
    SELECT a.*, p.name as patient_name, d.name as doctor_name, s.name as specialty_name
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    JOIN specialties s ON a.specialty_id = s.id
    ORDER BY a.id DESC
    LIMIT 3
    """)
    recent_appts = [dict(r) for r in cursor.fetchall()]

    # Dropdowns for Modals
    cursor.execute("SELECT id, name FROM patients ORDER BY name ASC")
    patients_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT d.id, d.name, s.name as specialty_name, d.consultation_fee FROM doctors d JOIN specialties s ON d.specialty_id = s.id ORDER BY d.name ASC")
    doctors_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM specialties ORDER BY name ASC")
    specialties_list = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        unread_notifications=unread_notifications,
        next_appt=next_appt,
        specialties=specialties,
        top_doctors=top_doctors,
        recent_appts=recent_appts,
        patients_list=patients_list,
        doctors_list=doctors_list,
        specialties_list=specialties_list
    )

@app.route('/patients')
def patients_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.*, COUNT(a.id) as total_appointments
    FROM patients p
    LEFT JOIN appointments a ON p.id = a.patient_id
    GROUP BY p.id
    ORDER BY p.id DESC
    """)
    patients = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('patients.html', patients=patients)

@app.route('/doctors')
def doctors_page():
    conn = get_db()
    cursor = conn.cursor()

    spec_filter = request.args.get('specialty_id')
    query = """
    SELECT d.*, s.name as specialty_name, s.icon as specialty_icon
    FROM doctors d
    JOIN specialties s ON d.specialty_id = s.id
    WHERE 1=1
    """
    params = []

    if spec_filter:
        query += " AND d.specialty_id = ?"
        params.append(spec_filter)

    query += " ORDER BY d.rating DESC"
    cursor.execute(query, params)
    doctors = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM specialties ORDER BY name ASC")
    specialties = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('doctors.html', doctors=doctors, specialties=specialties, selected_spec=spec_filter)

@app.route('/specialties')
def specialties_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT s.*, COUNT(d.id) as doctor_count
    FROM specialties s
    LEFT JOIN doctors d ON s.id = d.specialty_id
    GROUP BY s.id
    ORDER BY s.id ASC
    """)
    specialties = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('specialties.html', specialties=specialties)

@app.route('/appointments')
def appointments_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    query = """
    SELECT a.*, p.name as patient_name, d.name as doctor_name, d.location, s.name as specialty_name, s.icon as specialty_icon
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    JOIN specialties s ON a.specialty_id = s.id
    WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND a.status = ?"
        params.append(status_filter)

    query += " ORDER BY a.appointment_date DESC, a.appointment_time ASC"
    cursor.execute(query, params)
    appointments = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM patients ORDER BY name ASC")
    patients_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT d.id, d.name, s.name as specialty_name, d.consultation_fee FROM doctors d JOIN specialties s ON d.specialty_id = s.id ORDER BY d.name ASC")
    doctors_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM specialties ORDER BY name ASC")
    specialties_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('appointments.html', appointments=appointments, selected_status=status_filter, patients_list=patients_list, doctors_list=doctors_list, specialties_list=specialties_list)

@app.route('/schedules')
def schedules_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT sc.*, d.name as doctor_name, s.name as specialty_name
    FROM schedules sc
    JOIN doctors d ON sc.doctor_id = d.id
    JOIN specialties s ON d.specialty_id = s.id
    ORDER BY d.name ASC, sc.day_of_week ASC, sc.time_slot ASC
    """)
    schedules = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('schedules.html', schedules=schedules)

@app.route('/notifications')
def notifications_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notifications ORDER BY id DESC")
    notifications = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('notifications.html', notifications=notifications)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT h.*, p.name as patient_name, d.name as doctor_name, a.appointment_code, a.appointment_date, s.name as specialty_name
    FROM medical_history h
    JOIN appointments a ON h.appointment_id = a.id
    JOIN patients p ON h.patient_id = p.id
    JOIN doctors d ON h.doctor_id = d.id
    JOIN specialties s ON a.specialty_id = s.id
    ORDER BY h.id DESC
    """)
    records = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('history.html', records=records)

# API ENDPOINTS

@app.route('/api/appointment/book', methods=['POST'])
def api_book_appointment():
    try:
        data = request.get_json() or {}
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        specialty_id = data.get('specialty_id')
        appt_date = data.get('appointment_date', '').strip()
        appt_time = data.get('appointment_time', '').strip()
        reason = data.get('reason', '').strip()

        if not patient_id or not doctor_id or not appt_date or not appt_time:
            return jsonify({'success': False, 'message': 'Selecione o paciente, médico, data e hora da consulta.'}), 400

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT consultation_fee, specialty_id FROM doctors WHERE id = ?", (doctor_id,))
        doc_row = cursor.fetchone()
        fee = doc_row['consultation_fee'] if doc_row else 60.0
        if not specialty_id and doc_row:
            specialty_id = doc_row['specialty_id']

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("SELECT COUNT(*) as cnt FROM appointments")
        code_num = cursor.fetchone()['cnt'] + 505
        appt_code = f"CIT-2026-{code_num}"

        cursor.execute("""
        INSERT INTO appointments (appointment_code, patient_id, doctor_id, specialty_id, appointment_date, appointment_time, status, reason, fee, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'Confirmada', ?, ?, ?)
        """, (appt_code, patient_id, doctor_id, specialty_id, appt_date, appt_time, reason, fee, now_str))

        # Create notification
        cursor.execute("SELECT name FROM doctors WHERE id = ?", (doctor_id,))
        doc_name = cursor.fetchone()['name']

        cursor.execute("""
        INSERT INTO notifications (title, message, type, timestamp, is_read)
        VALUES (?, ?, 'Confirmação', ?, 0)
        """, (f"Cita Médica Agendada 🩺", f"Cita {appt_code} agendada com {doc_name} para {appt_date} às {appt_time}.", now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Consulta "{appt_code}" agendada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/appointment/status/<int:appt_id>', methods=['POST'])
def api_update_appointment_status(appt_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Concluída')
        diagnosis = data.get('diagnosis', '').strip()
        prescription = data.get('prescription', '').strip()

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, appt_id))

        if new_status == 'Concluída' and diagnosis:
            cursor.execute("SELECT patient_id, doctor_id FROM appointments WHERE id = ?", (appt_id,))
            a_row = cursor.fetchone()
            if a_row:
                cursor.execute("""
                INSERT INTO medical_history (appointment_id, patient_id, doctor_id, diagnosis, prescription, notes, created_at)
                VALUES (?, ?, ?, ?, ?, 'Consulta concluída com receita médica.', ?)
                """, (appt_id, a_row['patient_id'], a_row['doctor_id'], diagnosis, prescription, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Consulta alterada para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/patient/create', methods=['POST'])
def api_create_patient():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        birth_date = data.get('birth_date', '').strip()
        blood_type = data.get('blood_type', 'O+').strip()
        nif = data.get('nif', '').strip()

        if not name or not email or not nif:
            return jsonify({'success': False, 'message': 'Preencha o nome, email e NIF do paciente.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients (name, email, phone, birth_date, blood_type, nif, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, birth_date, blood_type, nif, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Paciente "{name}" cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/notification/read/<int:n_id>', methods=['POST'])
def api_read_notification(n_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (n_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT a.appointment_code, p.name as patient_name, d.name as doctor_name, s.name as specialty_name, a.appointment_date, a.appointment_time, a.fee, a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    JOIN specialties s ON a.specialty_id = s.id
    ORDER BY a.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        return Response(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=medicare_export.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Código Cita', 'Paciente', 'Médico', 'Especialidade', 'Data', 'Hora', 'Valor (€)', 'Estado'])
        for r in rows:
            writer.writerow([r['appointment_code'], r['patient_name'], r['doctor_name'], r['specialty_name'], r['appointment_date'], r['appointment_time'], r['fee'], r['status']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=medicare_export.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6930, debug=True)
