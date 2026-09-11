import sqlite3
import os
from datetime import datetime, date, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'taskcraft.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Teams Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        lead_name TEXT NOT NULL,
        members_count INTEGER DEFAULT 1,
        color TEXT DEFAULT '#6366F1',
        created_at TEXT NOT NULL
    )
    """)

    # 2. Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        client_name TEXT NOT NULL,
        team_id INTEGER NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Em Progresso',
        start_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        budget REAL DEFAULT 0.0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (team_id) REFERENCES teams (id)
    )
    """)

    # 3. Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        assigned_to TEXT NOT NULL,
        priority TEXT DEFAULT 'Média',
        status TEXT DEFAULT 'A Fazer',
        due_date TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    # 4. Comments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        comment_text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    # 5. Files Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        file_name TEXT NOT NULL,
        file_size TEXT NOT NULL,
        category TEXT DEFAULT 'Documento',
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    )
    """)

    # Seed Initial Data if empty
    cursor.execute("SELECT COUNT(*) FROM teams")
    if cursor.fetchone()[0] == 0:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        today_str = date.today().strftime("%Y-%m-%d")
        next_month = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")

        # Seed Teams
        teams_data = [
            ("Equipa Core Engineering", "Eng. Ricardo Alves", 6, "#6366F1", now_str),
            ("Equipa UI/UX & Design", "Mariana Costa", 4, "#8B5CF6", now_str),
            ("Equipa Growth & Marketing", "Tiago Neves", 5, "#10B981", now_str),
            ("Equipa DevOps & Cloud", "Diogo Carvalhal", 3, "#38BDF8", now_str)
        ]
        cursor.executemany("""
        INSERT INTO teams (name, lead_name, members_count, color, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, teams_data)

        # Seed Projects
        projects_data = [
            ("Refatoração SaaS Enterprise 2.0", "EJAJ TECH Global", 1, "Migração de microsserviços para arquitetura Serverless de alta performance.", "Em Progresso", today_str, next_month, 45000.0, now_str),
            ("Redesign da Plataforma e Design System", "FinTech Innovators", 2, "Criação do novo Design System com suporte completo para modo escuro e glassmorphism.", "Em Progresso", today_str, (date.today() + timedelta(days=20)).strftime("%Y-%m-%d"), 28000.0, now_str),
            ("Infraestrutura Cloud Multi-Region", "SaaS Scaleup EU", 4, "Deploy automatizado com Terraform, Kubernetes e monitorização Datadog.", "Concluído", (date.today() - timedelta(days=40)).strftime("%Y-%m-%d"), today_str, 35000.0, now_str),
            ("Campanha de Aquisição B2B Q4", "EJAJ TECH Marketing", 3, "Estratégia de SEO, anúncios pagos e automação de funil de vendas.", "Em Espera", today_str, (date.today() + timedelta(days=45)).strftime("%Y-%m-%d"), 18000.0, now_str)
        ]
        cursor.executemany("""
        INSERT INTO projects (name, client_name, team_id, description, status, start_date, due_date, budget, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, projects_data)

        # Seed Tasks
        tasks_data = [
            (1, "Desenvolver API Gateway de Autenticação OAuth2", "Eng. Alexandre Mendes", "Alta", "Em Progresso", (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")),
            (1, "Configurar Cache de Alta Velocidade com Redis", "Diogo Carvalhal", "Média", "A Fazer", (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")),
            (1, "Executar Testes de Carga e Stress (10k req/s)", "Beatriz Fonseca", "Alta", "A Fazer", (date.today() + timedelta(days=15)).strftime("%Y-%m-%d")),
            (2, "Finalizar Componentes de Tabela e Modais em Figma", "Inês Guerreiro", "Alta", "Concluído", today_str),
            (2, "Criar Tokens de Cores e Tipografia em CSS3", "Mariana Costa", "Média", "Em Progresso", (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")),
            (3, "Provisionar Cluster Kubernetes no AWS EKS", "Diogo Carvalhal", "Alta", "Concluído", (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")),
            (4, "Desenvolver Landing Page de Alta Conversão", "Tiago Neves", "Baixa", "Em Progresso", (date.today() + timedelta(days=12)).strftime("%Y-%m-%d"))
        ]
        cursor.executemany("""
        INSERT INTO tasks (project_id, title, assigned_to, priority, status, due_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, tasks_data)

        # Seed Comments
        comments_data = [
            (1, "Eng. Ricardo Alves", "Arquitetura base aprovada pela equipa técnica. Vamos dar início aos testes de integrações de API.", now_str),
            (1, "Eng. Alexandre Mendes", "Endpoints de login e JWT já se encontram prontos em staging.", now_str),
            (2, "Inês Guerreiro", "Adicionados os protótipos interativos para a versão mobile.", now_str)
        ]
        cursor.executemany("""
        INSERT INTO comments (project_id, author, comment_text, created_at)
        VALUES (?, ?, ?, ?)
        """, comments_data)

        # Seed Files
        files_data = [
            (1, "Arquitetura_Sistema_TaskCraft_v2.pdf", "4.2 MB", "Documento", now_str),
            (2, "Design_System_Tokens_Figma.fig", "18.5 MB", "Design", now_str),
            (3, "Terraform_Cluster_EKS_Config.zip", "2.1 MB", "Código", now_str)
        ]
        cursor.executemany("""
        INSERT INTO files (project_id, file_name, file_size, category, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
        """, files_data)

    conn.commit()
    conn.close()
    print("[Database OK] taskcraft.db inicializada com sucesso.")

if __name__ == '__main__':
    init_db()
