import os
import sqlite3
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import DB_PATH, init_db

app = Flask(__name__)
app.secret_key = 'olx_marketplace_saas_ejajtech_key'

# Custom Filters
@app.template_filter('currency')
def currency_filter(value):
    try:
        val = float(value)
        return f"€ {val:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')
    except Exception:
        return f"€ {value}"

@app.template_filter('escapejs')
def escapejs_filter(val):
    if not val:
        return ""
    return json.dumps(str(val))[1:-1]

# Ensure DB exists
if not os.path.exists(DB_PATH):
    init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Mock logged in buyer ID = 5 (Cliente Comprador Demo)
DEFAULT_BUYER_ID = 5
# Mock logged in seller ID = 1 (Enmanuel Jimenez EJAJ TECH)
DEFAULT_SELLER_ID = 1

@app.route('/')
def index():
    query_str = request.args.get('q', '').strip()
    category_filter = request.args.get('category', '').strip()
    
    conn = get_db_connection()
    sql = '''
        SELECT p.*, u.name as seller_name, u.rating as seller_rating
        FROM products p
        JOIN users u ON p.seller_id = u.id
        WHERE 1=1
    '''
    params = []
    
    if query_str:
        sql += ' AND (p.title LIKE ? OR p.description LIKE ?)'
        params.extend([f'%{query_str}%', f'%{query_str}%'])
    if category_filter:
        sql += ' AND p.category = ?'
        params.append(category_filter)
        
    sql += ' ORDER BY p.id DESC'
    products = [dict(r) for r in conn.execute(sql, params).fetchall()]
    
    categories = [r[0] for r in conn.execute('SELECT DISTINCT category FROM products').fetchall()]
    cart_count = conn.execute('SELECT SUM(quantity) FROM cart WHERE user_id = ?', (DEFAULT_BUYER_ID,)).fetchone()[0] or 0
    
    conn.close()
    return render_template('index.html', products=products, categories=categories, query_str=query_str, category_filter=category_filter, cart_count=cart_count)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    # Increment view count
    conn.execute('UPDATE products SET views = views + 1 WHERE id = ?', (product_id,))
    conn.commit()
    
    product_row = conn.execute('''
        SELECT p.*, u.name as seller_name, u.email as seller_email, u.phone as seller_phone, u.location as seller_location, u.rating as seller_rating
        FROM products p
        JOIN users u ON p.seller_id = u.id
        WHERE p.id = ?
    ''', (product_id,)).fetchone()
    
    if not product_row:
        conn.close()
        return "Produto não encontrado", 404
        
    product = dict(product_row)
    related_products = [dict(r) for r in conn.execute('''
        SELECT * FROM products WHERE category = ? AND id != ? LIMIT 4
    ''', (product['category'], product_id)).fetchall()]
    
    cart_count = conn.execute('SELECT SUM(quantity) FROM cart WHERE user_id = ?', (DEFAULT_BUYER_ID,)).fetchone()[0] or 0
    conn.close()
    return render_template('product.html', product=product, related_products=related_products, cart_count=cart_count)

@app.route('/cart')
def view_cart():
    conn = get_db_connection()
    cart_items = [dict(r) for r in conn.execute('''
        SELECT c.id as cart_id, c.quantity, p.*, u.name as seller_name
        FROM cart c
        JOIN products p ON c.product_id = p.id
        JOIN users u ON p.seller_id = u.id
        WHERE c.user_id = ?
    ''', (DEFAULT_BUYER_ID,)).fetchall()]
    
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping = 4.99 if subtotal > 0 else 0.0
    total = subtotal + shipping
    cart_count = sum(item['quantity'] for item in cart_items)
    
    conn.close()
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, shipping=shipping, total=total, cart_count=cart_count)

@app.route('/seller/dashboard')
def seller_dashboard():
    conn = get_db_connection()
    seller = dict(conn.execute('SELECT * FROM users WHERE id = ?', (DEFAULT_SELLER_ID,)).fetchone())
    my_products = [dict(r) for r in conn.execute('SELECT * FROM products WHERE seller_id = ? ORDER BY id DESC', (DEFAULT_SELLER_ID,)).fetchall()]
    
    # Orders containing seller's products
    seller_orders = [dict(r) for r in conn.execute('''
        SELECT o.order_number, o.created_at, o.status, u.name as buyer_name, p.title as product_title, oi.quantity, oi.unit_price
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        JOIN users u ON o.buyer_id = u.id
        WHERE p.seller_id = ?
        ORDER BY o.id DESC
    ''', (DEFAULT_SELLER_ID,)).fetchall()]
    
    total_sales = sum(o['quantity'] * o['unit_price'] for o in seller_orders)
    total_products = len(my_products)
    
    conn.close()
    return render_template('dashboard.html', seller=seller, my_products=my_products, seller_orders=seller_orders, total_sales=total_sales, total_products=total_products)

