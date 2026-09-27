import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'image_compressor.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compression_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_filename TEXT NOT NULL,
            compressed_filename TEXT NOT NULL,
            output_format TEXT NOT NULL,
            quality INTEGER NOT NULL,
            original_size_kb REAL NOT NULL,
            compressed_size_kb REAL NOT NULL,
            savings_pct REAL NOT NULL,
            original_dimensions TEXT NOT NULL,
            compressed_dimensions TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if seed data exists
    cursor.execute('SELECT COUNT(*) FROM compression_history')
    if cursor.fetchone()[0] == 0:
        seed_data = [
            ('landscape_photo.jpg', 'landscape_photo_compressed.webp', 'WEBP', 80, 4200.0, 520.0, 87.6, '3840x2160', '3840x2160', 'uploads/landscape_photo_compressed.webp'),
            ('portrait_banner.png', 'portrait_banner_compressed.jpg', 'JPEG', 75, 1850.4, 310.2, 83.2, '1920x1080', '1920x1080', 'uploads/portrait_banner_compressed.jpg'),
            ('app_icon.png', 'app_icon_compressed.png', 'PNG', 90, 890.0, 420.0, 52.8, '512x512', '512x512', 'uploads/app_icon_compressed.png')
        ]
        cursor.executemany('''
            INSERT INTO compression_history 
            (original_filename, compressed_filename, output_format, quality, original_size_kb, compressed_size_kb, savings_pct, original_dimensions, compressed_dimensions, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_data)
        conn.commit()
    conn.close()

def add_compression(original_filename, compressed_filename, output_format, quality, original_size_kb, compressed_size_kb, savings_pct, original_dimensions, compressed_dimensions, file_path):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO compression_history 
        (original_filename, compressed_filename, output_format, quality, original_size_kb, compressed_size_kb, savings_pct, original_dimensions, compressed_dimensions, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (original_filename, compressed_filename, output_format.upper(), quality, original_size_kb, compressed_size_kb, savings_pct, original_dimensions, compressed_dimensions, file_path))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_all_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM compression_history ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def clear_all_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM compression_history')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados image_compressor.db inicializada com sucesso!")
