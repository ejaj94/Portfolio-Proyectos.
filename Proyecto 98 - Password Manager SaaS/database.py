import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pass_craft.db")

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
            id INTEGER PRIMARY KEY DEFAULT 1,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            master_hash TEXT NOT NULL,
            tfa_enabled INTEGER DEFAULT 1
        )
    ''')

    # Table Vault Items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            category TEXT NOT NULL,
            website_url TEXT,
            notes TEXT,
            strength_score INTEGER DEFAULT 95,
            strength_label TEXT DEFAULT 'Forte',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table Categories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT NOT NULL
        )
    ''')

    # Seed default user if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (id, username, email, master_hash, tfa_enabled)
            VALUES (1, 'Enmanuel Jimenez', 'enmanuel@ejajtech.com', 'pbkdf2:sha256:600000$saltdemo$masterhash99', 1)
        ''')

    # Seed default categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_categories = [
            ("Trabalho", "fa-briefcase"),
            ("Pessoal", "fa-user"),
            ("Bancos/Finanças", "fa-building-columns"),
            ("Redes Sociais", "fa-share-nodes"),
            ("Servidores/Dev", "fa-server")
        ]
        cursor.executemany('''
            INSERT INTO categories (name, icon) VALUES (?, ?)
        ''', default_categories)

    # Seed default vault items if empty
    cursor.execute("SELECT COUNT(*) FROM vault_items")
    if cursor.fetchone()[0] == 0:
        default_vault = [
            (1, "EJAJ TECH Portal Cloud 🚀", "admin_enmanuel", "EjajTech#2026!Secured$", "Servidores/Dev", "https://portal.ejajtech.com", "Acesso root do servidor de produção.", 98, "Ultra-Forte"),
            (1, "GitHub Enterprise 💻", "ejajtech-admin", "G$89#kL2!xPz@2026", "Servidores/Dev", "https://github.com", "Conta de organização GitHub EJAJ TECH.", 95, "Forte"),
            (1, "Banco Millennium BCP 🏦", "user_bcp_9921", "M3#bcpPass!9921", "Bancos/Finanças", "https://ind.millenniumbcp.pt", "Conta empresarial principal.", 92, "Forte"),
            (1, "LinkedIn Corporativo 📱", "enmanuel@ejajtech.com", "LkInTech2026!Pass", "Redes Sociais", "https://linkedin.com", "Perfil executivo de tecnologia.", 88, "Forte"),
            (1, "E-mail Pessoal Gmail 📧", "jimenez.enmanuel@gmail.com", "senha12345", "Pessoal", "https://mail.google.com", "Atenção: alterar palavra-passe antiga.", 35, "Fraca")
        ]
        cursor.executemany('''
            INSERT INTO vault_items (user_id, title, username, encrypted_password, category, website_url, notes, strength_score, strength_label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_vault)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados pass_craft.db inicializado!")
