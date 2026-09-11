import os
import sqlite3
import json
import csv
import io
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'taskcraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_project_progress(cursor, project_id):
    cursor.execute("SELECT COUNT(*) as total FROM tasks WHERE project_id = ?", (project_id,))
    total = cursor.fetchone()['total']
    if total == 0:
        return 0
    cursor.execute("SELECT COUNT(*) as done FROM tasks WHERE project_id = ? AND status = 'Concluído'", (project_id,))
    done = cursor.fetchone()['done']
    return int((done / total) * 100)

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Metrics
    cursor.execute("SELECT COUNT(*) as cnt FROM projects")
    total_projects = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM projects WHERE status = 'Em Progresso'")
    active_projects = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM tasks WHERE status = 'Concluído'")
    completed_tasks = cursor.fetchone()['cnt']

    cursor.execute("SELECT COUNT(*) as cnt FROM tasks")
    total_tasks = cursor.fetchone()['cnt']

    cursor.execute("SELECT SUM(budget) as sum_budget FROM projects")
    total_budget = cursor.fetchone()['sum_budget'] or 0.0

    cursor.execute("SELECT COUNT(*) as cnt FROM teams")
    total_teams = cursor.fetchone()['cnt']

    overall_progress = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    # Projects List with Calculated Progress
    cursor.execute("""
    SELECT p.*, t.name as team_name, t.color as team_color
    FROM projects p
    JOIN teams t ON p.team_id = t.id
    ORDER BY p.id DESC
    """)
    projects_raw = cursor.fetchall()
    projects = []
    for pr in projects_raw:
        p_dict = dict(pr)
        p_dict['progress'] = calculate_project_progress(cursor, p_dict['id'])
        projects.append(p_dict)

    # Recent Tasks
    cursor.execute("""
    SELECT t.*, p.name as project_name
    FROM tasks t
    JOIN projects p ON t.project_id = p.id
    ORDER BY t.due_date ASC
    LIMIT 6
    """)
    upcoming_tasks = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return render_template(
        'dashboard.html',
        total_projects=total_projects,
        active_projects=active_projects,
        completed_tasks=completed_tasks,
        total_tasks=total_tasks,
        total_budget=total_budget,
        total_teams=total_teams,
        overall_progress=overall_progress,
        projects=projects,
        upcoming_tasks=upcoming_tasks
    )

@app.route('/projects')
def projects_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    query = """
    SELECT p.*, t.name as team_name, t.color as team_color
    FROM projects p
    JOIN teams t ON p.team_id = t.id
    WHERE 1=1
    """
    params = []
    if status_filter:
        query += " AND p.status = ?"
        params.append(status_filter)

    query += " ORDER BY p.id DESC"
    cursor.execute(query, params)

    projects_raw = cursor.fetchall()
    projects = []
    for pr in projects_raw:
        p_dict = dict(pr)
        p_dict['progress'] = calculate_project_progress(cursor, p_dict['id'])
        projects.append(p_dict)

    cursor.execute("SELECT * FROM teams ORDER BY name ASC")
    teams = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('projects.html', projects=projects, teams=teams, selected_status=status_filter)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.*, t.name as team_name, t.lead_name, t.color as team_color
    FROM projects p
    JOIN teams t ON p.team_id = t.id
    WHERE p.id = ?
    """, (project_id,))
    project_row = cursor.fetchone()

    if not project_row:
        conn.close()
        return redirect(url_for('projects_page'))

    project = dict(project_row)
    project['progress'] = calculate_project_progress(cursor, project_id)

    # Tasks for this project
    cursor.execute("SELECT * FROM tasks WHERE project_id = ? ORDER BY id DESC", (project_id,))
    tasks = [dict(r) for r in cursor.fetchall()]

    # Comments
    cursor.execute("SELECT * FROM comments WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
    comments = [dict(r) for r in cursor.fetchall()]

    # Files
    cursor.execute("SELECT * FROM files WHERE project_id = ? ORDER BY uploaded_at DESC", (project_id,))
    files = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('project_detail.html', project=project, tasks=tasks, comments=comments, files=files)

@app.route('/teams')
def teams_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT t.*, COUNT(p.id) as project_count
    FROM teams t
    LEFT JOIN projects p ON t.id = p.team_id
    GROUP BY t.id
    ORDER BY t.id ASC
    """)
    teams = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return render_template('teams.html', teams=teams)

@app.route('/tasks')
def tasks_page():
    conn = get_db()
    cursor = conn.cursor()

    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')

    query = """
    SELECT t.*, p.name as project_name, p.status as project_status
    FROM tasks t
    JOIN projects p ON t.project_id = p.id
    WHERE 1=1
    """
    params = []
    if status_filter:
        query += " AND t.status = ?"
        params.append(status_filter)
    if priority_filter:
        query += " AND t.priority = ?"
        params.append(priority_filter)

    query += " ORDER BY t.due_date ASC"
    cursor.execute(query, params)
    tasks = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM projects ORDER BY name ASC")
    projects = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('tasks.html', tasks=tasks, projects=projects, selected_status=status_filter, selected_priority=priority_filter)

