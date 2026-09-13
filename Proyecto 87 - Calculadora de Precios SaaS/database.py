import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'price_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: Products / Services catalog
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT DEFAULT 'Unidade',
            base_cost REAL DEFAULT 0.0,
            labor_cost REAL DEFAULT 0.0,
            overhead_cost REAL DEFAULT 0.0,
            total_cost REAL DEFAULT 0.0,
            target_margin_percent REAL DEFAULT 30.0,
            created_at TEXT NOT NULL
        )
    ''')

    # Table: Price calculations / Simulations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            title TEXT NOT NULL,
            base_cost REAL NOT NULL,
            labor_cost REAL NOT NULL,
            overhead_cost REAL NOT NULL,
            total_cost REAL NOT NULL,
            markup_percent REAL NOT NULL,
            gross_profit REAL NOT NULL,
            margin_percent REAL NOT NULL,
            discount_percent REAL DEFAULT 0.0,
            price_before_tax REAL NOT NULL,
            vat_rate REAL DEFAULT 23.0,
            vat_amount REAL NOT NULL,
            final_price REAL NOT NULL,
            net_profit REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Seed initial product catalog if empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        seed_products = [
            ('Desenvolvimento de Web SaaS', 'Tecnologia & Software', 'Projeto', 450.00, 800.00, 150.00, 1400.00, 45.0, '2026-09-01 10:00'),
            ('Consultoria de Arquitetura Cloud', 'Serviços Profissionais', 'Hora', 25.00, 45.00, 10.00, 80.00, 50.0, '2026-09-02 11:30'),
            ('Manutenção Preventiva de Servidores', 'Suporte Técnico', 'Mês', 120.00, 180.00, 50.00, 350.00, 35.0, '2026-09-03 14:15'),
            ('Licença Anual Enterprise AI', 'Software & SaaS', 'Licença', 200.00, 300.00, 100.00, 600.00, 60.0, '2026-09-04 09:45'),
            ('Formação Corporativa em Segurança', 'Formação & Treino', 'Sessão', 150.00, 350.00, 100.00, 600.00, 40.0, '2026-09-05 16:20')
        ]

        cursor.executemany('''
            INSERT INTO products (name, category, unit, base_cost, labor_cost, overhead_cost, total_cost, target_margin_percent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_products)

    # Seed initial calculations if empty
    cursor.execute('SELECT COUNT(*) FROM calculations')
    if cursor.fetchone()[0] == 0:
        seed_calcs = [
            (1, 'Simulação Web SaaS Enterprise', 1400.00, 0.0, 0.0, 1400.00, 81.82, 1145.45, 45.0, 5.0, 2418.18, 23.0, 556.18, 2974.36, 1018.18, '2026-09-10 11:00'),
            (2, 'Pacote 40H Consultoria Cloud', 3200.00, 0.0, 0.0, 3200.00, 100.0, 3200.00, 50.0, 10.0, 5760.00, 23.0, 1324.80, 7084.80, 2560.00, '2026-09-11 15:30'),
            (3, 'Contrato Anual Suporte IT', 4200.00, 0.0, 0.0, 4200.00, 53.85, 2261.54, 35.0, 0.0, 6461.54, 23.0, 1486.15, 7947.69, 2261.54, '2026-09-12 09:15')
        ]

        cursor.executemany('''
            INSERT INTO calculations (product_id, title, base_cost, labor_cost, overhead_cost, total_cost, markup_percent, gross_profit, margin_percent, discount_percent, price_before_tax, vat_rate, vat_amount, final_price, net_profit, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_calcs)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados price_craft.db inicializada com sucesso!")
