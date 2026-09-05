import os
import sqlite3

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'profitability.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Simulations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            product_cost REAL NOT NULL DEFAULT 0.0,
            labor_hours REAL NOT NULL DEFAULT 0.0,
            labor_rate REAL NOT NULL DEFAULT 0.0,
            overhead_cost REAL NOT NULL DEFAULT 0.0,
            monthly_fixed_costs REAL NOT NULL DEFAULT 0.0,
            vat_rate REAL NOT NULL DEFAULT 23.0,
            selling_price REAL NOT NULL DEFAULT 0.0,
            selling_price_with_vat REAL NOT NULL DEFAULT 0.0,
            total_cost REAL NOT NULL DEFAULT 0.0,
            gross_margin REAL NOT NULL DEFAULT 0.0,
            margin_percentage REAL NOT NULL DEFAULT 0.0,
            net_profit REAL NOT NULL DEFAULT 0.0,
            breakeven_units INTEGER NOT NULL DEFAULT 0,
            breakeven_revenue REAL NOT NULL DEFAULT 0.0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

    # Check if empty, seed demo simulations
    cursor.execute('SELECT COUNT(*) FROM simulations')
    if cursor.fetchone()[0] == 0:
        seed_data(cursor)

    conn.commit()
    conn.close()

def calculate_metrics(product_cost, labor_hours, labor_rate, overhead_cost, monthly_fixed_costs, vat_rate, selling_price):
    labor_total = labor_hours * labor_rate
    unit_variable_cost = product_cost + labor_total + overhead_cost
    selling_price_with_vat = selling_price * (1 + vat_rate / 100.0)
    gross_margin = selling_price - unit_variable_cost
    
    if selling_price > 0:
        margin_percentage = (gross_margin / selling_price) * 100.0
    else:
        margin_percentage = 0.0

    net_profit = gross_margin # per unit net before tax

    if gross_margin > 0:
        breakeven_units = int(monthly_fixed_costs / gross_margin) + (1 if (monthly_fixed_costs % gross_margin) > 0 else 0)
    else:
        breakeven_units = 0

    breakeven_revenue = breakeven_units * selling_price

    return {
        'total_cost': round(unit_variable_cost, 2),
        'selling_price_with_vat': round(selling_price_with_vat, 2),
        'gross_margin': round(gross_margin, 2),
        'margin_percentage': round(margin_percentage, 2),
        'net_profit': round(net_profit, 2),
        'breakeven_units': breakeven_units,
        'breakeven_revenue': round(breakeven_revenue, 2)
    }

def seed_data(cursor):
    demos = [
        ("T-Shirt E-Commerce Premium", "Produto Físico", 8.50, 0.2, 15.00, 3.50, 800.00, 23.0, 29.90, "Modelo de venda online com custo de anúncios social media por unidade."),
        ("Sprint Desenvolvedor Web SaaS", "Serviço Profissional", 50.00, 40.0, 35.00, 200.00, 2500.00, 23.0, 3500.00, "Projeto de desenvolvimento de módulo web com licenças de servidores inclusas."),
        ("Menu Hambúrguer Gourmet", "Restauração & Alimentos", 3.20, 0.25, 12.00, 1.20, 1800.00, 13.0, 12.50, "Custo de matérias-primas frescas, embalagem de entrega e tempo de cozinha."),
        ("Curso Digital de Marketing", "Produto Digital", 1.50, 0.1, 25.00, 8.00, 600.00, 23.0, 49.00, "Venda de curso gravado com tráfego pago por conversão.")
    ]

    for name, cat, p_cost, l_hrs, l_rate, ovh, fix_m, vat, s_price, notes in demos:
        metrics = calculate_metrics(p_cost, l_hrs, l_rate, ovh, fix_m, vat, s_price)
        cursor.execute('''
            INSERT INTO simulations (
                name, category, product_cost, labor_hours, labor_rate, overhead_cost,
                monthly_fixed_costs, vat_rate, selling_price, selling_price_with_vat,
                total_cost, gross_margin, margin_percentage, net_profit, breakeven_units,
                breakeven_revenue, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, cat, p_cost, l_hrs, l_rate, ovh, fix_m, vat, s_price,
            metrics['selling_price_with_vat'], metrics['total_cost'], metrics['gross_margin'],
            metrics['margin_percentage'], metrics['net_profit'], metrics['breakeven_units'],
            metrics['breakeven_revenue'], notes
        ))

if __name__ == '__main__':
    init_db()
    print("[OK] Base de dados profitability.db inicializada com sucesso para Proyecto 48!")
