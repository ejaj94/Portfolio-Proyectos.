import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'medicare.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        blood_type TEXT NOT NULL,
        nif TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL
    );
    """)

    # 2. Specialties Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS specialties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        icon TEXT NOT NULL,
        description TEXT NOT NULL
    );
    """)

    # 3. Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty_id INTEGER NOT NULL,
        crm_license TEXT NOT NULL UNIQUE,
        rating REAL NOT NULL DEFAULT 4.9,
        consultation_fee REAL NOT NULL DEFAULT 60.0,
        location TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Disponível',
        FOREIGN KEY (specialty_id) REFERENCES specialties (id)
    );
    """)

    # 4. Schedules Table (Available Time Slots)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        day_of_week TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        is_available INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    );
    """)

    # 5. Appointments Table (Citas Médicas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_code TEXT NOT NULL UNIQUE,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        specialty_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmada', -- Confirmada, Em Espera, Concluída, Cancelada
        reason TEXT NOT NULL,
        fee REAL NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id),
        FOREIGN KEY (specialty_id) REFERENCES specialties (id)
    );
    """)

    # 6. Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL DEFAULT 'Lembrete', -- Lembrete, Confirmação, Alerta
        timestamp TEXT NOT NULL,
        is_read INTEGER NOT NULL DEFAULT 0
    );
    """)

    # 7. Medical History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        diagnosis TEXT NOT NULL,
        prescription TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (appointment_id) REFERENCES appointments (id),
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    );
    """)

    # --- SEED DATA ---
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = date.today()

    # Seed Patients
    patients_data = [
        ("Maria Eduarda Silva", "maria.silva@email.com", "+351 912 888 111", "1992-05-14", "A+", "299100201", now_str),
        ("João Pedro Costa", "joao.costa@email.com", "+351 913 777 222", "1985-11-20", "O+", "288200302", now_str),
        ("Ana Beatriz Santos", "ana.santos@email.com", "+351 914 666 333", "1998-03-08", "B-", "277300403", now_str),
        ("Carlos Manuel Oliveira", "carlos.oliveira@email.com", "+351 915 555 444", "1978-08-30", "AB+", "266400504", now_str)
    ]
    cursor.executemany("""
    INSERT INTO patients (name, email, phone, birth_date, blood_type, nif, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, patients_data)

    # Seed Specialties
    specialties_data = [
        ("Cardiologia", "fa-heart-pulse", "Cuidados do coração e sistema cardiovascular"),
        ("Pediatria", "fa-baby", "Saúde e desenvolvimento infantil"),
        ("Dermatologia", "fa-disease", "Diagnóstico e tratamento da pele e cabelo"),
        ("Neurologia", "fa-brain", "Distúrbios do sistema nervoso e cérebro"),
        ("Ortopedia", "fa-bone", "Tratamento do sistema musculoesquelético"),
        ("Clínica Geral", "fa-user-doctor", "Atendimento médico primário e preventivo")
    ]
    cursor.executemany("""
    INSERT INTO specialties (name, icon, description)
    VALUES (?, ?, ?)
    """, specialties_data)

    # Seed Doctors
    doctors_data = [
        ("Dra. Sofia Ramos", 1, "OM-58901", 4.9, 75.0, "Hospital Central Lisboa - Bloco A", "Disponível"),
        ("Dr. Enmanuel Jimenez", 6, "OM-99203", 5.0, 60.0, "Clínica MediCare Porto - Sala 204", "Disponível"),
        ("Dra. Mariana Fonseca", 2, "OM-44120", 4.8, 65.0, "Centro Médico Cascais - Piso 1", "Disponível"),
        ("Dr. Rodrigo Mendes", 3, "OM-77304", 4.9, 80.0, "MediCare Saúde Coimbra", "Disponível"),
        ("Dr. Tiago Albuquerque", 4, "OM-33019", 4.9, 90.0, "Instituto de Neurologia Lisboa", "Disponível"),
        ("Dra. Beatriz Lima", 5, "OM-88214", 4.7, 70.0, "Clínica Ortopédica do Norte", "Disponível")
    ]
    cursor.executemany("""
    INSERT INTO doctors (name, specialty_id, crm_license, rating, consultation_fee, location, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, doctors_data)

    # Seed Schedules
    time_slots = ["09:00", "10:00", "11:30", "14:00", "15:30", "17:00"]
    days = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
    for doc_id in range(1, 7):
        for day in days[:3]:
            for slot in time_slots[:4]:
                cursor.execute("""
                INSERT INTO schedules (doctor_id, day_of_week, time_slot, is_available)
                VALUES (?, ?, ?, 1)
                """, (doc_id, day, slot))

    # Seed Appointments
    appts_data = [
        ("CIT-2026-501", 1, 1, 1, (today + timedelta(days=1)).strftime("%Y-%m-%d"), "10:00", "Confirmada", "Check-up cardiológico de rotina e eletrocardiograma.", 75.0, now_str),
        ("CIT-2026-502", 2, 2, 6, today.strftime("%Y-%m-%d"), "14:00", "Confirmada", "Consulta de medicina geral para sintomas de gripe.", 60.0, now_str),
        ("CIT-2026-503", 3, 3, 2, (today + timedelta(days=3)).strftime("%Y-%m-%d"), "11:30", "Confirmada", "Consulta pediátrica de acompanhamento de desenvolvimento.", 65.0, now_str),
        ("CIT-2026-504", 4, 4, 3, (today - timedelta(days=4)).strftime("%Y-%m-%d"), "15:30", "Concluída", "Avaliação dermatológica de sinais de pele.", 80.0, (today - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"))
    ]
    cursor.executemany("""
    INSERT INTO appointments (appointment_code, patient_id, doctor_id, specialty_id, appointment_date, appointment_time, status, reason, fee, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appts_data)

    # Seed Notifications
    notifications_data = [
        ("Lembrete de Consulta 🩺", "A sua consulta com a Dra. Sofia Ramos está agendada para amanhã às 10:00.", "Lembrete", (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), 0),
        ("Confirmação de Cita 🗓️", "Cita médica CIT-2026-502 com o Dr. Enmanuel Jimenez confirmada com sucesso.", "Confirmação", (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"), 0),
        ("Receita Médica Disponível 💊", "A receita médica da consulta de Dermatologia já se encontra disponível no seu historial.", "Alerta", (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d %H:%M"), 1)
    ]
    cursor.executemany("""
    INSERT INTO notifications (title, message, type, timestamp, is_read)
    VALUES (?, ?, ?, ?, ?)
    """, notifications_data)

    # Seed Medical History
    history_data = [
        (4, 4, 4, "Dermatite de contacto leve com eritema localizado.", "Creme Hidrocortisona 1% - Aplicar 2x ao dia durante 7 dias. Anti-histamínico oral.", "Paciente aconselhado a evitar sabões perfumados.", (today - timedelta(days=4)).strftime("%Y-%m-%d %H:%M"))
    ]
    cursor.executemany("""
    INSERT INTO medical_history (appointment_id, patient_id, doctor_id, diagnosis, prescription, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, history_data)

    conn.commit()
    conn.close()
    print("[Database OK] medicare.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
