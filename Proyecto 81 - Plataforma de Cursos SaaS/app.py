import os
import sqlite3
import csv
import io
import uuid
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/courses')
def courses():
    return render_template('courses.html', active_page='courses')

@app.route('/lessons')
def lessons():
    return render_template('lessons.html', active_page='lessons')

@app.route('/videos')
def videos():
    return render_template('videos.html', active_page='videos')

@app.route('/users')
def users():
    return render_template('users.html', active_page='users')

@app.route('/progress')
def progress():
    return render_template('progress.html', active_page='progress')

@app.route('/certificates')
def certificates():
    return render_template('certificates.html', active_page='certificates')

@app.route('/payments')
def payments():
    return render_template('payments.html', active_page='payments')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM courses WHERE status = "Publicado"')
    total_courses = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM users WHERE role = "Aluno"')
    total_students = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM lessons')
    total_lessons = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM certificates')
    issued_certificates = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(amount) FROM payments WHERE status = "Concluído"')
    total_revenue = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT SUM(views_count) FROM videos')
    total_views = cursor.fetchone()[0] or 0

    conn.close()
    return jsonify({
        'total_courses': total_courses,
        'total_students': total_students,
        'total_lessons': total_lessons,
        'issued_certificates': issued_certificates,
        'total_revenue': total_revenue,
        'total_views': total_views
    })

# Users API
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/users/create', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, role, nif, phone, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('email'), data.get('role', 'Aluno'),
            data.get('nif'), data.get('phone'), data.get('status', 'Ativo')
        ))
        conn.commit()
        uid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': uid, 'message': 'Utilizador criado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: Email ou NIF já registado.'}), 400

@app.route('/api/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (uid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Utilizador eliminado.'})

