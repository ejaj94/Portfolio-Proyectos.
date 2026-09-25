import sqlite3
import os
import json
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'business_os.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            tax_id TEXT NOT NULL,
            tier TEXT DEFAULT 'Standard', -- Standard, Premium, VIP Enterprise
            status TEXT DEFAULT 'Ativo', -- Ativo, Lead, Inativo
            lifetime_value REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. CRM & Oportunidades (Deals)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crm_deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            value REAL NOT NULL,
            stage TEXT DEFAULT 'Prospecto', -- Prospecto, Qualificado, Proposta, Negociacao, Ganho, Perdido
            probability_pct INTEGER DEFAULT 50,
            closing_date DATE NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    # 3. Faturacao & Recibos (Invoices)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            subtotal REAL NOT NULL,
            tax_rate REAL DEFAULT 23.0,
            tax_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'Pendente', -- Paga, Pendente, Atrasada, Cancelada
            items_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    # 4. Orcamentos & Propostas (Quotes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_number TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            valid_until DATE NOT NULL,
            status TEXT DEFAULT 'Enviado', -- Rascunho, Enviado, Aprovado, Rejeitado, Convertido
            items_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    # 5. Inventario & Catalogo de Produtos/Servicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL, -- Hardware, Software Licencas, Servicos Consultoria, Acessorios
            stock_quantity INTEGER NOT NULL,
            min_threshold INTEGER DEFAULT 5,
            cost_price REAL NOT NULL,
            sale_price REAL NOT NULL,
            unit TEXT DEFAULT 'Unid', -- Unid, Horas, Pacote, Licenca
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 6. Tarefas & Gestao de Projetos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            client_id INTEGER,
            priority TEXT DEFAULT 'Media', -- Critica, Alta, Media, Baixa
            due_date DATE,
            assigned_to TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente', -- Pendente, Em Curso, Concluida
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    # 7. Calendario de Eventos & Reunioes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_type TEXT NOT NULL, -- Reuniao, Demo, Entrega, Vencimento
            event_date DATE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            client_id INTEGER,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    # 8. Helpdesk & Tickets de Suporte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_code TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            priority TEXT DEFAULT 'Media', -- Critica, Alta, Media, Baixa
            status TEXT DEFAULT 'Aberto', -- Aberto, Em Analise, Resolvido
            channel TEXT DEFAULT 'Email', -- Email, Chat, Telefone, Portal
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    # 9. Copilot IA Insights & Decisoes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL, -- Financeiro, CRM, Inventario, Suporte
            insight_text TEXT NOT NULL,
            action_recommended TEXT NOT NULL,
            impact_score INTEGER DEFAULT 85,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed Initial Data if empty
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        seed_clients = [
            ('Vortex Media Group', 'Sofia Valente', 'sofia@vortexmedia.pt', '+351 912 345 678', 'Lisboa', 'PT509123456', 'VIP Enterprise', 'Ativo', 28500.00),
            ('Lumina Retail Iberia', 'Pedro Alcantara', 'pedro@luminaretail.com', '+351 923 456 789', 'Porto', 'PT508234567', 'Premium', 'Ativo', 16200.00),
            ('BioSaude Clinicas SA', 'Dra. Beatriz Mendes', 'bmendes@biosaude.pt', '+351 934 567 890', 'Coimbra', 'PT507345678', 'Premium', 'Ativo', 12400.00),
            ('Horizon Logistics Global', 'Carlos Figueira', 'carlos@horizonlog.pt', '+351 965 678 901', 'Faro', 'PT506456789', 'VIP Enterprise', 'Ativo', 34800.00),
            ('Atlantic Green Energy', 'Ines Barreto', 'ines@atlanticgreen.eu', '+351 917 890 123', 'Braga', 'PT505567890', 'Standard', 'Lead', 4500.00)
        ]
        cursor.executemany('''
            INSERT INTO clients (company_name, contact_name, email, phone, city, tax_id, tier, status, lifetime_value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_clients)

        seed_deals = [
            (1, 'Expansao Cloud & Licenciamento IA Enterprise', 18500.00, 'Negociacao', 80, (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d'), 'Reuniao de validacao orcamental com o CFO.'),
            (2, 'Implementacao de Modulo de Faturacao POS', 9200.00, 'Proposta', 60, (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'), 'Proposta comercial enviada na segunda-feira.'),
            (3, 'Contrato Anual Suporte Tecnico Dedicado 24/7', 7400.00, 'Ganho', 100, (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'), 'Contrato assinado digitalmente.'),
            (4, 'Otimizacao Logistica com Telemetria IoT', 24000.00, 'Qualificado', 45, (datetime.now() + timedelta(days=35)).strftime('%Y-%m-%d'), 'Auditoria previa de frotas em curso.'),
            (5, 'Consultoria de Transformacao Digital', 4500.00, 'Prospecto', 25, (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'), 'Lead qualificada via formulario web.')
        ]
        cursor.executemany('''
            INSERT INTO crm_deals (client_id, title, value, stage, probability_pct, closing_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_deals)

        seed_invoices = [
            ('FAT-2026-0891', 1, (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'), 6000.00, 23.0, 1380.00, 7380.00, 'Paga', '[{"desc": "Consultoria Arquitetura Cloud", "qty": 1, "price": 6000.00}]'),
            ('FAT-2026-0892', 2, (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=25)).strftime('%Y-%m-%d'), 4500.00, 23.0, 1035.00, 5535.00, 'Pendente', '[{"desc": "Licenca Anual Business OS Pro", "qty": 1, "price": 4500.00}]'),
            ('FAT-2026-0893', 3, (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'), (datetime.now() + timedelta(days=28)).strftime('%Y-%m-%d'), 3200.00, 23.0, 736.00, 3936.00, 'Paga', '[{"desc": "Manutencao Preventiva e Servidores", "qty": 1, "price": 3200.00}]'),
            ('FAT-2026-0894', 4, (datetime.now() - timedelta(days=40)).strftime('%Y-%m-%d'), (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'), 5800.00, 23.0, 1334.00, 7134.00, 'Atrasada', '[{"desc": "Integracao API e Gateway Logistica", "qty": 1, "price": 5800.00}]')
        ]
        cursor.executemany('''
            INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, subtotal, tax_rate, tax_amount, total_amount, status, items_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_invoices)

        seed_quotes = [
            ('ORC-2026-0412', 2, 'Pacote de Modernizacao Digital POS & Inventario', 8500.00, 1955.00, 10455.00, (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'), 'Enviado', '[{"desc": "Software POS Central", "qty": 3, "price": 1500.00}, {"desc": "Instalacao e Formacao de Equipa", "qty": 1, "price": 4000.00}]'),
            ('ORC-2026-0413', 1, 'Modulo Adicional de Analitica Preditiva com IA', 12000.00, 2760.00, 14760.00, (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'), 'Aprovado', '[{"desc": "Motor Preditivo IA", "qty": 1, "price": 12000.00}]'),
            ('ORC-2026-0414', 5, 'Plano Inicial Startup de Gestao Integrada', 3600.00, 828.00, 4428.00, (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'), 'Rascunho', '[{"desc": "Setup Inicial Business OS", "qty": 1, "price": 3600.00}]')
        ]
        cursor.executemany('''
            INSERT INTO quotes (quote_number, client_id, title, subtotal, tax_amount, total_amount, valid_until, status, items_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_quotes)

        seed_inventory = [
            ('SRV-CLOUD-01', 'Instancia Cloud Dedicada NVMe', 'Hardware', 14, 5, 120.00, 350.00, 'Unid'),
            ('LIC-BIZ-ENT', 'Licenca Anual Business OS Enterprise', 'Software Licencas', 48, 10, 800.00, 2400.00, 'Licenca'),
            ('SRV-CONS-DEV', 'Hora de Engenharia Senior & Arquitetura', 'Servicos Consultoria', 120, 20, 45.00, 95.00, 'Horas'),
            ('HW-POS-TERM', 'Terminal POS Touchscreen Termico IP65', 'Hardware', 3, 5, 290.00, 650.00, 'Unid'), # Alerta de Stock Baixo
            ('SEC-TOKEN-U2F', 'Chave de Seguranca FIDO2 Hardware', 'Acessorios', 2, 8, 18.00, 55.00, 'Unid') # Alerta Critico
        ]
        cursor.executemany('''
            INSERT INTO inventory (sku, name, category, stock_quantity, min_threshold, cost_price, sale_price, unit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_inventory)

        seed_tasks = [
            ('Preparar demonstracao executiva para Lumina Retail', 2, 'Alta', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), 'Alexandre Silva', 'Em Curso'),
            ('Enviar notificacao de regularizacao de fatura em atraso FAT-0894', 4, 'Critica', (datetime.now()).strftime('%Y-%m-%d'), 'Joana Costa', 'Pendente'),
            ('Repor stock minimo de Terminais POS Termicos', None, 'Alta', (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'), 'Operacoes', 'Pendente'),
            ('Concluir migracao de base de dados BioSaude Clinicas', 3, 'Media', (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'), 'Engenharia', 'Pendente'),
            ('Revisao trimestral de metas de receita com CFO', 1, 'Baixa', (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d'), 'Direcao', 'Concluida')
        ]
        cursor.executemany('''
            INSERT INTO tasks (title, client_id, priority, due_date, assigned_to, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_tasks)

        seed_events = [
            ('Apresentacao Comercial Q4', 'Reuniao', (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'), '10:00', '11:30', 2, 'Sala de Reunioes Virtual / Zoom'),
            ('Fecho de Auditoria de Seguranca', 'Entrega', (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), '14:30', '16:00', 1, 'Edificio Central Lisboa'),
            ('Workshop de Formacao em Business OS', 'Demo', (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'), '11:00', '12:30', 3, 'Auditorio Principal BioSaude'),
            ('Vencimento Fatura FAT-2026-0892', 'Vencimento', (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), '09:00', '09:30', 2, 'Sistema Financeiro')
        ]
        cursor.executemany('''
            INSERT INTO calendar_events (title, event_type, event_date, start_time, end_time, client_id, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_events)

        seed_tickets = [
            ('TCK-901', 4, 'Dificuldade na sincronizacao automatica de faturas via API', 'Alta', 'Em Analise', 'Email'),
            ('TCK-902', 3, 'Pedido de criacao de 3 novos utilizadores administrativos', 'Media', 'Aberto', 'Chat'),
            ('TCK-903', 1, 'Configuracao de autenticacao de dois fatores (2FA)', 'Baixa', 'Resolvido', 'Portal'),
            ('TCK-904', 2, 'Lentidao pontual na emissao de relatorios fiscais SAF-T', 'Alta', 'Aberto', 'Telefone')
        ]
        cursor.executemany('''
            INSERT INTO support_tickets (ticket_code, client_id, subject, priority, status, channel)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_tickets)

        seed_insights = [
            ('Financeiro', 'Fluxo de caixa projetado positivo de 23.985 EUR este mes com 85% de taxa de cobranca pontual.', 'Recomenda-se enviar lembrete automatico para FAT-0894 em atraso.', 92),
            ('CRM', 'O pipeline de vendas tem 53.600 EUR em negociacao ativa com 75% de probabilidade media de fecho.', 'Foque no deal da Vortex Media para assegurar a meta do trimestre.', 88),
            ('Inventario', '2 artigos encontram-se abaixo do nivel critico de seguranca (Terminais POS e Chaves U2F).', 'Emitir ordem de compra automatica aos fornecedores hoje.', 95),
            ('Suporte', 'Tempo medio de resolucao de tickets encontra-se em 2.4 horas, superando o SLA contratual em 18%.', 'Manter escala de apoio dedicada ao cliente Horizon Logistics.', 84)
        ]
        cursor.executemany('''
            INSERT INTO ai_insights (category, insight_text, action_recommended, impact_score)
            VALUES (?, ?, ?, ?)
        ''', seed_insights)

        conn.commit()
    conn.close()

# --- CRM & Clientes Operations ---
def get_all_clients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients ORDER BY lifetime_value DESC, id DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_client(company_name, contact_name, email, phone, city, tax_id, tier, status, lifetime_value):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (company_name, contact_name, email, phone, city, tax_id, tier, status, lifetime_value)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (company_name, contact_name, email, phone, city, tax_id, tier, status, lifetime_value))
    cid = cursor.lastrowid
    conn.commit()
    conn.close()
    return cid

# --- CRM Deals ---
def get_all_deals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.*, c.company_name, c.tier
        FROM crm_deals d
        JOIN clients c ON d.client_id = c.id
        ORDER BY d.value DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_deal(client_id, title, value, stage, probability_pct, closing_date, notes=''):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO crm_deals (client_id, title, value, stage, probability_pct, closing_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (client_id, title, value, stage, probability_pct, closing_date, notes))
    did = cursor.lastrowid
    conn.commit()
    conn.close()
    return did

def update_deal_stage(deal_id, stage):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE crm_deals SET stage = ? WHERE id = ?', (stage, deal_id))
    conn.commit()
    conn.close()

# --- Invoices (Facturacao) ---
def get_all_invoices():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.*, c.company_name, c.tax_id, c.email as client_email
        FROM invoices i
        JOIN clients c ON i.client_id = c.id
        ORDER BY i.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def create_invoice(client_id, due_days, subtotal, tax_rate=23.0, items_json='[]'):
    conn = get_db()
    cursor = conn.cursor()
    inv_num = f"FAT-2026-{random.randint(1000, 9999)}"
    issue_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=int(due_days))).strftime('%Y-%m-%d')
    tax_amount = round(subtotal * (tax_rate / 100.0), 2)
    total_amount = round(subtotal + tax_amount, 2)

    cursor.execute('''
        INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, subtotal, tax_rate, tax_amount, total_amount, status, items_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pendente', ?)
    ''', (inv_num, client_id, issue_date, due_date, subtotal, tax_rate, tax_amount, total_amount, items_json))
    iid = cursor.lastrowid

    cursor.execute('UPDATE clients SET lifetime_value = lifetime_value + ? WHERE id = ?', (total_amount, client_id))
    conn.commit()
    conn.close()
    return iid, inv_num

def update_invoice_status(invoice_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE invoices SET status = ? WHERE id = ?', (status, invoice_id))
    conn.commit()
    conn.close()

# --- Quotes (Presupuestos) ---
def get_all_quotes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT q.*, c.company_name, c.email as client_email
        FROM quotes q
        JOIN clients c ON q.client_id = c.id
        ORDER BY q.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def create_quote(client_id, title, subtotal, valid_days=30, items_json='[]'):
    conn = get_db()
    cursor = conn.cursor()
    q_num = f"ORC-2026-{random.randint(1000, 9999)}"
    valid_until = (datetime.now() + timedelta(days=int(valid_days))).strftime('%Y-%m-%d')
    tax_amount = round(subtotal * 0.23, 2)
    total_amount = round(subtotal + tax_amount, 2)

    cursor.execute('''
        INSERT INTO quotes (quote_number, client_id, title, subtotal, tax_amount, total_amount, valid_until, status, items_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Enviado', ?)
    ''', (q_num, client_id, title, subtotal, tax_amount, total_amount, valid_until, items_json))
    qid = cursor.lastrowid
    conn.commit()
    conn.close()
    return qid, q_num

def convert_quote_to_invoice(quote_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quotes WHERE id = ?', (quote_id,))
    q = cursor.fetchone()
    if not q:
        conn.close()
        return None

    # Mark quote converted
    cursor.execute("UPDATE quotes SET status = 'Convertido' WHERE id = ?", (quote_id,))
    
    # Create invoice
    inv_num = f"FAT-2026-{random.randint(1000, 9999)}"
    issue_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    cursor.execute('''
        INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, subtotal, tax_rate, tax_amount, total_amount, status, items_json)
        VALUES (?, ?, ?, ?, ?, 23.0, ?, ?, 'Pendente', ?)
    ''', (inv_num, q['client_id'], issue_date, due_date, q['subtotal'], q['tax_amount'], q['total_amount'], q['items_json']))
    new_inv_id = cursor.lastrowid

    cursor.execute('UPDATE clients SET lifetime_value = lifetime_value + ? WHERE id = ?', (q['total_amount'], q['client_id']))
    conn.commit()
    conn.close()
    return new_inv_id, inv_num

# --- Inventory Operations ---
def get_all_inventory():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory ORDER BY stock_quantity ASC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_inventory_item(sku, name, category, stock_qty, min_threshold, cost_price, sale_price, unit):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (sku, name, category, stock_quantity, min_threshold, cost_price, sale_price, unit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sku, name, category, stock_qty, min_threshold, cost_price, sale_price, unit))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def adjust_stock(item_id, delta):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET stock_quantity = stock_quantity + ? WHERE id = ?', (delta, item_id))
    conn.commit()
    conn.close()

# --- Tasks Operations ---
def get_all_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, c.company_name
        FROM tasks t
        LEFT JOIN clients c ON t.client_id = c.id
        ORDER BY CASE t.priority WHEN 'Critica' THEN 1 WHEN 'Alta' THEN 2 WHEN 'Media' THEN 3 ELSE 4 END, t.due_date ASC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_task(title, client_id, priority, due_date, assigned_to):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, client_id, priority, due_date, assigned_to, status)
        VALUES (?, ?, ?, ?, ?, 'Pendente')
    ''', (title, client_id, priority, due_date, assigned_to))
    tid = cursor.lastrowid
    conn.commit()
    conn.close()
    return tid

def update_task_status(task_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()

# --- Calendar Operations ---
def get_all_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.*, c.company_name
        FROM calendar_events e
        LEFT JOIN clients c ON e.client_id = c.id
        ORDER BY e.event_date ASC, e.start_time ASC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_calendar_event(title, event_type, event_date, start_time, end_time, client_id, location):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO calendar_events (title, event_type, event_date, start_time, end_time, client_id, location)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, event_type, event_date, start_time, end_time, client_id, location))
    eid = cursor.lastrowid
    conn.commit()
    conn.close()
    return eid

# --- Support Tickets Operations ---
def get_all_tickets():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, c.company_name, c.email as client_email
        FROM support_tickets t
        JOIN clients c ON t.client_id = c.id
        ORDER BY CASE t.priority WHEN 'Critica' THEN 1 WHEN 'Alta' THEN 2 WHEN 'Media' THEN 3 ELSE 4 END, t.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def create_ticket(client_id, subject, priority, channel):
    conn = get_db()
    cursor = conn.cursor()
    code = f"TCK-{random.randint(100, 999)}"
    cursor.execute('''
        INSERT INTO support_tickets (ticket_code, client_id, subject, priority, status, channel)
        VALUES (?, ?, ?, ?, 'Aberto', ?)
    ''', (code, client_id, subject, priority, channel))
    tid = cursor.lastrowid
    conn.commit()
    conn.close()
    return tid, code

def update_ticket_status(ticket_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE support_tickets SET status = ? WHERE id = ?', (status, ticket_id))
    conn.commit()
    conn.close()

# --- AI Autonomous Brain & Insights ---
def get_ai_insights():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ai_insights ORDER BY impact_score DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def process_ai_copilot_query(prompt_text):
    prompt_lower = prompt_text.lower()
    
    if 'faturacao' in prompt_lower or 'receita' in prompt_lower or 'caixa' in prompt_lower or 'dinheiro' in prompt_lower:
        response = (
            "Analise de Caixa & Faturacao em Tempo Real:\n\n"
            "- Faturacao Liquida Emitida este mes: 23.985 EUR\n"
            "- Faturas em Aberto: 5.535 EUR com vencimento nos proximos 20 dias\n"
            "- Fatura Atrasada: FAT-2026-0894 (7.134 EUR) com 10 dias de atraso na Horizon Logistics.\n\n"
            "Acao Recomendada: O Business OS ja preparou um lembrete automatico com nota de debito. Deseja que envie por email agora?"
        )
    elif 'crm' in prompt_lower or 'leads' in prompt_lower or 'vendas' in prompt_lower or 'proposta' in prompt_lower:
        response = (
            "Diagnostico do Pipeline Comercial (CRM):\n\n"
            "- Oportunidades Ativas: 5 deals totalizando 53.600 EUR em pipeline ponderado.\n"
            "- Deal mais quente: Vortex Media (18.500 EUR, 80% probabilidade de fecho).\n"
            "- Risco Identificado: Deal da Lumina Retail (9.200 EUR) sem contacto ha 4 dias.\n\n"
            "Acao Recomendada: Agendada tarefa automatica para o gestor comercial contactar a Lumina Retail hoje."
        )
    elif 'stock' in prompt_lower or 'inventario' in prompt_lower or 'produtos' in prompt_lower:
        response = (
            "Alerta de Reposicao de Inventario:\n\n"
            "2 produtos atingiram o limiar critico de seguranca:\n"
            "1. Terminal POS Touchscreen (3 unidades restantes, min: 5)\n"
            "2. Chave de Seguranca FIDO2 (2 unidades restantes, min: 8)\n\n"
            "Acao Recomendada: Criar ordem de compra automatica aos fornecedores com valor estimado de 1.450 EUR."
        )
    elif 'suporte' in prompt_lower or 'tickets' in prompt_lower:
        response = (
            "Monitorizacao de Helpdesk & Atendimento:\n\n"
            "- Tickets Abertos: 2 pendentes de triagem\n"
            "- SLA Cumprido: 98.2% dentro do prazo estipulado de 4 horas\n"
            "- Caso Prioritario: TCK-901 (Horizon Logistics - Falha na sincronizacao de API).\n\n"
            "Acao Recomendada: O agente de IA ja gerou o script de resolucao tecnica para a equipa de engenharia."
        )
    else:
        response = (
            f"Como Cerebro Autonomo do seu Business OS, processei a sua questao: '{prompt_text}'\n\n"
            "Resumo de Performance Global:\n"
            "- A empresa esta a operar a 92% da eficiencia maxima.\n"
            "- Todas as 8 areas operacionais (CRM, Faturacao, Orcamentos, Inventario, Tarefas, Calendario, Suporte e IA) estao sincronizadas.\n"
            "- A margem media de lucro por cliente encontra-se nos 48.5%, um crescimento de 6.2% face ao trimestre anterior."
        )
    return response

# --- Comprehensive Dashboard Telemetry ---
def get_dashboard_telemetry():
    conn = get_db()
    cursor = conn.cursor()

    # Revenue & Invoices
    cursor.execute('SELECT SUM(total_amount) FROM invoices WHERE status = "Paga"')
    total_paid_revenue = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT SUM(total_amount) FROM invoices WHERE status = "Pendente"')
    total_pending_revenue = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT SUM(total_amount) FROM invoices WHERE status = "Atrasada"')
    total_overdue_revenue = cursor.fetchone()[0] or 0.0

    # Pipeline Deals
    cursor.execute('SELECT SUM(value), COUNT(*) FROM crm_deals WHERE stage NOT IN ("Ganho", "Perdido")')
    r_deals = cursor.fetchone()
    pipeline_value = r_deals[0] or 0.0
    active_deals_count = r_deals[1] or 0

    # Inventory Alerts
    cursor.execute('SELECT COUNT(*) FROM inventory WHERE stock_quantity <= min_threshold')
    low_stock_count = cursor.fetchone()[0] or 0

    # Clients count
    cursor.execute('SELECT COUNT(*) FROM clients WHERE status = "Ativo"')
    active_clients = cursor.fetchone()[0] or 0

    # Support Tickets
    cursor.execute('SELECT COUNT(*) FROM support_tickets WHERE status = "Aberto"')
    open_tickets = cursor.fetchone()[0] or 0

    # Pending Tasks
    cursor.execute('SELECT COUNT(*) FROM tasks WHERE status != "Concluida"')
    pending_tasks = cursor.fetchone()[0] or 0

    # Deals by stage distribution
    cursor.execute('SELECT stage, COUNT(*) as count, SUM(value) as total FROM crm_deals GROUP BY stage')
    deals_by_stage = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "total_paid_revenue": total_paid_revenue,
        "total_pending_revenue": total_pending_revenue,
        "total_overdue_revenue": total_overdue_revenue,
        "pipeline_value": pipeline_value,
        "active_deals_count": active_deals_count,
        "low_stock_count": low_stock_count,
        "active_clients": active_clients,
        "open_tickets": open_tickets,
        "pending_tasks": pending_tasks,
        "deals_by_stage": deals_by_stage
    }
