import os
import sqlite3
from datetime import datetime, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'fleet.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Vehicles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT UNIQUE NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            category TEXT NOT NULL,
            year INTEGER NOT NULL,
            fuel_type TEXT NOT NULL,
            current_km INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Operacional',
            driver_name TEXT DEFAULT 'Não Atribuído',
            insurance_expiry TEXT NOT NULL,
            itv_expiry TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Drivers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            license_number TEXT UNIQUE NOT NULL,
            license_category TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            assigned_vehicle_plate TEXT DEFAULT 'Nenhum'
        )
    ''')

    # Fuel Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            vehicle_plate TEXT NOT NULL,
            fill_date TEXT NOT NULL,
            liters REAL NOT NULL,
            total_cost REAL NOT NULL,
            km_at_fill INTEGER NOT NULL,
            avg_consumption REAL NOT NULL DEFAULT 0.0,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE CASCADE
        )
    ''')

    # Maintenances Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            vehicle_plate TEXT NOT NULL,
            maint_type TEXT NOT NULL,
            description TEXT NOT NULL,
            maint_date TEXT NOT NULL,
            km_at_maint INTEGER NOT NULL,
            cost REAL NOT NULL,
            next_due_date TEXT,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE CASCADE
        )
    ''')

    # Alerts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            vehicle_plate TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT NOT NULL DEFAULT 'warning',
            is_resolved INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed demo data if empty
    cursor.execute('SELECT COUNT(*) FROM vehicles')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    today = datetime.now()
    t_str = today.strftime("%Y-%m-%d")
    next_month = (today + timedelta(days=25)).strftime("%Y-%m-%d")
    next_week = (today + timedelta(days=7)).strftime("%Y-%m-%d")

    # Drivers
    drivers = [
        ("João Silva", "C-889977", "Classe C + CE (Pesados)", "+351 912 345 678", "joao.silva@translogis.pt", "45-AB-89"),
        ("Pedro Santos", "B-554433", "Classe B (Ligeiros)", "+351 913 456 789", "pedro.santos@translogis.pt", "78-CD-12"),
        ("Maria Costa", "B-112233", "Classe B (Ligeiros Executivos)", "+351 914 567 890", "maria.costa@translogis.pt", "99-EF-34")
    ]
    cursor.executemany('''
        INSERT INTO drivers (name, license_number, license_category, phone, email, assigned_vehicle_plate)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', drivers)

    # Vehicles
    vehicles = [
        ("45-AB-89", "Volvo", "FH16 750 (Camião)", "Camião Pesado de Mercadorias", 2023, "Diesel", 145200, "Operacional", "João Silva", "2026-11-30", "2026-10-15"),
        ("78-CD-12", "Mercedes-Benz", "Sprinter 316 CDI", "Carrinha Comercial", 2022, "Diesel", 89400, "Operacional", "Pedro Santos", "2026-09-28", next_week),
        ("99-EF-34", "Volkswagen", "Golf Variant 2.0 TDI", "Ligeiro Executivo", 2024, "Diesel", 32100, "Operacional", "Maria Costa", "2026-12-15", "2027-01-20"),
        ("12-GH-56", "Renault", "Master Van H2L2", "Carrinha Comercial", 2021, "Diesel", 178900, "Em Manutenção", "Não Atribuído", "2026-09-15", "2026-09-12")
    ]
    cursor.executemany('''
        INSERT INTO vehicles (plate, brand, model, category, year, fuel_type, current_km, status, driver_name, insurance_expiry, itv_expiry)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', vehicles)

    # Fuel Logs
    fuel_logs = [
        (1, "45-AB-89", t_str, 350.0, 560.00, 145200, 28.5),
        (2, "78-CD-12", t_str, 65.0, 104.00, 89400, 8.2),
        (3, "99-EF-34", t_str, 45.0, 72.00, 32100, 5.4),
        (4, "12-GH-56", "2026-09-01", 70.0, 112.00, 178500, 9.1)
    ]
    cursor.executemany('''
        INSERT INTO fuel_logs (vehicle_id, vehicle_plate, fill_date, liters, total_cost, km_at_fill, avg_consumption)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', fuel_logs)

    # Maintenances
    maintenances = [
        (1, "45-AB-89", "Mudança de Óleo & Filtros", "Substituição completa de óleo sintético e filtro de combustível pesados.", "2026-08-15", 140000, 480.00, "2026-12-01"),
        (2, "78-CD-12", "Troca de Pneus Dianteiros", "Troca de 2 pneus Michelin Agilis 225/65 R16.", "2026-07-10", 85000, 260.00, "2027-01-10"),
        (4, "12-GH-56", "Revisão de Travões & Discos", "Substituição de pastilhas de travão e retificação de discos.", t_str, 178900, 350.00, "2026-11-01")
    ]
    cursor.executemany('''
        INSERT INTO maintenances (vehicle_id, vehicle_plate, maint_type, description, maint_date, km_at_maint, cost, next_due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', maintenances)

    # Alerts
    alerts = [
        (2, "78-CD-12", "Inspeção Periódica (ITV/IPO) Próxima", f"A inspeção técnica do veículo 78-CD-12 caduca a {next_week}. Agendar IPO com urgência.", "danger", 0),
        (4, "12-GH-56", "Seguro Automóvel por Expire", "O seguro da carrinha 12-GH-56 caduca em 2026-09-15. Renovar apólice.", "warning", 0),
        (1, "45-AB-89", "Revisão de Rodagem Atingida", "Camião 45-AB-89 superou os 145 000 km. Verificar estado de discos.", "info", 0)
    ]
    cursor.executemany('''
        INSERT INTO alerts (vehicle_id, vehicle_plate, title, message, severity, is_resolved)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', alerts)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados fleet.db inicializada com sucesso para Proyecto 50!")
