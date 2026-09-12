import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vetcraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS owners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        nif TEXT UNIQUE NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        species TEXT NOT NULL,
        breed TEXT NOT NULL,
        age_years REAL NOT NULL,
        weight_kg REAL NOT NULL,
        microchip_id TEXT UNIQUE NOT NULL,
        gender TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES owners (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        vet_name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Agendada',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE,
        FOREIGN KEY (owner_id) REFERENCES owners (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vaccines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER NOT NULL,
        vaccine_name TEXT NOT NULL,
        batch_number TEXT NOT NULL,
        admin_date TEXT NOT NULL,
        next_due_date TEXT NOT NULL,
        vet_name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Válida',
        notes TEXT,
        FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER NOT NULL,
        diagnosis TEXT NOT NULL,
        prescription TEXT NOT NULL,
        dosage TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        cost REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'Em Curso',
        FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER NOT NULL,
        owner_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        reminder_type TEXT NOT NULL,
        target_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pendente',
        sent_channel TEXT NOT NULL DEFAULT 'SMS / WhatsApp',
        FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE,
        FOREIGN KEY (owner_id) REFERENCES owners (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER NOT NULL,
        visit_date TEXT NOT NULL,
        symptoms TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        vet_signature TEXT NOT NULL,
        total_cost REAL NOT NULL,
        FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE
    )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM owners')
    if cursor.fetchone()[0] == 0:
        # Seed Owners
        owners_data = [
            ("Dra. Sofia Mendonça", "+351 912 345 678", "sofia.mendonca@email.pt", "Av. da Liberdade, 102, Lisboa", "239847102", "Cliente habitual com 2 animais."),
            ("João Carlos Ribeiro", "+351 934 567 890", "j.ribeiro@netcabo.pt", "Rua de Santa Catarina, 45, Porto", "198765432", "Prefere contacto por WhatsApp."),
            ("Ana Beatriz Fonseca", "+351 965 432 109", "ana.fonseca@sapo.pt", "Praça do Giraldo, 18, Évora", "287654321", "Membro do plano de saúde VetCraft Gold."),
            ("Dr. Miguel Ângelo Neves", "+351 927 890 123", "m.neves@veterinaria.pt", "Rua das Flores, 88, Coimbra", "210987654", "Proprietário de canil certificado."),
            ("Mariana Silva Santos", "+351 918 273 645", "mariana.santos@gmail.com", "Rua Garrett, 14, Lisboa", "254123987", "Acolheu pet resgatado recentemente.")
        ]
        cursor.executemany('''
            INSERT INTO owners (name, phone, email, address, nif, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', owners_data)

        # Seed Pets
        pets_data = [
            (1, "Thor", "Cão", "Rafeiro do Alentejo", 3.5, 32.4, "620098100293847", "Macho", "Muito dócil, medo de barulhos fortes."),
            (1, "Luna", "Gato", "Europeu Comum", 2.0, 4.1, "620098100998877", "Fêmea", "Esterilizada. Excelente estado geral."),
            (2, "Max", "Cão", "Pastor Alemão", 5.0, 38.0, "620098100554433", "Macho", "Treinado para guarda. Vacinação em dia."),
            (3, "Bibi", "Cão", "Cão de Fila de São Miguel", 1.8, 24.5, "620098100112233", "Fêmea", "Sensibilidade alimentar a frango."),
            (4, "Simba", "Gato", "Persa", 4.2, 5.2, "620098100778899", "Macho", "Escovagem diária necessária."),
            (5, "Pipoca", "Coelho", "Mini Lop", 1.0, 1.8, "620098100334455", "Fêmea", "Dieta rica em feno de timóteo.")
        ]
        cursor.executemany('''
            INSERT INTO pets (owner_id, name, species, breed, age_years, weight_kg, microchip_id, gender, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', pets_data)

        # Seed Appointments
        appointments_data = [
            (1, 1, "Dra. Mariana Costa (Vet)", "2026-09-15", "10:30", "Consulta Geral & Desparasitação", "Agendada", "Revisão anual completa."),
            (2, 2, "Dr. Ricardo Alvear (Vet)", "2026-09-15", "11:45", "Boletim de Vacinação - Reforço", "Agendada", "Vacina antirrábica obrigatória."),
            (3, 3, "Dra. Mariana Costa (Vet)", "2026-09-16", "15:00", "Check-up Dermatológico", "Confirmada", "Acompanhamento de alergia sazonal."),
            (4, 4, "Dr. Tiago Henriques (Vet)", "2026-09-17", "09:15", "Limpeza Dentária por Ultrassons", "Agendada", "Jejum de 8 horas necessário."),
            (5, 5, "Dr. Ricardo Alvear (Vet)", "2026-09-18", "16:30", "Controlo de Peso & Nutrição", "Agendada", "Ajuste na ração de coelhos sénior.")
        ]
        cursor.executemany('''
            INSERT INTO appointments (pet_id, owner_id, vet_name, date, time, reason, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', appointments_data)

        # Seed Vaccines
        vaccines_data = [
            (1, "Nobivac DHPPi + Lepto", "BATCH-PT-9842", "2025-09-10", "2026-09-10", "Dra. Mariana Costa", "Expirada", "Necessário agendar reforço urgente."),
            (2, "Purevax RCP + FeLV", "BATCH-PT-4421", "2026-03-15", "2027-03-15", "Dr. Ricardo Alvear", "Válida", "Tolerado sem reações adversas."),
            (3, "Rabisin Antirrábica", "BATCH-PT-1109", "2025-10-01", "2026-10-01", "Dr. Tiago Henriques", "Válida", "Obrigatória por lei."),
            (4, "Eurican DAP-Lmulti", "BATCH-PT-7762", "2026-01-20", "2027-01-20", "Dra. Mariana Costa", "Válida", "Dose administrada no membro posterior."),
            (5, "Felocell 4", "BATCH-PT-3321", "2026-05-12", "2027-05-12", "Dr. Ricardo Alvear", "Válida", "Próximo reforço em 2027.")
        ]
        cursor.executemany('''
            INSERT INTO vaccines (pet_id, vaccine_name, batch_number, admin_date, next_due_date, vet_name, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', vaccines_data)

        # Seed Treatments
        treatments_data = [
            (1, "Otite Externa Bilateral", "Ciprofloxacina gota otológica + Anti-inflamatório", "4 gotas cada ouvido de 12/12h", "2026-09-01", "2026-09-14", 45.50, "Em Curso"),
            (3, "Dermatite Atópica Canina", "Oclacitinib 16mg + Champô Hipoalergénico", "1 comprimido/dia durante 30 dias", "2026-08-20", "2026-09-20", 82.00, "Em Curso"),
            (4, "Gengivite Moderada", "Clorexidina gel oral + Amoxicilina 250mg", "Aplicação após refeições / 1 comp. 12/12h", "2026-09-05", "2026-09-15", 38.00, "Em Curso"),
            (2, "Desparasitação Interna", "Milbemax Gatos", "1 comprimido dose única", "2026-08-01", "2026-08-01", 12.50, "Concluído")
        ]
        cursor.executemany('''
            INSERT INTO treatments (pet_id, diagnosis, prescription, dosage, start_date, end_date, cost, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', treatments_data)

        # Seed Reminders
        reminders_data = [
            (1, 1, "Reforço de Vacina Antirrábica", "Vacina", "2026-09-15", "Pendente", "SMS / WhatsApp"),
            (2, 1, "Desparasitação Externa (Bravecto)", "Desparasitação", "2026-09-20", "Pendente", "Email"),
            (3, 2, "Check-up Trimestral de Displasia", "Consulta", "2026-09-25", "Pendente", "SMS / WhatsApp"),
            (4, 3, "Avaliação Dermatológica de Seguimento", "Exame", "2026-09-18", "Enviado", "WhatsApp"),
            (5, 4, "Controlo Terapêutico de Gengivite", "Tratamento", "2026-09-22", "Pendente", "Email")
        ]
        cursor.executemany('''
            INSERT INTO reminders (pet_id, owner_id, title, reminder_type, target_date, status, sent_channel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', reminders_data)

        # Seed Medical History
        history_data = [
            (1, "2026-06-10", "Claudicação ligeira na pata posterior esquerda", "Entorse articular ligeira", "Dr. Ricardo Alvear", 65.00),
            (1, "2026-01-15", "Vómitos esporádicos e prostração", "Gastrenterite alimentar benigna", "Dra. Mariana Costa", 50.00),
            (2, "2026-03-15", "Check-up preventivo de rotina", "Estado de saúde ótimo", "Dr. Ricardo Alvear", 35.00),
            (3, "2026-05-22", "Prurido intenso nas orelhas e patas", "Dermatite alérgica por picada de pulga", "Dra. Mariana Costa", 75.50),
            (4, "2026-04-02", "Táxi dentário acumulado e halitose", "Tártaro Grau II com inflamação gengival", "Dr. Tiago Henriques", 120.00)
        ]
        cursor.executemany('''
            INSERT INTO medical_history (pet_id, visit_date, symptoms, diagnosis, vet_signature, total_cost)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', history_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados VetCraft AI inicializada com sucesso!")
