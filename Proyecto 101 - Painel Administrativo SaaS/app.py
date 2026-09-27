from flask import Flask, render_template, request, jsonify
import sqlite3
from database import init_db, get_db
import os

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM admin_users ORDER BY id ASC")
    users = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM permissions_matrix ORDER BY id ASC")
    permissions = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM system_config WHERE id = 1")
    config = dict(cursor.fetchone())
    
    cursor.execute("SELECT * FROM system_logs ORDER BY id DESC LIMIT 15")
    logs = [dict(row) for row in cursor.fetchall()]

    # Stats calculation
    total_users = len(users)
    active_users = sum(1 for u in users if u['status'] == 'Ativo')
    error_logs_count = sum(1 for l in logs if l['log_level'] == 'ERROR')

    conn.close()
    
    return render_template(
        'index.html',
        users=users,
        permissions=permissions,
        config=config,
        logs=logs,
        stats={
            "total_users": total_users,
            "active_users": active_users,
            "error_logs_count": error_logs_count,
            "cpu_load": 24,
            "ram_usage": "4.2 GB / 16 GB",
            "active_sessions": 128
        }
    )

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json or {}
    name = data.get('name', 'Novo Administrador')
    email = data.get('email', '')
    role = data.get('role', 'Editor')
    
    if not email:
        return jsonify({"status": "error", "message": "E-mail é obrigatório"}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    avatar = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80"
    cursor.execute('''
        INSERT INTO admin_users (name, email, role, status, avatar_url)
        VALUES (?, ?, ?, 'Ativo', ?)
    ''', (name, email, role, avatar))
    
    cursor.execute('''
        INSERT INTO system_logs (log_level, message, module, ip_address)
        VALUES ('INFO', ?, 'USER_MANAGEMENT', '193.168.1.10')
    ''', (f"Novo utilizador administrativo criado: {name} ({role})",))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Utilizador criado com sucesso!"})

@app.route('/api/users/<int:user_id>/status', methods=['POST'])
def toggle_status(user_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT status, name FROM admin_users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"status": "error", "message": "Utilizador não encontrado"}), 404
        
    new_status = 'Inativo' if row['status'] == 'Ativo' else 'Ativo'
    cursor.execute("UPDATE admin_users SET status = ? WHERE id = ?", (new_status, user_id))
    
    cursor.execute('''
        INSERT INTO system_logs (log_level, message, module, ip_address)
        VALUES ('INFO', ?, 'USER_MANAGEMENT', '193.168.1.10')
    ''', (f"Estado do utilizador {row['name']} alterado para {new_status}",))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "new_status": new_status})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admin_users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/permissions', methods=['POST'])
def update_permissions():
    data = request.json or {}
    role_name = data.get('role_name')
    can_read = 1 if data.get('can_read') else 0
    can_write = 1 if data.get('can_write') else 0
    can_delete = 1 if data.get('can_delete') else 0
    can_config = 1 if data.get('can_config') else 0
    can_logs = 1 if data.get('can_logs') else 0

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE permissions_matrix
        SET can_read = ?, can_write = ?, can_delete = ?, can_config = ?, can_logs = ?
        WHERE role_name = ?
    ''', (can_read, can_write, can_delete, can_config, can_logs, role_name))
    
    cursor.execute('''
        INSERT INTO system_logs (log_level, message, module, ip_address)
        VALUES ('WARNING', ?, 'RBAC_CORE', '193.168.1.10')
    ''', (f"Matriz de permissões alterada para a função: {role_name}",))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Matriz de permissões atualizada!"})

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json or {}
    site_name = data.get('site_name', 'EJAJ TECH Enterprise Cloud')
    maint = 1 if data.get('maintenance_mode') else 0
    ssl = 1 if data.get('ssl_enforced') else 0
    smtp = data.get('smtp_host', 'smtp.ejajtech.com')
    max_mb = int(data.get('max_upload_mb', 50))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE system_config
        SET site_name = ?, maintenance_mode = ?, ssl_enforced = ?, smtp_host = ?, max_upload_mb = ?
        WHERE id = 1
    ''', (site_name, maint, ssl, smtp, max_mb))
    
    cursor.execute('''
        INSERT INTO system_logs (log_level, message, module, ip_address)
        VALUES ('WARNING', ?, 'SYSTEM_CONFIG', '193.168.1.10')
    ''', (f"Configurações globais do sistema alteradas (Modo Manutenção: {maint})",))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Configurações globais guardadas!"})

if __name__ == '__main__':
    print("Iniciando AdminPulse AI — Proyecto 101 na porta 6954...")
    app.run(host='0.0.0.0', port=6954, debug=True)
