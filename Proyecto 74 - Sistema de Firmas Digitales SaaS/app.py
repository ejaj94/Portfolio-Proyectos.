import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'signcraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Metrics
    cursor.execute("SELECT COUNT(*) as cnt FROM documents")
    total_docs = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM documents WHERE status = 'Assinado'")
    signed_docs = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM documents WHERE status IN ('Pendente', 'Em Processo')")
    pending_docs = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM signers")
    total_signers = cursor.fetchone()['cnt']

    conversion_rate = round((signed_docs / total_docs * 100), 1) if total_docs > 0 else 0.0

    # Recent Documents List with Signer Count & Completion Progress
    cursor.execute("""
    SELECT d.*, 
           COUNT(s.id) as total_signers, 
           SUM(CASE WHEN s.status = 'Assinado' THEN 1 ELSE 0 END) as signed_signers
    FROM documents d
    LEFT JOIN signers s ON d.id = s.document_id
    GROUP BY d.id
    ORDER BY d.id DESC
    LIMIT 6
    """)
    recent_docs = [dict(r) for r in cursor.fetchall()]

    # Audit Trail Recent Logs
    cursor.execute("""
    SELECT a.*, d.title as doc_title, d.doc_code
    FROM audit_logs a
    JOIN documents d ON a.document_id = d.id
    ORDER BY a.id DESC
    LIMIT 5
    """)
    recent_logs = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        total_docs=total_docs,
        signed_docs=signed_docs,
        pending_docs=pending_docs,
        total_signers=total_signers,
        conversion_rate=conversion_rate,
        recent_docs=recent_docs,
        recent_logs=recent_logs
    )

@app.route('/documents')
def documents_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    category_filter = request.args.get('category')
    search_q = request.args.get('q', '').strip()

    query = """
    SELECT d.*, 
           COUNT(s.id) as total_signers, 
           SUM(CASE WHEN s.status = 'Assinado' THEN 1 ELSE 0 END) as signed_signers
    FROM documents d
    LEFT JOIN signers s ON d.id = s.document_id
    WHERE 1=1
    """
    params = []

    if status_filter:
        query += " AND d.status = ?"
        params.append(status_filter)

    if category_filter:
        query += " AND d.category = ?"
        params.append(category_filter)

    if search_q:
        query += " AND (d.title LIKE ? OR d.doc_code LIKE ? OR d.created_by LIKE ?)"
        params.extend([f"%{search_q}%", f"%{search_q}%", f"%{search_q}%"])

    query += " GROUP BY d.id ORDER BY d.id DESC"
    cursor.execute(query, params)
    documents = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('documents.html', documents=documents, selected_status=status_filter, selected_category=category_filter, search_q=search_q)

@app.route('/signers')
def signers_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT s.*, d.title as doc_title, d.doc_code, d.status as doc_status
    FROM signers s
    JOIN documents d ON s.document_id = d.id
    ORDER BY s.id DESC
    """)
    signers = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('signers.html', signers=signers)

@app.route('/sign/<int:doc_id>')
def sign_studio(doc_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    d_row = cursor.fetchone()
    if not d_row:
        conn.close()
        return redirect(url_for('documents_page'))

    document = dict(d_row)

    cursor.execute("SELECT * FROM signers WHERE document_id = ? ORDER BY id ASC", (doc_id,))
    signers = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM audit_logs WHERE document_id = ? ORDER BY id ASC", (doc_id,))
    audit_logs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('sign_studio.html', document=document, signers=signers, audit_logs=audit_logs)

@app.route('/certificate/<int:doc_id>')
def certificate_page(doc_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    d_row = cursor.fetchone()
    if not d_row:
        conn.close()
        return redirect(url_for('documents_page'))

    document = dict(d_row)

    cursor.execute("SELECT * FROM signers WHERE document_id = ? ORDER BY id ASC", (doc_id,))
    signers = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT * FROM audit_logs WHERE document_id = ? ORDER BY id ASC", (doc_id,))
    audit_logs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('certificate.html', document=document, signers=signers, audit_logs=audit_logs)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT a.*, d.title as doc_title, d.doc_code, d.category
    FROM audit_logs a
    JOIN documents d ON a.document_id = d.id
    ORDER BY a.id DESC
    """)
    audit_logs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('history.html', audit_logs=audit_logs)

# API ENDPOINTS

