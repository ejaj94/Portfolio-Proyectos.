import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'academycraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        nif TEXT UNIQUE NOT NULL,
        birth_date TEXT NOT NULL,
        guardian_name TEXT,
        status TEXT NOT NULL DEFAULT 'Ativo',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        nif TEXT UNIQUE NOT NULL,
        qualification TEXT NOT NULL,
        hourly_rate REAL NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        duration_hours INTEGER NOT NULL,
        price REAL NOT NULL,
        teacher_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Ativo',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES teachers (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        room TEXT NOT NULL,
        class_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        summary TEXT,
        status TEXT NOT NULL DEFAULT 'Agendada',
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Presente',
        notes TEXT,
        FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_date TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pago',
        nif_invoice TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        evaluation_name TEXT NOT NULL,
        evaluation_date TEXT NOT NULL,
        score REAL NOT NULL,
        max_score REAL NOT NULL DEFAULT 20.0,
        comments TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM students')
    if cursor.fetchone()[0] == 0:
        # Seed Teachers
        teachers_data = [
            ("Prof. Dra. Maria Inês Barreto", "m.barreto@academia.pt", "+351 913 245 876", "219847109", "Doutoramento em Matemática Aplicada (ULisboa)", 35.00, "Coordenadora do departamento de Exames Nacionais."),
            ("Prof. Eng. Gonçalo Vasconcelos", "g.vasconcelos@academia.pt", "+351 932 109 876", "198745123", "Mestrado em Engenharia de Software (FEUP)", 40.00, "Especialista em Python, Django e IA."),
            ("Prof.ª Lic. Beatriz Castelo Branco", "b.castelo@academia.pt", "+351 965 432 987", "287654129", "Certificação Cambridge CELTA / C2 Proficiency", 30.00, "Formadora de preparação para exames IELTS e Cambridge."),
            ("Prof. Dr. Alexandre Fontes", "a.fontes@academia.pt", "+351 927 654 321", "210987345", "Doutoramento em Física Quântica (UC)", 38.00, "Leciona preparação para os exames nacionais do secundário.")
        ]
        cursor.executemany('''
            INSERT INTO teachers (name, email, phone, nif, qualification, hourly_rate, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', teachers_data)

        # Seed Students
        students_data = [
            ("Tomás Afonso Ferreira", "tomas.ferreira@estudante.pt", "+351 919 876 543", "254987123", "2007-04-12", "Fernando Ferreira", "Ativo", "Preparação para o exame nacional de Matemática A."),
            ("Inês Filipa Magalhães", "ines.magalhaes@gmail.com", "+351 934 123 789", "267890123", "2006-11-28", "Teresa Magalhães", "Ativo", "Inscrita no curso intensivo de Inglês C1."),
            ("Martim José Coimbra", "martim.coimbra@sapo.pt", "+351 961 234 567", "289123456", "2005-09-05", "Encarregado Autónomo", "Ativo", "Frequenta o módulo de Programação Python & IA."),
            ("Carolina Santos Paiva", "carolina.paiva@outloo.pt", "+351 925 876 123", "245678901", "2008-02-17", "Manuel Santos Paiva", "Ativo", "Apoio escolar a Física e Química A."),
            ("Diogo Alexandre Henriques", "diogo.henriques@netcabo.pt", "+351 918 345 678", "234567890", "2004-07-22", "Encarregado Autónomo", "Ativo", "Frequenta o programa de Design UI/UX."),
            ("Matilde Sofia Ramos", "matilde.ramos@gmail.com", "+351 967 890 123", "278901234", "2007-12-01", "Helena Ramos", "Ativo", "Excelente aproveitamento académico.")
        ]
        cursor.executemany('''
            INSERT INTO students (name, email, phone, nif, birth_date, guardian_name, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', students_data)

        # Seed Courses
        courses_data = [
            ("Programação Python & Inteligência Artificial", "CRS-PY-101", "Tecnologia & Programação", 60, 180.00, 2, "Ativo"),
            ("Matemática A - Preparação para Exame Nacional", "CRS-MAT-201", "Ensino Secundário", 90, 220.00, 1, "Ativo"),
            ("Inglês C1 Advanced & Preparação Cambridge", "CRS-ENG-301", "Línguas & Certificações", 50, 150.00, 3, "Ativo"),
            ("Física e Química A - Apoio Intensivo", "CRS-FQ-202", "Ensino Secundário", 80, 200.00, 4, "Ativo")
        ]
        cursor.executemany('''
            INSERT INTO courses (name, code, category, duration_hours, price, teacher_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', courses_data)

        # Seed Classes
        classes_data = [
            (1, "Introdução às Estruturas de Dados e Algoritmos", "Sala 101 - Laboratório Computadores", "2026-09-15", "18:00", "20:00", "Conceitos fundamentais de listas, dicionários e complexidade de algoritmos.", "Concluída"),
            (1, "Desenvolvimento de APIs RESTful com Flask", "Sala 101 - Laboratório Computadores", "2026-09-17", "18:00", "20:00", "Criação de rotas, manipulação de JSON e integração com bases de dados SQLite.", "Agendada"),
            (2, "Geometria Analítica e Funções Trigonometria", "Sala 204 - Auditório Principal", "2026-09-16", "17:30", "19:30", "Resolução de exercícios práticos dos exames nacionais dos últimos 5 anos.", "Agendada"),
            (3, "Writing & Essay Preparation for Cambridge C1", "Sala 302 - Sala Idiomas", "2026-09-18", "16:00", "18:00", "Análise de ensaios argumentativos e expansão de vocabulário académico.", "Agendada"),
            (4, "Termodinâmica e Mecânica de Fluidos", "Laboratório de Física", "2026-09-19", "10:00", "12:00", "Realização de experiências práticas e medições laboratoriais.", "Agendada")
        ]
        cursor.executemany('''
            INSERT INTO classes (course_id, title, room, class_date, start_time, end_time, summary, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', classes_data)

        # Seed Attendance
        attendance_data = [
            (1, 3, "Presente", "Participou ativamente na resolução dos exercícios de Python."),
            (1, 5, "Presente", "Excelente desempenho no laboratório."),
            (1, 1, "Falta Justificada", "Apresentou atestado médico por doença."),
            (1, 2, "Presente", "Chegou 5 minutos após o início da aula.")
        ]
        cursor.executemany('''
            INSERT INTO attendance (class_id, student_id, status, notes)
            VALUES (?, ?, ?, ?)
        ''', attendance_data)

        # Seed Payments
        payments_data = [
            (1, 2, 220.00, "2026-09-01", "MB WAY", "Pago", "254987123"),
            (2, 3, 150.00, "2026-09-02", "Multibanco", "Pago", "267890123"),
            (3, 1, 180.00, "2026-09-03", "Cartão de Crédito", "Pago", "289123456"),
            (4, 4, 200.00, "2026-09-05", "Transferência Bancária", "Pago", "245678901"),
            (5, 1, 180.00, "2026-09-10", "MB WAY", "Pendente", "234567890")
        ]
        cursor.executemany('''
            INSERT INTO payments (student_id, course_id, amount, payment_date, payment_method, status, nif_invoice)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', payments_data)

        # Seed Grades
        grades_data = [
            (1, 2, "Teste Prático 1 - Álgebra & Geometria", "2026-08-28", 18.5, 20.0, "Excelente domínio dos conceitos teóricos e resolução rigorosa."),
            (2, 3, "Mock Exam - Cambridge C1 Reading & Use of English", "2026-08-30", 17.0, 20.0, "Ótimo vocabulário, recomendada atenção na gestão do tempo."),
            (3, 1, "Projeto 1 - Aplicação Web Flask com SQLite", "2026-09-05", 19.2, 20.0, "Projeto sobressalente com arquitetura limpa e código bem documentado."),
            (4, 4, "Teste Diagnóstico - Física e Química A", "2026-09-02", 15.8, 20.0, "Bom raciocínio lógico nas questões de termodinâmica.")
        ]
        cursor.executemany('''
            INSERT INTO grades (student_id, course_id, evaluation_name, evaluation_date, score, max_score, comments)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', grades_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados AcademyCraft AI inicializada com sucesso!")
