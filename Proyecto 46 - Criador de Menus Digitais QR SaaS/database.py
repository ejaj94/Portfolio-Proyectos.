import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'menus.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Restaurants Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            tagline TEXT NOT NULL,
            logo_url TEXT NOT NULL,
            banner_url TEXT NOT NULL,
            primary_color TEXT NOT NULL DEFAULT '#FF6D00',
            bg_theme TEXT NOT NULL DEFAULT '#0F172A',
            phone_whatsapp TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')

    # Categories Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            icon TEXT NOT NULL DEFAULT 'bi-egg-fried',
            display_order INTEGER DEFAULT 0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id) ON DELETE CASCADE
        )
    ''')

    # Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            original_price REAL,
            image_url TEXT NOT NULL,
            allergens TEXT,
            is_available INTEGER DEFAULT 1,
            is_featured INTEGER DEFAULT 0,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    ''')

    # Offers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            badge_text TEXT NOT NULL,
            discount_percent INTEGER DEFAULT 0,
            valid_until TEXT NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed demo restaurants if empty
    cursor.execute('SELECT COUNT(*) FROM restaurants')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    # Restaurant 1: Burger & Crunch (Orange Neon Theme)
    cursor.execute('''
        INSERT INTO restaurants (name, slug, tagline, logo_url, banner_url, primary_color, bg_theme, phone_whatsapp, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Burger & Crunch Gourmet',
        'burgers-crunch',
        'Os Melhores Hambúrgueres Artesanais & Batatas Crocantes',
        'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=200&q=80',
        'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80',
        '#FF6D00',
        '#0F172A',
        '+351 911 151 993',
        'Av. da Liberdade 150, Lisboa'
    ))
    rest1_id = cursor.lastrowid

    # Categories for Rest 1
    cats1 = [
        (rest1_id, 'Hambúrgueres Especiais', 'bi-cup-hot', 1),
        (rest1_id, 'Entradas & Acompanhamentos', 'bi-box-seam', 2),
        (rest1_id, 'Bebidas & Batidos', 'bi-cup-straw', 3),
        (rest1_id, 'Sobremesas Gourmet', 'bi-cake2', 4)
    ]
    cursor.executemany('''
        INSERT INTO categories (restaurant_id, name, icon, display_order)
        VALUES (?, ?, ?, ?)
    ''', cats1)

    # Rest 1 Products
    prods1 = [
        (rest1_id, 1, 'Hambúrguer Monster Bacon Cheese', 'Nossa carne maturada 180g, queijo cheddar derretido, bacon crocante, cebola caramelizada e molho secreto da casa.', 14.50, 16.50, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80', 'Contém Glúten, Lactose', 1, 1),
        (rest1_id, 1, 'Hambúrguer Trufado Executive', 'Carne Black Angus 200g, maionese de trufa negra, queijo gruyère e rúcual fresca em pão brioche torrado.', 16.90, None, 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=800&q=80', 'Contém Glúten, Lactose', 1, 1),
        (rest1_id, 1, 'Veggie Green Beyond Burger', 'Hambúrguer 100% vegetal Beyond Meat, queijo vegano, abacate fresco, tomate e molho de ervas.', 13.90, None, 'https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=800&q=80', 'Vegetariano, Sem Glúten', 1, 0),
        (rest1_id, 2, 'Batatas Rústicas com Cheddar & Bacon', 'Batatas rústicas fritas com casca, cobertas por molho quente de cheddar e pedaços de bacon estaladiço.', 6.50, 7.50, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80', 'Lactose', 1, 1),
        (rest1_id, 2, 'Asas de Frango Buffalo Picantes', '8 asas de frango marinadas em molho picante buffalo, acompanhadas por molho ranch.', 8.90, None, 'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?auto=format&fit=crop&w=800&q=80', 'Picante', 1, 0),
        (rest1_id, 3, 'Milkshake Nutella & Oreo Monster', 'Batido cremoso de gelado de baunilha, Nutella, chantilly e bolacha Oreo triturada.', 5.50, None, 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=800&q=80', 'Lactose', 1, 0),
        (rest1_id, 4, 'Cheesecake de Frutos Vermelhos', 'Cheesecake cremoso com base de bolacha e cobertura caseira de frutos vermelhos silvestres.', 4.90, None, 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=800&q=80', 'Lactose', 1, 0)
    ]
    cursor.executemany('''
        INSERT INTO products (restaurant_id, category_id, name, description, price, original_price, image_url, allergens, is_available, is_featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', prods1)

    # Offers for Rest 1
    offers1 = [
        (rest1_id, 'Menu Almoço Executivo', 'Hambúrguer Monster + Batata Rústica + Bebida por apenas 14.90€ de segunda a sexta.', 'PROMO ALMOÇO', 20, '2026-12-31'),
        (rest1_id, 'Happy Hour de Batidos', '2º Milkshake com 50% de desconto todas as terças-feiras.', 'HAPPY HOUR 50%', 50, '2026-12-31')
    ]
    cursor.executemany('''
        INSERT INTO offers (restaurant_id, title, description, badge_text, discount_percent, valid_until)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', offers1)

    # Restaurant 2: Sushi Deluxe (Dark Gold Theme)
    cursor.execute('''
        INSERT INTO restaurants (name, slug, tagline, logo_url, banner_url, primary_color, bg_theme, phone_whatsapp, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Sushi Deluxe & Fusion Lounge',
        'sushi-deluxe',
        'Autêntica Culinária Japonesa & Fusion de Luxo',
        'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=200&q=80',
        'https://images.unsplash.com/photo-1611143669185-af224c5e3252?auto=format&fit=crop&w=1200&q=80',
        '#D97706',
        '#050505',
        '+351 912 345 678',
        'Marina de Albufeira, Loja 12, Algarve'
    ))

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados menus.db inicializada com sucesso para Proyecto 46 (Criador de Menus Digitais QR SaaS)!")
