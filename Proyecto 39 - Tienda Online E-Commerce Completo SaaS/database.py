import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de Produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            old_price REAL,
            rating REAL DEFAULT 4.9,
            reviews_count INTEGER DEFAULT 120,
            sales_count INTEGER DEFAULT 500,
            stock INTEGER DEFAULT 50,
            image_url TEXT NOT NULL,
            description TEXT NOT NULL,
            badge TEXT
        )
    ''')

    # Tabela de Utilizadores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            avatar TEXT,
            total_spent REAL DEFAULT 0.0,
            orders_count INTEGER DEFAULT 0
        )
    ''')

    # Tabela de Encomendas / Pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'Processado',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Tabela de Itens da Encomenda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    conn.commit()

    # Verificar se já existem produtos
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        conn.commit()

    conn.close()
    print("[OK] Base de dados ecommerce.db inicializada com êxito para Proyecto 39.")

def seed_data(cursor):
    products = [
        (
            'Smart Ring Aurora Pro',
            'Wearables',
            149.99,
            189.99,
            4.9,
            340,
            1420,
            45,
            '/static/images/smart_ring_aurora_pro.jpg',
            'Anel inteligente em titânio cirúrgico com monitorização contínua de sono, frequência cardíaca, oxigénio no sangue e autonomia para 7 dias.',
            'Mais Vendido'
        ),
        (
            'Auriculares AI SpatialSound X',
            'Áudio & Tech',
            199.99,
            249.99,
            5.0,
            512,
            2150,
            30,
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
            'Auriculares premium com cancelamento ativo de ruído inteligente (ANC 45dB), áudio espacial 360° e microfones estúdio com IA.',
            'Top Trend 2026'
        ),
        (
            'Carregador Solar UltraFast MagSafe 50W',
            'Energia & Gadgets',
            69.99,
            89.99,
            4.8,
            230,
            980,
            65,
            '/static/images/magsafe_solar_charger.jpg',
            'Powerbank solar magnético ultrafino com carregamento rápido MagSafe de 50W, resistência IP68 e indicador digital de bateria.',
            'Inovação'
        ),
        (
            'Lâmpada Levitação Magnética Lumina',
            'Smart Home',
            89.99,
            119.99,
            4.9,
            410,
            1850,
            25,
            '/static/images/lumina_levitating_lamp.jpg',
            'Lâmpada LED minimalista a flutuar no ar através de indução eletromagnética com carregador wireless integrado na base de madeira de nogueira.',
            'Bestseller Home'
        ),
        (
            'Garrafa Purificadora UV-C SmartTemp',
            'Lifestyle',
            54.99,
            69.99,
            4.8,
            190,
            1120,
            80,
            'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800',
            'Garrafa em aço inoxidável com tecnologia UV-C que esteriliza 99.9% da água e ecrã tátil OLED que indica a temperatura em tempo real.',
            'Eco Choice'
        ),
        (
            'Projetor Pocket 4K Laser Cinema',
            'Áudio & Tech',
            349.99,
            429.99,
            5.0,
            185,
            840,
            15,
            '/static/images/pocket_laser_projector.jpg',
            'Mini projetor laser portátil com resolução nativa 4K HDR, auto-foco laser instantâneo e colunas harman/kardon integradas.',
            'Premium Tech'
        ),
        (
            'Teclado Mecânico Ergonómico Split Glow',
            'Áudio & Tech',
            129.99,
            159.99,
            4.9,
            380,
            1670,
            40,
            'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800',
            'Teclado mecânico dividido ergonómico com switches hot-swappable ultrassilenciosos, iluminação RGB por tecla e conexão tri-mode.',
            'Produtividade'
        ),
        (
            'Mochila Antifurto Solar 30L',
            'Lifestyle',
            99.99,
            129.99,
            4.9,
            590,
            2300,
            55,
            'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800',
            'Mochila impermeável de 30 litros com painel solar flexível de alta eficiência, porta USB-C externa e fechos ocultos aprovados por segurança TSA.',
            'Mais Vendido'
        ),
        (
            'Óculos Inteligentes AudioFrames AR',
            'Wearables',
            249.99,
            299.99,
            4.8,
            145,
            760,
            20,
            'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800',
            'Óculos de sol polarizados com áudio de condução óssea, microfone duplo com inteligência artificial para chamadas cristalinas e navegação por voz.',
            'Lançamento 2026'
        ),
        (
            'Máscara de Sono NeuroWave EEG',
            'Wearables',
            119.99,
            149.99,
            4.9,
            280,
            1290,
            35,
            '/static/images/neurowave_eeg.jpg',
            'Máscara de sono inteligente em seda natural com sensores de ondas cerebrais EEG que induzem o sono profundo através de neurosom binaural.',
            'Saúde & Bem-Estar'
        )
    ]

    cursor.executemany('''
        INSERT INTO products (name, category, price, old_price, rating, reviews_count, sales_count, stock, image_url, description, badge)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)

    # Inserir Utilizador de Demonstração
    cursor.execute('''
        INSERT INTO users (name, email, avatar, total_spent, orders_count)
        VALUES ('Diogo Silva', 'diogo.silva@ejajtech.pt', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400', 449.97, 2)
    ''')
    user_id = cursor.lastrowid

    # Inserir Encomendas de Exemplo para Estatísticas
    cursor.execute('''
        INSERT INTO orders (order_number, user_id, customer_name, customer_email, address, city, postal_code, total_amount, payment_method, status, created_at)
        VALUES ('ORD-2026-8801', ?, 'Diogo Silva', 'diogo.silva@ejajtech.pt', 'Avenida da Liberdade 125, 3.º Dir', 'Lisboa', '1250-142', 249.98, 'MB WAY', 'Entregue', ?)
    ''', (user_id, (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')))
    order1_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO order_items (order_id, product_id, product_name, price, quantity, subtotal)
        VALUES (?, 1, 'Smart Ring Aurora Pro', 149.99, 1, 149.99)
    ''', (order1_id,))
    cursor.execute('''
        INSERT INTO order_items (order_id, product_id, product_name, price, quantity, subtotal)
        VALUES (?, 8, 'Mochila Antifurto Solar 30L', 99.99, 1, 99.99)
    ''', (order1_id,))

    cursor.execute('''
        INSERT INTO orders (order_number, user_id, customer_name, customer_email, address, city, postal_code, total_amount, payment_method, status, created_at)
        VALUES ('ORD-2026-9412', ?, 'Diogo Silva', 'diogo.silva@ejajtech.pt', 'Rua de Santa Catarina 410', 'Porto', '4000-443', 199.99, 'Cartão de Crédito', 'Em Trânsito', ?)
    ''', (user_id, (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')))
    order2_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO order_items (order_id, product_id, product_name, price, quantity, subtotal)
        VALUES (?, 2, 'Auriculares AI SpatialSound X', 199.99, 1, 199.99)
    ''', (order2_id,))

if __name__ == '__main__':
    init_db()
