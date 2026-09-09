import os
import sqlite3
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'logos.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("[DB] Removida base de dados antiga para recriação limpa.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Tabela de Logotipos Guardados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_logos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL,
            slogan TEXT,
            sector TEXT NOT NULL,
            style TEXT NOT NULL,
            primary_color TEXT NOT NULL,
            secondary_color TEXT NOT NULL,
            icon_symbol TEXT NOT NULL,
            layout_type TEXT NOT NULL,
            svg_code TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    # 2. Tabela de Paletas de Cores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brand_palettes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palette_name TEXT NOT NULL,
            color1 TEXT NOT NULL,
            color2 TEXT NOT NULL,
            color3 TEXT NOT NULL,
            theme_type TEXT NOT NULL
        );
    """)

    # --- POPULAR BASE DE DADOS COM DADOS DE EXEMPLO (Pt-PT) ---

    # 1. Paletas de Cores Animadas / Caricatura
    palettes_seed = [
        ("Vibrante Caricatura 3D", "#FFDE59", "#FF6B6B", "#4ECDC4", "Caricatura"),
        ("Bubblegum Pop & Neón", "#FF70A6", "#FF9F1C", "#2EC4B6", "Caricatura"),
        ("Cyber Cartoon Electric", "#00F5D4", "#FF007F", "#7000FF", "Caricatura"),
        ("Pastel Divertido", "#A8DADC", "#F4A261", "#E76F51", "Caricatura"),
        ("Dourado & Preto Executivo", "#F59E0B", "#0F172A", "#1E293B", "Corporativo")
    ]

    cursor.executemany("""
        INSERT INTO brand_palettes (palette_name, color1, color2, color3, theme_type)
        VALUES (?, ?, ?, ?, ?)
    """, palettes_seed)

    # 2. Logotipos Guardados de Exemplo
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    sample_svg_1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" rx="20" fill="#FFFDF0"/>
  <circle cx="200" cy="110" r="55" fill="#FFDE59" stroke="#1E293B" stroke-width="8"/>
  <path d="M 180 90 L 220 90 L 220 130 L 180 130 Z" fill="#FF6B6B" stroke="#1E293B" stroke-width="6" transform="rotate(15 200 110)"/>
  <text x="200" y="210" text-anchor="middle" font-family="Inter, sans-serif" font-weight="900" font-size="28" fill="#1E293B">EJAJ CARTOON</text>
  <text x="200" y="240" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="14" fill="#FF6B6B">CREATIVE STUDIO</text>
</svg>"""

    sample_svg_2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" rx="20" fill="#1E293B"/>
  <polygon points="200,45 250,140 150,140" fill="#4ECDC4" stroke="#FFDE59" stroke-width="6"/>
  <circle cx="200" cy="110" r="20" fill="#FF70A6"/>
  <text x="200" y="210" text-anchor="middle" font-family="Inter, sans-serif" font-weight="900" font-size="28" fill="#FFDE59">PIXEL BOT</text>
  <text x="200" y="240" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="14" fill="#4ECDC4">TECNOLOGIA DIVERTIDA</text>
</svg>"""

    cursor.executemany("""
        INSERT INTO saved_logos (brand_name, slogan, sector, style, primary_color, secondary_color, icon_symbol, layout_type, svg_code, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("EJAJ Cartoon", "Creative Studio", "Tecnologia", "Caricatura", "#FFDE59", "#FF6B6B", "rocket", "icon_top", sample_svg_1, now_str),
        ("Pixel Bot", "Tecnologia Divertida", "Jogos", "Caricatura", "#4ECDC4", "#FF70A6", "robot", "badge_3d", sample_svg_2, now_str)
    ])

    conn.commit()
    conn.close()
    print("[DB] Base de dados de Logotipos (logos.db) inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
