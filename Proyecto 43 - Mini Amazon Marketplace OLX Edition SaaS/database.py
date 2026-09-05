import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'marketplace.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table Users (Buyers & Sellers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'Comprador',
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            rating REAL DEFAULT 4.9,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table Products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            condition TEXT DEFAULT 'Novo',
            seller_id INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            stock INTEGER DEFAULT 10,
            location TEXT NOT NULL,
            views INTEGER DEFAULT 120,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users (id)
        )
    ''')
    
    # Table Cart
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Table Orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            buyer_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT DEFAULT 'MB WAY',
            status TEXT DEFAULT 'Em Processamento',
            shipping_address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (buyer_id) REFERENCES users (id)
        )
    ''')
    
    # Table Order Items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Seed Data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        today = datetime.now()
        
        users = [
            ("Enmanuel Jimenez (EJAJ TECH)", "enmanuel@ejajtech.com", "Vendedor", "+351 911 151 993", "Faro, Algarve", 5.0),
            ("TechStore Portugal", "contacto@techstore.pt", "Vendedor", "+351 912 345 678", "Lisboa, Portugal", 4.8),
            ("ElectroLuxe Porto", "geral@electroluxe.pt", "Vendedor", "+351 961 234 567", "Porto, Portugal", 4.9),
            ("CyberHome Algarve", "vendas@cyberhome.pt", "Vendedor", "+351 933 456 789", "Loulé, Algarve", 4.7),
            ("Cliente Comprador Demo", "cliente@empresa.pt", "Comprador", "+351 918 765 432", "Cascais, Lisboa", 5.0)
        ]
        
        cursor.executemany('''
            INSERT INTO users (name, email, role, phone, location, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users)
        
        products = [
            (
                "Smart Ring Aurora Pro (Titanium Black)",
                "Anel inteligente de titânio com monitorização contínua de ritmo cardíaco, rastreio de sono REM, medição de oxigénio no sangue (SpO2) e bateria para 7 dias ininterruptos. Resistente à água a 50 metros.",
                299.00,
                "Tecnologia",
                "Novo",
                1,
                "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80",
                15,
                "Faro, Algarve",
                340
            ),
            (
                "Máscara de Sono NeuroWave EEG",
                "Máscara inteligente com sensores EEG integrados que analisam as ondas cerebrais em tempo real e induzem o sono profundo através de frequências sonoras binaurais binaural beats e cancelamento de ruído.",
                189.00,
                "Saúde & Bem-Estar",
                "Novo",
                1,
                "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=800&q=80",
                8,
                "Faro, Algarve",
                210
            ),
            (
                "Carregador Solar UltraFast MagSafe 50W",
                "Painel solar dobrável ultra-leve de elevada eficiência (24%) com saída MagSafe sem fios de 50W e portas USB-C Power Delivery para carregar o computador portátil e smartphone em qualquer lugar ao ar livre.",
                129.00,
                "Gadgets",
                "Novo",
                2,
                "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80",
                20,
                "Lisboa, Portugal",
                185
            ),
            (
                "Projetor Pocket 4K Laser Cinema",
                "Projetor a laser portátil ultra-compacto com resolução 4K HDR nativa, sistema operativo Android TV integrado, foco automático e coluna de som espacial Harman Kardon de 20W.",
                499.00,
                "Imagem & Som",
                "Novo",
                3,
                "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
                5,
                "Porto, Portugal",
                420
            ),
            (
                "Lâmpada de Levitação Magnética Lumina",
                "Lâmpada LED flutuante no ar que utiliza levitação magnética de alta precisão. Transmissão de energia sem fios e base em madeira de nogueira natural trabalhada à mão.",
                149.00,
                "Casa & Decoração",
                "Como Novo",
                4,
                "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80",
                12,
                "Loulé, Algarve",
                160
            ),
            (
                "Auriculares True Wireless ANC Studio Pro",
                "Auriculares sem fios com cancelamento ativo de ruído de 45dB, áudio de alta resolução LDAC, 6 microfones para chamadas HD cristalinas e autonomia total de 36 horas com estojo de carregamento.",
                179.00,
                "Imagem & Som",
                "Novo",
                2,
                "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
                18,
                "Lisboa, Portugal",
                290
            ),
            (
                "Teclado Mecânico Ergonómico RGB Wireless",
                "Teclado split ergonómico mecânico com switches lubrificados Hot-Swap, retroiluminação RGB por tecla, conectividade Bluetooth 5.2 de baixa latência e descanso de pulsos em espuma de memória.",
                135.00,
                "Tecnologia",
                "Novo",
                1,
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
                10,
                "Faro, Algarve",
                230
            ),
            (
                "Relógio Inteligente Titan Titanium Edition",
                "Smartwatch militar em titânio com ecrã AMOLED Sapphire Glass, GPS de dupla frequência, mapas offline e mais de 100 modos desportivos avançados. Autonomia de 14 dias de bateria.",
                349.00,
                "Tecnologia",
                "Novo",
                3,
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                7,
                "Porto, Portugal",
                310
            ),
            (
                "Drone Compacto 4K HDR Pro",
                "Drone dobrável com gimbal mecânico de 3 eixos, câmara de 48MP com sensor CMOS de 1 polegada, transmissão HD a 10 km e sensores anti-colisão omnidirecionais.",
                599.00,
                "Gadgets",
                "Novo",
                1,
                "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?auto=format&fit=crop&w=800&q=80",
                4,
                "Faro, Algarve",
                480
            ),
            (
                "Purificador de Ar HEPA Silencioso Smart",
                "Purificador de ar inteligente com filtro True HEPA H13 de 3 camadas, eliminação de 99,97% de poeiras e alérgenos, controlo por app móvel e funcionamento ultra-silencioso a 22dB.",
                219.00,
                "Casa & Decoração",
                "Novo",
                4,
                "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=800&q=80",
                9,
                "Loulé, Algarve",
                195
            )
        ]
        
        cursor.executemany('''
            INSERT INTO products (title, description, price, category, condition, seller_id, image_url, stock, location, views)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
        
        orders = [
            ("AMZ-2026-8812", 5, 488.00, "MB WAY", "Enviado", "Av. Marginal 400, 2750-642 Cascais", (today - timedelta(days=2)).strftime('%Y-%m-%d %H:%M')),
            ("AMZ-2026-9045", 5, 149.00, "Cartão de Crédito", "Entregue", "Av. Marginal 400, 2750-642 Cascais", (today - timedelta(days=5)).strftime('%Y-%m-%d %H:%M'))
        ]
        
        cursor.executemany('''
            INSERT INTO orders (order_number, buyer_id, total_amount, payment_method, status, shipping_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', orders)
        
        order_items = [
            (1, 1, 1, 299.00),
            (1, 2, 1, 189.00),
            (2, 5, 1, 149.00)
        ]
        
        cursor.executemany('''
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        ''', order_items)
        
    conn.commit()
    conn.close()
    print("[OK] Base de dados marketplace.db inicializada com sucesso para OLX-MARKETPLACE SaaS.")

if __name__ == '__main__':
    init_db()
