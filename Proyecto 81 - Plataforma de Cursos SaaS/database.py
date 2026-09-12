import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'learncraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL DEFAULT 'Aluno',
        nif TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Ativo',
        joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        instructor_id INTEGER NOT NULL,
        level TEXT NOT NULL,
        price REAL NOT NULL,
        total_duration_min INTEGER NOT NULL,
        thumbnail_emoji TEXT NOT NULL DEFAULT '🎥',
        status TEXT NOT NULL DEFAULT 'Publicado',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (instructor_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        module_number INTEGER NOT NULL,
        lesson_order INTEGER NOT NULL,
        duration_min INTEGER NOT NULL,
        is_free_preview INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER NOT NULL,
        video_title TEXT NOT NULL,
        video_url TEXT NOT NULL,
        video_quality TEXT NOT NULL DEFAULT '1080p Full HD',
        resolution TEXT NOT NULL DEFAULT '1920x1080',
        stream_type TEXT NOT NULL DEFAULT 'HLS / MP4',
        views_count INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        completion_pct REAL NOT NULL DEFAULT 0.0,
        last_watched_timestamp TEXT NOT NULL DEFAULT '00:00',
        status TEXT NOT NULL DEFAULT 'Em Curso',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        certificate_code TEXT UNIQUE NOT NULL,
        issue_date TEXT NOT NULL,
        grade_achieved REAL NOT NULL DEFAULT 100.0,
        status TEXT NOT NULL DEFAULT 'Válido',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_date TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Concluído',
        transaction_id TEXT UNIQUE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
    )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Seed Users
        users_data = [
            ("Prof. Eng. Tiago Albuquerque", "tiago.albuquerque@learncraft.pt", "Instrutor", "219847001", "+351 912 345 678", "Ativo"),
            ("Dra. Beatriz Vasconcelos", "beatriz.vasconcelos@learncraft.pt", "Instrutor", "287654002", "+351 934 567 890", "Ativo"),
            ("Dr. Diogo Ribeiro Sanches", "diogo.sanches@learncraft.pt", "Instrutor", "210987003", "+351 965 432 109", "Ativo"),
            ("Gonçalo Afonso Mendes", "goncalo.mendes@email.pt", "Aluno", "254987111", "+351 918 765 432", "Ativo"),
            ("Inês Maria Carvalho", "ines.carvalho@gmail.com", "Aluno", "267890222", "+351 927 654 321", "Ativo"),
            ("Martim José Fonseca", "martim.fonseca@sapo.pt", "Aluno", "289123333", "+351 961 234 567", "Ativo"),
            ("Carolina Santos Lima", "carolina.lima@outloo.pt", "Aluno", "245678444", "+351 932 109 876", "Ativo")
        ]
        cursor.executemany('''
            INSERT INTO users (name, email, role, nif, phone, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users_data)

        # Seed Courses
        courses_data = [
            ("Masterclass Full-Stack Python & Flask", "Desenvolvimento Web", 1, "Intermédio", 149.00, 360, "🐍", "Publicado"),
            ("Design de Interfaces UI/UX com Figma & Design Systems", "Design & Multimédia", 2, "Iniciante", 99.00, 240, "🎨", "Publicado"),
            ("Inteligência Artificial Aplicada a Negócios & Automations", "Inteligência Artificial", 1, "Avançado", 199.00, 420, "🤖", "Publicado"),
            ("Marketing Digital, Estratégia de Conteúdo & SEO", "Marketing & Vendas", 3, "Iniciante", 79.00, 180, "📈", "Publicado")
        ]
        cursor.executemany('''
            INSERT INTO courses (title, category, instructor_id, level, price, total_duration_min, thumbnail_emoji, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', courses_data)

        # Seed Lessons
        lessons_data = [
            (1, "Introdução ao Desenvolvmento Web Moderno com Python", 1, 1, 25, 1),
            (1, "Configuração do Ambiente Virtual & Estrutura Flask", 1, 2, 35, 0),
            (1, "Modelos de Dados com SQLite e SQLAlchemy", 2, 3, 45, 0),
            (1, "Construção de APIs RESTful e Autenticação JWT", 2, 4, 50, 0),
            (2, "Fundamentos de UI/UX e Princípios de Tipografia", 1, 1, 20, 1),
            (2, "Criação de Componentes Reutilizáveis no Figma", 1, 2, 40, 0),
            (3, "Prompt Engineering & Integração da API da OpenAI", 1, 1, 30, 1),
            (4, "Otimização SEO On-Page e Pesquisa de Palavras-Chave", 1, 1, 25, 1)
        ]
        cursor.executemany('''
            INSERT INTO lessons (course_id, title, module_number, lesson_order, duration_min, is_free_preview)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', lessons_data)

        # Seed Videos
        videos_data = [
            (1, "Videoaula 1.1: Visão Geral do Ecossistema Python", "https://cdn.learncraft.pt/videos/py101_01.mp4", "1080p Full HD", "1920x1080", "HLS / MP4", 1420),
            (2, "Videoaula 1.2: Instalação do Flask, Pipenv e VS Code", "https://cdn.learncraft.pt/videos/py101_02.mp4", "1080p Full HD", "1920x1080", "HLS / MP4", 1150),
            (3, "Videoaula 2.1: Schemas SQLite e Migrações de Dados", "https://cdn.learncraft.pt/videos/py101_03.mp4", "4K Ultra HD", "3840x2160", "HLS / MP4", 980),
            (4, "Videoaula 2.2: Endpoints JSON e Tratamento de Erros", "https://cdn.learncraft.pt/videos/py101_04.mp4", "1080p Full HD", "1920x1080", "HLS / MP4", 870),
            (5, "Videoaula 1.1: Teoria das Cores e Grelhas de Layout", "https://cdn.learncraft.pt/videos/ui101_01.mp4", "1080p Full HD", "1920x1080", "HLS / MP4", 2100),
            (6, "Videoaula 1.2: Auto-Layout e Variantes no Figma", "https://cdn.learncraft.pt/videos/ui101_02.mp4", "1080p Full HD", "1920x1080", "HLS / MP4", 1750),
            (7, "Videoaula 1.1: Arquitetura de Agentes Inteligentes", "https://cdn.learncraft.pt/videos/ai101_01.mp4", "4K Ultra HD", "3840x2160", "HLS / MP4", 3200),
            (8, "Videoaula 1.1: Auditoria Técnica de SEO em Websites", "https://cdn.learncraft.pt/videos/seo101_01.mp4", "1080p Full HD", "1920x1080", "HLS / MP4", 1650)
        ]
        cursor.executemany('''
            INSERT INTO videos (lesson_id, video_title, video_url, video_quality, resolution, stream_type, views_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', videos_data)

        # Seed Progress
        progress_data = [
            (4, 1, 1, 100.0, "25:00", "Concluído"),
            (4, 1, 2, 100.0, "35:00", "Concluído"),
            (4, 1, 3, 100.0, "45:00", "Concluído"),
            (4, 1, 4, 100.0, "50:00", "Concluído"),
            (5, 1, 1, 100.0, "25:00", "Concluído"),
            (5, 1, 2, 45.0, "15:45", "Em Curso"),
            (6, 2, 5, 100.0, "20:00", "Concluído"),
            (7, 3, 7, 60.0, "18:00", "Em Curso")
        ]
        cursor.executemany('''
            INSERT INTO progress (user_id, course_id, lesson_id, completion_pct, last_watched_timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', progress_data)

        # Seed Certificates
        certificates_data = [
            (4, 1, "CERT-PY-2026-98421", "2026-09-01", 98.5, "Válido"),
            (5, 2, "CERT-UI-2026-44219", "2026-09-05", 95.0, "Válido")
        ]
        cursor.executemany('''
            INSERT INTO certificates (user_id, course_id, certificate_code, issue_date, grade_achieved, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', certificates_data)

        # Seed Payments
        payments_data = [
            (4, 1, 149.00, "2026-08-25", "MB WAY", "Concluído", "TXN-PT-984210"),
            (5, 1, 149.00, "2026-08-26", "Multibanco", "Concluído", "TXN-PT-442190"),
            (6, 2, 99.00, "2026-08-28", "Cartão de Crédito", "Concluído", "TXN-PT-771234"),
            (7, 3, 199.00, "2026-09-02", "MB WAY", "Concluído", "TXN-PT-332190")
        ]
        cursor.executemany('''
            INSERT INTO payments (user_id, course_id, amount, payment_date, payment_method, status, transaction_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', payments_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados LearnCraft AI inicializada com sucesso!")
