import os
import sqlite3
import csv
import io
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/pets')
def pets():
    return render_template('pets.html', active_page='pets')

@app.route('/owners')
def owners():
    return render_template('owners.html', active_page='owners')

@app.route('/appointments')
def appointments():
    return render_template('appointments.html', active_page='appointments')

@app.route('/vaccines')
def vaccines():
    return render_template('vaccines.html', active_page='vaccines')

@app.route('/treatments')
def treatments():
    return render_template('treatments.html', active_page='treatments')

@app.route('/reminders')
def reminders():
    return render_template('reminders.html', active_page='reminders')

@app.route('/history')
def history():
    return render_template('history.html', active_page='history')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM pets')
    total_pets = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM owners')
    total_owners = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status IN ('Agendada', 'Confirmada')")
    active_appointments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reminders WHERE status = 'Pendente'")
    pending_reminders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM treatments WHERE status = 'Em Curso'")
    active_treatments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vaccines WHERE status = 'Expirada'")
    expired_vaccines = cursor.fetchone()[0]

    conn.close()
    return jsonify({
        'total_pets': total_pets,
        'total_owners': total_owners,
        'active_appointments': active_appointments,
        'pending_reminders': pending_reminders,
        'active_treatments': active_treatments,
        'expired_vaccines': expired_vaccines
    })

# Owners API
@app.route('/api/owners', methods=['GET'])
def get_owners():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM owners ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/owners/create', methods=['POST'])
def create_owner():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO owners (name, phone, email, address, nif, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.get('name'), data.get('phone'), data.get('email'), data.get('address'), data.get('nif'), data.get('notes', '')))
        conn.commit()
        owner_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': owner_id, 'message': 'Proprietário registado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: NIF já existente no sistema.'}), 400

