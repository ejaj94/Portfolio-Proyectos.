import os
import sqlite3
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'restaurant.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_order_code():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM orders')
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"CMD-2026-{100 + count}"

def generate_invoice_code():
    return f"FT-2026-{random.randint(900, 999)}"

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Total Tables & Occupancy
    cursor.execute("SELECT COUNT(*) FROM tables")
    total_tables = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tables WHERE status = 'Ocupada'")
    occupied_tables = cursor.fetchone()[0]
    
    # 2. Daily Revenue
    cursor.execute("SELECT SUM(total_amount) FROM invoices")
    rev_row = cursor.fetchone()[0]
    daily_revenue = rev_row if rev_row else 0.0
    
    # 3. Kitchen Pending Orders
    cursor.execute("SELECT COUNT(*) FROM order_items WHERE kitchen_status = 'A Cozinhar'")
    kitchen_pending_count = cursor.fetchone()[0]
    
    # 4. Today's Reservations
    cursor.execute("SELECT COUNT(*) FROM reservations WHERE status = 'Confirmada'")
    reservations_count = cursor.fetchone()[0]
    
    # 5. Tables list for floor plan map
    cursor.execute("SELECT * FROM tables ORDER BY table_number ASC")
    tables = cursor.fetchall()
    
    # 6. Active Kitchen Items Stream
    cursor.execute("""
        SELECT oi.*, o.order_code, o.table_number, o.waiter_name 
        FROM order_items oi 
        JOIN orders o ON oi.order_id = o.id 
        WHERE oi.kitchen_status != 'Entregue' 
        ORDER BY oi.id ASC
    """)
    kitchen_items = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html',
                           total_tables=total_tables,
                           occupied_tables=occupied_tables,
                           daily_revenue=daily_revenue,
                           kitchen_pending_count=kitchen_pending_count,
                           reservations_count=reservations_count,
                           tables=tables,
                           kitchen_items=kitchen_items)

@app.route('/tables')
def tables_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tables ORDER BY table_number ASC")
    tables = cursor.fetchall()
    
    cursor.execute("SELECT * FROM waiters WHERE status = 'Em Serviço'")
    waiters = cursor.fetchall()
    
    conn.close()
    return render_template('tables.html', tables=tables, waiters=waiters)

@app.route('/reservations')
def reservations_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, t.table_number, t.location 
        FROM reservations r 
        JOIN tables t ON r.table_id = t.id 
        ORDER BY r.id DESC
    """)
    reservations = cursor.fetchall()
    
    cursor.execute("SELECT * FROM tables")
    tables = cursor.fetchall()
    
    conn.close()
    return render_template('reservations.html', reservations=reservations, tables=tables)

@app.route('/orders')
def orders_page():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    
    cursor.execute("SELECT * FROM tables")
    tables = cursor.fetchall()
    
    cursor.execute("SELECT * FROM waiters WHERE status = 'Em Serviço'")
    waiters = cursor.fetchall()
    
    cursor.execute("SELECT * FROM menu_items WHERE is_available = 1 ORDER BY category ASC")
    menu_items = cursor.fetchall()
    
    conn.close()
    return render_template('orders.html', orders=orders, tables=tables, waiters=waiters, menu_items=menu_items)

@app.route('/menu')
def menu_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items ORDER BY category ASC, price ASC")
    menu_items = cursor.fetchall()
    conn.close()
    return render_template('menu.html', menu_items=menu_items)

@app.route('/kitchen')
def kitchen_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT oi.*, o.order_code, o.table_number, o.waiter_name 
        FROM order_items oi 
        JOIN orders o ON oi.order_id = o.id 
        WHERE oi.kitchen_status != 'Entregue' 
        ORDER BY oi.id ASC
    """)
    items = cursor.fetchall()
    conn.close()
    return render_template('kitchen.html', items=items)

@app.route('/waiters')
def waiters_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM waiters ORDER BY id ASC")
    waiters = cursor.fetchall()
    conn.close()
    return render_template('waiters.html', waiters=waiters)

@app.route('/billing')
def billing_page():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM invoices ORDER BY id DESC")
    invoices = cursor.fetchall()
    
    cursor.execute("SELECT * FROM orders WHERE status = 'Em Preparação' OR status = 'Servido'")
    open_orders = cursor.fetchall()
    
    conn.close()
    return render_template('billing.html', invoices=invoices, open_orders=open_orders)

