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

@app.route('/campaigns')
def campaigns():
    return render_template('campaigns.html', active_page='campaigns')

@app.route('/donors')
def donors():
    return render_template('donors.html', active_page='donors')

@app.route('/donations')
def donations():
    return render_template('donations.html', active_page='donations')

@app.route('/history')
def history():
    return render_template('history.html', active_page='history')

@app.route('/stats')
def stats():
    return render_template('stats.html', active_page='stats')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html', active_page='showcase')

# --- API Endpoints ---
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM campaigns')
    total_campaigns = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM campaigns WHERE status = "Ativa"')
    active_campaigns = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(raised_amount) FROM campaigns')
    total_raised = cursor.fetchone()[0] or 0.0

    cursor.execute('SELECT COUNT(*) FROM donations')
    total_donations = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM donors')
    total_donors = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_raised': round(total_raised, 2),
        'total_donations': total_donations,
        'total_donors': total_donors
    })

@app.route('/api/campaigns', methods=['GET', 'POST'])
def handle_campaigns():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        title = data.get('title', '').strip()
        cause_category = data.get('cause_category', 'Apoio Social').strip()
        goal_amount = float(data.get('goal_amount', 0))
        description = data.get('description', '').strip()
        end_date = data.get('end_date', '').strip()
        image_url = data.get('image_url', '').strip() or 'https://images.unsplash.com/photo-1532629345422-7515f3d16bb0?w=600'

        if not title or goal_amount <= 0:
            return jsonify({'success': False, 'message': 'Preencha o título da campanha e uma meta válida!'}), 400

        cursor.execute('''
            INSERT INTO campaigns (title, cause_category, goal_amount, raised_amount, description, end_date, status, image_url)
            VALUES (?, ?, ?, 0.0, ?, ?, 'Ativa', ?)
        ''', (title, cause_category, goal_amount, description, end_date, image_url))
        conn.commit()

        new_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'message': 'Campanha solidária criada com sucesso!', 'id': new_id})

    cursor.execute('SELECT * FROM campaigns ORDER BY id DESC')
    campaigns = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # Calculate progress %
    for c in campaigns:
        c['progress_pct'] = min(round((c['raised_amount'] / c['goal_amount']) * 100, 1) if c['goal_amount'] > 0 else 0, 100)

    return jsonify(campaigns)

@app.route('/api/donors', methods=['GET'])
def get_donors():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM donors ORDER BY id DESC')
    donors = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(donors)

@app.route('/api/donations', methods=['GET', 'POST'])
def handle_donations():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        campaign_id = data.get('campaign_id')
        donor_name = data.get('donor_name', '').strip()
        donor_email = data.get('donor_email', '').strip()
        amount = float(data.get('amount', 0))
        payment_method = data.get('payment_method', 'MBWay').strip()
        note = data.get('note', '').strip()

        if not campaign_id or not donor_name or amount <= 0:
            return jsonify({'success': False, 'message': 'Dados de doação inválidos!'}), 400

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Insert donation
        cursor.execute('''
            INSERT INTO donations (campaign_id, donor_name, donor_email, amount, payment_method, note, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (campaign_id, donor_name, donor_email, amount, payment_method, note, now_str))

        # Update campaign raised amount
        cursor.execute('UPDATE campaigns SET raised_amount = raised_amount + ? WHERE id = ?', (amount, campaign_id))

        # Check if campaign reached goal
        cursor.execute('SELECT raised_amount, goal_amount FROM campaigns WHERE id = ?', (campaign_id,))
        c = cursor.fetchone()
        if c and c['raised_amount'] >= c['goal_amount']:
            cursor.execute('UPDATE campaigns SET status = "Concluída" WHERE id = ?', (campaign_id,))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Doação efetuada e registada com sucesso!'})

    cursor.execute('''
        SELECT donations.*, campaigns.title as campaign_title
        FROM donations
        JOIN campaigns ON donations.campaign_id = campaigns.id
        ORDER BY donations.id DESC
    ''')
    donations = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(donations)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT donations.id, donations.donor_name, donations.donor_email, donations.amount as Valor_EUR,
               donations.payment_method as Metodo_Pagamento, campaigns.title as Campanha, donations.created_at as Data
        SELECT_DONATIONS:
        FROM donations
        JOIN campaigns ON donations.campaign_id = campaigns.id
    '''.replace('SELECT_DONATIONS:\n        ', ''))
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_donacraft.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando DonaCraft AI SaaS no servidor local porta 6938...")
    app.run(host='0.0.0.0', port=6938, debug=True)
