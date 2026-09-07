import os
import sqlite3
import json
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'workorders.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Work Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            client_name TEXT NOT NULL,
            client_company TEXT NOT NULL,
            client_address TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            technician_name TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Média',
            status TEXT NOT NULL DEFAULT 'Pendente',
            title TEXT NOT NULL,
            problem_description TEXT NOT NULL,
            resolution_notes TEXT DEFAULT '',
            labor_hours REAL DEFAULT 0.0,
            labor_rate REAL DEFAULT 35.0,
            subtotal_materials REAL DEFAULT 0.0,
            total_cost REAL DEFAULT 0.0,
            photo_urls TEXT DEFAULT '[]',
            signature_data TEXT,
            signed_by_name TEXT,
            signed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Materials Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price REAL NOT NULL DEFAULT 0.0,
            total_price REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (work_order_id) REFERENCES work_orders (id) ON DELETE CASCADE
        )
    ''')

    # Technicians Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS technicians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Disponível'
        )
    ''')

    conn.commit()

    # Seed demo data if empty
    cursor.execute('SELECT COUNT(*) FROM work_orders')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    demo_sign = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK8AAAA8CAYAAAC6fH4/AAA..."

    # Technicians
    techs = [
        ("Carlos Rocha", "Técnico Sénior AVAC & Refrigeração", "+351 912 345 678", "carlos.rocha@ejajtech-services.pt", "Ocupado"),
        ("Bruno Ferreira", "Eletricista Industrial & Quadros", "+351 913 456 789", "bruno.ferreira@ejajtech-services.pt", "Disponível"),
        ("David Neves", "Automação & Mecânica de Precisão", "+351 914 567 890", "david.neves@ejajtech-services.pt", "Disponível")
    ]
    cursor.executemany('''
        INSERT INTO technicians (name, specialty, phone, email, status)
        VALUES (?, ?, ?, ?, ?)
    ''', techs)

    # Photos json
    sample_photos = json.dumps([
        "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1581092335397-9583fe92d232?auto=format&fit=crop&w=600&q=80"
    ])

    # Work Order 1 (Completed & Signed)
    cursor.execute('''
        INSERT INTO work_orders (
            code, client_name, client_company, client_address, client_phone,
            technician_name, priority, status, title, problem_description,
            resolution_notes, labor_hours, labor_rate, subtotal_materials, total_cost,
            photo_urls, signature_data, signed_by_name, signed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'OT-2026-1001', 'Eng. Manuel Ribeiro', 'Fábrica de Plásticos do Norte S.A.', 'Zona Industrial da Maia, Lote 45, Porto', '+351 919 888 777',
        'Carlos Rocha', 'Alta', 'Concluída',
        'Manutenção Preventiva & Troca de Compressor de Chiller Industrial',
        'O sistema de refrigeração principal apresenta vibração excessiva e perda de pressão de gás refrigerante no circuito 2.',
        'Efetuada descarga e reciclagem do gás R134a. Substituição do filtro secador, válvulas de expansão e recarga de 12kg de gás. Testes de estanqueidade conformes.',
        4.5, 40.00, 480.00, 660.00,
        sample_photos, demo_sign, 'Eng. Manuel Ribeiro', now_str
    ))
    wo1_id = cursor.lastrowid

    materials1 = [
        (wo1_id, 'Filtro Secador Danfoss DCL 305', 2, 45.00, 90.00),
        (wo1_id, 'Gás Refrigerante R134a (Garrafa 12kg)', 1, 240.00, 240.00),
        (wo1_id, 'Válvula de Expansão Termostática TE2', 2, 75.00, 150.00)
    ]
    cursor.executemany('INSERT INTO work_order_materials (work_order_id, item_name, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)', materials1)

    # Work Order 2 (In Progress)
    cursor.execute('''
        INSERT INTO work_orders (
            code, client_name, client_company, client_address, client_phone,
            technician_name, priority, status, title, problem_description,
            resolution_notes, labor_hours, labor_rate, subtotal_materials, total_cost
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'OT-2026-1002', 'Dra. Sofia Martins', 'Hotel Quinta da Marinha Luxe', 'Avenida da Marina 12, Cascais', '+351 918 777 666',
        'Bruno Ferreira', 'Urgente / Crítica', 'Em Progresso',
        'Reparação de Quadro Elétrico Principal & Disjuntor Geral de Potência',
        'Corte de energia no piso 2 do hotel devido a disparo contínuo do disjuntor diferencial por sobrecarga.',
        'Identificado curto-circuito na linha secundária de iluminação do restaurante. Em fase de substituição de cablagem.',
        3.0, 35.00, 310.00, 415.00
    ))
    wo2_id = cursor.lastrowid

    materials2 = [
        (wo2_id, 'Disjuntor Magnetotérmico Schneider 63A 4P', 1, 190.00, 190.00),
        (wo2_id, 'Cabo Elétrico Semirrígido 5x6mm (Metros)', 15, 8.00, 120.00)
    ]
    cursor.executemany('INSERT INTO work_order_materials (work_order_id, item_name, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)', materials2)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados workorders.db inicializada com sucesso para Proyecto 51!")
