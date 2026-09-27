import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "key_craft.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table Generation History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_mask TEXT NOT NULL,
            length INTEGER NOT NULL,
            entropy_bits REAL NOT NULL,
            strength_label TEXT NOT NULL,
            crack_time_est TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed default history if empty
    cursor.execute("SELECT COUNT(*) FROM generation_history")
    if cursor.fetchone()[0] == 0:
        default_logs = [
            ("K#92*xPz!8mL@2026", 18, 118.2, "Impenetrável", "8.4 Triliões de Anos", "2026-09-16 19:10:00"),
            ("EjajTech#2026!Secured", 21, 137.9, "Impenetrável", "520 Triliões de Anos", "2026-09-16 19:15:30"),
            ("A8#bC9!dE2", 10, 65.5, "Forte", "12 Dias", "2026-09-16 19:20:12")
        ]
        cursor.executemany('''
            INSERT INTO generation_history (password_mask, length, entropy_bits, strength_label, crack_time_est, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_logs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados key_craft.db inicializado!")
