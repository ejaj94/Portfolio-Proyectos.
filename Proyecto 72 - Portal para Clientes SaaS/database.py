import sqlite3
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'clientportal.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Client Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        contact_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        nif_vat TEXT NOT NULL,
        account_manager TEXT,
        avatar_url TEXT,
        status TEXT DEFAULT 'Ativo',
        created_at TEXT NOT NULL
    );
    """)

    # Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        project_name TEXT NOT NULL,
        category TEXT NOT NULL,
        progress_percent INTEGER DEFAULT 0,
        status TEXT NOT NULL, -- Em Progresso, Em Revisão, Concluído, Em Espera
        start_date TEXT NOT NULL,
        deadline TEXT NOT NULL,
        budget_total REAL NOT NULL,
        description TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    );
    """)

    # Documents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        project_id INTEGER,
        title TEXT NOT NULL,
        doc_type TEXT NOT NULL, -- Contrato, Especificação, Relatório, Entrega
        file_size TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        file_url TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """)

    # Invoices Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        invoice_number TEXT UNIQUE NOT NULL,
        issue_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        amount_total REAL NOT NULL,
        status TEXT NOT NULL, -- Paga, Pendente, Vencida
        description TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    );
    """)

    # Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        sender_type TEXT NOT NULL, -- Cliente, Gestor
        sender_name TEXT NOT NULL,
        content TEXT NOT NULL,
        sent_at TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    );
    """)

    # Support Tickets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        ticket_code TEXT UNIQUE NOT NULL,
        subject TEXT NOT NULL,
        category TEXT NOT NULL, -- Técnico, Faturação, Dúvida, Alteração
        priority TEXT NOT NULL, -- Alta, Média, Baixa
        status TEXT NOT NULL, -- Aberto, Em Análise, Resolvido
        created_at TEXT NOT NULL,
        last_update TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    );
    """)

    # Seed Initial Data
    # 1. Clients
    cursor.execute("""
    INSERT INTO clients (company_name, contact_name, email, phone, nif_vat, account_manager, avatar_url, status, created_at)
    VALUES 
    ('Aura Luxe Group', 'Sofia Manso', 'sofia@auraluxe.pt', '+351 912 884 100', 'PT509887766', 'Enmanuel Jimenez', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150', 'Ativo', '2026-01-10 10:00'),
    ('Vortex Media House', 'Lucas Ferreira', 'lucas@vortexmedia.io', '+351 961 234 567', 'PT501234999', 'Enmanuel Jimenez', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150', 'Ativo', '2026-02-01 11:30')
    """)

    # 2. Projects
    cursor.execute("""
    INSERT INTO projects (client_id, project_name, category, progress_percent, status, start_date, deadline, budget_total, description)
    VALUES 
    (1, 'Redesign Pleno e-Commerce Luxury', 'Desenvolvimento Web', 85, 'Em Progresso', '2026-02-01', '2026-04-15', 18500.00, 'Remodelação completa do portal de e-Commerce com suporte multi-moedas e checkout em 1-clique.'),
    (1, 'Integração CRM & Automação VIP', 'Sistemas SaaS', 100, 'Concluído', '2026-01-15', '2026-03-01', 9200.00, 'Sincronização bidirecional do funil de clientes VIP com HubSpot e ERP de faturação.'),
    (1, 'App Mobile Experiência de Cliente', 'Mobile iOS/Android', 40, 'Em Progresso', '2026-03-01', '2026-06-30', 24000.00, 'Aplicação nativa em Flutter para membros do clube de fidelidade Aura Luxe.'),
    (2, 'Branding & Identidade Digital 2026', 'Design & Branding', 90, 'Em Revisão', '2026-02-10', '2026-03-25', 6500.00, 'Manual de marca executivo, guias de tipografia e ativos 3D para campanhas.')
    """)

    # 3. Documents
    cursor.execute("""
    INSERT INTO documents (client_id, project_id, title, doc_type, file_size, upload_date, file_url)
    VALUES 
    (1, 1, 'Contrato de Prestação de Serviços SaaS v2.pdf', 'Contrato', '2.4 MB', '2026-02-01', '#'),
    (1, 1, 'Arquitetura de Dados & Segurança GDPR.pdf', 'Especificação', '5.1 MB', '2026-02-15', '#'),
    (1, 2, 'Relatório de Conclusão & Certificado de Entrega.pdf', 'Entrega', '1.8 MB', '2026-03-01', '#'),
    (1, 3, 'Wireframes & User Journey Flow.pdf', 'Especificação', '8.4 MB', '2026-03-05', '#')
    """)

    # 4. Invoices
    cursor.execute("""
    INSERT INTO invoices (client_id, invoice_number, issue_date, due_date, amount_total, status, description)
    VALUES 
    (1, 'FT-2026-0104', '2026-02-01', '2026-02-15', 9250.00, 'Paga', 'Primeira Tranche (50%) - Redesign Pleno e-Commerce Luxury'),
    (1, 'FT-2026-0118', '2026-03-01', '2026-03-15', 9200.00, 'Paga', 'Liquidação Total - Integração CRM & Automação VIP'),
    (1, 'FT-2026-0135', '2026-03-10', '2026-03-25', 9250.00, 'Pendente', 'Segunda Tranche Final - Redesign Pleno e-Commerce Luxury'),
    (1, 'FT-2026-0142', '2026-03-12', '2026-03-27', 7200.00, 'Pendente', 'Sinal (30%) - App Mobile Experiência de Cliente')
    """)

    # 5. Messages
    cursor.execute("""
    INSERT INTO messages (client_id, sender_type, sender_name, content, sent_at)
    VALUES 
    (1, 'Gestor', 'Enmanuel Jimenez', 'Olá Sofia! A fase de testes de stress do e-Commerce foi concluída com sucesso. Os tempos de carregamento estão abaixo de 400ms.', '2026-03-10 14:20'),
    (1, 'Cliente', 'Sofia Manso', 'Excelente notícia Enmanuel! Quando podemos agendar a reunião de validação dos pagamentos via MB WAY e Klarna?', '2026-03-10 15:05'),
    (1, 'Gestor', 'Enmanuel Jimenez', 'Disponibilizei os horários na sua agenda. Quinta-feira às 11h00 funciona perfeitamente!', '2026-03-10 15:30'),
    (1, 'Cliente', 'Sofia Manso', 'Confirmado! Já recebi a convocatória. Obrigada pela rapidez.', '2026-03-10 16:00')
    """)

    # 6. Support Tickets
    cursor.execute("""
    INSERT INTO tickets (client_id, ticket_code, subject, category, priority, status, created_at, last_update)
    VALUES 
    (1, 'TCK-8801', 'Solicitação de novo método de pagamento (Stripe Connect)', 'Técnico', 'Média', 'Em Análise', '2026-03-08 09:30', '2026-03-10 11:00'),
    (1, 'TCK-8824', 'Dúvida sobre fatura FT-2026-0135 e retenção na fonte', 'Faturação', 'Baixa', 'Resolvido', '2026-03-02 16:45', '2026-03-03 10:15'),
    (1, 'TCK-8890', 'Ajuste de permissões de utilizadores gestores no portal', 'Alteração', 'Alta', 'Aberto', '2026-03-11 10:00', '2026-03-11 10:00')
    """)

    conn.commit()
    conn.close()
    print("[Database OK] clientportal.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
