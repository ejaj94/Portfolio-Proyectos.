import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'donations_system.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create Campaigns Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            cause_category TEXT NOT NULL,
            goal_amount REAL NOT NULL,
            raised_amount REAL DEFAULT 0.0,
            description TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT DEFAULT 'Ativa',
            image_url TEXT
        )
    ''')

    # Create Donors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            donor_tier TEXT DEFAULT 'Benfeitor Solidário',
            total_donated REAL DEFAULT 0.0
        )
    ''')

    # Create Donations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            donor_name TEXT NOT NULL,
            donor_email TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT DEFAULT 'MBWay / Cartão',
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
    ''')

    # Seed Data if empty
    cursor.execute('SELECT COUNT(*) FROM campaigns')
    if cursor.fetchone()[0] == 0:
        sample_campaigns = [
            ("Fundo de Apoio Alimentar Comunitário", "Apoio Humanitário & Social", 30000.0, 24500.0, "Reforço de cabazes alimentares de emergência e refeições quentes para famílias carenciadas e idosos em situação de isolamento.", "2026-11-30", "Ativa", "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=600"),
            ("Resgate & Cuidados Veterinários de Urgência", "Proteção Animal", 15000.0, 15000.0, "Financiamento de tratamentos cirúrgicos, vacinação e alimentação para animais de rua resgatados por associações de proteção animal.", "2026-10-15", "Concluída", "https://images.unsplash.com/photo-1548767797-d8c844163c4c?w=600"),
            ("Bolsas de Estudo para Jovens Talentos", "Educação & Igualdade", 20000.0, 14200.0, "Financiamento de propinas, material escolar e apoio habitacional para estudantes universitários com elevado rendimento académico e carência financeira.", "2026-12-15", "Ativa", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=600"),
            ("Equipamento Médico para Cuidados Pediátricos", "Saúde & Emergência Médica", 50000.0, 38900.0, "Aquisição de incubadoras de transporte e monitores de sinais vitais para unidades de pediatria de hospitais públicos.", "2026-12-31", "Ativa", "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=600")
        ]
        cursor.executemany('INSERT INTO campaigns (title, cause_category, goal_amount, raised_amount, description, end_date, status, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', sample_campaigns)

        sample_donors = [
            ("Dra. Beatriz Mendes", "beatriz.mendes@saude.pt", "+351 912 345 678", "Patrono Benemérito", 2500.0),
            ("Eng.º Henrique Alvares", "henrique.alvares@tech.pt", "+351 934 567 890", "Doador VIP", 1200.0),
            ("Clara Fontes", "clara.fontes@gmail.com", "+351 965 432 109", "Benfeitor Solidário", 450.0),
            ("Tiago Gouveia", "tiago.gouveia@outlook.pt", "+351 927 890 123", "Membro Solidário", 250.0)
        ]
        cursor.executemany('INSERT INTO donors (name, email, phone, donor_tier, total_donated) VALUES (?, ?, ?, ?, ?)', sample_donors)

        sample_donations = [
            (1, "Dra. Beatriz Mendes", "beatriz.mendes@saude.pt", 1500.0, "MBWay", "Contribuição para aquisição de 100 cabazes alimentares de emergência.", "2026-09-08 11:20"),
            (1, "Eng.º Henrique Alvares", "henrique.alvares@tech.pt", 500.0, "Cartão de Crédito", "Apoio continuado ao programa de apoio comunitário.", "2026-09-09 16:45"),
            (2, "Clara Fontes", "clara.fontes@gmail.com", 350.0, "Transferência Bancária", "Doação destinada a cuidados veterinários e cirurgias de urgência.", "2026-09-10 10:15"),
            (3, "Tiago Gouveia", "tiago.gouveia@outlook.pt", 250.0, "MBWay", "Financiamento de propinas escolares de início de ano letivo.", "2026-09-11 14:30"),
            (4, "Dra. Beatriz Mendes", "beatriz.mendes@saude.pt", 1000.0, "Cartão de Crédito", "Contribuição prioritária para equipamentos de neonatologia.", "2026-09-12 17:10")
        ]
        cursor.executemany('INSERT INTO donations (campaign_id, donor_name, donor_email, amount, payment_method, note, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)', sample_donations)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de Dados donations_system.db inicializado com sucesso!")
