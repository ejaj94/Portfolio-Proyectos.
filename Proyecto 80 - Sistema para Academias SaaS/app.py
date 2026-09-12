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

@app.route('/students')
def students():
    return render_template('students.html', active_page='students')

@app.route('/teachers')
def teachers():
    return render_template('teachers.html', active_page='teachers')

@app.route('/courses')
def courses():
    return render_template('courses.html', active_page='courses')

@app.route('/classes')
def classes():
    return render_template('classes.html', active_page='classes')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html', active_page='attendance')

@app.route('/payments')
def payments():
    return render_template('payments.html', active_page='payments')

@app.route('/grades')
def grades():
    return render_template('grades.html', active_page='grades')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM students WHERE status = "Ativo"')
    total_students = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM teachers')
    total_teachers = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM courses WHERE status = "Ativo"')
    active_courses = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM classes WHERE status = "Agendada"')
    upcoming_classes = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(amount) FROM payments WHERE status = "Pago"')
    total_revenue = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT COUNT(*) FROM payments WHERE status = "Pendente"')
    pending_payments = cursor.fetchone()[0]

    conn.close()
    return jsonify({
        'total_students': total_students,
        'total_teachers': total_teachers,
        'active_courses': active_courses,
        'upcoming_classes': upcoming_classes,
        'total_revenue': total_revenue,
        'pending_payments': pending_payments
    })

# Students API
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/students/create', methods=['POST'])
def create_student():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (name, email, phone, nif, birth_date, guardian_name, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('email'), data.get('phone'), data.get('nif'),
            data.get('birth_date'), data.get('guardian_name', ''), data.get('status', 'Ativo'), data.get('notes', '')
        ))
        conn.commit()
        sid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': sid, 'message': 'Aluno matriculado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: NIF já existente no sistema.'}), 400

@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (sid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ficha de aluno removida.'})

# Teachers API
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM teachers ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/teachers/create', methods=['POST'])
def create_teacher():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO teachers (name, email, phone, nif, qualification, hourly_rate, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('email'), data.get('phone'), data.get('nif'),
            data.get('qualification'), float(data.get('hourly_rate', 0)), data.get('notes', '')
        ))
        conn.commit()
        tid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': tid, 'message': 'Professor/Formador registado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: NIF já existente.'}), 400

@app.route('/api/teachers/<int:tid>', methods=['DELETE'])
def delete_teacher(tid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM teachers WHERE id = ?', (tid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Professor removido com sucesso.'})

# Courses API
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT courses.*, teachers.name as teacher_name
        FROM courses
        JOIN teachers ON courses.teacher_id = teachers.id
        ORDER BY courses.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/courses/create', methods=['POST'])
def create_course():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO courses (name, code, category, duration_hours, price, teacher_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('code'), data.get('category'),
            int(data.get('duration_hours', 0)), float(data.get('price', 0)),
            data.get('teacher_id'), data.get('status', 'Ativo')
        ))
        conn.commit()
        cid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': cid, 'message': 'Curso criado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: Código de curso já existente.'}), 400

@app.route('/api/courses/<int:cid>', methods=['DELETE'])
def delete_course(cid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE id = ?', (cid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Curso eliminado com sucesso.'})

# Classes API
@app.route('/api/classes', methods=['GET'])
def get_classes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT classes.*, courses.name as course_name, courses.code as course_code, teachers.name as teacher_name
        FROM classes
        JOIN courses ON classes.course_id = courses.id
        JOIN teachers ON courses.teacher_id = teachers.id
        ORDER BY classes.class_date ASC, classes.start_time ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/classes/create', methods=['POST'])
def create_class():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO classes (course_id, title, room, class_date, start_time, end_time, summary, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('course_id'), data.get('title'), data.get('room'),
        data.get('class_date'), data.get('start_time'), data.get('end_time'),
        data.get('summary', ''), data.get('status', 'Agendada')
    ))
    conn.commit()
    clid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': clid, 'message': 'Aula agendada com sucesso!'}), 201

