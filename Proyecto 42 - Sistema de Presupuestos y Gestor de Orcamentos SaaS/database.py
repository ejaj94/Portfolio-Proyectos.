import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'quotes.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table Clients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT NOT NULL,
            nif TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table Quotes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_number TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            valid_until TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax_rate REAL DEFAULT 23.0,
            tax_amount REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Pendente',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Table Quote Items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quote_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (quote_id) REFERENCES quotes (id) ON DELETE CASCADE
        )
    ''')
    
    # Seed data if clients table is empty
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        today = datetime.now()
        
        clients = [
            ("Dr. Alexandre Mendes", "Algarve Health Clinic & Spa", "PT509123456", "alexandre.mendes@algarvehealth.pt", "+351 912 345 678", "Av. 5 de Outubro 120, 8000-076 Faro"),
            ("Engª. Sofia Rodrigues", "Imobiliária Vale do Lobo Lux", "PT508987654", "sofia.rodrigues@valelobo.pt", "+351 961 234 567", "Praça Central 45, 8135-034 Almancil"),
            ("Carlos Fontes", "Restaurante Mariscaria Gourmet", "PT507654321", "geral@mariscariagourmet.pt", "+351 933 456 789", "Marina de Vilamoura Loja 12, 8125-401 Quarteira"),
            ("Mariana Vasconcelos", "TechLogistics Portugal Lda", "PT506543210", "m.vasconcelos@techlogistics.pt", "+351 918 765 432", "Zona Industrial de Loulé Lote 8, 8100-272 Loulé"),
            ("Gonçalo Pinheiro", "Executive Studio Barber & Spa", "PT505432109", "goncalo@executivestudio.pt", "+351 922 111 222", "Rua de Santo António 88, 8000-283 Faro")
        ]
        
        cursor.executemany('''
            INSERT INTO clients (name, company, nif, email, phone, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', clients)
        
        quotes = [
            ("ORC-2026-001", 1, today.strftime('%Y-%m-%d'), (today + timedelta(days=30)).strftime('%Y-%m-%d'), 4500.0, 23.0, 1035.0, 5535.0, 'Aprovado', 'Condições de pagamento: 50% na aprovação e 50% após entrega final.'),
            ("ORC-2026-002", 2, today.strftime('%Y-%m-%d'), (today + timedelta(days=30)).strftime('%Y-%m-%d'), 8900.0, 23.0, 2047.0, 10947.0, 'Enviado', 'Inclui módulo de realidade virtual e tour 360º de imóveis de luxo.'),
            ("ORC-2026-003", 3, (today - timedelta(days=5)).strftime('%Y-%m-%d'), (today + timedelta(days=25)).strftime('%Y-%m-%d'), 2800.0, 23.0, 644.0, 3444.0, 'Pendente', 'Implementação do sistema KDS de cozinha com ecrãs táteis.'),
            ("ORC-2026-004", 4, (today - timedelta(days=10)).strftime('%Y-%m-%d'), (today + timedelta(days=20)).strftime('%Y-%m-%d'), 12500.0, 23.0, 2875.0, 15375.0, 'Aprovado', 'Desenvolvimento de plataforma telemétrica de frota com MB WAY e Stripe.'),
            ("ORC-2026-005", 5, (today - timedelta(days=12)).strftime('%Y-%m-%d'), (today + timedelta(days=18)).strftime('%Y-%m-%d'), 1500.0, 23.0, 345.0, 1845.0, 'Aprovado', 'Sistema de agendamentos online e gestão de clientes.'),
            ("ORC-2026-006", 1, (today - timedelta(days=2)).strftime('%Y-%m-%d'), (today + timedelta(days=28)).strftime('%Y-%m-%d'), 3200.0, 23.0, 736.0, 3936.0, 'Pendente', 'Manutenção preventiva e otimização de infraestrutura de servidores cloud.')
        ]
        
        cursor.executemany('''
            INSERT INTO quotes (quote_number, client_id, issue_date, valid_until, subtotal, tax_rate, tax_amount, total, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', quotes)
        
        quote_items = [
            # ORC-2026-001
            (1, "Desenvolvimento de Plataforma SaaS de Gestão Clínica Veterinária/Médica", 1.0, 3500.0, 3500.0),
            (1, "Integração de Notificações SMS & E-mail para Lembretes de Consultas", 1.0, 1000.0, 1000.0),
            
            # ORC-2026-002
            (2, "Portal Inmobiliário de Luxo com Filtros Geográficos e Moedas Internacionais", 1.0, 6500.0, 6500.0),
            (2, "Módulo de Tour Virtual 360º e Integração CRM de Vendas", 1.0, 2400.0, 2400.0),
            
            # ORC-2026-003
            (3, "Instalação e Configuração do Sistema KDS de Cozinha (Fast & Gourmet)", 1.0, 1800.0, 1800.0),
            (3, "Formação Técnica de Staff e Suporte Presencial no Lançamento", 1.0, 1000.0, 1000.0),
            
            # ORC-2026-004
            (4, "Arquitetura e Desenvolvimento de App Telemétrica de Logística & Entregas", 1.0, 9500.0, 9500.0),
            (4, "Integração de Pasarela de Pagamentos Stripe & MB WAY", 1.0, 3000.0, 3000.0),
            
            # ORC-2026-005
            (5, "Website Responsivo com Sistema de Agendamento em Tempo Real", 1.0, 1500.0, 1500.0),
            
            # ORC-2026-006
            (6, "Auditoria de Segurança e Migração de Base de Dados para Nuvem", 1.0, 3200.0, 3200.0)
        ]
        
        cursor.executemany('''
            INSERT INTO quote_items (quote_id, description, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', quote_items)
        
    conn.commit()
    conn.close()
    print("[OK] Base de dados quotes.db inicializada com sucesso para PRESUPUESTO PRO SaaS.")

if __name__ == '__main__':
    init_db()