@app.route('/api/document/create', methods=['POST'])
def api_create_document():
    try:
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        category = data.get('category', 'Contrato')
        created_by = data.get('created_by', 'Enmanuel Jimenez').strip()
        signer_name = data.get('signer_name', '').strip()
        signer_email = data.get('signer_email', '').strip()
        signer_role = data.get('signer_role', 'Cliente Signatário').strip()

        if not title or not signer_name or not signer_email:
            return jsonify({'success': False, 'message': 'Preencha o título do documento e dados do signatário.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        today_date = date.today().strftime("%Y-%m-%d")
        deadline_date = (date.today() + timedelta(days=15)).strftime("%Y-%m-%d")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as cnt FROM documents")
        cnt = cursor.fetchone()['cnt'] + 1
        doc_code = f"SIG-2026-{cnt:03d}"

        cursor.execute("""
        INSERT INTO documents (doc_code, title, category, file_size, status, deadline, created_by, created_at, signed_at)
        VALUES (?, ?, ?, '2.5 MB', 'Pendente', ?, ?, ?, NULL)
        """, (doc_code, title, category, deadline_date, created_by, now_str))

        doc_id = cursor.lastrowid

        # Insert Signer
        cursor.execute("""
        INSERT INTO signers (document_id, full_name, email, role_title, status, signature_data, signed_at, ip_address)
        VALUES (?, ?, ?, ?, 'Pendente', NULL, NULL, NULL)
        """, (doc_id, signer_name, signer_email, signer_role))

        # Add Audit Trail Entry
        cursor.execute("""
        INSERT INTO audit_logs (document_id, action, actor_name, timestamp, ip_hash)
        VALUES (?, 'Documento Criado & Pedido de Assinatura Emitido', ?, ?, 'IP-194-65-112-45')
        """, (doc_id, created_by, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'doc_id': doc_id, 'message': f'Documento "{doc_code}" criado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/sign/submit', methods=['POST'])
def api_submit_signature():
    try:
        data = request.get_json() or {}
        doc_id = data.get('doc_id')
        signer_id = data.get('signer_id')
        signature_data = data.get('signature_data', 'SIG_DESENHO_OK')

        if not doc_id or not signer_id:
            return jsonify({'success': False, 'message': 'IDs de documento e signatário inválidos.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        # Update Signer
        cursor.execute("""
        UPDATE signers 
        SET status = 'Assinado', signature_data = ?, signed_at = ?, ip_address = '194.65.112.45'
        WHERE id = ? AND document_id = ?
        """, (signature_data, now_str, signer_id, doc_id))

        cursor.execute("SELECT full_name FROM signers WHERE id = ?", (signer_id,))
        s_row = cursor.fetchone()
        signer_name = s_row['full_name'] if s_row else "Signatário"

        # Audit Log
        cursor.execute("""
        INSERT INTO audit_logs (document_id, action, actor_name, timestamp, ip_hash)
        VALUES (?, ?, ?, ?, 'IP-194-65-112-45')
        """, (doc_id, f"Assinatura Registada por {signer_name}", signer_name, now_str))

        # Check if all signers of this document have signed
        cursor.execute("SELECT COUNT(*) as cnt FROM signers WHERE document_id = ? AND status != 'Assinado'", (doc_id,))
        pending_cnt = cursor.fetchone()['cnt']

        if pending_cnt == 0:
            cursor.execute("UPDATE documents SET status = 'Assinado', signed_at = ? WHERE id = ?", (now_str, doc_id))
            cursor.execute("""
            INSERT INTO audit_logs (document_id, action, actor_name, timestamp, ip_hash)
            VALUES (?, 'Certificado Digital de Conclusão Emitido', 'SISTEMA SIGN CRAFT', ?, 'SHA256-CERT-OK')
            """, (doc_id, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Assinatura de {signer_name} registada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT d.doc_code, d.title, d.category, d.file_size, d.status, d.created_by, d.created_at, d.signed_at,
           COUNT(s.id) as total_signers
    FROM documents d
    LEFT JOIN signers s ON d.id = s.document_id
    GROUP BY d.id
    ORDER BY d.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        return Response(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=signcraft_export.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Código', 'Título do Documento', 'Categoria', 'Tamanho', 'Estado', 'Criado Por', 'Data Criação', 'Data Assinatura', 'Nº Signatários'])
        for r in rows:
            writer.writerow([r['doc_code'], r['title'], r['category'], r['file_size'], r['status'], r['created_by'], r['created_at'], r['signed_at'] or 'N/A', r['total_signers']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=signcraft_export.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6927, debug=True)
