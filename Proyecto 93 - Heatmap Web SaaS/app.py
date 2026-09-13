import os
import sqlite3
import csv
import io
import datetime
import random
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/clicks')
def clicks():
    return render_template('clicks.html', active_page='clicks')

@app.route('/scroll')
def scroll():
    return render_template('scroll.html', active_page='scroll')

@app.route('/hotzones')
def hotzones():
    return render_template('hotzones.html', active_page='hotzones')

@app.route('/pages')
def pages():
    return render_template('pages.html', active_page='pages')

@app.route('/users')
def users():
    return render_template('users.html', active_page='users')

@app.route('/stats')
def stats():
    return render_template('stats.html', active_page='stats')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html', active_page='showcase')

# --- REST API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(total_clicks), AVG(avg_scroll_pct), SUM(total_sessions) FROM monitored_pages')
    row = cursor.fetchone()

    total_clicks = row[0] or 0
    avg_scroll = round(row[1] or 0.0, 1)
    total_sessions = row[2] or 0

    cursor.execute('SELECT page_title, page_path FROM monitored_pages ORDER BY total_clicks DESC LIMIT 1')
    top_page = cursor.fetchone()
    top_page_title = top_page['page_title'] if top_page else 'Landing Page'

    cursor.execute('SELECT COUNT(*) FROM click_events')
    tracked_events = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'total_clicks': total_clicks,
        'avg_scroll_pct': avg_scroll,
        'total_sessions': total_sessions,
        'top_page_title': top_page_title,
        'tracked_events': tracked_events,
        'hotspot_intensity': '🔥 Alta (Hot)'
    })

@app.route('/api/clicks', methods=['GET'])
def get_clicks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM click_events ORDER BY id DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/scroll', methods=['GET'])
def get_scroll():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scroll_metrics ORDER BY id ASC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/hotzones', methods=['GET'])
def get_hotzones():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT target_element, COUNT(*) as click_count, AVG(pos_x_pct) as avg_x, AVG(pos_y_px) as avg_y
        FROM click_events
        GROUP BY target_element
        ORDER BY click_count DESC
    ''')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/pages', methods=['GET'])
def get_pages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM monitored_pages ORDER BY total_clicks DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_sessions ORDER BY id DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT page_path as Pagina, page_title as Titulo, total_clicks as Cliques_Totais,
               avg_scroll_pct as Scroll_Medio_Pct, total_sessions as Sessoes,
               hotspot_score as Score_Termico
        FROM monitored_pages
    ''')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if fmt == 'json':
        return jsonify(rows)
    elif fmt == 'csv':
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_heatmap_analytics.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando HotTrace AI — Heatmap Web SaaS na porta 6946...")
    app.run(host='0.0.0.0', port=6946, debug=True)
