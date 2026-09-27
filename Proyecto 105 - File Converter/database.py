import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'file_converter.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversion_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_filename TEXT NOT NULL,
            converted_filename TEXT NOT NULL,
            source_format TEXT NOT NULL,
            target_format TEXT NOT NULL,
            category TEXT NOT NULL,
            original_size_kb REAL NOT NULL,
            converted_size_kb REAL NOT NULL,
            status TEXT DEFAULT 'Completed',
            file_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if seed data exists
    cursor.execute('SELECT COUNT(*) FROM conversion_history')
    if cursor.fetchone()[0] == 0:
        seed_data = [
            ('hero_banner.png', 'hero_banner.webp', 'PNG', 'WEBP', 'Imagem', 2450.5, 380.2, 'Completed', 'uploads/hero_banner.webp'),
            ('relatorio_vendas.csv', 'relatorio_vendas.json', 'CSV', 'JSON', 'Dados', 540.0, 480.0, 'Completed', 'uploads/relatorio_vendas.json'),
            ('documento_tecnico.md', 'documento_tecnico.html', 'MD', 'HTML', 'Documento', 120.4, 135.0, 'Completed', 'uploads/documento_tecnico.html'),
            ('logo_empresa.jpg', 'logo_empresa.ico', 'JPG', 'ICO', 'Imagem', 890.0, 45.2, 'Completed', 'uploads/logo_empresa.ico')
        ]
        cursor.executemany('''
            INSERT INTO conversion_history 
            (original_filename, converted_filename, source_format, target_format, category, original_size_kb, converted_size_kb, status, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_data)
        conn.commit()
    conn.close()

def add_conversion(original_filename, converted_filename, source_format, target_format, category, original_size_kb, converted_size_kb, file_path):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversion_history 
        (original_filename, converted_filename, source_format, target_format, category, original_size_kb, converted_size_kb, status, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Completed', ?)
    ''', (original_filename, converted_filename, source_format.upper(), target_format.upper(), category, original_size_kb, converted_size_kb, file_path))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_all_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversion_history ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_all_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM conversion_history')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados file_converter.db inicializada com sucesso!")
