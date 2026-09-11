import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'realtycraft.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Properties Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        property_type TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        price REAL NOT NULL,
        bedrooms INTEGER DEFAULT 1,
        bathrooms INTEGER DEFAULT 1,
        area_sqm REAL NOT NULL,
        status TEXT DEFAULT 'Disponível',
        image_icon TEXT DEFAULT 'fa-building',
        agent_name TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Clients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        client_type TEXT DEFAULT 'Comprador',
        budget_max REAL DEFAULT 0.0,
        preferred_type TEXT DEFAULT 'Apartamento',
        status TEXT DEFAULT 'Ativo',
        created_at TEXT NOT NULL
    )
    """)

    # 3. Leads Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        property_id INTEGER,
        source TEXT DEFAULT 'Website',
        status TEXT DEFAULT 'Novo Lead',
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (property_id) REFERENCES properties (id)
    )
    """)

    # 4. Visits Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        visit_date TEXT NOT NULL,
        visit_time TEXT NOT NULL,
        agent_name TEXT NOT NULL,
        status TEXT DEFAULT 'Agendada',
        notes TEXT,
        FOREIGN KEY (property_id) REFERENCES properties (id),
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    """)

    # 5. Offers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        offer_amount REAL NOT NULL,
        status TEXT DEFAULT 'Pendente',
        offer_date TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (property_id) REFERENCES properties (id),
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    """)

    # Seed Initial Data if empty
    cursor.execute("SELECT COUNT(*) FROM properties")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        today_str = date.today().strftime("%Y-%m-%d")
        next_week = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")

        # Seed Properties
        properties_data = [
            ("Apartamento T3 de Luxo nas Avenidas Novas", "Apartamento", "Av. da República, 45", "Lisboa", 680000.0, 3, 2, 145.0, "Disponível", "fa-building", "Enmanuel Jimenez", now_str),
            ("Moradia Contemporânea V4 com Piscina", "Moradia", "Rua das Palmeiras, 12", "Cascais", 1250000.0, 4, 4, 320.0, "Disponível", "fa-house-chimney", "Sofia Martins", now_str),
            ("Escritório Prime em Edifício Corporativo", "Escritório", "Av. da Boavista, 1200", "Porto", 420000.0, 0, 2, 180.0, "Reservado", "fa-briefcase", "Ricardo Alves", now_str),
            ("Loja Comercial com Alta Visibilidade", "Loja", "Rua Augusta, 88", "Lisboa", 890000.0, 0, 1, 110.0, "Disponível", "fa-store", "Carlos Ferreira", now_str),
            ("Terreno Urbanizável com Projeto Aprovado", "Terreno", "Quinta da Beloura", "Sintra", 350000.0, 0, 0, 850.0, "Disponível", "fa-mountain-sun", "Mariana Magalhães", now_str)
        ]
        cursor.executemany("""
        INSERT INTO properties (title, property_type, address, city, price, bedrooms, bathrooms, area_sqm, status, image_icon, agent_name, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, properties_data)

        # Seed Clients
        clients_data = [
            ("Dr. Fernando Albuquerque", "fernando.albuquerque@email.com", "+351 912 345 777", "Comprador", 750000.0, "Apartamento", "Ativo", now_str),
            ("Dra. Maria Clara Ramos", "clara.ramos@email.com", "+351 913 456 888", "Investidor", 1500000.0, "Moradia", "Ativo", now_str),
            ("Grupo Empresarial Silva & Filhos", "contacto@gruposilva.pt", "+351 914 567 999", "Comprador", 500000.0, "Escritório", "Ativo", now_str),
            ("Pedro Mendonça", "pedro.mendonca@email.com", "+351 915 678 111", "Vendedor", 0.0, "Moradia", "Ativo", now_str)
        ]
        cursor.executemany("""
        INSERT INTO clients (full_name, email, phone, client_type, budget_max, preferred_type, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, clients_data)

        # Seed Leads
        leads_data = [
            ("Dr. Fernando Albuquerque", "fernando.albuquerque@email.com", "+351 912 345 777", 1, "Portal Imobiliário", "Visita Agendada", "Interessado no T3 de Luxo para habitação própria.", now_str),
            ("Dra. Maria Clara Ramos", "clara.ramos@email.com", "+351 913 456 888", 2, "Website", "Proposta", "Proposta formal apresentada para a Moradia em Cascais.", now_str),
            ("Grupo Empresarial Silva & Filhos", "contacto@gruposilva.pt", "+351 914 567 999", 3, "Recomendação", "Em Contacto", "Procura sede corporativa no Porto.", now_str),
            ("Teresa Barreto", "teresa.barreto@email.com", "+351 916 789 222", 4, "Redes Sociais", "Novo Lead", "Solicitou informações sobre a Loja na Rua Augusta.", now_str)
        ]
        cursor.executemany("""
        INSERT INTO leads (client_name, email, phone, property_id, source, status, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, leads_data)

        # Seed Visits
        visits_data = [
            (1, 1, next_week, "15:30", "Enmanuel Jimenez", "Agendada", "Primeira visita acompanhada com o cliente."),
            (2, 2, (date.today() - timedelta(days=2)).strftime("%Y-%m-%d"), "11:00", "Sofia Martins", "Realizada", "Cliente adorou a piscina e a zona de jardim."),
            (3, 3, (date.today() + timedelta(days=3)).strftime("%Y-%m-%d"), "16:00", "Ricardo Alves", "Agendada", "Visita técnica com arquiteto do cliente.")
        ]
        cursor.executemany("""
        INSERT INTO visits (property_id, client_id, visit_date, visit_time, agent_name, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, visits_data)

        # Seed Offers
        offers_data = [
            (2, 2, 1200000.0, "Pendente", today_str, "Oferta de 1.20M € sujeita a aprovação de financiamento bancário."),
            (3, 3, 400000.0, "Em Negociação", (date.today() - timedelta(days=4)).strftime("%Y-%m-%d"), "Contraproposta do proprietário enviada.")
        ]
        cursor.executemany("""
        INSERT INTO offers (property_id, client_id, offer_amount, status, offer_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, offers_data)

    conn.commit()
    conn.close()
    print("[Database OK] realtycraft.db inicializada com sucesso.")

if __name__ == '__main__':
    init_db()
