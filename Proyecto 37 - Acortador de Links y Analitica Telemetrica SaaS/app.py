import os
import random
import string
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'ejajtech_veloce_link_secret_key_2026'

# Inicializar BD
database.init_db()

BASE_HOST = 'http://127.0.0.1:6050'

def generate_random_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def detect_device_and_os(user_agent):
    ua = user_agent.lower()
    
    # Device
    if 'mobile' in ua or 'iphone' in ua or 'android' in ua:
        device = 'Mobile'
    elif 'ipad' in ua or 'tablet' in ua:
        device = 'Tablet'
    else:
        device = 'Desktop'

    # OS
    if 'windows' in ua:
        os_name = 'Windows'
    elif 'macintosh' in ua or 'mac os' in ua:
        os_name = 'macOS'
    elif 'iphone' in ua or 'ipad' in ua:
        os_name = 'iOS'
    elif 'android' in ua:
        os_name = 'Android'
    elif 'linux' in ua:
        os_name = 'Linux'
    else:
        os_name = 'Outro'

    # Browser
    if 'edg' in ua:
        browser = 'Edge'
    elif 'chrome' in ua and 'safari' in ua:
        browser = 'Chrome'
    elif 'safari' in ua and 'chrome' not in ua:
        browser = 'Safari'
    elif 'firefox' in ua:
        browser = 'Firefox'
    else:
        browser = 'Navegador Web'

    return device, os_name, browser

# --- MOTOR DE REDIRECÇÃO HTTP 302 ---

