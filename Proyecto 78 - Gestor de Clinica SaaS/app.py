import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'cliniccraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    today_str = date.today().strftime("%Y-%m-%d")

    # Metrics
    cursor.execute("SELECT COUNT(*) as cnt FROM appointments WHERE appointment_date = ?", (today_str,))
    today_appts = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(amount) as total FROM payments WHERE status = 'Pago'")
    total_revenue = cursor.fetchone()['total'] or 0.0

    cursor.execute("SELECT COUNT(*) as cnt FROM patients")
    total_patients = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM professionals WHERE status = 'Ativo'")
    active_professionals = cursor.fetchone()['cnt']

    # Today's Appointments
    cursor.execute("""
    SELECT a.*, p.name as patient_name, p.insurance, pr.name as professional_name, pr.specialty
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN professionals pr ON a.professional_id = pr.id
    WHERE a.appointment_date = ?
    ORDER BY a.appointment_time ASC
    """, (today_str,))
    today_appts_list = [dict(r) for r in cursor.fetchall()]

    # Recent Payments
    cursor.execute("""
    SELECT py.*, p.name as patient_name, a.appointment_code
    FROM payments py
    JOIN patients p ON py.patient_id = p.id
    JOIN appointments a ON py.appointment_id = a.id
    ORDER BY py.id DESC
    LIMIT 4
    """)
    recent_payments = [dict(r) for r in cursor.fetchall()]

    # Dropdowns for Modals
    cursor.execute("SELECT id, name, nif FROM patients ORDER BY name ASC")
    patients_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, specialty, consultation_fee FROM professionals WHERE status = 'Ativo' ORDER BY name ASC")
    professionals_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT a.id, a.appointment_code, p.name as patient_name, a.fee FROM appointments a JOIN patients p ON a.patient_id = p.id ORDER BY a.id DESC")
    appointments_list = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        today_appts=today_appts,
        total_revenue=round(total_revenue, 2),
        total_patients=total_patients,
        active_professionals=active_professionals,
        today_appts_list=today_appts_list,
        recent_payments=recent_payments,
        patients_list=patients_list,
        professionals_list=professionals_list,
        appointments_list=appointments_list
    )

@app.route('/patients')
def patients_page():
    conn = get_db()
    cursor = conn.cursor()

    insurance_filter = request.args.get('insurance')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT p.*, COUNT(a.id) as total_appointments
    FROM patients p
    LEFT JOIN appointments a ON p.id = a.patient_id
    WHERE 1=1
    """
    params = []

    if insurance_filter:
        query += " AND p.insurance = ?"
        params.append(insurance_filter)

    if search_q:
        query += " AND (p.patient_code LIKE ? OR p.name LIKE ? OR p.nif LIKE ? OR p.email LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " GROUP BY p.id ORDER BY p.id DESC"
    cursor.execute(query, params)
    patients = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT insurance FROM patients ORDER BY insurance ASC")
    insurances = [r['insurance'] for r in cursor.fetchall()]

    conn.close()
    return render_template('patients.html', patients=patients, insurances=insurances, selected_insurance=insurance_filter, search_q=search_q)

@app.route('/professionals')
def professionals_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT pr.*, COUNT(a.id) as total_appointments
    FROM professionals pr
    LEFT JOIN appointments a ON pr.id = a.professional_id
    GROUP BY pr.id
    ORDER BY pr.id DESC
    """)
    professionals = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('professionals.html', professionals=professionals)

@app.route('/appointments')
def appointments_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT a.*, p.name as patient_name, p.nif, pr.name as professional_name, pr.specialty
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN professionals pr ON a.professional_id = pr.id
    WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND a.status = ?"
        params.append(status_filter)

    if search_q:
        query += " AND (a.appointment_code LIKE ? OR p.name LIKE ? OR pr.name LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " ORDER BY a.appointment_date DESC, a.appointment_time ASC"
    cursor.execute(query, params)
    appointments = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, nif FROM patients ORDER BY name ASC")
    patients_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, specialty, consultation_fee FROM professionals WHERE status = 'Ativo' ORDER BY name ASC")
    professionals_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('appointments.html', appointments=appointments, selected_status=status_filter, search_q=search_q, patients_list=patients_list, professionals_list=professionals_list)

