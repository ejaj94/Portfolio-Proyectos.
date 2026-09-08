import os
import sqlite3
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ejajtech_client_portal_secret_key_2026'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'clientportal.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Middleware check current user
def get_current_user():
    user_id = session.get('user_id', 1) # Default demo user ID 1
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password_hash = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['company_name'] = user['company_name']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciais inválidas. Por favor tente novamente.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    # Active Projects
    cursor.execute('SELECT COUNT(*) FROM projects WHERE client_id = ? AND status != "Concluído"', (user['id'],))
    active_projects_count = cursor.fetchone()[0]
    
    # Pending Invoices Total
    cursor.execute('SELECT SUM(total_amount) FROM invoices WHERE client_id = ? AND status = "Pendente"', (user['id'],))
    pending_invoices_row = cursor.fetchone()[0]
    pending_invoices_total = pending_invoices_row if pending_invoices_row else 0.0
    
    # Approved Budgets Total
    cursor.execute('SELECT SUM(amount) FROM budgets WHERE client_id = ? AND status = "Aprovado"', (user['id'],))
    approved_budgets_row = cursor.fetchone()[0]
    approved_budgets_total = approved_budgets_row if approved_budgets_row else 0.0
    
    # Open Tickets
    cursor.execute('SELECT COUNT(*) FROM support_tickets WHERE client_id = ? AND status != "Resolvido"', (user['id'],))
    open_tickets_count = cursor.fetchone()[0]
    
    # Projects list
    cursor.execute('SELECT * FROM projects WHERE client_id = ? ORDER BY id DESC', (user['id'],))
    projects = cursor.fetchall()
    
    # Recent Messages
    cursor.execute('SELECT * FROM messages WHERE client_id = ? ORDER BY id DESC LIMIT 5', (user['id'],))
    messages = cursor.fetchall()
    
    # Recent Invoices
    cursor.execute('SELECT * FROM invoices WHERE client_id = ? ORDER BY id DESC LIMIT 3', (user['id'],))
    invoices = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                           user=user,
                           active_projects_count=active_projects_count,
                           pending_invoices_total=pending_invoices_total,
                           approved_budgets_total=approved_budgets_total,
                           open_tickets_count=open_tickets_count,
                           projects=projects,
                           messages=messages,
                           invoices=invoices)

@app.route('/projects')
def projects():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE client_id = ? ORDER BY id DESC', (user['id'],))
    projects_list = cursor.fetchall()
    conn.close()
    
    return render_template('projects.html', user=user, projects=projects_list)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ? AND client_id = ?', (project_id, user['id']))
    project = cursor.fetchone()
    
    if not project:
        conn.close()
        return "Projeto não encontrado", 404
        
    cursor.execute('SELECT * FROM milestones WHERE project_id = ? ORDER BY id ASC', (project_id,))
    milestones = cursor.fetchall()
    
    cursor.execute('SELECT * FROM documents WHERE project_id = ? ORDER BY id DESC', (project_id,))
    documents = cursor.fetchall()
    
    cursor.execute('SELECT * FROM messages WHERE project_id = ? ORDER BY id ASC', (project_id,))
    messages = cursor.fetchall()
    
    conn.close()
    return render_template('project_detail.html', user=user, project=project, milestones=milestones, documents=documents, messages=messages)

@app.route('/budgets')
def budgets():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM budgets WHERE client_id = ? ORDER BY id DESC', (user['id'],))
    budgets_list = cursor.fetchall()
    conn.close()
    
    return render_template('budgets.html', user=user, budgets=budgets_list)

@app.route('/invoices')
def invoices():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM invoices WHERE client_id = ? ORDER BY id DESC', (user['id'],))
    invoices_list = cursor.fetchall()
    conn.close()
    
    return render_template('invoices.html', user=user, invoices=invoices_list)

@app.route('/documents')
def documents():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents WHERE client_id = ? ORDER BY id DESC', (user['id'],))
    docs_list = cursor.fetchall()
    conn.close()
    
    return render_template('documents.html', user=user, documents=docs_list)

@app.route('/messages')
def messages():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE client_id = ? ORDER BY id ASC', (user['id'],))
    messages_list = cursor.fetchall()
    
    cursor.execute('SELECT * FROM projects WHERE client_id = ?', (user['id'],))
    projects_list = cursor.fetchall()
    conn.close()
    
    return render_template('messages.html', user=user, messages=messages_list, projects=projects_list)

@app.route('/support')
def support():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM support_tickets WHERE client_id = ? ORDER BY id DESC', (user['id'],))
    tickets_list = cursor.fetchall()
    conn.close()
    
    return render_template('support.html', user=user, tickets=tickets_list)

@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    return render_template('profile.html', user=user)

# REST API ENDPOINTS

@app.route('/api/messages/send', methods=['POST'])
def api_send_message():
    try:
        user = get_current_user()
        data = request.get_json()
        content = data.get('content', '').strip()
        project_id = data.get('project_id')
        
        if not content:
            return jsonify({'success': False, 'message': 'A mensagem não pode estar vazia.'}), 400
            
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (client_id, project_id, sender_name, is_agency, content)
            VALUES (?, ?, ?, 0, ?)
        ''', (user['id'], project_id, user['full_name'], content))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Mensagem enviada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/tickets/create', methods=['POST'])
def api_create_ticket():
    try:
        user = get_current_user()
        data = request.get_json()
        subject = data.get('subject', '').strip()
        priority = data.get('priority', 'Média')
        description = data.get('description', '').strip()
        
        ticket_code = f"TK-2026-{random.randint(500, 999)}"
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO support_tickets (client_id, ticket_code, subject, priority, status, description)
            VALUES (?, ?, ?, ?, 'Aberto', ?)
        ''', (user['id'], ticket_code, subject, priority, description))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'ticket_code': ticket_code, 'message': 'Ticket de suporte criado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/budgets/approve', methods=['POST'])
def api_approve_budget():
    try:
        data = request.get_json()
        budget_id = data.get('budget_id')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE budgets SET status = "Aprovado" WHERE id = ?', (budget_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Orçamento aprovado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/profile/update', methods=['POST'])
def api_update_profile():
    try:
        user = get_current_user()
        data = request.get_json()
        full_name = data.get('full_name', '').strip()
        company_name = data.get('company_name', '').strip()
        phone = data.get('phone', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET full_name = ?, company_name = ?, phone = ? WHERE id = ?
        ''', (full_name, company_name, phone, user['id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Perfil atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - Portal de Clientes SaaS na porta 6905...")
    app.run(host='0.0.0.0', port=6905, debug=True)
