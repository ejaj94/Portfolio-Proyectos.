import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'nutrition.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    today_str = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    cursor = conn.cursor()

    # 1. Fetch User Daily Goals
    cursor.execute("SELECT * FROM daily_goals LIMIT 1")
    goals = cursor.fetchone()
    if not goals:
        goals = {
            'target_calories': 2200.0,
            'target_protein_g': 160.0,
            'target_carbs_g': 220.0,
            'target_fat_g': 60.0
        }

    # 2. Fetch Today's Consumed Totals
    cursor.execute("""
        SELECT 
            COALESCE(SUM(calories), 0.0) as total_cal,
            COALESCE(SUM(protein_g), 0.0) as total_prot,
            COALESCE(SUM(carbs_g), 0.0) as total_carbs,
            COALESCE(SUM(fat_g), 0.0) as total_fat
        FROM meal_logs
        WHERE log_date = ?
    """, (today_str,))
    totals = cursor.fetchone()

    consumed = {
        'calories': round(totals['total_cal'], 1),
        'protein_g': round(totals['total_prot'], 1),
        'carbs_g': round(totals['total_carbs'], 1),
        'fat_g': round(totals['total_fat'], 1)
    }

    # Percentages
    pct = {
        'calories': min(100, round((consumed['calories'] / goals['target_calories']) * 100)) if goals['target_calories'] > 0 else 0,
        'protein': min(100, round((consumed['protein_g'] / goals['target_protein_g']) * 100)) if goals['target_protein_g'] > 0 else 0,
        'carbs': min(100, round((consumed['carbs_g'] / goals['target_carbs_g']) * 100)) if goals['target_carbs_g'] > 0 else 0,
        'fat': min(100, round((consumed['fat_g'] / goals['target_fat_g']) * 100)) if goals['target_fat_g'] > 0 else 0
    }

    # 3. Today's Meals Categorized
    cursor.execute("SELECT * FROM meal_logs WHERE log_date = ? ORDER BY id ASC", (today_str,))
    all_today_logs = cursor.fetchall()

    meals_by_type = {
        'Pequeno-almoço': [],
        'Almoço': [],
        'Jantar': [],
        'Lanches': []
    }

    for log in all_today_logs:
        mtype = log['meal_type']
        if mtype in meals_by_type:
            meals_by_type[mtype].append(log)
        else:
            meals_by_type['Lanches'].append(log)

    conn.close()

    return render_template('index.html',
                           today_date=today_str,
                           goals=goals,
                           consumed=consumed,
                           pct=pct,
                           meals_by_type=meals_by_type)

@app.route('/foods')
def foods_page():
    conn = get_db()
    cursor = conn.cursor()
    
    category = request.args.get('category', '').strip()
    query_q = request.args.get('q', '').strip()

    sql = "SELECT * FROM foods WHERE 1=1"
    params = []

    if category:
        sql += " AND category = ?"
        params.append(category)

    if query_q:
        sql += " AND (name LIKE ? OR category LIKE ?)"
        term = f"%{query_q}%"
        params.extend([term, term])

    sql += " ORDER BY category ASC, name ASC"

    cursor.execute(sql, params)
    foods = cursor.fetchall()
    conn.close()

    return render_template('foods.html', foods=foods, category=category, query_q=query_q)

@app.route('/log')
def log_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM foods ORDER BY category ASC, name ASC")
    foods = cursor.fetchall()
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM meal_logs WHERE log_date = ? ORDER BY id DESC", (today_str,))
    recent_logs = cursor.fetchall()

    conn.close()

    return render_template('log.html', foods=foods, recent_logs=recent_logs, today_date=today_str)

@app.route('/goals')
def goals_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_goals LIMIT 1")
    goals = cursor.fetchone()
    conn.close()
    return render_template('goals.html', goals=goals)

