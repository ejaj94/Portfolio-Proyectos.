import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'habits.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de Hábitos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            frequency TEXT DEFAULT 'Diário',
            current_streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            icon TEXT DEFAULT 'fa-check',
            color TEXT DEFAULT '#10b981',
            completed_today INTEGER DEFAULT 0,
            created_at DATE DEFAULT CURRENT_DATE
        )
    ''')

    # Tabela de Histórico de Conclusão (Logs)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            log_date DATE NOT NULL,
            status TEXT DEFAULT 'Completed',
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    ''')

    # Tabela de Objetivos / Metas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            target_value REAL NOT NULL,
            current_value REAL DEFAULT 0.0,
            unit TEXT NOT NULL,
            deadline DATE,
            status TEXT DEFAULT 'Em Progresso'
        )
    ''')

    conn.commit()

    # Povoamento Inicial
    cursor.execute('SELECT COUNT(*) FROM habits')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)
        conn.commit()

    conn.close()
    print("[OK] Base de dados habits.db inicializada com êxito para Proyecto 40.")

def seed_data(cursor):
    habits = [
        ('Leitura Focada 30 Min', 'Aprendizagem', 'Diário', 14, 21, 'fa-book', '#8b5cf6', 1),
        ('Treino de Alta Intensidade', 'Fitness', 'Diário', 8, 15, 'fa-dumbbell', '#10b981', 1),
        ('Meditação & Respiração Box', 'Mente', 'Diário', 19, 30, 'fa-brain', '#3b82f6', 1),
        ('Hidratação 3 Litros de Água', 'Saúde', 'Diário', 25, 45, 'fa-droplet', '#06b6d4', 0),
        ('Deep Work sem Distrações (2h)', 'Foco', 'Diário', 11, 18, 'fa-bolt', '#f59e0b', 0),
        ('Suplementação & Vitaminas', 'Saúde', 'Diário', 5, 12, 'fa-capsules', '#ec4899', 1)
    ]

    cursor.executemany('''
        INSERT INTO habits (title, category, frequency, current_streak, best_streak, icon, color, completed_today)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', habits)

    today = datetime.now().date()
    
    # Gerar logs passados dos últimos 30 dias para os hábitos
    for habit_id in range(1, 7):
        for i in range(30):
            past_date = today - timedelta(days=i)
            # Simular consistência alta (80% dos dias concluídos)
            if (i + habit_id) % 5 != 0 or i == 0:
                cursor.execute('''
                    INSERT INTO habit_logs (habit_id, log_date, status)
                    VALUES (?, ?, 'Completed')
                ''', (habit_id, past_date.strftime('%Y-%m-%d')))

    # Inserir Objetivos
    goals = [
        ('Ler 12 Livros de Neurociência & Produtividade em 2026', 'Aprendizagem', 12.0, 8.0, 'livros', '2026-12-31', 'Em Progresso'),
        ('Completar 100 Dias de Meditação Guiada', 'Mente', 100.0, 65.0, 'dias', '2026-10-15', 'Em Progresso'),
        ('Acumular 50 Horas de Treino Físico Intenso', 'Fitness', 50.0, 32.0, 'horas', '2026-08-30', 'Em Progresso'),
        ('Manter Streak de Foco Profundo por 30 Dias', 'Foco', 30.0, 18.0, 'dias', '2026-09-30', 'Em Progresso')
    ]

    cursor.executemany('''
        INSERT INTO goals (title, category, target_value, current_value, unit, deadline, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', goals)

if __name__ == '__main__':
    init_db()
