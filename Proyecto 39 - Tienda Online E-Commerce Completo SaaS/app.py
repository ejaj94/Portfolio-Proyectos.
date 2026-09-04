import os
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import database

app = Flask(__name__)
app.secret_key = 'ejajtech_nova_trends_ecommerce_secret_2026'

# Inicializar Base de Dados
database.init_db()

def get_cart_count():
    cart = session.get('cart', {})
    return sum(cart.values())

@app.context_processor
def inject_global_vars():
    return dict(cart_count=get_cart_count())

# --- ROTAS DA LOJA ---

@app.route('/')
def index():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip()

    conn = database.get_db_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM products WHERE 1=1'
    params = []

    if category != 'all':
        query += ' AND category = ?'
        params.append(category)

    if search:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])

    query += ' ORDER BY sales_count DESC'
    cursor.execute(query, params)
    products = cursor.fetchall()

    # Categorias únicas para filtro
    cursor.execute('SELECT DISTINCT category FROM products')
    categories = [row['category'] for row in cursor.fetchall()]

    conn.close()

    return render_template(
        'index.html',
        products=products,
        categories=categories,
        current_category=category,
        search_query=search
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    if not product:
        conn.close()
        flash('O produto solicitado não foi encontrado.', 'warning')
        return redirect(url_for('index'))

    # Produtos Relacionados
    cursor.execute('SELECT * FROM products WHERE category = ? AND id != ? LIMIT 4', (product['category'], product_id))
    related_products = cursor.fetchall()

    conn.close()

    return render_template(
        'product_detail.html',
        product=product,
        related_products=related_products
    )

@app.route('/cart')
def cart():
    cart_dict = session.get('cart', {})
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cart_items = []
    subtotal = 0.0

    for pid_str, qty in cart_dict.items():
        cursor.execute('SELECT * FROM products WHERE id = ?', (int(pid_str),))
        prod = cursor.fetchone()
        if prod:
            item_subtotal = prod['price'] * qty
            subtotal += item_subtotal
            cart_items.append({
                'id': prod['id'],
                'name': prod['name'],
                'price': prod['price'],
                'image_url': prod['image_url'],
                'category': prod['category'],
                'quantity': qty,
                'subtotal': item_subtotal
            })

    conn.close()

    tax = subtotal * 0.23  # IVA 23%
    shipping = 0.0 if subtotal > 80.0 else 4.99
    total = subtotal + shipping

    return render_template(
        'cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        total=total
    )

@app.route('/checkout')
def checkout():
    cart_dict = session.get('cart', {})
    if not cart_dict:
        flash('O teu carrinho está vazio. Adiciona produtos antes de continuar.', 'info')
        return redirect(url_for('index'))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    cart_items = []
    subtotal = 0.0

    for pid_str, qty in cart_dict.items():
        cursor.execute('SELECT * FROM products WHERE id = ?', (int(pid_str),))
        prod = cursor.fetchone()
        if prod:
            item_subtotal = prod['price'] * qty
            subtotal += item_subtotal
            cart_items.append({
                'id': prod['id'],
                'name': prod['name'],
                'price': prod['price'],
                'quantity': qty,
                'subtotal': item_subtotal
            })

    conn.close()

    shipping = 0.0 if subtotal > 80.0 else 4.99
    total = subtotal + shipping

    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        total=total
    )

@app.route('/order-success/<order_number>')
def order_success(order_number):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM orders WHERE order_number = ?', (order_number,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        flash('Encomenda não encontrada.', 'danger')
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],))
    items = cursor.fetchall()
    conn.close()

    return render_template('order_success.html', order=order, items=items)

