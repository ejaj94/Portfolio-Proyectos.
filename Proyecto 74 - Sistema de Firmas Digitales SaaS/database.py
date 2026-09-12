import sqlite3
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'signcraft.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Documents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL, -- Contrato, Acordo NDA, Proposta, RH, Procuração
        file_size TEXT NOT NULL,
        status TEXT NOT NULL, -- Pendente, Em Processo, Assinado, Rejeitado
        deadline TEXT NOT NULL,
        created_by TEXT NOT NULL,
        created_at TEXT NOT NULL,
        signed_at TEXT
    );
    """)

    # Signers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        role_title TEXT NOT NULL, -- Cliente, Diretor, Advogado, Testemunha
        status TEXT NOT NULL, -- Pendente, Assinado, Rejeitado
        signature_data TEXT, -- SVG / Base64 drawn signature representation
        signed_at TEXT,
        ip_address TEXT,
        FOREIGN KEY (document_id) REFERENCES documents (id)
    );
    """)

    # Audit Trail Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        actor_name TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        ip_hash TEXT NOT NULL,
        FOREIGN KEY (document_id) REFERENCES documents (id)
    );
    """)

    # Seed Initial Data
    # 1. Documents
    cursor.execute("""
    INSERT INTO documents (doc_code, title, category, file_size, status, deadline, created_by, created_at, signed_at)
    VALUES 
    ('SIG-2026-001', 'Contrato de Prestação de Serviços SaaS v3.pdf', 'Contrato', '4.2 MB', 'Assinado', '2026-03-15', 'Sofia Manso', '2026-03-01 10:00', '2026-03-02 14:30'),
    ('SIG-2026-002', 'Acordo de Confidencialidade Mútuo NDA.pdf', 'Acordo NDA', '1.8 MB', 'Assinado', '2026-03-20', 'Carlos Silva', '2026-03-05 11:15', '2026-03-06 09:45'),
    ('SIG-2026-003', 'Proposta Comercial & Termos de Licenciamento.pdf', 'Proposta', '2.6 MB', 'Pendente', '2026-03-25', 'Enmanuel Jimenez', '2026-03-08 15:00', NULL),
    ('SIG-2026-004', 'Adenda Contratual - Extensão de Escopo App.pdf', 'RH', '3.1 MB', 'Em Processo', '2026-03-28', 'Mariana Rocha', '2026-03-10 09:30', NULL)
    """)

    # 2. Signers
    cursor.execute("""
    INSERT INTO signers (document_id, full_name, email, role_title, status, signature_data, signed_at, ip_address)
    VALUES 
    (1, 'Enmanuel Jimenez', 'enmanuel@ejajtech.com', 'Diretor Geral (Prestador)', 'Assinado', 'SIG_DRAW_EJ', '2026-03-01 11:20', '194.65.112.45'),
    (1, 'Sofia Manso', 'sofia@auraluxe.pt', 'CEO (Cliente)', 'Assinado', 'SIG_DRAW_SM', '2026-03-02 14:30', '85.240.18.99'),
    (2, 'Lucas Ferreira', 'lucas@vortexmedia.io', 'Diretor de Operações', 'Assinado', 'SIG_DRAW_LF', '2026-03-06 09:45', '185.220.101.5'),
    (3, 'Ana Rita Silva', 'ana.rita@empresa.pt', 'Diretora Financeira', 'Pendente', NULL, NULL, NULL),
    (4, 'Carlos Silva', 'carlos@ejajtech.com', 'Advogado Responsável', 'Assinado', 'SIG_DRAW_CS', '2026-03-10 11:00', '194.65.112.45'),
    (4, 'Mariana Rocha', 'mariana@cliente.pt', 'Gerente de RH', 'Pendente', NULL, NULL, NULL)
    """)

    # 3. Audit Trail Logs
    cursor.execute("""
    INSERT INTO audit_logs (document_id, action, actor_name, timestamp, ip_hash)
    VALUES 
    (1, 'Documento Criado & Enviado para Assinatura', 'Sofia Manso', '2026-03-01 10:00:12', 'IP-194-65-112-45'),
    (1, 'Assinatura Registada por Enmanuel Jimenez', 'Enmanuel Jimenez', '2026-03-01 11:20:45', 'IP-194-65-112-45'),
    (1, 'Assinatura Registada por Sofia Manso', 'Sofia Manso', '2026-03-02 14:30:10', 'IP-85-240-18-99'),
    (1, 'Certificado Digital de Integridade Emitido', 'SISTEMA SIGN CRAFT', '2026-03-02 14:30:12', 'SHA256-CERT-OK'),
    (2, 'Documento Criado', 'Carlos Silva', '2026-03-05 11:15:00', 'IP-194-65-112-45'),
    (2, 'Assinatura Concluída com Sucesso', 'Lucas Ferreira', '2026-03-06 09:45:30', 'IP-185-220-101-5')
    """)

    conn.commit()
    conn.close()
    print("[Database OK] signcraft.db criada e populada com sucesso.")

if __name__ == '__main__':
    init_db()
