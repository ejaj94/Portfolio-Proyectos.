import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'ejajtech_mindhabit_tracker_secret_2026'

database.init_db()

@app.route('/')
def index():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM habits ORDER BY id ASC')
    habits = cursor.fetchall()

    # Métricas de Streaks e Conclusão Hoje
    total_habits = len(habits)
    completed_today_count = sum(1 for h in habits if h['completed_today'] == 1)
    completion_rate = (completed_today_count / total_habits * 100) if total_habits > 0 else 0

    best_current_streak = max((h['current_streak'] for h in habits), default=0)
    total_best_streak = max((h['best_streak'] for h in habits), default=0)

    conn.close()

    return render_template(
        'index.html',
        habits=habits,
        total_habits=total_habits,
        completed_today_count=completed_today_count,
        completion_rate=completion_rate,
        best_current_streak=best_current_streak,
        total_best_streak=total_best_streak
    )

@app.route('/calendar')
def calendar():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM habits ORDER BY title ASC')
    habits = cursor.fetchall()

    today = datetime.now().date()
    # Construir calendário dos últimos 28 dias (4 semanas)
    days_list = []
    for i in range(27, -1, -1):
        day_date = today - timedelta(days=i)
        date_str = day_date.strftime('%Y-%m-%d')
        
        # Buscar logs desse dia
        cursor.execute('''
            SELECT COUNT(*) FROM habit_logs WHERE log_date = ? AND status = 'Completed'
        ''', (date_str,))
        completed_count = cursor.fetchone()[0]

        days_list.append({
            'date': date_str,
            'day_name': day_date.strftime('%a'),
            'day_number': day_date.day,
            'completed_count': completed_count,
            'is_today': (day_date == today)
        })

    conn.close()

    return render_template('calendar.html', habits=habits, days_list=days_list)

@app.route('/analytics')
def analytics():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Hábitos por Categoria
    cursor.execute('''
        SELECT category, COUNT(*) as count, SUM(current_streak) as total_streak
        FROM habits
        GROUP BY category
    ''')
    categories_data = cursor.fetchall()

    # Tendência dos últimos 7 dias
    today = datetime.now().date()
    weekly_trend = []

    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        date_str = d.strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) FROM habit_logs WHERE log_date = ? AND status = 'Completed'
        ''', (date_str,))
        cnt = cursor.fetchone()[0]
        weekly_trend.append({
            'day': d.strftime('%d/%m'),
            'count': cnt
        })

    cursor.execute('SELECT * FROM habits')
    habits = cursor.fetchall()
    conn.close()

    return render_template(
        'analytics.html',
        categories_data=categories_data,
        weekly_trend=weekly_trend,
        habits=habits
    )

@app.route('/goals')
def goals():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM goals ORDER BY deadline ASC')
    goals_list = cursor.fetchall()
    conn.close()

    return render_template('goals.html', goals=goals_list)

# --- APIS REST ---

def _get_req_data():
    if request.is_json and request.get_json(silent=True):
        return request.get_json(silent=True)
    if request.form:
        return request.form.to_dict()
    if request.data:
        try:
            return json.loads(request.data.decode('utf-8'))
        except:
            pass
    return request.args.to_dict() or {}

@app.route('/api/habits/toggle', methods=['POST'])
def api_habit_toggle():
    data = _get_req_data()
    habit_id = data.get('habit_id')

    if not habit_id:
        return jsonify({'success': False, 'message': 'ID do hábito inválido'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
    habit = cursor.fetchone()

    if not habit:
        conn.close()
        return jsonify({'success': False, 'message': 'Hábito não encontrado'}), 404

    new_status = 0 if habit['completed_today'] == 1 else 1
    today_str = datetime.now().date().strftime('%Y-%m-%d')

    if new_status == 1:
        new_streak = habit['current_streak'] + 1
        new_best = max(habit['best_streak'], new_streak)
        cursor.execute('''
            UPDATE habits
            SET completed_today = 1, current_streak = ?, best_streak = ?
            WHERE id = ?
        ''', (new_streak, new_best, habit_id))

        cursor.execute('''
            INSERT INTO habit_logs (habit_id, log_date, status)
            VALUES (?, ?, 'Completed')
        ''', (habit_id, today_str))
    else:
        new_streak = max(0, habit['current_streak'] - 1)
        cursor.execute('''
            UPDATE habits
            SET completed_today = 0, current_streak = ?
            WHERE id = ?
        ''', (new_streak, habit_id))

        cursor.execute('''
            DELETE FROM habit_logs WHERE habit_id = ? AND log_date = ?
        ''', (habit_id, today_str))

    conn.commit()

    # Recalcular métricas globais
    cursor.execute('SELECT COUNT(*), SUM(completed_today) FROM habits')
    tot, comp = cursor.fetchone()
    rate = (comp / tot * 100) if tot > 0 else 0

    conn.close()

    return jsonify({
        'success': True,
        'completed_today': new_status,
        'current_streak': new_streak,
        'completion_rate': round(rate, 1),
        'message': 'Estado do hábito atualizado com êxito!'
    })

@app.route('/api/habits/create', methods=['POST'])
def api_habit_create():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'Saúde')
    icon = request.form.get('icon', 'fa-check')
    color = request.form.get('color', '#10b981')

    if not title:
        flash('O título do hábito é obrigatório.', 'danger')
        return redirect(url_for('index'))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO habits (title, category, frequency, current_streak, best_streak, icon, color, completed_today)
        VALUES (?, ?, 'Diário', 0, 0, ?, ?, 0)
    ''', (title, category, icon, color))

    conn.commit()
    conn.close()

    flash(f'Hábito "{title}" criado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/api/goals/create', methods=['POST'])
def api_goal_create():
    title = request.form.get('title', '').strip()
    category = request.form.get('category', 'Geral')
    target_value = float(request.form.get('target_value', 10.0))
    current_value = float(request.form.get('current_value', 0.0))
    unit = request.form.get('unit', 'unidades')
    deadline = request.form.get('deadline', '2026-12-31')

    if not title:
        flash('O título do objetivo é obrigatório.', 'danger')
        return redirect(url_for('goals'))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO goals (title, category, target_value, current_value, unit, deadline, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Em Progresso')
    ''', (title, category, target_value, current_value, unit, deadline))

    conn.commit()
    conn.close()

    flash(f'Objetivo "{title}" adicionado com êxito!', 'success')
    return redirect(url_for('goals'))

@app.route('/api/goals/update', methods=['POST'])
def api_goal_update():
    data = _get_req_data()
    goal_id = data.get('goal_id')
    add_val = float(data.get('add_value', 1.0))

    if not goal_id:
        return jsonify({'success': False, 'message': 'ID de objetivo inválido'}), 400

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM goals WHERE id = ?', (goal_id,))
    goal = cursor.fetchone()

    if not goal:
        conn.close()
        return jsonify({'success': False, 'message': 'Objetivo não encontrado'}), 404

    new_val = goal['current_value'] + add_val
    new_status = 'Concluído' if new_val >= goal['target_value'] else 'Em Progresso'

    cursor.execute('''
        UPDATE goals
        SET current_value = ?, status = ?
        WHERE id = ?
    ''', (new_val, new_status, goal_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'new_value': new_val,
        'status': new_status,
        'message': 'Progresso do objetivo atualizado!'
    })

if __name__ == '__main__':
    print("=" * 60)
    print(" [MINDHABIT SaaS] EJAJ TECH - Habit & Neuro-Performance Tracker")
    print(" Servidor Flask a correr em http://127.0.0.1:6200")
    print("=" * 60)
    app.run(host='0.0.0.0', port=6200, debug=True)
