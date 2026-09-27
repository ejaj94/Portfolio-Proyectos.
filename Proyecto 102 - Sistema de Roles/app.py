from flask import Flask, render_template, request, jsonify
from database import init_db, get_db
from datetime import datetime

app = Flask(__name__)

# Guarantee DB initialization
init_db()

def log_audit(actor, action, details, ip="127.0.0.1"):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO audit_logs (timestamp, actor_name, action_type, details, ip_address)
        VALUES (?, ?, ?, ?, ?)
    ''', (now, actor, action, details, ip))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()

    # Fetch Users
    cursor.execute('SELECT * FROM users ORDER BY id ASC')
    users = [dict(row) for row in cursor.fetchall()]

    # Fetch Permissions
    cursor.execute('SELECT * FROM permissions_matrix')
    raw_perms = [dict(row) for row in cursor.fetchall()]

    # Structure permissions by role -> module -> level
    matrix = {}
    for p in raw_perms:
        role = p['role_type']
        module = p['module_name']
        if role not in matrix:
            matrix[role] = {}
        matrix[role][module] = p['access_level']

    # Fetch Active Sessions with User Names
    cursor.execute('''
        SELECT s.*, u.name as user_name, u.role_type, u.email
        FROM active_sessions s
        JOIN users u ON s.user_id = u.id
        ORDER BY s.is_active DESC, s.id DESC
    ''')
    sessions = [dict(row) for row in cursor.fetchall()]

    # Fetch Audit Logs
    cursor.execute('SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50')
    audit_logs = [dict(row) for row in cursor.fetchall()]

    # Statistics
    stats = {
        'total_users': len(users),
        'admins': sum(1 for u in users if u['role_type'] == 'Administrador'),
        'empleados': sum(1 for u in users if u['role_type'] == 'Empleado'),
        'usuarios': sum(1 for u in users if u['role_type'] == 'Usuario'),
        'active_sessions': sum(1 for s in sessions if s['is_active'] == 1)
    }

    conn.close()
    return render_template('index.html', users=users, matrix=matrix, sessions=sessions, audit_logs=audit_logs, stats=stats)

@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM users ORDER BY id ASC')
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(users)

    elif request.method == 'POST':
        data = request.json or {}
        name = data.get('name')
        email = data.get('email')
        role_type = data.get('role_type', 'Usuario')
        department = data.get('department', 'Geral')

        if not name or not email:
            conn.close()
            return jsonify({'error': 'Nome e email são obrigatórios'}), 400

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            cursor.execute('''
                INSERT INTO users (name, email, role_type, department, status, created_at)
                VALUES (?, ?, ?, ?, 'Ativo', ?)
            ''', (name, email, role_type, department, now))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()

            log_audit("Angel Rafael (Admin)", "USER_ADD", f"Criou utilizador '{name}' ({email}) como {role_type} no departamento {department}")
            return jsonify({'success': True, 'id': new_id}), 201
        except Exception as e:
            conn.close()
            return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>/role', methods=['POST'])
def update_user_role(user_id):
    data = request.json or {}
    new_role = data.get('role_type')
    new_status = data.get('status')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT name, role_type, status FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Utilizador não encontrado'}), 404

    old_role = user['role_type']
    old_status = user['status']
    updated_role = new_role or old_role
    updated_status = new_status or old_status

    cursor.execute('''
        UPDATE users
        SET role_type = ?, status = ?
        WHERE id = ?
    ''', (updated_role, updated_status, user_id))
    conn.commit()
    conn.close()

    log_audit("Angel Rafael (Admin)", "ROLE_CHANGE", f"Alterou cargo/status de {user['name']}: Role ({old_role} -> {updated_role}), Status ({old_status} -> {updated_status})")
    return jsonify({'success': True})

@app.route('/api/permissions', methods=['POST'])
def update_permissions():
    data = request.json or {}
    role_type = data.get('role_type')
    module_name = data.get('module_name')
    access_level = data.get('access_level')

    if not role_type or not module_name or not access_level:
        return jsonify({'error': 'Dados incompletos'}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE permissions_matrix
        SET access_level = ?
        WHERE role_type = ? AND module_name = ?
    ''', (access_level, role_type, module_name))
    conn.commit()
    conn.close()

    log_audit("Angel Rafael (Admin)", "PERMISSION_UPDATE", f"Atualizou privilégio de {role_type} no módulo {module_name} para '{access_level}'")
    return jsonify({'success': True})

@app.route('/api/sessions/<int:session_id>/revoke', methods=['POST'])
def revoke_session(session_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.id, u.name
        FROM active_sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.id = ?
    ''', (session_id,))
    sess = cursor.fetchone()
    if not sess:
        conn.close()
        return jsonify({'error': 'Sessão não encontrada'}), 404

    cursor.execute('UPDATE active_sessions SET is_active = 0 WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()

    log_audit("Angel Rafael (Admin)", "SESSION_REVOKE", f"Revogou sessão ativa #{session_id} pertencente a {sess['name']}")
    return jsonify({'success': True})

if __name__ == '__main__':
    print("Servidor RoleCraft AI iniciado com sucesso na porta 6955!")
    app.run(host='0.0.0.0', port=6955, debug=True)
