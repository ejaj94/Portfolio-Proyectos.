import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'hotel_booking.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Habitaciones (Rooms)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            title TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            base_price REAL NOT NULL,
            status TEXT DEFAULT 'Disponível', -- Disponível, Ocupado, Limpeza, Manutenção
            floor INTEGER NOT NULL,
            amenities TEXT NOT NULL,
            icon TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # 2. Clientes (Guests / Customers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            document_id TEXT NOT NULL,
            nationality TEXT NOT NULL,
            vip_level TEXT DEFAULT 'Standard', -- Standard, Silver VIP, Gold VIP, Platinum VIP
            notes TEXT,
            total_stays INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Reservas (Bookings)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_code TEXT UNIQUE NOT NULL,
            room_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            guests_count INTEGER NOT NULL,
            total_price REAL NOT NULL,
            paid_amount REAL DEFAULT 0,
            status TEXT DEFAULT 'Confirmada', -- Confirmada, Check-in, Check-out, Cancelada
            payment_status TEXT DEFAULT 'Pendente', -- Pendente, Pago Parcial, Pago Total
            special_requests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # 4. Precios & Tarifação Dinâmica (Pricing Rules)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pricing_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            season_type TEXT NOT NULL, -- Época Alta, Época Baixa, Fim de Semana, Feriado
            multiplier REAL NOT NULL,
            description TEXT NOT NULL,
            active INTEGER DEFAULT 1
        )
    ''')
    
    # 5. Pagos (Payments)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            method TEXT NOT NULL, -- Cartão de Crédito, Transferência Bancária, MB Way, Dinheiro
            status TEXT DEFAULT 'Concluído',
            reference TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES bookings(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # Seed Data if table is empty
    cursor.execute('SELECT COUNT(*) FROM rooms')
    if cursor.fetchone()[0] == 0:
        seed_rooms = [
            ('101', 'Standard Double', 'Quarto Standard Jardim', 2, 95.00, 'Disponível', 1, 'Wi-Fi 6, Ar Condicionado, TV 4K, Cofre', 'fa-bed', 'Acolhedor quarto duplo com vista para os jardins interiores.'),
            ('102', 'Deluxe Ocean', 'Suite Deluxe Vista Mar', 2, 160.00, 'Ocupado', 1, 'Varanda Privada, Cama King, Banheira Hidromassagem, Frigobar', 'fa-water', 'Elegante suite com vista panorâmica frontal sobre o oceano.'),
            ('201', 'Executive Suite', 'Suite Executiva Grand Panorâmica', 3, 220.00, 'Disponível', 2, 'Sala de Estar, Cama Super King, Máquina Nespresso, Smart TV 65\"', 'fa-gem', 'Espaçosa suite de luxo com zona de reuniões e lounge privado.'),
            ('202', 'Family Comfort', 'Apartamento Familiar Duplex', 4, 190.00, 'Limpeza', 2, 'Dois Quartos, Kitchenette, 2 WC, Área Kids', 'fa-people-roof', 'Ideal para estadias familiares prolongadas com conforto de resort.'),
            ('301', 'Presidential Penthouse', 'Penthouse Presidencial Real', 4, 450.00, 'Confirmada', 3, 'Piscina Privada no Rooftop, Mordomo 24h, Bar Exclusivo, Jacuzzi', 'fa-crown', 'A joia da nossa hotelaria: luxo absoluto com terraço de 120m².'),
            ('302', 'Junior Suite', 'Junior Suite Sunset & Spa', 2, 140.00, 'Manutenção', 3, 'Acesso Grátis ao Spa, Vista Pôr do Sol, Cama Queen', 'fa-spa', 'Ambiente zen e relaxante com acesso direto ao circuito de hidroterapia.')
        ]
        cursor.executemany('''
            INSERT INTO rooms (room_number, room_type, title, capacity, base_price, status, floor, amenities, icon, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_rooms)
        
        seed_clients = [
            ('Henrique Albuquerque', 'henrique.albuquerque@luxmail.pt', '+351 912 345 678', 'CC 14892019', 'Portugal', 'Platinum VIP', 'Prefere travesseiros de penas e champanhe à chegada.', 8),
            ('Charlotte Dupont', 'charlotte.dupont@paris-luxury.fr', '+33 6 12 34 56 78', 'PASS 22FR99812', 'França', 'Gold VIP', 'Check-in tardio habitual, alérgica a marisco.', 4),
            ('Marcus Vance', 'marcus.vance@techinvest.co.uk', '+44 7700 900123', 'PASS 55UK88120', 'Reino Unido', 'Silver VIP', 'Viajante corporativo frequente, necessita de secretária e internet ultrarrápida.', 3),
            ('Elena Morales', 'elena.morales@madrid-exec.es', '+34 600 123 456', 'DNI 50998811K', 'Espanha', 'Standard', 'Reserva de escapadinha de fim de semana com pacote spa.', 1)
        ]
        cursor.executemany('''
            INSERT INTO clients (full_name, email, phone, document_id, nationality, vip_level, notes, total_stays)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_clients)
        
        # Calculate dynamic sample dates
        today = datetime.now()
        d_in_1 = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        d_out_1 = (today + timedelta(days=2)).strftime('%Y-%m-%d')
        
        d_in_2 = (today + timedelta(days=3)).strftime('%Y-%m-%d')
        d_out_2 = (today + timedelta(days=7)).strftime('%Y-%m-%d')
        
        seed_bookings = [
            ('RES-8921', 2, 1, d_in_1, d_out_1, 2, 480.00, 480.00, 'Check-in', 'Pago Total', 'Garrafa de espumante e fruta fresca no quarto.'),
            ('RES-8922', 5, 2, d_in_2, d_out_2, 3, 1800.00, 500.00, 'Confirmada', 'Pago Parcial', 'Transfer privado do aeroporto de Faro solicitado.')
        ]
        cursor.executemany('''
            INSERT INTO bookings (booking_code, room_id, client_id, check_in, check_out, guests_count, total_price, paid_amount, status, payment_status, special_requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_bookings)
        
        seed_pricing = [
            ('Tarifa Padrão Época Média', 'Época Média', 1.0, 'Tarifa regular de referência para reservas durante a semana.'),
            ('Suplemento de Fim de Semana', 'Fim de Semana', 1.25, 'Acréscimo de 25% para noites de Sexta-feira e Sábado.'),
            ('Tarifa Época Alta & Verão', 'Época Alta', 1.50, 'Acréscimo de 50% entre Junho e Setembro para máxima rentabilidade.'),
            ('Desconto Longa Estadia (7+ noites)', 'Promoção', 0.85, 'Desconto automático de 15% para estadias de 7 noites ou mais.')
        ]
        cursor.executemany('''
            INSERT INTO pricing_rules (name, season_type, multiplier, description)
            VALUES (?, ?, ?, ?)
        ''', seed_pricing)
        
        seed_payments = [
            (1, 1, 480.00, 'Cartão de Crédito', 'Concluído', 'PAY-CC-9921'),
            (2, 2, 500.00, 'Transferência Bancária', 'Concluído', 'PAY-TRF-4412')
        ]
        cursor.executemany('''
            INSERT INTO payments (booking_id, client_id, amount, method, status, reference)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_payments)
        
        conn.commit()
    conn.close()

# Room Operations
def get_all_rooms():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms ORDER BY room_number ASC')
    rooms = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rooms

def add_room(room_number, room_type, title, capacity, base_price, floor, amenities, icon, description):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rooms (room_number, room_type, title, capacity, base_price, floor, amenities, icon, description, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Disponível')
    ''', (room_number, room_type, title, capacity, base_price, floor, amenities, icon, description))
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return room_id

def update_room_status(room_id, status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE rooms SET status = ? WHERE id = ?', (status, room_id))
    conn.commit()
    conn.close()

# Client Operations
def get_all_clients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients ORDER BY total_stays DESC, full_name ASC')
    clients = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return clients

def add_client(full_name, email, phone, document_id, nationality, vip_level, notes):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (full_name, email, phone, document_id, nationality, vip_level, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (full_name, email, phone, document_id, nationality, vip_level, notes))
    client_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return client_id

# Availability & Bookings
def check_availability(check_in, check_out, room_type=None):
    conn = get_db()
    cursor = conn.cursor()
    query = '''
        SELECT r.* FROM rooms r
        WHERE r.status != 'Manutenção'
        AND r.id NOT IN (
            SELECT b.room_id FROM bookings b
            WHERE b.status IN ('Confirmada', 'Check-in')
            AND (
                (b.check_in <= ? AND b.check_out > ?) OR
                (b.check_in < ? AND b.check_out >= ?) OR
                (b.check_in >= ? AND b.check_out <= ?)
            )
        )
    '''
    params = [check_in, check_in, check_out, check_out, check_in, check_out]
    if room_type and room_type != 'Todas':
        query += ' AND r.room_type = ?'
        params.append(room_type)
        
    query += ' ORDER BY r.base_price ASC'
    cursor.execute(query, params)
    available_rooms = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return available_rooms

def get_all_bookings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, r.room_number, r.room_type, r.title as room_title, c.full_name as client_name, c.email as client_email, c.phone as client_phone
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN clients c ON b.client_id = c.id
        ORDER BY b.id DESC
    ''')
    bookings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return bookings

def create_booking(room_id, client_id, check_in, check_out, guests_count, total_price, paid_amount, payment_method, special_requests):
    conn = get_db()
    cursor = conn.cursor()
    
    # Generate unique code
    import random
    code = f"RES-{random.randint(1000, 9999)}"
    
    pay_status = 'Pago Total' if paid_amount >= total_price else ('Pago Parcial' if paid_amount > 0 else 'Pendente')
    
    cursor.execute('''
        INSERT INTO bookings (booking_code, room_id, client_id, check_in, check_out, guests_count, total_price, paid_amount, status, payment_status, special_requests)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Confirmada', ?, ?)
    ''', (code, room_id, client_id, check_in, check_out, guests_count, total_price, paid_amount, pay_status, special_requests))
    booking_id = cursor.lastrowid
    
    # If initial payment made, register in payments
    if paid_amount > 0:
        ref_code = f"PAY-{random.randint(10000, 99999)}"
        cursor.execute('''
            INSERT INTO payments (booking_id, client_id, amount, method, status, reference)
            VALUES (?, ?, ?, ?, 'Concluído', ?)
        ''', (booking_id, client_id, paid_amount, payment_method, ref_code))
        
    # Increment client stays count
    cursor.execute('UPDATE clients SET total_stays = total_stays + 1 WHERE id = ?', (client_id,))
    
    # Update room status to Ocupado if check_in is today
    today_str = datetime.now().strftime('%Y-%m-%d')
    if check_in == today_str:
        cursor.execute("UPDATE rooms SET status = 'Ocupado' WHERE id = ?", (room_id,))
        
    conn.commit()
    conn.close()
    return booking_id, code

def update_booking_status(booking_id, new_status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT room_id FROM bookings WHERE id = ?', (booking_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
        
    room_id = row['room_id']
    cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', (new_status, booking_id))
    
    if new_status == 'Check-in':
        cursor.execute("UPDATE rooms SET status = 'Ocupado' WHERE id = ?", (room_id,))
    elif new_status == 'Check-out':
        cursor.execute("UPDATE rooms SET status = 'Limpeza' WHERE id = ?", (room_id,))
    elif new_status == 'Cancelada':
        cursor.execute("UPDATE rooms SET status = 'Disponível' WHERE id = ?", (room_id,))
        
    conn.commit()
    conn.close()
    return True

# Pricing Rules
def get_all_pricing():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pricing_rules ORDER BY multiplier DESC')
    rules = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rules

def add_pricing_rule(name, season_type, multiplier, description):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pricing_rules (name, season_type, multiplier, description)
        VALUES (?, ?, ?, ?)
    ''', (name, season_type, multiplier, description))
    conn.commit()
    conn.close()

# Payments
def get_all_payments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, b.booking_code, c.full_name as client_name
        FROM payments p
        JOIN bookings b ON p.booking_id = b.id
        JOIN clients c ON p.client_id = c.id
        ORDER BY p.id DESC
    ''')
    payments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return payments

def add_payment(booking_id, amount, method):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT client_id, total_price, paid_amount FROM bookings WHERE id = ?', (booking_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
        
    client_id = row['client_id']
    new_paid = row['paid_amount'] + amount
    total = row['total_price']
    new_pay_status = 'Pago Total' if new_paid >= total else 'Pago Parcial'
    
    import random
    ref = f"PAY-{random.randint(10000, 99999)}"
    cursor.execute('''
        INSERT INTO payments (booking_id, client_id, amount, method, status, reference)
        VALUES (?, ?, ?, ?, 'Concluído', ?)
    ''', (booking_id, client_id, amount, method, ref))
    
    cursor.execute('UPDATE bookings SET paid_amount = ?, payment_status = ? WHERE id = ?', (new_paid, new_pay_status, booking_id))
    conn.commit()
    conn.close()
    return ref

# Dashboard KPIs
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    # Total rooms
    cursor.execute('SELECT COUNT(*) as total, SUM(CASE WHEN status="Ocupado" THEN 1 ELSE 0 END) as occupied, SUM(CASE WHEN status="Disponível" THEN 1 ELSE 0 END) as available, SUM(CASE WHEN status="Limpeza" THEN 1 ELSE 0 END) as cleaning, SUM(CASE WHEN status="Manutenção" THEN 1 ELSE 0 END) as maintenance FROM rooms')
    room_stats = dict(cursor.fetchone())
    total_rooms = room_stats['total'] or 1
    occupied_rooms = room_stats['occupied'] or 0
    occupancy_rate = round((occupied_rooms / total_rooms) * 100, 1)
    
    # Financials
    cursor.execute('SELECT SUM(amount) as total_revenue FROM payments WHERE status = "Concluído"')
    total_revenue = cursor.fetchone()['total_revenue'] or 0.0
    
    # Bookings counts
    cursor.execute('SELECT COUNT(*) as active_bookings FROM bookings WHERE status IN ("Confirmada", "Check-in")')
    active_bookings = cursor.fetchone()['active_bookings'] or 0
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) as today_checkins FROM bookings WHERE check_in = ? AND status = "Confirmada"', (today_str,))
    today_checkins = cursor.fetchone()['today_checkins'] or 0
    
    cursor.execute('SELECT COUNT(*) as today_checkouts FROM bookings WHERE check_out = ? AND status = "Check-in"', (today_str,))
    today_checkouts = cursor.fetchone()['today_checkouts'] or 0
    
    # RevPAR (Revenue Per Available Room)
    revpar = round(total_revenue / total_rooms, 2)
    
    conn.close()
    return {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": room_stats['available'] or 0,
        "cleaning_rooms": room_stats['cleaning'] or 0,
        "maintenance_rooms": room_stats['maintenance'] or 0,
        "occupancy_rate": occupancy_rate,
        "total_revenue": total_revenue,
        "active_bookings": active_bookings,
        "today_checkins": today_checkins,
        "today_checkouts": today_checkouts,
        "revpar": revpar
    }
