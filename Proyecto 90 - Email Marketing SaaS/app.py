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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', active_page='contacts')

@app.route('/lists')
def lists():
    return render_template('lists.html', active_page='lists')

@app.route('/campaigns')
def campaigns():
    return render_template('campaigns.html', active_page='campaigns')

@app.route('/templates_page')
def templates_page():
    return render_template('templates_page.html', active_page='templates_page')

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

    cursor.execute('SELECT COUNT(*) FROM contacts WHERE status = "Ativo"')
    total_contacts = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM lists')
    total_lists = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM campaigns WHERE status IN ("Enviada", "Programada")')
    active_campaigns = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(recipients_count), SUM(opens_count), SUM(clicks_count) FROM campaigns WHERE status = "Enviada"')
    row = cursor.fetchone()
    tot_recipients = row[0] or 0
    tot_opens = row[1] or 0
    tot_clicks = row[2] or 0

    avg_open_rate = round((tot_opens / tot_recipients * 100.0) if tot_recipients > 0 else 0.0, 1)
    avg_click_rate = round((tot_clicks / tot_recipients * 100.0) if tot_recipients > 0 else 0.0, 1)

    conn.close()

    return jsonify({
        'total_contacts': total_contacts,
        'total_lists': total_lists,
        'active_campaigns': active_campaigns,
        'avg_open_rate': avg_open_rate,
        'avg_click_rate': avg_click_rate
    })

@app.route('/api/contacts', methods=['GET', 'POST'])
def handle_contacts():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        company = data.get('company', '').strip()
        tags = data.get('tags', 'Subscritor').strip()
        list_ids = data.get('list_ids', [])
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name or not email:
            return jsonify({'success': False, 'message': 'Nome e Email são obrigatórios!'}), 400

        try:
            cursor.execute('''
                INSERT INTO contacts (name, email, company, status, tags, subscribed_at)
                VALUES (?, ?, ?, 'Ativo', ?, ?)
            ''', (name, email, company, tags, now_str))
            contact_id = cursor.lastrowid

            # Associate with lists
            for lid in list_ids:
                cursor.execute('INSERT OR IGNORE INTO contact_list_rel (contact_id, list_id) VALUES (?, ?)', (contact_id, int(lid)))
                cursor.execute('UPDATE lists SET member_count = (SELECT COUNT(*) FROM contact_list_rel WHERE list_id = ?) WHERE id = ?', (int(lid), int(lid)))

            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Contacto registado com sucesso!'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Email já registado no sistema!'}), 400

    cursor.execute('SELECT * FROM contacts ORDER BY id DESC')
    contacts_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(contacts_list)

@app.route('/api/lists', methods=['GET', 'POST'])
def handle_lists():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name:
            return jsonify({'success': False, 'message': 'Nome da lista é obrigatório!'}), 400

        cursor.execute('''
            INSERT INTO lists (name, description, member_count, created_at)
            VALUES (?, ?, 0, ?)
        ''', (name, description, now_str))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Lista de distribuição criada com sucesso!'})

    cursor.execute('SELECT * FROM lists ORDER BY id DESC')
    lists_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(lists_list)

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        category = data.get('category', 'Geral').strip()
        subject_default = data.get('subject_default', '').strip()
        content_html = data.get('content_html', '').strip()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not title or not content_html:
            return jsonify({'success': False, 'message': 'Título e conteúdo são obrigatórios!'}), 400

        cursor.execute('''
            INSERT INTO templates (title, category, subject_default, content_html, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, subject_default, content_html, now_str))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Modelo de e-mail criado com sucesso!'})

    cursor.execute('SELECT * FROM templates ORDER BY id DESC')
    templates_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(templates_list)

@app.route('/api/campaigns', methods=['GET', 'POST'])
def handle_campaigns():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        subject = data.get('subject', '').strip()
        list_id = data.get('list_id')
        template_id = data.get('template_id')
        scheduled_at = data.get('scheduled_at')
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name or not subject or not list_id:
            return jsonify({'success': False, 'message': 'Preencha o nome, assunto e lista alvo!'}), 400

        # Get recipient count
        cursor.execute('SELECT member_count FROM lists WHERE id = ?', (list_id,))
        l_row = cursor.fetchone()
        recipients_count = l_row['member_count'] if l_row else 0

        status = 'Programada' if scheduled_at else 'Rascunho'

        cursor.execute('''
            INSERT INTO campaigns (name, subject, list_id, template_id, status, scheduled_at, recipients_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, subject, list_id, template_id, status, scheduled_at or None, recipients_count, now_str))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Campanha criada e configurada com sucesso!'})

    cursor.execute('''
        SELECT campaigns.*, lists.name as list_name, templates.title as template_title
        FROM campaigns
        LEFT JOIN lists ON campaigns.list_id = lists.id
        LEFT JOIN templates ON campaigns.template_id = templates.id
        ORDER BY campaigns.id DESC
    ''')
    campaigns_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(campaigns_list)

@app.route('/api/campaigns/<int:campaign_id>/send', methods=['POST'])
def trigger_campaign_send(campaign_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
    camp = cursor.fetchone()

    if not camp:
        conn.close()
        return jsonify({'success': False, 'message': 'Campanha não encontrada!'}), 404

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    recipients = max(camp['recipients_count'], 5)
    opens = int(recipients * 0.75) # 75% simulated open rate
    clicks = int(recipients * 0.45) # 45% simulated click rate

    cursor.execute('''
        UPDATE campaigns
        SET status = 'Enviada', sent_at = ?, recipients_count = ?, opens_count = ?, clicks_count = ?
        WHERE id = ?
    ''', (now_str, recipients, opens, clicks, campaign_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f"Campanha '{camp['name']}' disparada com sucesso para {recipients} contactos!",
        'stats': {'recipients': recipients, 'opens': opens, 'clicks': clicks}
    })

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT campaigns.id, campaigns.name as Nome_Campanha, campaigns.subject as Assunto,
               lists.name as Lista_Alvo, campaigns.status as Estado, campaigns.recipients_count as Destinatarios,
               campaigns.opens_count as Aberturas, campaigns.clicks_count as Cliques,
               campaigns.sent_at as Data_Envio, campaigns.created_at as Data_Criacao
        FROM campaigns
        LEFT JOIN lists ON campaigns.list_id = lists.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_email_marketing.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando MailCraft AI — Email Marketing & Automation SaaS na porta 6943...")
    app.run(host='0.0.0.0', port=6943, debug=True)
