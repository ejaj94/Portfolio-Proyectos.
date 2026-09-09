import os
import sqlite3
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, 'logos.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def generate_svg_logo(brand_name, slogan, sector, style, c1, c2, symbol, layout):
    """Dynamically builds clean SVG vector logo code with Cartoon 3D aesthetics"""
    b_name = (brand_name or "MINHA MARCA").upper()
    s_name = (slogan or "").upper()
    
    bg_fill = "#1E293B" if style == 'Dark Cyber' else "#FFFDF0"
    text_fill = "#FFDE59" if style == 'Dark Cyber' else "#1E293B"
    stroke_color = "#1E293B" if style != 'Dark Cyber' else "#FFDE59"
    
    # Symbols shapes
    icon_paths = {
        'rocket': f'<path d="M 200 65 Q 230 95 230 135 L 170 135 Q 170 95 200 65 Z" fill="{c2}" stroke="{stroke_color}" stroke-width="6"/><circle cx="200" cy="105" r="14" fill="{c1}" stroke="{stroke_color}" stroke-width="4"/>',
        'robot': f'<rect x="165" y="70" width="70" height="55" rx="12" fill="{c1}" stroke="{stroke_color}" stroke-width="6"/><circle cx="185" cy="92" r="8" fill="{c2}"/><circle cx="215" cy="92" r="8" fill="{c2}"/><rect x="180" y="110" width="40" height="6" rx="3" fill="{stroke_color}"/>',
        'star': f'<polygon points="200,60 213,95 250,95 220,118 232,152 200,130 168,152 180,118 150,95 187,95" fill="{c1}" stroke="{stroke_color}" stroke-width="6"/>',
        'crown': f'<polygon points="160,130 160,75 180,105 200,65 220,105 240,75 240,130" fill="{c1}" stroke="{stroke_color}" stroke-width="6"/><circle cx="200" cy="65" r="7" fill="{c2}"/>',
        'coffee': f'<rect x="170" y="75" width="60" height="55" rx="10" fill="{c1}" stroke="{stroke_color}" stroke-width="6"/><path d="M 230 85 C 250 85 250 115 230 115" fill="none" stroke="{stroke_color}" stroke-width="6"/>'
    }
    
    symbol_svg = icon_paths.get(symbol, icon_paths['star'])
    
    if layout == 'badge_3d':
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 320" width="100%" height="100%">
  <rect width="400" height="320" rx="24" fill="{bg_fill}"/>
  <rect x="50" y="35" width="300" height="250" rx="30" fill="{c1}" stroke="{stroke_color}" stroke-width="8"/>
  <rect x="58" y="43" width="284" height="234" rx="24" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="8 8"/>
  <g transform="translate(0, -10)">
    {symbol_svg}
  </g>
  <text x="200" y="215" text-anchor="middle" font-family="'Inter', sans-serif" font-weight="900" font-size="26" fill="{stroke_color}">{b_name}</text>
  <text x="200" y="245" text-anchor="middle" font-family="'Inter', sans-serif" font-weight="800" font-size="13" fill="{c2}" letter-spacing="1">{s_name}</text>
</svg>"""
    elif layout == 'icon_left':
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 220" width="100%" height="100%">
  <rect width="440" height="220" rx="20" fill="{bg_fill}"/>
  <g transform="translate(-70, 0)">
    {symbol_svg}
  </g>
  <text x="240" y="115" text-anchor="start" font-family="'Inter', sans-serif" font-weight="900" font-size="28" fill="{text_fill}">{b_name}</text>
  <text x="240" y="145" text-anchor="start" font-family="'Inter', sans-serif" font-weight="700" font-size="14" fill="{c2}">{s_name}</text>
</svg>"""
    elif layout == 'minimal_circle':
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360" width="100%" height="100%">
  <rect width="360" height="360" rx="30" fill="{bg_fill}"/>
  <circle cx="180" cy="180" r="145" fill="{c1}" stroke="{stroke_color}" stroke-width="8"/>
  <circle cx="180" cy="180" r="128" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="6 6"/>
  <g transform="translate(-20, -30)">
    {symbol_svg}
  </g>
  <text x="180" y="250" text-anchor="middle" font-family="'Inter', sans-serif" font-weight="900" font-size="24" fill="{stroke_color}">{b_name}</text>
  <text x="180" y="278" text-anchor="middle" font-family="'Inter', sans-serif" font-weight="800" font-size="12" fill="{c2}">{s_name}</text>
