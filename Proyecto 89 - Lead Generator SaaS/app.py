import os
import sqlite3
import csv
import io
import datetime
from flask import Flask, render_template, request, jsonify, Response
from database import get_db, init_db

app = Flask(__name__)

# Ensure DB initialized
init_db()

# --- Page Routes ---
@app.route('/')
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/landing')
def landing():
    return render_template('landing.html', active_page='landing')

@app.route('/leads')
def leads():
    return render_template('leads.html', active_page='leads')

@app.route('/followup')
def followup():
    return render_template('followup.html', active_page='followup')

@app.route('/email')
def email_page():
    return render_template('email.html', active_page='email')

@app.route('/stats')
def stats():
    return render_template('stats.html', active_page='stats')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html', active_page='showcase')

# --- REST API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM leads')
    total_leads = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM leads WHERE status = "Novo Lead"')
    new_leads = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM leads WHERE status = "Convertido"')
    converted_leads = cursor.fetchone()[0]

    cursor.execute('SELECT AVG(lead_score) FROM leads')
    avg_score = round(cursor.fetchone()[0] or 0, 1)

    conversion_rate = round((converted_leads / total_leads * 100.0) if total_leads > 0 else 0.0, 1)

    conn.close()

    return jsonify({
        'total_leads': total_leads,
        'new_leads': new_leads,
        'converted_leads': converted_leads,
        'conversion_rate': conversion_rate,
        'avg_score': avg_score
    })

@app.route('/api/leads', methods=['GET', 'POST'])
def handle_leads():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        company = data.get('company', '').strip()
        team_size = data.get('team_size', '1-10').strip()
        interest_area = data.get('interest_area', 'Consultoria TI').strip()
        source = data.get('source', 'Landing Page').strip()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name or not email:
            return jsonify({'success': False, 'message': 'Nome e Email são obrigatórios!'}), 400

        # Calculate initial lead score
        lead_score = 50
        if company: lead_score += 15
        if phone: lead_score += 15
        if team_size in ['10-50', '50-200', '200+']: lead_score += 20

        try:
            cursor.execute('''
                INSERT INTO leads (name, email, phone, company, team_size, interest_area, lead_score, status, source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Novo Lead', ?, ?)
            ''', (name, email, phone, company, team_size, interest_area, lead_score, source, now_str))
            conn.commit()
            lead_id = cursor.lastrowid
            conn.close()

            return jsonify({
                'success': True,
                'message': 'Obrigado! O seu pedido de contacto foi recebido com sucesso.',
                'lead_id': lead_id,
                'lead_score': lead_score
            })
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Este endereço de email já se encontra registado!'}), 400

    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    leads_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(leads_list)

@app.route('/api/leads/<int:lead_id>/status', methods=['PUT'])
def update_lead_status(lead_id):
    data = request.get_json() or {}
    new_status = data.get('status', '').strip()

    valid_statuses = ['Novo Lead', 'Contactado', 'Qualificado', 'Proposta Enviada', 'Convertido', 'Perdido']
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'message': 'Estado inválido!'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE leads SET status = ? WHERE id = ?', (new_status, lead_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': f'Estado do lead atualizado para "{new_status}".'})

@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        lead_id = data.get('lead_id')
        author = data.get('author', 'Gestor Comercial').strip()
        note_type = data.get('note_type', 'Chamada').strip()
        content = data.get('content', '').strip()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not lead_id or not content:
            return jsonify({'success': False, 'message': 'Selecione o lead e escreva a nota!'}), 400

        cursor.execute('''
            INSERT INTO notes (lead_id, author, note_type, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (lead_id, author, note_type, content, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Nota de seguimento adicionada com sucesso!'})

    cursor.execute('''
        SELECT notes.*, leads.name as lead_name, leads.company as lead_company
        FROM notes
        JOIN leads ON notes.lead_id = leads.id
        ORDER BY notes.id DESC
    ''')
    notes_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(notes_list)

@app.route('/api/email_templates', methods=['GET'])
def get_email_templates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM email_templates ORDER BY id ASC')
    templates = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(templates)

@app.route('/api/email/send', methods=['POST'])
def send_automated_email():
    data = request.get_json() or {}
    lead_id = data.get('lead_id')
    template_id = data.get('template_id')

    if not lead_id or not template_id:
        return jsonify({'success': False, 'message': 'Selecione o lead e o modelo de email!'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, company FROM leads WHERE id = ?', (lead_id,))
    lead = cursor.fetchone()
    cursor.execute('SELECT subject, body_text FROM email_templates WHERE id = ?', (template_id,))
    tmpl = cursor.fetchone()

    if not lead or not tmpl:
        conn.close()
        return jsonify({'success': False, 'message': 'Lead ou modelo não encontrado!'}), 404

    # Replace placeholders
    body = tmpl['body_text'].replace('{{NOME}}', lead['name']).replace('{{EMPRESA}}', lead['company'] or 'sua empresa')

    # Record follow-up note automatically
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute('''
        INSERT INTO notes (lead_id, author, note_type, content, created_at)
        VALUES (?, 'Sistema Automático', 'Email Enviado', ?, ?)
    ''', (lead_id, f"Email enviado: {tmpl['subject']}", now_str))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f"E-mail '{tmpl['subject']}' enviado com sucesso para {lead['email']}!",
        'body_preview': body
    })

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT leads.id, leads.name as Nome_Lead, leads.email as Email, leads.phone as Telefone,
               leads.company as Empresa, leads.team_size as Tamanho_Equipa, leads.interest_area as Area_Interesse,
               leads.lead_score as Lead_Score, leads.status as Estado, leads.source as Origem,
               leads.created_at as Data_Captura
        FROM leads
    ''')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if fmt == 'json':
        return jsonify(rows)
    elif fmt == 'csv':
        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_leads_capturados.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando LeadCraft AI — Lead Generator & Automation SaaS na porta 6942...")
    app.run(host='0.0.0.0', port=6942, debug=True)