@app.route('/<short_code>')
def redirect_short_link(short_code):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Buscar link por código ou alias
    cursor.execute('SELECT * FROM links WHERE short_code = ? OR custom_alias = ?', (short_code, short_code))
    link = cursor.fetchone()

    if not link or not link['is_active']:
        conn.close()
        flash('O hiperlink solicitado não existe ou foi desativado.', 'danger')
        return redirect(url_for('index'))

    link_id = link['id']
    target_url = link['original_url']

    # Capturar telemetria do visitante
    ip_addr = request.remote_addr or '185.210.45.12'
    user_agent = request.headers.get('User-Agent', '')
    referrer = request.headers.get('Referer', 'Acesso Direto / WhatsApp')

    device_type, os_name, browser_name = detect_device_and_os(user_agent)

    # Simulação de geolocalização por país para demonstração
    countries_pool = [
        ('PT', 'Portugal', 'Lisboa'),
        ('PT', 'Portugal', 'Porto'),
        ('ES', 'Espanha', 'Madrid'),
        ('FR', 'França', 'Paris'),
        ('US', 'Estados Unidos', 'New York')
    ]
    cnt = random.choice(countries_pool)

    # Incrementar contador total de clics
    cursor.execute('UPDATE links SET total_clicks = total_clicks + 1 WHERE id = ?', (link_id,))

    # Registar log telemétrico
    cursor.execute('''
        INSERT INTO clicks_log (link_id, ip_address, country_code, country_name, city, device_type, os_name, browser_name, referrer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (link_id, ip_addr, cnt[0], cnt[1], cnt[2], device_type, os_name, browser_name, referrer))

    conn.commit()
    conn.close()

    # Redireção 302 para URL original
    return redirect(target_url, code=302)


# --- ROTAS DA CONSOLA WEB ---

@app.route('/')
def index():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Parâmetro de pesquisa
    search_q = request.args.get('q', '').strip()

    query = 'SELECT * FROM links WHERE 1=1'
    params = []

    if search_q:
        query += ' AND (title LIKE ? OR short_code LIKE ? OR custom_alias LIKE ? OR original_url LIKE ?)'
        wildcard = f'%{search_q}%'
        params.extend([wildcard, wildcard, wildcard, wildcard])

    query += ' ORDER BY created_at DESC'
    cursor.execute(query, params)
    links = cursor.fetchall()

    # KPIs Telemétricos Gerais
    cursor.execute('SELECT COUNT(*) FROM links')
    total_links = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(total_clicks) FROM links')
    sum_clicks = cursor.fetchone()[0] or 0

    cursor.execute('SELECT country_name, COUNT(*) as cnt FROM clicks_log GROUP BY country_name ORDER BY cnt DESC LIMIT 1')
    top_country_row = cursor.fetchone()
    top_country = top_country_row['country_name'] if top_country_row else 'Portugal'

    cursor.execute('SELECT device_type, COUNT(*) as cnt FROM clicks_log GROUP BY device_type ORDER BY cnt DESC LIMIT 1')
    top_device_row = cursor.fetchone()
    top_device = top_device_row['device_type'] if top_device_row else 'Desktop'

    conn.close()

    return render_template(
        'index.html',
        links=links,
        total_links=total_links,
        sum_clicks=sum_clicks,
        top_country=top_country,
        top_device=top_device,
        search_q=search_q,
        base_host=BASE_HOST
    )


@app.route('/stats/<code_or_alias>')
def stats(code_or_alias):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM links WHERE short_code = ? OR custom_alias = ?', (code_or_alias, code_or_alias))
    link = cursor.fetchone()

    if not link:
        conn.close()
        flash('O hiperlink solicitado não foi encontrado.', 'danger')
        return redirect(url_for('index'))

    link_id = link['id']

    # Historial de Clics Telemétricos
    cursor.execute('SELECT * FROM clicks_log WHERE link_id = ? ORDER BY clicked_at DESC LIMIT 50', (link_id,))
    clicks = cursor.fetchall()

    # Telemetria por País
    cursor.execute('SELECT country_code, country_name, COUNT(*) as count FROM clicks_log WHERE link_id = ? GROUP BY country_name ORDER BY count DESC', (link_id,))
    countries_stats = cursor.fetchall()

    # Telemetria por Dispositivo
    cursor.execute('SELECT device_type, COUNT(*) as count FROM clicks_log WHERE link_id = ? GROUP BY device_type ORDER BY count DESC', (link_id,))
    devices_stats = cursor.fetchall()

    # Telemetria por Sistema Operativo
    cursor.execute('SELECT os_name, COUNT(*) as count FROM clicks_log WHERE link_id = ? GROUP BY os_name ORDER BY count DESC', (link_id,))
    os_stats = cursor.fetchall()

    conn.close()

    return render_template(
        'stats.html',
        link=link,
        clicks=clicks,
        countries_stats=countries_stats,
        devices_stats=devices_stats,
        os_stats=os_stats,
        base_host=BASE_HOST
    )


# --- APIS REST ---

@app.route('/api/links/create', methods=['POST'])
def api_create_link():
    data = request.form if request.form else (request.json or {})
    title = data.get('title', '').strip()
    original_url = data.get('original_url', '').strip()
    custom_alias = data.get('custom_alias', '').strip()

    if not original_url:
        if request.is_json:
            return jsonify({'success': False, 'message': 'O URL de destino é obrigatório'}), 400
        flash('O URL de destino é obrigatório.', 'danger')
        return redirect(url_for('index'))

    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    if not title:
        title = original_url.replace('https://', '').replace('http://', '').split('/')[0]

    short_code = custom_alias if custom_alias else generate_random_code(6)

    # QR Code via QuickChart
    short_full_url = f"{BASE_HOST}/{short_code}"
    qr_code_url = f"https://api.quickchart.io/qr?text={short_full_url}&size=250"

    conn = database.get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO links (short_code, title, original_url, custom_alias, qr_code_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (short_code, title, original_url, custom_alias or None, qr_code_url))
        conn.commit()
        new_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        msg = f"O alias '{custom_alias or short_code}' já está em utilização. Escolha outro."
        if request.is_json:
            return jsonify({'success': False, 'message': msg}), 400
        flash(msg, 'danger')
        return redirect(url_for('index'))

    conn.close()

    if request.is_json:
        return jsonify({
            'success': True,
            'short_code': short_code,
            'short_url': short_full_url,
            'original_url': original_url,
            'qr_code_url': qr_code_url
        })

    flash(f'¡Hiperlink encurtado com sucesso! Código: {short_code}', 'success')
    return redirect(url_for('stats', code_or_alias=short_code))


@app.route('/api/links/<code_or_alias>/analytics')
def api_link_analytics(code_or_alias):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM links WHERE short_code = ? OR custom_alias = ?', (code_or_alias, code_or_alias))
    link = cursor.fetchone()

    if not link:
        conn.close()
        return jsonify({'success': False, 'message': 'Link não encontrado'}), 404

    link_id = link['id']

    cursor.execute('SELECT country_name, COUNT(*) as count FROM clicks_log WHERE link_id = ? GROUP BY country_name ORDER BY count DESC', (link_id,))
    countries = [dict(r) for r in cursor.fetchall()]

    cursor.execute('SELECT device_type, COUNT(*) as count FROM clicks_log WHERE link_id = ? GROUP BY device_type ORDER BY count DESC', (link_id,))
    devices = [dict(r) for r in cursor.fetchall()]

    cursor.execute('SELECT os_name, COUNT(*) as count FROM clicks_log WHERE link_id = ? GROUP BY os_name ORDER BY count DESC', (link_id,))
    os_list = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return jsonify({
        'success': True,
        'countries': countries,
        'devices': devices,
        'os': os_list
    })


if __name__ == '__main__':
    print("=" * 60)
    print(" [VELOCE-LINK SaaS] EJAJ TECH Telemetric Link Shortener Suite")
    print(" Servidor Flask a correr em http://127.0.0.1:6050")
    print("=" * 60)
    app.run(host='0.0.0.0', port=6050, debug=True)
