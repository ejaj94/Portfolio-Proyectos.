import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'quotecraft.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Clients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        company_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        vat_nif TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Items Catalog Table (Services & Products)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT DEFAULT 'Serviço',
        unit_price REAL NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 3. Quotes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_number TEXT UNIQUE NOT NULL,
        client_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Enviado',
        issue_date TEXT NOT NULL,
        valid_until TEXT NOT NULL,
        discount_percent REAL DEFAULT 0.0,
        vat_rate REAL DEFAULT 23.0,
        subtotal REAL DEFAULT 0.0,
        tax_amount REAL DEFAULT 0.0,
        total_amount REAL DEFAULT 0.0,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    """)

    # 4. Quote Line Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quote_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        line_total REAL NOT NULL,
        FOREIGN KEY (quote_id) REFERENCES quotes (id)
    )
    """)

    # Seed Initial Data if empty
    cursor.execute("SELECT COUNT(*) FROM clients")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        today_str = date.today().strftime("%Y-%m-%d")
        valid_date = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")

        # Seed Clients
        clients_data = [
            ("Dr. Alexandre Mendes", "EJAJ TECH Global Lda", "alexandre@ejajtech.com", "+351 912 345 001", "PT509123456", "Av. da Liberdade, 200, Lisboa", now_str),
            ("Sofia Martins", "Inovação Digital SA", "sofia@inovacaodigital.pt", "+351 913 456 002", "PT508456789", "Rua de Santa Catarina, 450, Porto", now_str),
            ("Ricardo Alves", "Arquitetura & Design Lda", "ricardo@arqdesign.pt", "+351 914 567 003", "PT507789123", "Av. dos Aliados, 88, Porto", now_str),
            ("Mariana Magalhães", "Boutique Hotel Cascais", "mariana@hotelcascais.pt", "+351 915 678 004", "PT506111222", "Rua das Flores, 12, Cascais", now_str)
        ]
        cursor.executemany("""
        INSERT INTO clients (full_name, company_name, email, phone, vat_nif, address, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, clients_data)

        # Seed Catalog Items
        items_data = [
            ("Desenvolvimento de Plataforma Web SaaS", "Serviço", 3500.0, "Desenvolvimento completo de aplicação web responsiva com BD e API REST.", now_str),
            ("Consultoria de Arquitetura & Cloud AWS", "Serviço", 1500.0, "Auditoria técnica, infraestrutura de segurança e deployment em nuvem.", now_str),
            ("Módulo de Inteligência Artificial & Chatbot", "Serviço", 2200.0, "Integração de assistente virtual IA com processamento de linguagem natural.", now_str),
            ("Licença de Software SaaS Anual", "Produto", 1200.0, "Licença corporativa de uso para até 20 utilizadores em simultâneo.", now_str),
            ("Manutenção & Suporte Técnico 24/7 (Mensal)", "Serviço", 450.0, "Suporte prioritário com SLA de resposta garantido em 2 horas.", now_str)
        ]
        cursor.executemany("""
        INSERT INTO items (item_name, category, unit_price, description, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, items_data)

        # Seed Quotes
        quotes_data = [
            ("ORC-2026-001", 1, "Aprovado", today_str, valid_date, 5.0, 23.0, 5000.0, 1092.5, 5842.5, "Orçamento aprovado. Condição de pagamento: 50% na adjudicação e 50% na entrega final.", now_str),
            ("ORC-2026-002", 2, "Enviado", today_str, valid_date, 0.0, 23.0, 3700.0, 851.0, 4551.0, "Aguardando validação da administração técnica.", now_str),
            ("ORC-2026-003", 3, "Rascunho", today_str, valid_date, 10.0, 23.0, 1500.0, 310.5, 1660.5, "Rascunho inicial de consultoria de infraestrutura.", now_str),
            ("ORC-2026-004", 4, "Faturado", (date.today() - timedelta(days=15)).strftime("%Y-%m-%d"), today_str, 0.0, 23.0, 8200.0, 1886.0, 10086.0, "Proposta adjudicada e faturada com sucesso.", now_str)
        ]
        cursor.executemany("""
        INSERT INTO quotes (quote_number, client_id, status, issue_date, valid_until, discount_percent, vat_rate, subtotal, tax_amount, total_amount, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, quotes_data)

        # Seed Quote Line Items
        quote_items_data = [
            # Quote 1
            (1, "Desenvolvimento de Plataforma Web SaaS", 1, 3500.0, 3500.0),
            (1, "Consultoria de Arquitetura & Cloud AWS", 1, 1500.0, 1500.0),

            # Quote 2
            (2, "Módulo de Inteligência Artificial & Chatbot", 1, 2200.0, 2200.0),
            (2, "Consultoria de Arquitetura & Cloud AWS", 1, 1500.0, 1500.0),

            # Quote 3
            (3, "Consultoria de Arquitetura & Cloud AWS", 1, 1500.0, 1500.0),

            # Quote 4
            (4, "Desenvolvimento de Plataforma Web SaaS", 2, 3500.0, 7000.0),
            (4, "Licença de Software SaaS Anual", 1, 1200.0, 1200.0)
        ]
        cursor.executemany("""
        INSERT INTO quote_items (quote_id, item_name, quantity, unit_price, line_total)
        VALUES (?, ?, ?, ?, ?)
        """, quote_items_data)

    conn.commit()
    conn.close()
    print("[Database OK] quotecraft.db inicializada com sucesso.")

if __name__ == '__main__':
    init_db()
