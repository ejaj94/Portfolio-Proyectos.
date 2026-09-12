import os
import sqlite3
import csv
import io
import uuid
import datetime
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/certificates')
def certificates():
    return render_template('certificates.html', active_page='certificates')

@app.route('/templates')
def templates():
    return render_template('templates.html', active_page='templates')

@app.route('/recipients')
def recipients():
    return render_template('recipients.html', active_page='recipients')

@app.route('/verify')
def verify():
    return render_template('verify.html', active_page='verify')

@app.route('/history')
def history():
    return render_template('history.html', active_page='history')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM certificates WHERE status = "Válido"')
    valid_certificates = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM recipients')
    total_recipients = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM templates WHERE status = "Ativo"')
    active_templates = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM verification_logs')
    total_verifications = cursor.fetchone()[0]

    conn.close()
    return jsonify({
        'valid_certificates': valid_certificates,
        'total_recipients': total_recipients,
        'active_templates': active_templates,
        'total_verifications': total_verifications
    })

# Recipients API
@app.route('/api/recipients', methods=['GET'])
def get_recipients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipients ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/recipients/create', methods=['POST'])
def create_recipient():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO recipients (full_name, email, nif, phone, organization)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('full_name'), data.get('email'), data.get('nif'),
            data.get('phone'), data.get('organization', 'Particular')
        ))
        conn.commit()
        rid = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': rid, 'message': 'Formando / Destinatário registado com sucesso!'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Erro: Email ou NIF já registado no sistema.'}), 400

@app.route('/api/recipients/<int:rid>', methods=['DELETE'])
def delete_recipient(rid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipients WHERE id = ?', (rid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Formando eliminado.'})

# Templates API
@app.route('/api/templates', methods=['GET'])
def get_templates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM templates ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/templates/create', methods=['POST'])
def create_template():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO templates (title, category, background_theme, font_style, border_style, issuer_name, issuer_title, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'), data.get('category'), data.get('background_theme', 'Púrpura & Magenta'),
        data.get('font_style', 'Inter Clean'), data.get('border_style', 'Moldura Dourada'),
        data.get('issuer_name'), data.get('issuer_title'), data.get('status', 'Ativo')
    ))
    conn.commit()
    tid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': tid, 'message': 'Modelo de certificado criado com sucesso!'}), 201

@app.route('/api/templates/<int:tid>', methods=['DELETE'])
def delete_template(tid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM templates WHERE id = ?', (tid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Modelo eliminado.'})

# Certificates API
@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT certificates.*, recipients.full_name as recipient_name, recipients.email as recipient_email, recipients.nif as recipient_nif,
               templates.title as template_title, templates.issuer_name, templates.issuer_title
        FROM certificates
        JOIN recipients ON certificates.recipient_id = recipients.id
        JOIN templates ON certificates.template_id = templates.id
        ORDER BY certificates.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/certificates/create', methods=['POST'])
def create_certificate():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    code = f"CERT-2026-PT-{uuid.uuid4().hex[:6].upper()}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={code}"
    
    cursor.execute('''
        INSERT INTO certificates (recipient_id, template_id, course_title, verification_code, qr_code_url, issue_date, expiry_date, grade_achieved, pdf_status, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('recipient_id'), data.get('template_id'), data.get('course_title'),
        code, qr_url, data.get('issue_date'), data.get('expiry_date', 'Sem Validade'),
        float(data.get('grade_achieved', 100.0)), 'Pronto para Download', 'Válido'
    ))
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': cid, 'code': code, 'qr_url': qr_url, 'message': 'Certificado Digital emitido com sucesso!'}), 201

@app.route('/api/certificates/verify/<code>', methods=['GET'])
def verify_certificate(code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT certificates.*, recipients.full_name as recipient_name, recipients.nif as recipient_nif, recipients.email as recipient_email,
               templates.title as template_title, templates.issuer_name, templates.issuer_title
        FROM certificates
        JOIN recipients ON certificates.recipient_id = recipients.id
        JOIN templates ON certificates.template_id = templates.id
        WHERE certificates.verification_code = ? OR certificates.id = ?
    ''', (code, code))
    cert = cursor.fetchone()
    
    if cert:
        # Log verification
        cursor.execute('''
            INSERT INTO verification_logs (certificate_id, verified_by_ip, is_valid, notes)
            VALUES (?, ?, 1, 'Verificação autêntica de certificado realizada.')
        ''', (cert['id'], request.remote_addr or '127.0.0.1'))
        conn.commit()
        res = dict(cert)
        conn.close()
        return jsonify({'valid': True, 'certificate': res, 'message': 'Certificado AUTÊNTICO e VÁLIDO no registo nacional.'})
    else:
        conn.close()
        return jsonify({'valid': False, 'message': 'Código de verificação inválido ou certificado revogado.'}), 404

@app.route('/api/certificates/<int:cid>', methods=['DELETE'])
def delete_certificate(cid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM certificates WHERE id = ?', (cid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Certificado revogado com sucesso.'})

# Verification Logs API
@app.route('/api/verification_logs', methods=['GET'])
def get_verification_logs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT verification_logs.*, certificates.verification_code, certificates.course_title, recipients.full_name as recipient_name
        FROM verification_logs
        JOIN certificates ON verification_logs.certificate_id = certificates.id
        JOIN recipients ON certificates.recipient_id = recipients.id
        ORDER BY verification_logs.id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Export API
@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT certificates.verification_code as Codigo_Verificacao, recipients.full_name as Formando,
               recipients.nif as NIF, certificates.course_title as Curso_Formacao,
               certificates.issue_date as Data_Emissao, certificates.status as Estado
        FROM certificates
        JOIN recipients ON certificates.recipient_id = recipients.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_certicraft.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando CertiCraft AI SaaS no servidor local porta 6935...")
    app.run(host='0.0.0.0', port=6935, debug=True)