@app.route('/api/classes/update-status/<int:clid>', methods=['POST'])
def update_class_status(clid):
    status = request.json.get('status')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE classes SET status = ? WHERE id = ?', (status, clid))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Estado da aula alterado para {status}.'})

@app.route('/api/classes/<int:clid>', methods=['DELETE'])
def delete_class(clid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM classes WHERE id = ?', (clid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Aula removida.'})

# Attendance API
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT attendance.*, students.name as student_name, classes.title as class_title, classes.class_date, courses.name as course_name
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        JOIN classes ON attendance.class_id = classes.id
        JOIN courses ON classes.course_id = courses.id
        ORDER BY classes.class_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/attendance/create', methods=['POST'])
def create_attendance():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO attendance (class_id, student_id, status, notes)
        VALUES (?, ?, ?, ?)
    ''', (
        data.get('class_id'), data.get('student_id'),
        data.get('status', 'Presente'), data.get('notes', '')
    ))
    conn.commit()
    att_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': att_id, 'message': 'Presença/Assiduidade registada com sucesso!'}), 201

@app.route('/api/attendance/<int:att_id>', methods=['DELETE'])
def delete_attendance(att_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM attendance WHERE id = ?', (att_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de assiduidade eliminado.'})

# Payments API
@app.route('/api/payments', methods=['GET'])
def get_payments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT payments.*, students.name as student_name, students.nif as student_nif, courses.name as course_name
        FROM payments
        JOIN students ON payments.student_id = students.id
        JOIN courses ON payments.course_id = courses.id
        ORDER BY payments.payment_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/payments/create', methods=['POST'])
def create_payment():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Get NIF from student if not provided
    student_id = data.get('student_id')
    cursor.execute('SELECT nif FROM students WHERE id = ?', (student_id,))
    srow = cursor.fetchone()
    nif_invoice = data.get('nif_invoice') or (srow['nif'] if srow else '999999990')

    cursor.execute('''
        INSERT INTO payments (student_id, course_id, amount, payment_date, payment_method, status, nif_invoice)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_id, data.get('course_id'), float(data.get('amount', 0)),
        data.get('payment_date'), data.get('payment_method'), data.get('status', 'Pago'), nif_invoice
    ))
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': pid, 'message': 'Pagamento / Propropina emitida com sucesso!'}), 201

@app.route('/api/payments/update-status/<int:pid>', methods=['POST'])
def update_payment_status(pid):
    status = request.json.get('status')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE payments SET status = ? WHERE id = ?', (status, pid))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Estado do pagamento alterado para {status}.'})

@app.route('/api/payments/<int:pid>', methods=['DELETE'])
def delete_payment(pid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM payments WHERE id = ?', (pid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de pagamento eliminado.'})

# Grades API
@app.route('/api/grades', methods=['GET'])
def get_grades():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT grades.*, students.name as student_name, courses.name as course_name
        FROM grades
        JOIN students ON grades.student_id = students.id
        JOIN courses ON grades.course_id = courses.id
        ORDER BY grades.evaluation_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/grades/create', methods=['POST'])
def create_grade():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO grades (student_id, course_id, evaluation_name, evaluation_date, score, max_score, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('student_id'), data.get('course_id'), data.get('evaluation_name'),
        data.get('evaluation_date'), float(data.get('score', 0)),
        float(data.get('max_score', 20.0)), data.get('comments', '')
    ))
    conn.commit()
    gid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': gid, 'message': 'Nota / Avaliação registada com sucesso!'}), 201

@app.route('/api/grades/<int:gid>', methods=['DELETE'])
def delete_grade(gid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM grades WHERE id = ?', (gid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de nota eliminado.'})

# Export API
@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT students.name as Aluno, students.nif as NIF, courses.name as Curso,
               payments.amount as Valor_EUR, payments.status as Estado_Pagamento, payments.payment_date as Data
        FROM payments
        JOIN students ON payments.student_id = students.id
        JOIN courses ON payments.course_id = courses.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_academycraft.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando AcademyCraft AI SaaS no servidor local porta 6933...")
    app.run(host='0.0.0.0', port=6933, debug=True)
