import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'mail_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: Contacts (Contactos & Subscritores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            company TEXT,
            status TEXT DEFAULT 'Ativo',
            tags TEXT DEFAULT 'Lead',
            subscribed_at TEXT NOT NULL
        )
    ''')

    # Table: Lists (Listas de Segmentação)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            member_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')

    # Table: Relationship Contacts <-> Lists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_list_rel (
            contact_id INTEGER,
            list_id INTEGER,
            PRIMARY KEY (contact_id, list_id),
            FOREIGN KEY (contact_id) REFERENCES contacts (id),
            FOREIGN KEY (list_id) REFERENCES lists (id)
        )
    ''')

    # Table: Templates (Plantillas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'Newsletter',
            subject_default TEXT NOT NULL,
            content_html TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Table: Campaigns (Campañas & Programación)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            list_id INTEGER NOT NULL,
            template_id INTEGER,
            status TEXT DEFAULT 'Rascunho',
            scheduled_at TEXT,
            sent_at TEXT,
            recipients_count INTEGER DEFAULT 0,
            opens_count INTEGER DEFAULT 0,
            clicks_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (list_id) REFERENCES lists (id),
            FOREIGN KEY (template_id) REFERENCES templates (id)
        )
    ''')

    # Seed Lists if empty
    cursor.execute('SELECT COUNT(*) FROM lists')
    if cursor.fetchone()[0] == 0:
        seed_lists = [
            ('Clientes VIP Enterprise', 'Lista exclusiva para grandes contas e parceiros estratégicos', 4, '2026-09-01 10:00'),
            ('Leads Qualificados SaaS', 'Contactos capturados na landing page e webinars', 5, '2026-09-02 11:30'),
            ('Newsletter Semanal EJAJ TECH', 'Subscritores do digest semanal de tecnologia e inovação', 6, '2026-09-03 14:00')
        ]

        cursor.executemany('''
            INSERT INTO lists (name, description, member_count, created_at)
            VALUES (?, ?, ?, ?)
        ''', seed_lists)

    # Seed Contacts if empty
    cursor.execute('SELECT COUNT(*) FROM contacts')
    if cursor.fetchone()[0] == 0:
        seed_contacts = [
            ('Dra. Catarina Vasconcelos', 'catarina.v@empresa.pt', 'Vasconcelos & Associados', 'Ativo', 'VIP,Cliente', '2026-09-05 09:30'),
            ('Eng. Miguel Ângelo Silva', 'miguel.silva@techportugal.pt', 'Tech Portugal SA', 'Ativo', 'Lead,SaaS', '2026-09-06 10:15'),
            ('Dr. Afonso Henriques', 'afonso@nortenegocios.pt', 'Norte Negócios Lda', 'Ativo', 'Newsletter', '2026-09-07 11:00'),
            ('Sofia Isabel Guimarães', 'sofia.g@startupcenter.pt', 'StartUp Center', 'Ativo', 'VIP,SaaS', '2026-09-08 14:20'),
            ('Dr. Rodrigo Simões', 'rodrigo.simoes@consulting.pt', 'Simões Consulting', 'Ativo', 'Lead,Newsletter', '2026-09-09 16:45'),
            ('Marta Teresa Faria', 'marta.faria@inovagroup.pt', 'InovaGroup PT', 'Ativo', 'Newsletter', '2026-09-10 09:10')
        ]

        cursor.executemany('''
            INSERT INTO contacts (name, email, company, status, tags, subscribed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_contacts)

        # Populate relations
        cursor.executemany('''
            INSERT OR IGNORE INTO contact_list_rel (contact_id, list_id)
            VALUES (?, ?)
        ''', [(1, 1), (4, 1), (2, 2), (5, 2), (3, 3), (6, 3), (1, 3), (2, 3)])

    # Seed Templates if empty
    cursor.execute('SELECT COUNT(*) FROM templates')
    if cursor.fetchone()[0] == 0:
        seed_templates = [
            ('Lançamento de Nova Funcionalidade SaaS', 'Produto', 'Descubra a nova revolução na gestão do seu negócio com a EJAJ TECH!', '<p>Olá {{NOME}},</p><p>Temos o prazer de apresentar a nova atualização da nossa plataforma SaaS.</p><p>Abraço,<br>EJAJ TECH</p>', '2026-09-01 12:00'),
            ('Digest Semanal de Inovação & Tecnologia', 'Newsletter', 'O seu resumo semanal sobre inteligência artificial e negócios', '<p>Olá {{NOME}},</p><p>Aqui estão as principais notícias de tecnologia desta semana.</p><p>Atenciosamente,<br>Equipa EJAJ TECH</p>', '2026-09-02 15:30'),
            ('Convite Exclusivo para Webinar VIP', 'Evento', 'Convite VIP: Como escalar o seu negócio com automação em 2026', '<p>Estimado(a) {{NOME}},</p><p>Gostaríamos de o convidar para o nosso próximo webinar exclusivo.</p><p>Com os melhores cumprimentos,<br>Enmanuel Jimenez</p>', '2026-09-03 16:00')
        ]

        cursor.executemany('''
            INSERT INTO templates (title, category, subject_default, content_html, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_templates)

    # Seed Campaigns if empty
    cursor.execute('SELECT COUNT(*) FROM campaigns')
    if cursor.fetchone()[0] == 0:
        seed_campaigns = [
            ('Campanha Lançamento Q3', 'Lançamento Exclusivo MailCraft AI', 1, 1, 'Enviada', '2026-09-10 10:00', '2026-09-10 10:05', 4, 3, 2, '2026-09-10 09:30'),
            ('Newsletter Digest Edição #42', 'Digest Semanal de Inovação', 3, 2, 'Enviada', '2026-09-12 14:00', '2026-09-12 14:02', 6, 5, 4, '2026-09-12 13:45'),
            ('Webinar VIP Automação Comercial', 'Convite Exclusivo Webinar VIP', 2, 3, 'Programada', '2026-09-15 11:00', None, 5, 0, 0, '2026-09-13 16:00')
        ]

        cursor.executemany('''
            INSERT INTO campaigns (name, subject, list_id, template_id, status, scheduled_at, sent_at, recipients_count, opens_count, clicks_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_campaigns)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados mail_craft.db inicializada com sucesso!")
