import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'sub_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Subscriptions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL,
            plan_name TEXT NOT NULL,
            billing_cycle TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'Active',
            next_billing_date TEXT NOT NULL,
            cancellation_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Invoices Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL,
            plan_name TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'Paid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM subscriptions')
    if cursor.fetchone()[0] == 0:
        seed_subscriptions = [
            ('Angel Rafael', 'admin@subcraft.ai', 'Pro Plan', 'Mensal', 29.00, 'Active', '2026-10-15', None),
            ('Carlos Silva', 'carlos@empresa.pt', 'Enterprise Plan', 'Anual', 290.00, 'Active', '2027-09-01', None),
            ('Maria Santos', 'maria@techlabs.io', 'Starter Plan', 'Mensal', 12.00, 'Active', '2026-10-02', None),
            ('Pedro Ramos', 'pedro@marketing.com', 'Pro Plan', 'Mensal', 29.00, 'Canceled', '2026-09-10', 'Preço elevado'),
            ('Ana Ferreira', 'ana@designstudio.pt', 'Enterprise Plan', 'Mensal', 49.00, 'Active', '2026-10-20', None)
        ]
        cursor.executemany('''
            INSERT INTO subscriptions (user_name, user_email, plan_name, billing_cycle, amount, status, next_billing_date, cancellation_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_subscriptions)
        
        seed_invoices = [
            ('INV-2026-001', 'Angel Rafael', 'admin@subcraft.ai', 'Pro Plan', 29.00, 'Cartão de Crédito', 'Paid'),
            ('INV-2026-002', 'Carlos Silva', 'carlos@empresa.pt', 'Enterprise Plan', 290.00, 'MB WAY', 'Paid'),
            ('INV-2026-003', 'Maria Santos', 'maria@techlabs.io', 'Starter Plan', 12.00, 'Multibanco', 'Paid'),
            ('INV-2026-004', 'Pedro Ramos', 'pedro@marketing.com', 'Pro Plan', 29.00, 'Cartão de Crédito', 'Paid'),
            ('INV-2026-005', 'Ana Ferreira', 'ana@designstudio.pt', 'Enterprise Plan', 49.00, 'PayPal', 'Paid')
        ]
        cursor.executemany('''
            INSERT INTO invoices (invoice_number, user_name, user_email, plan_name, amount, payment_method, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_invoices)
        
        conn.commit()
    conn.close()

def add_subscription(user_name, user_email, plan_name, billing_cycle, amount, payment_method):
    conn = get_db()
    cursor = conn.cursor()
    
    next_date = "2026-10-17" if billing_cycle == 'Mensal' else "2027-09-17"
    
    cursor.execute('''
        INSERT INTO subscriptions (user_name, user_email, plan_name, billing_cycle, amount, status, next_billing_date)
        VALUES (?, ?, ?, ?, ?, 'Active', ?)
    ''', (user_name, user_email, plan_name, billing_cycle, amount, next_date))
    sub_id = cursor.lastrowid
    
    inv_num = f"INV-2026-00{sub_id + 5}"
    cursor.execute('''
        INSERT INTO invoices (invoice_number, user_name, user_email, plan_name, amount, payment_method, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Paid')
    ''', (inv_num, user_name, user_email, plan_name, amount, payment_method))
    
    conn.commit()
    conn.close()
    return sub_id

def cancel_subscription(sub_id, reason):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE subscriptions 
        SET status = 'Canceled', cancellation_reason = ?
        WHERE id = ?
    ''', (reason, sub_id))
    conn.commit()
    conn.close()

def get_all_subscriptions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM subscriptions ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_invoices():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoices ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_saas_metrics():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM subscriptions WHERE status = 'Active' AND billing_cycle = 'Mensal'")
    mrr_monthly = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT SUM(amount) FROM subscriptions WHERE status = 'Active' AND billing_cycle = 'Anual'")
    mrr_yearly = (cursor.fetchone()[0] or 0.0) / 12.0
    
    mrr_total = round(mrr_monthly + mrr_yearly, 2)
    arr_total = round(mrr_total * 12.0, 2)
    
    cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE status = 'Active'")
    active_subs = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE status = 'Canceled'")
    canceled_subs = cursor.fetchone()[0]
    
    total_subs = active_subs + canceled_subs
    churn_rate = round((canceled_subs / total_subs) * 100, 1) if total_subs > 0 else 0.0
    
    conn.close()
    return {
        "mrr": mrr_total,
        "arr": arr_total,
        "active_subscribers": active_subs,
        "canceled_subscribers": canceled_subs,
        "churn_rate": churn_rate
    }

if __name__ == '__main__':
    init_db()
    print("Base de dados sub_craft.db inicializada com sucesso!")
