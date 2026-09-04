import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'shortener.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla Links
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            original_url TEXT NOT NULL,
            custom_alias TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_clicks INTEGER DEFAULT 0,
            qr_code_url TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Tabla Historial Telemétrico de Clicks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clicks_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link_id INTEGER NOT NULL,
            ip_address TEXT,
            country_code TEXT NOT NULL,
            country_name TEXT NOT NULL,
            city TEXT,
            device_type TEXT NOT NULL,
            os_name TEXT NOT NULL,
            browser_name TEXT NOT NULL,
            referrer TEXT,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (link_id) REFERENCES links(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    seed_initial_data()

def seed_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM links')
    if cursor.fetchone()[0] == 0:
        now = datetime.now()

        # Seed Links
        sample_links = [
            (
                'veloce-suite',
                'VELOCE WORKSHOP Suite - Sistema de Gestão Telemétrica Supercars',
                'https://ejajtech.com/veloce-workshop-suite-telemetria-oficina',
                'veloce-suite',
                (now - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
                142,
                'https://api.quickchart.io/qr?text=http://127.0.0.1:6050/veloce-suite&size=250',
                1
            ),
            (
                'sabonetes-a4',
                'Sabonetes Artesanais - Folha de Etiquetas A4 Impressão',
                'https://ejajtech.com/downloads/sabonetes_etiquetas_nombres_a4.pdf',
                'sabonetes-a4',
                (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
                98,
                'https://api.quickchart.io/qr?text=http://127.0.0.1:6050/sabonetes-a4&size=250',
                1
            ),
            (
                'helpdesk-saas',
                'RESOLV-IT SaaS - Sistema de Tickets & Suporte Técnico EJAJ TECH',
                'http://127.0.0.1:5980/',
                'helpdesk-saas',
                (now - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
                215,
                'https://api.quickchart.io/qr?text=http://127.0.0.1:6050/helpdesk-saas&size=250',
                1
            ),
            (
                'chat-messenger',
                'CONNECT-CHAT SaaS - Plataforma de Mensagens Facebook Messenger Blue',
                'http://127.0.0.1:5990/',
                'chat-messenger',
                (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                87,
                'https://api.quickchart.io/qr?text=http://127.0.0.1:6050/chat-messenger&size=250',
                1
            )
        ]

        cursor.executemany('''
            INSERT INTO links (short_code, title, original_url, custom_alias, created_at, total_clicks, qr_code_url, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_links)

        # Seed Clicks Telemétricos para Link #1 (veloce-suite)
        countries = [
            ('PT', 'Portugal', 'Lisboa'),
            ('PT', 'Portugal', 'Porto'),
            ('PT', 'Portugal', 'Faro'),
            ('ES', 'Espanha', 'Madrid'),
            ('ES', 'Espanha', 'Barcelona'),
            ('FR', 'França', 'Paris'),
            ('US', 'Estados Unidos', 'New York'),
            ('BR', 'Brasil', 'São Paulo'),
            ('DE', 'Alemanha', 'Berlim'),
            ('GB', 'Reino Unido', 'Londres')
        ]
        
        devices = ['Desktop', 'Mobile', 'Tablet']
        os_list = ['Windows', 'macOS', 'iOS', 'Android', 'Linux']
        browsers = ['Chrome', 'Safari', 'Firefox', 'Edge']
        referrers = ['Instagram (@ejajtech)', 'Direct / WhatsApp', 'LinkedIn', 'Google Search', 'Facebook']

        clicks_data = []
        for i in range(120):
            cnt = random.choice(countries)
            dev = random.choice(devices)
            os_name = 'iOS' if dev == 'Mobile' and random.random() > 0.5 else ('Android' if dev == 'Mobile' else random.choice(['Windows', 'macOS', 'Linux']))
            browser = 'Safari' if os_name in ['iOS', 'macOS'] else random.choice(['Chrome', 'Firefox', 'Edge'])
            ref = random.choice(referrers)
            click_time = (now - timedelta(hours=random.randint(1, 72))).strftime('%Y-%m-%d %H:%M:%S')

            clicks_data.append((
                1, # veloce-suite
                f"185.210.{random.randint(1, 255)}.{random.randint(1, 255)}",
                cnt[0],
                cnt[1],
                cnt[2],
                dev,
                os_name,
                browser,
                ref,
                click_time
            ))

        # Seed Clicks para Link #3 (helpdesk-saas)
        for i in range(90):
            cnt = random.choice(countries[:5]) # Principalmente Portugal e Espanha
            dev = random.choice(devices)
            os_name = random.choice(os_list)
            browser = random.choice(browsers)
            ref = random.choice(referrers)
            click_time = (now - timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S')

            clicks_data.append((
                3, # helpdesk-saas
                f"193.136.{random.randint(1, 255)}.{random.randint(1, 255)}",
                cnt[0],
                cnt[1],
                cnt[2],
                dev,
                os_name,
                browser,
                ref,
                click_time
            ))

        cursor.executemany('''
            INSERT INTO clicks_log (link_id, ip_address, country_code, country_name, city, device_type, os_name, browser_name, referrer, clicked_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', clicks_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("[OK] Base de datos shortener.db inicializada con exito para Proyecto 37.")