@app.route('/consultations')
def consultations_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.*, p.name as patient_name, p.nif, pr.name as professional_name, pr.specialty, a.appointment_code
    FROM consultations c
    JOIN appointments a ON c.appointment_id = a.id
    JOIN patients p ON c.patient_id = p.id
    JOIN professionals pr ON c.professional_id = pr.id
    ORDER BY c.id DESC
    """)
    consultations = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
    SELECT a.id, a.appointment_code, p.name as patient_name, pr.name as professional_name, a.patient_id, a.professional_id
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN professionals pr ON a.professional_id = pr.id
    ORDER BY a.id DESC
    """)
    appointments_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('consultations.html', consultations=consultations, appointments_list=appointments_list)

@app.route('/documents')
def documents_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT d.*, p.name as patient_name, p.patient_code
    FROM documents d
    JOIN patients p ON d.patient_id = p.id
    ORDER BY d.id DESC
    """)
    documents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM patients ORDER BY name ASC")
    patients_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('documents.html', documents=documents, patients_list=patients_list)

@app.route('/payments')
def payments_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT py.*, p.name as patient_name, p.nif, a.appointment_code
    FROM payments py
    JOIN patients p ON py.patient_id = p.id
    JOIN appointments a ON py.appointment_id = a.id
    ORDER BY py.id DESC
    """)
    payments = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT a.id, a.appointment_code, p.name as patient_name, a.patient_id, a.fee FROM appointments a JOIN patients p ON a.patient_id = p.id ORDER BY a.id DESC")
    appointments_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('payments.html', payments=payments, appointments_list=appointments_list)

# API ENDPOINTS

