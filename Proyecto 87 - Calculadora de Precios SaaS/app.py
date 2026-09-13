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

@app.route('/calculator')
def calculator():
    return render_template('calculator.html', active_page='calculator')

@app.route('/products')
def products():
    return render_template('products.html', active_page='products')

@app.route('/history')
def history():
    return render_template('history.html', active_page='history')

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

    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM calculations')
    total_simulations = cursor.fetchone()[0]

    cursor.execute('SELECT AVG(margin_percent), SUM(final_price), SUM(net_profit) FROM calculations')
    row = cursor.fetchone()
    avg_margin = round(row[0] or 0.0, 2)
    total_revenue = round(row[1] or 0.0, 2)
    total_profit = round(row[2] or 0.0, 2)

    conn.close()

    return jsonify({
        'total_products': total_products,
        'total_simulations': total_simulations,
        'avg_margin': avg_margin,
        'total_revenue': total_revenue,
        'total_profit': total_profit
    })

@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        category = data.get('category', 'Geral').strip()
        unit = data.get('unit', 'Unidade').strip()
        base_cost = float(data.get('base_cost', 0.0))
        labor_cost = float(data.get('labor_cost', 0.0))
        overhead_cost = float(data.get('overhead_cost', 0.0))
        target_margin = float(data.get('target_margin_percent', 30.0))
        total_cost = base_cost + labor_cost + overhead_cost
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if not name:
            return jsonify({'success': False, 'message': 'Preencha o nome do produto/serviço!'}), 400

        cursor.execute('''
            INSERT INTO products (name, category, unit, base_cost, labor_cost, overhead_cost, total_cost, target_margin_percent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, unit, base_cost, labor_cost, overhead_cost, total_cost, target_margin, now_str))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Produto/Serviço registado com sucesso!'})

    cursor.execute('SELECT * FROM products ORDER BY id DESC')
    products_list = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(products_list)

@app.route('/api/calculations', methods=['GET', 'POST'])
def handle_calculations():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json() or {}
        product_id = data.get('product_id')
        title = data.get('title', '').strip()
        base_cost = float(data.get('base_cost', 0.0))
        labor_cost = float(data.get('labor_cost', 0.0))
        overhead_cost = float(data.get('overhead_cost', 0.0))
        total_cost = base_cost + labor_cost + overhead_cost

        margin_percent = float(data.get('margin_percent', 30.0))
        discount_percent = float(data.get('discount_percent', 0.0))
        vat_rate = float(data.get('vat_rate', 23.0))

        if total_cost < 0:
            return jsonify({'success': False, 'message': 'Custo total deve ser maior ou igual a zero!'}), 400

        # Calculations
        # Margin % formula: Price_before_discount = Total_Cost / (1 - Margin/100)
        if margin_percent >= 100:
            margin_percent = 99.9

        raw_price = total_cost / (1 - (margin_percent / 100.0)) if margin_percent < 100 else total_cost * 2
        gross_profit = raw_price - total_cost
        markup_percent = (gross_profit / total_cost * 100.0) if total_cost > 0 else 0.0

        # Apply Discount
        price_before_tax = raw_price * (1 - (discount_percent / 100.0))

        # VAT calculation
        vat_amount = price_before_tax * (vat_rate / 100.0)
        final_price = price_before_tax + vat_amount
        net_profit = price_before_tax - total_cost

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        cursor.execute('''
            INSERT INTO calculations (product_id, title, base_cost, labor_cost, overhead_cost, total_cost, markup_percent, gross_profit, margin_percent, discount_percent, price_before_tax, vat_rate, vat_amount, final_price, net_profit, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product_id, title or 'Cálculo de Preço', base_cost, labor_cost, overhead_cost, total_cost, round(markup_percent, 2), round(gross_profit, 2), round(margin_percent, 2), round(discount_percent, 2), round(price_before_tax, 2), round(vat_rate, 2), round(vat_amount, 2), round(final_price, 2), round(net_profit, 2), now_str))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Cálculo de preço efetuado e guardado com sucesso!',
            'data': {
                'total_cost': round(total_cost, 2),
                'markup_percent': round(markup_percent, 2),
                'gross_profit': round(gross_profit, 2),
                'price_before_tax': round(price_before_tax, 2),
                'vat_amount': round(vat_amount, 2),
                'final_price': round(final_price, 2),
                'net_profit': round(net_profit, 2)
            }
        })

    cursor.execute('''
        SELECT calculations.*, products.name as product_name, products.category as product_category
        FROM calculations
        LEFT JOIN products ON calculations.product_id = products.id
        ORDER BY calculations.id DESC
    ''')
    calcs = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(calcs)

@app.route('/api/export/<fmt>', methods=['GET'])
def export_data(fmt):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT calculations.id, calculations.title as Titulo_Simulacao, products.name as Produto,
               calculations.total_cost as Custo_Total_EUR, calculations.margin_percent as Margem_Pct,
               calculations.discount_percent as Desconto_Pct, calculations.price_before_tax as Preco_Sem_IVA_EUR,
               calculations.vat_rate as Taxa_IVA_Pct, calculations.vat_amount as Valor_IVA_EUR,
               calculations.final_price as Preco_Final_Com_IVA_EUR, calculations.net_profit as Lucro_Liquido_EUR,
               calculations.created_at as Data_Calculo
        FROM calculations
        LEFT JOIN products ON calculations.product_id = products.id
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
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=export_calculadora_precos.csv'})
    return jsonify({'error': 'Formato inválido'}), 400

if __name__ == '__main__':
    print("Iniciando PriceCraft AI — Calculadora de Preços & Margens SaaS na porta 6940...")
    app.run(host='0.0.0.0', port=6940, debug=True)
