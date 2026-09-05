import os
import sqlite3
from datetime import datetime, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'bookings.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Professionals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professionals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            specialty TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            avatar_url TEXT NOT NULL,
            bio TEXT NOT NULL
        )
    ''')

    # Services Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professional_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (professional_id) REFERENCES professionals (id) ON DELETE CASCADE
        )
    ''')

    # Schedules Table (Working Hours per day of week: 0=Mon, 6=Sun)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professional_id INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            start_time TEXT NOT NULL DEFAULT '09:00',
            end_time TEXT NOT NULL DEFAULT '18:00',
            lunch_start TEXT NOT NULL DEFAULT '13:00',
            lunch_end TEXT NOT NULL DEFAULT '14:00',
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (professional_id) REFERENCES professionals (id) ON DELETE CASCADE
        )
    ''')

    # Appointments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            professional_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            client_notes TEXT,
            status TEXT NOT NULL DEFAULT 'Confirmada',
            cancel_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professional_id) REFERENCES professionals (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')

    # Reminders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER NOT NULL,
            type TEXT NOT NULL DEFAULT 'SMS & E-mail',
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (appointment_id) REFERENCES appointments (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed demo professionals if empty
    cursor.execute('SELECT COUNT(*) FROM professionals')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    # Professionals
    profs = [
        ('Dr. Gabriel Santos', 'Médico Especialista', 'Medicina Geral & Preventiva', 'gabriel.santos@medilux.pt', '+351 912 345 678', 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=400&q=80', 'Mais de 15 anos de experiência em medicina preventiva, check-ups executivos e rastreios de saúde.'),
        ('Dra. Sofia Lima', 'Psicóloga Clínica', 'Psicologia & Neuro-Performance', 'sofia.lima@menteforma.pt', '+351 913 456 789', '/static/images/sofia_lima.jpg', 'Especialista em psicoterapia cognitiva-comportamental, gestão de stress ocupacional e desenvolvimento pessoal.'),
        ('Dr. Miguel Costa', 'Advogado Sénior', 'Direito Empresarial & Contratos', 'miguel.costa@costalaw.pt', '+351 914 567 890', 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80', 'Consultoria jurídica especializada para startups, reestruturações empresariais e assessoria contratual.')
    ]
    cursor.executemany('''
        INSERT INTO professionals (name, title, specialty, email, phone, avatar_url, bio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', profs)

    # Services for Prof 1 (Dr. Gabriel Santos)
    services = [
        (1, 'Consulta Geral de Medicina Preventiva', 'Saúde', 45, 75.00, 'Check-up completo de parâmetros vitais, análise de exames e plano de saúde preventiva.'),
        (1, 'Atestado Médico & Renovação de Carta', 'Saúde', 30, 45.00, 'Avaliação física e visão para emissão ou renovação de atestado médico oficial.'),
        (2, 'Sessão de Psicoterapia Individual', 'Psicologia', 50, 65.00, 'Sessão de apoio psicológico, gestão de ansiedade e estratégias cognitivas.'),
        (2, 'Avaliação de Neuro-Performance Executiva', 'Psicologia', 60, 90.00, 'Diagnóstico de foco, hábitos de sono, prevenção de burnout e otimização mental.'),
        (3, 'Consulta de Assessoria Jurídica Empresarial', 'Direito', 60, 120.00, 'Análise de contratos comerciais, proteção de marca e consultoria de negócios.'),
        (3, 'Elaboração & Revisão de Contratos', 'Direito', 90, 180.00, 'Redação minuciosa de minutas legais, acordos de sócios e proteção de património.')
    ]
    cursor.executemany('''
        INSERT INTO services (professional_id, title, category, duration_minutes, price, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', services)

    # Schedules for all professionals (Mon to Fri)
    for p_id in range(1, 4):
        for day in range(0, 5): # Mon(0) to Fri(4)
            cursor.execute('''
                INSERT INTO schedules (professional_id, day_of_week, start_time, end_time, lunch_start, lunch_end, is_active)
                VALUES (?, ?, '09:00', '18:00', '13:00', '14:00', 1)
            ''', (p_id, day))

    # Seed Sample Appointments
    today_str = datetime.now().strftime('%Y-%m-%d')
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    appointments = [
        ('AG-2026-1001', 1, 1, today_str, '10:00', '10:45', 'Ana Rodrigues', 'ana.rodrigues@email.pt', '+351 919 888 777', 'Consulta anual de rotina.', 'Confirmada', None),
        ('AG-2026-1002', 1, 2, today_str, '11:00', '11:30', 'Carlos Oliveira', 'carlos.o@email.pt', '+351 918 777 666', 'Renovação de atestado.', 'Confirmada', None),
        ('AG-2026-1003', 2, 3, tomorrow_str, '15:00', '15:50', 'Mariana Pinto', 'mariana.p@email.pt', '+351 917 666 555', 'Primeira consulta de ansiedade.', 'Confirmada', None),
        ('AG-2026-1004', 3, 5, tomorrow_str, '16:00', '17:00', 'TechCorp Portugal Lda', 'geral@techcorp.pt', '+351 210 987 654', 'Revisão de contrato de investimento.', 'Cancelada', 'Impossibilidade de comparência do cliente')
    ]
    cursor.executemany('''
        INSERT INTO appointments (code, professional_id, service_id, appointment_date, start_time, end_time, client_name, client_email, client_phone, client_notes, status, cancel_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', appointments)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados bookings.db inicializada com sucesso para Proyecto 47 (Sistema de Cita Previa SaaS)!")
