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

    # Reset tables to seed rich high-definition data
    cursor.execute('DELETE FROM donations')
    cursor.execute('DELETE FROM projects')
    cursor.execute('DELETE FROM creators')
    cursor.execute('DELETE FROM users')

    sample_creators = [
        ("Eng.ª Lia Mendonça", "lia.mendonca@techportugal.pt", "Especialista em Engenharia de Energias Renováveis e investigadora sénior do EcoTech Lab. Lidera projetos internacionais de descarbonização urbana e mobilidade solar autónoma."),
        ("Mário Silva", "mario.silva@creativestudio.pt", "Realizador de cinema independente, produtor audiovisual de documentários de património cultural e mentor de jovens talentos de animação e artes plásticas em Portugal."),
        ("Prof.ª Ana Beatriz", "ana.beatriz@eduopen.pt", "Educadora social, doutorada em Pedagogia e dinamizadora de bibliotecas itinerantes para erradicação da info-exclusão em comunidades vulneráveis e zonas rurais."),
        ("Eng.º Gonçalo Neves", "goncalo.neves@robotics.pt", "Engenheiro mecatrónico e investigador especializado em robótica de salvamento aquático e sistemas autónomos de apoio a equipas de resgate na costa atlântica.")
    ]
    cursor.executemany('INSERT INTO creators (name, email, bio, project_count, total_raised) VALUES (?, ?, ?, 1, 0.0)', sample_creators)

    sample_projects = [
        ("EcoBikes Elétricas Solares de Alta Eficiência", "Eng.ª Lia Mendonça", "Mobilidade Urbana & Sustentabilidade", 25000.0, 18450.0, "Sistema de mobilidade urbana inteligente baseado em bicicletas elétricas ultraleves com baterias fotovoltaicas de carregamento solar autónomo e telemetria GPS em tempo real.", "2026-10-31", "Ativo", "https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=600"),
        ("Documentário Histórico: Os Guardiões do Douro", "Mário Silva", "Cinema & Património Cultural", 12000.0, 12000.0, "Produção cinematográfica independente em resolução 4K sobre a tradição secular dos viticultores do Vale do Douro, a preservação ambiental e a arquitetura das encostas património mundial.", "2026-09-25", "Financiado", "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=600"),
        ("Biblioteca Itinerante Digital Sol-E-Ler", "Prof.ª Ana Beatriz", "Educação Social & Inclusão Digital", 8500.0, 6200.0, "Unidade móvel solar equipada com computadores, impressoras 3D, ligação satélite Starlink e acervo literário digital para prestar apoio pedagógico e tecnológico em aldeias isoladas.", "2026-11-15", "Ativo", "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600"),
        ("Drone de Resgate Marítimo LifeBuoy AI", "Eng.º Gonçalo Neves", "Tecnologia & Robótica de Resgate", 40000.0, 31200.0, "Aparelho aéreo não tripulado dotado de visão computacional e inteligência artificial para deteção automática de banhistas em aflição e lançamento imediato de bóias insufláveis em alto mar.", "2026-12-01", "Ativo", "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=600")
    ]
    cursor.executemany('INSERT INTO projects (title, creator_name, category, goal_amount, raised_amount, description, end_date, status, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_projects)

    sample_users = [
        ("Dr. Carlos Ramos", "carlos.ramos@invest.pt", "Investidor Anjo & Patrono VIP", 1500.0),
        ("Dra. Sofia Carvalho", "sofia.carvalho@gmail.com", "Apoiante Estratégica", 750.0),
        ("Pedro Santos", "pedro.santos@outlook.pt", "Doador Frequente", 320.0),
        ("Inês Figueiredo", "ines.figueiredo@sapo.pt", "Membro da Comunidade", 200.0)
    ]
    cursor.executemany('INSERT INTO users (name, email, role, total_donated) VALUES (?, ?, ?, ?)', sample_users)

    sample_donations = [
        (1, "Dr. Carlos Ramos", "carlos.ramos@invest.pt", 1000.0, "Patrono Ouro (Kit Completo + Gravura no Painel Solar)", "2026-09-10 14:30"),
        (1, "Dra. Sofia Carvalho", "sofia.carvalho@gmail.com", 250.0, "Patrono Prata (Acesso Prioritário ao Test-Drive de 48h)", "2026-09-11 10:15"),
        (2, "Pedro Santos", "pedro.santos@outlook.pt", 300.0, "Bilhete VIP Estreia de Cinema + Edição Limitada do Artbook", "2026-09-08 18:45"),
        (3, "Inês Figueiredo", "ines.figueiredo@sapo.pt", 150.0, "Kit Leitor Digital + Certificado Oficial de Doador Fundador", "2026-09-12 09:20"),
        (4, "Dr. Carlos Ramos", "carlos.ramos@invest.pt", 500.0, "Patrono Ouro (Demonstração Exclusiva de Resgate Live no Mar)", "2026-09-12 16:05")
    ]
    cursor.executemany('INSERT INTO donations (project_id, donor_name, donor_email, amount, reward_tier, created_at) VALUES (?, ?, ?, ?, ?, ?)', sample_donations)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de Dados crowdfund.db atualizado com definições de alta precisão!")
