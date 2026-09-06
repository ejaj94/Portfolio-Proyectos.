import os
import sqlite3
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'proposals.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Proposals Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            client_name TEXT NOT NULL,
            client_company TEXT NOT NULL,
            client_email TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            validity_days INTEGER DEFAULT 30,
            subtotal REAL NOT NULL DEFAULT 0.0,
            vat_rate REAL NOT NULL DEFAULT 23.0,
            vat_amount REAL NOT NULL DEFAULT 0.0,
            total_amount REAL NOT NULL DEFAULT 0.0,
            payment_terms TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Enviada',
            signature_data TEXT,
            signed_at TIMESTAMP,
            signed_by_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposal_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            service_title TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price REAL NOT NULL DEFAULT 0.0,
            total_price REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (proposal_id) REFERENCES proposals (id) ON DELETE CASCADE
        )
    ''')

    # Timeline Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposal_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            phase_name TEXT NOT NULL,
            duration_text TEXT NOT NULL,
            deliverables TEXT NOT NULL,
            FOREIGN KEY (proposal_id) REFERENCES proposals (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed demo data if empty
    cursor.execute('SELECT COUNT(*) FROM proposals')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    demo_sign = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK8AAAA8CAYAAAC6fH4/AAA..." # sample string marker
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Proposal 1 (Signed)
    cursor.execute('''
        INSERT INTO proposals (
            code, client_name, client_company, client_email, client_phone,
            title, description, validity_days, subtotal, vat_rate, vat_amount,
            total_amount, payment_terms, status, signature_data, signed_at, signed_by_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'PROP-2026-1001', 'Dr. Ricardo Fonseca', 'Grupo Retail Luxe Lda', 'r.fonseca@retailluxe.pt', '+351 912 345 678',
        'Redesenho de Plataforma E-Commerce SaaS & App Móvel iOS/Android',
        'Proposta comercial completa para reformulação integral da loja online, integração com ERP de stocks, pasarela de pagamento Stripe & MB WAY e lançamento de aplicação móvel nativa.',
        30, 8500.00, 23.0, 1955.00, 10455.00,
        '50% no início do projeto e 50% após aprovação final e entrega em produção.',
        'Aceite / Assinada', demo_sign, now_str, 'Dr. Ricardo Fonseca'
    ))
    prop1_id = cursor.lastrowid

    # Items for Proposal 1
    items1 = [
        (prop1_id, 'Design UI/UX & Protótipo Interativo', 'Criativo Figma completo de todas as páginas da loja web e app móvel com sistema de design corporativo.', 1, 2500.00, 2500.00),
        (prop1_id, 'Desenvolvimento Web Frontend & Backend SaaS', 'Plataforma em Python/Flask com base de dados SQLite/PostgreSQL, checkout responsivo e área de cliente.', 1, 4000.00, 4000.00),
        (prop1_id, 'Aplicação Móvel Nativa iOS & Android', 'Desenvolvimento da app móvel nativa em Kotlin WebView wrapper com notificações push.', 1, 2000.00, 2000.00)
    ]
    cursor.executemany('INSERT INTO proposal_items (proposal_id, service_title, description, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?, ?)', items1)

    # Timeline for Proposal 1
    timeline1 = [
        (prop1_id, 'Fase 1: Levantamento de Requisitos & Wireframes', 'Semana 1 - 2', 'Documento de especificação técnica e protótipo interativo no Figma.'),
        (prop1_id, 'Fase 2: Desenvolvimento de Software & APIs', 'Semana 3 - 6', 'Código fonte backend, módulos de checkout e integrações de pagamentos.'),
        (prop1_id, 'Fase 3: Testes de Segurança & Publicação', 'Semana 7 - 8', 'Testes de carga, validação de pagamentos e lançamento em produção.')
    ]
    cursor.executemany('INSERT INTO proposal_timeline (proposal_id, phase_name, duration_text, deliverables) VALUES (?, ?, ?, ?)', timeline1)

    # Proposal 2 (Sent)
    cursor.execute('''
        INSERT INTO proposals (
            code, client_name, client_company, client_email, client_phone,
            title, description, validity_days, subtotal, vat_rate, vat_amount,
            total_amount, payment_terms, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'PROP-2026-1002', 'Eng. Fernando Mendes', 'TechLogistics Portugal S.A.', 'f.mendes@techlogistics.pt', '+351 913 888 999',
        'Sistema de Gestão ERP & Automação de Faturação Enterprise',
        'Implementação de software de gestão de frotas, automação de processos de armazém e integração direta com a Autoridade Tributária.',
        15, 14200.00, 23.0, 3266.00, 17466.00,
        '40% Adjudicação, 30% Entrega Beta e 30% com Lançamento Oficial.',
        'Enviada'
    ))
    prop2_id = cursor.lastrowid

    items2 = [
        (prop2_id, 'Módulo de Gestão de Frotas & GPS', 'Rastreio satelital de viaturas e cálculo automático de rotas de entrega.', 1, 6200.00, 6200.00),
        (prop2_id, 'Motor de Faturação Certificada pela AT', 'Software de faturação com transmissão SAF-T e assinatura digital de documentos.', 1, 8000.00, 8000.00)
    ]
    cursor.executemany('INSERT INTO proposal_items (proposal_id, service_title, description, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?, ?)', items2)

    timeline2 = [
        (prop2_id, 'Fase 1: Arquitetura de Dados & Base de Dados', 'Semana 1 - 3', 'Esquema relacional e infraestrutura de servidores cloud.'),
        (prop2_id, 'Fase 2: Integração SAF-T & Testes Homologados', 'Semana 4 - 8', 'Certificação pela AT e validação de documentos fiscais.')
    ]
    cursor.executemany('INSERT INTO proposal_timeline (proposal_id, phase_name, duration_text, deliverables) VALUES (?, ?, ?, ?)', timeline2)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados proposals.db inicializada com sucesso para Proyecto 49!")
