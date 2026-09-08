import os
import sqlite3
from datetime import datetime, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'gym.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Membership Plans Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            duration_months INTEGER NOT NULL DEFAULT 1,
            price REAL NOT NULL,
            access_hours TEXT NOT NULL,
            perks TEXT NOT NULL,
            is_popular INTEGER DEFAULT 0
        )
    ''')

    # 2. Members (Socios) Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_code TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            nif TEXT NOT NULL,
            plan_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            expiration_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Ativo',
            avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        )
    ''')

    # 3. Payments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            receipt_number TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL DEFAULT 'MBWay',
            status TEXT NOT NULL DEFAULT 'Pago',
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE
        )
    ''')

    # 4. Personal Trainers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Ativo'
        )
    ''')

    # 5. Group Classes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            trainer_name TEXT NOT NULL,
            schedule_time TEXT NOT NULL,
            room TEXT NOT NULL,
            max_capacity INTEGER DEFAULT 20,
            enrolled_count INTEGER DEFAULT 0
        )
    ''')

    # 6. Check-in / Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            member_name TEXT NOT NULL,
            checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            entry_type TEXT NOT NULL DEFAULT 'Turnstile QR',
            FOREIGN KEY (member_id) REFERENCES members (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed Demo Data if empty
    cursor.execute('SELECT COUNT(*) FROM plans')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    
    exp_active = (now + timedelta(days=25)).strftime("%Y-%m-%d")
    exp_expiring_soon = (now + timedelta(days=3)).strftime("%Y-%m-%d")
    exp_expired = (now - timedelta(days=5)).strftime("%Y-%m-%d")

    # 1. Seed Plans
    plans_data = [
        ('Passe Mensal Total', 1, 45.00, '06:00 - 23:00 (Livre Trânsito)', 'Acesso a musculação, cardio e banho quente', 0),
        ('Plano Anual Fit VIP', 12, 35.00, '06:00 - 23:00 (Livre Trânsito)', 'Acesso total, aulas de grupo ilimitadas e 1 sessão PT/mês', 1),
        ('Pack Estudante Off-Peak', 1, 29.90, '09:00 - 17:00 (Segunda a Sexta)', 'Acesso a musculação e cardio em horário reduzido', 0),
        ('Personal Training Elite', 1, 120.00, 'Horário Personalizado', '8 Sessões individuais de treino personalizado com acompanhamento nutricional', 0)
    ]
    cursor.executemany('''
        INSERT INTO plans (name, duration_months, price, access_hours, perks, is_popular)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', plans_data)

    # 2. Seed Trainers
    trainers_data = [
        ('Rodrigo Silva', 'CrossFit & Treino Funcional', '+351 912 999 888', 'rodrigo.silva@fitclub.pt', 'Ativo'),
        ('Camila Santos', 'Yoga, Pilates & Mobilidade', '+351 913 888 777', 'camila.santos@fitclub.pt', 'Ativo'),
        ('Gonçalo Mendes', 'Bodybuilding & Hipertrofia', '+351 914 777 666', 'goncalo.mendes@fitclub.pt', 'Ativo')
    ]
    cursor.executemany('''
        INSERT INTO trainers (name, specialty, phone, email, status)
        VALUES (?, ?, ?, ?, ?)
    ''', trainers_data)

    # 3. Seed Members
    members_data = [
        ('SOC-2026-101', 'Dra. Sofia Martins', 'sofia.martins@luxehotel.pt', '+351 918 777 666', '245890123', 2, now_str, exp_active, 'Ativo', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'),
        ('SOC-2026-102', 'Eng. Manuel Ribeiro', 'manuel.ribeiro@plasticosnorte.pt', '+351 919 888 777', '219876543', 1, now_str, exp_expiring_soon, 'Ativo', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'),
        ('SOC-2026-103', 'Tiago Oliveira', 'tiago.oliveira@gmail.com', '+351 916 555 444', '267123987', 3, '2026-07-01', exp_expired, 'Atrasado', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80'),
        ('SOC-2026-104', 'Beatriz Costa', 'beatriz.costa@hotmail.com', '+351 917 444 333', '289345123', 2, now_str, exp_active, 'Ativo', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80')
    ]
    cursor.executemany('''
        INSERT INTO members (member_code, full_name, email, phone, nif, plan_id, start_date, expiration_date, status, avatar_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', members_data)

    # 4. Seed Payments
    payments_data = [
        (1, 'REC-2026-801', 35.00, 'MBWay', 'Pago', now_str + ' 09:15:00'),
        (2, 'REC-2026-802', 45.00, 'Multibanco', 'Pago', now_str + ' 10:30:00'),
        (4, 'REC-2026-803', 35.00, 'Cartão', 'Pago', now_str + ' 14:00:00')
    ]
    cursor.executemany('''
        INSERT INTO payments (member_id, receipt_number, amount, payment_method, status, payment_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', payments_data)

    # 5. Seed Group Classes
    classes_data = [
        ('CrossFit WOD de Alta Intensidade', 'Rodrigo Silva', '08:30 - 09:30', 'Estúdio 1 (CrossFit)', 18, 14),
        ('Yoga Vinyasa & Mobilidade Articular', 'Camila Santos', '10:00 - 11:00', 'Estúdio 2 (Mind & Body)', 15, 12),
        ('Spinning Power Cycle 45', 'Gonçalo Mendes', '18:30 - 19:15', 'Sala de Cycling', 25, 22),
        ('Treino de Musculação & Hipertrofia', 'Gonçalo Mendes', '19:30 - 20:30', 'Zona de Halteres', 15, 10)
    ]
    cursor.executemany('''
        INSERT INTO classes (class_name, trainer_name, schedule_time, room, max_capacity, enrolled_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', classes_data)

    # 6. Seed Attendance / Check-ins
    attendance_data = [
        (1, 'Dra. Sofia Martins', now.strftime("%Y-%m-%d") + ' 08:12:00', 'Torniquete QR Code'),
        (2, 'Eng. Manuel Ribeiro', now.strftime("%Y-%m-%d") + ' 09:05:00', 'Torniquete QR Code'),
        (4, 'Beatriz Costa', now.strftime("%Y-%m-%d") + ' 12:45:00', 'Manual Receção')
    ]
    cursor.executemany('''
        INSERT INTO attendance (member_id, member_name, checkin_time, entry_type)
        VALUES (?, ?, ?, ?)
    ''', attendance_data)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados gym.db inicializada com sucesso para Proyecto 53!")
