import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "auth_craft.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Table Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Standard',
            verified INTEGER DEFAULT 1,
            avatar_url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table OTP Tokens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            email TEXT NOT NULL,
            token_code TEXT NOT NULL,
            expires_at DATETIME,
            used INTEGER DEFAULT 0
        )
    ''')

    # Table Security Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_email TEXT,
            action TEXT NOT NULL,
            ip_address TEXT,
            device TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed default users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        pwd_hash = generate_password_hash("EjajTech#2026!")
        default_users = [
            ("Enmanuel Jimenez", "enmanuel@ejajtech.com", pwd_hash, "Super Admin", 1, "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"),
            ("Sarah Connor", "sarah@ejajtech.com", pwd_hash, "Manager", 1, "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80"),
            ("Alex Rivera", "alex@ejajtech.com", pwd_hash, "Developer", 1, "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80"),
            ("Pedro Santos", "pedro@ejajtech.com", pwd_hash, "Standard", 0, "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80")
        ]
        cursor.executemany('''
            INSERT INTO users (full_name, email, password_hash, role, verified, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', default_users)

    # Seed default logs if empty
    cursor.execute("SELECT COUNT(*) FROM security_logs")
    if cursor.fetchone()[0] == 0:
        sample_logs = [
            (1, "enmanuel@ejajtech.com", "Login Efetuado com Sucesso", "193.168.1.10", "Desktop (Windows 11 / Chrome)", "2026-09-16 18:40:12"),
            (1, "enmanuel@ejajtech.com", "Alteração de Função RBAC -> Super Admin", "193.168.1.10", "Desktop (Windows 11 / Chrome)", "2026-09-16 18:45:00"),
            (2, "sarah@ejajtech.com", "Verificação OTP Concluída", "188.82.12.99", "Mobile (iPhone 15)", "2026-09-16 19:02:44"),
            (4, "pedro@ejajtech.com", "Pedido de Recuperação de Palavra-passe", "85.240.40.12", "Mobile (Android)", "2026-09-16 19:15:30")
        ]
        cursor.executemany('''
            INSERT INTO security_logs (user_id, user_email, action, ip_address, device, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_logs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados auth_craft.db inicializado!")
