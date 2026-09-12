import sqlite3
import os
import uuid

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certicraft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        nif TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        organization TEXT NOT NULL DEFAULT 'Particular',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        background_theme TEXT NOT NULL DEFAULT 'Púrpura & Magenta',
        font_style TEXT NOT NULL DEFAULT 'Inter / Serif Classic',
        border_style TEXT NOT NULL DEFAULT 'Moldura Dourada Dupla',
        issuer_name TEXT NOT NULL,
        issuer_title TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Ativo'
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_id INTEGER NOT NULL,
        template_id INTEGER NOT NULL,
        course_title TEXT NOT NULL,
        verification_code TEXT UNIQUE NOT NULL,
        qr_code_url TEXT NOT NULL,
        issue_date TEXT NOT NULL,
        expiry_date TEXT,
        grade_achieved REAL DEFAULT 100.0,
        pdf_status TEXT NOT NULL DEFAULT 'Pronto para Download',
        status TEXT NOT NULL DEFAULT 'Válido',
        FOREIGN KEY (recipient_id) REFERENCES recipients (id) ON DELETE CASCADE,
        FOREIGN KEY (template_id) REFERENCES templates (id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verification_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        certificate_id INTEGER NOT NULL,
        verification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        verified_by_ip TEXT NOT NULL DEFAULT '127.0.0.1',
        is_valid INTEGER NOT NULL DEFAULT 1,
        notes TEXT,
        FOREIGN KEY (certificate_id) REFERENCES certificates (id) ON DELETE CASCADE
    )
    ''')

    # Seed initial data if empty
    cursor.execute('SELECT COUNT(*) FROM recipients')
    if cursor.fetchone()[0] == 0:
        # Seed Recipients
        recipients_data = [
            ("Dra. Sofia Maria Mendonça", "sofia.mendonca@empresa.pt", "239847109", "+351 912 345 678", "TechCorp Portugal"),
            ("Eng. João Carlos Ribeiro", "j.ribeiro@netcabo.pt", "198765432", "+351 934 567 890", "Inovação Digital SA"),
            ("Ana Beatriz Fonseca", "ana.fonseca@sapo.pt", "287654321", "+351 965 432 109", "Academia de Formação Lisboa"),
            ("Dr. Miguel Ângelo Neves", "m.neves@veterinaria.pt", "210987654", "+351 927 890 123", "Instituto de Saúde & Ciência"),
            ("Mariana Silva Santos", "mariana.santos@gmail.com", "254123987", "+351 918 273 645", "Particular")
        ]
        cursor.executemany('''
            INSERT INTO recipients (full_name, email, nif, phone, organization)
            VALUES (?, ?, ?, ?, ?)
        ''', recipients_data)

        # Seed Templates
        templates_data = [
            ("Diploma de Excelência Executiva", "Executivo & Pós-Graduação", "Púrpura & Dourado", "Serif Elegant", "Moldura Real Dourada", "Prof. Dr. Alexandre Fontes", "Diretor Pedagógico", "Ativo"),
            ("Certificado de Conclusão Técnica", "Formação Profissional", "Magenta Moderno", "Inter Clean", "Borda Geométrica Minimalista", "Eng.ª Maria Inês Barreto", "Coordenadora de Formação", "Ativo"),
            ("Certificado de Participação em Workshop", "Eventos & Seminários", "Violeta & Azul", "Sans-Serif Modern", "Borda Suave Dupla", "Dr. Tiago Albuquerque", "Presidente do Comité", "Ativo")
        ]
        cursor.executemany('''
            INSERT INTO templates (title, category, background_theme, font_style, border_style, issuer_name, issuer_title, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', templates_data)

        # Seed Certificates
        certs_data = [
            (1, 1, "Pós-Graduação em Gestão de Projetos & Inteligência Artificial", "CERT-2026-PT-984210", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=CERT-2026-PT-984210", "2026-09-01", "Sem Validade", 98.5, "Pronto para Download", "Válido"),
            (2, 2, "Curso Intensivo de Full-Stack Python & Flask Development", "CERT-2026-PT-442190", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=CERT-2026-PT-442190", "2026-09-03", "Sem Validade", 95.0, "Pronto para Download", "Válido"),
            (3, 3, "Workshop Internacional de Design Systems & Figma UI/UX", "CERT-2026-PT-771234", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=CERT-2026-PT-771234", "2026-09-05", "Sem Validade", 100.0, "Pronto para Download", "Válido"),
            (4, 1, "Certificação Profissional em Segurança da Informação & RGPD", "CERT-2026-PT-332190", "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=CERT-2026-PT-332190", "2026-09-10", "2029-09-10", 92.0, "Pronto para Download", "Válido")
        ]
        cursor.executemany('''
            INSERT INTO certificates (recipient_id, template_id, course_title, verification_code, qr_code_url, issue_date, expiry_date, grade_achieved, pdf_status, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', certs_data)

        # Seed Verification Logs
        logs_data = [
            (1, "192.168.1.50", 1, "Verificação bem-sucedida via Código QR."),
            (2, "192.168.1.75", 1, "Consulta de autenticidade realizada pelo empregador."),
            (3, "127.0.0.1", 1, "Validação de código único de verificação.")
        ]
        cursor.executemany('''
            INSERT INTO verification_logs (certificate_id, verified_by_ip, is_valid, notes)
            VALUES (?, ?, ?, ?)
        ''', logs_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados CertiCraft AI inicializada com sucesso!")
