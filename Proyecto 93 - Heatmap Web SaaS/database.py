import sqlite3
import os
import datetime
import random

DB_PATH = os.path.join(os.path.dirname(__file__), 'heatmap_saas.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Monitored Pages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT UNIQUE NOT NULL,
            page_title TEXT NOT NULL,
            total_clicks INTEGER DEFAULT 0,
            avg_scroll_pct REAL DEFAULT 0.0,
            total_sessions INTEGER DEFAULT 0,
            hotspot_score INTEGER DEFAULT 0
        )
    ''')

    # Click Heatmaps Coordinates Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS click_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT NOT NULL,
            pos_x_pct REAL NOT NULL, -- 0 to 100% relative X position
            pos_y_px INTEGER NOT NULL, -- Y position in pixels
            target_element TEXT NOT NULL, -- e.g., 'btn-cta-primary', 'nav-pricing', 'hero-headline'
            device_type TEXT NOT NULL, -- Desktop, Mobile, Tablet
            timestamp TEXT NOT NULL
        )
    ''')

    # Scroll Depth Metrics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scroll_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT NOT NULL,
            depth_25_pct REAL NOT NULL,
            depth_50_pct REAL NOT NULL,
            depth_75_pct REAL NOT NULL,
            depth_100_pct REAL NOT NULL,
            avg_scroll_depth REAL NOT NULL
        )
    ''')

    # User Sessions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_code TEXT UNIQUE NOT NULL,
            user_ip TEXT NOT NULL,
            device TEXT NOT NULL,
            browser TEXT NOT NULL,
            clicks_count INTEGER NOT NULL,
            max_scroll_pct REAL NOT NULL,
            duration_sec INTEGER NOT NULL,
            recorded_at TEXT NOT NULL
        )
    ''')

    # Seed initial mock data if empty
    cursor.execute('SELECT COUNT(*) FROM monitored_pages')
    if cursor.fetchone()[0] == 0:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        past_str = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M")

        # Seed Pages
        pages_seed = [
            ('/landing-page', 'Landing Page Principal de Vendas', 18450, 78.4, 6200, 94),
            ('/pricing-table', 'Tabela de Preços & Planos Enterprise', 12380, 84.2, 4500, 89),
            ('/checkout-flow', 'Checkout & Pagamento Seguro', 8920, 92.1, 3100, 96),
            ('/features-demo', 'Demonstração de Funcionalidades', 6450, 65.0, 2400, 78),
            ('/blog/growth-hacks', 'Artigo: Growth Hacks para SaaS', 4120, 58.6, 1800, 65)
        ]
        cursor.executemany('''
            INSERT INTO monitored_pages (page_path, page_title, total_clicks, avg_scroll_pct, total_sessions, hotspot_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', pages_seed)

        # Seed Click Events (Hotspots coordinates)
        elements = [
            ('btn-cta-primary', 48.5, 340),
            ('nav-pricing', 72.0, 45),
            ('hero-headline', 35.0, 180),
            ('btn-start-free', 50.0, 420),
            ('feature-card-1', 25.0, 680),
            ('feature-card-2', 75.0, 690),
            ('pricing-plan-pro', 65.0, 920),
            ('footer-terms', 15.0, 1450)
        ]

        clicks_seed = []
        for i in range(120):
            elem, base_x, base_y = random.choice(elements)
            offset_x = random.uniform(-8.0, 8.0)
            offset_y = random.randint(-25, 25)
            x_pct = min(max(base_x + offset_x, 5.0), 95.0)
            y_px = max(base_y + offset_y, 20)
            dev = random.choice(['Desktop', 'Desktop', 'Mobile', 'Tablet'])
            clicks_seed.append(('/landing-page', round(x_pct, 1), y_px, elem, dev, now_str))

        cursor.executemany('''
            INSERT INTO click_events (page_path, pos_x_pct, pos_y_px, target_element, device_type, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', clicks_seed)

        # Seed Scroll Metrics
        scroll_seed = [
            ('/landing-page', 98.5, 82.4, 64.1, 41.2, 78.4),
            ('/pricing-table', 99.1, 88.0, 72.5, 52.8, 84.2),
            ('/checkout-flow', 100.0, 95.2, 89.4, 78.0, 92.1),
            ('/features-demo', 94.2, 71.0, 48.5, 28.1, 65.0),
            ('/blog/growth-hacks', 92.0, 64.5, 42.0, 22.4, 58.6)
        ]
        cursor.executemany('''
            INSERT INTO scroll_metrics (page_path, depth_25_pct, depth_50_pct, depth_75_pct, depth_100_pct, avg_scroll_depth)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', scroll_seed)

        # Seed User Sessions
        sessions_seed = [
            ('SESS-9081', '185.22.45.12', 'Desktop', 'Google Chrome', 24, 95.0, 210, now_str),
            ('SESS-9082', '192.168.1.45', 'Mobile', 'Apple Safari', 14, 82.0, 145, now_str),
            ('SESS-9083', '84.23.11.90', 'Desktop', 'Mozilla Firefox', 32, 100.0, 310, past_str),
            ('SESS-9084', '201.54.89.2', 'Tablet', 'Apple Safari', 8, 65.0, 98, past_str),
            ('SESS-9085', '178.12.90.4', 'Desktop', 'Microsoft Edge', 19, 88.5, 180, past_str)
        ]
        cursor.executemany('''
            INSERT INTO user_sessions (session_code, user_ip, device, browser, clicks_count, max_scroll_pct, duration_sec, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sessions_seed)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados heatmap_saas.db inicializada com sucesso!")
