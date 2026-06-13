import sqlite3
from contextlib import contextmanager
from pathlib import Path
from werkzeug.security import generate_password_hash


class Database:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._initialize_database()

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        
        # Corrección 1: Activar de forma obligatoria el motor de llaves foráneas en SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        
        try:
            yield conn
            conn.commit()
        except Exception:
            # Corrección 3: Si la consulta SQL falla, revierte los cambios para no congelar la base de datos
            conn.rollback()
            raise
        finally:
            conn.close()

    def _initialize_database(self) -> None:
        db_file = Path(self.database_path)
        if not db_file.exists():
            db_file.parent.mkdir(parents=True, exist_ok=True)
            
        try:
            self._try_initialize_database()
        except Exception as e:
            print(f"Database initialization failed: {e}. Auto-healing by removing old database file and rebuilding.")
            import os
            try:
                if db_file.exists():
                    os.remove(self.database_path)
            except Exception as del_err:
                print(f"Failed to delete old database file: {del_err}")
            self._try_initialize_database()

    def _try_initialize_database(self) -> None:
        with self.connection() as conn:
            # Tabla: Restaurantes
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS restaurants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    owner_name TEXT NOT NULL,
                    nif TEXT NOT NULL,
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
            
            # Tabla: Clientes
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    restaurant_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    whatsapp TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    address TEXT NOT NULL,
                    map_link TEXT DEFAULT '',
                    is_email_verified INTEGER DEFAULT 0,
                    is_phone_verified INTEGER DEFAULT 0,
                    email_verification_token TEXT DEFAULT '',
                    phone_verification_pin TEXT DEFAULT '',
                    stripe_customer_id TEXT DEFAULT '',
                    verification_method TEXT DEFAULT 'email',
                    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
                )
                """
            )
            
            # Tabla: Estafetas (Couriers)
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
                    status TEXT DEFAULT 'pending',
                    online_status INTEGER DEFAULT 0,
                    latitude REAL DEFAULT 0.0,
                    longitude REAL DEFAULT 0.0,
                    balance REAL DEFAULT 0.0,
                    active INTEGER DEFAULT 1,
                    profile_picture TEXT DEFAULT ''
                )
                """
            )
            
            # Tabla: Pedidos
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

            # Tabla: Relaciones de Estafetas Favoritos
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS restaurant_favorite_couriers (
                    restaurant_id INTEGER NOT NULL,
                    courier_id INTEGER NOT NULL,
                    PRIMARY KEY (restaurant_id, courier_id),
                    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
                    FOREIGN KEY (courier_id) REFERENCES couriers(id) ON DELETE CASCADE
                )
                """
            )

            # Tabla: Relaciones de Estafetas Bloqueados
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS restaurant_blocked_couriers (
                    restaurant_id INTEGER NOT NULL,
                    courier_id INTEGER NOT NULL,
                    PRIMARY KEY (restaurant_id, courier_id),
                    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
                    FOREIGN KEY (courier_id) REFERENCES couriers(id) ON DELETE CASCADE
                )
                """
            )

            # Tabla: Pratos (Menú de platos dinámicos)
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

            # Tabla: Restaurantes Favoritos de Clientes
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS client_favorite_restaurants (
                    client_id INTEGER NOT NULL,
                    restaurant_id INTEGER NOT NULL,
                    PRIMARY KEY (client_id, restaurant_id),
                    FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE,
                    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
                )
                """
            )

            # Verificar y sembrar restaurante demo si la tabla está vacía
            r_check = conn.execute("SELECT id FROM restaurants WHERE id = 1").fetchone()
            if not r_check:
                hashed_rest = generate_password_hash("admin")
                conn.execute(
                    """
                    INSERT INTO restaurants (
                        id, name, owner_name, nif, phone, whatsapp, email, password_hash, address, map_link, logo_url, banner_url, region
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        1,
                        "Com Cheiro de Amor",
                        "Manuel Silva",
                        "500123456",
                        "+351210000000",
                        "+351910000000",
                        "geral@comcheirodeamor.pt",
                        hashed_rest,
                        "Rua de Santa Catarina 123, Porto, Portugal",
                        "https://maps.google.com/?q=Rua+de+Santa+Catarina+123+Porto",
                        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=150&q=80",
                        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
                        "Porto"
                    )
                )
                
                # Sembrar platos
                plates = [
                    (1, "Pizza Margherita", 8.50, "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=400&q=80", "Molho de tomate fresco, mozzarella fior di latte, manjericão fresco e azeite extra virgem.", "Pizzas", 0),
                    (2, "Pizza Pepperoni", 9.50, "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=400&q=80", "Molho de tomate, queijo mozzarella e pepperoni artesanal picante fatiado.", "Pizzas", 0),
                    (3, "Hambúrguer Clássico", 7.90, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=400&q=80", "Carne bovina grelhada 150g, queijo cheddar, alface, tomate e molho especial da casa.", "Hambúrgueres", 0),
                    (4, "Hambúrguer de Frango Crocante", 8.20, "https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?auto=format&fit=crop&w=400&q=80", "Peito de frango crocante, bacon caramelizado, maionese de alho e rúcula fresca.", "Hambúrgueres", 1),
                    (5, "Tiramisú Clássico", 4.50, "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=400&q=80", "Sobremesa italiana caseira com biscoito champanhe, café e queijo mascarpone polvilhado com cacau.", "Sobremesas", 0),
                    (6, "Petit Gâteau", 4.90, "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=400&q=80", "Bolo quente de chocolate con recheio cremoso, servido con uma bola de gelado de baunilha.", "Sobremesas", 1),
                    (7, "Cerveja Sagres 33cl", 2.00, "https://images.unsplash.com/photo-1608270176054-8a7300f6e6b0?auto=format&fit=crop&w=400&q=80", "Cerveja lager portuguesa clásica e fresca.", "Bebidas", 0),
                    (8, "Refrigerante Coca-Cola", 1.80, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80", "Lata de 33cl servida bem gelada.", "Bebidas", 0)
                ]
                for p in plates:
                    conn.execute(
                        """
                        INSERT INTO plates (id, restaurant_id, name, price, image_url, description, category, is_weekly)
                        VALUES (?, 1, ?, ?, ?, ?, ?, ?)
                        """,
                        p
                    )

