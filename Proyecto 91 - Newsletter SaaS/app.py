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

@app.route('/subscribers')
def subscribers():
    return render_template('subscribers.html', active_page='subscribers')

@app.route('/issues')
def issues():
    return render_template('issues.html', active_page='issues')

@app.route('/editor')
def editor():
    return render_template('editor.html', active_page='editor')

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

    cursor.execute('SELECT COUNT(*) FROM subscribers WHERE status = "Ativo"')
    total_subscribers = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM subscribers WHERE tier = "VIP"')
    vip_subscribers = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM issues')
    total_issues = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM issues WHERE status = "Publicado"')
    published_issues = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(recipients_count), SUM(opens_count), SUM(clicks_count) FROM issues WHERE status = "Publicado"')
    row = cursor.fetchone()
    tot_rec = row[0] or 0
    tot_op = row[1] or 0
    tot_cl = row[2] or 0

    avg_open_rate = round((tot_op / tot_rec * 100.0) if tot_rec > 0 else 0.0, 1)
    avg_click_rate = round((tot_cl / tot_rec * 100.0) if tot_rec > 0 else 0.0, 1)

    conn.close()

    return jsonify({
        'total_subscribers': total_subscribers,
        'vip_subscribers': vip_subscribers,
        'total_issues': total_issues,
        'published_issues': published_issues,
        'avg_open_rate': avg_open_rate,
        'avg_click_rate': avg_click_rate
    })

@app.route('/api/subscribers', methods=['GET', 'POST'])
def handle_subscribers():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        tier = data.get('tier', 'Gratuito').strip()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name or not email:
            return jsonify({'success': False, 'message': 'Nome e E-mail são obrigatórios!'}), 400

        try:
            cursor.execute('''
                INSERT INTO subscribers (name, email, tier, status, open_rate, subscribed_at)
                VALUES (?, ?, ?, 'Ativo', 100.0, ?)
            ''', (name, email, tier, now_str))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Subscritor registado com sucesso!'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Este endereço de e-mail já está inscrito!'}), 400

    cursor.execute('SELECT * FROM subscribers ORDER BY id DESC')
    subs = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(subs)

@app.route('/api/issues', methods=['GET', 'POST'])
def handle_issues():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        subject = data.get('subject', '').strip()
        preview_text = data.get('preview_text', '').strip()
        template_id = data.get('template_id')
        content_html = data.get('content_html', '').strip()
        action = data.get('action', 'save') # 'save', 'schedule', 'publish'
        scheduled_at = data.get('scheduled_at')
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not title or not subject or not content_html:
            return jsonify({'success': False, 'message': 'Título, Assunto e Conteúdo são obrigatórios!'}), 400

        cursor.execute('SELECT MAX(issue_number) FROM issues')
        max_num = cursor.fetchone()[0] or 100
        issue_number = max_num + 1

        cursor.execute('SELECT COUNT(*) FROM subscribers WHERE status = "Ativo"')
        recipients_count = cursor.fetchone()[0]

        status = 'Rascunho'
        pub_at = None
        opens = 0
        clicks = 0

        if action == 'publish':
            status = 'Publicado'
            pub_at = now_str
            opens = int(recipients_count * 0.82) # 82% simulated open rate
            clicks = int(recipients_count * 0.48) # 48% simulated click rate
        elif action == 'schedule':
            status = 'Programado'

        cursor.execute('''
            INSERT INTO issues (issue_number, title, subject, preview_text, template_id, content_html, status, scheduled_at, published_at, recipients_count, opens_count, clicks_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (issue_number, title, subject, preview_text, template_id or None, content_html, status, scheduled_at or None, pub_at, recipients_count, opens, clicks, now_str))

        conn.commit()
        conn.close()

        msg = f"Edição #{issue_number} publicada com sucesso!" if status == 'Publicado' else (f"Edição #{issue_number} agendada!" if status == 'Programado' else f"Rascunho da Edição #{issue_number} guardado.")
        return jsonify({'success': True, 'message': msg})

    cursor.execute('''
        SELECT issues.*, templates.title as template_title
        FROM issues
        LEFT JOIN templates ON issues.template_id = templates.id
        ORDER BY issues.id DESC
    ''')
    issues_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(issues_list)

@app.route('/api/issues/<int:issue_id>/publish', methods=['POST'])
def publish_issue(issue_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM issues WHERE id = ?', (issue_id,))
    issue = cursor.fetchone()

    if not issue:
        conn.close()
        return jsonify({'success': False, 'message': 'Edição não encontrada!'}), 404

    cursor.execute('SELECT COUNT(*) FROM subscribers WHERE status = "Ativo"')
    recipients = cursor.fetchone()[0] or 10
    opens = int(recipients * 0.85)
    clicks = int(recipients * 0.52)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute('''
        UPDATE issues
        SET status = 'Publicado', published_at = ?, recipients_count = ?, opens_count = ?, clicks_count = ?
        WHERE id = ?
    ''', (now_str, recipients, opens, clicks, issue_id))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f"Edição #{issue['issue_number']} publicada para {recipients} subscritores!"
    })

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        category = data.get('category', 'Geral').strip()
        header_subtitle = data.get('header_subtitle', '').strip()
        content_html = data.get('content_html', '').strip()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not title or not content_html:
            return jsonify({'success': False, 'message': 'Título e conteúdo são obrigatórios!'}), 400

        cursor.execute('''
            INSERT INTO templates (title, category, header_subtitle, content_html, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, header_subtitle, content_html, now_str))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Modelo de newsletter guardado com sucesso!'})

    cursor.execute('SELECT * FROM templates ORDER BY id DESC')
    tmps = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(tmps)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT issues.issue_number as Edicao, issues.title as Titulo, issues.subject as Assunto,
               issues.status as Estado, issues.recipients_count as Leitores,
               issues.opens_count as Aberturas, issues.clicks_count as Cliques,
               issues.published_at as Data_Publicacao
        FROM issues
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_newsletter_editions.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando Publishing SaaS - Newsletter Platform na porta 6944...")
    app.run(host='0.0.0.0', port=6944, debug=True)
