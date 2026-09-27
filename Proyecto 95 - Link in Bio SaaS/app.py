from flask import Flask, render_template, request, jsonify
import sqlite3
from database import init_db, get_db
import datetime
import os

app = Flask(__name__)

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM profile WHERE id = 1")
    profile = dict(cursor.fetchone())
    
    cursor.execute("SELECT * FROM links ORDER BY position ASC, id ASC")
    links = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM social_links WHERE active = 1")
    socials = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM theme_config WHERE id = 1")
    theme = dict(cursor.fetchone())
    
    # Calculate analytics
    cursor.execute("SELECT SUM(clicks) FROM links")
    total_clicks = cursor.fetchone()[0] or 0
    total_views = total_clicks + 480 # Simulated total pageviews
    ctr = round((total_clicks / total_views * 100), 1) if total_views > 0 else 0
    
    cursor.execute("SELECT title, clicks FROM links ORDER BY clicks DESC LIMIT 1")
    top_link_row = cursor.fetchone()
    top_link = top_link_row['title'] if top_link_row else 'Nenhum'
    
    cursor.execute("SELECT * FROM clicks_log ORDER BY id DESC LIMIT 10")
    clicks_log = [dict(row) for row in cursor.fetchall()]

    conn.close()
    
    return render_template(
        'index.html',
        profile=profile,
        links=links,
        socials=socials,
        theme=theme,
        analytics={
            "total_views": total_views,
            "total_clicks": total_clicks,
            "ctr": ctr,
            "top_link": top_link,
            "logs": clicks_log
        }
    )

@app.route('/api/profile', methods=['POST'])
def update_profile():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE profile
        SET name = ?, handle = ?, bio = ?, avatar_url = ?, location = ?, verified = ?
        WHERE id = 1
    ''', (
        data.get('name', 'Enmanuel Jimenez'),
        data.get('handle', '@ejajtech'),
        data.get('bio', ''),
        data.get('avatar_url', ''),
        data.get('location', 'Lisboa, Portugal'),
        1 if data.get('verified') else 0
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Perfil atualizado com sucesso!"})

@app.route('/api/links', methods=['GET', 'POST'])
def handle_links():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        data = request.json or {}
        cursor.execute('''
            INSERT INTO links (title, url, icon, badge, highlight, position)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (
            data.get('title', 'Novo Link'),
            data.get('url', 'https://ejajtech.com'),
            data.get('icon', 'fa-solid fa-link'),
            data.get('badge', ''),
            1 if data.get('highlight') else 0
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Link adicionado com sucesso!"})
    
    cursor.execute("SELECT * FROM links ORDER BY position ASC, id ASC")
    links = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(links)

@app.route('/api/links/<int:link_id>', methods=['DELETE', 'PUT'])
def modify_link(link_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM links WHERE id = ?", (link_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Link eliminado com sucesso!"})
    
    data = request.json or {}
    cursor.execute('''
        UPDATE links
        SET title = ?, url = ?, icon = ?, badge = ?, highlight = ?
        WHERE id = ?
    ''', (
        data.get('title'),
        data.get('url'),
        data.get('icon'),
        data.get('badge'),
        1 if data.get('highlight') else 0,
        link_id
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Link atualizado!"})

@app.route('/api/links/<int:link_id>/click', methods=['POST'])
def record_click(link_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Increment link clicks
    cursor.execute("UPDATE links SET clicks = clicks + 1 WHERE id = ?", (link_id,))
    
    # Fetch link title
    cursor.execute("SELECT title FROM links WHERE id = ?", (link_id,))
    link_row = cursor.fetchone()
    link_title = link_row['title'] if link_row else 'Link Desconhecido'
    
    # Insert into clicks log
    cursor.execute('''
        INSERT INTO clicks_log (link_id, link_title, timestamp, ip_simulated, device, location)
        VALUES (?, ?, datetime('now'), '193.168.1.100', 'Mobile (iOS App)', 'Lisboa, Portugal')
    ''', (link_id, link_title))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Clique registado!"})

@app.route('/api/theme', methods=['POST'])
def update_theme():
    data = request.json or {}
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE theme_config
        SET theme_name = ?, bg_style = ?, button_style = ?, font_family = ?, accent_color = ?
        WHERE id = 1
    ''', (
        data.get('theme_name', 'cyber-glass'),
        data.get('bg_style', 'animated-gradient'),
        data.get('button_style', 'pill-glass'),
        data.get('font_family', 'Plus Jakarta Sans'),
        data.get('accent_color', '#38bdf8')
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Tema atualizado!"})

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(clicks) FROM links")
    total_clicks = cursor.fetchone()[0] or 0
    total_views = total_clicks + 480
    ctr = round((total_clicks / total_views * 100), 1) if total_views > 0 else 0
    
    cursor.execute("SELECT title, clicks FROM links ORDER BY clicks DESC LIMIT 1")
    top_link_row = cursor.fetchone()
    top_link = top_link_row['title'] if top_link_row else 'Nenhum'
    
    cursor.execute("SELECT * FROM clicks_log ORDER BY id DESC LIMIT 10")
    logs = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({
        "total_views": total_views,
        "total_clicks": total_clicks,
        "ctr": ctr,
        "top_link": top_link,
        "logs": logs
    })

if __name__ == '__main__':
    print("Iniciando BioCraft AI — Proyecto 95 en port 6948...")
    app.run(host='0.0.0.0', port=6948, debug=True)
