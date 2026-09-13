import sqlite3
import os
import datetime
import random

DB_PATH = os.path.join(os.path.dirname(__file__), 'analytics_saas.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Daily Traffic Metrics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_traffic (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_str TEXT UNIQUE NOT NULL,
            visits INTEGER NOT NULL,
            unique_visitors INTEGER NOT NULL,
            pageviews INTEGER NOT NULL,
            bounce_rate REAL NOT NULL,
            avg_duration_sec INTEGER NOT NULL
        )
    ''')

    # Top Pages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS top_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT UNIQUE NOT NULL,
            page_title TEXT NOT NULL,
            pageviews INTEGER NOT NULL,
            unique_views INTEGER NOT NULL,
            avg_time_sec INTEGER NOT NULL,
            exit_rate REAL NOT NULL
        )
    ''')

    # Geographic Countries Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS country_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code TEXT UNIQUE NOT NULL,
            country_name TEXT NOT NULL,
            flag_emoji TEXT NOT NULL,
            visitors_count INTEGER NOT NULL,
            traffic_share_pct REAL NOT NULL
        )
    ''')

    # Device & OS Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL, -- 'Device', 'OS', 'Browser'
            name TEXT NOT NULL,
            share_pct REAL NOT NULL,
            users_count INTEGER NOT NULL
        )
    ''')

    # Traffic Sources Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS traffic_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name TEXT NOT NULL, -- Direct, Google Search, Organic Social, Email, Referral
            referrer_domain TEXT,
            visits INTEGER NOT NULL,
            conversion_rate REAL NOT NULL
        )
    ''')

    # Seed initial mock data if empty
    cursor.execute('SELECT COUNT(*) FROM daily_traffic')
    if cursor.fetchone()[0] == 0:
        # Seed 14 days of traffic
        base_date = datetime.datetime.now() - datetime.timedelta(days=13)
        daily_entries = []
        for i in range(14):
            day_dt = base_date + datetime.timedelta(days=i)
            day_str = day_dt.strftime("%Y-%m-%d")
            v = random.randint(1200, 3400)
            u = int(v * random.uniform(0.72, 0.85))
            pv = int(v * random.uniform(1.8, 3.2))
            br = round(random.uniform(32.5, 46.8), 1)
            dur = random.randint(110, 240)
            daily_entries.append((day_str, v, u, pv, br, dur))

        cursor.executemany('''
            INSERT INTO daily_traffic (date_str, visits, unique_visitors, pageviews, bounce_rate, avg_duration_sec)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', daily_entries)

        # Seed Top Pages
        pages_seed = [
            ('/home', 'Página Principal — SaaS Platform', 14850, 11200, 185, 28.4),
            ('/pricing', 'Planos & Preços Enterprise', 9420, 7850, 240, 34.2),
            ('/blog/futuro-da-ia', 'Artigo: O Futuro da IA em 2026', 6230, 5400, 310, 42.1),
            ('/features/analytics', 'Funcionalidades & Relatórios', 4890, 4100, 195, 31.8),
            ('/docs/api-guide', 'Documentação da API RESTful', 3750, 2900, 420, 22.5),
            ('/signup', 'Registo & Teste Gratuito', 2980, 2750, 135, 18.2)
        ]
        cursor.executemany('''
            INSERT INTO top_pages (page_path, page_title, pageviews, unique_views, avg_time_sec, exit_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', pages_seed)

        # Seed Countries
        countries_seed = [
            ('PT', 'Portugal', '🇵🇹', 12450, 38.5),
            ('BR', 'Brasil', '🇧🇷', 7890, 24.3),
            ('ES', 'Espanha', '🇪🇸', 4120, 12.7),
            ('US', 'Estados Unidos', '🇺🇸', 3540, 10.9),
            ('UK', 'Reino Unido', '🇬🇧', 2180, 6.7),
            ('FR', 'França', '🇫🇷', 1210, 3.7),
            ('AO', 'Angola', '🇦🇴', 1040, 3.2)
        ]
        cursor.executemany('''
            INSERT INTO country_analytics (country_code, country_name, flag_emoji, visitors_count, traffic_share_pct)
            VALUES (?, ?, ?, ?, ?)
        ''', countries_seed)

        # Seed Devices & OS & Browsers
        device_seed = [
            ('Device', 'Computador (Desktop)', 58.4, 18950),
            ('Device', 'Telemóvel (Mobile)', 36.2, 11750),
            ('Device', 'Tablet', 5.4, 1750),
            ('OS', 'Windows', 44.5, 14450),
            ('OS', 'macOS', 26.8, 8700),
            ('OS', 'iOS', 16.2, 5260),
            ('OS', 'Android', 12.5, 4060),
            ('Browser', 'Google Chrome', 62.4, 20250),
            ('Browser', 'Apple Safari', 21.8, 7080),
            ('Browser', 'Mozilla Firefox', 9.5, 3080),
            ('Browser', 'Microsoft Edge', 6.3, 2040)
        ]
        cursor.executemany('''
            INSERT INTO device_analytics (category, name, share_pct, users_count)
            VALUES (?, ?, ?, ?)
        ''', device_seed)

        # Seed Traffic Sources
        sources_seed = [
            ('Pesquisa Orgânica', 'google.com', 13450, 4.8),
            ('Tráfego Direto', 'direto', 9820, 6.2),
            ('Redes Sociais', 'linkedin.com / instagram', 5240, 3.9),
            ('E-mail Marketing', 'mailcraft / newsletter', 3150, 8.4),
            ('Links de Referência', 'techcrunch / medium', 1840, 5.1)
        ]
        cursor.executemany('''
            INSERT INTO traffic_sources (channel_name, referrer_domain, visits, conversion_rate)
            VALUES (?, ?, ?, ?)
        ''', sources_seed)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados analytics_saas.db inicializada com sucesso!")
