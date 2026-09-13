import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'crowdfund.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            creator_name TEXT NOT NULL,
            category TEXT NOT NULL,
            goal_amount REAL NOT NULL,
            raised_amount REAL DEFAULT 0.0,
            description TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT DEFAULT 'Ativo',
            image_url TEXT
        )
    ''')

    # Create Creators Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            bio TEXT NOT NULL,
            project_count INTEGER DEFAULT 1,
            total_raised REAL DEFAULT 0.0
        )
    ''')

    # Create Donations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            donor_name TEXT NOT NULL,
            donor_email TEXT NOT NULL,
            amount REAL NOT NULL,
            reward_tier TEXT DEFAULT 'Apoio Livre',
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT DEFAULT 'Apoiante',
            total_donated REAL DEFAULT 0.0
        )
    ''')

    # Seed Sample Data if empty
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        sample_creators = [
            ("Lia Mendonça", "lia.mendonca@techportugal.pt", "Fundadora do EcoTech Lab, especialista em soluções sustentáveis de energia limpa."),
            ("Mário Silva", "mario.silva@creativestudio.pt", "Realizador de cinema independente e mentor de jovens talentos de animação."),
            ("Ana Beatriz", "ana.beatriz@eduopen.pt", "Educadora social e dinamizadora de bibliotecas itinerantes para zonas rurais."),
            ("Gonçalo Neves", "goncalo.neves@robotics.pt", "Engenheiro mecatrónico e investigador de robótica de salvamento aquático.")
        ]
        cursor.executemany('INSERT INTO creators (name, email, bio, project_count, total_raised) VALUES (?, ?, ?, 1, 0.0)', sample_creators)

        sample_projects = [
            ("EcoBikes Elétricas Solares", "Lia Mendonça", "Mobilidade Urbana", 25000.0, 18450.0, "Bicicletas elétricas de carregamento ultrarrápido com painéis solares para cidades inteligentes.", "2026-10-31", "Ativo", "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=600"),
            ("Documentário: Os Guardiões do Douro", "Mário Silva", "Cinema & Artes", 12000.0, 12000.0, "Filme sobre a tradição secular dos viticultores do Vale do Douro e a preservação do ecossistema.", "2026-09-25", "Financiado", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=600"),
            ("Biblioteca Itinerante Digital Sol-E-Ler", "Ana Beatriz", "Educação Social", 8500.0, 6200.0, "Carrinha solar equipada com tablets, internet satélite e livros físicos para escolas isoladas.", "2026-11-15", "Ativo", "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600"),
            ("Drone de Resgate Marítimo LifeBuoy AI", "Gonçalo Neves", "Tecnologia & Inovação", 40000.0, 31200.0, "Drone autónomo com visão computacional para apoio a salvamento nas praias da costa atlântica.", "2026-12-01", "Ativo", "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=600")
        ]
        cursor.executemany('INSERT INTO projects (title, creator_name, category, goal_amount, raised_amount, description, end_date, status, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_projects)

        sample_users = [
            ("Carlos Ramos", "carlos.ramos@invest.pt", "Investidor Anjo", 1500.0),
            ("Sofia Carvalho", "sofia.carvalho@gmail.com", "Apoiante VIP", 750.0),
            ("Pedro Santos", "pedro.santos@outlook.pt", "Doador Frequente", 320.0),
            ("Inês Figueiredo", "ines.figueiredo@sapo.pt", "Membro Comunidade", 200.0)
        ]
        cursor.executemany('INSERT INTO users (name, email, role, total_donated) VALUES (?, ?, ?, ?)', sample_users)

        sample_donations = [
            (1, "Carlos Ramos", "carlos.ramos@invest.pt", 1000.0, "Patrono Ouro (Kit Completo + Nome no Painel)", "2026-09-10 14:30"),
            (1, "Sofia Carvalho", "sofia.carvalho@gmail.com", 250.0, "Apoiante Prata (Bicicleta Teste 48h)", "2026-09-11 10:15"),
            (2, "Pedro Santos", "pedro.santos@outlook.pt", 300.0, "Bilhete VIP Estreia Cinema + Livro Artbook", "2026-09-08 18:45"),
            (3, "Inês Figueiredo", "ines.figueiredo@sapo.pt", 150.0, "Kit Leitor Digital + Certificado Doador", "2026-09-12 09:20"),
            (4, "Carlos Ramos", "carlos.ramos@invest.pt", 500.0, "Patrono Ouro (Demonstração Live de Resgate)", "2026-09-12 16:05")
        ]
        cursor.executemany('INSERT INTO donations (project_id, donor_name, donor_email, amount, reward_tier, created_at) VALUES (?, ?, ?, ?, ?, ?)', sample_donations)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de Dados crowdfund.db inicializado com sucesso!")
