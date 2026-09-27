import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "qr_craft.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table QR History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qr_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            qr_type TEXT NOT NULL,
            payload_data TEXT NOT NULL,
            fg_color TEXT DEFAULT '#0f172a',
            bg_color TEXT DEFAULT '#ffffff',
            logo_icon TEXT DEFAULT 'fa-solid fa-qrcode',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            downloads INTEGER DEFAULT 0
        )
    ''')

    # Table Presets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preset_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            fg_color TEXT NOT NULL,
            bg_color TEXT NOT NULL,
            pattern_style TEXT NOT NULL
        )
    ''')

    # Seed default history if empty
    cursor.execute("SELECT COUNT(*) FROM qr_history")
    if cursor.fetchone()[0] == 0:
        default_qrs = [
            ("Website EJAJ TECH 🚀", "URL", "https://ejajtech.com", "#1d4ed8", "#ffffff", "fa-solid fa-globe", "2026-09-15 19:10:00", 142),
            ("Wi-Fi Escritório VIP 📶", "WiFi", "WIFI:S:EJAJ_TECH_5G;T:WPA;P:EjajTech2026!;;", "#0f172a", "#e0f2fe", "fa-solid fa-wifi", "2026-09-15 19:30:15", 89),
            ("Contacto Enmanuel Jimenez 👤", "Contacto", "BEGIN:VCARD\nVERSION:3.0\nN:Jimenez;Enmanuel;;;\nFN:Enmanuel Jimenez\nORG:EJAJ TECH\nTEL:+351900000000\nEMAIL:enmanuel@ejajtech.com\nEND:VCARD", "#047857", "#ffffff", "fa-solid fa-address-card", "2026-09-15 20:05:40", 215),
            ("Showcase 80 Projetos 💎", "URL", "http://localhost:6947", "#38bdf8", "#0f172a", "fa-solid fa-gem", "2026-09-15 20:40:22", 310)
        ]
        cursor.executemany('''
            INSERT INTO qr_history (title, qr_type, payload_data, fg_color, bg_color, logo_icon, created_at, downloads)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_qrs)

    # Seed default templates if empty
    cursor.execute("SELECT COUNT(*) FROM preset_templates")
    if cursor.fetchone()[0] == 0:
        default_presets = [
            ("Cyber Blue", "#38bdf8", "#0f172a", "dots"),
            ("Luxury Gold", "#d97706", "#fffbeb", "squares"),
            ("Emerald Eco", "#059669", "#ecfdf5", "rounded"),
            ("Midnight Dark", "#f8fafc", "#020617", "dots")
        ]
        cursor.executemany('''
            INSERT INTO preset_templates (name, fg_color, bg_color, pattern_style)
            VALUES (?, ?, ?, ?)
        ''', default_presets)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados qr_craft.db inicializado!")
