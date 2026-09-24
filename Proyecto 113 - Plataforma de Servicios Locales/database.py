import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'servicos_locais.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Tabela de Profissionais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professionals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            category TEXT NOT NULL, -- Electricidade, Canalização, Pintura, Limpeza, Carpintaria, Jardinagem, Climatização, Eletrodomésticos
            city TEXT NOT NULL, -- Lisboa, Porto, Braga, Coimbra, Faro, Cascais, Setúbal
            hourly_rate REAL NOT NULL,
            rating REAL DEFAULT 5.0,
            review_count INTEGER DEFAULT 0,
            bio TEXT NOT NULL,
            experience_years INTEGER NOT NULL,
            status TEXT DEFAULT 'Disponível', -- Disponível, Ocupado
            verified INTEGER DEFAULT 1,
            avatar_icon TEXT DEFAULT 'fa-user-tie',
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Tabela de Serviços Oferecidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professional_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            price_type TEXT DEFAULT 'Por Hora', -- Por Hora, Preço Fixo, Sob Orçamento
            estimated_hours REAL DEFAULT 2.0,
            icon TEXT DEFAULT 'fa-wrench',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professional_id) REFERENCES professionals(id)
        )
    ''')

    # 3. Tabela de Reservas / Agendamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_code TEXT UNIQUE NOT NULL,
            service_id INTEGER NOT NULL,
            professional_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            client_email TEXT NOT NULL,
            service_address TEXT NOT NULL,
            city TEXT NOT NULL,
            booking_date DATE NOT NULL,
            time_slot TEXT NOT NULL, -- 09:00 - 11:00, 11:30 - 13:30, 14:30 - 16:30, 17:00 - 19:00
            status TEXT DEFAULT 'Confirmada', -- Pendente, Confirmada, Em Andamento, Concluída, Cancelada
            total_price REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services(id),
            FOREIGN KEY (professional_id) REFERENCES professionals(id)
        )
    ''')

    # 4. Tabela de Avaliações / Testemunhos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professional_id INTEGER NOT NULL,
            booking_id INTEGER,
            client_name TEXT NOT NULL,
            rating INTEGER NOT NULL, -- 1 a 5
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professional_id) REFERENCES professionals(id),
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        )
    ''')

    # 5. Tabela de Mensagens de Chat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professional_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            sender TEXT NOT NULL, -- 'client' ou 'pro'
            message_text TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (professional_id) REFERENCES professionals(id)
        )
    ''')

    # Seed inicial se vazio
    cursor.execute('SELECT COUNT(*) FROM professionals')
    if cursor.fetchone()[0] == 0:
        seed_pros = [
            ('Eng. Tiago Ramos', 'tiago.eletricista@localpro.pt', '+351 912 345 678', 'Electricidade', 'Lisboa', 35.00, 4.9, 38, 'Eletricista certificado pela DGEG com 12 anos de experiência. Instalações trifásicas, quadros elétricos, iluminação LED e reparações de emergência 24/7.', 12, 'Disponível', 1, 'fa-bolt', 'Avenida da Liberdade, Lisboa'),
            ('Mestre Carlos Antunes', 'carlos.canalizador@localpro.pt', '+351 923 456 789', 'Canalização', 'Porto', 30.00, 4.8, 45, 'Especialista em deteção de fugas não destrutiva, desentupimentos mecanizados, substituição de tubagens e instalação de loiças sanitárias.', 15, 'Disponível', 1, 'fa-faucet-drip', 'Rua de Santa Catarina, Porto'),
            ('Ana Beatriz Rodrigues', 'ana.limpeza@localpro.pt', '+351 934 567 890', 'Limpeza', 'Lisboa', 18.00, 5.0, 52, 'Serviço profissional de higienização profunda residencial e pós-obras. Produtos ecológicos certificados e equipa rigorosa.', 7, 'Disponível', 1, 'fa-broom', 'Parque das Nações, Lisboa'),
            ('Miguel Valente', 'miguel.pintor@localpro.pt', '+351 965 678 901', 'Pintura', 'Braga', 25.00, 4.7, 29, 'Pintor de interiores e fachadas com acabamentos de luxo. Tratamento anti-humidade, lacagem de portas e aplicação de microcimento.', 10, 'Ocupado', 1, 'fa-paint-roller', 'Avenida Central, Braga'),
            ('Rui Ferreira', 'rui.clima@localpro.pt', '+351 917 890 123', 'Climatização', 'Faro', 40.00, 4.9, 31, 'Instalação e manutenção preventiva de Ar Condicionado, bombas de calor e painéis solares térmicos. Assistência técnica multimarca.', 9, 'Disponível', 1, 'fa-snowflake', 'Baixa de Faro, Algarve'),
            ('Eduardo Silveira', 'eduardo.carpintaria@localpro.pt', '+351 938 901 234', 'Carpintaria', 'Cascais', 28.00, 4.8, 22, 'Montador oficial de cozinhas e roupeiros por medida. Restauro de madeiras nobres, pavimentos flutuantes e mobiliário Ikea.', 8, 'Disponível', 1, 'fa-hammer', 'Centro Histórico, Cascais')
        ]
        cursor.executemany('''
            INSERT INTO professionals (name, email, phone, category, city, hourly_rate, rating, review_count, bio, experience_years, status, verified, avatar_icon, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_pros)

        seed_services = [
            (1, 'Substituição de Quadro Elétrico e Disjuntores', 'Electricidade', 'Remodelação completa do quadro geral com diferenciais de alta sensibilidade e certificação.', 140.00, 'Preço Fixo', 3.0, 'fa-bolt'),
            (1, 'Instalação de Pontos de Luz e Tomadas', 'Electricidade', 'Abertura de roços, passagem de cablagem e montagem de interruptores e tomadas.', 35.00, 'Por Hora', 1.0, 'fa-lightbulb'),
            (2, 'Desentupimento e Deteção de Fugas com Câmara', 'Canalização', 'Diagnóstico por vídeo-inspeção e resolução imediata sem quebrar azulejos.', 95.00, 'Preço Fixo', 2.0, 'fa-faucet-drip'),
            (2, 'Reparação de Autoclismo e Torneiras', 'Canalização', 'Substituição de válvulas de descarga, boias e cartuchos cerâmicos.', 30.00, 'Por Hora', 1.0, 'fa-wrench'),
            (3, 'Higienização Profunda Residencial (T2/T3)', 'Limpeza', 'Limpeza minuciosa de vidros, caixilharias, cozinhas engorduradas e sanitários.', 75.00, 'Preço Fixo', 4.0, 'fa-sparkles'),
            (4, 'Pintura Interior de Divisões (Teto e Paredes)', 'Pintura', 'Isolamento de chão e móveis, reparação de fissuras e duas demãos de tinta lavável.', 25.00, 'Por Hora', 5.0, 'fa-paint-roller'),
            (5, 'Instalação e Carga de Gás de Ar Condicionado (Mono-Split)', 'Climatização', 'Fixação de unidade interior e exterior com vácuo de linha frigorífica e teste de rendimento.', 180.00, 'Preço Fixo', 3.5, 'fa-snowflake'),
            (6, 'Montagem de Mobiliário e Roupeiros', 'Carpintaria', 'Montagem rápida e alinhamento perfeito de portas e gavetas de qualquer fabricante.', 28.00, 'Por Hora', 2.5, 'fa-hammer')
        ]
        cursor.executemany('''
            INSERT INTO services (professional_id, title, category, description, price, price_type, estimated_hours, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_services)

        today = datetime.now()
        seed_bookings = [
            ('SRV-101', 1, 1, 'Gonçalo Marques', '+351 918 111 222', 'goncalo.marques@email.com', 'Rua Castilho 42, 3º Dto', 'Lisboa', (today + timedelta(days=1)).strftime('%Y-%m-%d'), '09:00 - 11:00', 'Confirmada', 140.00, 'Quadro elétrico antigo a disparar constantemente quando liga o forno.'),
            ('SRV-102', 3, 2, 'Catarina Faria', '+351 927 333 444', 'catarina.faria@email.com', 'Avenida da Boavista 1200', 'Porto', (today + timedelta(days=2)).strftime('%Y-%m-%d'), '14:30 - 16:30', 'Confirmada', 95.00, 'Infiltração na parede da casa de banho que parece vir do esgoto.'),
            ('SRV-103', 5, 3, 'Diogo Mendonça', '+351 936 555 666', 'diogo.mendonca@email.com', 'Rua dos Fanqueiros 80', 'Lisboa', (today - timedelta(days=1)).strftime('%Y-%m-%d'), '10:00 - 14:00', 'Concluída', 75.00, 'Limpeza pós-mudança de inquilino. Apartamento impecável.'),
            ('SRV-104', 7, 5, 'Sofia Nogueira', '+351 969 777 888', 'sofia.nogueira@email.com', 'Urbanização Quinta do Eucalipto', 'Faro', (today + timedelta(days=3)).strftime('%Y-%m-%d'), '11:30 - 13:30', 'Pendente', 180.00, 'Instalação de AC Daikin de 12.000 BTU na sala principal.')
        ]
        cursor.executemany('''
            INSERT INTO bookings (booking_code, service_id, professional_id, client_name, client_phone, client_email, service_address, city, booking_date, time_slot, status, total_price, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_bookings)

        seed_reviews = [
            (1, 1, 'Gonçalo Marques', 5, 'O Eng. Tiago foi pontualíssimo, explicou todo o problema do quadro e resolveu o curto-circuito com total perícia. Recomendo a 100%!'),
            (2, 2, 'Catarina Faria', 5, 'Excelente trabalho do Mestre Carlos. Descobriu a fuga sem partir nada e deixou a canalização como nova. Muito limpo e prestável.'),
            (3, 3, 'Diogo Mendonça', 5, 'A Ana e a equipa fizeram um trabalho soberbo. Deixaram o apartamento a brilhar para a nova entrada. Profissionalismo de topo.'),
            (5, 4, 'Sofia Nogueira', 5, 'O Rui Ferreira é super experiente em climatização. Montou o ar condicionado em pouco mais de 2 horas e com linhas impecáveis.')
        ]
        cursor.executemany('''
            INSERT INTO reviews (professional_id, booking_id, client_name, rating, comment)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_reviews)

        seed_messages = [
            (1, 'Gonçalo Marques', 'client', 'Boa tarde Eng. Tiago, tem disponibilidade para vir na terça de manhã?', 1),
            (1, 'Gonçalo Marques', 'pro', 'Boa tarde Gonçalo! Sim, tenho a janela das 09h às 11h disponível. Pode marcar pelo sistema que confirmo logo.', 1),
            (2, 'Catarina Faria', 'client', 'Olá Sr. Carlos, o desentupimento com câmara inclui relatório?', 1),
            (2, 'Catarina Faria', 'pro', 'Olá Catarina! Sim, forneço o vídeo e o relatório técnico para o seguro do condomínio.', 1)
        ]
        cursor.executemany('''
            INSERT INTO messages (professional_id, client_name, sender, message_text, is_read)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_messages)

        conn.commit()
    conn.close()

# --- Professional Operations ---
def get_all_professionals(category=None, city=None, min_rating=None, status=None):
    conn = get_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM professionals WHERE 1=1'
    params = []

    if category and category != 'Todas':
        query += ' AND category = ?'
        params.append(category)
    if city and city != 'Todas':
        query += ' AND city = ?'
        params.append(city)
    if min_rating and float(min_rating) > 0:
        query += ' AND rating >= ?'
        params.append(float(min_rating))
    if status and status != 'Todos':
        query += ' AND status = ?'
        params.append(status)

    query += ' ORDER BY rating DESC, review_count DESC'
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_professional_by_id(pro_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM professionals WHERE id = ?', (pro_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_professional(name, email, phone, category, city, hourly_rate, bio, experience_years, address=''):
    conn = get_db()
    cursor = conn.cursor()
    
    icon_map = {
        'Electricidade': 'fa-bolt',
        'Canalização': 'fa-faucet-drip',
        'Limpeza': 'fa-broom',
        'Pintura': 'fa-paint-roller',
        'Climatização': 'fa-snowflake',
        'Carpintaria': 'fa-hammer',
        'Jardinagem': 'fa-seedling',
        'Eletrodomésticos': 'fa-blender'
    }
    avatar_icon = icon_map.get(category, 'fa-user-gear')

    cursor.execute('''
        INSERT INTO professionals (name, email, phone, category, city, hourly_rate, rating, review_count, bio, experience_years, status, verified, avatar_icon, address)
        VALUES (?, ?, ?, ?, ?, ?, 5.0, 0, ?, ?, 'Disponível', 1, ?, ?)
    ''', (name, email, phone, category, city, hourly_rate, bio, experience_years, avatar_icon, address))
    pro_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pro_id

def update_professional_status(pro_id, new_status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE professionals SET status = ? WHERE id = ?', (new_status, pro_id))
    conn.commit()
    conn.close()

# --- Services Operations ---
def get_all_services(category=None):
    conn = get_db()
    cursor = conn.cursor()
    query = '''
        SELECT s.*, p.name as pro_name, p.city, p.rating as pro_rating, p.avatar_icon
        FROM services s
        JOIN professionals p ON s.professional_id = p.id
    '''
    params = []
    if category and category != 'Todas':
        query += ' WHERE s.category = ?'
        params.append(category)
    query += ' ORDER BY s.id DESC'
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_service(professional_id, title, category, description, price, price_type, estimated_hours):
    conn = get_db()
    cursor = conn.cursor()
    icon_map = {
        'Electricidade': 'fa-bolt',
        'Canalização': 'fa-wrench',
        'Limpeza': 'fa-sparkles',
        'Pintura': 'fa-paint-roller',
        'Climatização': 'fa-snowflake',
        'Carpintaria': 'fa-hammer',
        'Jardinagem': 'fa-seedling'
    }
    icon = icon_map.get(category, 'fa-toolbox')
    cursor.execute('''
        INSERT INTO services (professional_id, title, category, description, price, price_type, estimated_hours, icon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (professional_id, title, category, description, price, price_type, estimated_hours, icon))
    sid = cursor.lastrowid
    conn.commit()
    conn.close()
    return sid

# --- Bookings Operations ---
def get_all_bookings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, s.title as service_title, p.name as pro_name, p.phone as pro_phone, p.category as pro_category
        FROM bookings b
        JOIN services s ON b.service_id = s.id
        JOIN professionals p ON b.professional_id = p.id
        ORDER BY b.id DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def create_booking(service_id, client_name, client_phone, client_email, service_address, city, booking_date, time_slot, notes=''):
    conn = get_db()
    cursor = conn.cursor()
    
    # Get service and pro info
    cursor.execute('SELECT professional_id, price FROM services WHERE id = ?', (service_id,))
    s_row = cursor.fetchone()
    if not s_row:
        conn.close()
        return None
        
    pro_id = s_row['professional_id']
    total_price = s_row['price']
    
    import random
    code = f"SRV-{random.randint(100, 999)}"
    
    cursor.execute('''
        INSERT INTO bookings (booking_code, service_id, professional_id, client_name, client_phone, client_email, service_address, city, booking_date, time_slot, status, total_price, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmada', ?, ?)
    ''', (code, service_id, pro_id, client_name, client_phone, client_email, service_address, city, booking_date, time_slot, total_price, notes))
    booking_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return booking_id, code

def update_booking_status(booking_id, new_status):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', (new_status, booking_id))
    conn.commit()
    conn.close()
    return True

# --- Reviews Operations ---
def get_all_reviews(pro_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if pro_id:
        cursor.execute('''
            SELECT r.*, p.name as pro_name, p.category
            FROM reviews r
            JOIN professionals p ON r.professional_id = p.id
            WHERE r.professional_id = ?
            ORDER BY r.id DESC
        ''', (pro_id,))
    else:
        cursor.execute('''
            SELECT r.*, p.name as pro_name, p.category
            FROM reviews r
            JOIN professionals p ON r.professional_id = p.id
            ORDER BY r.id DESC
        ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_review(professional_id, booking_id, client_name, rating, comment):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reviews (professional_id, booking_id, client_name, rating, comment)
        VALUES (?, ?, ?, ?, ?)
    ''', (professional_id, booking_id, client_name, rating, comment))
    
    # Recalculate average rating & review count for professional
    cursor.execute('SELECT AVG(rating) as avg_r, COUNT(*) as cnt FROM reviews WHERE professional_id = ?', (professional_id,))
    res = cursor.fetchone()
    avg_rating = round(res['avg_r'], 1) if res and res['avg_r'] else 5.0
    cnt = res['cnt'] if res else 1
    
    cursor.execute('UPDATE professionals SET rating = ?, review_count = ? WHERE id = ?', (avg_rating, cnt, professional_id))
    
    conn.commit()
    conn.close()
    return True

# --- Messages Operations ---
def get_messages_for_pro(pro_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages 
        WHERE professional_id = ? 
        ORDER BY id ASC
    ''', (pro_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_conversations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.professional_id, p.name as pro_name, p.category, p.avatar_icon, m.client_name, 
               COUNT(*) as total_msgs, 
               MAX(m.created_at) as last_time
        FROM messages m
        JOIN professionals p ON m.professional_id = p.id
        GROUP BY m.professional_id, m.client_name
        ORDER BY last_time DESC
    ''')
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def send_message(professional_id, client_name, sender, message_text):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (professional_id, client_name, sender, message_text, is_read)
        VALUES (?, ?, ?, ?, 1)
    ''', (professional_id, client_name, sender, message_text))
    mid = cursor.lastrowid
    conn.commit()
    conn.close()
    return mid

# --- Dashboard & KPIs ---
def get_marketplace_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM professionals')
    total_pros = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM professionals WHERE status = "Disponível"')
    active_pros = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM bookings')
    total_bookings = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM bookings WHERE status = "Confirmada"')
    confirmed_bookings = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(total_price) FROM bookings WHERE status != "Cancelada"')
    total_volume = cursor.fetchone()[0] or 0.0
    
    cursor.execute('SELECT AVG(rating) FROM reviews')
    avg_satisfaction = round(cursor.fetchone()[0] or 5.0, 1)
    
    cursor.execute('SELECT COUNT(DISTINCT city) FROM professionals')
    total_cities = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM messages')
    total_messages = cursor.fetchone()[0]
    
    # Category distribution
    cursor.execute('SELECT category, COUNT(*) as count FROM professionals GROUP BY category')
    cat_counts = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {
        "total_pros": total_pros,
        "active_pros": active_pros,
        "total_bookings": total_bookings,
        "confirmed_bookings": confirmed_bookings,
        "total_volume": total_volume,
        "avg_satisfaction": avg_satisfaction,
        "total_cities": total_cities,
        "total_messages": total_messages,
        "category_distribution": cat_counts
    }
