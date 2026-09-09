import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'timepulse.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    today_str = date.today().strftime("%Y-%m-%d")

    # Metrics Calculation
    cursor.execute("SELECT COUNT(*) as cnt FROM employees WHERE status = 'Ativo'")
    total_employees = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM attendance_logs WHERE log_date = ? AND clock_in IS NOT NULL", (today_str,))
    present_today = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM attendance_logs WHERE log_date = ? AND status = 'No Horário'", (today_str,))
    on_time_today = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(delay_minutes) as total_delay FROM attendance_logs WHERE log_date = ?", (today_str,))
    total_delay_min = cursor.fetchone()['total_delay'] or 0

    cursor.execute("SELECT SUM(total_hours) as sum_hours FROM attendance_logs WHERE log_date = ?", (today_str,))
    total_hours_today = cursor.fetchone()['sum_hours'] or 0.0

    punctuality_rate = round((on_time_today / present_today * 100), 1) if present_today > 0 else 100.0

    # Today's Logs with Employee & Shift Data
    cursor.execute("""
    SELECT a.*, e.emp_code, e.full_name, e.department, e.position, s.name as shift_name, s.start_time as shift_start, s.end_time as shift_end
    FROM attendance_logs a
    JOIN employees e ON a.employee_id = e.id
    JOIN shifts s ON e.shift_id = s.id
    WHERE a.log_date = ?
    ORDER BY a.clock_in DESC
    """, (today_str,))
    today_logs = [dict(r) for r in cursor.fetchall()]

    # Active Employees for Quick Punch Form
    cursor.execute("SELECT id, emp_code, full_name, position FROM employees WHERE status = 'Ativo' ORDER BY full_name ASC")
    employees = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        total_employees=total_employees,
        present_today=present_today,
        punctuality_rate=punctuality_rate,
        total_delay_min=total_delay_min,
        total_hours_today=total_hours_today,
        today_logs=today_logs,
        employees=employees,
        today_str=today_str
    )

@app.route('/terminal')
def terminal_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT e.id, e.emp_code, e.full_name, e.position, e.department, s.name as shift_name, s.start_time, s.end_time
    FROM employees e
    JOIN shifts s ON e.shift_id = s.id
    WHERE e.status = 'Ativo'
    ORDER BY e.emp_code ASC
    """)
    employees = [dict(r) for r in cursor.fetchall()]
    conn.close()

    today_str = date.today().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    return render_template('terminal.html', employees=employees, today_str=today_str, now_time=now_time)

@app.route('/employees')
def employees_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT e.*, s.name as shift_name, s.start_time, s.end_time
    FROM employees e
    JOIN shifts s ON e.shift_id = s.id
    ORDER BY e.emp_code ASC
    """)
    employees = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM shifts ORDER BY id ASC")
    shifts = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('employees.html', employees=employees, shifts=shifts)