@app.route('/stats')
def stats_page():
    conn = get_db()
    cursor = conn.cursor()

    # Macro distribution aggregated
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT log_date, 
               SUM(calories) as total_cal, 
               SUM(protein_g) as total_prot, 
               SUM(carbs_g) as total_carbs, 
               SUM(fat_g) as total_fat
        FROM meal_logs
        GROUP BY log_date
        ORDER BY log_date DESC
        LIMIT 7
    """)
    daily_history = cursor.fetchall()

    cursor.execute("SELECT * FROM daily_goals LIMIT 1")
    goals = cursor.fetchone()

    conn.close()
    return render_template('stats.html', daily_history=daily_history, goals=goals)

# REST API ENDPOINTS

@app.route('/api/log/add', methods=['POST'])
def api_add_log():
    try:
        data = request.get_json()
        log_date = data.get('log_date', datetime.now().strftime("%Y-%m-%d")).strip()
        meal_type = data.get('meal_type', 'Lanches').strip()
        food_name = data.get('food_name', '').strip()
        quantity_g = float(data.get('quantity_g', 100.0))

        if not food_name or quantity_g <= 0:
            return jsonify({'success': False, 'message': 'Introduza um alimento válido e quantidade em gramas.'}), 400

        conn = get_db()
        cursor = conn.cursor()
        
        # Look up food info in foods table
        cursor.execute("SELECT * FROM foods WHERE name = ?", (food_name,))
        food = cursor.fetchone()

        if food:
            mult = quantity_g / 100.0
            calories = round(food['calories_100g'] * mult, 1)
            protein = round(food['protein_g'] * mult, 1)
            carbs = round(food['carbs_g'] * mult, 1)
            fat = round(food['fat_g'] * mult, 1)
        else:
            # Custom quick manual values
            calories = round(float(data.get('calories', 0.0)), 1)
            protein = round(float(data.get('protein_g', 0.0)), 1)
            carbs = round(float(data.get('carbs_g', 0.0)), 1)
            fat = round(float(data.get('fat_g', 0.0)), 1)

        cursor.execute("""
            INSERT INTO meal_logs (log_date, meal_type, food_name, quantity_g, calories, protein_g, carbs_g, fat_g)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (log_date, meal_type, food_name, quantity_g, calories, protein, carbs, fat))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'{food_name} ({quantity_g}g) adicionado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/log/delete/<int:log_id>', methods=['POST', 'DELETE'])
def api_delete_log(log_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meal_logs WHERE id = ?", (log_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Registo de refeição removido.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/food/add', methods=['POST'])
def api_add_food():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        category = data.get('category', 'Proteínas').strip()
        calories = float(data.get('calories_100g', 0.0))
        protein = float(data.get('protein_g', 0.0))
        carbs = float(data.get('carbs_g', 0.0))
        fat = float(data.get('fat_g', 0.0))
        fiber = float(data.get('fiber_g', 0.0))

        if not name:
            return jsonify({'success': False, 'message': 'O nome do alimento é obrigatório.'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO foods (name, category, calories_100g, protein_g, carbs_g, fat_g, fiber_g)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, category, calories, protein, carbs, fat, fiber))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Alimento "{name}" criado e guardado na biblioteca!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/goals/update', methods=['POST'])
def api_update_goals():
    try:
        data = request.get_json()
        user_name = data.get('user_name', 'Enmanuel Jimenez').strip()
        cal = float(data.get('target_calories', 2200))
        prot = float(data.get('target_protein_g', 160))
        carbs = float(data.get('target_carbs_g', 220))
        fat = float(data.get('target_fat_g', 60))

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM daily_goals")
        cursor.execute("""
            INSERT INTO daily_goals (user_name, target_calories, target_protein_g, target_carbs_g, target_fat_g)
            VALUES (?, ?, ?, ?, ?)
        """, (user_name, cal, prot, carbs, fat))

        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Objetivos nutricionais atualizados com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - NutriTracker Dashboard SaaS na porta 6909...")
    app.run(host='0.0.0.0', port=6909, debug=True)
