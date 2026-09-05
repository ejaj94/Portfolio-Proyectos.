import os
import sqlite3
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import DB_PATH, init_db, calculate_metrics

app = Flask(__name__)
app.secret_key = 'ejajtech_profitability_saas_secret_key'

# Custom Filters
@app.template_filter('currency')
def currency_filter(value):
    if value is None:
        return "€ 0,00"
    try:
        val = float(value)
        return f"€ {val:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
    except Exception:
        return f"€ {value}"

@app.template_filter('percent')
def percent_filter(value):
    if value is None:
        return "0,0%"
    try:
        val = float(value)
        return f"{val:,.1f}%".replace('.', ',')
    except Exception:
        return f"{value}%"

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Ensure DB exists
if not os.path.exists(DB_PATH):
    init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    simulations = [dict(r) for r in conn.execute('SELECT * FROM simulations ORDER BY created_at DESC').fetchall()]
    conn.close()
    return render_template('index.html', simulations=simulations)

@app.route('/simulations')
def simulations_page():
    conn = get_db_connection()
    simulations = [dict(r) for r in conn.execute('SELECT * FROM simulations ORDER BY created_at DESC').fetchall()]
    conn.close()
    return render_template('simulations.html', simulations=simulations)

@app.route('/report/<int:sim_id>')
def report_page(sim_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM simulations WHERE id = ?', (sim_id,)).fetchone()
    conn.close()
    if not row:
        return "Simulação não encontrada", 404
        
    sim = dict(row)
    # Generate break even chart data points
    be_units = sim['breakeven_units']
    max_units = max(be_units * 2, 50)
    step = max(1, max_units // 10)
    
    chart_points = []
    for u in range(0, max_units + step, step):
        total_costs = sim['monthly_fixed_costs'] + (sim['total_cost'] * u)
        total_revenue = sim['selling_price'] * u
        chart_points.append({
            'units': u,
            'costs': round(total_costs, 2),
            'revenue': round(total_revenue, 2),
            'profit': round(total_revenue - total_costs, 2)
        })
        
    return render_template('report.html', sim=sim, chart_points=chart_points)

# API ENDPOINTS
@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.json or {}
    product_cost = float(data.get('product_cost', 0))
    labor_hours = float(data.get('labor_hours', 0))
    labor_rate = float(data.get('labor_rate', 0))
    overhead_cost = float(data.get('overhead_cost', 0))
    monthly_fixed_costs = float(data.get('monthly_fixed_costs', 0))
    vat_rate = float(data.get('vat_rate', 23))
    selling_price = float(data.get('selling_price', 0))
    
    metrics = calculate_metrics(
        product_cost, labor_hours, labor_rate, overhead_cost,
        monthly_fixed_costs, vat_rate, selling_price
    )
    
    # Calculate Break-Even Chart Curve Data
    be_units = metrics['breakeven_units']
    max_units = max(be_units * 2, 50)
    step = max(1, max_units // 10)
    
    curve_data = []
    for u in range(0, max_units + step, step):
        total_c = monthly_fixed_costs + (metrics['total_cost'] * u)
        total_r = selling_price * u
        curve_data.append({
            'units': u,
            'fixed_cost': monthly_fixed_costs,
            'total_cost': round(total_c, 2),
            'revenue': round(total_r, 2),
            'profit': round(total_r - total_c, 2)
        })
        
    metrics['curve_data'] = curve_data
    return jsonify({'success': True, 'data': metrics})

@app.route('/api/simulations/save', methods=['POST'])
def api_simulation_save():
    data = request.json or {}
    name = data.get('name', '').strip()
    category = data.get('category', 'Geral').strip()
    notes = data.get('notes', '').strip()
    
    product_cost = float(data.get('product_cost', 0))
    labor_hours = float(data.get('labor_hours', 0))
    labor_rate = float(data.get('labor_rate', 0))
    overhead_cost = float(data.get('overhead_cost', 0))
    monthly_fixed_costs = float(data.get('monthly_fixed_costs', 0))
    vat_rate = float(data.get('vat_rate', 23))
    selling_price = float(data.get('selling_price', 0))
    
    if not name:
        return jsonify({'success': False, 'message': 'Nome da simulação é obrigatório.'}), 400
        
    metrics = calculate_metrics(
        product_cost, labor_hours, labor_rate, overhead_cost,
        monthly_fixed_costs, vat_rate, selling_price
    )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO simulations (
            name, category, product_cost, labor_hours, labor_rate, overhead_cost,
            monthly_fixed_costs, vat_rate, selling_price, selling_price_with_vat,
            total_cost, gross_margin, margin_percentage, net_profit, breakeven_units,
            breakeven_revenue, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name, category, product_cost, labor_hours, labor_rate, overhead_cost,
        monthly_fixed_costs, vat_rate, selling_price,
        metrics['selling_price_with_vat'], metrics['total_cost'], metrics['gross_margin'],
        metrics['margin_percentage'], metrics['net_profit'], metrics['breakeven_units'],
        metrics['breakeven_revenue'], notes
    ))
    
    sim_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'sim_id': sim_id,
        'message': f'Simulação "{name}" guardada com sucesso com ponto de equilíbrio em {metrics["breakeven_units"]} unidades/mês!'
    })

@app.route('/api/simulations/delete/<int:sim_id>', methods=['DELETE', 'POST'])
def api_simulation_delete(sim_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM simulations WHERE id = ?', (sim_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Simulação eliminada com sucesso.'})

if __name__ == '__main__':
    print("[SERVER] Calculadora de Rentabilidade SaaS a iniciar na porta 6901...")
    app.run(host='0.0.0.0', port=6901, debug=False)
