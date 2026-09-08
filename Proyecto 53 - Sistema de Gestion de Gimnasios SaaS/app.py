import os
import sqlite3
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'gym.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_member_code():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM members')
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"SOC-2026-{100 + count}"

def generate_receipt_number():
    return f"REC-2026-{random.randint(800, 999)}"

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Total Active Members
    cursor.execute("SELECT COUNT(*) FROM members WHERE status = 'Ativo'")
    active_members_count = cursor.fetchone()[0]
    
    # 2. Total Monthly Revenue
    cursor.execute("SELECT SUM(amount) FROM payments WHERE status = 'Pago'")
    revenue_row = cursor.fetchone()[0]
    total_revenue = revenue_row if revenue_row else 0.0
    
    # 3. Today's Check-ins
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE checkin_time LIKE ?", (f"{today_str}%",))
    today_checkins_count = cursor.fetchone()[0]
    
    # 4. Expiring Memberships (Within next 7 days or already expired)
    cursor.execute("""
        SELECT m.*, p.name as plan_name 
        FROM members m 
        JOIN plans p ON m.plan_id = p.id 
        WHERE m.expiration_date <= date('now', '+7 days')
        ORDER BY m.expiration_date ASC
    """)
    expiring_members = cursor.fetchall()
    
    # 5. Recent Check-ins
    cursor.execute("SELECT * FROM attendance ORDER BY id DESC LIMIT 5")
    recent_checkins = cursor.fetchall()
    
    # 6. Today's Group Classes
    cursor.execute("SELECT * FROM classes ORDER BY id ASC")
    group_classes = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html',
                           active_members_count=active_members_count,
                           total_revenue=total_revenue,
                           today_checkins_count=today_checkins_count,
                           expiring_count=len(expiring_members),
                           expiring_members=expiring_members,
                           recent_checkins=recent_checkins,
                           group_classes=group_classes)

@app.route('/members')
def members_list():
    conn = get_db()
    cursor = conn.cursor()
    
    status_filter = request.args.get('status', '')
    query_search = request.args.get('q', '').strip()
    
    sql = """
        SELECT m.*, p.name as plan_name, p.price as plan_price 
        FROM members m 
        JOIN plans p ON m.plan_id = p.id 
        WHERE 1=1
    """
    params = []
    
    if status_filter:
        sql += " AND m.status = ?"
        params.append(status_filter)
        
    if query_search:
        sql += " AND (m.full_name LIKE ? OR m.member_code LIKE ? OR m.email LIKE ? OR m.nif LIKE ?)"
        term = f"%{query_search}%"
        params.extend([term, term, term, term])
        
    sql += " ORDER BY m.id DESC"
    
    cursor.execute(sql, params)
    members = cursor.fetchall()
    
    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()
    
    conn.close()
    return render_template('members.html', members=members, plans=plans, status_filter=status_filter, query_search=query_search)

@app.route('/member/new')
def member_new_form():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()
    conn.close()
    
    next_code = generate_member_code()
    return render_template('member_form.html', plans=plans, next_code=next_code)

@app.route('/member/<int:member_id>')
def member_detail(member_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT m.*, p.name as plan_name, p.price as plan_price, p.access_hours, p.perks 
        FROM members m 
        JOIN plans p ON m.plan_id = p.id 
        WHERE m.id = ?
    """, (member_id,))
    member = cursor.fetchone()
    
    if not member:
        conn.close()
        return "Sócio não encontrado", 404
        
    cursor.execute("SELECT * FROM payments WHERE member_id = ? ORDER BY id DESC", (member_id,))
    payments = cursor.fetchall()
    
    cursor.execute("SELECT * FROM attendance WHERE member_id = ? ORDER BY id DESC LIMIT 10", (member_id,))
    attendances = cursor.fetchall()
    
    conn.close()
    return render_template('member_detail.html', member=member, payments=payments, attendances=attendances)

@app.route('/plans')
def plans_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plans ORDER BY price ASC")
    plans = cursor.fetchall()
    conn.close()
    return render_template('plans.html', plans=plans)

@app.route('/payments')
def payments_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, m.full_name as member_name, m.member_code 
        FROM payments p 
        JOIN members m ON p.member_id = m.id 
        ORDER BY p.id DESC
    """)
    payments = cursor.fetchall()
    
    cursor.execute("SELECT * FROM members WHERE status = 'Ativo'")
    active_members = cursor.fetchall()
    
    conn.close()
    return render_template('payments.html', payments=payments, members=active_members)

@app.route('/trainers')
def trainers_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trainers ORDER BY id ASC")
    trainers = cursor.fetchall()
    conn.close()
    return render_template('trainers.html', trainers=trainers)