@app.route('/files')
def files_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT f.*, p.name as project_name
    FROM files f
    JOIN projects p ON f.project_id = p.id
    ORDER BY f.uploaded_at DESC
    """)
    files = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM projects ORDER BY name ASC")
    projects = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('files.html', files=files, projects=projects)

# API ENDPOINTS

@app.route('/api/project/save', methods=['POST'])
def api_save_project():
    try:
        data = request.get_json() or {}
        p_id = data.get('id')
        name = data.get('name', '').strip()
        client_name = data.get('client_name', '').strip()
        team_id = data.get('team_id')
        description = data.get('description', '').strip()
        status = data.get('status', 'Em Progresso')
        start_date = data.get('start_date', date.today().strftime("%Y-%m-%d"))
        due_date = data.get('due_date', (date.today() + timedelta(days=30)).strftime("%Y-%m-%d"))
        budget = float(data.get('budget', 0.0))

        if not all([name, client_name, team_id]):
            return jsonify({'success': False, 'message': 'Por favor preencha todos os campos obrigatórios.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()

        if p_id:
            cursor.execute("""
            UPDATE projects
            SET name = ?, client_name = ?, team_id = ?, description = ?, status = ?, start_date = ?, due_date = ?, budget = ?
            WHERE id = ?
            """, (name, client_name, team_id, description, status, start_date, due_date, budget, p_id))
        else:
            cursor.execute("""
            INSERT INTO projects (name, client_name, team_id, description, status, start_date, due_date, budget, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, client_name, team_id, description, status, start_date, due_date, budget, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Projeto "{name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/task/save', methods=['POST'])
def api_save_task():
    try:
        data = request.get_json() or {}
        project_id = data.get('project_id')
        title = data.get('title', '').strip()
        assigned_to = data.get('assigned_to', '').strip()
        priority = data.get('priority', 'Média')
        status = data.get('status', 'A Fazer')
        due_date = data.get('due_date', date.today().strftime("%Y-%m-%d"))

        if not all([project_id, title, assigned_to]):
            return jsonify({'success': False, 'message': 'Preencha o projeto, título da tarefa e responsável.'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO tasks (project_id, title, assigned_to, priority, status, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (project_id, title, assigned_to, priority, status, due_date))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Tarefa "{title}" criada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/task/status/<int:task_id>', methods=['POST'])
def api_update_task_status(task_id):
    try:
        data = request.get_json() or {}
        new_status = data.get('status', 'Concluído')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Estado da tarefa alterado para "{new_status}".'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/comment/add', methods=['POST'])
def api_add_comment():
    try:
        data = request.get_json() or {}
        project_id = data.get('project_id')
        author = data.get('author', 'Gestor de Projeto').strip()
        comment_text = data.get('comment_text', '').strip()

        if not project_id or not comment_text:
            return jsonify({'success': False, 'message': 'Comentário inválido.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO comments (project_id, author, comment_text, created_at)
        VALUES (?, ?, ?, ?)
        """, (project_id, author, comment_text, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Comentário adicionado!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/file/add', methods=['POST'])
def api_add_file():
    try:
        data = request.get_json() or {}
        project_id = data.get('project_id')
        file_name = data.get('file_name', '').strip()
        file_size = data.get('file_size', '1.5 MB').strip()
        category = data.get('category', 'Documento').strip()

        if not project_id or not file_name:
            return jsonify({'success': False, 'message': 'Ficheiro inválido.'}), 400

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO files (project_id, file_name, file_size, category, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
        """, (project_id, file_name, file_size, category, now_str))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Ficheiro "{file_name}" anexado ao projeto!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/export/<fmt>')
def api_export_projects(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.id, p.name, p.client_name, t.name as team_name, p.status, p.start_date, p.due_date, p.budget
    FROM projects p
    JOIN teams t ON p.team_id = t.id
    ORDER BY p.id ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    if fmt.lower() == 'json':
        output_list = [dict(r) for r in rows]
        json_data = json.dumps(output_list, indent=2, ensure_ascii=False)
        return Response(
            json_data,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=relatorio_projetos_taskcraft.json'}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID Projeto', 'Nome Projeto', 'Cliente', 'Equipa', 'Estado', 'Data Início', 'Data Fim', 'Orçamento (€)'])

        for r in rows:
            writer.writerow([r['id'], r['name'], r['client_name'], r['team_name'], r['status'], r['start_date'], r['due_date'], f"{r['budget']:.2f}"])

        csv_content = output.getvalue()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=relatorio_projetos_taskcraft.csv'}
        )

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - TaskCraft AI SaaS na porta 6922...")
    app.run(host='127.0.0.1', port=6922, debug=False, use_reloader=False)
