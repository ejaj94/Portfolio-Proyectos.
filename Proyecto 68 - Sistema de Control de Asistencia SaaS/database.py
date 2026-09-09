import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'timepulse.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_code TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        position TEXT NOT NULL,
        shift_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Ativo',
        created_at TEXT NOT NULL
    )
    """)

    # 2. Work Schedules / Shifts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        grace_minutes INTEGER DEFAULT 15,
        target_hours REAL DEFAULT 8.0
    )
    """)

    # 3. Attendance Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,
        clock_in TEXT,
        clock_out TEXT,
        delay_minutes INTEGER DEFAULT 0,
        total_hours REAL DEFAULT 0.0,
        overtime_hours REAL DEFAULT 0.0,
        status TEXT DEFAULT 'No Horário',
        notes TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
    """)

    # Seed initial data if database is empty
    cursor.execute("SELECT COUNT(*) FROM shifts")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        today_str = date.today().strftime("%Y-%m-%d")
        yesterday_str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Seed Shifts
        shifts_data = [
            ("Turno Geral Padrão", "09:00", "18:00", 15, 8.0),
            ("Turno Matutino Adiantado", "08:00", "17:00", 10, 8.0),
            ("Turno Noturno / Flexível", "14:00", "23:00", 15, 8.0)
        ]
        cursor.executemany("""
        INSERT INTO shifts (name, start_time, end_time, grace_minutes, target_hours)
        VALUES (?, ?, ?, ?, ?)
        """, shifts_data)

        # Seed Employees
        employees_data = [
            ("EMP-101", "Eng. Carlos Ferreira", "carlos.ferreira@ejajtech.com", "Engenharia & Software", "Senior Lead Architect", 1, "Ativo", now_str),
            ("EMP-102", "Mariana Magalhães", "mariana.magalhaes@ejajtech.com", "Recursos Humanos", "People Ops Specialist", 1, "Ativo", now_str),
            ("EMP-103", "Gonçalo Ribeiro", "goncalo.ribeiro@ejajtech.com", "Engenharia & Software", "Full-Stack Developer", 1, "Ativo", now_str),
            ("EMP-104", "Daniela Alvim", "daniela.alvim@ejajtech.com", "Design & UX", "Senior UI/UX Designer", 2, "Ativo", now_str),
            ("EMP-105", "Vítor Hugo Santos", "vitor.santos@ejajtech.com", "Suporte & DevOps", "Cloud Systems Engineer", 3, "Ativo", now_str)
        ]
        cursor.executemany("""
        INSERT INTO employees (emp_code, full_name, email, department, position, shift_id, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, employees_data)

        # Seed Attendance Logs for Yesterday
        logs_yesterday = [
            (1, yesterday_str, "08:52", "18:05", 0, 8.2, 0.2, "No Horário", "Entrada antes do horário"),
            (2, yesterday_str, "09:05", "18:00", 0, 8.0, 0.0, "No Horário", "Dentro da tolerância"),
            (3, yesterday_str, "09:28", "18:30", 28, 8.0, 0.0, "Atrasado", "Atraso no trânsito de Lisboa"),
            (4, yesterday_str, "07:58", "17:02", 0, 8.0, 0.0, "No Horário", "Turno matutino cumprido"),
            (5, yesterday_str, "14:00", "23:15", 0, 8.25, 0.25, "No Horário", "Suporte noturno estendido")
        ]
        cursor.executemany("""
        INSERT INTO attendance_logs (employee_id, log_date, clock_in, clock_out, delay_minutes, total_hours, overtime_hours, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, logs_yesterday)

        # Seed Attendance Logs for Today
        logs_today = [
            (1, today_str, "08:50", "18:00", 0, 8.1, 0.1, "No Horário", "Ponto registado via Terminal"),
            (2, today_str, "08:58", None, 0, 0.0, 0.0, "No Horário", "Em trabalho"),
            (3, today_str, "09:35", None, 35, 0.0, 0.0, "Atrasado", "Atraso registado de 35 min"),
            (4, today_str, "07:55", "17:00", 0, 8.0, 0.0, "No Horário", "Turno concluído")
        ]
        cursor.executemany("""
        INSERT INTO attendance_logs (employee_id, log_date, clock_in, clock_out, delay_minutes, total_hours, overtime_hours, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, logs_today)

    conn.commit()
    conn.close()
    print("[Database OK] timepulse.db inicializada com dados de assiduidade e turnos.")

if __name__ == '__main__':
    init_db()
