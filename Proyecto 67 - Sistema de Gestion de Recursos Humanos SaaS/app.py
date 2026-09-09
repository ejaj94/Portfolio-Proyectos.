import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'hr_talent.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Total Employees
    cursor.execute("SELECT COUNT(*) as cnt FROM employees")
    total_employees = cursor.fetchone()['cnt']

    # Total Active Employees
    cursor.execute("SELECT COUNT(*) as cnt FROM employees WHERE status = 'Ativo'")
    active_employees = cursor.fetchone()['cnt']

    # Total Departments
    cursor.execute("SELECT COUNT(*) as cnt FROM departments")
    total_departments = cursor.fetchone()['cnt']

    # Pending Vacations
    cursor.execute("SELECT COUNT(*) as cnt FROM vacations WHERE status = 'Pendente'")
    pending_vacations = cursor.fetchone()['cnt']

    # Total Monthly Payroll Budget
    cursor.execute("SELECT SUM(salary) as sum_salary FROM employees WHERE status = 'Ativo'")
    payroll_sum = cursor.fetchone()['sum_salary'] or 0.0

    # Today Attendance Count
    today_str = date.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) as cnt FROM attendance WHERE date = ? AND status IN ('Presente', 'Atrasado')", (today_str,))
    present_today = cursor.fetchone()['cnt']

    # Pending Vacation Requests List with Employee Info
    cursor.execute("""
    SELECT v.*, e.full_name, e.position, d.name as dept_name
    FROM vacations v
    JOIN employees e ON v.employee_id = e.id
    JOIN departments d ON e.department_id = d.id
    WHERE v.status = 'Pendente'
    ORDER BY v.requested_at DESC
    """)
    pending_vacations_list = [dict(r) for r in cursor.fetchall()]

    # Today's Attendance List
    cursor.execute("""
    SELECT a.*, e.full_name, e.position, d.name as dept_name
    FROM attendance a
    JOIN employees e ON a.employee_id = e.id
    JOIN departments d ON e.department_id = d.id
    WHERE a.date = ?
    ORDER BY a.clock_in DESC
    """, (today_str,))
    today_attendance_list = [dict(r) for r in cursor.fetchall()]

    conn.close()

    attendance_rate = round((present_today / total_employees * 100), 1) if total_employees > 0 else 0.0

    return render_template(
        'dashboard.html',
        total_employees=total_employees,
        active_employees=active_employees,
        total_departments=total_departments,
        pending_vacations=pending_vacations,
        payroll_sum=payroll_sum,
        present_today=present_today,
        attendance_rate=attendance_rate,
        pending_vacations_list=pending_vacations_list,
        today_attendance_list=today_attendance_list
    )

@app.route('/employees')
def employees_page():
    conn = get_db()
    cursor = conn.cursor()

    dept_filter = request.args.get('department_id')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT e.*, d.name as department_name, d.color as department_color
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    WHERE 1=1
    """
    params = []

    if dept_filter:
        query += " AND e.department_id = ?"
        params.append(dept_filter)

    if search_q:
        query += " AND (e.full_name LIKE ? OR e.email LIKE ? OR e.position LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " ORDER BY e.id DESC"
    cursor.execute(query, params)
    employees = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM departments ORDER BY name ASC")
    departments = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('employees.html', employees=employees, departments=departments, selected_dept=dept_filter, search_q=search_q)

@app.route('/departments')
def departments_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT d.*, 
           COUNT(e.id) as employee_count,
           COALESCE(SUM(e.salary), 0) as total_dept_salary
    FROM departments d
    LEFT JOIN employees e ON d.id = e.department_id
    GROUP BY d.id
    ORDER BY d.id ASC
    """)
    departments = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('departments.html', departments=departments)

