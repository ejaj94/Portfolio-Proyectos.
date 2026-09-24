import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'rentacar.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Vehículos (Fleet)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT UNIQUE NOT NULL,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            category TEXT NOT NULL, -- SUV, Sedán, Desportivo, Compacto, Elétrico, Premium
            year INTEGER NOT NULL,
            transmission TEXT NOT NULL, -- Automático, Manual
            fuel_type TEXT NOT NULL, -- Gasolina, Diesel, Elétrico, Híbrido
            daily_rate REAL NOT NULL,
            mileage INTEGER NOT NULL,
            fuel_level INTEGER DEFAULT 100, -- percentagem
            status TEXT DEFAULT 'Disponível', -- Disponível, Alugado, Manutenção, Lavagem
            seats INTEGER NOT NULL,
            deposit REAL NOT NULL, -- Franquia / Caução
            features TEXT NOT NULL,
            image_icon TEXT NOT NULL
        )
    ''')
    
    # 2. Clientes (Drivers / Customers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            license_number TEXT UNIQUE NOT NULL,
            license_expiry DATE NOT NULL,
            nationality TEXT NOT NULL,
            client_type TEXT DEFAULT 'Particular', -- Particular, VIP, Empresa
            notes TEXT,
            total_rentals INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Reservas (Rentals / Bookings)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rental_code TEXT UNIQUE NOT NULL,
            vehicle_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            pickup_location TEXT NOT NULL,
            return_location TEXT NOT NULL,
            total_days INTEGER NOT NULL,
            daily_price REAL NOT NULL,
            extras_price REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            paid_amount REAL DEFAULT 0,
            deposit_amount REAL NOT NULL,
            status TEXT DEFAULT 'Confirmada', -- Confirmada, Em Curso, Concluído, Cancelada
            payment_status TEXT DEFAULT 'Pendente', -- Pendente, Pago Parcial, Pago Total
            extras TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # 4. Contratos & Vistorias (Contracts & Inspections)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_number TEXT UNIQUE NOT NULL,
            rental_id INTEGER NOT NULL,
            initial_mileage INTEGER NOT NULL,
            final_mileage INTEGER,
            initial_fuel INTEGER NOT NULL,
            final_fuel INTEGER,
            insurance_type TEXT NOT NULL, -- Básico, Cobertura Total (CDW VIP)
            terms_accepted INTEGER DEFAULT 1,
            notes TEXT,
            signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rental_id) REFERENCES rentals(id)
        )
    ''')
    
    # 5. Precios & Tarifas Sazonais (Pricing Rules)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            season TEXT NOT NULL, -- Época Alta, Época Baixa, Fim de Semana, Longa Duração
            multiplier REAL NOT NULL,
            min_days INTEGER DEFAULT 1,
            description TEXT NOT NULL
        )
    ''')
    
    # 6. Pagos (Payments & Deposits)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rental_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_type TEXT NOT NULL, -- Aluguer, Caução, Extras, Extensão
            method TEXT NOT NULL, -- Cartão de Crédito, MB Way, Transferência, Dinheiro
            status TEXT DEFAULT 'Concluído',
            reference TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rental_id) REFERENCES rentals(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # Seed Data
    cursor.execute('SELECT COUNT(*) FROM vehicles')
    if cursor.fetchone()[0] == 0:
        seed_vehicles = [
            ('AA-21-TX', 'Mercedes-Benz', 'Classe A 200 AMG Line', 'Premium', 2024, 'Automático', 'Gasolina', 85.00, 14200, 100, 'Disponível', 5, 800.00, 'GPS, Apple CarPlay, Sensores 360°, Cruise Control', 'fa-car-side'),
            ('77-XX-99', 'BMW', 'Série 4 Cabrio M Sport', 'Desportivo', 2024, 'Automático', 'Gasolina', 160.00, 8900, 95, 'Alugado', 4, 1500.00, 'Capota Elétrica, Bancos Desportivos, Áudio Harman Kardon', 'fa-car'),
            ('44-ZZ-12', 'Tesla', 'Model 3 Long Range AWD', 'Elétrico', 2024, 'Automático', 'Elétrico', 110.00, 19500, 90, 'Disponível', 5, 1000.00, 'Autopilot, Teto Panorâmico, Carregamento Supercharger', 'fa-bolt'),
            ('88-MM-34', 'Porsche', 'Macan GTS 440cv', 'SUV', 2023, 'Automático', 'Gasolina', 240.00, 22100, 100, 'Alugado', 5, 2500.00, 'Tração 4x4, Suspensão Pneumática, Escape Desportivo', 'fa-truck-monster'),
            ('33-BB-77', 'Audi', 'Q5 S-Line 40 TDI quattro', 'SUV', 2023, 'Automático', 'Diesel', 125.00, 31000, 100, 'Lavagem', 5, 1200.00, 'Virtual Cockpit, Faróis Matrix LED, Mala Elétrica', 'fa-car-rear'),
            ('11-CC-55', 'Volkswagen', 'Golf 8 R-Line 1.5 eTSI', 'Compacto', 2024, 'Automático', 'Híbrido', 65.00, 11400, 85, 'Manutenção', 5, 600.00, 'Cockpit Digital, Sensores Estacionamento, Baixo Consumo', 'fa-car-side')
        ]
        cursor.executemany('''
            INSERT INTO vehicles (plate, brand, model, category, year, transmission, fuel_type, daily_rate, mileage, fuel_level, status, seats, deposit, features, image_icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_vehicles)
        
        seed_clients = [
            ('Ricardo Silveira', 'ricardo.silveira@corp.pt', '+351 915 889 123', 'CC 15998844', '2029-08-15', 'Portugal', 'VIP', 'Cliente frequente de frotas executivas. Exige sempre veículos higienizados.', 5),
            ('Sophie Laurent', 'sophie.laurent@paris-invest.fr', '+33 6 45 88 12 90', 'FR-99887711', '2028-04-20', 'França', 'Particular', 'Reserva de férias para o Algarve. Solicitou cadeira de criança.', 2),
            ('Alexander Wright', 'alex.wright@londontech.uk', '+44 7911 123456', 'UK-55443322', '2030-11-05', 'Reino Unido', 'Empresa', 'Gestor de eventos corporate, faturação direta à empresa.', 4)
        ]
        cursor.executemany('''
            INSERT INTO clients (full_name, email, phone, license_number, license_expiry, nationality, client_type, notes, total_rentals)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_clients)
        
        today = datetime.now()
        start_1 = (today - timedelta(days=2)).strftime('%Y-%m-%d')
        end_1 = (today + timedelta(days=3)).strftime('%Y-%m-%d')
        
        start_2 = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        end_2 = (today + timedelta(days=4)).strftime('%Y-%m-%d')
        
        seed_rentals = [
            ('ALUG-501', 2, 1, start_1, end_1, 'Aeroporto de Lisboa', 'Aeroporto de Lisboa', 5, 160.00, 100.00, 900.00, 900.00, 1500.00, 'Em Curso', 'Pago Total', 'Seguro VIP Total (CDW), GPS'),
            ('ALUG-502', 4, 3, start_2, end_2, 'Aeroporto de Faro', 'Aeroporto de Faro', 5, 240.00, 150.00, 1350.00, 500.00, 2500.00, 'Em Curso', 'Pago Parcial', 'Condutor Adicional, Cobertura Pneus & Vidros')
        ]
        cursor.executemany('''
            INSERT INTO rentals (rental_code, vehicle_id, client_id, start_date, end_date, pickup_location, return_location, total_days, daily_price, extras_price, total_amount, paid_amount, deposit_amount, status, payment_status, extras)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_rentals)
        
        seed_contracts = [
            ('CONT-2026-001', 1, 8900, None, 95, None, 'Cobertura Total (CDW VIP)', 1, 'Inspeção inicial realizada sem danos assinalados. Vistoria digital aprovada.'),
            ('CONT-2026-002', 2, 22100, None, 100, None, 'Cobertura Total (CDW VIP)', 1, 'Entregue no Terminal VIP do Aeroporto de Faro com depósito atestado.')
        ]
        cursor.executemany('''
            INSERT INTO contracts (contract_number, rental_id, initial_mileage, final_mileage, initial_fuel, final_fuel, insurance_type, terms_accepted, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_contracts)
        
        seed_pricing = [
            ('Tarifa Base Época Padrão', 'Todos', 'Época Baixa', 1.0, 1, 'Preço de tabela diário padrão durante a semana.'),
            ('Pack Fim de Semana Veloz', 'Desportivo / Premium', 'Fim de Semana', 1.25, 2, 'Acréscimo de 25% para alugueres de Sexta a Domingo.'),
            ('Tarifa Verão & Férias (High Season)', 'SUV / Desportivo', 'Época Alta', 1.45, 3, 'Tarifa dinâmica para picos de procura turística de verão.'),
            ('Desconto Semanal Long-Term (7+ dias)', 'Todos', 'Longa Duração', 0.85, 7, 'Desconto automático de 15% para estadias de 7 ou mais dias.')
        ]
        cursor.executemany('''
            INSERT INTO pricing_rules (title, category, season, multiplier, min_days, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_pricing)
        
        seed_payments = [
            (1, 1, 900.00, 'Aluguer', 'Cartão de Crédito', 'Concluído', 'PAY-CAR-9912'),
            (1, 1, 1500.00, 'Caução', 'Cartão de Crédito (Retenção)', 'Retido', 'DEP-HOLD-9912'),
            (2, 3, 500.00, 'Aluguer', 'Transferência Bancária', 'Concluído', 'PAY-CAR-4411'),
            (2, 3, 2500.00, 'Caução', 'Cartão de Crédito (Retenção)', 'Retido', 'DEP-HOLD-4411')
        ]
        cursor.executemany('''
            INSERT INTO payments (rental_id, client_id, amount, payment_type, method, status, reference)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_payments)
        
        conn.commit()
    conn.close()

# Vehicle Operations
def get_all_vehicles():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles ORDER BY brand ASC, model ASC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_vehicle(plate, brand, model, category, year, transmission, fuel_type, daily_rate, mileage, fuel_level, seats, deposit, features, image_icon):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicles (plate, brand, model, category, year, transmission, fuel_type, daily_rate, mileage, fuel_level, status, seats, deposit, features, image_icon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Disponível', ?, ?, ?, ?)
    ''', (plate, brand, model, category, year, transmission, fuel_type, daily_rate, mileage, fuel_level, seats, deposit, features, image_icon))
    vid = cursor.lastrowid
    conn.commit()
    conn.close()
    return vid

def update_vehicle_status(vehicle_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE vehicles SET status = ? WHERE id = ?', (status, vehicle_id))
    conn.commit()
    conn.close()

# Client Operations
def get_all_clients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients ORDER BY total_rentals DESC, full_name ASC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_client(full_name, email, phone, license_number, license_expiry, nationality, client_type, notes):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (full_name, email, phone, license_number, license_expiry, nationality, client_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (full_name, email, phone, license_number, license_expiry, nationality, client_type, notes))
    cid = cursor.lastrowid
    conn.commit()
    conn.close()
    return cid

# Availability Check
def check_vehicle_availability(start_date, end_date, category=None):
    conn = get_db()
    cursor = conn.cursor()
    query = '''
        SELECT v.* FROM vehicles v
        WHERE v.status != 'Manutenção'
        AND v.id NOT IN (
            SELECT r.vehicle_id FROM rentals r
            WHERE r.status IN ('Confirmada', 'Em Curso')
            AND (
                (r.start_date <= ? AND r.end_date > ?) OR
                (r.start_date < ? AND r.end_date >= ?) OR
                (r.start_date >= ? AND r.end_date <= ?)
            )
        )
    '''
    params = [start_date, start_date, end_date, end_date, start_date, end_date]
    if category and category != 'Todas':
        query += ' AND v.category = ?'
        params.append(category)
        
    query += ' ORDER BY v.daily_rate ASC'
    cursor.execute(query, params)
    available = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return available

# Rentals & Bookings
def get_all_rentals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.*, v.brand, v.model, v.plate, v.category, v.transmission, c.full_name as client_name, c.phone as client_phone, c.license_number
        FROM rentals r
        JOIN vehicles v ON r.vehicle_id = v.id
        JOIN clients c ON r.client_id = c.id
        ORDER BY r.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def create_rental(vehicle_id, client_id, start_date, end_date, pickup_loc, return_loc, total_days, daily_price, extras_price, total_amount, paid_amount, deposit_amount, extras, insurance_type):
    conn = get_db()
    cursor = conn.cursor()
    
    import random
    code = f"ALUG-{random.randint(100, 999)}"
    pay_status = 'Pago Total' if paid_amount >= total_amount else ('Pago Parcial' if paid_amount > 0 else 'Pendente')
    
    cursor.execute('''
        INSERT INTO rentals (rental_code, vehicle_id, client_id, start_date, end_date, pickup_location, return_location, total_days, daily_price, extras_price, total_amount, paid_amount, deposit_amount, status, payment_status, extras)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmada', ?, ?)
    ''', (code, vehicle_id, client_id, start_date, end_date, pickup_loc, return_loc, total_days, daily_price, extras_price, total_amount, paid_amount, deposit_amount, pay_status, extras))
    rental_id = cursor.lastrowid
    
    # Generate Contract
    contract_num = f"CONT-2026-{rental_id:03d}"
    cursor.execute('SELECT mileage, fuel_level FROM vehicles WHERE id = ?', (vehicle_id,))
    v_data = cursor.fetchone()
    init_km = v_data['mileage'] if v_data else 10000
    init_fuel = v_data['fuel_level'] if v_data else 100
    
    cursor.execute('''
        INSERT INTO contracts (contract_number, rental_id, initial_mileage, initial_fuel, insurance_type, terms_accepted, notes)
        VALUES (?, ?, ?, ?, ?, 1, 'Contrato gerado e validado digitalmente.')
    ''', (contract_num, rental_id, init_km, init_fuel, insurance_type))
    
    # Register Initial Payment
    if paid_amount > 0:
        pay_ref = f"PAY-CAR-{random.randint(1000, 9999)}"
        cursor.execute('''
            INSERT INTO payments (rental_id, client_id, amount, payment_type, method, status, reference)
            VALUES (?, ?, ?, 'Aluguer', 'Cartão de Crédito', 'Concluído', ?)
        ''', (rental_id, client_id, paid_amount, pay_ref))
        
    # Update Client total rentals
    cursor.execute('UPDATE clients SET total_rentals = total_rentals + 1 WHERE id = ?', (client_id,))
    
    # Update vehicle status if start is today
    today_str = datetime.now().strftime('%Y-%m-%d')
    if start_date == today_str:
        cursor.execute("UPDATE vehicles SET status = 'Alugado' WHERE id = ?", (vehicle_id,))
        
    conn.commit()
    conn.close()
    return rental_id, code, contract_num

def update_rental_status(rental_id, new_status, final_km=None, final_fuel=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT vehicle_id FROM rentals WHERE id = ?', (rental_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
        
    vehicle_id = row['vehicle_id']
    cursor.execute('UPDATE rentals SET status = ? WHERE id = ?', (new_status, rental_id))
    
    if new_status == 'Em Curso':
        cursor.execute("UPDATE vehicles SET status = 'Alugado' WHERE id = ?", (vehicle_id,))
    elif new_status == 'Concluído':
        cursor.execute("UPDATE vehicles SET status = 'Lavagem' WHERE id = ?", (vehicle_id,))
        if final_km:
            cursor.execute("UPDATE vehicles SET mileage = ? WHERE id = ?", (final_km, vehicle_id))
            cursor.execute("UPDATE contracts SET final_mileage = ?, final_fuel = ? WHERE rental_id = ?", (final_km, final_fuel or 100, rental_id))
    elif new_status == 'Cancelada':
        cursor.execute("UPDATE vehicles SET status = 'Disponível' WHERE id = ?", (vehicle_id,))
        
    conn.commit()
    conn.close()
    return True

# Contracts
def get_all_contracts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, r.rental_code, r.start_date, r.end_date, r.total_amount, v.plate, v.brand, v.model, cl.full_name as client_name, cl.license_number
        FROM contracts c
        JOIN rentals r ON c.rental_id = r.id
        JOIN vehicles v ON r.vehicle_id = v.id
        JOIN clients cl ON r.client_id = cl.id
        ORDER BY c.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# Pricing
def get_all_pricing():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pricing_rules ORDER BY multiplier DESC')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_pricing_rule(title, category, season, multiplier, min_days, description):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pricing_rules (title, category, season, multiplier, min_days, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, category, season, multiplier, min_days, description))
    conn.commit()
    conn.close()

# Payments
def get_all_payments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, r.rental_code, cl.full_name as client_name
        FROM payments p
        JOIN rentals r ON p.rental_id = r.id
        JOIN clients cl ON p.client_id = cl.id
        ORDER BY p.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_payment(rental_id, amount, payment_type, method):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT client_id, total_amount, paid_amount FROM rentals WHERE id = ?', (rental_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
        
    client_id = row['client_id']
    import random
    ref = f"PAY-CAR-{random.randint(10000, 99999)}"
    cursor.execute('''
        INSERT INTO payments (rental_id, client_id, amount, payment_type, method, status, reference)
        VALUES (?, ?, ?, ?, ?, 'Concluído', ?)
    ''', (rental_id, client_id, amount, payment_type, method, ref))
    
    if payment_type == 'Aluguer':
        new_paid = row['paid_amount'] + amount
        total = row['total_amount']
        new_pay_status = 'Pago Total' if new_paid >= total else 'Pago Parcial'
        cursor.execute('UPDATE rentals SET paid_amount = ?, payment_status = ? WHERE id = ?', (new_paid, new_pay_status, rental_id))
        
    conn.commit()
    conn.close()
    return ref

# Dashboard KPIs
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    # Fleet counts
    cursor.execute('''
        SELECT 
            COUNT(*) as total_fleet,
            SUM(CASE WHEN status="Disponível" THEN 1 ELSE 0 END) as available_fleet,
            SUM(CASE WHEN status="Alugado" THEN 1 ELSE 0 END) as rented_fleet,
            SUM(CASE WHEN status="Lavagem" THEN 1 ELSE 0 END) as washing_fleet,
            SUM(CASE WHEN status="Manutenção" THEN 1 ELSE 0 END) as maintenance_fleet
        FROM vehicles
    ''')
    f_stats = dict(cursor.fetchone())
    total_fleet = f_stats['total_fleet'] or 1
    rented_fleet = f_stats['rented_fleet'] or 0
    fleet_utilization = round((rented_fleet / total_fleet) * 100, 1)
    
    # Financials
    cursor.execute('SELECT SUM(amount) as total_revenue FROM payments WHERE status = "Concluído" AND payment_type != "Caução"')
    total_revenue = cursor.fetchone()['total_revenue'] or 0.0
    
    cursor.execute('SELECT SUM(amount) as active_deposits FROM payments WHERE payment_type = "Caução" AND status = "Retido"')
    active_deposits = cursor.fetchone()['active_deposits'] or 0.0
    
    # Active Rentals
    cursor.execute('SELECT COUNT(*) as active_rentals FROM rentals WHERE status IN ("Confirmada", "Em Curso")')
    active_rentals = cursor.fetchone()['active_rentals'] or 0
    
    # Today deliveries & returns
    today_str = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) as today_pickups FROM rentals WHERE start_date = ? AND status = "Confirmada"', (today_str,))
    today_pickups = cursor.fetchone()['today_pickups'] or 0
    
    cursor.execute('SELECT COUNT(*) as today_returns FROM rentals WHERE end_date = ? AND status = "Em Curso"', (today_str,))
    today_returns = cursor.fetchone()['today_returns'] or 0
    
    conn.close()
    return {
        "total_fleet": total_fleet,
        "available_fleet": f_stats['available_fleet'] or 0,
        "rented_fleet": rented_fleet,
        "washing_fleet": f_stats['washing_fleet'] or 0,
        "maintenance_fleet": f_stats['maintenance_fleet'] or 0,
        "fleet_utilization": fleet_utilization,
        "total_revenue": total_revenue,
        "active_deposits": active_deposits,
        "active_rentals": active_rentals,
        "today_pickups": today_pickups,
        "today_returns": today_returns
    }
