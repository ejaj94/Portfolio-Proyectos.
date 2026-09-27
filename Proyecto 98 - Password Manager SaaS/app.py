from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import string
from database import init_db, get_db
import os

app = Flask(__name__)
init_db()

def calculate_strength(pwd):
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_symbol = any(c in string.punctuation for c in pwd)
    
    score = min(length * 4, 40)
    if has_upper: score += 15
    if has_lower: score += 15
    if has_digit: score += 15
    if has_symbol: score += 15
    
    score = min(score, 100)
    if score >= 90:
        label = "Ultra-Forte"
    elif score >= 75:
        label = "Forte"
    elif score >= 50:
        label = "Média"
    else:
        label = "Fraca"
        
    return score, label

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = 1")
    user = dict(cursor.fetchone())
    
    cursor.execute("SELECT * FROM vault_items ORDER BY id DESC")
    vault_items = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM categories")
    categories = [dict(row) for row in cursor.fetchall()]

    # Security Audit calculation
    total_items = len(vault_items)
    weak_count = sum(1 for item in vault_items if item['strength_score'] < 60)
    
    # Check reused passwords
    passwords = [item['encrypted_password'] for item in vault_items]
    reused_count = len(passwords) - len(set(passwords))
    
    avg_score = int(sum(item['strength_score'] for item in vault_items) / total_items) if total_items > 0 else 100
    health_score = max(avg_score - (weak_count * 5) - (reused_count * 10), 20)

    conn.close()
    
    return render_template(
        'index.html',
        user=user,
        vault_items=vault_items,
        categories=categories,
        audit={
            "total_items": total_items,
            "weak_count": weak_count,
            "reused_count": reused_count,
            "health_score": health_score
        }
    )

@app.route('/api/vault', methods=['GET', 'POST'])
def handle_vault():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json or {}
        title = data.get('title', 'Nova Credencial')
        username = data.get('username', '')
        password = data.get('password', '')
        category = data.get('category', 'Pessoal')
        website_url = data.get('website_url', '')
        notes = data.get('notes', '')
        
        score, label = calculate_strength(password)
        
        cursor.execute('''
            INSERT INTO vault_items (user_id, title, username, encrypted_password, category, website_url, notes, strength_score, strength_label)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, username, password, category, website_url, notes, score, label))
        
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Credencial guardada com sucesso!"})

    cursor.execute("SELECT * FROM vault_items ORDER BY id DESC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

@app.route('/api/vault/<int:item_id>', methods=['DELETE'])
def delete_vault_item(item_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vault_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/generate-password', methods=['POST'])
def generate_password():
    data = request.json or {}
    length = int(data.get('length', 16))
    use_upper = data.get('uppercase', True)
    use_numbers = data.get('numbers', True)
    use_symbols = data.get('symbols', True)
    
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_numbers: chars += string.digits
    if use_symbols: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    pwd = "".join(random.choice(chars) for _ in range(length))
    score, label = calculate_strength(pwd)
    
    return jsonify({
        "password": pwd,
        "score": score,
        "label": label
    })

if __name__ == '__main__':
    print("Iniciando PassCraft AI — Proyecto 98 na porta 6951...")
    app.run(host='0.0.0.0', port=6951, debug=True)
