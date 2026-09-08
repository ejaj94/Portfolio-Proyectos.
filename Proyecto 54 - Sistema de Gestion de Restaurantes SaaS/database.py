import os
import sqlite3
from datetime import datetime, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'restaurant.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Tables Floor Plan Map Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER UNIQUE NOT NULL,
            capacity INTEGER NOT NULL DEFAULT 4,
            status TEXT NOT NULL DEFAULT 'Livre',
            waiter_name TEXT DEFAULT 'Sem Atribuição',
            location TEXT NOT NULL DEFAULT 'Salão Principal'
        )
    ''')

    # 2. Table Reservations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            guest_phone TEXT NOT NULL,
            party_size INTEGER NOT NULL DEFAULT 2,
            reservation_time TEXT NOT NULL,
            table_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Confirmada',
            special_requests TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (table_id) REFERENCES tables (id)
        )
    ''')

    # 3. Digital Menu Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            allergens TEXT DEFAULT 'Sem Alergénios',
            is_available INTEGER DEFAULT 1
        )
    ''')

    # 4. Orders (Comandas POS) Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_code TEXT UNIQUE NOT NULL,
            table_number INTEGER NOT NULL,
            waiter_name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Em Preparação',
            subtotal REAL DEFAULT 0.0,
            tax_amount REAL DEFAULT 0.0,
            total_amount REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Order Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit_price REAL NOT NULL DEFAULT 0.0,
            total_price REAL NOT NULL DEFAULT 0.0,
            kitchen_status TEXT NOT NULL DEFAULT 'A Cozinhar',
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
        )
    ''')

    # 6. Waitstaff Roster Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS waiters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            shift TEXT NOT NULL DEFAULT 'Almoço & Jantar',
            assigned_tables TEXT DEFAULT 'Todas',
            status TEXT NOT NULL DEFAULT 'Em Serviço'
        )
    ''')

    # 7. Invoices Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_code TEXT UNIQUE NOT NULL,
            order_id INTEGER NOT NULL,
            table_number INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            tax_rate REAL DEFAULT 23.0,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL DEFAULT 'MBWay',
            issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
    ''')

    conn.commit()

    # Seed Demo Data if empty
    cursor.execute('SELECT COUNT(*) FROM tables')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Seed Waiters
    waiters_data = [
        ('Marco Antonio', '+351 912 333 444', 'Almoço & Jantar', 'Mesas 1 a 4', 'Em Serviço'),
        ('Inês Filipa', '+351 913 444 555', 'Jantar', 'Mesas 5 a 8', 'Em Serviço'),
        ('João Pedro', '+351 914 555 666', 'Almoço', 'Esplanada', 'De Folga')
    ]
    cursor.executemany('''
        INSERT INTO waiters (name, phone, shift, assigned_tables, status)
        VALUES (?, ?, ?, ?, ?)
    ''', waiters_data)

    # 2. Seed Tables Map
    tables_data = [
        (1, 2, 'Ocupada', 'Marco Antonio', 'Salão Principal'),
        (2, 4, 'Ocupada', 'Marco Antonio', 'Salão Principal'),
        (3, 4, 'Reservada', 'Marco Antonio', 'Salão Principal'),
        (4, 6, 'Livre', 'Marco Antonio', 'Salão Principal'),
        (5, 2, 'Ocupada', 'Inês Filipa', 'Esplanada'),
        (6, 4, 'Livre', 'Inês Filipa', 'Esplanada'),
        (7, 8, 'Livre', 'Inês Filipa', 'Zona VIP Gourmet'),
        (8, 4, 'Livre', 'Inês Filipa', 'Zona VIP Gourmet')
    ]
    cursor.executemany('''
        INSERT INTO tables (table_number, capacity, status, waiter_name, location)
        VALUES (?, ?, ?, ?, ?)
    ''', tables_data)

    # 3. Seed Menu Items
    menu_data = [
        ('Entradas', 'Tábua Premium de Queijos & Enchidos Ibéricos', 18.50, 'Seleção de queijo da Serra, presunto ibérico e fogaça artesanal', 'Laticínios, Glúten', 1),
        ('Entradas', 'Gambas ao Alhinho em Azeite de Trás-os-Montes', 14.00, 'Gambas salteadas com alho, malagueta e coentros frescos', 'Marisco', 1),
        ('Pratos Principais', 'Bacalhau à Lagareiro com Batata a Murro', 22.00, 'Lombo de bacalhau assado no forno com azeite virgem extra e grelos salteados', 'Peixe', 1),
        ('Pratos Principais', 'Nacos de Vitela Maturada com Molho de Pimenta', 26.50, 'Carne de vitela de raça maronesa acompanhada de batata frita rústica', 'Glúten', 1),
        ('Pratos Principais', 'Risotto de Cogumelos Selvagens & Trufa Preta', 19.50, 'Arroz carnaroli aveludado com cogumelos boletus e lascas de parmesão', 'Laticínios', 1),
        ('Sobremesas', 'Petit Gâteau de Chocolate com Gelado de Baunilha', 7.50, 'Bolo morno de chocolate com recheio fluído e gelado artesanal', 'Laticínios, Ovos, Glúten', 1),
        ('Sobremesas', 'Toucinho do Céu Tradicional com Amêndoa', 6.50, 'Doce tradicional conventual rico em gemas de ovo e amêndoa torrada', 'Frutos Secos, Ovos', 1),
        ('Bebidas', 'Vinho Tinto Quinta do Crasto Douro Reserva', 24.00, 'Garrafa de 75cl, colheita selecionada', 'Sulfitos', 1),
        ('Bebidas', 'Sangria Espumante de Frutos Vermelhos (1.5L)', 16.00, 'Jarra tradicional preparada no momento com espumante e hortelã', 'Sulfitos', 1)
    ]
    cursor.executemany('''
        INSERT INTO menu_items (category, name, price, description, allergens, is_available)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', menu_data)

    # 4. Seed Reservations
    reservations_data = [
        ('Eng. Manuel Ribeiro', '+351 919 888 777', 4, '20:30', 3, 'Confirmada', 'Mesa de canto junto à janela, celebração de aniversário.'),
        ('Dra. Sofia Martins', '+351 918 777 666', 2, '21:00', 8, 'Confirmada', 'Preferência por vinho branco fresco.')
    ]
    cursor.executemany('''
        INSERT INTO reservations (guest_name, guest_phone, party_size, reservation_time, table_id, status, special_requests)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', reservations_data)

    # 5. Seed Active Orders (Comandas)
    # Order 1 (Mesa 1)
    cursor.execute('''
        INSERT INTO orders (order_code, table_number, waiter_name, status, subtotal, tax_amount, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('CMD-2026-101', 1, 'Marco Antonio', 'Em Preparação', 40.50, 9.32, 49.82))
    order1_id = cursor.lastrowid

    items1 = [
        (order1_id, 'Gambas ao Alhinho em Azeite de Trás-os-Montes', 1, 14.00, 14.00, 'Pronto'),
        (order1_id, 'Bacalhau à Lagareiro com Batata a Murro', 1, 22.00, 22.00, 'A Cozinhar'),
        (order1_id, 'Petit Gâteau de Chocolate com Gelado de Baunilha', 1, 7.50, 7.50, 'Pendente')
    ]
    cursor.executemany('INSERT INTO order_items (order_id, item_name, quantity, unit_price, total_price, kitchen_status) VALUES (?, ?, ?, ?, ?, ?)', items1)

    # Order 2 (Mesa 2)
    cursor.execute('''
        INSERT INTO orders (order_code, table_number, waiter_name, status, subtotal, tax_amount, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('CMD-2026-102', 2, 'Marco Antonio', 'Em Preparação', 70.00, 16.10, 86.10))
    order2_id = cursor.lastrowid

    items2 = [
        (order2_id, 'Tábua Premium de Queijos & Enchidos Ibéricos', 1, 18.50, 18.50, 'Pronto'),
        (order2_id, 'Nacos de Vitela Maturada com Molho de Pimenta', 1, 26.50, 26.50, 'A Cozinhar'),
        (order2_id, 'Vinho Tinto Quinta do Crasto Douro Reserva', 1, 24.00, 24.00, 'Servido')
    ]
    cursor.executemany('INSERT INTO order_items (order_id, item_name, quantity, unit_price, total_price, kitchen_status) VALUES (?, ?, ?, ?, ?, ?)', items2)

    # 6. Seed Invoice
    cursor.execute('''
        INSERT INTO invoices (invoice_code, order_id, table_number, subtotal, tax_rate, total_amount, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('FT-2026-901', order1_id, 1, 40.50, 23.0, 49.82, 'MBWay'))

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados restaurant.db inicializada com sucesso para Proyecto 54!")