@app.route('/orders')
def orders():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT o.*, COUNT(oi.id) as total_items
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        GROUP BY o.id
        ORDER BY o.created_at DESC
    ''')
    orders_list = cursor.fetchall()
    conn.close()

    return render_template('orders.html', orders=orders_list)

@app.route('/admin/dashboard')
def dashboard():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Métricas Globais
    cursor.execute('SELECT SUM(total_amount), COUNT(*) FROM orders')
    totals = cursor.fetchone()
    total_revenue = totals[0] or 0.0
    total_orders = totals[1] or 0

    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(sales_count) FROM products')
    total_items_sold = cursor.fetchone()[0] or 0

    # Produto Mais Vendido
    cursor.execute('SELECT * FROM products ORDER BY sales_count DESC LIMIT 1')
    top_product = cursor.fetchone()

    # Vendas por Categoria para Chart.js
    cursor.execute('''
        SELECT category, SUM(sales_count) as total_sales, SUM(sales_count * price) as revenue
        FROM products
        GROUP BY category
    ''')
    category_metrics = cursor.fetchall()

    # Encomendas Recentes
    cursor.execute('''
        SELECT * FROM orders ORDER BY created_at DESC LIMIT 5
    ''')
    recent_orders = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_products=total_products,
        total_items_sold=total_items_sold,
        top_product=top_product,
        category_metrics=category_metrics,
        recent_orders=recent_orders
    )

# --- APIS REST ---

@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.get_json() or request.form
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'success': False, 'message': 'ID de produto inválido'}), 400

    cart_dict = session.get('cart', {})
    cart_dict[product_id] = cart_dict.get(product_id, 0) + quantity
    session['cart'] = cart_dict

    return jsonify({
        'success': True,
        'message': 'Produto adicionado ao carrinho com sucesso!',
        'cart_count': sum(cart_dict.values())
    })

@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    data = request.get_json() or request.form
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 1))

    cart_dict = session.get('cart', {})
    if quantity <= 0:
        cart_dict.pop(product_id, None)
    else:
        cart_dict[product_id] = quantity

    session['cart'] = cart_dict

    return jsonify({
        'success': True,
        'cart_count': sum(cart_dict.values())
    })

@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    data = request.get_json() or request.form
    product_id = str(data.get('product_id'))

    cart_dict = session.get('cart', {})
    cart_dict.pop(product_id, None)
    session['cart'] = cart_dict

    return jsonify({
        'success': True,
        'message': 'Produto removido do carrinho.',
        'cart_count': sum(cart_dict.values())
    })

@app.route('/api/checkout/process', methods=['POST'])
def api_checkout_process():
    cart_dict = session.get('cart', {})
    if not cart_dict:
        flash('O teu carrinho está vazio!', 'warning')
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    address = request.form.get('address', '').strip()
    city = request.form.get('city', '').strip()
    postal_code = request.form.get('postal_code', '').strip()
    payment_method = request.form.get('payment_method', 'MB WAY')

    if not name or not email or not address or not city or not postal_code:
        flash('Por favor preencha todos os campos obrigatórios do envio.', 'danger')
        return redirect(url_for('checkout'))

    conn = database.get_db_connection()
    cursor = conn.cursor()

    # Calcular total do pedido
    subtotal = 0.0
    order_items_data = []

    for pid_str, qty in cart_dict.items():
        cursor.execute('SELECT * FROM products WHERE id = ?', (int(pid_str),))
        prod = cursor.fetchone()
        if prod:
            item_subtotal = prod['price'] * qty
            subtotal += item_subtotal
            order_items_data.append((prod['id'], prod['name'], prod['price'], qty, item_subtotal))

    shipping = 0.0 if subtotal > 80.0 else 4.99
    total_amount = subtotal + shipping

    # Criar Número de Encomenda
    order_number = f"ORD-2026-{random.randint(1000, 9999)}"

    # Inserir Encomenda
    cursor.execute('''
        INSERT INTO orders (order_number, user_id, customer_name, customer_email, address, city, postal_code, total_amount, payment_method, status)
        VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?, 'Processado')
    ''', (order_number, name, email, address, city, postal_code, total_amount, payment_method))

    order_id = cursor.lastrowid

    # Inserir Itens & Atualizar Stock e Vendas
    for pid, p_name, p_price, qty, sub in order_items_data:
        cursor.execute('''
            INSERT INTO order_items (order_id, product_id, product_name, price, quantity, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order_id, pid, p_name, p_price, qty, sub))

        cursor.execute('''
            UPDATE products
            SET sales_count = sales_count + ?, stock = MAX(0, stock - ?)
            WHERE id = ?
        ''', (qty, qty, pid))

    # Atualizar métricas do utilizador
    cursor.execute('''
        UPDATE users
        SET total_spent = total_spent + ?, orders_count = orders_count + 1
        WHERE id = 1
    ''')

    conn.commit()
    conn.close()

    # Limpar Carrinho
    session['cart'] = {}

    flash(f'¡Encomenda {order_number} efetuada com sucesso!', 'success')
    return redirect(url_for('order_success', order_number=order_number))

if __name__ == '__main__':
    print("=" * 60)
    print(" [NOVA TRENDS E-Commerce SaaS] EJAJ TECH")
    print(" Servidor Flask a correr em http://127.0.0.1:6150")
    print("=" * 60)
    app.run(host='0.0.0.0', port=6150, debug=True)
