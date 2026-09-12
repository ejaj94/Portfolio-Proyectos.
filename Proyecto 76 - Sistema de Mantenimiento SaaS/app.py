import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'maintaincraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Metrics
    cursor.execute("SELECT COUNT(*) as cnt FROM equipment WHERE status = 'Ativo'")
    active_equipment = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM maintenances WHERE status IN ('Agendado', 'Em Execução')")
    pending_orders = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM incidents WHERE status IN ('Aberto', 'Em Análise', 'Em Reparação')")
    open_incidents = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(total_cost) as total FROM maintenances")
    total_cost_val = cursor.fetchone()['total'] or 0.0

    # Recent Work Orders
    cursor.execute("""
    SELECT m.*, e.name as equipment_name, e.equipment_code, e.location, t.name as technician_name
    FROM maintenances m
    JOIN equipment e ON m.equipment_id = e.id
    JOIN technicians t ON m.technician_id = t.id
    ORDER BY m.id DESC
    LIMIT 5
    """)
    recent_orders = [dict(r) for r in cursor.fetchall()]

    # Active Incidents
    cursor.execute("""
    SELECT i.*, e.name as equipment_name, e.equipment_code, e.location
    FROM incidents i
    JOIN equipment e ON i.equipment_id = e.id
    ORDER BY i.id DESC
    LIMIT 4
    """)
    recent_incidents = [dict(r) for r in cursor.fetchall()]

    # Dropdowns for Modals
    cursor.execute("SELECT id, name, equipment_code, category FROM equipment ORDER BY name ASC")
    equipment_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, specialty FROM technicians ORDER BY name ASC")
    technicians_list = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        active_equipment=active_equipment,
        pending_orders=pending_orders,
        open_incidents=open_incidents,
        total_cost_val=round(total_cost_val, 2),
        recent_orders=recent_orders,
        recent_incidents=recent_incidents,
        equipment_list=equipment_list,
        technicians_list=technicians_list
    )

@app.route('/equipment')
def equipment_page():
    conn = get_db()
    cursor = conn.cursor()

    cat_filter = request.args.get('category')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT e.*, COUNT(m.id) as maintenance_count
    FROM equipment e
    LEFT JOIN maintenances m ON e.id = m.equipment_id
    WHERE 1=1
    """
    params = []

    if cat_filter:
        query += " AND e.category = ?"
        params.append(cat_filter)

    if search_q:
        query += " AND (e.equipment_code LIKE ? OR e.name LIKE ? OR e.location LIKE ? OR e.serial_number LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " GROUP BY e.id ORDER BY e.id DESC"
    cursor.execute(query, params)
    equipments = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT category FROM equipment ORDER BY category ASC")
    categories = [r['category'] for r in cursor.fetchall()]

    conn.close()
    return render_template('equipment.html', equipments=equipments, categories=categories, selected_cat=cat_filter, search_q=search_q)

@app.route('/technicians')
def technicians_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT t.*, COUNT(m.id) as assigned_orders
    FROM technicians t
    LEFT JOIN maintenances m ON t.id = m.technician_id AND m.status IN ('Agendado', 'Em Execução')
    GROUP BY t.id
    ORDER BY t.id DESC
    """)
    technicians = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('technicians.html', technicians=technicians)

@app.route('/maintenances')
def maintenances_page():
    conn = get_db()
    cursor = conn.cursor()

    type_filter = request.args.get('type')
    status_filter = request.args.get('status')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT m.*, e.name as equipment_name, e.equipment_code, e.location, t.name as technician_name
    FROM maintenances m
    JOIN equipment e ON m.equipment_id = e.id
    JOIN technicians t ON m.technician_id = t.id
    WHERE 1=1
    """
    params = []

    if type_filter:
        query += " AND m.type = ?"
        params.append(type_filter)

    if status_filter:
        query += " AND m.status = ?"
        params.append(status_filter)

    if search_q:
        query += " AND (m.order_code LIKE ? OR e.name LIKE ? OR e.equipment_code LIKE ? OR t.name LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " ORDER BY m.id DESC"
    cursor.execute(query, params)
    maintenances = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, equipment_code FROM equipment ORDER BY name ASC")
    equipment_list = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, specialty FROM technicians ORDER BY name ASC")
    technicians_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template(
        'maintenances.html',
        maintenances=maintenances,
        selected_type=type_filter,
        selected_status=status_filter,
        search_q=search_q,
        equipment_list=equipment_list,
        technicians_list=technicians_list
    )

@app.route('/incidents')
def incidents_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    query = """
    SELECT i.*, e.name as equipment_name, e.equipment_code, e.location
    FROM incidents i
    JOIN equipment e ON i.equipment_id = e.id
    WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND i.status = ?"
        params.append(status_filter)

    query += " ORDER BY i.id DESC"
    cursor.execute(query, params)
    incidents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, equipment_code FROM equipment ORDER BY name ASC")
    equipment_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('incidents.html', incidents=incidents, selected_status=status_filter, equipment_list=equipment_list)

