import os
import sqlite3
import json
import csv
import io
import random
import string
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'docucraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def format_bytes(bytes_val):
    if bytes_val >= 1024 * 1024 * 1024:
        return f"{bytes_val / (1024**3):.2f} GB"
    elif bytes_val >= 1024 * 1024:
        return f"{bytes_val / (1024**2):.1f} MB"
    elif bytes_val >= 1024:
        return f"{bytes_val / 1024:.0f} KB"
    else:
        return f"{bytes_val} B"

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Storage Statistics
    cursor.execute("SELECT COUNT(*) as cnt, COALESCE(SUM(bytes_size), 0) as total_bytes FROM documents")
    row = cursor.fetchone()
    total_files = row['cnt']
    total_bytes = row['total_bytes']

    # Total allocated capacity: 100 GB (100 * 1024^3 bytes)
    max_capacity_bytes = 100 * 1024 * 1024 * 1024
    used_gb = round(total_bytes / (1024**3), 2)
    storage_percentage = min(round((total_bytes / max_capacity_bytes) * 100, 1), 100)

    # Total Folders
    cursor.execute("SELECT COUNT(*) as cnt FROM folders")
    total_folders = cursor.fetchone()['cnt']

    # Total Downloads
    cursor.execute("SELECT COALESCE(SUM(download_count), 0) as total_dl FROM documents")
    total_downloads = cursor.fetchone()['total_dl']

    # Recent Folders
    cursor.execute("""
    SELECT f.*, COUNT(d.id) as file_count, COALESCE(SUM(d.bytes_size), 0) as folder_bytes
    FROM folders f
    LEFT JOIN documents d ON f.id = d.folder_id
    GROUP BY f.id
    ORDER BY f.id ASC
    """)
    folders = [dict(r) for r in cursor.fetchall()]
    for f in folders:
        f['folder_size'] = format_bytes(f['folder_bytes'])

    # Starred / Favorite Documents
    cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id WHERE d.is_starred = 1 ORDER BY d.id DESC")
    starred_files = [dict(r) for r in cursor.fetchall()]

    # Recent Documents List
    cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id ORDER BY d.id DESC LIMIT 8")
    recent_files = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        total_files=total_files,
        total_folders=total_folders,
        used_gb=used_gb,
        storage_percentage=storage_percentage,
        total_downloads=total_downloads,
        folders=folders,
        starred_files=starred_files,
        recent_files=recent_files
    )

@app.route('/folders')
def folders_page():
    conn = get_db()
    cursor = conn.cursor()

    folder_id = request.args.get('id', type=int)

    cursor.execute("""
    SELECT f.*, COUNT(d.id) as file_count, COALESCE(SUM(d.bytes_size), 0) as folder_bytes
    FROM folders f
    LEFT JOIN documents d ON f.id = d.folder_id
    GROUP BY f.id
    ORDER BY f.id ASC
    """)
    folders = [dict(r) for r in cursor.fetchall()]
    for f in folders:
        f['folder_size'] = format_bytes(f['folder_bytes'])

    selected_folder = None
    folder_files = []
    if folder_id:
        cursor.execute("SELECT * FROM folders WHERE id = ?", (folder_id,))
        sf = cursor.fetchone()
        if sf:
            selected_folder = dict(sf)
            cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id WHERE d.folder_id = ? ORDER BY d.id DESC", (folder_id,))
            folder_files = [dict(r) for r in cursor.fetchall()]
    else:
        # Default view: all files in root
        cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id ORDER BY d.id DESC")
        folder_files = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('folders.html', folders=folders, selected_folder=selected_folder, folder_files=folder_files)

@app.route('/documents')
def documents_page():
    conn = get_db()
    cursor = conn.cursor()

    q = request.args.get('q', '').strip()
    cat_filter = request.args.get('category', '').strip()
    perm_filter = request.args.get('permission', '').strip()

    query = "SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id WHERE 1=1"
    params = []

    if q:
        query += " AND (d.file_name LIKE ? OR d.uploaded_by LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    if cat_filter:
        query += " AND d.category = ?"
        params.append(cat_filter)

    if perm_filter:
        query += " AND d.access_permission = ?"
        params.append(perm_filter)

    query += " ORDER BY d.id DESC"
    cursor.execute(query, params)
    documents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, folder_name FROM folders ORDER BY folder_name ASC")
    all_folders = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template(
        'documents.html',
        documents=documents,
        all_folders=all_folders,
        search_query=q,
        selected_category=cat_filter,
        selected_permission=perm_filter
    )

@app.route('/categories')
def categories_page():
    conn = get_db()
    cursor = conn.cursor()

    categories_list = ['Jurídico', 'Financeiro', 'Marketing', 'RH', 'Técnico', 'Geral']
    category_stats = []

    for cat in categories_list:
        cursor.execute("SELECT COUNT(*) as cnt, COALESCE(SUM(bytes_size), 0) as sum_b, COALESCE(SUM(download_count), 0) as sum_dl FROM documents WHERE category = ?", (cat,))
        r = cursor.fetchone()
        cnt = r['cnt']
        b_val = r['sum_b']
        dl_val = r['sum_dl']
        category_stats.append({
            'name': cat,
            'count': cnt,
            'formatted_size': format_bytes(b_val),
            'downloads': dl_val
        })

    cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id ORDER BY d.category ASC, d.id DESC")
    all_docs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('categories.html', category_stats=category_stats, all_docs=all_docs)