@app.route('/classes')
def classes_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classes ORDER BY schedule_time ASC")
    classes = cursor.fetchall()
    conn.close()
    return render_template('classes.html', classes=classes)

@app.route('/attendance')
def attendance_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance ORDER BY id DESC LIMIT 25")
    attendances = cursor.fetchall()
    
    cursor.execute("SELECT * FROM members WHERE status = 'Ativo'")
    members = cursor.fetchall()
    
    conn.close()
    return render_template('attendance.html', attendances=attendances, members=members)

@app.route('/expirations')
def expirations_page():
    conn = get_db()
    cursor = conn.cursor()
    
    # Expirations query
    cursor.execute("""
        SELECT m.*, p.name as plan_name, p.price as plan_price 
        FROM members m 
        JOIN plans p ON m.plan_id = p.id 
        WHERE m.expiration_date <= date('now', '+15 days')
        ORDER BY m.expiration_date ASC
    """)
    expiring_members = cursor.fetchall()
    
    conn.close()
    return render_template('expirations.html', members=expiring_members)

# REST API ENDPOINTS

@app.route('/api/members/create', methods=['POST'])
def api_create_member():
    try:
        data = request.get_json()
        code = generate_member_code()
        name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        nif = data.get('nif', '').strip()
        plan_id = int(data.get('plan_id', 1))
        
        now = datetime.now()
        start_date = now.strftime("%Y-%m-%d")
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT duration_months, price FROM plans WHERE id = ?", (plan_id,))
        plan_row = cursor.fetchone()
        duration = plan_row['duration_months'] if plan_row else 1
        plan_price = plan_row['price'] if plan_row else 35.0
        
        expiration_date = (now + timedelta(days=30 * duration)).strftime("%Y-%m-%d")
        
        cursor.execute("""
            INSERT INTO members (member_code, full_name, email, phone, nif, plan_id, start_date, expiration_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Ativo')
        """, (code, name, email, phone, nif, plan_id, start_date, expiration_date))
        
        member_id = cursor.lastrowid
        
        # Initial Payment Record
        receipt = generate_receipt_number()
        cursor.execute("""
            INSERT INTO payments (member_id, receipt_number, amount, payment_method, status)
            VALUES (?, ?, ?, 'MBWay', 'Pago')
        """, (member_id, receipt, plan_price))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'code': code, 'message': 'Sócio registado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/attendance/checkin', methods=['POST'])
def api_record_checkin():
    try:
        data = request.get_json()
        member_id = data.get('member_id')
        entry_type = data.get('entry_type', 'Torniquete QR')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, status, expiration_date FROM members WHERE id = ?", (member_id,))
        member = cursor.fetchone()
        
        if not member:
            conn.close()
            return jsonify({'success': False, 'message': 'Sócio não encontrado.'}), 404
            
        if member['status'] != 'Ativo':
            conn.close()
            return jsonify({'success': False, 'message': f"Acesso Negado: A quota de {member['full_name']} está {member['status']}!"}), 403
            
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO attendance (member_id, member_name, checkin_time, entry_type)
            VALUES (?, ?, ?, ?)
        """, (member_id, member['full_name'], now_str, entry_type))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'member_name': member['full_name'], 'message': f"Entrada autorizada! Bom treino, {member['full_name']}."})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/members/renew', methods=['POST'])
def api_renew_membership():
    try:
        data = request.get_json()
        member_id = data.get('member_id')
        payment_method = data.get('payment_method', 'MBWay')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.full_name, m.expiration_date, p.price, p.duration_months 
            FROM members m 
            JOIN plans p ON m.plan_id = p.id 
            WHERE m.id = ?
        """, (member_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'success': False, 'message': 'Sócio não encontrado.'}), 404
            
        now = datetime.now()
        current_exp = datetime.strptime(row['expiration_date'], "%Y-%m-%d") if row['expiration_date'] else now
        new_start = now if current_exp < now else current_exp
        new_exp = (new_start + timedelta(days=30 * row['duration_months'])).strftime("%Y-%m-%d")
        
        cursor.execute("""
            UPDATE members 
            SET expiration_date = ?, status = 'Ativo' 
            WHERE id = ?
        """, (new_exp, member_id))
        
        # Payment record
        receipt = generate_receipt_number()
        cursor.execute("""
            INSERT INTO payments (member_id, receipt_number, amount, payment_method, status)
            VALUES (?, ?, ?, ?, 'Pago')
        """, (member_id, receipt, row['price'], payment_method))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'new_expiration': new_exp, 'message': f"Quota renovada com sucesso até {new_exp}!"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - Sistema de Gestão de Gimnasios SaaS na porta 6906...")
    app.run(host='0.0.0.0', port=6906, debug=True)
