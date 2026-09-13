import os
import sqlite3
import csv
import io
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

@app.route('/projects')
def projects():
    return render_template('projects.html', active_page='projects')

@app.route('/creators')
def creators():
    return render_template('creators.html', active_page='creators')

@app.route('/donations')
def donations():
    return render_template('donations.html', active_page='donations')

@app.route('/users')
def users():
    return render_template('users.html', active_page='users')

@app.route('/stats')
def stats():
    return render_template('stats.html', active_page='stats')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html', active_page='showcase')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM projects')
    total_projects = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM projects WHERE status = "Ativo"')
    active_projects = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(raised_amount) FROM projects')
    total_raised = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT COUNT(*) FROM donations')
    total_donations = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM creators')
    total_creators = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'total_projects': total_projects,
        'active_projects': active_projects,
        'total_raised': round(total_raised, 2),
        'total_donations': total_donations,
        'total_users': total_users,
        'total_creators': total_creators
    })

@app.route('/api/projects', methods=['GET', 'POST'])
def handle_projects():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        creator_name = data.get('creator_name', '').strip()
        category = data.get('category', 'Geral').strip()
        goal_amount = float(data.get('goal_amount', 0))
        description = data.get('description', '').strip()
        end_date = data.get('end_date', '').strip()
        image_url = data.get('image_url', '').strip() or 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=600'

        if not title or not creator_name or goal_amount <= 0:
            return jsonify({'success': False, 'message': 'Preencha o título, criador e objetivo válido!'}), 400

        cursor.execute('''
            INSERT INTO projects (title, creator_name, category, goal_amount, raised_amount, description, end_date, status, image_url)
            VALUES (?, ?, ?, ?, 0.0, ?, ?, 'Ativo', ?)
        ''', (title, creator_name, category, goal_amount, description, end_date, image_url))
        conn.commit()

        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'message': 'Projeto publicado com sucesso!', 'id': new_id})

    cursor.execute('SELECT * FROM projects ORDER BY id DESC')
    projects = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # Calculate progress %
    for p in projects:
        p['progress_pct'] = min(round((p['raised_amount'] / p['goal_amount']) * 100, 1) if p['goal_amount'] > 0 else 0, 100)

    return jsonify(projects)

@app.route('/api/creators', methods=['GET'])
def get_creators():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM creators ORDER BY id DESC')
    creators = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(creators)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id DESC')
    users = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/api/donations', methods=['GET', 'POST'])
def handle_donations():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        project_id = data.get('project_id')
        donor_name = data.get('donor_name', '').strip()
        donor_email = data.get('donor_email', '').strip()
        amount = float(data.get('amount', 0))
        reward_tier = data.get('reward_tier', 'Apoio Livre').strip()

        if not project_id or not donor_name or amount <= 0:
            return jsonify({'success': False, 'message': 'Dados de doação inválidos!'}), 400

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Insert donation
        cursor.execute('''
            INSERT INTO donations (project_id, donor_name, donor_email, amount, reward_tier, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (project_id, donor_name, donor_email, amount, reward_tier, now_str))

        # Update project raised amount
        cursor.execute('UPDATE projects SET raised_amount = raised_amount + ? WHERE id = ?', (amount, project_id))

        # Check if project reached goal
        cursor.execute('SELECT raised_amount, goal_amount FROM projects WHERE id = ?', (project_id,))
        p = cursor.fetchone()
        if p and p['raised_amount'] >= p['goal_amount']:
            cursor.execute('UPDATE projects SET status = "Financiado" WHERE id = ?', (project_id,))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Contribuição efetuada com sucesso!'})

    cursor.execute('''
        SELECT donations.*, projects.title as project_title
        FROM donations
        JOIN projects ON donations.project_id = projects.id
        ORDER BY donations.id DESC
    ''')
    donations = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(donations)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT donations.id, donations.donor_name, donations.donor_email, donations.amount as Valor_EUR,
               donations.reward_tier as Recompensa, projects.title as Projeto, donations.created_at as Data
        FROM donations
        JOIN projects ON donations.project_id = projects.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_crowdfund.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando FundCraft AI SaaS no servidor local porta 6937...")
    app.run(host='0.0.0.0', port=6937, debug=True)
