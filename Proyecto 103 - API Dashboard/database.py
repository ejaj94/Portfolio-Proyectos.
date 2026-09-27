import sqlite3
import os
import secrets
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'api_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # API Keys Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            key_token TEXT UNIQUE NOT NULL,
            environment TEXT NOT NULL, -- 'Production', 'Staging', 'Development'
            permission_scope TEXT NOT NULL, -- 'Read-only', 'Read-Write', 'Admin'
            rate_limit_per_min INTEGER NOT NULL DEFAULT 1000,
            status TEXT NOT NULL DEFAULT 'Ativa', -- 'Ativa', 'Revogada'
            created_at TEXT NOT NULL
        )
    ''')

    # API Requests Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_id INTEGER NOT NULL,
            endpoint TEXT NOT NULL,
            http_method TEXT NOT NULL, -- 'GET', 'POST', 'PUT', 'DELETE'
            status_code INTEGER NOT NULL, -- 200, 201, 400, 401, 429, 500
            latency_ms INTEGER NOT NULL,
            payload_size_kb REAL NOT NULL,
            ip_address TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(key_id) REFERENCES api_keys(id)
        )
    ''')

    # API Errors Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            error_message TEXT NOT NULL,
            client_ip TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM api_keys')
    if cursor.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Seed Keys
        keys = [
            ("Mobile App Production", "apicraft_live_" + secrets.token_hex(16), "Production", "Read-Write", 2500, "Ativa", now),
            ("Web Dashboard Admin", "apicraft_live_" + secrets.token_hex(16), "Production", "Admin", 5000, "Ativa", now),
            ("Staging Testing Integration", "apicraft_test_" + secrets.token_hex(16), "Staging", "Read-Write", 1000, "Ativa", now),
            ("Legacy Partner API Key", "apicraft_live_" + secrets.token_hex(16), "Production", "Read-only", 500, "Revogada", now)
        ]
        cursor.executemany('''
            INSERT INTO api_keys (name, key_token, environment, permission_scope, rate_limit_per_min, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', keys)

        # Seed Requests
        sample_requests = [
            (1, "/v1/users", "GET", 200, 45, 1.2, "193.168.1.10", "2026-09-16 20:00:15"),
            (1, "/v1/auth/login", "POST", 200, 120, 0.8, "193.168.1.10", "2026-09-16 20:01:02"),
            (2, "/v1/payments/charge", "POST", 201, 310, 2.5, "188.82.12.99", "2026-09-16 20:02:40"),
            (3, "/v1/webhooks/dispatch", "POST", 500, 850, 4.1, "195.23.110.4", "2026-09-16 20:04:10"),
            (1, "/v1/data/export", "GET", 429, 15, 0.2, "85.240.12.5", "2026-09-16 20:05:00"),
            (2, "/v1/users/profile", "GET", 200, 38, 1.1, "193.168.1.10", "2026-09-16 20:06:22"),
            (3, "/v1/reports/monthly", "GET", 401, 22, 0.3, "195.23.110.4", "2026-09-16 20:07:45")
        ]
        cursor.executemany('''
            INSERT INTO api_requests (key_id, endpoint, http_method, status_code, latency_ms, payload_size_kb, ip_address, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_requests)

        # Seed Errors
        sample_errors = [
            ("/v1/webhooks/dispatch", 500, "Internal Server Error: Connection timeout to payment gateway microservice.", "195.23.110.4", "2026-09-16 20:04:10"),
            ("/v1/data/export", 429, "Rate Limit Exceeded: Client exceeded maximum quota of 1000 requests per minute.", "85.240.12.5", "2026-09-16 20:05:00"),
            ("/v1/reports/monthly", 401, "Unauthorized: Invalid OAuth Bearer token or token expired.", "195.23.110.4", "2026-09-16 20:07:45")
        ]
        cursor.executemany('''
            INSERT INTO api_errors (endpoint, status_code, error_message, client_ip, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_errors)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados APICraft inicializada com sucesso!")
