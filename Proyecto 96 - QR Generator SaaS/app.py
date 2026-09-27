from flask import Flask, render_template, request, jsonify
import sqlite3
from database import init_db, get_db
import os

app = Flask(__name__)
init_db()

def format_wifi_payload(ssid, password, security):
    sec = security if security in ['WPA', 'WEP', 'nopass'] else 'WPA'
    return f"WIFI:S:{ssid};T:{sec};P:{password};;"

def format_vcard_payload(name, phone, email, company, job):
    return (
        f"BEGIN:VCARD\n"
        f"VERSION:3.0\n"
        f"FN:{name}\n"
        f"ORG:{company}\n"
        f"TITLE:{job}\n"
        f"TEL:{phone}\n"
        f"EMAIL:{email}\n"
        f"END:VCARD"
    )

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM qr_history ORDER BY id DESC")
    history = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM preset_templates")
    presets = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT SUM(downloads) FROM qr_history")
    total_downloads = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return render_template(
        'index.html',
        history=history,
        presets=presets,
        total_downloads=total_downloads
    )

@app.route('/api/generate', methods=['POST'])
def generate_qr():
    data = request.json or {}
    qr_type = data.get('qr_type', 'URL')
    title = data.get('title', 'Código QR')
    fg_color = data.get('fg_color', '#0f172a')
    bg_color = data.get('bg_color', '#ffffff')
    logo_icon = data.get('logo_icon', 'fa-solid fa-qrcode')
    
    payload = ""
    if qr_type == 'URL':
        payload = data.get('url', 'https://ejajtech.com')
    elif qr_type == 'Texto':
        payload = data.get('text', '')
    elif qr_type == 'WiFi':
        ssid = data.get('wifi_ssid', 'Minha_Rede')
        pwd = data.get('wifi_password', '')
        sec = data.get('wifi_security', 'WPA')
        payload = format_wifi_payload(ssid, pwd, sec)
    elif qr_type == 'Contacto':
        name = data.get('card_name', 'Contacto')
        phone = data.get('card_phone', '')
        email = data.get('card_email', '')
        company = data.get('card_company', '')
        job = data.get('card_job', '')
        payload = format_vcard_payload(name, phone, email, company, job)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO qr_history (title, qr_type, payload_data, fg_color, bg_color, logo_icon, downloads)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    ''', (title, qr_type, payload, fg_color, bg_color, logo_icon))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "id": new_id,
        "title": title,
        "payload": payload,
        "fg_color": fg_color,
        "bg_color": bg_color,
        "logo_icon": logo_icon
    })

@app.route('/api/history/<int:qr_id>/download', methods=['POST'])
def record_download(qr_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE qr_history SET downloads = downloads + 1 WHERE id = ?", (qr_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/history/<int:qr_id>', methods=['DELETE'])
def delete_qr(qr_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM qr_history WHERE id = ?", (qr_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Iniciando QRCraft AI — Proyecto 96 na porta 6949...")
    app.run(host='0.0.0.0', port=6949, debug=True)
