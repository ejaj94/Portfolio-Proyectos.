from flask import Flask, render_template, request, jsonify
from database import init_db, get_db
import secrets
from datetime import datetime
import random

app = Flask(__name__)

# Guarantee DB initialization
init_db()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()

    # Fetch API Keys
    cursor.execute('SELECT * FROM api_keys ORDER BY id ASC')
    keys = [dict(row) for row in cursor.fetchall()]

    # Fetch Requests Log
    cursor.execute('''
        SELECT r.*, k.name as key_name, k.key_token
        FROM api_requests r
        LEFT JOIN api_keys k ON r.key_id = k.id
        ORDER BY r.id DESC LIMIT 50
    ''')
    requests_log = [dict(row) for row in cursor.fetchall()]

    # Fetch Errors Log
    cursor.execute('SELECT * FROM api_errors ORDER BY id DESC LIMIT 30')
    errors_log = [dict(row) for row in cursor.fetchall()]

    # Consolidated Metrics & Statistics
    cursor.execute('SELECT COUNT(*) FROM api_requests')
    total_requests = cursor.fetchone()[0]

    cursor.execute('SELECT AVG(latency_ms) FROM api_requests')
    avg_latency = round(cursor.fetchone()[0] or 0, 1)

    cursor.execute('SELECT COUNT(*) FROM api_requests WHERE status_code >= 400')
    total_errors_count = cursor.fetchone()[0]

    error_rate = round((total_errors_count / total_requests * 100) if total_requests > 0 else 0, 2)

    stats = {
        'total_keys': len(keys),
        'active_keys': sum(1 for k in keys if k['status'] == 'Ativa'),
        'total_requests': total_requests,
        'avg_latency': avg_latency,
        'total_errors': total_errors_count,
        'error_rate': error_rate,
        'success_rate': round(100 - error_rate, 2)
    }

    conn.close()
    return render_template('index.html', keys=keys, requests=requests_log, errors=errors_log, stats=stats)

@app.route('/api/keys', methods=['GET', 'POST'])
def handle_keys():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM api_keys ORDER BY id ASC')
        keys = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(keys)

    elif request.method == 'POST':
        data = request.json or {}
        name = data.get('name')
        environment = data.get('environment', 'Production')
        scope = data.get('permission_scope', 'Read-Write')
        limit = int(data.get('rate_limit_per_min', 1000))

        if not name:
            conn.close()
            return jsonify({'error': 'Nome da aplicação/chave é obrigatório'}), 400

        prefix = "sk_live_" if environment == "Production" else "sk_test_"
        token = prefix + secrets.token_hex(16)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO api_keys (name, key_token, environment, permission_scope, rate_limit_per_min, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'Ativa', ?)
        ''', (name, token, environment, scope, limit, now))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'key_token': token}), 201

@app.route('/api/keys/<int:key_id>/revoke', methods=['POST'])
def revoke_key(key_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT status FROM api_keys WHERE id = ?', (key_id,))
    key = cursor.fetchone()
    if not key:
        conn.close()
        return jsonify({'error': 'API Key não encontrada'}), 404

    new_status = 'Revogada' if key['status'] == 'Ativa' else 'Ativa'
    cursor.execute('UPDATE api_keys SET status = ? WHERE id = ?', (new_status, key_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'new_status': new_status})

@app.route('/api/simulate-request', methods=['POST'])
def simulate_request():
    endpoints = ["/v1/users", "/v1/auth/token", "/v1/payments", "/v1/webhooks", "/v1/analytics"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    statuses = [200, 200, 200, 201, 400, 429, 500]

    endpoint = random.choice(endpoints)
    method = random.choice(methods)
    status_code = random.choice(statuses)
    latency = random.randint(15, 450)
    size = round(random.uniform(0.1, 5.0), 2)
    ip = f"193.168.1.{random.randint(2, 250)}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM api_keys WHERE status = "Ativa" ORDER BY RANDOM() LIMIT 1')
    active_key = cursor.fetchone()
    key_id = active_key['id'] if active_key else 1

    cursor.execute('''
        INSERT INTO api_requests (key_id, endpoint, http_method, status_code, latency_ms, payload_size_kb, ip_address, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (key_id, endpoint, method, status_code, latency, size, ip, now))

    if status_code >= 400:
        msg = f"HTTP {status_code} error response encountered on endpoint {endpoint}"
        cursor.execute('''
            INSERT INTO api_errors (endpoint, status_code, error_message, client_ip, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (endpoint, status_code, msg, ip, now))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'status_code': status_code, 'latency': latency})

if __name__ == '__main__':
    print("Servidor APICraft AI iniciado com sucesso na porta 6956!")
    app.run(host='0.0.0.0', port=6956, debug=True)
