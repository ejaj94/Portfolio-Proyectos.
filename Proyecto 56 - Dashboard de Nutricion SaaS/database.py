import os
import sqlite3
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'nutrition.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("[DB] Removida base de dados antiga para recriação limpa.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Tabela de Alimentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            calories_100g REAL NOT NULL,
            protein_g REAL NOT NULL,
            carbs_g REAL NOT NULL,
            fat_g REAL NOT NULL,
            fiber_g REAL DEFAULT 0.0
        );
    """)

    # 2. Tabela de Objetivos Diários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            target_calories REAL NOT NULL,
            target_protein_g REAL NOT NULL,
            target_carbs_g REAL NOT NULL,
            target_fat_g REAL NOT NULL
        );
    """)

    # 3. Tabela de Registo de Refeições
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            food_name TEXT NOT NULL,
            quantity_g REAL NOT NULL,
            calories REAL NOT NULL,
            protein_g REAL NOT NULL,
            carbs_g REAL NOT NULL,
            fat_g REAL NOT NULL
        );
    """)

    # --- POPULAR BASE DE DADOS COM DADOS DE EXEMPLO (Pt-PT) ---

    # 1. Alimentos (100g)
    foods_seed = [
        ("Peito de Frango Grelhado", "Proteínas", 165.0, 31.0, 0.0, 3.6, 0.0),
        ("Lombo de Salmão no Forno", "Proteínas", 208.0, 20.0, 0.0, 13.0, 0.0),
        ("Ovos Inteiros Cozidos", "Proteínas", 155.0, 13.0, 1.1, 11.0, 0.0),
        ("Queijo Fresco Magro", "Proteínas", 72.0, 12.5, 3.0, 1.0, 0.0),
        ("Proteína Whey Isolada", "Proteínas", 370.0, 82.0, 3.0, 1.5, 0.0),
        ("Arroz Basmati Cozido", "Hidratos", 130.0, 2.7, 28.0, 0.3, 0.4),
        ("Batata-Doce Assada", "Hidratos", 90.0, 2.0, 21.0, 0.1, 3.0),
        ("Flocos de Aveia Integral", "Hidratos", 368.0, 13.5, 60.0, 7.0, 10.0),
        ("Pão de Centeio Artesanal", "Hidratos", 220.0, 7.5, 45.0, 1.8, 6.0),
        ("Quinoa Cozida", "Hidratos", 120.0, 4.4, 21.3, 1.9, 2.8),
        ("Azeite Virgem Extra", "Gorduras", 884.0, 0.0, 0.0, 100.0, 0.0),
        ("Abacate Maduro", "Gorduras", 160.0, 2.0, 8.5, 14.7, 6.7),
        ("Amêndoas Torradas", "Gorduras", 579.0, 21.0, 22.0, 50.0, 12.5),
        ("Maçã Bravo de Esmolfe", "Frutas & Vegetais", 52.0, 0.3, 14.0, 0.2, 2.4),
        ("Banana da Madeira", "Frutas & Vegetais", 89.0, 1.1, 23.0, 0.3, 2.6),
        ("Brócolos ao Vapor", "Frutas & Vegetais", 34.0, 2.8, 7.0, 0.4, 2.6),
        ("Espinafres Frescos", "Frutas & Vegetais", 23.0, 2.9, 3.6, 0.4, 2.2)
    ]

    cursor.executemany("""
        INSERT INTO foods (name, category, calories_100g, protein_g, carbs_g, fat_g, fiber_g)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, foods_seed)

    # 2. Objetivo Diário do Utilizador
    cursor.execute("""
        INSERT INTO daily_goals (user_name, target_calories, target_protein_g, target_carbs_g, target_fat_g)
        VALUES (?, ?, ?, ?, ?)
    """, ("Enmanuel Jimenez", 2200.0, 160.0, 220.0, 60.0))

    # 3. Registos Diários de Exemplo para Hoje
    today_str = datetime.now().strftime("%Y-%m-%d")

    meal_logs_seed = [
        (today_str, "Pequeno-almoço", "Flocos de Aveia Integral", 70.0, 257.6, 9.45, 42.0, 4.9),
        (today_str, "Pequeno-almoço", "Proteína Whey Isolada", 30.0, 111.0, 24.6, 0.9, 0.45),
        (today_str, "Pequeno-almoço", "Banana da Madeira", 120.0, 106.8, 1.32, 27.6, 0.36),
        (today_str, "Almoço", "Peito de Frango Grelhado", 200.0, 330.0, 62.0, 0.0, 7.2),
        (today_str, "Almoço", "Arroz Basmati Cozido", 180.0, 234.0, 4.86, 50.4, 0.54),
        (today_str, "Almoço", "Azeite Virgem Extra", 10.0, 88.4, 0.0, 0.0, 10.0),
        (today_str, "Almoço", "Brócolos ao Vapor", 150.0, 51.0, 4.2, 10.5, 0.6),
        (today_str, "Lanche", "Queijo Fresco Magro", 150.0, 108.0, 18.75, 4.5, 1.5),
        (today_str, "Lanche", "Maçã Bravo de Esmolfe", 150.0, 78.0, 0.45, 21.0, 0.3)
    ]

    cursor.executemany("""
        INSERT INTO meal_logs (log_date, meal_type, food_name, quantity_g, calories, protein_g, carbs_g, fat_g)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, meal_logs_seed)

    conn.commit()
    conn.close()
    print("[DB] Base de dados de Nutrição (nutrition.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
