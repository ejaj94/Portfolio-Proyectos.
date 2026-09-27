import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'presentation20.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects_showcase_20 ORDER BY day_number ASC")
    projects = cursor.fetchall()
    conn.close()
    return render_template('index.html', projects=projects)

@app.route('/script')
def script_page():
    return render_template('script.html')

@app.route('/api/projects')
def api_projects():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects_showcase_20 ORDER BY day_number ASC")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - Apresentação Especial DÍA 20 na porta 6911...")
    app.run(host='0.0.0.0', port=6911, debug=True)
