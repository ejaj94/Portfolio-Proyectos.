import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "uptime_pulse.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table Monitored URLs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_url TEXT NOT NULL,
            status TEXT DEFAULT 'Operational',
            last_status_code INTEGER DEFAULT 200,
            last_latency_ms INTEGER DEFAULT 45,
            uptime_percentage REAL DEFAULT 99.9,
            total_checks INTEGER DEFAULT 120,
            failed_checks INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table Check Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS check_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            url_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status_code INTEGER,
            latency_ms INTEGER,
            status_label TEXT
        )
    ''')

    # Table Alerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER,
            url_name TEXT,
            alert_type TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved INTEGER DEFAULT 1
        )
    ''')

    # Seed default monitored URLs if empty
    cursor.execute("SELECT COUNT(*) FROM monitored_urls")
    if cursor.fetchone()[0] == 0:
        default_monitors = [
            ("Website Oficial EJAJ TECH 🚀", "https://ejajtech.com", "Operational", 200, 38, 100.0, 350, 0),
            ("Showcase 80 Projetos em 80 Dias 💎", "http://localhost:6947", "Operational", 200, 14, 100.0, 280, 0),
            ("BioCraft AI Link-in-Bio SaaS 🔗", "http://localhost:6948", "Operational", 200, 18, 99.8, 240, 1),
            ("QRCraft AI QR Generator SaaS 📱", "http://localhost:6949", "Operational", 200, 22, 100.0, 190, 0),
            ("GitHub Public API Endpoint 🌐", "https://api.github.com", "Operational", 200, 85, 99.6, 500, 2)
        ]
        cursor.executemany('''
            INSERT INTO monitored_urls (name, target_url, status, last_status_code, last_latency_ms, uptime_percentage, total_checks, failed_checks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_monitors)

    # Seed default check logs if empty
    cursor.execute("SELECT COUNT(*) FROM check_logs")
    if cursor.fetchone()[0] == 0:
        sample_logs = [
            (1, "Website Oficial EJAJ TECH 🚀", "2026-09-15 20:55:10", 200, 38, "200 OK"),
            (2, "Showcase 80 Projetos em 80 Dias 💎", "2026-09-15 20:56:02", 200, 14, "200 OK"),
            (3, "BioCraft AI Link-in-Bio SaaS 🔗", "2026-09-15 20:57:15", 200, 18, "200 OK"),
            (4, "QRCraft AI QR Generator SaaS 📱", "2026-09-15 20:58:30", 200, 22, "200 OK"),
            (5, "GitHub Public API Endpoint 🌐", "2026-09-15 21:00:01", 200, 85, "200 OK")
        ]
        cursor.executemany('''
            INSERT INTO check_logs (url_id, url_name, timestamp, status_code, latency_ms, status_label)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_logs)

    # Seed default alerts if empty
    cursor.execute("SELECT COUNT(*) FROM alerts")
    if cursor.fetchone()[0] == 0:
        sample_alerts = [
            (3, "BioCraft AI Link-in-Bio SaaS 🔗", "Latência Elevada", "Latência temporária de 240ms detetada durante reinício de processo.", "2026-09-15 18:30:00", 1),
            (5, "GitHub Public API Endpoint 🌐", "Rate Limit Limitado", "Resposta de API excedeu limite de chamadas não autenticadas (429).", "2026-09-15 15:12:40", 1)
        ]
        cursor.executemany('''
            INSERT INTO alerts (url_id, url_name, alert_type, message, timestamp, resolved)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_alerts)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados uptime_pulse.db inicializado!")
