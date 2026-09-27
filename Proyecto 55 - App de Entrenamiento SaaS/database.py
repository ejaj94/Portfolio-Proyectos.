import os
import sqlite3
from datetime import datetime, timedelta

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'workouts.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Routines Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'Hipertrofia',
            target_days TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Exercise Catalog Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            equipment TEXT NOT NULL DEFAULT 'Barra',
            instructions TEXT NOT NULL,
            video_url TEXT DEFAULT ''
        )
    ''')

    # 3. Routine Exercises Mapping Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routine_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            routine_id INTEGER NOT NULL,
            exercise_id INTEGER NOT NULL,
            target_sets INTEGER NOT NULL DEFAULT 4,
            target_reps TEXT NOT NULL DEFAULT '8-12',
            order_index INTEGER DEFAULT 1,
            FOREIGN KEY (routine_id) REFERENCES routines (id) ON DELETE CASCADE,
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
    ''')

    # 4. Workout Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            routine_name TEXT NOT NULL,
            workout_date TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            total_volume_kg REAL DEFAULT 0.0,
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Set Logs Table (Series, Reps, Weight)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS set_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_log_id INTEGER NOT NULL,
            exercise_name TEXT NOT NULL,
            set_number INTEGER NOT NULL,
            set_type TEXT NOT NULL DEFAULT 'Trabalho',
            reps INTEGER NOT NULL,
            weight_kg REAL NOT NULL,
            is_pr INTEGER DEFAULT 0,
            FOREIGN KEY (workout_log_id) REFERENCES workout_logs (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed Demo Data if empty
    cursor.execute('SELECT COUNT(*) FROM exercises')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def seed_data(cursor):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    date_prev1 = (now - timedelta(days=2)).strftime("%Y-%m-%d")
    date_prev2 = (now - timedelta(days=5)).strftime("%Y-%m-%d")

    # 1. Seed Exercises Catalog
    exercises_data = [
        ('Supino Reto com Barra', 'Peito', 'Barra Olimpíada', 'Deite-se no banco plano, segure a barra com uma pegada ligeiramente mais larga que os ombros, desça até ao peito e empurre com força explosiva.'),
        ('Supino Inclinado com Halteres', 'Peito', 'Halteres', 'Ajuste o banco a 30 graus, mantenha os cotovelos a 45º do tronco e eleve os halteres convergindo no topo.'),
        ('Agachamento Livre com Barra', 'Pernas', 'Barra Olímpica', 'Posicione a barra nos trapézios, pés à largura dos ombros, agache até passar os 90 graus mantendo as costas direitas.'),
        ('Prensa de Pernas (Leg Press 45º)', 'Pernas', 'Máquina', 'Empurre a plataforma com os calcanhares sem bloquear completamente os joelhos no topo.'),
        ('Levantamento Terra (Deadlift)', 'Costas', 'Barra Olímpica', 'Mantenha a barra junto às canelas, peito aberto, ombros para trás e eleve a carga usando a força dos glúteos e isquiotibiais.'),
        ('Puxada à Frente na Polia (Lat Pulldown)', 'Costas', 'Máquina Polia', 'Puxe a barra em direção ao peito contraindo as grande dorsais e estenda os braços com controlo.'),
        ('Press Militar de Ombros', 'Ombros', 'Barra', 'Em pé ou sentado, empurre a barra verticalmente acima da cabeça até ao bloqueio controlado dos braços.'),
        ('Elevação Lateral com Halteres', 'Ombros', 'Halteres', 'Eleve os halteres lateralmente até à altura dos ombros focando no deltoide lateral.'),
        ('Curl de Bíceps com Barra Z', 'Braços', 'Barra Z', 'Mantenha os cotovelos fixos junto ao tronco e flecta os braços focando na contração do bíceps.'),
        ('Tríceps na Polia Alta com Corda', 'Braços', 'Máquina Polia', 'Estenda os braços para baixo separando a corda no final do movimento para contração máxima do tríceps.')
    ]
    cursor.executemany('''
        INSERT INTO exercises (name, muscle_group, equipment, instructions)
        VALUES (?, ?, ?, ?)
    ''', exercises_data)

    # 2. Seed Routines
    routines_data = [
        ('Push / Peito, Ombros e Tríceps', 'Push/Pull/Legs', 'Segunda & Quinta', 'Rotina focada no desenvolvimento hipertrófico da musculatura de empurrar.'),
        ('Pull / Costas, Bíceps e Deltoide Posterior', 'Push/Pull/Legs', 'Terça & Sexta', 'Foco na densidade de costas, puxadas pesadas e flexão de braços.'),
        ('Legs / Pernas Completo & Glúteos', 'Push/Pull/Legs', 'Quarta & Sábado', 'Treino pesado de quadríceps, isquiotibiais e gémeos com cargas progressivas.')
    ]
    cursor.executemany('''
        INSERT INTO routines (name, category, target_days, description)
        VALUES (?, ?, ?, ?)
    ''', routines_data)

    # 3. Seed Routine Exercises
    # Push (Routine 1) -> Supino Reto (Ex 1), Supino Inclinado (Ex 2), Press Militar (Ex 7), Tríceps Corda (Ex 10)
    routine_exs = [
        (1, 1, 4, '8-10', 1),
        (1, 2, 4, '10-12', 2),
        (1, 7, 3, '8-10', 3),
        (1, 10, 4, '12-15', 4),
        # Pull (Routine 2) -> Levantamento Terra (Ex 5), Puxada (Ex 6), Curl Z (Ex 9)
        (2, 5, 4, '6-8', 1),
        (2, 6, 4, '10-12', 2),
        (2, 9, 4, '10-12', 3),
        # Legs (Routine 3) -> Agachamento (Ex 3), Leg Press (Ex 4)
        (3, 3, 4, '8-10', 1),
        (3, 4, 4, '10-12', 2)
    ]
    cursor.executemany('''
        INSERT INTO routine_exercises (routine_id, exercise_id, target_sets, target_reps, order_index)
        VALUES (?, ?, ?, ?, ?)
    ''', routine_exs)

    # 4. Seed Workout Logs
    # Workout 1 (Today - Push)
    cursor.execute('''
        INSERT INTO workout_logs (routine_name, workout_date, duration_minutes, total_volume_kg, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Push / Peito, Ombros e Tríceps', now_str, 55, 4820.0, 'Sessão com excelente energia! Novo recorde pessoal no Supino Reto.'))
    log1_id = cursor.lastrowid

    set_logs1 = [
        (log1_id, 'Supino Reto com Barra', 1, 'Aquecimento', 12, 60.0, 0),
        (log1_id, 'Supino Reto com Barra', 2, 'Trabalho', 10, 90.0, 0),
        (log1_id, 'Supino Reto com Barra', 3, 'Trabalho', 8, 100.0, 0),
        (log1_id, 'Supino Reto com Barra', 4, 'Trabalho', 6, 105.0, 1), # PR
        (log1_id, 'Supino Inclinado com Halteres', 1, 'Trabalho', 10, 32.0, 0),
        (log1_id, 'Supino Inclinado com Halteres', 2, 'Trabalho', 10, 32.0, 0),
        (log1_id, 'Press Militar de Ombros', 1, 'Trabalho', 8, 50.0, 0),
        (log1_id, 'Tríceps na Polia Alta com Corda', 1, 'Trabalho', 15, 35.0, 0)
    ]
    cursor.executemany('''
        INSERT INTO set_logs (workout_log_id, exercise_name, set_number, set_type, reps, weight_kg, is_pr)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', set_logs1)

    # Workout 2 (2 Days ago - Pull)
    cursor.execute('''
        INSERT INTO workout_logs (routine_name, workout_date, duration_minutes, total_volume_kg, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Pull / Costas, Bíceps e Deltoide Posterior', date_prev1, 60, 5340.0, 'Treino focado em densidade dorsal.'))
    log2_id = cursor.lastrowid

    set_logs2 = [
        (log2_id, 'Levantamento Terra (Deadlift)', 1, 'Trabalho', 8, 120.0, 0),
        (log2_id, 'Levantamento Terra (Deadlift)', 2, 'Trabalho', 6, 140.0, 0),
        (log2_id, 'Puxada à Frente na Polia (Lat Pulldown)', 1, 'Trabalho', 12, 65.0, 0),
        (log2_id, 'Curl de Bíceps com Barra Z', 1, 'Trabalho', 10, 35.0, 0)
    ]
    cursor.executemany('''
        INSERT INTO set_logs (workout_log_id, exercise_name, set_number, set_type, reps, weight_kg, is_pr)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', set_logs2)

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados workouts.db inicializada com sucesso para Proyecto 55!")