@app.route('/permissions')
def permissions_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT access_permission, COUNT(*) as cnt, COALESCE(SUM(bytes_size), 0) as sum_bytes
    FROM documents
    GROUP BY access_permission
    """)
    perm_summary = [dict(r) for r in cursor.fetchall()]
    for p in perm_summary:
        p['formatted_size'] = format_bytes(p['sum_bytes'])

    cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id ORDER BY d.access_permission ASC, d.id DESC")
    documents = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('permissions.html', perm_summary=perm_summary, documents=documents)

@app.route('/share/<share_code>')
def share_landing(share_code):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT d.*, f.folder_name FROM documents d LEFT JOIN folders f ON d.folder_id = f.id WHERE d.share_code = ?", (share_code,))
    doc_row = cursor.fetchone()

    if not doc_row:
        conn.close()
        return render_template('share.html', error='Link de partilha inválido ou expirado.')

    document = dict(doc_row)
    conn.close()
    return render_template('share.html', document=document)

# API ENDPOINTS

@app.route('/api/document/upload', methods=['POST'])
def api_upload_document():
    try:
        data = request.get_json() or {}
        file_name = data.get('file_name', '').strip()
        category = data.get('category', 'Geral')
        folder_id = data.get('folder_id')
        file_extension = data.get('file_extension', 'pdf').lower().replace('.', '')
        access_permission = data.get('access_permission', 'Equipas')
        uploaded_by = data.get('uploaded_by', 'Enmanuel Jimenez').strip()

        if not file_name:
            return jsonify({'success': False, 'message': 'Introduza o nome do ficheiro.'}), 400

        if not file_name.endswith(f".{file_extension}"):
            file_name += f".{file_extension}"

        # Generate random file size between 1.2 MB and 18.5 MB
        bytes_size = random.randint(1200000, 19400000)
        formatted_size = format_bytes(bytes_size)

        # Generate unique share code
        rand_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        share_code = f"SHR-{category[:3].upper()}-{rand_suffix}"

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO documents (file_name, category, folder_id, file_extension, file_size, bytes_size, access_permission, uploaded_by, download_count, is_starred, share_code, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?)
        """, (file_name, category, folder_id if folder_id else None, file_extension, formatted_size, bytes_size, access_permission, uploaded_by, share_code, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Ficheiro "{file_name}" ({formatted_size}) carregado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/folder/create', methods=['POST'])
def api_create_folder():
    try:
        data = request.get_json() or {}
        folder_name = data.get('folder_name', '').strip()
        color = data.get('color', '#0369A1')

        if not folder_name:
            return jsonify({'success': False, 'message': 'Introduza o nome da pasta.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO folders (folder_name, icon, color, parent_id, created_at)
        VALUES (?, 'fa-folder-closed', ?, NULL, ?)
        """, (folder_name, color, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Pasta "{folder_name}" criada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/document/star/<int:doc_id>', methods=['POST'])
def api_toggle_star(doc_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT is_starred FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({'success': False, 'message': 'Ficheiro não encontrado.'}), 404

        new_star = 0 if row['is_starred'] == 1 else 1
        cursor.execute("UPDATE documents SET is_starred = ? WHERE id = ?", (new_star, doc_id))
        conn.commit()
        conn.close()

        msg = 'Adicionado aos favoritos' if new_star == 1 else 'Removido dos favoritos'
        return jsonify({'success': True, 'is_starred': new_star, 'message': msg})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/document/download/<int:doc_id>', methods=['GET', 'POST'])
def api_download_doc(doc_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE documents SET download_count = download_count + 1 WHERE id = ?", (doc_id,))
        cursor.execute("SELECT file_name FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()

        file_name = row['file_name'] if row else "documento.pdf"
        return jsonify({'success': True, 'message': f'Iniciando download do ficheiro "{file_name}"...'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT d.file_name, d.category, f.folder_name, d.file_size, d.access_permission, d.uploaded_by, d.download_count, d.created_at
    FROM documents d
    LEFT JOIN folders f ON d.folder_id = f.id
    ORDER BY d.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        return Response(
            json.dumps(output_list, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=docucraft_export.json'}
        )
    else:  # CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Nome do Ficheiro', 'Categoria', 'Pasta', 'Tamanho', 'Permissões', 'Enviado por', 'Downloads', 'Data'])
        for r in rows:
            writer.writerow([r['file_name'], r['category'], r['folder_name'] or 'Geral', r['file_size'], r['access_permission'], r['uploaded_by'], r['download_count'], r['created_at']])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=docucraft_export.csv'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6926, debug=True)
