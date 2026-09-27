import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'member_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Members Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            tier TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            renewal_date TEXT NOT NULL,
            amount_paid REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Perks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tier_required TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            access_link TEXT NOT NULL
        )
    ''')

    # Payments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_name TEXT NOT NULL,
            member_email TEXT NOT NULL,
            tier TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM members')
    if cursor.fetchone()[0] == 0:
        seed_members = [
            ('Angel Rafael', 'admin@membercraft.ai', 'VIP Platinum', 'Active', '2026-10-15', 79.00),
            ('Bernardo Costa', 'bernardo@techvip.pt', 'Gold', 'Active', '2026-10-10', 39.00),
            ('Carolina Dias', 'carolina@design.io', 'Silver', 'Active', '2026-10-05', 19.00),
            ('Diogo Mendes', 'diogo@devs.pt', 'Bronze', 'Active', '2026-09-28', 9.00),
            ('Elena Viana', 'elena@startup.com', 'VIP Platinum', 'Active', '2026-10-22', 79.00)
        ]
        cursor.executemany('''
            INSERT INTO members (name, email, tier, status, renewal_date, amount_paid)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_members)

        seed_perks = [
            ('Bronze', 'Biblioteca de Código & Snippets', 'Acesso a mais de 100 templates e componentes de código prontos a utilizar.', 'fa-code', '#'),
            ('Silver', 'Masterclasses Semanais em HD', 'Acesso a transmissões ao vivo e gravações das aulas de engenharia de software.', 'fa-video', '#'),
            ('Gold', 'Canal VIP no Discord & Suporte', 'Comunidade privada com mentoria direta e resposta a dúvidas técnicas em menos de 2h.', 'fa-comments', '#'),
            ('VIP Platinum', 'Consultoria Individual 1-on-1', 'Sessão mensal privada para revisão de arquitetura de projetos e código.', 'fa-crown', '#')
        ]
        cursor.executemany('''
            INSERT INTO perks (tier_required, title, description, icon, access_link)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_perks)

        seed_payments = [
            ('Angel Rafael', 'admin@membercraft.ai', 'VIP Platinum', 79.00, 'Cartão de Crédito'),
            ('Bernardo Costa', 'bernardo@techvip.pt', 'Gold', 39.00, 'MB WAY'),
            ('Carolina Dias', 'carolina@design.io', 'Silver', 19.00, 'Multibanco'),
            ('Elena Viana', 'elena@startup.com', 'VIP Platinum', 79.00, 'PayPal')
        ]
        cursor.executemany('''
            INSERT INTO payments (member_name, member_email, tier, amount, payment_method)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_payments)

        conn.commit()
    conn.close()

def add_member(name, email, tier, amount_paid, payment_method):
    conn = get_db()
    cursor = conn.cursor()
    renewal_date = '2026-10-17'
    cursor.execute('''
        INSERT INTO members (name, email, tier, status, renewal_date, amount_paid)
        VALUES (?, ?, ?, 'Active', ?, ?)
    ''', (name, email, tier, renewal_date, amount_paid))
    member_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO payments (member_name, member_email, tier, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, tier, amount_paid, payment_method))

    conn.commit()
    conn.close()
    return member_id

def renew_member(member_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE members 
        SET status = 'Active', renewal_date = '2026-11-17'
        WHERE id = ?
    ''', (member_id,))
    conn.commit()
    conn.close()

def get_all_members():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_perks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM perks ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_payments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_membership_metrics():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM members WHERE status = 'Active'")
    active_members = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount_paid) FROM members WHERE status = 'Active'")
    total_revenue = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM members WHERE tier = 'VIP Platinum'")
    vip_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members WHERE tier = 'Gold'")
    gold_count = cursor.fetchone()[0]

    conn.close()
    return {
        "active_members": active_members,
        "total_revenue": round(total_revenue, 2),
        "vip_count": vip_count,
        "gold_count": gold_count,
        "renewal_rate": 96.5
    }

if __name__ == '__main__':
    init_db()
    print("Base de dados member_craft.db inicializada com sucesso!")
