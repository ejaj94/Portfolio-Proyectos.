import os
import sqlite3
import json
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'clientportal.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Users Table (Clients & Admin)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
            role TEXT NOT NULL DEFAULT 'cliente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            project_code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Em Desenvolvimento',
            progress_pct INTEGER DEFAULT 0,
            deadline TEXT NOT NULL,
            budget_total REAL DEFAULT 0.0,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 3. Project Milestones Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    ''')

    # 4. Budgets / Proposals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            project_id INTEGER,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            valid_until TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 5. Invoices Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            invoice_number TEXT UNIQUE NOT NULL,
            concept TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax_rate REAL DEFAULT 23.0,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            due_date TEXT NOT NULL,
            paid_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 6. Documents Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            project_id INTEGER,
            title TEXT NOT NULL,
            file_category TEXT NOT NULL,
            file_size TEXT NOT NULL,
            download_url TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 7. Messages / Activity Stream Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            project_id INTEGER,
            sender_name TEXT NOT NULL,
            is_agency INTEGER DEFAULT 0,
            content TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 8. Support Tickets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            ticket_code TEXT UNIQUE NOT NULL,
            subject TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Média',
            status TEXT NOT NULL DEFAULT 'Aberto',
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed Demo Data if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Demo Client 1 (Sofia Martins)
    cursor.execute('''
        INSERT INTO users (email, password_hash, full_name, company_name, phone, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('sofia.martins@luxehotel.pt', '123456', 'Dra. Sofia Martins', 'Hotel Quinta da Marinha Luxe', '+351 918 777 666', 'cliente'))
    client_id = cursor.lastrowid

    # Admin User
    cursor.execute('''
        INSERT INTO users (email, password_hash, full_name, company_name, phone, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('enmanuel.jimenez@ejajtech.pt', 'admin123', 'Eng. Enmanuel Jimenez', 'EJAJ TECH Head Office', '+351 911 151 993', 'admin'))

    # Demo Projects
    cursor.execute('''
        INSERT INTO projects (client_id, project_code, title, category, status, progress_pct, deadline, budget_total, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        client_id, 'PRJ-2026-088', 'Redesenho do Portal de Reservas & App Mobile Luxe', 'Desenvolvimento Web SaaS',
        'Em Desenvolvimento', 75, '2026-10-15', 14500.00,
        'Reformulação completa da arquitetura do portal do cliente, integração de motor de reservas em tempo real com confirmação automática via SMS/WhatsApp e painel de fidelidade.'
    ))
    prj1_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO projects (client_id, project_code, title, category, status, progress_pct, deadline, budget_total, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        client_id, 'PRJ-2026-092', 'Módulo de Inteligência Artificial para Atendimento ao Hóspede', 'IA & Bots',
        'Fase de Testes', 90, '2026-09-30', 8200.00,
        'Agente virtual com LLM integrado ao PMS do hotel para resposta instantânea de dúvidas em 5 idiomas 24/7.'
    ))
    prj2_id = cursor.lastrowid

    # Milestones for Project 1
    milestones1 = [
        (prj1_id, 'Aprovação de Protótipos UI/UX & Wireframes', '2026-08-10', 'Concluído'),
        (prj1_id, 'Integração de Gateway de Pagamento Stripe/MBWay', '2026-08-25', 'Concluído'),
        (prj1_id, 'Desenvolvimento do Painel de Administração', '2026-09-15', 'Em Progresso'),
        (prj1_id, 'Testes de Carga & Lançamento em Produção', '2026-10-15', 'Pendente')
    ]
    cursor.executemany('INSERT INTO milestones (project_id, title, due_date, status) VALUES (?, ?, ?, ?)', milestones1)

    # Budgets
    budgets_data = [
        (client_id, prj1_id, 'ORC-2026-041', 'Desenvolvimento do Portal de Reservas Web & Mobile', 14500.00, 'Aprovado', '2026-07-30'),
        (client_id, prj2_id, 'ORC-2026-055', 'Módulo AI Assistant para Atendimento Multilingue 24/7', 8200.00, 'Aprovado', '2026-08-15'),
        (client_id, None, 'ORC-2026-078', 'Módulo Adicional de Gestão de Spa & Experiências VIP', 4200.00, 'Pendente', '2026-10-01')
    ]
    cursor.executemany('''
        INSERT INTO budgets (client_id, project_id, code, title, amount, status, valid_until)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', budgets_data)

    # Invoices
    invoices_data = [
        (client_id, 'FAT-2026-1088', 'Adiantamento 50% - Portal de Reservas Web & Mobile', 5894.31, 23.0, 7250.00, 'Paga', '2026-08-01', '2026-08-03 11:20:00'),
        (client_id, 'FAT-2026-1142', 'Pagamento Fase 1 - Módulo AI Assistant', 3333.33, 23.0, 4100.00, 'Paga', '2026-08-20', '2026-08-21 15:45:00'),
        (client_id, 'FAT-2026-1205', 'Entrega Intermédia 25% - Portal de Reservas', 2947.15, 23.0, 3625.00, 'Pendente', '2026-09-20', None)
    ]
    cursor.executemany('''
        INSERT INTO invoices (client_id, invoice_number, concept, subtotal, tax_rate, total_amount, status, due_date, paid_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', invoices_data)

    # Documents
    docs_data = [
        (client_id, prj1_id, 'Arquitetura_Tecnica_e_Fluxo_de_Dados.pdf', 'Documento Técnico', '3.4 MB', 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'),
        (client_id, prj1_id, 'Manual_de_Identidade_Visual_Hotel_Luxe.pdf', 'Design & Assets', '12.1 MB', 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'),
        (client_id, prj2_id, 'Relatorio_Testes_Precisao_AI_Model.pdf', 'Relatório QA', '1.8 MB', 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf')
    ]
    cursor.executemany('''
        INSERT INTO documents (client_id, project_id, title, file_category, file_size, download_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', docs_data)

    # Messages
    msgs = [
        (client_id, prj1_id, 'Eng. Enmanuel Jimenez', 1, 'Olá Dra. Sofia! Concluímos a integração do módulo de pagamento com sucesso.'),
        (client_id, prj1_id, 'Dra. Sofia Martins', 0, 'Excelente notícia Enmanuel! O design está fantástico. Quando poderemos testar o ambiente de staging?'),
        (client_id, prj1_id, 'Eng. Enmanuel Jimenez', 1, 'Na próxima terça-feira disponibilizamos o acesso restrito ao ambiente de staging com credenciais exclusivas.')
    ]
    cursor.executemany('''
        INSERT INTO messages (client_id, project_id, sender_name, is_agency, content)
        VALUES (?, ?, ?, ?, ?)
    ''', msgs)

    # Support Tickets
    tickets = [
        (client_id, 'TK-2026-401', 'Dúvida sobre integração do gateway MBWay no portal de reservas', 'Média', 'Resolvido', 'Gostávamos de confirmar a taxa cobrada por transação MBWay.'),
        (client_id, 'TK-2026-445', 'Pedido de inclusão de campo NIF opcional na ficha de hóspede', 'Alta', 'Em Resposta', 'Precisamos que o cliente possa introduzir o NIF para emissão direta de fatura.')
    ]
    cursor.executemany('''
        INSERT INTO support_tickets (client_id, ticket_code, subject, priority, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', tickets)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados clientportal.db inicializada com sucesso para Proyecto 52!")
