import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'api_tester.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # History Table for executed API Requests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS request_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL, -- 'GET', 'POST', 'PUT', 'DELETE'
            url TEXT NOT NULL,
            headers_json TEXT,
            body_json TEXT,
            status_code INTEGER NOT NULL,
            status_text TEXT NOT NULL,
            response_time_ms INTEGER NOT NULL,
            response_size_kb REAL NOT NULL,
            response_body TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Seed sample history if empty
    cursor.execute('SELECT COUNT(*) FROM request_history')
    if cursor.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        samples = [
            ("GET", "https://jsonplaceholder.typicode.com/users", '{"Accept": "application/json"}', "", 200, "200 OK", 142, 5.8, '[{"id": 1, "name": "Leanne Graham", "email": "Sincere@april.biz", "address": {"city": "Gwenborough"}}]', now),
            ("POST", "https://jsonplaceholder.typicode.com/posts", '{"Content-Type": "application/json"}', '{"title": "Novo Post API", "body": "Conteúdo de teste via APITester AI", "userId": 1}', 201, "201 Created", 285, 0.4, '{"id": 101, "title": "Novo Post API", "body": "Conteúdo de teste via APITester AI", "userId": 1}', now),
            ("PUT", "https://jsonplaceholder.typicode.com/posts/1", '{"Content-Type": "application/json"}', '{"id": 1, "title": "Post Atualizado", "body": "Alterado com sucesso"}', 200, "200 OK", 190, 0.3, '{"id": 1, "title": "Post Atualizado", "body": "Alterado com sucesso"}', now),
            ("DELETE", "https://jsonplaceholder.typicode.com/posts/1", '{"Authorization": "Bearer sk_test_99218a"}', "", 200, "200 OK", 115, 0.1, '{}', now)
        ]

        cursor.executemany('''
            INSERT INTO request_history (method, url, headers_json, body_json, status_code, status_text, response_time_ms, response_size_kb, response_body, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', samples)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados APITester inicializada com sucesso!")