@app.route('/calendar')
def calendar_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT m.*, e.name as equipment_name, e.equipment_code, t.name as technician_name
    FROM maintenances m
    JOIN equipment e ON m.equipment_id = e.id
    JOIN technicians t ON m.technician_id = t.id
    ORDER BY m.scheduled_date ASC
    """)
    events = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('calendar.html', events=events)

@app.route('/costs')
def costs_page():
    conn = get_db()
    cursor = conn.cursor()

    # Costs by Equipment Category
    cursor.execute("""
    SELECT e.category, SUM(m.labor_cost) as total_labor, SUM(m.parts_cost) as total_parts, SUM(m.total_cost) as grand_total
    FROM maintenances m
    JOIN equipment e ON m.equipment_id = e.id
    GROUP BY e.category
    ORDER BY grand_total DESC
    """)
    category_costs = [dict(r) for r in cursor.fetchall()]

    # Costs by Maintenance Type
    cursor.execute("""
    SELECT m.type, COUNT(m.id) as count, SUM(m.labor_cost) as total_labor, SUM(m.parts_cost) as total_parts, SUM(m.total_cost) as grand_total
    FROM maintenances m
    GROUP BY m.type
    ORDER BY grand_total DESC
    """)
    type_costs = [dict(r) for r in cursor.fetchall()]

    # Detailed Cost Table
    cursor.execute("""
    SELECT m.*, e.name as equipment_name, e.equipment_code, t.name as technician_name
    FROM maintenances m
    JOIN equipment e ON m.equipment_id = e.id
    JOIN technicians t ON m.technician_id = t.id
    ORDER BY m.total_cost DESC
    """)
    detailed_costs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('costs.html', category_costs=category_costs, type_costs=type_costs, detailed_costs=detailed_costs)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT l.*, m.order_code, i.incident_code
    FROM intervention_logs l
    LEFT JOIN maintenances m ON l.maintenance_id = m.id
    LEFT JOIN incidents i ON l.incident_id = i.id
    ORDER BY l.id DESC
    """)
    logs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('history.html', logs=logs)

# API ENDPOINTS

