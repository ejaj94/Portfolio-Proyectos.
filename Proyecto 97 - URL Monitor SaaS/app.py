from flask import Flask, render_template, request, jsonify
import sqlite3
import time
import urllib.request
import urllib.error
from database import init_db, get_db
import os

app = Flask(__name__)
init_db()

def perform_http_check(url):
    start_time = time.perf_counter()
    status_code = 500
    status_label = "500 Error"
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'UptimePulseAI/1.0 (EJAJ TECH Health Check)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            status_label = f"{status_code} OK"
    except urllib.error.HTTPError as e:
        status_code = e.code
        status_label = f"{status_code} HTTP Error"
    except urllib.error.URLError as e:
        status_code = 503
        status_label = "503 Unavailable"
    except Exception as e:
        status_code = 500
        status_label = "500 Timeout"

    latency_ms = int((time.perf_counter() - start_time) * 1000)
    return status_code, latency_ms, status_label

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM monitored_urls ORDER BY id DESC")
    monitors = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM check_logs ORDER BY id DESC LIMIT 15")
    logs = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 10")
    alerts = [dict(row) for row in cursor.fetchall()]
    
    # Aggregated Stats
    cursor.execute("SELECT AVG(uptime_percentage), AVG(last_latency_ms), SUM(total_checks) FROM monitored_urls")
    avg_row = cursor.fetchone()
    avg_uptime = round(avg_row[0] or 100.0, 2)
    avg_latency = int(avg_row[1] or 25)
    total_checks = avg_row[2] or 0
    
    cursor.execute("SELECT COUNT(*) FROM monitored_urls WHERE status != 'Operational'")
    incidents_count = cursor.fetchone()[0] or 0

    conn.close()
    
    return render_template(
        'index.html',
        monitors=monitors,
        logs=logs,
        alerts=alerts,
        stats={
            "avg_uptime": avg_uptime,
            "avg_latency": avg_latency,
            "total_checks": total_checks,
            "incidents_count": incidents_count
        }
    )

@app.route('/api/monitors', methods=['GET', 'POST'])
def handle_monitors():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name', 'Novo Monitor')
        target_url = data.get('target_url', 'https://ejajtech.com')
        
        # Immediate first check
        code, latency, label = perform_http_check(target_url)
        status = 'Operational' if code == 200 else 'Degraded' if code < 500 else 'Offline'
        
        cursor.execute('''
            INSERT INTO monitored_urls (name, target_url, status, last_status_code, last_latency_ms, uptime_percentage, total_checks, failed_checks)
            VALUES (?, ?, ?, ?, ?, 100.0, 1, ?)
        ''', (name, target_url, status, code, latency, 0 if code == 200 else 1))
        
        new_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO check_logs (url_id, url_name, timestamp, status_code, latency_ms, status_label)
            VALUES (?, ?, datetime('now'), ?, ?, ?)
        ''', (new_id, name, code, latency, label))
        
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Monitor adicionado com sucesso!"})

    cursor.execute("SELECT * FROM monitored_urls ORDER BY id DESC")
    monitors = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(monitors)

@app.route('/api/monitors/<int:url_id>/ping', methods=['POST'])
def ping_monitor(url_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM monitored_urls WHERE id = ?", (url_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"status": "error", "message": "Monitor não encontrado"}), 404

    target_url = row['target_url']
    url_name = row['name']
    
    code, latency, label = perform_http_check(target_url)
    status = 'Operational' if code == 200 else 'Degraded' if code < 500 else 'Offline'
    
    new_total = row['total_checks'] + 1
    new_failed = row['failed_checks'] + (0 if code == 200 else 1)
    new_uptime = round(((new_total - new_failed) / new_total * 100), 2)
    
    cursor.execute('''
        UPDATE monitored_urls
        SET status = ?, last_status_code = ?, last_latency_ms = ?, uptime_percentage = ?, total_checks = ?, failed_checks = ?
        WHERE id = ?
    ''', (status, code, latency, new_uptime, new_total, new_failed, url_id))
    
    cursor.execute('''
        INSERT INTO check_logs (url_id, url_name, timestamp, status_code, latency_ms, status_label)
        VALUES (?, ?, datetime('now'), ?, ?, ?)
    ''', (url_id, url_name, code, latency, label))
    
    if code != 200:
        cursor.execute('''
            INSERT INTO alerts (url_id, url_name, alert_type, message, timestamp, resolved)
            VALUES (?, ?, ?, ?, datetime('now'), 0)
        ''', (url_id, url_name, 'Falha HTTP', f"Resposta anómala ({code}): {label}", 0))

    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "success",
        "url_id": url_id,
        "status_code": code,
        "latency_ms": latency,
        "status_label": label,
        "uptime_percentage": new_uptime
    })

@app.route('/api/monitors/<int:url_id>', methods=['DELETE'])
def delete_monitor(url_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monitored_urls WHERE id = ?", (url_id,))
    cursor.execute("DELETE FROM check_logs WHERE url_id = ?", (url_id,))
    cursor.execute("DELETE FROM alerts WHERE url_id = ?", (url_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Iniciando UptimePulse AI — Proyecto 97 na porta 6950...")
    app.run(host='0.0.0.0', port=6950, debug=True)