# REST API ENDPOINTS

@app.route('/api/tables/status', methods=['POST'])
def api_update_table_status():
    try:
        data = request.get_json()
        table_id = data.get('table_id')
        status = data.get('status')
        waiter = data.get('waiter_name')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE tables SET status = ?, waiter_name = COALESCE(?, waiter_name) WHERE id = ?", (status, waiter, table_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Estado da mesa atualizado!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/orders/create', methods=['POST'])
def api_create_order():
    try:
        data = request.get_json()
        order_code = generate_order_code()
        table_number = int(data.get('table_number'))
        waiter_name = data.get('waiter_name')
        items = data.get('items', [])
        
        subtotal = 0.0
        for item in items:
            qty = int(item.get('quantity', 1))
            price = float(item.get('unit_price', 0.0))
            subtotal += qty * price
            
        tax_amount = subtotal * 0.23
        total_amount = subtotal + tax_amount
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO orders (order_code, table_number, waiter_name, status, subtotal, tax_amount, total_amount)
            VALUES (?, ?, ?, 'Em Preparação', ?, ?, ?)
        """, (order_code, table_number, waiter_name, subtotal, tax_amount, total_amount))
        
        order_id = cursor.lastrowid
        
        for item in items:
            name = item.get('item_name')
            qty = int(item.get('quantity', 1))
            price = float(item.get('unit_price', 0.0))
            line_total = qty * price
            cursor.execute("""
                INSERT INTO order_items (order_id, item_name, quantity, unit_price, total_price, kitchen_status)
                VALUES (?, ?, ?, ?, ?, 'A Cozinhar')
            """, (order_id, name, qty, price, line_total))
            
        # Update Table Status to Ocupada
        cursor.execute("UPDATE tables SET status = 'Ocupada', waiter_name = ? WHERE table_number = ?", (waiter_name, table_number))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'order_code': order_code, 'message': 'Comanda enviada para a cozinha!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/kitchen/status', methods=['POST'])
def api_update_kitchen_status():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        kitchen_status = data.get('kitchen_status')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE order_items SET kitchen_status = ? WHERE id = ?", (kitchen_status, item_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Estado do prato atualizado!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/reservations/create', methods=['POST'])
def api_create_reservation():
    try:
        data = request.get_json()
        guest_name = data.get('guest_name', '').strip()
        guest_phone = data.get('guest_phone', '').strip()
        party_size = int(data.get('party_size', 2))
        res_time = data.get('reservation_time', '20:00')
        table_id = int(data.get('table_id', 1))
        notes = data.get('special_requests', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservations (guest_name, guest_phone, party_size, reservation_time, table_id, status, special_requests)
            VALUES (?, ?, ?, ?, ?, 'Confirmada', ?)
        """, (guest_name, guest_phone, party_size, res_time, table_id, notes))
        
        # Mark table as Reservada
        cursor.execute("UPDATE tables SET status = 'Reservada' WHERE id = ?", (table_id,))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Mesa reservada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/invoices/create', methods=['POST'])
def api_create_invoice():
    try:
        data = request.get_json()
        order_id = int(data.get('order_id'))
        payment_method = data.get('payment_method', 'MBWay')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        
        if not order:
            conn.close()
            return jsonify({'success': False, 'message': 'Comanda não encontrada'}), 404
            
        inv_code = generate_invoice_code()
        
        cursor.execute("""
            INSERT INTO invoices (invoice_code, order_id, table_number, subtotal, tax_rate, total_amount, payment_method)
            VALUES (?, ?, ?, ?, 23.0, ?, ?)
        """, (inv_code, order_id, order['table_number'], order['subtotal'], order['total_amount'], payment_method))
        
        # Update order status & free table
        cursor.execute("UPDATE orders SET status = 'Fechado' WHERE id = ?", (order_id,))
        cursor.execute("UPDATE tables SET status = 'Livre' WHERE table_number = ?", (order['table_number'],))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'invoice_code': inv_code, 'message': 'Fatura emitida e conta liquidadas!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - Gourmet POS & Sistema de Gestão de Restaurantes SaaS na porta 6907...")
    app.run(host='0.0.0.0', port=6907, debug=True)
