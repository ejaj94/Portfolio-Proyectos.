from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db
import os

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users ORDER BY id ASC")
    users = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM security_logs ORDER BY id DESC LIMIT 15")
    logs = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM otp_tokens ORDER BY id DESC LIMIT 5")
    otps = [dict(row) for row in cursor.fetchall()]

    # Stats
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE verified = 1")
    verified_users = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM security_logs")
    total_logs = cursor.fetchone()[0] or 0

    conn.close()
    
    return render_template(
        'index.html',
        users=users,
        logs=logs,
        otps=otps,
        stats={
            "total_users": total_users,
            "verified_users": verified_users,
            "total_logs": total_logs
        }
    )

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}
    full_name = data.get('full_name', 'Novo Utilizador')
    email = data.get('email', '')
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({"status": "error", "message": "E-mail e palavra-passe obrigatórios"}), 400

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status": "error", "message": "Este e-mail já se encontra registado!"}), 400

    pwd_hash = generate_password_hash(password)
    avatar = f"https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80"
    
    cursor.execute('''
        INSERT INTO users (full_name, email, password_hash, role, verified, avatar_url)
        VALUES (?, ?, ?, 'Standard', 0, ?)
    ''', (full_name, email, pwd_hash, avatar))
    
    new_id = cursor.lastrowid
    
    # Log registration event
    cursor.execute('''
        INSERT INTO security_logs (user_id, user_email, action, ip_address, device)
        VALUES (?, ?, 'Novo Registo de Utilizador (Pendente de OTP)', '193.168.1.150', 'Desktop (Chrome)')
    ''', (new_id, email))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Registo efetuado com sucesso! Código OTP enviado."})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email', '')
    password = data.get('password', '')

    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user or not check_password_hash(user['password_hash'], password):
        # Log failed attempt
        cursor.execute('''
            INSERT INTO security_logs (user_id, user_email, action, ip_address, device)
            VALUES (0, ?, 'Tentativa de Login Falhada (Credenciais Inválidas)', '193.168.1.150', 'Desktop (Chrome)')
        ''', (email,))
        conn.commit()
        conn.close()
        return jsonify({"status": "error", "message": "E-mail ou palavra-passe incorretos!"}), 401

    # Log successful login
    cursor.execute('''
        INSERT INTO security_logs (user_id, user_email, action, ip_address, device)
        VALUES (?, ?, 'Login Efetuado com Sucesso', '193.168.1.150', 'Desktop (Chrome)')
    ''', (user['id'], email))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "success",
        "message": "Autenticação bem-sucedida!",
        "user": {
            "id": user['id'],
            "name": user['full_name'],
            "email": user['email'],
            "role": user['role'],
            "verified": bool(user['verified'])
        }
    })

@app.route('/api/recover-request', methods=['POST'])
def recover_request():
    data = request.json or {}
    email = data.get('email', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({"status": "error", "message": "E-mail não encontrado no sistema"}), 404
        
    otp_code = str(random.randint(100000, 999999))
    
    cursor.execute('''
        INSERT INTO otp_tokens (user_id, email, token_code, expires_at)
        VALUES (?, ?, ?, datetime('now', '+15 minutes'))
    ''', (user['id'], email, otp_code))
    
    cursor.execute('''
        INSERT INTO security_logs (user_id, user_email, action, ip_address, device)
        VALUES (?, ?, 'Gerado Código OTP de Recuperação', '193.168.1.150', 'Mobile (App)')
    ''', (user['id'], email))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "success",
        "message": f"Código OTP gerado com sucesso: {otp_code}",
        "otp": otp_code
    })

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json or {}
    email = data.get('email', '')
    code = data.get('code', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM otp_tokens WHERE email = ? AND token_code = ? AND used = 0 ORDER BY id DESC LIMIT 1", (email, code))
    token = cursor.fetchone()
    
    if not token:
        conn.close()
        return jsonify({"status": "error", "message": "Código OTP inválido ou já utilizado!"}), 400
        
    cursor.execute("UPDATE otp_tokens SET used = 1 WHERE id = ?", (token['id'],))
    cursor.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
    
    cursor.execute('''
        INSERT INTO security_logs (user_id, user_email, action, ip_address, device)
        VALUES (?, ?, 'Verificação de Conta por OTP Concluída com Sucesso', '193.168.1.150', 'Desktop (Chrome)')
    ''', (token['user_id'], email))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Conta verificada e ativada com sucesso!"})

@app.route('/api/update-role', methods=['POST'])
def update_role():
    data = request.json or {}
    user_id = data.get('user_id')
    new_role = data.get('role', 'Standard')
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"status": "error", "message": "Utilizador não encontrado"}), 404
        
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    
    cursor.execute('''
        INSERT INTO security_logs (user_id, user_email, action, ip_address, device)
        VALUES (?, ?, ?, '193.168.1.10', 'Console Super Admin')
    ''', (user_id, row['email'], f"Alteração de Função RBAC -> {new_role}"))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Função RBAC atualizada com sucesso!"})

if __name__ == '__main__':
    print("Iniciando AuthCraft AI — Proyecto 100 na porta 6953...")
    app.run(host='0.0.0.0', port=6953, debug=True)