@app.route('/api/equipment/create', methods=['POST'])
def api_create_equipment():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        category = data.get('category', '').strip()
        serial_number = data.get('serial_number', '').strip().upper()
        location = data.get('location', '').strip()

        if not name or not category or not serial_number or not location:
            return jsonify({'success': False, 'message': 'Preencha o nome, categoria, nº de série e localização.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM equipment")
        code_num = cursor.fetchone()['cnt'] + 10
        eqp_code = f"EQP-{category[:3].upper()}-{code_num:02d}"

        cursor.execute("""
        INSERT INTO equipment (equipment_code, name, category, serial_number, location, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'Ativo', ?)
        """, (eqp_code, name, category, serial_number, location, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Equipamento "{eqp_code}" cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/technician/create', methods=['POST'])
def api_create_technician():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        specialty = data.get('specialty', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()

        if not name or not specialty or not email:
            return jsonify({'success': False, 'message': 'Preencha o nome, especialidade e email.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO technicians (name, specialty, email, phone, status, created_at)
        VALUES (?, ?, ?, ?, 'Disponível', ?)
        """, (name, specialty, email, phone, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Técnico "{name}" registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/maintenance/create', methods=['POST'])
def api_create_maintenance():
    try:
        data = request.get_json() or {}
        equipment_id = data.get('equipment_id')
        technician_id = data.get('technician_id')
        m_type = data.get('type', 'Preventiva')
        priority = data.get('priority', 'Média')
        scheduled_date = data.get('scheduled_date', '').strip()
        estimated_hours = float(data.get('estimated_hours', 2.0))
        labor_cost = float(data.get('labor_cost', 0.0))
        parts_cost = float(data.get('parts_cost', 0.0))
        description = data.get('description', '').strip()

        if not equipment_id or not technician_id or not scheduled_date or not description:
            return jsonify({'success': False, 'message': 'Selecione o equipamento, técnico, data agendada e descrição.'}), 400

        total_cost = labor_cost + parts_cost
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM maintenances")
        code_num = cursor.fetchone()['cnt'] + 106
        order_code = f"OT-2026-{code_num}"

        cursor.execute("""
        INSERT INTO maintenances (order_code, equipment_id, technician_id, type, priority, scheduled_date, estimated_hours, labor_cost, parts_cost, total_cost, description, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Agendado', ?)
        """, (order_code, equipment_id, technician_id, m_type, priority, scheduled_date, estimated_hours, labor_cost, parts_cost, total_cost, description, now_str))

        m_id = cursor.lastrowid

        # Insert intervention log
        cursor.execute("SELECT name FROM technicians WHERE id = ?", (technician_id,))
        tech_row = cursor.fetchone()
        tech_name = tech_row['name'] if tech_row else "Técnico Responsável"

        cursor.execute("""
        INSERT INTO intervention_logs (maintenance_id, action, technician, parts_used, cost, timestamp, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (m_id, f"Agendamento de Manutenção {m_type}", tech_name, "N/A (Aguardando Execução)", total_cost, now_str, f"Ordem de trabalho {order_code} criada com prioridade {priority}."))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Ordem de trabalho "{order_code}" agendada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/maintenance/status/<int:m_id>', methods=['POST'])
def api_update_maintenance_status(m_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Concluído')
        notes = data.get('notes', 'Atualização de intervenção.').strip()
        parts_used = data.get('parts_used', 'Peças padrão de reposição').strip()
        technician = data.get('technician', 'Eng. Enmanuel Jimenez')

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        completed_date = now_str if new_status == 'Concluído' else None

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE maintenances SET status = ?, completed_date = COALESCE(?, completed_date) WHERE id = ?
        """, (new_status, completed_date, m_id))

        cursor.execute("""
        INSERT INTO intervention_logs (maintenance_id, action, technician, parts_used, cost, timestamp, notes)
        VALUES (?, ?, ?, ?, 0.0, ?, ?)
        """, (m_id, f"Estado Alterado para '{new_status}'", technician, parts_used, now_str, notes))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Ordem de trabalho alterada para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/incident/create', methods=['POST'])
def api_create_incident():
    try:
        data = request.get_json() or {}
        equipment_id = data.get('equipment_id')
        reported_by = data.get('reported_by', 'Operador de Turno').strip()
        severity = data.get('severity', 'Média')
        description = data.get('description', '').strip()

        if not equipment_id or not description:
            return jsonify({'success': False, 'message': 'Selecione o equipamento e descreva a anomalia.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM incidents")
        code_num = cursor.fetchone()['cnt'] + 8903
        incident_code = f"INC-{code_num}"

        cursor.execute("""
        INSERT INTO incidents (incident_code, equipment_id, reported_by, severity, description, status, reported_at)
        VALUES (?, ?, ?, ?, ?, 'Aberto', ?)
        """, (incident_code, equipment_id, reported_by, severity, description, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Incidência "{incident_code}" reportada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/incident/status/<int:inc_id>', methods=['POST'])
def api_update_incident_status(inc_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Resolvido')
        technician = data.get('technician', 'Eng. Enmanuel Jimenez')
        notes = data.get('notes', 'Incidência sanada e reativada.').strip()

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        resolved_at = now_str if new_status == 'Resolvido' else None

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE incidents SET status = ?, resolved_at = COALESCE(?, resolved_at) WHERE id = ?
        """, (new_status, resolved_at, inc_id))

        cursor.execute("""
        INSERT INTO intervention_logs (incident_id, action, technician, parts_used, cost, timestamp, notes)
        VALUES (?, ?, ?, 'Componentes de correção', 0.0, ?, ?)
        """, (inc_id, f"Incidência '{new_status}'", technician, now_str, notes))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Incidência atualizada para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT m.order_code, e.equipment_code, e.name as equipment_name, e.category, t.name as technician_name, m.type, m.priority, m.scheduled_date, m.completed_date, m.total_cost, m.status
    FROM maintenances m
    JOIN equipment e ON m.equipment_id = e.id
    JOIN technicians t ON m.technician_id = t.id
    ORDER BY m.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        return Response(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=maintaincraft_export.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Ordem Trabalho', 'Código Equipamento', 'Nome Equipamento', 'Categoria', 'Técnico', 'Tipo', 'Prioridade', 'Data Agendada', 'Data Conclusão', 'Custo Total (€)', 'Estado'])
        for r in rows:
            writer.writerow([r['order_code'], r['equipment_code'], r['equipment_name'], r['category'], r['technician_name'], r['type'], r['priority'], r['scheduled_date'], r['completed_date'], r['total_cost'], r['status']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=maintaincraft_export.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6929, debug=True)
