import sqlite3
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'docucraft.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Folders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS folders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folder_name TEXT NOT NULL,
        icon TEXT DEFAULT 'fa-folder',
        color TEXT DEFAULT '#0369A1',
        parent_id INTEGER DEFAULT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # Documents/Files Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        category TEXT NOT NULL, -- Jurídico, Financeiro, Marketing, RH, Técnico, Geral
        folder_id INTEGER,
        file_extension TEXT NOT NULL, -- pdf, docx, xlsx, png, zip, etc.
        file_size TEXT NOT NULL,
        bytes_size INTEGER NOT NULL,
        access_permission TEXT NOT NULL, -- Privado, Equipas, Público, Leitura
        uploaded_by TEXT NOT NULL,
        download_count INTEGER DEFAULT 0,
        is_starred INTEGER DEFAULT 0,
        share_code TEXT UNIQUE,
        created_at TEXT NOT NULL,
        FOREIGN KEY (folder_id) REFERENCES folders (id)
    );
    """)

    # Shared Links Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        share_code TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        access_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (document_id) REFERENCES documents (id)
    );
    """)

    # Seed Initial Data
    # 1. Folders
    cursor.execute("""
    INSERT INTO folders (folder_name, icon, color, parent_id, created_at)
    VALUES 
    ('Contratos & Jurídico 2026', 'fa-folder-closed', '#0369A1', NULL, '2026-01-10 09:00'),
    ('Faturação & Relatórios Financeiros', 'fa-folder-closed', '#0284C7', NULL, '2026-01-15 10:30'),
    ('Ativos de Marketing & Branding', 'fa-folder-closed', '#F59E0B', NULL, '2026-02-01 11:00'),
    ('Recursos Humanos & Protocolos', 'fa-folder-closed', '#10B981', NULL, '2026-02-12 14:20'),
    ('Especificações Técnicas & API', 'fa-folder-closed', '#6366F1', NULL, '2026-03-01 16:00')
    """)

    # 2. Documents
    cursor.execute("""
    INSERT INTO documents (file_name, category, folder_id, file_extension, file_size, bytes_size, access_permission, uploaded_by, download_count, is_starred, share_code, created_at)
    VALUES 
    ('Acordo_Confidencialidade_NDA_ClienteVIP_2026.pdf', 'Jurídico', 1, 'pdf', '3.4 MB', 3565158, 'Privado', 'Sofia Manso', 14, 1, 'SHR-NDA-9901', '2026-02-01 10:15'),
    ('Relatorio_Financeiro_Executivo_Q1_2026.xlsx', 'Financeiro', 2, 'xlsx', '5.8 MB', 6081740, 'Equipas', 'Carlos Silva', 28, 1, 'SHR-FIN-8820', '2026-03-01 11:45'),
    ('Manual_Identidade_Visual_Branding_EJAJ.pdf', 'Marketing', 3, 'pdf', '12.6 MB', 13212057, 'Público', 'Ana Rita', 85, 1, 'SHR-MKT-4412', '2026-02-15 14:00'),
    ('Plano_Beneficios_Contratuais_Equipa.pdf', 'RH', 4, 'pdf', '1.8 MB', 1887436, 'Equipas', 'Mariana Rocha', 42, 0, 'SHR-RH-3319', '2026-02-20 09:30'),
    ('Arquitetura_Seguranca_Cloud_SaaS.pdf', 'Técnico', 5, 'pdf', '8.2 MB', 8598323, 'Leitura', 'Enmanuel Jimenez', 19, 1, 'SHR-TEC-7705', '2026-03-05 16:10'),
    ('Logotipo_Vetor_HighRes_Pack.zip', 'Marketing', 3, 'zip', '45.0 MB', 47185920, 'Público', 'Ana Rita', 62, 0, 'SHR-MKT-5591', '2026-03-08 12:00'),
    ('Balancete_Contabil_Certificado_2025.pdf', 'Financeiro', 2, 'pdf', '2.9 MB', 3040870, 'Privado', 'Carlos Silva', 8, 0, 'SHR-FIN-1122', '2026-01-20 17:30')
    """)

    # 3. Shares
    cursor.execute("""
    INSERT INTO shares (document_id, share_code, expires_at, access_count, created_at)
    VALUES 
    (1, 'SHR-NDA-9901', '2026-12-31', 14, '2026-02-01 10:15'),
    (3, 'SHR-MKT-4412', '2026-06-30', 85, '2026-02-15 14:00'),
    (5, 'SHR-TEC-7705', '2026-09-30', 19, '2026-03-05 16:10')
    """)

    conn.commit()
    conn.close()
    print("[Database OK] docucraft.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
