import sqlite3
import os
import uuid

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eventcraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS organizers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        nif TEXT UNIQUE NOT NULL,
        verified_status TEXT NOT NULL DEFAULT 'Verificado',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        nif TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        organizer_id INTEGER NOT NULL,
        venue_name TEXT NOT NULL,
        city TEXT NOT NULL,
        event_date TEXT NOT NULL,
        event_time TEXT NOT NULL,
        total_capacity INTEGER NOT NULL,
        available_tickets INTEGER NOT NULL,
        ticket_price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Ativo',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (organizer_id) REFERENCES organizers (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        ticket_code TEXT UNIQUE NOT NULL,
        qr_code_url TEXT NOT NULL,
        seat_category TEXT NOT NULL DEFAULT 'Geral / Plateia',
        price_paid REAL NOT NULL,
        purchase_date TEXT NOT NULL,
        checkin_status TEXT NOT NULL DEFAULT 'Pendente',
        checkin_time TEXT,
        FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS checkin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        gate_number TEXT NOT NULL DEFAULT 'Porta Principal A1',
        validator_name TEXT NOT NULL DEFAULT 'Staff EventCraft',
        status_result TEXT NOT NULL DEFAULT 'VÁLIDO',
        FOREIGN KEY (ticket_id) REFERENCES tickets (id) ON DELETE CASCADE
    )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM organizers')
    if cursor.fetchone()[0] == 0:
        # Seed Organizers
        organizers_data = [
            ("Dra. Sofia Mendonça", "Lisbon Tech Events Lda.", "sofia@lisbontech.pt", "+351 912 345 678", "239847109", "Verificado"),
            ("Eng. João Carlos Ribeiro", "Porto Live Productions SA", "j.ribeiro@portolive.pt", "+351 934 567 890", "198765432", "Verificado"),
            ("Ana Beatriz Fonseca", "Cascais Entertainment Group", "ana@cascais-ent.pt", "+351 965 432 109", "287654321", "Verificado")
        ]
        cursor.executemany('''
            INSERT INTO organizers (name, company_name, email, phone, nif, verified_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', organizers_data)

        # Seed Users
        users_data = [
            ("Tomás Afonso Ferreira", "tomas.ferreira@estudante.pt", "+351 919 876 543", "254987123"),
            ("Inês Filipa Magalhães", "ines.magalhaes@gmail.com", "+351 934 123 789", "267890123"),
            ("Martim José Coimbra", "martim.coimbra@sapo.pt", "+351 961 234 567", "289123456"),
            ("Carolina Santos Paiva", "carolina.paiva@outloo.pt", "+351 925 876 123", "245678901"),
            ("Diogo Alexandre Henriques", "diogo.henriques@netcabo.pt", "+351 918 345 678", "234567890")
        ]
        cursor.executemany('''
            INSERT INTO users (name, email, phone, nif)
            VALUES (?, ?, ?, ?)
        ''', users_data)

        # Seed Events
        events_data = [
            ("Summit de Tecnologia & IA Lisboa 2026", "Conferência", 1, "MEO Arena / Altice Arena", "Lisboa", "2026-09-25", "09:00", 2500, 2480, 85.00, "Ativo"),
            ("Festival de Música Eletrónica Sunset Porto", "Festival / Concérto", 2, "Parque da Cidade", "Porto", "2026-10-02", "16:00", 5000, 4920, 45.00, "Ativo"),
            ("Gala Anual de Inovação & Empreendedorismo", "Gala & Network", 1, "Casino Estoril", "Cascais", "2026-10-15", "20:00", 600, 580, 120.00, "Ativo"),
            ("Congresso Nacional de Medicina & Saúde", "Congresso", 3, "Centro de Congressos de Lisboa", "Lisboa", "2026-11-05", "08:30", 1200, 1150, 95.00, "Ativo")
        ]
        cursor.executemany('''
            INSERT INTO events (title, category, organizer_id, venue_name, city, event_date, event_time, total_capacity, available_tickets, ticket_price, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', events_data)

        # Seed Tickets
        tickets_data = [
            (1, 1, "TCK-EVT-984210", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TCK-EVT-984210", "VIP Pass", 85.00, "2026-09-01", "Validado (Check-in Efetuado)", "2026-09-12 10:30:00"),
            (1, 2, "TCK-EVT-442190", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TCK-EVT-442190", "Geral", 85.00, "2026-09-02", "Pendente", None),
            (2, 3, "TCK-EVT-771234", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TCK-EVT-771234", "Relvado Frontstage", 45.00, "2026-09-05", "Validado (Check-in Efetuado)", "2026-09-12 11:15:00"),
            (3, 4, "TCK-EVT-332190", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TCK-EVT-332190", "Mesa VIP", 120.00, "2026-09-10", "Pendente", None)
        ]
        cursor.executemany('''
            INSERT INTO tickets (event_id, user_id, ticket_code, qr_code_url, seat_category, price_paid, purchase_date, checkin_status, checkin_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tickets_data)

        # Seed Checkin Logs
        logs_data = [
            (1, "Porta VIP 1", "Operador Miguel Silva", "VÁLIDO - Entrada Autorizada"),
            (3, "Porta Geral 3", "Operadora Beatriz Santos", "VÁLIDO - Entrada Autorizada")
        ]
        cursor.executemany('''
            INSERT INTO checkin_logs (ticket_id, gate_number, validator_name, status_result)
            VALUES (?, ?, ?, ?)
        ''', logs_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados EventCraft AI inicializada com sucesso!")
