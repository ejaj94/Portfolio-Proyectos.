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

@app.route('/salespeople')
def salespeople():
    return render_template('salespeople.html', active_page='salespeople')

@app.route('/sales')
def sales():
    return render_template('sales.html', active_page='sales')

@app.route('/commissions')
def commissions():
    return render_template('commissions.html', active_page='commissions')

@app.route('/rankings')
def rankings():
    return render_template('rankings.html', active_page='rankings')

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

    cursor.execute('SELECT COUNT(*) FROM salespeople')
    total_salespeople = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*), SUM(amount), SUM(commission_amount), AVG(commission_rate) FROM sales')
    row = cursor.fetchone()
    total_sales_count = row[0] or 0
    total_sales_volume = round(row[1] or 0.0, 2)
    total_commissions_paid = round(row[2] or 0.0, 2)
    avg_commission_rate = round(row[3] or 0.0, 2)

    conn.close()

    return jsonify({
        'total_salespeople': total_salespeople,
        'total_sales_count': total_sales_count,
        'total_sales_volume': total_sales_volume,
        'total_commissions_paid': total_commissions_paid,
        'avg_commission_rate': avg_commission_rate
    })

@app.route('/api/salespeople', methods=['GET', 'POST'])
def handle_salespeople():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        role = data.get('role', 'Consultor Comercial').strip()
        tier_level = data.get('tier_level', 'Junior').strip()
        base_salary = float(data.get('base_salary', 1000.0))
        monthly_target = float(data.get('monthly_target', 10000.0))
        default_rate = float(data.get('default_commission_rate', 5.0))
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name or not email:
            return jsonify({'success': False, 'message': 'Nome e Email são obrigatórios!'}), 400

        try:
            cursor.execute('''
                INSERT INTO salespeople (name, email, phone, role, tier_level, base_salary, monthly_target, default_commission_rate, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, role, tier_level, base_salary, monthly_target, default_rate, now_str))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Vendedor registado com sucesso!'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'success': False, 'message': 'Email já registado no sistema!'}), 400

    cursor.execute('SELECT * FROM salespeople ORDER BY id DESC')
    sp_list = [dict(r) for r in cursor.fetchall()]

    # Attach stats for each salesperson
    for sp in sp_list:
        cursor.execute('SELECT SUM(amount), SUM(commission_amount) FROM sales WHERE salesperson_id = ?', (sp['id'],))
        s_row = cursor.fetchone()
        sp['total_sales_amount'] = round(s_row[0] or 0.0, 2)
        sp['total_commissions'] = round(s_row[1] or 0.0, 2)
        sp['target_progress_percent'] = round((sp['total_sales_amount'] / sp['monthly_target'] * 100.0) if sp['monthly_target'] > 0 else 0.0, 1)

    conn.close()
    return jsonify(sp_list)

@app.route('/api/sales', methods=['GET', 'POST'])
def handle_sales():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        salesperson_id = data.get('salesperson_id')
        client_name = data.get('client_name', '').strip()
        product_category = data.get('product_category', 'Geral').strip()
        amount = float(data.get('amount', 0.0))
        custom_rate = data.get('commission_rate')
        period_name = data.get('period_name', 'Setembro 2026').strip()
        sale_date = data.get('sale_date', datetime.datetime.now().strftime("%Y-%m-%d"))

        if not salesperson_id or not client_name or amount <= 0:
            return jsonify({'success': False, 'message': 'Selecione o vendedor, cliente e valor válido!'}), 400

        # Calculate rate based on rules if custom_rate not provided
        if custom_rate is not None and str(custom_rate).strip() != '':
            commission_rate = float(custom_rate)
        else:
            cursor.execute('SELECT commission_rate, bonus_amount FROM commission_rules WHERE min_amount <= ? AND max_amount >= ?', (amount, amount))
            rule = cursor.fetchone()
            if rule:
                commission_rate = float(rule['commission_rate'])
            else:
                cursor.execute('SELECT default_commission_rate FROM salespeople WHERE id = ?', (salesperson_id,))
                sp = cursor.fetchone()
                commission_rate = float(sp['default_commission_rate']) if sp else 5.0

        commission_amount = round(amount * (commission_rate / 100.0), 2)

        cursor.execute('''
            INSERT INTO sales (salesperson_id, client_name, product_category, amount, commission_rate, commission_amount, status, period_name, sale_date)
            VALUES (?, ?, ?, ?, ?, ?, 'Concluída', ?, ?)
        ''', (salesperson_id, client_name, product_category, amount, commission_rate, commission_amount, period_name, sale_date))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Venda registada e comissão calculada com sucesso!', 'commission_amount': commission_amount})

    cursor.execute('''
        SELECT sales.*, salespeople.name as salesperson_name, salespeople.tier_level
        FROM sales
        JOIN salespeople ON sales.salesperson_id = salespeople.id
        ORDER BY sales.id DESC
    ''')
    sales_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(sales_list)

@app.route('/api/rules', methods=['GET'])
def get_rules():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM commission_rules ORDER BY min_amount ASC')
    rules = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rules)

@app.route('/api/rankings', methods=['GET'])
def get_rankings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT salespeople.id, salespeople.name, salespeople.role, salespeople.tier_level, salespeople.monthly_target,
               COALESCE(SUM(sales.amount), 0.0) as total_sales_volume,
               COALESCE(SUM(sales.commission_amount), 0.0) as total_commissions,
               COUNT(sales.id) as total_deals
        FROM salespeople
        LEFT JOIN sales ON salespeople.id = sales.salesperson_id
        GROUP BY salespeople.id
        ORDER BY total_sales_volume DESC
    ''')
    rankings = [dict(r) for r in cursor.fetchall()]

    for rank, sp in enumerate(rankings, 1):
        sp['rank'] = rank
        sp['target_achievement'] = round((sp['total_sales_volume'] / sp['monthly_target'] * 100.0) if sp['monthly_target'] > 0 else 0.0, 1)

    conn.close()
    return jsonify(rankings)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT sales.id, sales.sale_date as Data_Venda, salespeople.name as Vendedor,
               salespeople.tier_level as Nivel, sales.client_name as Cliente,
               sales.product_category as Categoria, sales.amount as Valor_Venda_EUR,
               sales.commission_rate as Taxa_Comissao_Pct, sales.commission_amount as Valor_Comissao_EUR,
               sales.period_name as Periodo
        FROM sales
        JOIN salespeople ON sales.salesperson_id = salespeople.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_comissoes_vendas.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando ComisiCraft AI — Sistema de Comissões & Performance SaaS na porta 6941...")
    app.run(host='0.0.0.0', port=6941, debug=True)