# Courses API
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT courses.*, users.name as instructor_name, users.email as instructor_email,
               (SELECT COUNT(*) FROM lessons WHERE lessons.course_id = courses.id) as lessons_count
        FROM courses
        JOIN users ON courses.instructor_id = users.id
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
    cursor.execute('''
        INSERT INTO courses (title, category, instructor_id, level, price, total_duration_min, thumbnail_emoji, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'), data.get('category'), data.get('instructor_id'),
        data.get('level'), float(data.get('price', 0)), int(data.get('total_duration_min', 0)),
        data.get('thumbnail_emoji', '🎥'), data.get('status', 'Publicado')
    ))
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': cid, 'message': 'Curso publicado com sucesso!'}), 201

@app.route('/api/courses/<int:cid>', methods=['DELETE'])
def delete_course(cid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE id = ?', (cid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Curso eliminado.'})

# Lessons API
@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lessons.*, courses.title as course_title
        FROM lessons
        JOIN courses ON lessons.course_id = courses.id
        ORDER BY lessons.course_id ASC, lessons.module_number ASC, lessons.lesson_order ASC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/lessons/create', methods=['POST'])
def create_lesson():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO lessons (course_id, title, module_number, lesson_order, duration_min, is_free_preview)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('course_id'), data.get('title'), int(data.get('module_number', 1)),
        int(data.get('lesson_order', 1)), int(data.get('duration_min', 15)),
        1 if data.get('is_free_preview') else 0
    ))
    conn.commit()
    lid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': lid, 'message': 'Lição criada com sucesso!'}), 201

@app.route('/api/lessons/<int:lid>', methods=['DELETE'])
def delete_lesson(lid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lessons WHERE id = ?', (lid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Lição eliminada.'})

# Videos API
@app.route('/api/videos', methods=['GET'])
def get_videos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT videos.*, lessons.title as lesson_title, courses.title as course_title
        FROM videos
        JOIN lessons ON videos.lesson_id = lessons.id
        JOIN courses ON lessons.course_id = courses.id
        ORDER BY videos.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/videos/create', methods=['POST'])
def create_video():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO videos (lesson_id, video_title, video_url, video_quality, resolution, stream_type, views_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('lesson_id'), data.get('video_title'), data.get('video_url'),
        data.get('video_quality', '1080p Full HD'), data.get('resolution', '1920x1080'),
        data.get('stream_type', 'HLS / MP4'), int(data.get('views_count', 0))
    ))
    conn.commit()
    vid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': vid, 'message': 'Vídeo associado com sucesso!'}), 201

@app.route('/api/videos/<int:vid>', methods=['DELETE'])
def delete_video(vid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM videos WHERE id = ?', (vid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Vídeo eliminado.'})

# Progress API
@app.route('/api/progress', methods=['GET'])
def get_progress():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT progress.*, users.name as user_name, courses.title as course_title, lessons.title as lesson_title
        FROM progress
        JOIN users ON progress.user_id = users.id
        JOIN courses ON progress.course_id = courses.id
        JOIN lessons ON progress.lesson_id = lessons.id
        ORDER BY progress.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/progress/create', methods=['POST'])
def create_progress():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO progress (user_id, course_id, lesson_id, completion_pct, last_watched_timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('user_id'), data.get('course_id'), data.get('lesson_id'),
        float(data.get('completion_pct', 0.0)), data.get('last_watched_timestamp', '00:00'),
        data.get('status', 'Em Curso')
    ))
    conn.commit()
    prid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': prid, 'message': 'Progresso atualizado!'}), 201

@app.route('/api/progress/update/<int:prid>', methods=['POST'])
def update_progress(prid):
    pct = float(request.json.get('completion_pct', 100.0))
    status = 'Concluído' if pct >= 100.0 else 'Em Curso'
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE progress SET completion_pct = ?, status = ? WHERE id = ?', (pct, status, prid))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'Progresso atualizado para {pct}%.'})

@app.route('/api/progress/<int:prid>', methods=['DELETE'])
def delete_progress(prid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM progress WHERE id = ?', (prid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de progresso eliminado.'})

# Certificates API
@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT certificates.*, users.name as user_name, users.nif as user_nif, courses.title as course_title
        FROM certificates
        JOIN users ON certificates.user_id = users.id
        JOIN courses ON certificates.course_id = courses.id
        ORDER BY certificates.issue_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/certificates/create', methods=['POST'])
def create_certificate():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    code = f"CERT-{data.get('course_id')}-2026-{uuid.uuid4().hex[:5].upper()}"
    cursor.execute('''
        INSERT INTO certificates (user_id, course_id, certificate_code, issue_date, grade_achieved, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('user_id'), data.get('course_id'), code,
        data.get('issue_date'), float(data.get('grade_achieved', 100.0)), data.get('status', 'Válido')
    ))
    conn.commit()
    cert_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': cert_id, 'code': code, 'message': 'Certificado Digital emitido com sucesso!'}), 201

@app.route('/api/certificates/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM certificates WHERE id = ?', (cert_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Certificado revogado.'})

# Payments API
@app.route('/api/payments', methods=['GET'])
def get_payments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT payments.*, users.name as user_name, users.nif as user_nif, courses.title as course_title
        FROM payments
        JOIN users ON payments.user_id = users.id
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
    txn = f"TXN-PT-{uuid.uuid4().hex[:6].upper()}"
    cursor.execute('''
        INSERT INTO payments (user_id, course_id, amount, payment_date, payment_method, status, transaction_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('user_id'), data.get('course_id'), float(data.get('amount', 0)),
        data.get('payment_date'), data.get('payment_method'), data.get('status', 'Concluído'), txn
    ))
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': pid, 'transaction_id': txn, 'message': 'Inscrição & Pagamento efetuados com sucesso!'}), 201

@app.route('/api/payments/<int:pid>', methods=['DELETE'])
def delete_payment(pid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM payments WHERE id = ?', (pid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Registo de pagamento eliminado.'})

# Export API
@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT users.name as Aluno, users.email as Email, courses.title as Curso,
               payments.amount as Valor_EUR, payments.payment_method as Metodo, payments.payment_date as Data
        FROM payments
        JOIN users ON payments.user_id = users.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_learncraft.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando LearnCraft AI SaaS no servidor local porta 6934...")
    app.run(host='0.0.0.0', port=6934, debug=True)
