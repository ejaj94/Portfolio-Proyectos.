import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'role_craft.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users Table (Admins, Empregados, Utilizadores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role_type TEXT NOT NULL, -- 'Administrador', 'Empleado', 'Usuario'
            department TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Ativo', -- 'Ativo', 'Suspenso', 'Pendente'
            created_at TEXT NOT NULL
        )
    ''')

    # Permissions Matrix (RBAC por módulo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_type TEXT NOT NULL,
            module_name TEXT NOT NULL,
            access_level TEXT NOT NULL -- 'None', 'Read', 'Write', 'Admin'
        )
    ''')

    # Active Accesses / Sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            ip_address TEXT NOT NULL,
            device_browser TEXT NOT NULL,
            location TEXT NOT NULL,
            login_time TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Audit Trail Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            actor_name TEXT NOT NULL,
            action_type TEXT NOT NULL, -- 'ROLE_CHANGE', 'PERMISSION_UPDATE', 'SESSION_REVOKE', 'USER_ADD'
            details TEXT NOT NULL,
            ip_address TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Seed Initial Data if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Seed Users
        seed_users = [
            ("Angel Rafael", "admin@rolecraft.ai", "Administrador", "Direção & TI", "Ativo", now),
            ("Beatriz Santos", "beatriz.santos@rolecraft.ai", "Administrador", "Segurança & Compliance", "Ativo", now),
            ("Carlos Mendes", "carlos.mendes@rolecraft.ai", "Empleado", "Recursos Humanos", "Ativo", now),
            ("Diana Lima", "diana.lima@rolecraft.ai", "Empleado", "Vendas & CRM", "Ativo", now),
            ("Eduardo Rocha", "eduardo.rocha@rolecraft.ai", "Empleado", "Suporte Técnico", "Ativo", now),
            ("Fernanda Alves", "fernanda.alves@client.com", "Usuario", "Cliente Externo", "Ativo", now),
            ("Gabriel Costa", "gabriel.costa@client.com", "Usuario", "Parceiro B2B", "Pendente", now)
        ]
        cursor.executemany('''
            INSERT INTO users (name, email, role_type, department, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_users)

        # Seed Permissions Matrix
        seed_permissions = [
            # Administrador
            ("Administrador", "Financeiro", "Admin"),
            ("Administrador", "Recursos Humanos", "Admin"),
            ("Administrador", "Vendas", "Admin"),
            ("Administrador", "Infraestrutura", "Admin"),
            ("Administrador", "Auditoria", "Admin"),
            # Empleado
            ("Empleado", "Financeiro", "Read"),
            ("Empleado", "Recursos Humanos", "Write"),
            ("Empleado", "Vendas", "Write"),
            ("Empleado", "Infraestrutura", "None"),
            ("Empleado", "Auditoria", "Read"),
            # Usuario
            ("Usuario", "Financeiro", "None"),
            ("Usuario", "Recursos Humanos", "None"),
            ("Usuario", "Vendas", "Read"),
            ("Usuario", "Infraestrutura", "None"),
            ("Usuario", "Auditoria", "None")
        ]
        cursor.executemany('''
            INSERT INTO permissions_matrix (role_type, module_name, access_level)
            VALUES (?, ?, ?)
        ''', seed_permissions)

        # Seed Active Sessions
        seed_sessions = [
            (1, "193.168.1.10", "Chrome 128 / Windows 11", "Lisboa, Portugal", "2026-09-16 19:10:00", 1),
            (2, "188.82.12.99", "Firefox 130 / macOS", "Porto, Portugal", "2026-09-16 18:45:00", 1),
            (3, "195.23.110.4", "Safari / iOS 18", "Coimbra, Portugal", "2026-09-16 17:30:00", 1),
            (4, "85.240.12.5", "Edge 128 / Windows 10", "Braga, Portugal", "2026-09-16 16:15:00", 0)
        ]
        cursor.executemany('''
            INSERT INTO active_sessions (user_id, ip_address, device_browser, location, login_time, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', seed_sessions)

        # Seed Audit Logs
        seed_audit = [
            ("2026-09-16 19:12:00", "Angel Rafael", "ROLE_CHANGE", "Promoveu Beatriz Santos de Empleado para Administrador", "193.168.1.10"),
            ("2026-09-16 18:50:00", "Beatriz Santos", "PERMISSION_UPDATE", "Atualizou nível de acesso do módulo Financeiro para Empleado -> Read", "188.82.12.99"),
            ("2026-09-16 17:40:00", "Angel Rafael", "USER_ADD", "Criou o utilizador Gabriel Costa (Parceiro B2B)", "193.168.1.10"),
            ("2026-09-16 16:20:00", "Sistema Core", "SESSION_REVOKE", "Revogou sessão inativa de Diana Lima", "127.0.0.1")
        ]
        cursor.executemany('''
            INSERT INTO audit_logs (timestamp, actor_name, action_type, details, ip_address)
            VALUES (?, ?, ?, ?, ?)
        ''', seed_audit)

        conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de dados RoleCraft inicializada com sucesso!")
