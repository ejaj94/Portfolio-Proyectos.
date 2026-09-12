import sqlite3
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'warrantycraft.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        contact_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        nif_vat TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        model_code TEXT NOT NULL,
        category TEXT NOT NULL, -- Hardware, Maquinaria, Eletrodoméstico, IT
        brand TEXT NOT NULL,
        default_warranty_months INTEGER NOT NULL DEFAULT 24
    );
    """)

    # Warranties Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warranties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        warranty_code TEXT UNIQUE NOT NULL,
        client_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        serial_number TEXT UNIQUE NOT NULL,
        purchase_date TEXT NOT NULL,
        expiration_date TEXT NOT NULL,
        warranty_months INTEGER NOT NULL,
        status TEXT NOT NULL, -- Ativa, Prestes a Expirar, Expirada
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    );
    """)

    # Incidents / RMA Claims Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_code TEXT UNIQUE NOT NULL,
        warranty_id INTEGER NOT NULL,
        fault_description TEXT NOT NULL,
        severity TEXT NOT NULL, -- Crítica, Alta, Média, Baixa
        status TEXT NOT NULL, -- Aberto, Em Reparação, Em Testes, Concluído, Substituído
        assigned_technician TEXT,
        opened_date TEXT NOT NULL,
        resolved_date TEXT,
        FOREIGN KEY (warranty_id) REFERENCES warranties (id)
    );
    """)

    # Technical Intervention Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intervention_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        technician TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (incident_id) REFERENCES incidents (id)
    );
    """)

    # Seed Initial Data
    # 1. Clients
    cursor.execute("""
    INSERT INTO clients (company_name, contact_name, email, phone, nif_vat, created_at)
    VALUES 
    ('Aura Luxe Group', 'Sofia Manso', 'sofia@auraluxe.pt', '+351 912 884 100', 'PT509887766', '2026-01-10 10:00'),
    ('Vortex Media House', 'Lucas Ferreira', 'lucas@vortexmedia.io', '+351 961 234 567', 'PT501234999', '2026-02-01 11:30'),
    ('Nexus Tech Solutions', 'Carlos Silva', 'carlos@nexustech.pt', '+351 933 445 566', 'PT503344556', '2026-02-15 14:00')
    """)

    # 2. Products
    cursor.execute("""
    INSERT INTO products (product_name, model_code, category, brand, default_warranty_months)
    VALUES 
    ('Servidor Rack Enterprise 2U', 'SRV-2U-2026', 'Hardware', 'Dell PowerEdge', 36),
    ('Impressora Industrial 3D Pro', 'PRN-3D-MAX', 'Maquinaria', 'Ultimaker', 24),
    ('Estação de Trabalho Pro 16"', 'WST-16-PRO', 'IT', 'Apple Mac Studio', 24),
    ('Sistema UPS Proteção 10kVA', 'UPS-10K-VA', 'Hardware', 'APC Schneider', 36)
    """)

    # 3. Warranties
    cursor.execute("""
    INSERT INTO warranties (warranty_code, client_id, product_id, serial_number, purchase_date, expiration_date, warranty_months, status, notes, created_at)
    VALUES 
    ('GAR-2026-101', 1, 1, 'SN-DELL-882910', '2025-04-15', '2028-04-15', 36, 'Ativa', 'Garantia Premium 24/7 On-Site incluída.', '2025-04-15 10:00'),
    ('GAR-2026-102', 1, 3, 'SN-APPL-449120', '2024-03-20', '2026-03-20', 24, 'Prestes a Expirar', 'Garantia padrão de fábrica prestes a expirar.', '2024-03-20 11:30'),
    ('GAR-2026-103', 2, 2, 'SN-ULTI-771829', '2025-01-10', '2027-01-10', 24, 'Ativa', 'Manutenção preventiva semestral recomendada.', '2025-01-10 14:00'),
    ('GAR-2026-104', 3, 4, 'SN-APC-110293', '2023-01-05', '2026-01-05', 36, 'Expirada', 'Garantia expirada. Proposta de extensão de cobertura pendente.', '2023-01-05 16:00')
    """)

    # 4. Incidents (RMA Claims)
    cursor.execute("""
    INSERT INTO incidents (incident_code, warranty_id, fault_description, severity, status, assigned_technician, opened_date, resolved_date)
    VALUES 
    ('RMA-8801', 1, 'Falha no módulo de fonte redundante PSU 2', 'Média', 'Em Reparação', 'Enmanuel Jimenez', '2026-03-05 09:30', NULL),
    ('RMA-8802', 2, 'Aquecimento anormal no ventilador secundário', 'Baixa', 'Em Testes', 'Carlos Rocha', '2026-03-08 14:15', NULL),
    ('RMA-8803', 3, 'Erro de calibração do extrusor de alta temperatura', 'Alta', 'Concluído', 'Enmanuel Jimenez', '2026-02-20 10:00', '2026-02-22 16:30')
    """)

    # 5. Technical Intervention Logs
    cursor.execute("""
    INSERT INTO intervention_logs (incident_id, action, technician, timestamp, notes)
    VALUES 
    (1, 'Abertura de Chamado RMA', 'Sofia Manso', '2026-03-05 09:30', 'Cliente reportou alerta led em PSU2.'),
    (1, 'Diagnóstico Técnico Presencial', 'Enmanuel Jimenez', '2026-03-06 11:00', 'Substituição recomendada da peça de reposição em garantia.'),
    (3, 'Diagnóstico & Calibração de Extrusor', 'Enmanuel Jimenez', '2026-02-20 11:30', 'Substituído bocal de extrusão 0.4mm sob garantia.'),
    (3, 'Testes de Qualidade & Encerramento', 'Enmanuel Jimenez', '2026-02-22 16:30', 'Impressora testada com 10h de impressão contínua. OK.')
    """)

    conn.commit()
    conn.close()
    print("[Database OK] warrantycraft.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
