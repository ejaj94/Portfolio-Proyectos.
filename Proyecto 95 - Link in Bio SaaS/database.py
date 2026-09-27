import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bio_craft.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table Profile
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY DEFAULT 1,
            name TEXT NOT NULL,
            handle TEXT NOT NULL,
            bio TEXT,
            avatar_url TEXT,
            location TEXT,
            verified INTEGER DEFAULT 1
        )
    ''')

    # Table Links
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            icon TEXT DEFAULT 'fa-solid fa-link',
            badge TEXT,
            clicks INTEGER DEFAULT 0,
            highlight INTEGER DEFAULT 0,
            position INTEGER DEFAULT 0
        )
    ''')

    # Table Social Media
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS social_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            icon TEXT NOT NULL,
            active INTEGER DEFAULT 1
        )
    ''')

    # Table Clicks Log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clicks_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_id INTEGER,
            link_title TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_simulated TEXT,
            device TEXT,
            location TEXT
        )
    ''')

    # Table Theme Config
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS theme_config (
            id INTEGER PRIMARY KEY DEFAULT 1,
            theme_name TEXT DEFAULT 'cyber-glass',
            bg_style TEXT DEFAULT 'animated-gradient',
            button_style TEXT DEFAULT 'pill-glass',
            font_family TEXT DEFAULT 'Plus Jakarta Sans',
            accent_color TEXT DEFAULT '#38bdf8'
        )
    ''')

    # Seed default profile if empty
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (id, name, handle, bio, avatar_url, location, verified)
            VALUES (1, 'Enmanuel Jimenez', '@ejajtech', 'Lead Architect & Founder na EJAJ TECH. A reinventar a arquitetura de software moderno e soluções de IA.', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80', 'Lisboa, Portugal', 1)
        ''')

    # Seed default links if empty
    cursor.execute("SELECT COUNT(*) FROM links")
    if cursor.fetchone()[0] == 0:
        default_links = [
            ("Portefólio Oficial EJAJ TECH 🚀", "https://ejajtech.com", "fa-solid fa-globe", "NOVO", 342, 1, 1),
            ("Agendar Consultoria de IA & Software 📅", "https://ejajtech.com/agendar", "fa-solid fa-calendar-check", "VIP", 189, 0, 2),
            ("Showcase 80 Projetos em 80 Dias 💎", "http://localhost:6947", "fa-solid fa-gem", "DESTAQUE", 512, 1, 3),
            ("GitHub Repositórios & Código Aberto 💻", "https://github.com/ejajtech", "fa-brands fa-github", "", 128, 0, 4),
            ("Canal Oficial Telegram & Comunitário 📱", "https://t.me/ejajtech", "fa-paper-plane", "COMUNIDADE", 95, 0, 5)
        ]
        cursor.executemany('''
            INSERT INTO links (title, url, icon, badge, clicks, highlight, position)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', default_links)

    # Seed default social links if empty
    cursor.execute("SELECT COUNT(*) FROM social_links")
    if cursor.fetchone()[0] == 0:
        default_socials = [
            ("Instagram", "https://instagram.com/ejajtech", "fa-brands fa-instagram", 1),
            ("LinkedIn", "https://linkedin.com/in/ejajtech", "fa-brands fa-linkedin-in", 1),
            ("YouTube", "https://youtube.com/@ejajtech", "fa-brands fa-youtube", 1),
            ("X / Twitter", "https://x.com/ejajtech", "fa-brands fa-x-twitter", 1),
            ("WhatsApp", "https://wa.me/351900000000", "fa-brands fa-whatsapp", 1)
        ]
        cursor.executemany('''
            INSERT INTO social_links (platform, url, icon, active)
            VALUES (?, ?, ?, ?)
        ''', default_socials)

    # Seed theme if empty
    cursor.execute("SELECT COUNT(*) FROM theme_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO theme_config (id, theme_name, bg_style, button_style, font_family, accent_color)
            VALUES (1, 'cyber-glass', 'animated-gradient', 'pill-glass', 'Plus Jakarta Sans', '#38bdf8')
        ''')

    # Seed sample clicks log if empty
    cursor.execute("SELECT COUNT(*) FROM clicks_log")
    if cursor.fetchone()[0] == 0:
        sample_logs = [
            (3, "Showcase 80 Projetos em 80 Dias 💎", "2026-09-15 18:20:11", "193.168.1.45", "Mobile (iPhone 15)", "Lisboa, Portugal"),
            (1, "Portefólio Oficial EJAJ TECH 🚀", "2026-09-15 18:45:00", "188.82.10.12", "Desktop (Chrome / Windows)", "Porto, Portugal"),
            (2, "Agendar Consultoria de IA & Software 📅", "2026-09-15 19:10:33", "85.240.55.99", "Mobile (Samsung Galaxy)", "Faro, Portugal"),
            (3, "Showcase 80 Projetos em 80 Dias 💎", "2026-09-15 19:35:12", "195.23.112.5", "Desktop (MacBook Pro)", "Madrid, Espanha"),
            (4, "GitHub Repositórios & Código Aberto 💻", "2026-09-15 20:02:44", "213.13.40.80", "Mobile (Android)", "Coimbra, Portugal")
        ]
        cursor.executemany('''
            INSERT INTO clicks_log (link_id, link_title, timestamp, ip_simulated, device, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_logs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados bio_craft.db inicializado com sucesso!")
