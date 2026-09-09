import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response

app = Flask(__name__)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))




DB_PATH = os.path.join(PROJECT_DIR, 'landings.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def build_landing_html(title, hero_headline, hero_subheadline, cta_text, c1, c2, bg_color, features, testimonials):
    """Generates complete standalone HTML5 code for the landing page"""
    title_text = (title or "Minha Landing Page").strip()
    headline = (hero_headline or "A Plataforma de Inteligência Artificial para a Sua Empresa").strip()
    subheadline = (hero_subheadline or "Automatize processos, aumente a produtividade e impulsione o seu negócio.").strip()
    btn_text = (cta_text or "Começar Agora Gratuitamente").strip()
    
    c1_color = c1 or "#00F5D4"
    c2_color = c2 or "#7000FF"
    bg_fill = bg_color or "#0F172A"
    
    # Render Features Cards HTML
    features_html = ""
    if features and isinstance(features, list):
        for item in features:
            icon = item.get('icon', 'fa-bolt')
            t = item.get('title', 'Serviço de Excelência')
            d = item.get('desc', 'Descrição detalhada das vantagens e benefícios.')
            features_html += f"""
            <div class="feature-card">
                <div class="feature-icon"><i class="fa-solid {icon}"></i></div>
                <h3 class="feature-title">{t}</h3>
                <p class="feature-desc">{d}</p>
            </div>
            """
    else:
        features_html = """
        <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-rocket"></i></div>
            <h3 class="feature-title">Alta Velocidade</h3>
            <p class="feature-desc">Infraestrutura otimizada para carregar em milissegundos.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-shield-halved"></i></div>
            <h3 class="feature-title">Segurança Máxima</h3>
            <p class="feature-desc">Proteção de dados de nível empresarial e encriptação total.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon"><i class="fa-solid fa-chart-pie"></i></div>
            <h3 class="feature-title">Analytics Avançado</h3>
            <p class="feature-desc">Relatórios e métricas claras para tomar as melhores decisões.</p>
        </div>
        """

    # Render Testimonials HTML
    testimonials_html = ""
    if testimonials and isinstance(testimonials, list):
        for test in testimonials:
            name = test.get('name', 'Cliente Satisfeito')
            role = test.get('role', 'Empresário')
            comment = test.get('comment', 'Excelente serviço e resultados surpreendentes!')
            stars = '<i class="fa-solid fa-star"></i>' * int(test.get('rating', 5))
            testimonials_html += f"""
            <div class="testimonial-card">
                <div class="stars">{stars}</div>
                <p class="comment">"{comment}"</p>
                <div class="client-info">
                    <strong>{name}</strong>
                    <span>{role}</span>
                </div>
            </div>
            """
    else:
        testimonials_html = """
        <div class="testimonial-card">
            <div class="stars"><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i></div>
            <p class="comment">"Aumentámos as conversões em 40% na primeira semana após o lançamento da nossa nova landing page."</p>
            <div class="client-info"><strong>Carlos Mendes</strong><span>CEO TechGroup</span></div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} | EJAJ TECH</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --c1: {c1_color};
            --c2: {c2_color};
            --bg: {bg_fill};
            --card-bg: rgba(255, 255, 255, 0.04);
            --border: rgba(255, 255, 255, 0.12);
            --text-light: #F8FAFC;
            --text-muted: #94A3B8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg);
            color: var(--text-light);
            line-height: 1.6;
        }}
        .header-nav {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .brand-logo {{
            font-weight: 900;
            font-size: 1.4rem;
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}
        .brand-logo span {{ color: var(--c1); }}
        
        .hero-section {{
            max-width: 1100px;
            margin: 3rem auto 5rem auto;
            text-align: center;
            padding: 0 1.5rem;
        }}
        .badge-tag {{
            background: linear-gradient(135deg, var(--c1), var(--c2));
            color: #0F172A;
            font-weight: 900;
            font-size: 0.85rem;
            padding: 0.4rem 1.2rem;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 1.25rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .hero-headline {{
            font-size: 3.2rem;
            font-weight: 900;
            line-height: 1.15;
            margin-bottom: 1.25rem;
            background: linear-gradient(135deg, #FFFFFF 40%, var(--c1) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-subheadline {{
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 750px;
            margin: 0 auto 2.5rem auto;
            font-weight: 600;
        }}
        .btn-cta {{
            background: linear-gradient(135deg, var(--c1), var(--c2));
            color: #0F172A;
            font-weight: 900;
            font-size: 1.15rem;
            padding: 1rem 2.5rem;
            border-radius: 14px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            box-shadow: 0 10px 30px rgba(0,245,212,0.3);
            transition: transform 0.2s ease;
        }}
        .btn-cta:hover {{ transform: translateY(-3px); }}

        .section-container {{
            max-width: 1200px;
            margin: 5rem auto;
            padding: 0 1.5rem;
        }}
        .section-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        .section-title {{
            font-size: 2.2rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.75rem;
        }}
        .feature-card {{
            background: var(--card-bg);
            border: 1.5px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.3s ease;
        }}
        .feature-card:hover {{
            border-color: var(--c1);
            transform: translateY(-5px);
        }}
        .feature-icon {{
            width: 52px;
            height: 52px;
            border-radius: 14px;
            background: linear-gradient(135deg, var(--c1), var(--c2));
            color: #0F172A;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            margin-bottom: 1.25rem;
            font-weight: 900;
        }}
        .feature-title {{
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }}
        .feature-desc {{
            color: var(--text-muted);
            font-size: 0.95rem;
        }}

        .testimonials-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.75rem;
        }}
        .testimonial-card {{
            background: var(--card-bg);
            border: 1.5px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
        }}
        .stars {{ color: #F59E0B; margin-bottom: 1rem; }}
        .comment {{ font-style: italic; font-size: 1rem; margin-bottom: 1.25rem; color: #E2E8F0; }}
        .client-info strong {{ display: block; font-weight: 800; color: white; }}
        .client-info span {{ font-size: 0.85rem; color: var(--text-muted); }}

        .cta-bottom-banner {{
            max-width: 1100px;
            margin: 6rem auto;
            background: linear-gradient(135deg, rgba(112,0,255,0.2), rgba(0,245,212,0.2));
            border: 2px solid var(--c1);
            border-radius: 24px;
            padding: 3.5rem 2rem;
            text-align: center;
        }}

        footer {{
            border-top: 1px solid var(--border);
            padding: 2.5rem 1.5rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>

    <nav class="header-nav">
        <a href="#" class="brand-logo"><i class="fa-solid fa-layer-group" style="color: var(--c1);"></i> {title_text}</a>
        <a href="https://wa.me/351911151993?text=AJUDA%20-%20Landing%20Page" target="_blank" class="btn-cta" style="padding: 0.55rem 1.4rem; font-size: 0.9rem;">
            <i class="fa-brands fa-whatsapp"></i> Falar com Especialista
        </a>
    </nav>

    <header class="hero-section">
        <span class="badge-tag">🚀 TECNOLOGIA DE ALTA PERFORMANCE</span>
        <h1 class="hero-headline">{headline}</h1>
        <p class="hero-subheadline">{subheadline}</p>
        <a href="https://wa.me/351911151993?text=AJUDA%20-%20{title_text}" target="_blank" class="btn-cta">
            <i class="fa-solid fa-rocket"></i> {btn_text}
        </a>
    </header>

    <section class="section-container">
        <div class="section-header">
            <h2 class="section-title">Soluções & Funcionalidades Principais</h2>
            <p style="color: var(--text-muted);">Concebido para maximizar os resultados do seu negócio.</p>
        </div>
        <div class="features-grid">
            {features_html}
        </div>
    </section>

    <section class="section-container">
        <div class="section-header">
            <h2 class="section-title">O que dizem os nossos clientes</h2>
            <p style="color: var(--text-muted);">Prova social de empresas que já transformaram a sua presença digital.</p>
        </div>
        <div class="testimonials-grid">
            {testimonials_html}
        </div>
    </section>

    <section class="cta-bottom-banner">
        <h2 style="font-size: 2.4rem; font-weight: 900; margin-bottom: 1rem;">Pronto para transformar a sua empresa?</h2>
        <p style="color: var(--text-muted); font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto;">
            Entre em contacto connosco e obtenha uma consultoria personalizada com a EJAJ TECH.
        </p>
        <a href="https://wa.me/351911151993?text=AJUDA%20-%20Consultoria" target="_blank" class="btn-cta">
            <i class="fa-brands fa-whatsapp"></i> WhatsApp: +351 911 151 993 (Digite "AJUDA")
        </a>
    </section>

    <footer>
        <p>&copy; 2026 {title_text}. Desenvolvido por Enmanuel Jimenez | Lead Architect EJAJ TECH.</p>
    </footer>

</body>
</html>"""
    return html

@app.route('/')
def studio_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM landing_templates ORDER BY id ASC")
    templates = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return render_template('studio.html', templates=templates)

@app.route('/history')
def history_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_landings ORDER BY id DESC")
    landings = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return render_template('history.html', landings=landings)

@app.route('/export/<int:landing_id>')
def export_page(landing_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_landings WHERE id = ?", (landing_id,))
    landing_row = cursor.fetchone()
    conn.close()
    if not landing_row:
        return redirect(url_for('history_page'))
    return render_template('export.html', landing=dict(landing_row))

@app.route('/preview-full/<int:landing_id>')
def preview_full_page(landing_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_landings WHERE id = ?", (landing_id,))
    landing = cursor.fetchone()
    conn.close()
    if not landing:
        return redirect(url_for('history_page'))
    return landing['html_code']

@app.route('/templates-gallery')
def templates_gallery_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM landing_templates ORDER BY id ASC")
    templates = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return render_template('templates_gallery.html', templates=templates)


# REST API ENDPOINTS

@app.route('/api/landing/generate', methods=['POST'])
def api_generate_landing():
    try:
        data = request.get_json() or {}
        title = data.get('title', 'EJAJ TECH Landing').strip()
        hero_headline = data.get('hero_headline', 'A Plataforma de Inteligência Artificial').strip()
        hero_subheadline = data.get('hero_subheadline', 'Automatize processos e aumente vendas.').strip()
        cta_text = data.get('cta_text', 'Começar Agora').strip()
        c1 = data.get('primary_color', '#00F5D4').strip()
        c2 = data.get('secondary_color', '#7000FF').strip()
        bg_color = data.get('bg_color', '#0F172A').strip()
        features = data.get('features', [])
        testimonials = data.get('testimonials', [])

        html_code = build_landing_html(title, hero_headline, hero_subheadline, cta_text, c1, c2, bg_color, features, testimonials)

        return jsonify({
            'success': True,
            'html_code': html_code
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/landing/save', methods=['POST'])
def api_save_landing():
    try:
        data = request.get_json() or {}
        title = data.get('title', 'Nova Landing Page').strip()
        template_name = data.get('template_name', 'Custom SaaS').strip()
        hero_headline = data.get('hero_headline', '').strip()
        hero_subheadline = data.get('hero_subheadline', '').strip()
        cta_text = data.get('cta_text', 'Começar Agora').strip()
        c1 = data.get('primary_color', '#00F5D4').strip()
        c2 = data.get('secondary_color', '#7000FF').strip()
        bg_color = data.get('bg_color', '#0F172A').strip()
        features = data.get('features', [])
        testimonials = data.get('testimonials', [])
        html_code = data.get('html_code', '').strip()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not html_code:
            html_code = build_landing_html(title, hero_headline, hero_subheadline, cta_text, c1, c2, bg_color, features, testimonials)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO saved_landings (title, template_name, hero_headline, hero_subheadline, cta_text, primary_color, secondary_color, bg_color, features_json, testimonials_json, html_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, template_name, hero_headline, hero_subheadline, cta_text,
            c1, c2, bg_color, json.dumps(features), json.dumps(testimonials),
            html_code, now_str
        ))

        landing_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'landing_id': landing_id, 'message': f'Landing Page "{title}" guardada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/landing/delete/<int:landing_id>', methods=['POST', 'DELETE'])
def api_delete_landing(landing_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_landings WHERE id = ?", (landing_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Landing Page removida da galeria.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/landing/download/<int:landing_id>')
def api_download_landing_file(landing_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_landings WHERE id = ?", (landing_id,))
        landing = cursor.fetchone()
        conn.close()

        if not landing:
            return redirect(url_for('history_page'))

        filename = f"landing_{landing['title'].lower().replace(' ', '_')}.html"
        return Response(
            landing['html_code'],
            mimetype="text/html",
            headers={"Content-disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    print("[Starting] EJAJ TECH - LandingCraft AI SaaS na porta 6916...")
    app.run(host='127.0.0.1', port=6916, debug=False, use_reloader=False)


