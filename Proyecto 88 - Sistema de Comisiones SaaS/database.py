import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'comision_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: Salespeople (Vendedores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salespeople (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            role TEXT DEFAULT 'Consultor Comercial',
            tier_level TEXT DEFAULT 'Junior',
            base_salary REAL DEFAULT 1000.0,
            monthly_target REAL DEFAULT 10000.0,
            default_commission_rate REAL DEFAULT 5.0,
            created_at TEXT NOT NULL
        )
    ''')

    # Table: Sales (Ventas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            salesperson_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            product_category TEXT NOT NULL,
            amount REAL NOT NULL,
            commission_rate REAL NOT NULL,
            commission_amount REAL NOT NULL,
            status TEXT DEFAULT 'Concluída',
            period_name TEXT NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (salesperson_id) REFERENCES salespeople (id)
        )
    ''')

    # Table: Commission Rules / Escalões de Porcentagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commission_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT NOT NULL,
            min_amount REAL NOT NULL,
            max_amount REAL NOT NULL,
            commission_rate REAL NOT NULL,
            bonus_amount REAL DEFAULT 0.0,
            description TEXT
        )
    ''')

    # Seed salespeople if empty
    cursor.execute('SELECT COUNT(*) FROM salespeople')
    if cursor.fetchone()[0] == 0:
        seed_salespeople = [
            ('Ana Sofia Martins', 'ana.martins@ejajtech.pt', '+351 912 345 678', 'Senior Account Executive', 'Senior', 1600.0, 25000.0, 8.5, '2026-09-01 09:00'),
            ('Diogo Alexandre Silva', 'diogo.silva@ejajtech.pt', '+351 923 456 789', 'Consultor de Vendas SaaS', 'Pleno', 1250.0, 18000.0, 6.5, '2026-09-01 09:30'),
            ('Beatriz Carmo Ribeiro', 'beatriz.ribeiro@ejajtech.pt', '+351 934 567 890', 'Business Development Rep', 'Junior', 1000.0, 12000.0, 5.0, '2026-09-02 10:15'),
            ('Gonçalo Nuno Ferreira', 'goncalo.ferreira@ejajtech.pt', '+351 965 678 901', 'Key Account Manager', 'Senior', 1800.0, 30000.0, 10.0, '2026-09-03 11:00')
        ]

        cursor.executemany('''
            INSERT INTO salespeople (name, email, phone, role, tier_level, base_salary, monthly_target, default_commission_rate, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_salespeople)

    # Seed commission rules if empty
    cursor.execute('SELECT COUNT(*) FROM commission_rules')
    if cursor.fetchone()[0] == 0:
        seed_rules = [
            ('Escalão Base (Vendas até 5k€)', 0.0, 5000.0, 5.0, 0.0, 'Taxa normal para vendas de baixo volume'),
            ('Escalão Intermédio (5k€ a 15k€)', 5000.01, 15000.0, 7.5, 150.0, 'Comissão acrescida com bónus de 150€'),
            ('Escalão Premium (> 15k€)', 15000.01, 999999.0, 10.0, 500.0, 'Comissão máxima de 10% com bónus de superação')
        ]

        cursor.executemany('''
            INSERT INTO commission_rules (rule_name, min_amount, max_amount, commission_rate, bonus_amount, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_rules)

    # Seed sales if empty
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        seed_sales = [
            (1, 'Empresa Global Tech Lda', 'Software SaaS', 18500.0, 10.0, 1850.0, 'Concluída', 'Setembro 2026', '2026-09-05'),
            (1, 'Grupo Hoteleiro do Norte', 'Licenciamento Enterprise', 9500.0, 7.5, 712.5, 'Concluída', 'Setembro 2026', '2026-09-07'),
            (2, 'Clínica Médica Central', 'Plano Cloud Anual', 6200.0, 7.5, 465.0, 'Concluída', 'Setembro 2026', '2026-09-08'),
            (2, 'Escola Profissional Alfa', 'Serviços de Suporte', 3800.0, 5.0, 190.0, 'Concluída', 'Setembro 2026', '2026-09-09'),
            (3, 'Oficina Mecânica Rapidez', 'Módulo de Faturação', 2500.0, 5.0, 125.0, 'Concluída', 'Setembro 2026', '2026-09-10'),
            (4, 'Logística & Transportes Ibérica', 'Contrato Integrado ERP', 28000.0, 10.0, 2800.0, 'Concluída', 'Setembro 2026', '2026-09-12')
        ]

        cursor.executemany('''
            INSERT INTO sales (salesperson_id, client_name, product_category, amount, commission_rate, commission_amount, status, period_name, sale_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_sales)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados comision_craft.db inicializada com sucesso!")
