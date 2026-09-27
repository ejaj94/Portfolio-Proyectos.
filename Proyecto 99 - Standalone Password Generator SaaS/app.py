from flask import Flask, render_template, request, jsonify
import sqlite3
import math
import random
import string
from database import init_db, get_db
import os

app = Flask(__name__)
init_db()

AMBIGUOUS_CHARS = set("0O1lI|")

def evaluate_entropy(password, pool_size):
    length = len(password)
    if pool_size <= 1:
        return 0, "Muito Fraca", "Instantâneo"
        
    entropy_bits = round(length * math.log2(pool_size), 1)
    combinations = pool_size ** length
    
    # 100 Billion attempts per sec (10^11)
    attempts_per_sec = 100_000_000_000
    seconds = combinations / (2 * attempts_per_sec)
    
    if seconds < 1:
        crack_time = "Instantâneo (< 1 seg)"
        label = "Muito Fraca"
    elif seconds < 60:
        crack_time = f"{int(seconds)} Segundos"
        label = "Fraca"
    elif seconds < 3600:
        crack_time = f"{int(seconds / 60)} Minutos"
        label = "Média"
    elif seconds < 86400:
        crack_time = f"{int(seconds / 3600)} Horas"
        label = "Média"
    elif seconds < 31536000:
        crack_time = f"{int(seconds / 86400)} Dias"
        label = "Forte"
    elif seconds < 315360000:
        crack_time = f"{int(seconds / 31536000)} Anos"
        label = "Forte"
    elif seconds < 31536000000:
        crack_time = f"{int(seconds / 31536000)} Séculos"
        label = "Ultra-Segura"
    else:
        trillions = round(seconds / (31536000 * 1_000_000_000), 1)
        crack_time = f"{trillions} Triliões de Anos"
        label = "Impenetrável"
        
    return entropy_bits, label, crack_time

def build_char_pool(use_upper, use_lower, use_numbers, use_symbols, exclude_ambiguous):
    pool = ""
    if use_lower: pool += string.ascii_lowercase
    if use_upper: pool += string.ascii_uppercase
    if use_numbers: pool += string.digits
    if use_symbols: pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if exclude_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARS)
        
    return pool

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM generation_history ORDER BY id DESC LIMIT 10")
    history = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM generation_history")
    total_generated = cursor.fetchone()[0] or 0

    conn.close()
    
    return render_template(
        'index.html',
        history=history,
        total_generated=total_generated
    )

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json or {}
    length = int(data.get('length', 16))
    use_upper = data.get('uppercase', True)
    use_lower = data.get('lowercase', True)
    use_numbers = data.get('numbers', True)
    use_symbols = data.get('symbols', True)
    exclude_ambiguous = data.get('exclude_ambiguous', False)
    
    pool = build_char_pool(use_upper, use_lower, use_numbers, use_symbols, exclude_ambiguous)
    if not pool:
        pool = string.ascii_lowercase
        
    password = "".join(random.choice(pool) for _ in range(length))
    entropy_bits, label, crack_time = evaluate_entropy(password, len(pool))

    # Mask password for history Privacy
    masked = password[:3] + "..." + password[-3:] if len(password) > 8 else "***"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO generation_history (password_mask, length, entropy_bits, strength_label, crack_time_est)
        VALUES (?, ?, ?, ?, ?)
    ''', (masked, length, entropy_bits, label, crack_time))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "password": password,
        "entropy_bits": entropy_bits,
        "label": label,
        "crack_time": crack_time
    })

@app.route('/api/batch', methods=['POST'])
def generate_batch():
    data = request.json or {}
    count = min(int(data.get('count', 10)), 20)
    length = int(data.get('length', 16))
    use_upper = data.get('uppercase', True)
    use_lower = data.get('lowercase', True)
    use_numbers = data.get('numbers', True)
    use_symbols = data.get('symbols', True)
    
    pool = build_char_pool(use_upper, use_lower, use_numbers, use_symbols, False)
    if not pool: pool = string.ascii_lowercase
    
    batch = []
    for _ in range(count):
        pwd = "".join(random.choice(pool) for _ in range(length))
        bits, label, crack_time = evaluate_entropy(pwd, len(pool))
        batch.append({"password": pwd, "entropy_bits": bits, "label": label})
        
    return jsonify({"status": "success", "batch": batch})

if __name__ == '__main__':
    print("Iniciando KeyCraft AI — Proyecto 99 na porta 6952...")
    app.run(host='0.0.0.0', port=6952, debug=True)
