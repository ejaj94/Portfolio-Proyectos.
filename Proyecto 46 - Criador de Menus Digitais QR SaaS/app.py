import os
import sqlite3
import json
import io
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from database import DB_PATH, init_db

# QR Code Generation Library
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

app = Flask(__name__)
app.secret_key = 'ejajtech_qr_digital_menu_builder_secret_key'

# Custom Filters
@app.template_filter('currency')
def currency_filter(value):
    if value is None:
        return ""
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
    restaurants = [dict(r) for r in conn.execute('SELECT * FROM restaurants ORDER BY id ASC').fetchall()]
    conn.close()
    return render_template('index.html', restaurants=restaurants)

@app.route('/menu/<slug>')
def public_menu(slug):
    conn = get_db_connection()
    rest_row = conn.execute('SELECT * FROM restaurants WHERE slug = ?', (slug,)).fetchone()
    if not rest_row:
        conn.close()
        return "Restaurante não encontrado", 404
        
    restaurant = dict(rest_row)
    categories = [dict(r) for r in conn.execute('SELECT * FROM categories WHERE restaurant_id = ? ORDER BY display_order ASC', (restaurant['id'],)).fetchall()]
    
    # Map products to categories
    for cat in categories:
        cat['products'] = [dict(r) for r in conn.execute('''
            SELECT * FROM products 
            WHERE category_id = ? AND is_available = 1 
            ORDER BY is_featured DESC, id ASC
        ''', (cat['id'],)).fetchall()]
        
    featured_products = [dict(r) for r in conn.execute('SELECT * FROM products WHERE restaurant_id = ? AND is_featured = 1 AND is_available = 1', (restaurant['id'],)).fetchall()]
    offers = [dict(r) for r in conn.execute('SELECT * FROM offers WHERE restaurant_id = ? ORDER BY id DESC', (restaurant['id'],)).fetchall()]
    
    conn.close()
    return render_template('menu_public.html', restaurant=restaurant, categories=categories, featured_products=featured_products, offers=offers)

@app.route('/admin')
@app.route('/admin/<slug>')
def admin_panel(slug='burgers-crunch'):
    conn = get_db_connection()
    restaurants = [dict(r) for r in conn.execute('SELECT * FROM restaurants ORDER BY id ASC').fetchall()]
    
    rest_row = conn.execute('SELECT * FROM restaurants WHERE slug = ?', (slug,)).fetchone()
    if not rest_row:
        rest_row = conn.execute('SELECT * FROM restaurants LIMIT 1').fetchone()
        
    restaurant = dict(rest_row)
    categories = [dict(r) for r in conn.execute('SELECT * FROM categories WHERE restaurant_id = ? ORDER BY display_order ASC', (restaurant['id'],)).fetchall()]
    products = [dict(r) for r in conn.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.restaurant_id = ?
        ORDER BY p.id DESC
    ''', (restaurant['id'],)).fetchall()]
    offers = [dict(r) for r in conn.execute('SELECT * FROM offers WHERE restaurant_id = ? ORDER BY id DESC', (restaurant['id'],)).fetchall()]
    
    conn.close()
    return render_template('admin.html', restaurants=restaurants, restaurant=restaurant, categories=categories, products=products, offers=offers)

@app.route('/qr/<slug>')
def qr_standee(slug):
    conn = get_db_connection()
    rest_row = conn.execute('SELECT * FROM restaurants WHERE slug = ?', (slug,)).fetchone()
    if not rest_row:
        conn.close()
        return "Restaurante não encontrado", 404
        
    restaurant = dict(rest_row)
    conn.close()
    return render_template('qr_standee.html', restaurant=restaurant)

# API ENDPOINTS
@app.route('/api/qr/image/<slug>')
def api_qr_image(slug):
    target_url = f"http://{request.host}/menu/{slug}"
    
    if HAS_QRCODE:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(target_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return send_file(buffer, mimetype="image/png")
    else:
        # Fallback redirect to QR Server API
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={target_url}"
        return redirect(qr_api_url)

@app.route('/api/products/create', methods=['POST'])
def api_product_create():
    data = request.json or {}
    restaurant_id = data.get('restaurant_id')
    category_id = data.get('category_id')
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    price = float(data.get('price', 0))
    original_price = float(data['original_price']) if data.get('original_price') else None
    image_url = data.get('image_url') or 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80'
    allergens = data.get('allergens', '')
    is_featured = 1 if data.get('is_featured') else 0
    
    if not restaurant_id or not category_id or not name or not price:
        return jsonify({'success': False, 'message': 'Nome, categoria e preço são obrigatórios.'}), 400
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO products (restaurant_id, category_id, name, description, price, original_price, image_url, allergens, is_available, is_featured)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
    ''', (restaurant_id, category_id, name, description, price, original_price, image_url, allergens, is_featured))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Prato/Bebida adicionado ao menu com sucesso!'})

@app.route('/api/categories/create', methods=['POST'])
def api_category_create():
    data = request.json or {}
    restaurant_id = data.get('restaurant_id')
    name = data.get('name', '').strip()
    icon = data.get('icon', 'bi-egg-fried')
    
    if not restaurant_id or not name:
        return jsonify({'success': False, 'message': 'Nome da categoria é obrigatório.'}), 400
        
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM categories WHERE restaurant_id = ?', (restaurant_id,)).fetchone()[0]
    conn.execute('''
        INSERT INTO categories (restaurant_id, name, icon, display_order)
        VALUES (?, ?, ?, ?)
    ''', (restaurant_id, name, icon, count + 1))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Categoria "{name}" criada com sucesso!'})

@app.route('/api/offers/create', methods=['POST'])
def api_offer_create():
    data = request.json or {}
    restaurant_id = data.get('restaurant_id')
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    badge_text = data.get('badge_text', 'PROMO').strip()
    discount_percent = int(data.get('discount_percent', 10))
    valid_until = data.get('valid_until', '2026-12-31')
    
    if not restaurant_id or not title:
        return jsonify({'success': False, 'message': 'Título da promoção é obrigatório.'}), 400
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO offers (restaurant_id, title, description, badge_text, discount_percent, valid_until)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (restaurant_id, title, description, badge_text, discount_percent, valid_until))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Promoção/Oferta ativada com sucesso no menu!'})

@app.route('/api/theme/update', methods=['POST'])
def api_theme_update():
    data = request.json or {}
    restaurant_id = data.get('restaurant_id')
    primary_color = data.get('primary_color', '#FF6D00')
    bg_theme = data.get('bg_theme', '#0F172A')
    tagline = data.get('tagline')
    phone_whatsapp = data.get('phone_whatsapp')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE restaurants 
        SET primary_color = ?, bg_theme = ?, tagline = COALESCE(?, tagline), phone_whatsapp = COALESCE(?, phone_whatsapp)
        WHERE id = ?
    ''', (primary_color, bg_theme, tagline, phone_whatsapp, restaurant_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Tema e identidade do restaurante atualizados com sucesso!'})

if __name__ == '__main__':
    print("[SERVER] QR Digital Menu Builder SaaS a iniciar na porta 6800...")
    app.run(host='0.0.0.0', port=6800, debug=False)
