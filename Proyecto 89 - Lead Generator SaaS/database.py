import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'lead_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: Leads
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            company TEXT,
            team_size TEXT DEFAULT '1-10',
            interest_area TEXT DEFAULT 'Consultoria TI',
            lead_score INTEGER DEFAULT 50,
            status TEXT DEFAULT 'Novo Lead',
            source TEXT DEFAULT 'Landing Page',
            created_at TEXT NOT NULL
        )
    ''')

    # Table: Follow-up Notes & Interactions (Seguimiento)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            author TEXT DEFAULT 'Gestor Comercial',
            note_type TEXT DEFAULT 'Chamada',
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    ''')

    # Table: Email Templates & Automated Nurturing (Email)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            category TEXT DEFAULT 'Boas-vindas',
            body_text TEXT NOT NULL,
            trigger_status TEXT DEFAULT 'Novo Lead'
        )
    ''')

    # Seed leads if empty
    cursor.execute('SELECT COUNT(*) FROM leads')
    if cursor.fetchone()[0] == 0:
        seed_leads = [
            ('Eng. Carlos Eduardo Ramos', 'carlos.ramos@techiberica.pt', '+351 912 888 777', 'Tech Ibérica Lda.', '50-200', 'Transformação Digital', 85, 'Qualificado', 'Landing Page', '2026-09-08 10:30'),
            ('Dra. Maria Inês Fonseca', 'ines.fonseca@inovasolucoes.pt', '+351 923 777 666', 'Inova Soluções SA', '10-50', 'Software SaaS', 70, 'Contactado', 'Webinar', '2026-09-09 14:15'),
            ('Dr. Tiago Albuquerque', 'tiago.a@albuquerque-adv.pt', '+351 934 666 555', 'Albuquerque Advogados', '1-10', 'Automação Legal', 90, 'Proposta Enviada', 'Google Search', '2026-09-10 11:00'),
            ('Sofia Margarida Barreto', 'sofia.barreto@startnorte.pt', '+351 965 555 444', 'StartNorte Hub', '10-50', 'Consultoria TI', 95, 'Convertido', 'Formulário Directo', '2026-09-11 16:45'),
            ('Pedro Miguel Coimbra', 'pedro.coimbra@retailgroup.pt', '+351 919 444 333', 'Retail Group PT', '200+', 'Cloud Infrastructure', 40, 'Novo Lead', 'Landing Page', '2026-09-12 09:20')
        ]

        cursor.executemany('''
            INSERT INTO leads (name, email, phone, company, team_size, interest_area, lead_score, status, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_leads)

    # Seed notes if empty
    cursor.execute('SELECT COUNT(*) FROM notes')
    if cursor.fetchone()[0] == 0:
        seed_notes = [
            (1, 'Enmanuel Jimenez', 'Reunião Zoom', 'Apresentação da solução SaaS executada com sucesso. Cliente demonstrou elevado interesse na integração de API.', '2026-09-09 11:00'),
            (3, 'Ana Martins', 'Chamada', 'Proposta comercial de 15.000€ enviada para avaliação da direção financeira.', '2026-09-11 15:00'),
            (4, 'Diogo Silva', 'Email', 'Contrato assinado e pagamento da primeira licença concluído!', '2026-09-12 10:30')
        ]

        cursor.executemany('''
            INSERT INTO notes (lead_id, author, note_type, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_notes)

    # Seed email templates if empty
    cursor.execute('SELECT COUNT(*) FROM email_templates')
    if cursor.fetchone()[0] == 0:
        seed_emails = [
            ('Bem-vindo à LeadCraft AI — O seu acesso demonstrativo está pronto!', 'Boas-vindas', 'Olá {{NOME}},\n\nObrigado por demonstrar interesse na nossa plataforma SaaS. A equipa da EJAJ TECH agendou uma sessão demonstrativa personalizada.\n\nCom os melhores cumprimentos,\nEJAJ TECH Team', 'Novo Lead'),
            ('Seguimento da sua Proposta Comercial', 'Seguimento', 'Olá {{NOME}},\n\nGostaríamos de saber se teve oportunidade de analisar a proposta enviada para a {{EMPRESA}}. Ficamos totalmente disponíveis para esclarecer qualquer dúvida.\n\nAtenciosamente,\nEJAJ TECH', 'Proposta Enviada'),
            ('Obrigado por se juntar a nós! - Onboarding de Cliente', 'Onboarding', 'Olá {{NOME}},\n\nÉ um enorme orgulho dar as boas-vindas à {{EMPRESA}} como nosso novo parceiro de crescimento!\n\nUm abraço,\nLead Architect Enmanuel Jimenez', 'Convertido')
        ]

        cursor.executemany('''
            INSERT INTO email_templates (subject, category, body_text, trigger_status)
            VALUES (?, ?, ?, ?)
        ''', seed_emails)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados lead_craft.db inicializada com sucesso!")