@app.route('/vacations')
def vacations_page():
    conn = get_db()
    cursor = conn.cursor()

    # Vacations List
    cursor.execute("""
    SELECT v.*, e.full_name, e.position, d.name as dept_name
    FROM vacations v
    JOIN employees e ON v.employee_id = e.id
    JOIN departments d ON e.department_id = d.id
    ORDER BY v.requested_at DESC
    """)
    vacations = [dict(r) for r in cursor.fetchall()]

    # Absences List
    cursor.execute("""
    SELECT a.*, e.full_name, e.position, d.name as dept_name
    FROM absences a
    JOIN employees e ON a.employee_id = e.id
    JOIN departments d ON e.department_id = d.id
    ORDER BY a.date DESC
    """)
    absences = [dict(r) for r in cursor.fetchall()]

    # All Active Employees for Form
    cursor.execute("SELECT id, full_name, position FROM employees WHERE status != 'Inativo' ORDER BY full_name ASC")
    employees = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('vacations.html', vacations=vacations, absences=absences, employees=employees)

@app.route('/attendance')
def attendance_page():
    conn = get_db()
    cursor = conn.cursor()

    today_str = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT a.*, e.full_name, e.position, e.avatar_color, d.name as dept_name
    FROM attendance a
    JOIN employees e ON a.employee_id = e.id
    JOIN departments d ON e.department_id = d.id
    ORDER BY a.date DESC, a.clock_in DESC
    """)
    attendance_records = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, full_name, position FROM employees WHERE status = 'Ativo' ORDER BY full_name ASC")
    employees = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('attendance.html', attendance_records=attendance_records, employees=employees, today_str=today_str)

@app.route('/documents')
def documents_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT doc.*, e.full_name, e.position, d.name as dept_name
    FROM documents doc
    JOIN employees e ON doc.employee_id = e.id
    JOIN departments d ON e.department_id = d.id
    ORDER BY doc.uploaded_at DESC
    """)
    documents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, full_name FROM employees ORDER BY full_name ASC")
    employees = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('documents.html', documents=documents, employees=employees)

# API ENDPOINTS

@app.route('/api/clock-in', methods=['POST'])
def api_clock_in():
    try:
        data = request.get_json() or {}
        employee_id = data.get('employee_id')
        status = data.get('status', 'Presente')

        if not employee_id:
            return jsonify({'success': False, 'message': 'Selecione um colaborador.'}), 400

        today_str = date.today().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")

        conn = get_db()
        cursor = conn.cursor()

        # Check existing record for today
        cursor.execute("SELECT id, clock_in, clock_out FROM attendance WHERE employee_id = ? AND date = ?", (employee_id, today_str))
        existing = cursor.fetchone()

        if existing:
            if not existing['clock_out']:
                # Clock out
                cursor.execute("""
                UPDATE attendance 
                SET clock_out = ?, total_hours = 8.0 
                WHERE id = ?
                """, (now_time, existing['id']))
                conn.commit()
                conn.close()
                return jsonify({'success': True, 'message': f'Saída registada às {now_time} com sucesso!'})
            else:
                conn.close()
                return jsonify({'success': False, 'message': 'Este colaborador já registou entrada e saída hoje.'}), 400
        else:
            # Clock in
            cursor.execute("""
            INSERT INTO attendance (employee_id, date, clock_in, status)
            VALUES (?, ?, ?, ?)
            """, (employee_id, today_str, now_time, status))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': f'Entrada registada às {now_time} com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/vacation/status/<int:vacation_id>', methods=['POST'])
