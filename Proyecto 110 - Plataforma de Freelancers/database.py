import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'freelance_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Freelancers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS freelancers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            hourly_rate REAL NOT NULL,
            rating REAL NOT NULL,
            reviews_count INTEGER NOT NULL,
            bio TEXT NOT NULL,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            avatar_icon TEXT NOT NULL
        )
    ''')
    
    # Services/Gigs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            freelancer_id INTEGER NOT NULL,
            freelancer_name TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            delivery_days INTEGER NOT NULL,
            rating REAL NOT NULL,
            thumbnail_icon TEXT NOT NULL
        )
    ''')

    # Proposals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_title TEXT NOT NULL,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            bid_amount REAL NOT NULL,
            delivery_days INTEGER NOT NULL,
            cover_letter TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            message_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Reviews Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            freelancer_name TEXT NOT NULL,
            client_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM freelancers')
    if cursor.fetchone()[0] == 0:
        seed_freelancers = [
            ('Angel Rafael', 'Engenheiro de IA & Developer Full Stack', 'Desenvolvimento Web', 65.00, 5.0, 48, 'Especialista em construir aplicações web escaláveis, microsserviços e integração de motores de Inteligência Artificial.', 'Python, Flask, React, Tailwind, SQLite, AI', 'Lisboa, Portugal', 'fa-user-astronaut'),
            ('Beatriz Lima', 'UI/UX Designer & Product Designer', 'Design & UX', 45.00, 4.9, 36, 'Especialista em criar interfaces modernas, design systems responsivos e wireframes focados em conversão.', 'Figma, UI/UX, Design System, Tailwind', 'Porto, Portugal', 'fa-palette'),
            ('Carlos Eduardo', 'Especialista em DevOps & Cloud', 'DevOps & Cloud', 55.00, 4.8, 29, 'Automação de CI/CD, gestão de infraestrutura em nuvem, Docker, Kubernetes e segurança de servidores.', 'Docker, AWS, Kubernetes, Linux, Nginx', 'Coimbra, Portugal', 'fa-server'),
            ('Daniela Rocha', 'Copywriter & Gestora de Conteúdos', 'Marketing & Redação', 35.00, 4.9, 52, 'Criação de artigos SEO, textos comerciais de alta conversão, e-mail marketing e estratégias de conteúdo.', 'SEO, Copywriting, Content, Marketing', 'Faro, Portugal', 'fa-pen-nib')
        ]
        cursor.executemany('''
            INSERT INTO freelancers (name, title, category, hourly_rate, rating, reviews_count, bio, skills, location, avatar_icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_freelancers)

        seed_services = [
            (1, 'Angel Rafael', 'Desenvolvimento de Aplicação Web SaaS Completa', 'Desenvolvimento Web', 450.00, 3, 5.0, 'fa-laptop-code'),
            (1, 'Angel Rafael', 'Integração de APIs de IA & Chatbots em Python', 'Desenvolvimento Web', 280.00, 2, 5.0, 'fa-robot'),
            (2, 'Beatriz Lima', 'Design UI/UX Completo de Website / App Mobile', 'Design & UX', 350.00, 4, 4.9, 'fa-wand-magic-sparkles'),
            (3, 'Carlos Eduardo', 'Configuração de Servidor & CI/CD Pipeline', 'DevOps & Cloud', 220.00, 2, 4.8, 'fa-terminal'),
            (4, 'Daniela Rocha', 'Redação de Copy Comercial & Landing Page SEO', 'Marketing & Redação', 150.00, 1, 4.9, 'fa-file-lines')
        ]
        cursor.executemany('''
            INSERT INTO services (freelancer_id, freelancer_name, title, category, price, delivery_days, rating, thumbnail_icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_services)

        seed_proposals = [
            ('Desenvolvimento de Aplicação Web SaaS Completa', 'Gonçalo Neves', 'goncalo@empresa.pt', 420.00, 3, 'Gostaria de contratar para o desenvolvimento de um portal SaaS de agendamento.', 'Accepted'),
            ('Design UI/UX Completo de Website / App Mobile', 'Marta Silva', 'marta@agency.io', 350.00, 4, 'Precisamos de um redesign completo da nossa plataforma e landing page.', 'Pending')
        ]
        cursor.executemany('''
            INSERT INTO proposals (service_title, client_name, client_email, bid_amount, delivery_days, cover_letter, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_proposals)

        seed_messages = [
            ('Gonçalo Neves', 'Angel Rafael', 'Olá Angel, vimos o teu portfólio e ficámos impressionados com a velocidade dos projetos!'),
            ('Angel Rafael', 'Gonçalo Neves', 'Olá Gonçalo! Muito obrigado. Em que tipo de projeto estão a trabalhar atualmente?')
        ]
        cursor.executemany('''
            INSERT INTO messages (sender_name, receiver_name, message_text)
            VALUES (?, ?, ?)
        ''', seed_messages)

        seed_reviews = [
            ('Angel Rafael', 'Gonçalo Neves', 5, 'Excelente profissional! Entrega extremamente rápida e código super limpo.'),
            ('Beatriz Lima', 'Marta Silva', 5, 'O design ficou incrível. Superou todas as expetativas da nossa equipa.')
        ]
        cursor.executemany('''
            INSERT INTO reviews (freelancer_name, client_name, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', seed_reviews)

        conn.commit()
    conn.close()

def add_proposal(service_title, client_name, client_email, bid_amount, delivery_days, cover_letter):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO proposals (service_title, client_name, client_email, bid_amount, delivery_days, cover_letter, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
    ''', (service_title, client_name, client_email, bid_amount, delivery_days, cover_letter))
    prop_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prop_id

def add_message(sender_name, receiver_name, message_text):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (sender_name, receiver_name, message_text)
        VALUES (?, ?, ?)
    ''', (sender_name, receiver_name, message_text))
    msg_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return msg_id

def add_review(freelancer_name, client_name, rating, comment):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reviews (freelancer_name, client_name, rating, comment)
        VALUES (?, ?, ?, ?)
    ''', (freelancer_name, client_name, rating, comment))
    conn.commit()
    conn.close()

def get_all_freelancers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM freelancers ORDER BY rating DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_services():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_proposals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proposals ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_reviews():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == '__main__':
    init_db()
    print("Base de dados freelance_craft.db inicializada com sucesso!")
