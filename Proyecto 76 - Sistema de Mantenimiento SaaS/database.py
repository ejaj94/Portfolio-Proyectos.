import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'maintaincraft.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Equipment Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        serial_number TEXT NOT NULL,
        location TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Ativo',
        created_at TEXT NOT NULL
    );
    """)

    # 2. Technicians Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technicians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Disponível',
        created_at TEXT NOT NULL
    );
    """)

    # 3. Maintenances Table (Work Orders)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS maintenances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_code TEXT NOT NULL UNIQUE,
        equipment_id INTEGER NOT NULL,
        technician_id INTEGER NOT NULL,
        type TEXT NOT NULL, -- Preventiva, Corretiva, Preditiva
        priority TEXT NOT NULL, -- Baixa, Média, Alta, Urgente
        scheduled_date TEXT NOT NULL,
        completed_date TEXT,
        estimated_hours REAL NOT NULL DEFAULT 2.0,
        labor_cost REAL NOT NULL DEFAULT 0.0,
        parts_cost REAL NOT NULL DEFAULT 0.0,
        total_cost REAL NOT NULL DEFAULT 0.0,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Agendado', -- Agendado, Em Execução, Concluído, Cancelado
        created_at TEXT NOT NULL,
        FOREIGN KEY (equipment_id) REFERENCES equipment (id),
        FOREIGN KEY (technician_id) REFERENCES technicians (id)
    );
    """)

    # 4. Incidents Table (Breakdowns)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_code TEXT NOT NULL UNIQUE,
        equipment_id INTEGER NOT NULL,
        reported_by TEXT NOT NULL,
        severity TEXT NOT NULL, -- Baixa, Média, Alta, Crítica
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Aberto', -- Aberto, Em Análise, Em Reparação, Resolvido
        reported_at TEXT NOT NULL,
        resolved_at TEXT,
        FOREIGN KEY (equipment_id) REFERENCES equipment (id)
    );
    """)

    # 5. Intervention Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intervention_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        maintenance_id INTEGER,
        incident_id INTEGER,
        action TEXT NOT NULL,
        technician TEXT NOT NULL,
        parts_used TEXT,
        cost REAL DEFAULT 0.0,
        timestamp TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (maintenance_id) REFERENCES maintenances (id),
        FOREIGN KEY (incident_id) REFERENCES incidents (id)
    );
    """)

    # --- SEED DATA ---
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = date.today()

    # Seed Equipment
    equipments_data = [
        ("EQP-CNC-01", "Torno CNC Alta Precisão 5 Eixos", "Usinagem & CNC", "SN-CNC-88941", "Nave Industrial A1", "Ativo", now_str),
        ("EQP-HYD-04", "Prensa Hidráulica 200 Toneladas", "Hidráulica", "SN-HYD-77210", "Nave Industrial B2", "Em Manutenção", now_str),
        ("EQP-HVAC-02", "Chiller Industrial Climatização Central 50kW", "HVAC & Frio", "SN-HVAC-44109", "Cobertura Bloco C", "Ativo", now_str),
        ("EQP-ROB-07", "Braço Robótico de Soldadura KUKA 6-Eixos", "Automação", "SN-KUKA-99231", "Linha de Montagem L3", "Ativo", now_str),
        ("EQP-COMP-03", "Compressor de Ar de Parafuso Atlas Copco", "Pneumática", "SN-COMP-33012", "Central de Fluidos", "Ativo", now_str),
        ("EQP-GEN-01", "Gerador Diesel Emergência 500 kVA", "Elétrica & Energia", "SN-GEN-55190", "Subestação Principal", "Ativo", now_str)
    ]
    cursor.executemany("""
    INSERT INTO equipment (equipment_code, name, category, serial_number, location, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, equipments_data)

    # Seed Technicians
    technicians_data = [
        ("Eng. Enmanuel Jimenez", "Eletromecânica & Automação", "enmanuel.jimenez@ejajtech.com", "+351 911 151 993", "Disponível", now_str),
        ("Carlos Oliveira", "Hidráulica & Pneumática", "carlos.oliveira@maintaincraft.io", "+351 912 345 678", "Em Intervenção", now_str),
        ("Sofia Martins", "HVAC & Termodinâmica", "sofia.martins@maintaincraft.io", "+351 913 888 777", "Disponível", now_str),
        ("Miguel Fernandes", "Manutenção Preditiva & Robótica", "miguel.fernandes@maintaincraft.io", "+351 914 222 333", "Disponível", now_str)
    ]
    cursor.executemany("""
    INSERT INTO technicians (name, specialty, email, phone, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, technicians_data)

    # Seed Maintenances
    maintenances_data = [
        ("OT-2026-101", 1, 1, "Preventiva", "Média", (today - timedelta(days=2)).strftime("%Y-%m-%d"), (today - timedelta(days=2)).strftime("%Y-%m-%d 16:30"), 3.5, 175.0, 320.0, 495.0, "Substituição de fluído refrigerante e calibração de eixos CNC.", "Concluído", now_str),
        ("OT-2026-102", 2, 2, "Corretiva", "Urgente", today.strftime("%Y-%m-%d"), None, 4.0, 200.0, 850.0, 1050.0, "Vazamento no retentor principal do cilindro hidráulico de pressão.", "Em Execução", now_str),
        ("OT-2026-103", 3, 3, "Preventiva", "Baixa", (today + timedelta(days=3)).strftime("%Y-%m-%d"), None, 2.0, 100.0, 120.0, 220.0, "Limpeza de filtros de ar e verificação de pressão do gás R410A.", "Agendado", now_str),
        ("OT-2026-104", 4, 4, "Preditiva", "Alta", (today + timedelta(days=5)).strftime("%Y-%m-%d"), None, 3.0, 150.0, 450.0, 600.0, "Análise de vibração nos redutores dos servo-motores das juntas 2 e 3.", "Agendado", now_str),
        ("OT-2026-105", 5, 1, "Preventiva", "Média", (today + timedelta(days=10)).strftime("%Y-%m-%d"), None, 1.5, 75.0, 90.0, 165.0, "Troca de óleo sintético do compresso e filtro de admissão.", "Agendado", now_str)
    ]
    cursor.executemany("""
    INSERT INTO maintenances (order_code, equipment_id, technician_id, type, priority, scheduled_date, completed_date, estimated_hours, labor_cost, parts_cost, total_cost, description, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, maintenances_data)

    # Seed Incidents
    incidents_data = [
        ("INC-8901", 2, "João Silva (Operador Linha B)", "Alta", "Prensa com queda súbita de barométrico durante ciclo de moldagem.", "Em Reparação", (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), None),
        ("INC-8902", 1, "Maria Santos (Qualidade)", "Baixa", "Ruído atípico no fuso principal em rotações superiores a 4000 RPM.", "Aberto", today.strftime("%Y-%m-%d %H:%M"), None),
        ("INC-8899", 6, "Pedro Costa (Supervisor)", "Média", "Alarme de bateria de arranque fraca em teste semanal sem carga.", "Resolvido", (today - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"), (today - timedelta(days=4)).strftime("%Y-%m-%d %H:%M"))
    ]
    cursor.executemany("""
    INSERT INTO incidents (incident_code, equipment_id, reported_by, severity, description, status, reported_at, resolved_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, incidents_data)

    # Seed Intervention Logs
    logs_data = [
        (1, None, "Conclusão de Manutenção Preventiva CNC", "Eng. Enmanuel Jimenez", "Fluído sintético Coolant 20L, Óleo lubrificante ISO VG 68", 495.0, (today - timedelta(days=2)).strftime("%Y-%m-%d 16:30"), "Equipamento testado sob carga de 100%. Tolerâncias geométricas validadas."),
        (2, 1, "Início de Intervenção Corretiva Urgente", "Carlos Oliveira", "Kit de selos hidráulicos NBR-70, 50L de óleo hidráulico ISO 46", 1050.0, today.strftime("%Y-%m-%d 09:15"), "Desmontagem do cilindro em curso na bancada de manutenção."),
        (None, 3, "Resolução de Incidência em Gerador", "Eng. Enmanuel Jimenez", "Bateria Varta 12V 100Ah Heavy Duty", 180.0, (today - timedelta(days=4)).strftime("%Y-%m-%d 14:20"), "Bateria substituída e teste de arranque em rampa concluído com sucesso.")
    ]
    cursor.executemany("""
    INSERT INTO intervention_logs (maintenance_id, incident_id, action, technician, parts_used, cost, timestamp, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, logs_data)

    conn.commit()
    conn.close()
    print("[Database OK] maintaincraft.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