@app.route('/api/appointment/create', methods=['POST'])
def api_create_appointment():
    try:
        data = request.get_json() or {}
        patient_id = data.get('patient_id')
        professional_id = data.get('professional_id')
        appt_date = data.get('appointment_date', '').strip()
        appt_time = data.get('appointment_time', '').strip()
        reason = data.get('reason', '').strip()

        if not patient_id or not professional_id or not appt_date or not appt_time:
            return jsonify({'success': False, 'message': 'Preencha o paciente, médico, data e hora da marcação.'}), 400

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT consultation_fee FROM professionals WHERE id = ?", (professional_id,))
        p_row = cursor.fetchone()
        fee = p_row['consultation_fee'] if p_row else 75.0

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("SELECT COUNT(*) as cnt FROM appointments")
        code_num = cursor.fetchone()['cnt'] + 705
        appt_code = f"CNS-2026-{code_num}"

        cursor.execute("""
        INSERT INTO appointments (appointment_code, patient_id, professional_id, appointment_date, appointment_time, status, reason, fee, created_at)
        VALUES (?, ?, ?, ?, ?, 'Confirmada', ?, ?, ?)
        """, (appt_code, patient_id, professional_id, appt_date, appt_time, reason, fee, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Marcação de consulta "{appt_code}" registada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/appointment/status/<int:appt_id>', methods=['POST'])
def api_update_appointment_status(appt_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Realizada')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, appt_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Estado da consulta alterado para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/consultation/create', methods=['POST'])
def api_create_consultation():
    try:
        data = request.get_json() or {}
        appointment_id = data.get('appointment_id')
        diagnosis = data.get('diagnosis', '').strip()
        symptoms = data.get('symptoms', '').strip()
        prescription = data.get('prescription', '').strip()
        vitals = data.get('vitals', 'Sinais vitais normais').strip()

        if not appointment_id or not diagnosis or not symptoms:
            return jsonify({'success': False, 'message': 'Selecione a marcação e preencha os sintomas e o diagnóstico.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT patient_id, professional_id FROM appointments WHERE id = ?", (appointment_id,))
        a_row = cursor.fetchone()

        if not a_row:
            conn.close()
            return jsonify({'success': False, 'message': 'Marcação não encontrada.'}), 400

        cursor.execute("""
        INSERT INTO consultations (appointment_id, patient_id, professional_id, diagnosis, symptoms, prescription, vitals, consultation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (appointment_id, a_row['patient_id'], a_row['professional_id'], diagnosis, symptoms, prescription, vitals, now_str))

        cursor.execute("UPDATE appointments SET status = 'Realizada' WHERE id = ?", (appointment_id,))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Consulta clínica registada e marcação alterada para Realizada!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/patient/create', methods=['POST'])
def api_create_patient():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        nif = data.get('nif', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        birth_date = data.get('birth_date', '').strip()
        insurance = data.get('insurance', 'Particular').strip()
        blood_type = data.get('blood_type', 'O+').strip()

        if not name or not nif or not email:
            return jsonify({'success': False, 'message': 'Preencha o nome, NIF e email do paciente.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM patients")
        code_num = cursor.fetchone()['cnt'] + 1005
        p_code = f"PAC-{code_num}"

        cursor.execute("""
        INSERT INTO patients (patient_code, name, nif, email, phone, birth_date, insurance, blood_type, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p_code, name, nif, email, phone, birth_date, insurance, blood_type, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Paciente "{name}" ({p_code}) registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/professional/create', methods=['POST'])
def api_create_professional():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        specialty = data.get('specialty', '').strip()
        license_no = data.get('license_no', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        fee = float(data.get('consultation_fee', 70.0))

        if not name or not specialty or not license_no:
            return jsonify({'success': False, 'message': 'Preencha o nome, especialidade e nº de cédula profissional.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO professionals (name, specialty, license_no, email, phone, consultation_fee, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'Ativo', ?)
        """, (name, specialty, license_no, email, phone, fee, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Profissional médico "{name}" registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/document/create', methods=['POST'])
def api_create_document():
    try:
        data = request.get_json() or {}
        patient_id = data.get('patient_id')
        title = data.get('title', '').strip()
        doc_type = data.get('doc_type', 'Exame').strip()
        file_name = data.get('file_name', 'relatorio_clinico.pdf').strip()

        if not patient_id or not title:
            return jsonify({'success': False, 'message': 'Selecione o paciente e introduza o título do documento.'}), 400

        now_date = date.today().strftime("%Y-%m-%d")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM documents")
        code_num = cursor.fetchone()['cnt'] + 104
        doc_code = f"DOC-2026-{code_num}"

        cursor.execute("""
        INSERT INTO documents (document_code, patient_id, title, doc_type, file_name, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (doc_code, patient_id, title, doc_type, file_name, now_date))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Documento "{doc_code}" anexado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/payment/create', methods=['POST'])
def api_create_payment():
    try:
        data = request.get_json() or {}
        appointment_id = data.get('appointment_id')
        amount = float(data.get('amount', 75.0))
        payment_method = data.get('payment_method', 'MB WAY').strip()
        status = data.get('status', 'Pago').strip()

        if not appointment_id:
            return jsonify({'success': False, 'message': 'Selecione a consulta médica.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT patient_id FROM appointments WHERE id = ?", (appointment_id,))
        a_row = cursor.fetchone()
        patient_id = a_row['patient_id'] if a_row else 1

        cursor.execute("SELECT COUNT(*) as cnt FROM payments")
        code_num = cursor.fetchone()['cnt'] + 904
        inv_code = f"FT-2026-{code_num}"

        cursor.execute("""
        INSERT INTO payments (invoice_code, appointment_id, patient_id, amount, payment_method, status, payment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (inv_code, appointment_id, patient_id, amount, payment_method, status, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Fatura "{inv_code}" emitida com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT a.appointment_code, p.name as patient_name, p.nif, pr.name as professional_name, pr.specialty, a.appointment_date, a.appointment_time, a.fee, a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN professionals pr ON a.professional_id = pr.id
    ORDER BY a.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        return Response(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=cliniccraft_export.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Código Consulta', 'Paciente', 'NIF', 'Profissional', 'Especialidade', 'Data', 'Hora', 'Valor (€)', 'Estado'])
        for r in rows:
            writer.writerow([r['appointment_code'], r['patient_name'], r['nif'], r['professional_name'], r['specialty'], r['appointment_date'], r['appointment_time'], r['fee'], r['status']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=cliniccraft_export.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6931, debug=True)
