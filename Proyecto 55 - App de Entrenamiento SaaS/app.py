import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'workouts.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Total Workouts Completed
    cursor.execute("SELECT COUNT(*) FROM workout_logs")
    total_workouts = cursor.fetchone()[0]
    
    # 2. Total Volume Moved (Tons)
    cursor.execute("SELECT SUM(total_volume_kg) FROM workout_logs")
    vol_row = cursor.fetchone()[0]
    total_volume_tons = (vol_row / 1000.0) if vol_row else 0.0
    
    # 3. Personal Records (PRs) Count
    cursor.execute("SELECT COUNT(*) FROM set_logs WHERE is_pr = 1")
    total_prs = cursor.fetchone()[0]
    
    # 4. Total Exercises Available
    cursor.execute("SELECT COUNT(*) FROM exercises")
    total_exercises = cursor.fetchone()[0]
    
    # 5. Recent Workout Logs
    cursor.execute("SELECT * FROM workout_logs ORDER BY id DESC LIMIT 5")
    recent_logs = cursor.fetchall()
    
    # 6. Active Routines
    cursor.execute("SELECT * FROM routines ORDER BY id ASC")
    routines = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html',
                           total_workouts=total_workouts,
                           total_volume_tons=total_volume_tons,
                           total_prs=total_prs,
                           total_exercises=total_exercises,
                           recent_logs=recent_logs,
                           routines=routines)

@app.route('/routines')
def routines_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routines ORDER BY id ASC")
    routines = cursor.fetchall()
    conn.close()
    return render_template('routines.html', routines=routines)

@app.route('/routine/<int:routine_id>')
def routine_detail(routine_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routines WHERE id = ?", (routine_id,))
    routine = cursor.fetchone()
    
    if not routine:
        conn.close()
        return "Rotina não encontrada", 404
        
    cursor.execute("""
        SELECT re.*, e.name as exercise_name, e.muscle_group, e.equipment 
        FROM routine_exercises re 
        JOIN exercises e ON re.exercise_id = e.id 
        WHERE re.routine_id = ? 
        ORDER BY re.order_index ASC
    """, (routine_id,))
    routine_exercises = cursor.fetchall()
    
    conn.close()
    return render_template('routine_detail.html', routine=routine, routine_exercises=routine_exercises)

@app.route('/exercises')
def exercises_page():
    conn = get_db()
    cursor = conn.cursor()
    
    muscle_filter = request.args.get('muscle', '')
    query_search = request.args.get('q', '').strip()
    
    sql = "SELECT * FROM exercises WHERE 1=1"
    params = []
    
    if muscle_filter:
        sql += " AND muscle_group = ?"
        params.append(muscle_filter)
        
    if query_search:
        sql += " AND (name LIKE ? OR equipment LIKE ? OR instructions LIKE ?)"
        term = f"%{query_search}%"
        params.extend([term, term, term])
        
    sql += " ORDER BY muscle_group ASC, name ASC"
    
    cursor.execute(sql, params)
    exercises = cursor.fetchall()
    
    conn.close()
    return render_template('exercises.html', exercises=exercises, muscle_filter=muscle_filter, query_search=query_search)

@app.route('/log/new')
def log_new_page():
    routine_id = request.args.get('routine_id')
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM exercises ORDER BY muscle_group ASC, name ASC")
    exercises = cursor.fetchall()
    
    routine = None
    preselected_exercises = []
    if routine_id:
        cursor.execute("SELECT * FROM routines WHERE id = ?", (routine_id,))
        routine = cursor.fetchone()
        if routine:
            cursor.execute("""
                SELECT e.name as exercise_name, re.target_sets, re.target_reps 
                FROM routine_exercises re 
                JOIN exercises e ON re.exercise_id = e.id 
                WHERE re.routine_id = ? 
                ORDER BY re.order_index ASC
            """, (routine_id,))
            preselected_exercises = cursor.fetchall()
            
    conn.close()
    return render_template('log_workout.html', exercises=exercises, routine=routine, preselected_exercises=preselected_exercises)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workout_logs ORDER BY id DESC")
    logs = cursor.fetchall()
    
    # Details of sets for each log
    log_details = {}
    for log in logs:
        cursor.execute("SELECT * FROM set_logs WHERE workout_log_id = ? ORDER BY id ASC", (log['id'],))
        log_details[log['id']] = cursor.fetchall()
        
    conn.close()
    return render_template('history.html', logs=logs, log_details=log_details)

@app.route('/progress')
def progress_page():
    conn = get_db()
    cursor = conn.cursor()
    
    # Personal Records Leaderboard
    cursor.execute("""
        SELECT exercise_name, MAX(weight_kg) as max_weight, reps, workout_log_id 
        FROM set_logs 
        GROUP BY exercise_name 
        ORDER BY max_weight DESC
    """)
    prs = cursor.fetchall()
    
    # Volume progression log
    cursor.execute("SELECT workout_date, routine_name, total_volume_kg FROM workout_logs ORDER BY id ASC")
    volume_history = cursor.fetchall()
    
    conn.close()
    return render_template('progress.html', prs=prs, volume_history=volume_history)

# REST API ENDPOINTS

@app.route('/api/workout/log', methods=['POST'])
def api_log_workout():
    try:
        data = request.get_json()
        routine_name = data.get('routine_name', 'Treino Livre').strip()
        duration = int(data.get('duration_minutes', 45))
        notes = data.get('notes', '').strip()
        sets_data = data.get('sets', [])
        
        now_str = datetime.now().strftime("%Y-%m-%d")
        
        total_volume = 0.0
        for s in sets_data:
            reps = int(s.get('reps', 0))
            weight = float(s.get('weight_kg', 0.0))
            total_volume += (reps * weight)
            
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO workout_logs (routine_name, workout_date, duration_minutes, total_volume_kg, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (routine_name, now_str, duration, total_volume, notes))
        
        log_id = cursor.lastrowid
        
        for s in sets_data:
            ex_name = s.get('exercise_name', '').strip()
            set_num = int(s.get('set_number', 1))
            set_type = s.get('set_type', 'Trabalho')
            reps = int(s.get('reps', 0))
            weight = float(s.get('weight_kg', 0.0))
            is_pr = 1 if s.get('is_pr') else 0
            
            if ex_name:
                cursor.execute("""
                    INSERT INTO set_logs (workout_log_id, exercise_name, set_number, set_type, reps, weight_kg, is_pr)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (log_id, ex_name, set_num, set_type, reps, weight, is_pr))
                
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Treino registado com sucesso! Bom trabalho!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/exercise/add', methods=['POST'])
def api_add_exercise():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        muscle = data.get('muscle_group', 'Peito').strip()
        equipment = data.get('equipment', 'Barra').strip()
        instructions = data.get('instructions', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exercises (name, muscle_group, equipment, instructions)
            VALUES (?, ?, ?, ?)
        """, (name, muscle, equipment, instructions))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Exercício adicionado à biblioteca!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - FitTracker App de Entrenamiento SaaS na porta 6908...")
    app.run(host='0.0.0.0', port=6908, debug=True)