@app.route('/orders')
def view_orders():
    conn = get_db_connection()
    buyer_orders = [dict(r) for r in conn.execute('''
        SELECT * FROM orders WHERE buyer_id = ? ORDER BY id DESC
    ''', (DEFAULT_BUYER_ID,)).fetchall()]
    
    for order in buyer_orders:
        order['order_items'] = [dict(r) for r in conn.execute('''
            SELECT oi.*, p.title, p.image_url, u.name as seller_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            JOIN users u ON p.seller_id = u.id
            WHERE oi.order_id = ?
        ''', (order['id'],)).fetchall()]
        
    cart_count = conn.execute('SELECT SUM(quantity) FROM cart WHERE user_id = ?', (DEFAULT_BUYER_ID,)).fetchone()[0] or 0
    conn.close()
    return render_template('orders.html', orders=buyer_orders, cart_count=cart_count)

# API ENDPOINTS
@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.json or {}
    product_id = data.get('product_id')
    qty = int(data.get('quantity', 1))
    
    if not product_id:
        return jsonify({'success': False, 'message': 'ID de produto inválido'}), 400
        
    conn = get_db_connection()
    existing = conn.execute('SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?', (DEFAULT_BUYER_ID, product_id)).fetchone()
    
    if existing:
        conn.execute('UPDATE cart SET quantity = quantity + ? WHERE id = ?', (qty, existing['id']))
    else:
        conn.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (DEFAULT_BUYER_ID, product_id, qty))
        
    conn.commit()
    cart_count = conn.execute('SELECT SUM(quantity) FROM cart WHERE user_id = ?', (DEFAULT_BUYER_ID,)).fetchone()[0] or 0
    conn.close()
    
    return jsonify({'success': True, 'message': 'Produto adicionado ao carrinho com sucesso!', 'cart_count': cart_count})

@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    data = request.json or {}
    cart_id = data.get('cart_id')
    
    conn = get_db_connection()
    conn.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', (cart_id, DEFAULT_BUYER_ID))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Item removido do carrinho.'})

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    data = request.json or {}
    payment_method = data.get('payment_method', 'MB WAY')
    shipping_address = data.get('shipping_address', 'Av. da Liberdade 100, 1250-145 Lisboa')
    phone_mbway = data.get('phone_mbway', '+351 912 345 678')
    
    conn = get_db_connection()
    cart_items = conn.execute('''
        SELECT c.quantity, p.id as product_id, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (DEFAULT_BUYER_ID,)).fetchall()
    
    if not cart_items:
        conn.close()
        return jsonify({'success': False, 'message': 'O seu carrinho está vazio!'}), 400
        
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping = 4.99
    total_amount = round(subtotal + shipping, 2)
    
    # Create order
    order_number = f"AMZ-2026-{random.randint(1000, 9999)}"
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (order_number, buyer_id, total_amount, payment_method, status, shipping_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (order_number, DEFAULT_BUYER_ID, total_amount, payment_method, 'Em Processamento', shipping_address))
    
    order_id = cursor.lastrowid
    
    for item in cart_items:
        cursor.execute('''
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        ''', (order_id, item['product_id'], item['quantity'], item['price']))
        
    # Clear cart
    cursor.execute('DELETE FROM cart WHERE user_id = ?', (DEFAULT_BUYER_ID,))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'order_number': order_number,
        'message': f'Encomenda {order_number} efetuada com sucesso via {payment_method}!'
    })

@app.route('/api/products/create', methods=['POST'])
def api_product_create():
    data = request.json or {}
    title = data.get('title')
    description = data.get('description')
    price = float(data.get('price', 0))
    category = data.get('category', 'Tecnologia')
    condition = data.get('condition', 'Novo')
    image_url = data.get('image_url') or 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=800&q=80'
    stock = int(data.get('stock', 10))
    location = data.get('location', 'Faro, Algarve')
    
    if not title or not price:
        return jsonify({'success': False, 'message': 'Título e preço são obrigatórios'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (title, description, price, category, condition, seller_id, image_url, stock, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, price, category, condition, DEFAULT_SELLER_ID, image_url, stock, location))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Anúncio publicado no OLX Marketplace com sucesso!'})

if __name__ == '__main__':
    print("[SERVER] OLX-MARKETPLACE SaaS a iniciar na porta 6500...")
    app.run(host='0.0.0.0', port=6500, debug=False)