@app.route('/schedules')
def schedules_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT s.*, COUNT(e.id) as assigned_employees
    FROM shifts s
    LEFT JOIN employees e ON s.id = e.shift_id
    GROUP BY s.id
    ORDER BY s.id ASC
    """)
    shifts = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('schedules.html', shifts=shifts)

@app.route('/reports')
def reports_page():
    conn = get_db()
    cursor = conn.cursor()

    selected_date = request.args.get('date', date.today().strftime("%Y-%m-%d"))

    cursor.execute("""
    SELECT a.*, e.emp_code, e.full_name, e.department, e.position, s.name as shift_name, s.start_time, s.end_time
    FROM attendance_logs a
    JOIN employees e ON a.employee_id = e.id
    JOIN shifts s ON e.shift_id = s.id
    WHERE a.log_date = ?
    ORDER BY a.clock_in ASC
    """, (selected_date,))
    logs = [dict(r) for r in cursor.fetchall()]

    # Summary calculations for selected date
    total_logs = len(logs)
    total_delays = sum(1 for l in logs if l['delay_minutes'] > 0)
    sum_delay_min = sum(l['delay_minutes'] for l in logs)
    sum_worked_hours = sum(l['total_hours'] for l in logs)

    conn.close()
    return render_template(
        'reports.html',
        logs=logs,
        selected_date=selected_date,
        total_logs=total_logs,
        total_delays=total_delays,
        sum_delay_min=sum_delay_min,
        sum_worked_hours=sum_worked_hours
    )

# API ENDPOINTS

@app.route('/api/punch', methods=['POST'])
def api_punch():
    try:
        data = request.get_json() or {}
        emp_identifier = data.get('employee_id') # Can be ID or Code

        if not emp_identifier:
            return jsonify({'success': False, 'message': 'Por favor selecione ou introduza o código de colaborador.'}), 400

        conn = get_db()
        cursor = conn.cursor()

        # Find employee
        if str(emp_identifier).isdigit():
            cursor.execute("SELECT e.*, s.start_time, s.end_time, s.grace_minutes, s.target_hours FROM employees e JOIN shifts s ON e.shift_id = s.id WHERE e.id = ?", (emp_identifier,))
        else:
            cursor.execute("SELECT e.*, s.start_time, s.end_time, s.grace_minutes, s.target_hours FROM employees e JOIN shifts s ON e.shift_id = s.id WHERE e.emp_code = ?", (str(emp_identifier).strip().upper(),))

        emp = cursor.fetchone()
        if not emp:
            conn.close()
            return jsonify({'success': False, 'message': f'Colaborador "{emp_identifier}" não encontrado.'}), 404

        today_str = date.today().strftime("%Y-%m-%d")
        now_dt = datetime.now()
        now_time_str = now_dt.strftime("%H:%M")

        # Check existing attendance log for today
        cursor.execute("SELECT * FROM attendance_logs WHERE employee_id = ? AND log_date = ?", (emp['id'], today_str))
        existing_log = cursor.fetchone()

        if existing_log:
            if not existing_log['clock_out']:
                # Clock Out Execution
                clock_in_dt = datetime.strptime(f"{today_str} {existing_log['clock_in']}", "%Y-%m-%d %H:%M")
                hours_worked = round((now_dt - clock_in_dt).total_seconds() / 3600.0, 2)
                target_h = emp['target_hours'] or 8.0
                overtime = max(round(hours_worked - target_h, 2), 0.0)

                cursor.execute("""
                UPDATE attendance_logs
                SET clock_out = ?, total_hours = ?, overtime_hours = ?
                WHERE id = ?
                """, (now_time_str, hours_worked, overtime, existing_log['id']))
                conn.commit()
                conn.close()

                return jsonify({
                    'success': True,
                    'action': 'CLOCK_OUT',
                    'employee_name': emp['full_name'],
                    'time': now_time_str,
                    'hours_worked': hours_worked,
                    'message': f'👋 Saída registada às {now_time_str} para {emp["full_name"]}. Total trabalhado: {hours_worked}h.'
                })
            else:
                conn.close()
                return jsonify({'success': False, 'message': f'O colaborador {emp["full_name"]} já concluiu o registo de entrada e saída hoje.'}), 400
        else:
            # Clock In Execution
            shift_start_dt = datetime.strptime(f"{today_str} {emp['start_time']}", "%Y-%m-%d %H:%M")
            grace_min = emp['grace_minutes'] or 15

            delay_minutes = 0
            status = 'No Horário'

            if now_dt > shift_start_dt + timedelta(minutes=grace_min):
                delay_minutes = int((now_dt - shift_start_dt).total_seconds() / 60)
                status = 'Atrasado'

            cursor.execute("""
            INSERT INTO attendance_logs (employee_id, log_date, clock_in, delay_minutes, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (emp['id'], today_str, now_time_str, delay_minutes, status, f"Ponto de entrada às {now_time_str}"))

            conn.commit()
            conn.close()

            status_emoji = '✅' if status == 'No Horário' else '⚠️'
            delay_text = f" ({delay_minutes} min de atraso)" if delay_minutes > 0 else ""

            return jsonify({
                'success': True,
                'action': 'CLOCK_IN',
                'employee_name': emp['full_name'],
                'time': now_time_str,
                'status': status,
                'delay_minutes': delay_minutes,
                'message': f'{status_emoji} Entrada registada às {now_time_str} para {emp["full_name"]} [{status}]{delay_text}.'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/employee/save', methods=['POST'])
def api_save_employee():
    try:
        data = request.get_json() or {}
        e_id = data.get('id')
        emp_code = data.get('emp_code', '').strip().upper()
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        department = data.get('department', 'Geral').strip()
        position = data.get('position', '').strip()
        shift_id = data.get('shift_id', 1)

        if not all([emp_code, full_name, email, position]):
            return jsonify({'success': False, 'message': 'Por favor preencha todos os campos obrigatórios.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        if e_id:
            cursor.execute("""
            UPDATE employees
            SET emp_code = ?, full_name = ?, email = ?, department = ?, position = ?, shift_id = ?
            WHERE id = ?
            """, (emp_code, full_name, email, department, position, shift_id, e_id))
        else:
            cursor.execute("""
            INSERT INTO employees (emp_code, full_name, email, department, position, shift_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (emp_code, full_name, email, department, position, shift_id, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Colaborador "{full_name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/schedule/save', methods=['POST'])
def api_save_schedule():
    try:
        data = request.get_json() or {}
        s_id = data.get('id')
        name = data.get('name', '').strip()
        start_time = data.get('start_time', '09:00').strip()
        end_time = data.get('end_time', '18:00').strip()
        grace_minutes = int(data.get('grace_minutes', 15))
        target_hours = float(data.get('target_hours', 8.0))

        if not name:
            return jsonify({'success': False, 'message': 'Nome do turno é obrigatório.'}), 400

        conn = get_db()
        cursor = conn.cursor()

        if s_id:
            cursor.execute("""
            UPDATE shifts
            SET name = ?, start_time = ?, end_time = ?, grace_minutes = ?, target_hours = ?
            WHERE id = ?
            """, (name, start_time, end_time, grace_minutes, target_hours, s_id))
        else:
            cursor.execute("""
            INSERT INTO shifts (name, start_time, end_time, grace_minutes, target_hours)
            VALUES (?, ?, ?, ?, ?)
            """, (name, start_time, end_time, grace_minutes, target_hours))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Turno "{name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_attendance(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.id, a.log_date, e.emp_code, e.full_name, e.department, e.position, a.clock_in, a.clock_out, a.delay_minutes, a.total_hours, a.overtime_hours, a.status
    FROM attendance_logs a
    JOIN employees e ON a.employee_id = e.id
    ORDER BY a.log_date DESC, a.clock_in DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=relatorio_assiduidade_timepulse.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID Log', 'Data', 'Código EMP', 'Nome Colaborador', 'Departamento', 'Cargo', 'Entrada', 'Saída', 'Atraso (Min)', 'Horas Trabalhadas', 'Horas Extra', 'Estado'])

        for r in rows:
            writer.writerow([r['id'], r['log_date'], r['emp_code'], r['full_name'], r['department'], r['position'], r['clock_in'] or '', r['clock_out'] or '', r['delay_minutes'], r['total_hours'], r['overtime_hours'], r['status']])

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=relatorio_assiduidade_timepulse.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - TimePulse AI SaaS na porta 6921...")
    app.run(host='127.0.0.1', port=6921, debug=False, use_reloader=False)
