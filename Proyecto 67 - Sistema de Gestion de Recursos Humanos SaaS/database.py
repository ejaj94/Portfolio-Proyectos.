import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'hr_talent.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Departments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manager_name TEXT NOT NULL,
        budget REAL DEFAULT 0.0,
        color TEXT DEFAULT '#2563EB',
        created_at TEXT NOT NULL
    )
    """)

    # 2. Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL,
        status TEXT DEFAULT 'Ativo',
        hire_date TEXT NOT NULL,
        avatar_color TEXT DEFAULT '#2563EB',
        FOREIGN KEY (department_id) REFERENCES departments (id)
    )
    """)

    # 3. Vacations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        days_count INTEGER NOT NULL,
        status TEXT DEFAULT 'Pendente',
        reason TEXT,
        requested_at TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
    """)

    # 4. Absences Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS absences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        absence_type TEXT NOT NULL,
        status TEXT DEFAULT 'Justificado',
        notes TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
    """)

    # 5. Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        clock_in TEXT,
        clock_out TEXT,
        total_hours REAL DEFAULT 0.0,
        status TEXT DEFAULT 'Presente',
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
    """)

    # 6. Documents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        file_url TEXT NOT NULL,
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
    """)

    # Seed Initial Data if empty
    cursor.execute("SELECT COUNT(*) FROM departments")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        today_str = date.today().strftime("%Y-%m-%d")

        # Seed Departments
        departments_data = [
            ("Engenharia & Software", "Eng. Ricardo Alves", 185000.0, "#2563EB", now_str),
            ("Recursos Humanos & Talento", "Dra. Sofia Martins", 95000.0, "#F43F5E", now_str),
            ("Marketing & Design", "Mariana Costa", 80000.0, "#60A5FA", now_str),
            ("Vendas & Expansão", "Carlos Eduardo", 120000.0, "#10B981", now_str)
        ]
        cursor.executemany("""
        INSERT INTO departments (name, manager_name, budget, color, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, departments_data)

        # Seed Employees
        employees_data = [
            ("Dr. Alexandre Mendes", "alexandre.mendes@ejajtech.com", "+351 912 345 001", 1, "Senior Full-Stack Engineer", 3800.0, "Ativo", "2023-01-15", "#2563EB"),
            ("Beatriz Fonseca", "beatriz.fonseca@ejajtech.com", "+351 913 456 002", 2, "HR Specialist & Recruiter", 2400.0, "Ativo", "2023-04-10", "#F43F5E"),
            ("Diogo Carvalhal", "diogo.carvalhal@ejajtech.com", "+351 914 567 003", 1, "DevOps & Cloud Architect", 4100.0, "Ativo", "2022-11-01", "#60A5FA"),
            ("Inês Guerreiro", "ines.guerreiro@ejajtech.com", "+351 915 678 004", 3, "UI/UX Product Designer", 2700.0, "Ativo", "2024-02-01", "#EC4899"),
            ("Tiago Neves", "tiago.neves@ejajtech.com", "+351 916 789 005", 4, "Enterprise Account Executive", 3200.0, "Ativo", "2023-08-15", "#10B981"),
            ("Carolina Rocha", "carolina.rocha@ejajtech.com", "+351 917 890 006", 2, "People Operations Lead", 2900.0, "De Férias", "2022-05-20", "#8B5CF6")
        ]
        cursor.executemany("""
        INSERT INTO employees (full_name, email, phone, department_id, position, salary, status, hire_date, avatar_color)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, employees_data)

        # Seed Vacations
        next_week = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
        two_weeks = (date.today() + timedelta(days=12)).strftime("%Y-%m-%d")
        
        vacations_data = [
            (6, today_str, next_week, 7, "Aprovado", "Férias de Verão Planeadas", now_str),
            (1, next_week, two_weeks, 7, "Pendente", "Descanso Familiar Anual", now_str),
            (4, (date.today() + timedelta(days=20)).strftime("%Y-%m-%d"), (date.today() + timedelta(days=25)).strftime("%Y-%m-%d"), 5, "Pendente", "Viagem Pessoal", now_str)
        ]
        cursor.executemany("""
        INSERT INTO vacations (employee_id, start_date, end_date, days_count, status, reason, requested_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, vacations_data)

        # Seed Absences
        absences_data = [
            (2, (date.today() - timedelta(days=3)).strftime("%Y-%m-%d"), "Doença", "Justificado", "Consulta médica de urgência"),
            (5, (date.today() - timedelta(days=10)).strftime("%Y-%m-%d"), "Assunto Pessoal", "Justificado", "Tratamento de assuntos burocráticos")
        ]
        cursor.executemany("""
        INSERT INTO absences (employee_id, date, absence_type, status, notes)
        VALUES (?, ?, ?, ?, ?)
        """, absences_data)

        # Seed Attendance for Today
        attendance_data = [
            (1, today_str, "08:55", "18:00", 8.5, "Presente"),
            (2, today_str, "09:02", "18:05", 8.0, "Presente"),
            (3, today_str, "08:45", "17:50", 8.2, "Presente"),
            (4, today_str, "09:15", "18:15", 8.0, "Atrasado"),
            (5, today_str, "09:00", "18:00", 8.0, "Presente")
        ]
        cursor.executemany("""
        INSERT INTO attendance (employee_id, date, clock_in, clock_out, total_hours, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, attendance_data)

        # Seed Documents
        docs_data = [
            (1, "Contrato de Trabalho Individual - Alexandre Mendes", "Contrato", "/docs/contrato_alexandre.pdf", now_str),
            (1, "Cartão de Cidadão & NIF", "Identificação", "/docs/cc_alexandre.pdf", now_str),
            (3, "Certificado AWS Solutions Architect - Diogo Carvalhal", "Certificado", "/docs/aws_diogo.pdf", now_str),
            (2, "Contrato de Trabalho - Beatriz Fonseca", "Contrato", "/docs/contrato_beatriz.pdf", now_str)
        ]
        cursor.executemany("""
        INSERT INTO documents (employee_id, title, category, file_url, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
        """, docs_data)

    conn.commit()
    conn.close()
    print("[Database OK] hr_talent.db inicializada com dados seed de Recursos Humanos.")

if __name__ == '__main__':
    init_db()
