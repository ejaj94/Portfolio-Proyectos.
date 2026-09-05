import os
import sqlite3
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import DB_PATH, init_db

app = Flask(__name__)
app.secret_key = 'ejaj_tech_grand_finale_secret_key_2026'

# Custom Filters
@app.template_filter('escapejs')
def escapejs_filter(val):
    if not val:
        return ""
    return json.dumps(str(val))[1:-1]

# Ensure DB exists
if not os.path.exists(DB_PATH):
    init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    projects = [dict(r) for r in conn.execute('SELECT * FROM projects ORDER BY day ASC').fetchall()]
    services = [dict(r) for r in conn.execute('SELECT * FROM services ORDER BY id ASC').fetchall()]
    
    # Categories list
    categories = [r[0] for r in conn.execute('SELECT DISTINCT category FROM projects').fetchall()]
    
    conn.close()
    return render_template('index.html', projects=projects, services=services, categories=categories, total_projects=len(projects))

@app.route('/project/<int:day>')
def project_detail(day):
    conn = get_db_connection()
    # Increment view count
    conn.execute('UPDATE projects SET views = views + 1 WHERE day = ?', (day,))
    conn.commit()
    
    proj_row = conn.execute('SELECT * FROM projects WHERE day = ?', (day,)).fetchone()
    if not proj_row:
        conn.close()
        return "Projeto não encontrado", 404
        
    project = dict(proj_row)
    prev_day = day - 1 if day > 1 else 29
    next_day = day + 1 if day < 29 else 1
    
    related = [dict(r) for r in conn.execute('SELECT * FROM projects WHERE category = ? AND day != ? LIMIT 3', (project['category'], day)).fetchall()]
    conn.close()
    
    return render_template('project_detail.html', project=project, prev_day=prev_day, next_day=next_day, related=related)

@app.route('/services')
def services_page():
    conn = get_db_connection()
    services = [dict(r) for r in conn.execute('SELECT * FROM services ORDER BY id ASC').fetchall()]
    conn.close()
    return render_template('services.html', services=services)

@app.route('/challenge')
def challenge_page():
    conn = get_db_connection()
    projects = [dict(r) for r in conn.execute('SELECT * FROM projects ORDER BY day ASC').fetchall()]
    conn.close()
    return render_template('challenge.html', projects=projects)

# API ENDPOINTS
@app.route('/api/projects', methods=['GET'])
def api_get_projects():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    
    conn = get_db_connection()
    sql = 'SELECT * FROM projects WHERE 1=1'
    params = []
    
    if q:
        sql += ' AND (title LIKE ? OR short_desc LIKE ? OR tech_stack LIKE ? OR features LIKE ?)'
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%', f'%{q}%'])
    if category:
        sql += ' AND category = ?'
        params.append(category)
        
    sql += ' ORDER BY day ASC'
    projects = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    
    return jsonify({'success': True, 'count': len(projects), 'projects': projects})

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.json or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    service = data.get('service', 'Desenvolvimento Web').strip()
    budget = data.get('budget', '€ 1.000 - € 3.000').strip()
    message = data.get('message', '').strip()
    
    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'Por favor preencha o seu nome, e-mail e mensagem.'}), 400
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO quotes (name, email, phone, service, budget, message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, service, budget, message))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': f'Obrigado {name}! A equipa da EJAJ TECH irá analisar o seu projeto e responder em menos de 2 horas.'
    })

if __name__ == '__main__':
    print("[SERVER] EJAJ TECH Grand Finale Agency SaaS a iniciar na porta 6600...")
    app.run(host='0.0.0.0', port=6600, debug=False)
