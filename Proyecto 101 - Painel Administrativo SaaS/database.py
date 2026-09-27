import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admin_pulse.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table Admin Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT DEFAULT 'Editor',
            status TEXT DEFAULT 'Ativo',
            last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
            avatar_url TEXT
        )
    ''')

    # Table Permissions Matrix
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE,
            can_read INTEGER DEFAULT 1,
            can_write INTEGER DEFAULT 1,
            can_delete INTEGER DEFAULT 0,
            can_config INTEGER DEFAULT 0,
            can_logs INTEGER DEFAULT 0
        )
    ''')

    # Table System Config
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            id INTEGER PRIMARY KEY DEFAULT 1,
            site_name TEXT DEFAULT 'EJAJ TECH Enterprise Cloud',
            maintenance_mode INTEGER DEFAULT 0,
            ssl_enforced INTEGER DEFAULT 1,
            smtp_host TEXT DEFAULT 'smtp.ejajtech.com',
            max_upload_mb INTEGER DEFAULT 50
        )
    ''')

    # Table System Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_level TEXT NOT NULL,
            message TEXT NOT NULL,
            module TEXT NOT NULL,
            ip_address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed Users if empty
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("Enmanuel Jimenez", "enmanuel@ejajtech.com", "Super Admin", "Ativo", "2026-09-16 19:30:00", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"),
            ("Carla Rodrigues", "carla@ejajtech.com", "Manager", "Ativo", "2026-09-16 19:12:10", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80"),
            ("Dinis Silva", "dinis@ejajtech.com", "Editor", "Ativo", "2026-09-16 18:45:22", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"),
            ("Beatriz Mendes", "beatriz@ejajtech.com", "Viewer", "Inativo", "2026-09-15 14:00:00", "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80")
        ]
        cursor.executemany('''
            INSERT INTO admin_users (name, email, role, status, last_login, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_users)

    # Seed Permissions Matrix if empty
    cursor.execute("SELECT COUNT(*) FROM permissions_matrix")
    if cursor.fetchone()[0] == 0:
        default_matrix = [
            ("Super Admin", 1, 1, 1, 1, 1),
            ("Manager", 1, 1, 1, 1, 0),
            ("Editor", 1, 1, 0, 0, 0),
            ("Viewer", 1, 0, 0, 0, 0)
        ]
        cursor.executemany('''
            INSERT INTO permissions_matrix (role_name, can_read, can_write, can_delete, can_config, can_logs)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_matrix)

    # Seed Config if empty
    cursor.execute("SELECT COUNT(*) FROM system_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO system_config (id, site_name, maintenance_mode, ssl_enforced, smtp_host, max_upload_mb)
            VALUES (1, 'EJAJ TECH Enterprise Cloud', 0, 1, 'smtp.ejajtech.com', 50)
        ''')

    # Seed Logs if empty
    cursor.execute("SELECT COUNT(*) FROM system_logs")
    if cursor.fetchone()[0] == 0:
        default_logs = [
            ("INFO", "Sessão de Administrador Iniciada por Enmanuel Jimenez", "AUTH_MODULE", "193.168.1.10", "2026-09-16 19:30:00"),
            ("WARNING", "Tentativa de alteração de ficheiro de configuração sem token SSL", "SECURITY_CORE", "188.82.12.99", "2026-09-16 19:20:15"),
            ("INFO", "Backup automático da base de dados concluído com sucesso", "DATABASE_BACKUP", "127.0.0.1", "2026-09-16 19:00:00"),
            ("ERROR", "Falha de ligação temporária no gateway SMTP secundário", "MAIL_GATEWAY", "195.23.110.4", "2026-09-16 18:35:40")
        ]
        cursor.executemany('''
            INSERT INTO system_logs (log_level, message, module, ip_address, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', default_logs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados admin_pulse.db inicializado!")