def api_update_vacation_status(vacation_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Aprovado')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE vacations SET status = ? WHERE id = ?", (new_status, vacation_id))
        
        # If approved, update employee status to "De Férias"
        if new_status == 'Aprovado':
            cursor.execute("SELECT employee_id FROM vacations WHERE id = ?", (vacation_id,))
            v = cursor.fetchone()
            if v:
                cursor.execute("UPDATE employees SET status = 'De Férias' WHERE id = ?", (v['employee_id'],))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Estado do pedido de férias alterado para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/employee/save', methods=['POST'])
def api_save_employee():
    try:
        data = request.get_json() or {}
        e_id = data.get('id')
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        department_id = data.get('department_id')
        position = data.get('position', '').strip()
        salary = float(data.get('salary', 0.0))
        status = data.get('status', 'Ativo')
        hire_date = data.get('hire_date', date.today().strftime("%Y-%m-%d"))
        avatar_color = data.get('avatar_color', '#2563EB')

        if not all([full_name, email, department_id, position]):
            return jsonify({'success': False, 'message': 'Por favor preencha todos os campos obrigatórios.'}), 400

        conn = get_db()
        cursor = conn.cursor()

        if e_id:
            cursor.execute("""
            UPDATE employees
            SET full_name = ?, email = ?, phone = ?, department_id = ?, position = ?, salary = ?, status = ?, hire_date = ?, avatar_color = ?
            WHERE id = ?
            """, (full_name, email, phone, department_id, position, salary, status, hire_date, avatar_color, e_id))
        else:
            cursor.execute("""
            INSERT INTO employees (full_name, email, phone, department_id, position, salary, status, hire_date, avatar_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (full_name, email, phone, department_id, position, salary, status, hire_date, avatar_color))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Colaborador "{full_name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/employee/delete/<int:employee_id>', methods=['POST', 'DELETE'])
def api_delete_employee(employee_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        cursor.execute("DELETE FROM vacations WHERE employee_id = ?", (employee_id,))
        cursor.execute("DELETE FROM attendance WHERE employee_id = ?", (employee_id,))
        cursor.execute("DELETE FROM documents WHERE employee_id = ?", (employee_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Colaborador e registos associados eliminados.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/department/save', methods=['POST'])
def api_save_department():
    try:
        data = request.get_json() or {}
        d_id = data.get('id')
        name = data.get('name', '').strip()
        manager_name = data.get('manager_name', '').strip()
        budget = float(data.get('budget', 0.0))
        color = data.get('color', '#2563EB').strip()

        if not name or not manager_name:
            return jsonify({'success': False, 'message': 'Nome e Gestor do departamento são obrigatórios.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        if d_id:
            cursor.execute("""
            UPDATE departments
            SET name = ?, manager_name = ?, budget = ?, color = ?
            WHERE id = ?
            """, (name, manager_name, budget, color, d_id))
        else:
            cursor.execute("""
            INSERT INTO departments (name, manager_name, budget, color, created_at)
            VALUES (?, ?, ?, ?, ?)
            """, (name, manager_name, budget, color, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Departamento "{name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/vacation/save', methods=['POST'])
def api_save_vacation():
    try:
        data = request.get_json() or {}
        employee_id = data.get('employee_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        reason = data.get('reason', '').strip()

        if not all([employee_id, start_date, end_date]):
            return jsonify({'success': False, 'message': 'Preencha o colaborador e as datas.'}), 400

        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(end_date, "%Y-%m-%d")
        days_count = max((d2 - d1).days + 1, 1)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO vacations (employee_id, start_date, end_date, days_count, status, reason, requested_at)
        VALUES (?, ?, ?, ?, 'Pendente', ?, ?)
        """, (employee_id, start_date, end_date, days_count, reason, now_str))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Pedido de férias submetido com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/document/save', methods=['POST'])
def api_save_document():
    try:
        data = request.get_json() or {}
        employee_id = data.get('employee_id')
        title = data.get('title', '').strip()
        category = data.get('category', 'Contrato')
        file_url = data.get('file_url', '/docs/documento_exemplo.pdf').strip()

        if not employee_id or not title:
            return jsonify({'success': False, 'message': 'Colaborador e Título são obrigatórios.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO documents (employee_id, title, category, file_url, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
        """, (employee_id, title, category, file_url, now_str))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Documento "{title}" registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_hr(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT e.id, e.full_name, e.email, e.phone, d.name as department, e.position, e.salary, e.status, e.hire_date
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    ORDER BY e.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=relatorio_colaboradores_rrhh.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Nome Completo', 'E-mail', 'Telefone', 'Departamento', 'Cargo', 'Salário (€)', 'Estado', 'Data Contratação'])

        for r in rows:
            writer.writerow([r['id'], r['full_name'], r['email'], r['phone'], r['department'], r['position'], f"{r['salary']:.2f}", r['status'], r['hire_date']])

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=relatorio_colaboradores_rrhh.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - HRTalent AI SaaS na porta 6920...")
    app.run(host='127.0.0.1', port=6920, debug=False, use_reloader=False)
