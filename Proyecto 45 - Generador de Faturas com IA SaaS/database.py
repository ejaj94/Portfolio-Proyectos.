import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'invoices.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            nif TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # Invoices Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            vat_rate REAL NOT NULL DEFAULT 23.0,
            vat_amount REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')

    # Invoice Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            quantity REAL NOT NULL DEFAULT 1.0,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed demo clients if empty
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    clients = [
        ('TechCorp Portugal Lda', '509123456', 'Av. da Liberdade 245, 1250-142 Lisboa', 'contacto@techcorp.pt', '+351 210 987 654'),
        ('Restaurante Gourmet Sol & Mar', '508234567', 'Rua de Sta. Catarina 88, 4000-442 Porto', 'financeiro@gourmetsol.pt', '+351 220 123 456'),
        ('Imobiliária Vale do Sol S.A.', '507345678', 'Av. 5 de Outubro 110, 8000-076 Faro', 'facturacao@valedosol.pt', '+351 289 800 900'),
        ('Clínica Estética Luxo & Saúde', '506456789', 'Alameda dos Oceanos 50, 1990-203 Lisboa', 'contabilidade@luxesaude.pt', '+351 218 900 100')
    ]
    cursor.executemany('''
        INSERT INTO clients (name, nif, address, email, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', clients)

    # Seed sample invoices
    invoices = [
        ('FT 2026/001', 1, '2026-09-01', '2026-09-15', 1500.00, 23.0, 345.00, 1845.00, 'Paga', 'Desenvolvimento de plataforma e-commerce SaaS'),
        ('FT 2026/002', 2, '2026-09-03', '2026-09-17', 850.00, 23.0, 195.50, 1045.50, 'Pendente', 'Design de identidade visual e menu digital QR'),
        ('FT 2026/003', 3, '2026-08-15', '2026-08-30', 2300.00, 23.0, 529.00, 2829.00, 'Vencida', 'Sistema de CRM e integração de API imobiliária')
    ]
    cursor.executemany('''
        INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, subtotal, vat_rate, vat_amount, total, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', invoices)

    items = [
        (1, 'Desenvolvimento de Plataforma E-Commerce SaaS', 1.0, 1200.00, 1200.00),
        (1, 'Configuração de Gateway de Pagamentos MB WAY', 1.0, 300.00, 300.00),
        (2, 'Design de Logótipo & Branding Neon', 1.0, 500.00, 500.00),
        (2, 'Implementação de Menu Digital QR Code', 1.0, 350.00, 350.00),
        (3, 'Licenciamento Anual de Software CRM Enterprise', 1.0, 1800.00, 1800.00),
        (3, 'Formação Técnica da Equipa Comercial (5h)', 5.0, 100.00, 500.00)
    ]
    cursor.executemany('''
        INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', items)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados invoices.db inicializada com sucesso para Proyecto 45 (Generador de Faturas com IA)!")