</svg>"""
    else: # icon_top
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <rect width="400" height="300" rx="20" fill="{bg_fill}"/>
  <circle cx="200" cy="105" r="60" fill="{c1}" stroke="{stroke_color}" stroke-width="7"/>
  <g transform="translate(0, 0)">
    {symbol_svg}
  </g>
  <text x="200" y="215" text-anchor="middle" font-family="'Inter', sans-serif" font-weight="900" font-size="28" fill="{text_fill}">{b_name}</text>
  <text x="200" y="245" text-anchor="middle" font-family="'Inter', sans-serif" font-weight="700" font-size="14" fill="{c2}">{s_name}</text>
</svg>"""
        
    return svg

@app.route('/')
def studio_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brand_palettes ORDER BY id ASC")
    palettes = cursor.fetchall()
    conn.close()
    return render_template('studio.html', palettes=palettes)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_logos ORDER BY id DESC")
    logos = cursor.fetchall()
    conn.close()
    return render_template('history.html', logos=logos)

@app.route('/export/<int:logo_id>')
def export_page(logo_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_logos WHERE id = ?", (logo_id,))
    logo = cursor.fetchone()
    conn.close()
    if not logo:
        return redirect(url_for('history_page'))
    return render_template('export.html', logo=logo)

@app.route('/palettes')
def palettes_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brand_palettes ORDER BY id ASC")
    palettes = cursor.fetchall()
    conn.close()
    return render_template('palettes.html', palettes=palettes)

@app.route('/dia50')
def dia50_page():
    return render_template('dia50.html')

# REST API ENDPOINTS

@app.route('/api/logo/generate', methods=['POST'])
def api_generate_logo():
    try:
        data = request.get_json() or {}
        b_name = data.get('brand_name', 'EJAJ TECH').strip()
        slogan = data.get('slogan', 'Software de Alta Performance').strip()
        sector = data.get('sector', 'Tecnologia').strip()
        style = data.get('style', 'Caricatura 3D').strip()
        c1 = data.get('primary_color', '#FFDE59').strip()
        c2 = data.get('secondary_color', '#FF6B6B').strip()
        symbol = data.get('icon_symbol', 'rocket').strip()

        # Build 4 main layout variations
        v1 = generate_svg_logo(b_name, slogan, sector, style, c1, c2, symbol, 'badge_3d')
        v2 = generate_svg_logo(b_name, slogan, sector, style, c1, c2, symbol, 'icon_top')
        v3 = generate_svg_logo(b_name, slogan, sector, style, c1, c2, symbol, 'icon_left')
        v4 = generate_svg_logo(b_name, slogan, sector, style, c1, c2, symbol, 'minimal_circle')

        return jsonify({
            'success': True,
            'variations': [
                {'layout': 'badge_3d', 'name': 'Emblema 3D Cartoon', 'svg': v1},
                {'layout': 'icon_top', 'name': 'Logótipo Central Top', 'svg': v2},
                {'layout': 'icon_left', 'name': 'Formato Horizontal Pro', 'svg': v3},
                {'layout': 'minimal_circle', 'name': 'Medalhão Circular 3D', 'svg': v4}
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/logo/save', methods=['POST'])
def api_save_logo():
    try:
        data = request.get_json()
        b_name = data.get('brand_name', 'EJAJ Studio').strip()
        slogan = data.get('slogan', '').strip()
        sector = data.get('sector', 'Tecnologia').strip()
        style = data.get('style', 'Caricatura').strip()
        c1 = data.get('primary_color', '#FFDE59').strip()
        c2 = data.get('secondary_color', '#FF6B6B').strip()
        symbol = data.get('icon_symbol', 'star').strip()
        layout = data.get('layout_type', 'badge_3d').strip()
        svg_code = data.get('svg_code', '').strip()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not svg_code:
            svg_code = generate_svg_logo(b_name, slogan, sector, style, c1, c2, symbol, layout)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO saved_logos (brand_name, slogan, sector, style, primary_color, secondary_color, icon_symbol, layout_type, svg_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (b_name, slogan, sector, style, c1, c2, symbol, layout, svg_code, now_str))

        logo_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'logo_id': logo_id, 'message': f'Logótipo "{b_name}" guardado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/logo/delete/<int:logo_id>', methods=['POST', 'DELETE'])
def api_delete_logo(logo_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_logos WHERE id = ?", (logo_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Logótipo removido da galeria.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def render_png_hd(brand_name, slogan, style, c1, c2, symbol, layout):
    """Renders a high-definition 1200x900 PNG logo using Pillow"""
    width, height = 1200, 900
    bg_color = "#1E293B" if style == 'Dark Cyber' else "#FFFDF0"
    text_color = "#FFDE59" if style == 'Dark Cyber' else "#1E293B"
    stroke_color = "#1E293B" if style != 'Dark Cyber' else "#FFDE59"
    
    img = Image.new("RGBA", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    b_name = (brand_name or "EJAJ TECH").upper()
    s_name = (slogan or "SOFTWARE DE ALTA PERFORMANCE").upper()
    
    # Draw Cartoon 3D Card / Frame
    if layout == 'badge_3d':
        draw.rounded_rectangle([150, 105, 1050, 795], radius=60, fill=c1, outline=stroke_color, width=24)
        draw.rounded_rectangle([174, 129, 1026, 771], radius=48, fill=None, outline="#FFFFFF", width=12)
    elif layout == 'minimal_circle':
        draw.ellipse([225, 75, 975, 825], fill=c1, outline=stroke_color, width=24)
        draw.ellipse([255, 105, 945, 795], fill=None, outline="#FFFFFF", width=12)
    else: # icon_top or icon_left
        draw.rounded_rectangle([100, 80, 1100, 820], radius=50, fill=c1, outline=stroke_color, width=20)
        
    # Draw Symbol Icon Shapes
    cx, cy = 600, 320
    if symbol == 'rocket':
        draw.polygon([(cx, cy - 120), (cx + 90, cy + 90), (cx - 90, cy + 90)], fill=c2, outline=stroke_color, width=16)
        draw.ellipse([cx - 40, cy - 20, cx + 40, cy + 60], fill=c1, outline=stroke_color, width=12)
    elif symbol == 'robot':
        draw.rounded_rectangle([cx - 110, cy - 90, cx + 110, cy + 70], radius=30, fill=c1, outline=stroke_color, width=18)
        draw.ellipse([cx - 60, cy - 30, cx - 20, cy + 10], fill=c2)
        draw.ellipse([cx + 20, cy - 30, cx + 60, cy + 10], fill=c2)
        draw.rectangle([cx - 70, cy + 30, cx + 70, cy + 48], fill=stroke_color)
    elif symbol == 'crown':
        draw.polygon([(cx - 140, cy + 80), (cx - 140, cy - 60), (cx - 70, cy + 20), (cx, cy - 100), (cx + 70, cy + 20), (cx + 140, cy - 60), (cx + 140, cy + 80)], fill=c1, outline=stroke_color, width=16)
        draw.ellipse([cx - 25, cy - 125, cx + 25, cy - 75], fill=c2)
    elif symbol == 'coffee':
        draw.rounded_rectangle([cx - 90, cy - 70, cx + 90, cy + 80], radius=30, fill=c1, outline=stroke_color, width=18)
        draw.arc([cx + 60, cy - 40, cx + 160, cy + 50], start=270, end=90, fill=stroke_color, width=18)
    else: # star
        draw.polygon([(cx, cy - 140), (cx + 35, cy - 35), (cx + 140, cy - 35), (cx + 55, cy + 30), (cx + 90, cy + 130), (cx, cy + 65), (cx - 90, cy + 130), (cx - 55, cy + 30), (cx - 140, cy - 35), (cx - 35, cy - 35)], fill=c1, outline=stroke_color, width=16)

    # Draw Brand Text
    try:
        font_large = ImageFont.truetype("arial.ttf", 64)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((600, 610), b_name, fill=stroke_color, font=font_large, anchor="mm")
    draw.text((600, 690), s_name, fill=c2, font=font_small, anchor="mm")

    buf = BytesIO()
    img.save(buf, format="PNG", quality=100)
    buf.seek(0)
    return buf

@app.route('/api/logo/export-png', methods=['GET', 'POST'])
def api_export_png():
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args

        logo_id = data.get('id')
        if logo_id:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM saved_logos WHERE id = ?", (logo_id,))
            saved = cursor.fetchone()
            conn.close()
            if saved:
                b_name = saved['brand_name']
                slogan = saved['slogan']
                style = saved['style']
                c1 = saved['primary_color']
                c2 = saved['secondary_color']
                symbol = saved['icon_symbol']
                layout = saved['layout_type']
                buf = render_png_hd(b_name, slogan, style, c1, c2, symbol, layout)
                filename = f"{b_name.lower().replace(' ', '_')}_hd.png"
                return send_file(buf, mimetype='image/png', as_attachment=True, download_name=filename)

        b_name = data.get('brand_name', 'EJAJ TECH')
        slogan = data.get('slogan', 'Software de Alta Performance')
        style = data.get('style', 'Caricatura 3D')
        c1 = data.get('primary_color', '#FFDE59')
        c2 = data.get('secondary_color', '#FF6B6B')
        symbol = data.get('icon_symbol', 'rocket')
        layout = data.get('layout_type', 'badge_3d')

        buf = render_png_hd(b_name, slogan, style, c1, c2, symbol, layout)
        filename = f"logotipo_ejajtech_hd.png"
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - LogoCraft AI SaaS na porta 6915...")
    app.run(host='0.0.0.0', port=6915, debug=True)
