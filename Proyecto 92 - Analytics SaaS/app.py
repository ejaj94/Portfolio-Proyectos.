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

@app.route('/users')
def users():
    return render_template('users.html', active_page='users')

@app.route('/geo_tech')
def geo_tech():
    return render_template('geo_tech.html', active_page='geo_tech')

@app.route('/pages_sources')
def pages_sources():
    return render_template('pages_sources.html', active_page='pages_sources')

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

    cursor.execute('SELECT SUM(visits), SUM(unique_visitors), SUM(pageviews), AVG(bounce_rate), AVG(avg_duration_sec) FROM daily_traffic')
    row = cursor.fetchone()

    total_visits = row[0] or 0
    total_uniques = row[1] or 0
    total_pageviews = row[2] or 0
    avg_bounce_rate = round(row[3] or 0.0, 1)
    avg_duration_sec = int(row[4] or 0)

    # Format duration (e.g. 2m 45s)
    mins = avg_duration_sec // 60
    secs = avg_duration_sec % 60
    duration_str = f"{mins}m {secs}s"

    # Simulate real-time online active users right now
    realtime_online = random.randint(142, 189)

    conn.close()

    return jsonify({
        'realtime_online': realtime_online,
        'total_visits': total_visits,
        'total_uniques': total_uniques,
        'total_pageviews': total_pageviews,
        'avg_bounce_rate': avg_bounce_rate,
        'avg_duration_str': duration_str
    })

@app.route('/api/traffic_chart', methods=['GET'])
def get_traffic_chart():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM daily_traffic ORDER BY id ASC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/countries', methods=['GET'])
def get_countries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM country_analytics ORDER BY visitors_count DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/devices', methods=['GET'])
def get_devices():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM device_analytics ORDER BY id ASC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # Group by category
    categorized = {
        'Device': [r for r in rows if r['category'] == 'Device'],
        'OS': [r for r in rows if r['category'] == 'OS'],
        'Browser': [r for r in rows if r['category'] == 'Browser']
    }
    return jsonify(categorized)

@app.route('/api/pages', methods=['GET'])
def get_pages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM top_pages ORDER BY pageviews DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/sources', methods=['GET'])
def get_sources():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM traffic_sources ORDER BY visits DESC')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date_str as Data, visits as Visitas, unique_visitors as Utilizadores_Unicos,
               pageviews as Visualizacoes_Pagina, bounce_rate as Taxa_Rejeicao_Pct,
               avg_duration_sec as Duracao_Media_Seg
        FROM daily_traffic
        ORDER BY id DESC
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_web_analytics.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando PulseAnalytics AI — Web Analytics SaaS na porta 6945...")
    app.run(host='0.0.0.0', port=6945, debug=True)
