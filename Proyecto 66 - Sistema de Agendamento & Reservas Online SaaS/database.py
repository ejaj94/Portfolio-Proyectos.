import sqlite3
import os
import json
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'bookings.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for Services
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        description TEXT,
        duration_min INTEGER NOT NULL DEFAULT 45,
        price REAL NOT NULL DEFAULT 0.0,
        category TEXT DEFAULT 'Geral',
        color TEXT DEFAULT '#DC2626'
    )
    """)

    # Table for Bookings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER NOT NULL,
        client_name TEXT NOT NULL,
        client_email TEXT NOT NULL,
        client_phone TEXT NOT NULL,
        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL,
        status TEXT DEFAULT 'Confirmado',
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (service_id) REFERENCES services (id) ON DELETE CASCADE
    )
    """)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Insert Seed Services (name, slug, description, duration_min, price, category, color)
    cursor.execute("""
    INSERT INTO services (name, slug, description, duration_min, price, category, color)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Consultoria de Software & IA 🧠",
        "consultoria-software-ia",
        "Sessão estratégica de arquitetura de software, automação empresarial e soluções SaaS.",
        60,
        150.0,
        "Tecnologia",
        "#DC2626"
    ))
    s1_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO services (name, slug, description, duration_min, price, category, color)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Consulta Médica / Nutrição VIP 🩺",
        "consulta-medica-nutricao-vip",
        "Avaliação personalizada de saúde, plano alimentar e acompanhamento biomecânico.",
        45,
        80.0,
        "Saúde",
        "#8B5CF6"
    ))
    s2_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO services (name, slug, description, duration_min, price, category, color)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Corte & Barba Salão Executive 💈",
        "corte-barba-salao-executive",
        "Atendimento exclusivo de barbearia premium com bebidas e tratamento capilar.",
        30,
        35.0,
        "Estética",
        "#EAB308"
    ))
    s3_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO services (name, slug, description, duration_min, price, category, color)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Sessão de Coaching Executivo 💼",
        "sessao-coaching-executivo",
        "Mentoria de liderança, gestão de equipas e plano de aceleração de carreira.",
        60,
        120.0,
        "Consultoria",
        "#06B6D4"
    ))

    # Insert Seed Bookings
    cursor.execute("""
    INSERT INTO bookings (service_id, client_name, client_email, client_phone, booking_date, booking_time, status, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        s1_id,
        "Ricardo Alvo",
        "ricardo.alvo@techcorp.pt",
        "+351 912 987 654",
        "2026-09-10",
        "10:00",
        "Confirmado",
        "Reunião de alinhamento para arquitetura SaaS.",
        now
    ))

    cursor.execute("""
    INSERT INTO bookings (service_id, client_name, client_email, client_phone, booking_date, booking_time, status, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        s2_id,
        "Sofia Fernandes",
        "sofia.fernandes@health.pt",
        "+351 919 888 777",
        "2026-09-10",
        "14:30",
        "Confirmado",
        "Primeira consulta de avaliação.",
        now
    ))

    cursor.execute("""
    INSERT INTO bookings (service_id, client_name, client_email, client_phone, booking_date, booking_time, status, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        s3_id,
        "Tiago Ramos",
        "tiago.ramos@email.com",
        "+351 961 222 333",
        "2026-09-11",
        "11:15",
        "Pendente",
        "Cliente habitual.",
        now
    ))

    conn.commit()
    conn.close()
    print("[Database OK] bookings.db criada e populada com serviços e marcações iniciais.")

if __name__ == '__main__':
    init_db()