@app.route('/api/owners/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM owners WHERE id = ?', (owner_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Proprietário eliminado com sucesso.'})

# Pets API
@app.route('/api/pets', methods=['GET'])
def get_pets():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pets.*, owners.name as owner_name, owners.phone as owner_phone
        FROM pets
        JOIN owners ON pets.owner_id = owners.id
        ORDER BY pets.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/pets/create', methods=['POST'])
def create_pet():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO pets (owner_id, name, species, breed, age_years, weight_kg, microchip_id, gender, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('owner_id'), data.get('name'), data.get('species'), data.get('breed'),
            float(data.get('age_years', 0)), float(data.get('weight_kg', 0)),
            data.get('microchip_id'), data.get('gender'), data.get('notes', '')
        ))
        conn.commit()
        pet_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': pet_id, 'message': 'Animal de estimação registado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: Microchip já registado no sistema.'}), 400

@app.route('/api/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pets WHERE id = ?', (pet_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ficha de animal eliminada com sucesso.'})

# Appointments API
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT appointments.*, pets.name as pet_name, pets.species as pet_species, owners.name as owner_name, owners.phone as owner_phone
        FROM appointments
        JOIN pets ON appointments.pet_id = pets.id
        JOIN owners ON appointments.owner_id = owners.id
        ORDER BY appointments.date ASC, appointments.time ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/appointments/create', methods=['POST'])
def create_appointment():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Fetch owner_id from pet_id if not supplied
    pet_id = data.get('pet_id')
    cursor.execute('SELECT owner_id FROM pets WHERE id = ?', (pet_id,))
    pet_row = cursor.fetchone()
    if not pet_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Animal não encontrado.'}), 404
    owner_id = pet_row['owner_id']

    cursor.execute('''
        INSERT INTO appointments (pet_id, owner_id, vet_name, date, time, reason, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        pet_id, owner_id, data.get('vet_name'), data.get('date'),
        data.get('time'), data.get('reason'), data.get('status', 'Agendada'), data.get('notes', '')
    ))
    conn.commit()
    appt_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': appt_id, 'message': 'Marcação veterinária agendada com sucesso!'}), 201

@app.route('/api/appointments/update-status/<int:appt_id>', methods=['POST'])
def update_appointment_status(appt_id):
    status = request.json.get('status')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', (status, appt_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Estado alterado para {status}.'})

@app.route('/api/appointments/<int:appt_id>', methods=['DELETE'])
def delete_appointment(appt_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appointments WHERE id = ?', (appt_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Marcação removida com sucesso.'})

# Vaccines API
@app.route('/api/vaccines', methods=['GET'])
def get_vaccines():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT vaccines.*, pets.name as pet_name, pets.species as pet_species, owners.name as owner_name
        FROM vaccines
        JOIN pets ON vaccines.pet_id = pets.id
        JOIN owners ON pets.owner_id = owners.id
        ORDER BY vaccines.next_due_date ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/vaccines/create', methods=['POST'])
def create_vaccine():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vaccines (pet_id, vaccine_name, batch_number, admin_date, next_due_date, vet_name, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('pet_id'), data.get('vaccine_name'), data.get('batch_number'),
        data.get('admin_date'), data.get('next_due_date'), data.get('vet_name'),
        data.get('status', 'Válida'), data.get('notes', '')
    ))
    conn.commit()
    v_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': v_id, 'message': 'Vacina registada com sucesso!'}), 201

@app.route('/api/vaccines/<int:v_id>', methods=['DELETE'])
def delete_vaccine(v_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vaccines WHERE id = ?', (v_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de vacina eliminado.'})

# Treatments API
@app.route('/api/treatments', methods=['GET'])
def get_treatments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT treatments.*, pets.name as pet_name, pets.species as pet_species, owners.name as owner_name
        FROM treatments
        JOIN pets ON treatments.pet_id = pets.id
        JOIN owners ON pets.owner_id = owners.id
        ORDER BY treatments.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/treatments/create', methods=['POST'])
def create_treatment():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO treatments (pet_id, diagnosis, prescription, dosage, start_date, end_date, cost, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('pet_id'), data.get('diagnosis'), data.get('prescription'),
        data.get('dosage'), data.get('start_date'), data.get('end_date'),
        float(data.get('cost', 0)), data.get('status', 'Em Curso')
    ))
    conn.commit()
    t_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': t_id, 'message': 'Tratamento registado com sucesso!'}), 201

@app.route('/api/treatments/update-status/<int:t_id>', methods=['POST'])
def update_treatment_status(t_id):
    status = request.json.get('status')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE treatments SET status = ? WHERE id = ?', (status, t_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Estado do tratamento atualizado para {status}.'})

@app.route('/api/treatments/<int:t_id>', methods=['DELETE'])
def delete_treatment(t_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM treatments WHERE id = ?', (t_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Tratamento eliminado com sucesso.'})

# Reminders API
@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT reminders.*, pets.name as pet_name, owners.name as owner_name, owners.phone as owner_phone, owners.email as owner_email
        FROM reminders
        JOIN pets ON reminders.pet_id = pets.id
        JOIN owners ON reminders.owner_id = owners.id
        ORDER BY reminders.target_date ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/reminders/create', methods=['POST'])
def create_reminder():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    pet_id = data.get('pet_id')
    cursor.execute('SELECT owner_id FROM pets WHERE id = ?', (pet_id,))
    pet_row = cursor.fetchone()
    if not pet_row:
        conn.close()
        return jsonify({'success': False, 'message': 'Animal não encontrado.'}), 404
    owner_id = pet_row['owner_id']

    cursor.execute('''
        INSERT INTO reminders (pet_id, owner_id, title, reminder_type, target_date, status, sent_channel)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        pet_id, owner_id, data.get('title'), data.get('reminder_type'),
        data.get('target_date'), data.get('status', 'Pendente'), data.get('sent_channel', 'SMS / WhatsApp')
    ))
    conn.commit()
    r_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': r_id, 'message': 'Lembrete automático agendado com sucesso!'}), 201

@app.route('/api/reminders/send/<int:r_id>', methods=['POST'])
def send_reminder(r_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE reminders SET status = 'Enviado' WHERE id = ?", (r_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Notificação/Lembrete enviado ao cliente com sucesso via WhatsApp/SMS!'})

@app.route('/api/reminders/<int:r_id>', methods=['DELETE'])
def delete_reminder(r_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reminders WHERE id = ?', (r_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Lembrete removido.'})

# History API
@app.route('/api/history', methods=['GET'])
def get_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT medical_history.*, pets.name as pet_name, pets.species as pet_species, owners.name as owner_name
        FROM medical_history
        JOIN pets ON medical_history.pet_id = pets.id
        JOIN owners ON pets.owner_id = owners.id
        ORDER BY medical_history.visit_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/history/create', methods=['POST'])
def create_history():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medical_history (pet_id, visit_date, symptoms, diagnosis, vet_signature, total_cost)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('pet_id'), data.get('visit_date'), data.get('symptoms'),
        data.get('diagnosis'), data.get('vet_signature'), float(data.get('total_cost', 0))
    ))
    conn.commit()
    h_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': h_id, 'message': 'Registo clínico veterinário adicionado!'}), 201

@app.route('/api/history/<int:h_id>', methods=['DELETE'])
def delete_history(h_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM medical_history WHERE id = ?', (h_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de histórico eliminado.'})

# Export Data
@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pets.id, pets.name as Pet, pets.species as Espécie, pets.breed as Raça, pets.weight_kg as Peso_kg,
               owners.name as Proprietário, owners.phone as Telefone, owners.email as Email
        FROM pets
        JOIN owners ON pets.owner_id = owners.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_vetcraft.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando VetCraft AI SaaS no servidor local porta 6932...")
    app.run(host='0.0.0.0', port=6932, debug=True)
