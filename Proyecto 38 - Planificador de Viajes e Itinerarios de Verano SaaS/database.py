import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'travel.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla Destinos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            image_url TEXT NOT NULL,
            weather TEXT NOT NULL,
            avg_daily_cost REAL NOT NULL,
            currency TEXT NOT NULL,
            best_months TEXT NOT NULL,
            visa_required TEXT NOT NULL
        )
    ''')

    # Tabla Viagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            destination_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            total_budget REAL NOT NULL,
            total_spent REAL DEFAULT 0,
            status TEXT DEFAULT 'Planeada',
            cover_image TEXT,
            FOREIGN KEY (destination_id) REFERENCES destinations(id)
        )
    ''')

    # Tabla Itinerário Dia a Dia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itinerary_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            time_slot TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT,
            cost REAL DEFAULT 0,
            notes TEXT,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
    ''')

    # Tabla Hotéis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            stars INTEGER NOT NULL,
            price_per_night REAL NOT NULL,
            image_url TEXT NOT NULL,
            amenities TEXT NOT NULL,
            FOREIGN KEY (destination_id) REFERENCES destinations(id)
        )
    ''')

    conn.commit()
    conn.close()
    seed_initial_data()

def seed_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM destinations')
    if cursor.fetchone()[0] == 0:
        now = datetime.now()

        # Seed Destinos de Verão
        destinations_data = [
            (
                'Algarve & Grutas de Benagil',
                'Portugal',
                'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=600',
                '32°C Ensolarado',
                120.0,
                'EUR (€)',
                'Junho - Setembro',
                'Isento (UE)'
            ),
            (
                'Santorini & Ilhas Cíclades',
                'Grécia',
                'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=600',
                '30°C Céu Limpo',
                180.0,
                'EUR (€)',
                'Maio - Outubro',
                'Isento (Schengen)'
            ),
            (
                'Costa Amalfitana & Positano',
                'Itália',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?w=600',
                '29°C Brisa Marítima',
                210.0,
                'EUR (€)',
                'Junho - Setembro',
                'Isento (Schengen)'
            ),
            (
                'Riviera Maya & Tulum',
                'México',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600',
                '33°C Tropical',
                150.0,
                'USD ($)',
                'Novembro - Abril',
                'Visto Turístico'
            )
        ]

        cursor.executemany('''
            INSERT INTO destinations (name, country, image_url, weather, avg_daily_cost, currency, best_months, visa_required)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', destinations_data)

        # Seed Viagem Principal de Verão (Algarve)
        trip_start = (now + timedelta(days=15)).strftime('%Y-%m-%d')
        trip_end = (now + timedelta(days=22)).strftime('%Y-%m-%d')

        cursor.execute('''
            INSERT INTO trips (title, destination_id, start_date, end_date, total_budget, total_spent, status, cover_image)
            VALUES ('Férias de Verão no Algarve & Cruzeiro nas Grutas', 1, ?, ?, 2500.0, 1450.0, 'Em Curso', 'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=800')
        ''', (trip_start, trip_end))
        
        trip_id = cursor.lastrowid

        # Seed Itinerário Dia a Dia (Pt-PT)
        itinerary_data = [
            (trip_id, 1, '10:00', 'Vôo Lisboa (LIS) -> Faro (FAO)', 'Vôo', 'Aeroporto de Faro', 180.0, 'Vôo direto de 45 minutos'),
            (trip_id, 1, '14:00', 'Check-in no Pine Cliffs Luxury Resort', 'Hotel', 'Praia da Falésia', 650.0, 'Suíte Luxo com vista mar e pequeno-almoço'),
            (trip_id, 1, '20:00', 'Jantar de Boas-Vindas no Rest. Marisqueira', 'Restaurante', 'Marina de Vilamoura', 120.0, 'Reserva para 2 pessoas no terraço marítimo'),
            (trip_id, 2, '09:30', 'Passeio de Catamarã & Gruta de Benagil', 'Atividade', 'Portimão', 140.0, 'Cruzeiro privado de 4 horas com prova de vinhos'),
            (trip_id, 2, '13:30', 'Almoço Grelhados na Praia da Marinha', 'Restaurante', 'Praia da Marinha', 75.0, 'Sardinhas assadas e vinho verde algarvio'),
            (trip_id, 2, '18:00', 'Sunset Party no NoSoloAgua Beach Club', 'Atividade', 'Praia da Rocha', 90.0, 'Cama balinesa e cocktails ao pôr do sol'),
            (trip_id, 3, '11:00', 'Experiência de Mergulho na Costa de Albufeira', 'Atividade', 'Albufeira', 110.0, 'Batismo de mergulho com instrutor certificado'),
            (trip_id, 3, '20:30', 'Jantar de Gala no Restaurante Ocean 2★ Michelin', 'Restaurante', 'Vila Vita Parc', 380.0, 'Menu de degustação com harmonização de vinhos')
        ]

        cursor.executemany('''
            INSERT INTO itinerary_items (trip_id, day_number, time_slot, title, category, location, cost, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', itinerary_data)

        # Seed Hotéis
        hotels_data = [
            (1, 'Pine Cliffs Ocean Suites & Spa', 5, 320.0, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500', 'Piscina Infinito, Spa, Acesso Privado à Praia, Pequeno-almoço'),
            (1, 'Vila Vita Parc Resort & Spa', 5, 450.0, 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=500', '2 Estrelas Michelin, Campo de Golfe, Heliponto, Vista Mar'),
            (2, 'Canaves Oia Luxury Suites', 5, 520.0, 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=500', 'Piscina de Borda Infinita na Caldeira, Pôr do Sol de Oia')
        ]

        cursor.executemany('''
            INSERT INTO hotels (destination_id, name, stars, price_per_night, image_url, amenities)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', hotels_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados travel.db inicializada com exito para Proyecto 38.")
