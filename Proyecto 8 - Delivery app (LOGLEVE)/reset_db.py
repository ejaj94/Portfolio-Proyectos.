import os
import sqlite3
from werkzeug.security import generate_password_hash

def reset_database(db_path="delivery_app.db"):
    print("=== INICIANDO RESTABLECIMIENTO Y SIEMBRA COMPLETA DE BASE DE DATOS ===")
    
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Base de datos anterior {db_path} eliminada.")
        
    conn = sqlite3.connect(db_path)
    
    try:
        # 1. Tabla: Restaurantes
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                nif TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                address TEXT NOT NULL,
                map_link TEXT DEFAULT '',
                logo_url TEXT DEFAULT '',
                banner_url TEXT DEFAULT '',
                region TEXT DEFAULT 'Porto'
            )
            """
        )
        
        # 2. Tabla: Clientes
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                address TEXT NOT NULL,
                nif TEXT DEFAULT '',
                stripe_customer_id TEXT DEFAULT '',
                saved_cards TEXT DEFAULT '[]',
                default_payment_method TEXT DEFAULT 'cash',
                FOREIGN KEY(id) REFERENCES restaurants(id) ON DELETE CASCADE
            )
            """
        )
        
        # 3. Tabla: Estafetas (Couriers)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS couriers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                nif TEXT NOT NULL,
                birthdate TEXT NOT NULL,
                phone TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                vehicle TEXT NOT NULL,
                vehicle_plate TEXT DEFAULT '',
                id_doc TEXT DEFAULT '',
                license_doc TEXT DEFAULT '',
                insurance_doc TEXT DEFAULT '',
                status TEXT DEFAULT 'approved',
                online_status INTEGER DEFAULT 1,
                latitude REAL DEFAULT 41.1579,
                longitude REAL DEFAULT -8.6291,
                balance REAL DEFAULT 148.50,
                active INTEGER DEFAULT 1,
                profile_picture TEXT DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
            )
            """
        )
        
        # 4. Tabla: Pedidos
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                courier_id INTEGER,
                status TEXT NOT NULL,
                note TEXT DEFAULT '',
                delivery_note TEXT DEFAULT '',
                fare_amount REAL DEFAULT 3.50,
                created_at TEXT NOT NULL,
                accepted_at TEXT,
                picked_up_at TEXT,
                delivered_at TEXT,
                FOREIGN KEY(restaurant_id) REFERENCES restaurants(id),
                FOREIGN KEY(client_id) REFERENCES clients(id),
                FOREIGN KEY(courier_id) REFERENCES couriers(id)
            )
            """
        )

        # 5. Tabla: Relaciones
        conn.execute("CREATE TABLE IF NOT EXISTS restaurant_favorite_couriers (restaurant_id INTEGER, courier_id INTEGER, PRIMARY KEY (restaurant_id, courier_id))")
        conn.execute("CREATE TABLE IF NOT EXISTS restaurant_blocked_couriers (restaurant_id INTEGER, courier_id INTEGER, PRIMARY KEY (restaurant_id, courier_id))")
        conn.execute("CREATE TABLE IF NOT EXISTS client_favorite_restaurants (client_id INTEGER, restaurant_id INTEGER, PRIMARY KEY (client_id, restaurant_id))")

        # 6. Tabla: Pratos
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS plates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                image_url TEXT DEFAULT '',
                description TEXT DEFAULT '',
                category TEXT NOT NULL,
                is_weekly INTEGER DEFAULT 0,
                FOREIGN KEY(restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
            )
            """
        )
        
        print("Tablas creadas con éxito.")

        pwd_demo = generate_password_hash("demo123")
        pwd_admin = generate_password_hash("adminpass")

        # Seed Restaurantes Demo
        conn.execute(
            """
            INSERT INTO restaurants (id, name, owner_name, nif, phone, whatsapp, email, password_hash, address, map_link, logo_url, banner_url, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "Restaurante Sabor Português",
                "Manuel Silva",
                "500123456",
                "+351 210 000 000",
                "+351 910 000 000",
                "sabor.portugues@logleve.com",
                pwd_demo,
                "Rua de Santa Catarina 123, Porto, Portugal",
                "https://maps.google.com/?q=Rua+de+Santa+Catarina+123+Porto",
                "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=150&q=80",
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
                "Porto"
            )
        )
        conn.execute(
            """
            INSERT INTO restaurants (id, name, owner_name, nif, phone, whatsapp, email, password_hash, address, map_link, logo_url, banner_url, region)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                2,
                "Com Cheiro de Amor Gourmet",
                "Stephanie Santos",
                "500987654",
                "+351 220 111 222",
                "+351 920 111 222",
                "geral@comcheirodeamor.pt",
                pwd_demo,
                "Avenida dos Aliados 45, Porto, Portugal",
                "https://maps.google.com/?q=Avenida+dos+Aliados+45+Porto",
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=150&q=80",
                "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
                "Porto"
            )
        )
        print("Restaurantes demo sembrados (IDs: 1, 2).")

        # Seed Cliente Demo
        conn.execute(
            """
            INSERT INTO clients (id, name, phone, email, password_hash, address, nif)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "Ana Silva",
                "+351 912 345 678",
                "cliente.demo@logleve.com",
                pwd_demo,
                "Rua de Santa Catarina 450, 4000-444 Porto",
                "234567890"
            )
        )
        print("Cliente demo sembrado (cliente.demo@logleve.com).")

        # Seed Entregador Demo
        conn.execute(
            """
            INSERT INTO couriers (id, name, nif, birthdate, phone, whatsapp, email, password_hash, vehicle, vehicle_plate, status, online_status, latitude, longitude, balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "João Oliveira",
                "299888777",
                "1995-06-15",
                "+351 933 888 999",
                "+351 933 888 999",
                "entregador.demo@logleve.com",
                pwd_demo,
                "Moto Honda PCX 125cc",
                "45-AB-89",
                "approved",
                1,
                41.1579,
                -8.6291,
                148.50
            )
        )
        print("Entregador demo sembrado (entregador.demo@logleve.com).")

        # Seed Platos
        plates = [
            (1, 1, "Pizza Margherita Gourmet", 8.50, "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=400&q=80", "Molho de tomate fresco, mozzarella fior di latte, manjericão fresco e azeite extra virgem.", "Pizzas", 0),
            (2, 1, "Pizza Pepperoni Artesanal", 9.50, "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=400&q=80", "Molho de tomate, queijo mozzarella e pepperoni artesanal picante fatiado.", "Pizzas", 0),
            (3, 1, "Hambúrguer Clássico Porto", 7.90, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=400&q=80", "Carne bovina grelhada 150g, queijo cheddar, alface, tomate e molho especial da casa.", "Hambúrgueres", 0),
            (4, 1, "Hambúrguer Frango Crocante", 8.20, "https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?auto=format&fit=crop&w=400&q=80", "Peito de frango crocante, bacon caramelizado, maionese de alho e rúcula fresca.", "Hambúrgueres", 1),
            (5, 1, "Tiramisú Clássico Italiano", 4.50, "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=400&q=80", "Sobremesa italiana caseira com biscoito champanhe, café e mascarpone.", "Sobremesas", 0),
            (6, 1, "Petit Gâteau Chocolate", 4.90, "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=400&q=80", "Bolo quente de chocolate com recheio cremoso e gelado de baunilha.", "Sobremesas", 1),
            (7, 1, "Cerveja Sagres 33cl", 2.00, "https://images.unsplash.com/photo-1608270176054-8a7300f6e6b0?auto=format&fit=crop&w=400&q=80", "Cerveja lager portuguesa clássica e fresca.", "Bebidas", 0),
            (8, 1, "Refrigerante Coca-Cola", 1.80, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80", "Lata de 33cl servida bem gelada.", "Bebidas", 0)
        ]
        
        for p in plates:
            conn.execute(
                """
                INSERT INTO plates (id, restaurant_id, name, price, image_url, description, category, is_weekly)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                p
            )
        print(f"Semeados {len(plates)} pratos dinâmicos con éxito.")

        # Pre-seed Pedido Demo Ativo (ID: 101)
        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            """
            INSERT INTO orders (id, restaurant_id, client_id, courier_id, status, note, delivery_note, fare_amount, created_at, accepted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                101,
                1,
                1,
                1,
                "accepted",
                "2x Pizza Pepperoni, 1x Coca-Cola",
                "Entregar no 3º andar, tocar a campainha.",
                3.50,
                now_str,
                now_str
            )
        )
        print("Pedido demo ativo (ID: 101 - Em Preparação) sembrado con éxito.")

        conn.commit()
        print("=== BASE DE DATOS LOGLEVE RESTABLECIDA Y SIEMBRA FINALIZADA CON ÉXITO ===")

    except Exception as e:
        conn.rollback()
        print(f"Error al restablecer la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database()
