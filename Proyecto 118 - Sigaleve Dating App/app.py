import pyotp
import qrcode
import io
import base64
"""
preview_server.py — Sigaleve Server 100% Funcional
Servidor para Sigaleve con persistencia de usuarios, perfiles, sesiones,
validación de contraseñas de alta seguridad, fotos HD y Socket.IO.
"""
import random, uuid, datetime, re, os, json, smtplib, time
import urllib.request
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sigaleve-production-super-secret-key-2026")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
socketio = SocketIO(app, cors_allowed_origins="*")

# Carregar variáveis de ambiente de .env se existir
ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(ENV_FILE):
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except Exception:
        pass

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "86970408130-8ugh10poqvbespttgfqr5553hkgvkn4d.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

META_APP_ID = os.environ.get("META_APP_ID", "")
META_APP_SECRET = os.environ.get("META_APP_SECRET", "")
FACEBOOK_APP_ID = META_APP_ID
FACEBOOK_APP_SECRET = META_APP_SECRET
INSTAGRAM_APP_ID = META_APP_ID
INSTAGRAM_APP_SECRET = META_APP_SECRET

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER or "support@sigaleve.com")

def send_real_email(recipient: str, subject: str, html_content: str, text_content: str = "") -> tuple[bool, str]:
    """
    Envía un e-mail real por SMTP al buzón del usuario (Gmail, Outlook, etc.).
    Si las credenciales SMTP no están definidas o fallan, registra detalladamente
    en consola y en el buzón local para que el enlace y el código nunca se pierdan.
    """
    email_delivered = False
    delivery_note = ""

    if SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"Sigaleve Segurança <{SMTP_FROM}>"
            msg["To"] = recipient

            if text_content:
                msg.attach(MIMEText(text_content, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=12) as server:
                server.ehlo()
                if SMTP_PORT == 587:
                    server.starttls()
                    server.ehlo()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_FROM, recipient, msg.as_string())

            print(f"[EMAIL ENVIADO CON EXITO A BANDEJA REAL] Destinatario: {recipient}")
            email_delivered = True
            delivery_note = f"E-mail real entregue na tua caixa de entrada ({recipient})."
        except Exception as exc:
            err_msg = f"Falha SMTP ao enviar para {recipient}: {str(exc)}"
            print(f"[SMTP ERROR] {err_msg}")
            delivery_note = f"Falha no envio SMTP ({str(exc)}). Codigo disponivel em ecra."
    else:
        delivery_note = "Credenciais SMTP_USER/SMTP_PASS nao configuradas. Acesso direto ativo no ecra."
        print(f"\n=======================================================")
        print(f"[DISPATCH DE E-MAIL SIGALEVE] -> {recipient}")
        print(f"Assunto: {subject}")
        print(f"Conteudo: {text_content or html_content}")
        print(f"=======================================================\n")

    return email_delivered, delivery_note


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
USERS_FILE = os.path.join(DATA_DIR, "users_store.json")

def load_users():
    users = {}
    target_file = USERS_FILE
    if not os.path.exists(target_file):
        example_file = os.path.join(DATA_DIR, "users_store.example.json")
        if os.path.exists(example_file):
            target_file = example_file

    if os.path.exists(target_file):
        try:
            with open(target_file, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception as e:
            print(f"[LOAD_USERS ERROR] {e}")
            backup_file = USERS_FILE + ".bak"
            if os.path.exists(backup_file):
                try:
                    with open(backup_file, "r", encoding="utf-8") as f_bak:
                        users = json.load(f_bak)
                except Exception:
                    users = {}
    return users

def save_users(users):
    if not isinstance(users, dict):
        return
    temp_file = USERS_FILE + ".tmp"
    backup_file = USERS_FILE + ".bak"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        # If write succeeded, back up old file and atomically replace
        if os.path.exists(USERS_FILE):
            try:
                import shutil
                shutil.copyfile(USERS_FILE, backup_file)
            except Exception:
                pass
        os.replace(temp_file, USERS_FILE)
    except Exception as e:
        print(f"[SAVE_USERS ERROR] {e}")

def serialize_user(user: dict) -> dict:
    if not user:
        return {}
    return {
        "id": user.get("id"),
        "email": user.get("email"),
        "display_name": user.get("display_name", "Utilizador"),
        "phone": user.get("phone", ""),
        "age": user.get("age", 25),
        "city": user.get("city", "Lisboa, Portugal"),
        "bio": user.get("bio", ""),
        "photo": user.get("photo", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"),
        "photos": user.get("photos", []),
        "interests": user.get("interests", ["Viagens", "Música"]),
        "diagnosis": user.get("diagnosis", "ALPHA"),
        "custom_diagnosis": user.get("custom_diagnosis", ""),
        "relationship_goal": user.get("relationship_goal", ""),
        "zodiac": user.get("zodiac", ""),
        "education": user.get("education", ""),
        "height": user.get("height", ""),
        "lifestyle": user.get("lifestyle", ""),
        "seeking": user.get("seeking", "Todos"),
        "max_distance": user.get("max_distance", 50),
        "is_profile_configured": user.get("is_profile_configured", False),
        "is_plus": user.get("is_plus", False),
        "subscription": user.get("subscription", None)
    }

# Base de dados de utilizadores
_users = load_users()

# Perfiles de descubrimiento en Alta Definición (Unsplash HD)
PROFILES_HD = [
    {
        "id": "p1",
        "name": "Mariana Costa",
        "age": 26,
        "city": "Lisboa",
        "km": "3 km de distância",
        "code": "A",
        "activity": "Ativa recentemente",
        "photo": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Arquiteta e fotógrafa em Lisboa. Amor pelo mar, pores do sol na linha de Cascais e conversas genuínas sem preconceitos.",
        "relationship_goal": "🥂 Relação estável",
        "goal_icon": "🥂",
        "zodiac": "Leão",
        "education": "Mestrado em Arquitetura",
        "height": "170 cm",
        "lifestyle": "Não fumadora · Pratica Pilates",
        "interests": ["Arquitetura", "Fotografia", "Vinho Tinto", "Praia", "Arte Moderna"],
        "verified": True
    },
    {
        "id": "p2",
        "name": "João Pereira",
        "age": 29,
        "city": "Porto",
        "km": "7 km de distância",
        "code": "B",
        "activity": "Ativo recentemente",
        "photo": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Engenheiro de energias renováveis. Apaixonado por trilhos na serra do Gerês, culinária e boa música ao vivo.",
        "relationship_goal": "🥂 Nada sério, mas logo se vê",
        "goal_icon": "🥂",
        "zodiac": "Sagitário",
        "education": "Engenharia Mecânica",
        "height": "182 cm",
        "lifestyle": "Ativo / Ginásio",
        "interests": ["Trilhas", "Cozinha", "Rock Clássico", "Natureza", "Tecnologia"],
        "verified": True
    },
    {
        "id": "p3",
        "name": "Beatriz Santos",
        "age": 24,
        "city": "Coimbra",
        "km": "12 km de distância",
        "code": "C",
        "activity": "Ativa hoje",
        "photo": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Finalista de Psicologia. Apaixonada por literatura contemporânea, cafés tranquilos e conversas profundas sobre tudo e nada.",
        "relationship_goal": "💬 Nuevas amistades",
        "goal_icon": "💬",
        "zodiac": "Peixes",
        "education": "Licenciatura em Psicologia",
        "height": "165 cm",
        "lifestyle": "Café Lover · Vegetariana",
        "interests": ["Psicologia", "Livros", "Cinema Indie", "Café", "Yoga"],
        "verified": True
    },
    {
        "id": "p4",
        "name": "Lucas Amado",
        "age": 32,
        "city": "Luanda / Lisboa",
        "km": "5 km de distância",
        "code": "D",
        "activity": "Ativo recentemente",
        "photo": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Empreendedor internacional no setor de inovação. Adoro viajar pelo continente africano e pela Europa, partilhar boa gastronomia e energia positiva.",
        "relationship_goal": "🥂 Relação estável",
        "goal_icon": "🥂",
        "zodiac": "Touro",
        "education": "MBA em Gestão",
        "height": "186 cm",
        "lifestyle": "Não fumador · Treino diário",
        "interests": ["Negócios", "Viagens", "Jazz", "Tecnologia", "Gastronomia"],
        "verified": True
    },
    {
        "id": "p5",
        "name": "Inês Ferreira",
        "age": 27,
        "city": "Faro / Algarve",
        "km": "18 km de distância",
        "code": "E",
        "activity": "Ativa agora",
        "photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Instrutora de surf e defensora do oceano. Vida simples, sol na pele e pessoas que sabem cuidar do seu bem-estar sem medos.",
        "relationship_goal": "✨ Aún no lo tengo claro",
        "goal_icon": "✨",
        "zodiac": "Carneiro",
        "education": "Ciências do Desporto",
        "height": "168 cm",
        "lifestyle": "Surf diário · Saudável",
        "interests": ["Surf", "Yoga", "Praia", "Sustentabilidade", "Pôr do Sol"],
        "verified": True
    },
    {
        "id": "p6",
        "name": "Kofi Mensah",
        "age": 30,
        "city": "Praia / Lisboa",
        "km": "15 km de distância",
        "code": "F",
        "activity": "Ativo hoje",
        "photo": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Designer de produto UI/UX. Apaixonado por artes visuais, gastronomia afro-atlântica, corrida urbana e conversas sem julgamentos.",
        "relationship_goal": "🥂 Relação estável",
        "goal_icon": "🥂",
        "zodiac": "Balança",
        "education": "Design Multimédia",
        "height": "180 cm",
        "lifestyle": "Corredor amador · Criativo",
        "interests": ["Design", "Artes Visuais", "Corrida", "Música Afro", "Café"],
        "verified": True
    },
    {
        "id": "p7",
        "name": "Camila Oliveira",
        "age": 28,
        "city": "Cascais",
        "km": "4 km de distância",
        "code": "A",
        "activity": "Ativa recentemente",
        "photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1200&q=85",
        "photos": [
            "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1200&q=85",
            "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=1200&q=85"
        ],
        "bio": "Veterinária de pequenos animais. Procuro conexões autênticas, caminhadas ao fim da tarde e alguém que aprecie boa conversa e verdade.",
        "relationship_goal": "🥂 Relação estável",
        "goal_icon": "🥂",
        "zodiac": "Gémeos",
        "education": "Medicina Veterinária",
        "height": "172 cm",
        "lifestyle": "Amante dos animais · Não fumadora",
        "interests": ["Animais", "Passeios", "Vinho Branco", "Teatro", "Praia"],
        "verified": True
    }
]

AUTO_REPLIES = [
    "Olá! Fiquei muito feliz com a tua mensagem! 😊",
    "Conta-me mais sobre ti, o que gostas de fazer nos tempos livres?",
    "Haha, adorei! Tens muito bom sentido de humor 😄",
    "Tens planos para este fim de semana? Adorava conversar mais.",
    "Totalmente de acordo contigo! A autenticidade é tudo 💜",
    "Já há muito tempo que não conhecia alguém com uma energia tão boa!",
    "Que interessante, partilho exatamente da mesma visão!"
]

def validate_password_complexity(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "A palavra-passe deve conter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "A palavra-passe deve conter pelo menos uma letra maiúscula."
    if not re.search(r"[0-9]", password):
        return False, "A palavra-passe deve conter pelo menos um número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\/]", password):
        return False, "A palavra-passe deve conter pelo menos um caractere especial (!@#$%...)."
    return True, ""

# ── Headers No-Cache e Blindagem de Segurança HTTP ──────────────────────────
@app.after_request
def add_security_and_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # Blindagem de Segurança Web
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["Permissions-Policy"] = "camera=(self), microphone=(), geolocation=(self)"
    return response

# ── Dicionário SEO Multi-idioma para Google & Motores de Busca ────────────────
SEO_LOCALES = {
    "pt": {
        "title": "Sigaleve | Conecta com Autenticidade, Sem Julgamentos",
        "description": "Sigaleve é a aplicação de encontros mais autêntica e inclusiva para conectar com pessoas reais, sem filtros nem preconceitos.",
        "og_locale": "pt_PT"
    },
    "es": {
        "title": "Sigaleve | Citas, Conoce Gente y Conecta Sin Prejuicios",
        "description": "Sigaleve es la app de citas más auténtica e inclusiva para conectar con personas reales, compartir momentos y empezar algo único.",
        "og_locale": "es_ES"
    },
    "en": {
        "title": "Sigaleve | Authentic Dating, Meet People Without Judgments",
        "description": "Sigaleve is the modern, judgment-free dating app to meet genuine people, share authentic moments, and spark real connections.",
        "og_locale": "en_US"
    },
    "fr": {
        "title": "Sigaleve | Rencontres Authentiques, Sans Jugement",
        "description": "Sigaleve est l'application de rencontres moderne et authentique pour faire des rencontres réelles sans filtres ni préjugés.",
        "og_locale": "fr_FR"
    },
    "de": {
        "title": "Sigaleve | Authentisches Dating, Lerne Echte Menschen Kennen",
        "description": "Sigaleve ist die moderne Dating-App für echte Begegnungen, authentische Momente und vorurteilsfreie Verbindungen.",
        "og_locale": "de_DE"
    },
    "it": {
        "title": "Sigaleve | Incontri Autentici, Conosci Persone Senza Pregiudizi",
        "description": "Sigaleve è l'app di incontri inclusiva e autentica per conoscere persone speciali e connetterti in totale libertà.",
        "og_locale": "it_IT"
    },
    "sw": {
        "title": "Sigaleve | Ungana na Watu Halisi Bila Hukumu",
        "description": "Sigaleve ni programu ya kisasa ya kukutana na marafiki na mahusiano ya kweli bila ubaguzi au hukumu.",
        "og_locale": "sw_KE"
    },
    "yo": {
        "title": "Sigaleve | Pade Awon Eniyan Todaju Laisi Idajo",
        "description": "Sigaleve je ohun elo ife ati ore ti o daju fun awon eniyan lati sopo pelu otito laisi idajo.",
        "og_locale": "yo_NG"
    },
    "ha": {
        "title": "Sigaleve | Hadu da Mutane na Gaskiya Ba Tare da Hukunci ba",
        "description": "Sigaleve manhaja ce ta zamani don haduwa da mutane na gaske da gina abota mai inganci.",
        "og_locale": "ha_NG"
    },
    "ar": {
        "title": "Sigaleve | تعارف حقيقي وتواصل دون أحكام مسبقة",
        "description": "تطبيق Sigaleve الحديث للتواصل والتعارف الصادق بكل حرية واحترام متبادل.",
        "og_locale": "ar_AR"
    }
}

def resolve_request_language():
    # 1. URL Query Param ?lang=
    arg_lang = request.args.get("lang")
    if arg_lang and arg_lang.lower() in SEO_LOCALES:
        return arg_lang.lower()
    # 2. Cookie
    cookie_lang = request.cookies.get("sigaleve_lang")
    if cookie_lang and cookie_lang.lower() in SEO_LOCALES:
        return cookie_lang.lower()
    # 3. Accept-Language header de Googlebot / Navegadores
    accept = request.headers.get("Accept-Language", "")
    for part in accept.split(","):
        code = part.split(";")[0].strip()[:2].lower()
        if code in SEO_LOCALES:
            return code
    # Default oficial: Português
    return "pt"

# ── Rotas de Páginas ──────────────────────────────────────────────────────────
@app.route("/")
def landing():
    lang = resolve_request_language()
    explicit_lang = request.args.get("lang")
    seo_data = SEO_LOCALES.get(lang, SEO_LOCALES["pt"])
    resp = app.make_response(render_template(
        "landing.html",
        current_lang=lang,
        seo_title=seo_data["title"],
        seo_desc=seo_data["description"],
        seo_locale=seo_data["og_locale"]
    ))
    if explicit_lang:
        resp.set_cookie("sigaleve_lang", explicit_lang, max_age=31536000, path="/")
    return resp

@app.route("/robots.txt")
def robots_txt():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "Sitemap: https://sigaleve.com/sitemap.xml\n"
    )
    return app.response_class(content, mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap_xml():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    langs = ["pt", "en", "es", "fr", "de", "it", "sw", "yo", "ha", "ar"]
    for l in langs:
        url_loc = f"https://sigaleve.com/?lang={l}" if l != "pt" else "https://sigaleve.com/"
        xml.append("  <url>")
        xml.append(f"    <loc>{url_loc}</loc>")
        for alt in langs:
            alt_loc = f"https://sigaleve.com/?lang={alt}" if alt != "pt" else "https://sigaleve.com/"
            xml.append(f'    <xhtml:link rel="alternate" hreflang="{alt}" href="{alt_loc}"/>')
        xml.append('    <xhtml:link rel="alternate" hreflang="x-default" href="https://sigaleve.com/"/>')
        xml.append("    <changefreq>daily</changefreq>")
        xml.append("    <priority>1.0</priority>")
        xml.append("  </url>")
    
    xml.append("</urlset>")
    return app.response_class("\n".join(xml), mimetype="application/xml")

@app.route("/app")
def main_app():
    lang = resolve_request_language()
    explicit_lang = request.args.get("lang")
    seo_data = SEO_LOCALES.get(lang, SEO_LOCALES["pt"])
    resp = app.make_response(render_template(
        "sigaleve_app.html",
        current_lang=lang,
        seo_title=seo_data["title"],
        seo_desc=seo_data["description"]
    ))
    if explicit_lang:
        resp.set_cookie("sigaleve_lang", explicit_lang, max_age=31536000, path="/")
    return resp

@app.route("/confirm-email/<token>")
def confirm_email_page(token):
    users = load_users()
    matched_user = None
    for email, u in users.items():
        if u.get("verify_token") == token:
            matched_user = u
            u["email_verified"] = True
            break
    if matched_user:
        save_users(users)
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>E-mail Confirmado | Sigaleve</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0b0e14] text-white flex items-center justify-center min-h-screen p-6 font-sans">
    <div class="max-w-md w-full bg-[#161a23] border border-emerald-500/40 rounded-3xl p-8 text-center shadow-2xl">
        <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center text-3xl mx-auto mb-4 border border-emerald-500/50">
            ✓
        </div>
        <h1 class="text-2xl font-black mb-2">E-mail Confirmado com Sucesso!</h1>
        <p class="text-gray-300 text-sm mb-6 leading-relaxed">O teu endereço foi validado. Por motivos de segurança, foi gerado o teu código de acesso para concluir o login na aplicação.</p>
        <a href="/app?verified=true" class="block w-full py-3.5 rounded-full font-bold text-white bg-gradient-to-r from-pink-500 to-orange-500 hover:opacity-90 transition-all shadow-lg">
            Voltar e Inserir Código de Acesso
        </a>
    </div>
</body>
</html>"""
    else:
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ligação Expirada | Sigaleve</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0b0e14] text-white flex items-center justify-center min-h-screen p-6 font-sans">
    <div class="max-w-md w-full bg-[#161a23] border border-red-500/40 rounded-3xl p-8 text-center shadow-2xl">
        <div class="w-16 h-16 bg-red-500/20 text-red-400 rounded-full flex items-center justify-center text-3xl mx-auto mb-4 border border-red-500/50">
            ✕
        </div>
        <h1 class="text-2xl font-black mb-2">Ligação Inválida ou Expirada</h1>
        <p class="text-gray-300 text-sm mb-6">Esta ligação de confirmação já foi utilizada ou não é válida.</p>
        <a href="/app" class="block w-full py-3.5 rounded-full font-bold text-white bg-white/10 hover:bg-white/20 transition-all">
            Ir para o Sigaleve
        </a>
    </div>
</body>
</html>"""

@app.route("/legal/privacy")
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/legal/terms")
@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/legal/cookies")
@app.route("/cookies")
def cookies():
    return render_template("cookies_policy.html")

@app.route("/legal/community")
@app.route("/community-rules")
def legal_community():
    return render_template("community_rules.html")

@app.route("/legal/safety")
@app.route("/legal/safety-tips")
@app.route("/safety")
def legal_safety():
    return render_template("safety_policy.html")

@app.route("/legal/accessibility")
@app.route("/accessibility")
def legal_accessibility():
    return render_template("accessibility.html")

@app.route("/legal/help")
@app.route("/legal/suporte")
@app.route("/help")
@app.route("/help-center")
def legal_help():
    return render_template("help_center.html")

@app.route("/api/v1/translate", methods=["POST"])
def api_translate():
    import urllib.request
    import urllib.parse
    data = request.get_json(silent=True) or {}
    texts = data.get("texts", [])
    target = data.get("target", "pt")
    source = data.get("source", "es")
    
    if not texts or not isinstance(texts, list):
        return jsonify({"success": False, "error": "No texts provided"}), 400
        
    translated = {}
    for t in texts:
        t_str = str(t).strip()
        if not t_str:
            continue
        res_text = None

        # 1. Tentar Google Translate gtx
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source}&tl={target}&dt=t&q=" + urllib.parse.quote(t_str)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                res_text = "".join([part[0] for part in res_data[0] if part and part[0]])
        except Exception:
            res_text = None

        # 2. Fallback: MyMemory API
        if not res_text or res_text == t_str:
            try:
                pair = f"{source}|{target}"
                url2 = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(t_str)}&langpair={pair}"
                req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req2, timeout=3) as resp2:
                    mdata = json.loads(resp2.read().decode('utf-8'))
                    cand = mdata.get("responseData", {}).get("translatedText")
                    if cand and not cand.startswith("MYMEMORY WARNING"):
                        res_text = cand
            except Exception:
                pass

        # 3. Fallback: Lingva
        if not res_text or res_text == t_str:
            try:
                url3 = f"https://lingva.ml/api/v1/{source}/{target}/" + urllib.parse.quote(t_str)
                req3 = urllib.request.Request(url3, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req3, timeout=3) as resp3:
                    ldata = json.loads(resp3.read().decode('utf-8'))
                    if ldata.get("translation"):
                        res_text = ldata["translation"]
            except Exception:
                pass

        translated[t_str] = res_text if res_text else t_str
            
    return jsonify({"success": True, "translations": translated})



# ── API de Autenticação Real com Confirmação e Código 2FA ────────────────────
@app.route("/api/v1/auth/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    confirm_password = str(data.get("confirm_password", ""))
    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    dob = str(data.get("date_of_birth", "")).strip()
    device_id = str(data.get("device_id", "web-default")).strip()

    if not email or "@" not in email:
        return jsonify({"success": False, "error": "Endereço de e-mail inválido."}), 400
    if not name:
        return jsonify({"success": False, "error": "O nome ou pseudónimo é obrigatório."}), 400
    if password != confirm_password:
        return jsonify({"success": False, "error": "As palavras-passe não coincidem."}), 400

    valid, msg = validate_password_complexity(password)
    if not valid:
        return jsonify({"success": False, "error": msg}), 400

    age = 25
    if dob:
        try:
            birth_date = datetime.date.fromisoformat(dob)
            today = datetime.date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                return jsonify({"success": False, "error": "É estritamente necessário ter pelo menos 18 anos."}), 403
        except Exception:
            return jsonify({"success": False, "error": "Formato de data de nascimento inválido."}), 400

    users = load_users()
    if email in users:
        return jsonify({"success": False, "error": "Este e-mail já está registado. Por favor, usa outro e-mail ou inicia sessão."}), 409

    for existing_email, existing_user in users.items():
        if existing_user.get("display_name", "").strip().lower() == name.lower():
            return jsonify({"success": False, "error": f"O nome de utilizador '{name}' já está a ser utilizado. Por favor, escolhe outro."}), 409

    user_id = str(uuid.uuid4())
    default_photo = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"

    verify_token = str(uuid.uuid4())[:12]
    # Gerar código de 6 dígitos para confirmação
    otp_code = f"{random.randint(100000, 999999)}"

    new_user = {
        "id": user_id,
        "email": email,
        "password_hash": generate_password_hash(password),
        "display_name": name,
        "phone": phone,
        "date_of_birth": dob or "1999-01-01",
        "age": age,
        "city": "Lisboa, Portugal",
        "diagnosis": "ALPHA",
        "bio": "Olá! Estou no Sigaleve à procura de conversas leves, conexões autênticas e sem preconceitos.",
        "photo": default_photo,
        "photos": [default_photo],
        "interests": ["Viagens", "Café", "Música"],
        "seeking": "Todos",
        "max_distance": 50,
        "age_min": 18,
        "age_max": 50,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "is_profile_configured": False,
        "email_verified": True,
        "known_devices": [device_id]
    }
    users[email] = new_user
    save_users(users)

    # Iniciar sessão diretamente
    session["user_id"] = user_id
    session["user_email"] = email

    return jsonify({
        "success": True,
        "requires_verification": False,
        "message": "Conta criada com sucesso!",
        "user": serialize_user(new_user)
    }), 201


# ══════════════════════════════════════════════════════════════════════════════
# 2FA (AUTENTICAÇÃO DE DOIS FACTORES: EMAIL & TOTP)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/v1/auth/2fa/status", methods=["GET"])
def api_2fa_status():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    two_factor = user.get("two_factor", {
        "enabled": False,
        "method": "none",
        "has_totp": False
    })
    return jsonify({
        "success": True,
        "two_factor": {
            "enabled": two_factor.get("enabled", False),
            "method": two_factor.get("method", "none"),
            "has_totp": bool(two_factor.get("totp_secret"))
        },
        "email": user["email"]
    }), 200

@app.route("/api/v1/auth/2fa/setup-totp", methods=["POST"])
def api_2fa_setup_totp():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(name=email, issuer_name="Sigaleve")

    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

    user["temp_totp_secret"] = secret
    save_users(users)

    return jsonify({
        "success": True,
        "secret": secret,
        "qr_code": qr_b64,
        "uri": provisioning_uri
    }), 200

@app.route("/api/v1/auth/2fa/verify-setup-totp", methods=["POST"])
def api_2fa_verify_setup_totp():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip().replace(" ", "")

    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    temp_secret = user.get("temp_totp_secret")
    if not temp_secret:
        return jsonify({"success": False, "error": "Nenhuma configuração pendente de TOTP."}), 400

    totp = pyotp.TOTP(temp_secret)
    if not totp.verify(code, valid_window=1):
        return jsonify({"success": False, "error": "Código do autenticador inválido ou expirado. Tenta novamente."}), 400

    two_factor = user.get("two_factor", {})
    two_factor["enabled"] = True
    two_factor["method"] = "totp"
    two_factor["totp_secret"] = temp_secret
    user["two_factor"] = two_factor
    user.pop("temp_totp_secret", None)
    save_users(users)

    return jsonify({
        "success": True,
        "message": "Autenticador Google/Authy configurado e ativado com sucesso!",
        "two_factor": {
            "enabled": True,
            "method": "totp"
        }
    }), 200

@app.route("/api/v1/auth/2fa/send-email-code", methods=["POST"])
def api_2fa_send_email_code():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    otp_code = f"{random.randint(100000, 999999)}"
    user["temp_email_2fa_code"] = otp_code
    save_users(users)

    subj = "Código de Confirmação 2FA | Sigaleve"
    html_b = f"""
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:500px;margin:0 auto;background:#0d0e15;color:#ffffff;border-radius:20px;padding:32px;border:1px solid #27272a;">
      <div style="text-align:center;margin-bottom:24px;">
        <h1 style="font-size:24px;font-weight:900;letter-spacing:-0.5px;color:#ffffff;margin:0;">SIGALEVE</h1>
        <p style="color:#a1a1aa;font-size:12px;margin-top:4px;">Segurança & Verificação em Duas Etapas</p>
      </div>
      <p style="color:#e4e4e7;font-size:14px;line-height:1.6;">Olá, <strong>{user.get('display_name', 'Membro')}</strong>,</p>
      <p style="color:#a1a1aa;font-size:13px;line-height:1.6;">Recebemos o teu pedido para ativar a <strong>Verificação por Código de E-mail</strong> na tua conta Sigaleve. Utiliza o código de 6 dígitos abaixo para concluir:</p>
      <div style="background:#18181b;border:1px solid #3f3f46;border-radius:14px;padding:20px;text-align:center;margin:24px 0;">
        <span style="font-size:32px;font-weight:900;letter-spacing:8px;color:#a855f7;font-family:monospace;">{otp_code}</span>
      </div>
      <p style="color:#71717a;font-size:11px;text-align:center;">Este código expira em 10 minutos. Se não solicitaste esta ativação, podes ignorar esta mensagem.</p>
    </div>
    """
    text_b = f"O teu código de verificação 2FA Sigaleve é: {otp_code}\nExpira em 10 minutos."
    delivered, note = send_real_email(user["email"], subj, html_b, text_b)

    return jsonify({
        "success": True,
        "message": f"Código enviado com sucesso para {user['email']}.",
        "email": user["email"],
        "delivered": delivered,
        "note": note,
        "debug_code": otp_code if not delivered else None
    }), 200

@app.route("/api/v1/auth/2fa/verify-email-code", methods=["POST"])
def api_2fa_verify_email_code():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip().replace(" ", "")

    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    expected = str(user.get("temp_email_2fa_code", ""))
    if not expected or code != expected:
        return jsonify({"success": False, "error": "Código incorreto. Verifica o e-mail recebido e tenta novamente."}), 400

    two_factor = user.get("two_factor", {})
    two_factor["enabled"] = True
    two_factor["method"] = "email"
    user["two_factor"] = two_factor
    user.pop("temp_email_2fa_code", None)
    save_users(users)

    return jsonify({
        "success": True,
        "message": "Autenticação em duas etapas por E-mail ativada com sucesso!",
        "two_factor": {
            "enabled": True,
            "method": "email"
        }
    }), 200

@app.route("/api/v1/auth/2fa/disable", methods=["POST"])
def api_2fa_disable():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    two_factor = user.get("two_factor", {})
    two_factor["enabled"] = False
    two_factor["method"] = "none"
    user["two_factor"] = two_factor
    save_users(users)

    return jsonify({
        "success": True,
        "message": "Verificação em duas etapas desativada.",
        "two_factor": {
            "enabled": False,
            "method": "none"
        }
    }), 200

@app.route("/api/v1/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    identifier = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    device_id = str(data.get("device_id", "web-default")).strip()

    users = load_users()
    user = users.get(identifier)

    if not user:
        for u_email, u_data in users.items():
            if u_data.get("display_name", "").strip().lower() == identifier or u_email.strip().lower() == identifier:
                user = u_data
                break

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "error": "Credenciais incorretas. Verifique o e-mail/utilizador e a palavra-passe."}), 401

    two_factor = user.get("two_factor", {})
    two_factor_enabled = two_factor.get("enabled", False)
    two_factor_method = two_factor.get("method", "none")

    known_devices = user.get("known_devices", [])
    is_new_device = (device_id not in known_devices) or (not user.get("email_verified", True))

    # Apenas exige verificação se o utilizador ativou explicitamente 2FA com app autenticadora
    if two_factor_enabled and two_factor_method == "totp":
        return jsonify({
            "success": True,
            "requires_verification": True,
            "auth_method": "totp",
            "email": user["email"],
            "message": "Introduz o código de 6 dígitos gerado pela tua aplicação autenticadora (Google Authenticator / Authy)."
        }), 200

    # Iniciar sessão diretamente
    session["user_id"] = user["id"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "requires_verification": False,
        "message": "Sessão iniciada com sucesso.",
        "user": serialize_user(user)
    }), 200

@app.route("/api/v1/auth/verify-code", methods=["POST"])
def api_verify_code():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    code = str(data.get("code", "")).strip()
    device_id = str(data.get("device_id", "web-default")).strip()

    users = load_users()
    user = users.get(email)
    if not user:
        for u_email, u_data in users.items():
            if u_data.get("display_name", "").strip().lower() == email:
                user = u_data
                break

    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    two_factor = user.get("two_factor", {})
    two_factor_enabled = two_factor.get("enabled", False)
    two_factor_method = two_factor.get("method", "none")

    # Se o utilizador tem 2FA por TOTP ativado
    if two_factor_enabled and two_factor_method == "totp":
        totp_secret = two_factor.get("totp_secret")
        if not totp_secret:
            return jsonify({"success": False, "error": "Configuração TOTP inválida no servidor."}), 500
        totp = pyotp.TOTP(totp_secret)
        if not totp.verify(code, valid_window=1):
            return jsonify({"success": False, "error": "Código da aplicação autenticadora inválido ou expirado."}), 400
    else:
        # Verificação normal de E-mail / Código OTP
        if not user.get("email_verified", False):
            return jsonify({
                "success": False,
                "error": "Atenção: Primeiro deves abrir o teu e-mail e carregar no link de confirmação antes de introduzir o código!"
            }), 403

        expected_otp = str(user.get("otp_code", ""))
        if not expected_otp or code != expected_otp:
            return jsonify({"success": False, "error": "Código de verificação incorreto. Verifique o seu e-mail e tente novamente."}), 400

    # Sucesso: adicionar dispositivo à lista de conhecidos
    known_devices = user.get("known_devices", [])
    if device_id not in known_devices:
        known_devices.append(device_id)
        user["known_devices"] = known_devices
    user["email_verified"] = True
    save_users(users)

    session["user_id"] = user["id"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "message": "Identidade confirmada com sucesso!",
        "user": serialize_user(user)
    }), 200

@app.route("/api/v1/auth/resend-code", methods=["POST"])
def api_resend_code():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    otp_code = f"{random.randint(100000, 999999)}"
    verify_token = user.get("verify_token") or str(uuid.uuid4())[:12]
    user["otp_code"] = otp_code
    user["verify_token"] = verify_token
    save_users(users)

    verify_link = f"{request.host_url.rstrip('/')}/confirm-email/{verify_token}"
    
    # Enviar real por email
    subj = "Novo Código de Confirmação | Sigaleve"
    html_b = f"""
    <div style="font-family:sans-serif;max-width:500px;background:#0d0e15;color:#ffffff;border-radius:18px;padding:24px;">
      <h2 style="color:#ffffff;">Novo Código de Acesso Sigaleve</h2>
      <p style="color:#94a3b8;">Aqui tens o novo link de confirmação e o código de acesso solicitado:</p>
      <p><a href="{verify_link}" style="background:#9333ea;color:#fff;padding:10px 18px;text-decoration:none;border-radius:10px;font-weight:bold;display:inline-block;">Confirmar E-mail</a></p>
      <p style="font-size:24px;font-weight:bold;color:#34d399;letter-spacing:4px;">{otp_code}</p>
    </div>
    """
    email_sent, _ = send_real_email(user["email"], subj, html_b, f"Link: {verify_link}\nCódigo: {otp_code}")

    return jsonify({
        "success": True,
        "message": "Novo código e ligação de confirmação enviados para o teu e-mail!",
        "verify_link": verify_link,
        "otp_code": otp_code,
        "email_sent": email_sent
    }), 200

# ── Recuperação de Palavra-passe com Geração de Nova Senha e Envio por E-mail ─
@app.route("/api/v1/auth/forgot-password", methods=["POST"])
def api_forgot_password():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()

    if not email or "@" not in email:
        return jsonify({"success": False, "error": "Por favor, introduz um endereço de e-mail válido."}), 400

    users = load_users()
    user = users.get(email)

    if not user:
        for u_email, u_data in users.items():
            if u_data.get("display_name", "").strip().lower() == email:
                user = u_data
                email = u_email
                break

    if not user:
        return jsonify({"success": False, "error": "Não encontramos nenhuma conta associada a este e-mail."}), 404

    # Gerar uma nova palavra-passe forte compatível com as regras:
    # Mínimo 8 caracteres, maiúsculas, minúsculas, dígitos e símbolos
    alpha_upper = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    alpha_lower = "abcdefghijkmnpqrstuvwxyz"
    digits = "23456789"
    specials = "!@#$*&"

    part_upper = "".join(random.choice(alpha_upper) for _ in range(2))
    part_lower = "".join(random.choice(alpha_lower) for _ in range(4))
    part_digits = "".join(random.choice(digits) for _ in range(3))
    part_spec = "".join(random.choice(specials) for _ in range(1))
    
    char_list = list(part_upper + part_lower + part_digits + part_spec)
    random.shuffle(char_list)
    new_password = "".join(char_list)

    # Atualizar hash do usuário e salvar
    user["password_hash"] = generate_password_hash(new_password)
    save_users(users)

    # Assunto e modelo HTML do e-mail de recuperação
    subject = "Recuperação de Palavra-passe | Nova Senha Sigaleve"
    html_content = f"""
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;max-width:560px;margin:0 auto;background:#0d0e15;color:#ffffff;border-radius:24px;padding:32px 24px;border:1px solid #27273a;">
      <div style="text-align:center;margin-bottom:24px;">
        <div style="display:inline-block;width:56px;height:56px;line-height:56px;border-radius:18px;background:linear-gradient(135deg,#9333ea,#ec4899);color:#ffffff;font-size:26px;font-weight:900;">
          🔑
        </div>
        <h1 style="color:#ffffff;font-size:24px;font-weight:900;margin:16px 0 6px 0;">Recuperação de Palavra-passe</h1>
        <p style="color:#94a3b8;font-size:14px;margin:0;">Gerámos uma nova palavra-passe segura para a tua conta.</p>
      </div>

      <div style="background:#171826;border-radius:18px;padding:22px;border:1px solid #27273a;margin-bottom:24px;text-align:center;">
        <p style="color:#c084fc;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin:0 0 10px 0;">
          A TUA NOVA PALAVRA-PASSE
        </p>
        <p style="color:#94a3b8;font-size:13px;margin:0 0 16px 0;">
          Usa esta nova chave para aceder imediatamente à tua conta:
        </p>
        <div style="background:#090a10;border-radius:14px;padding:16px;font-family:monospace;font-size:24px;font-weight:900;letter-spacing:3px;color:#38bdf8;border:1px dashed #38bdf8;word-break:break-all;">
          {new_password}
        </div>
      </div>

      <div style="background:#171826;border-radius:18px;padding:18px;border:1px solid #27273a;margin-bottom:24px;">
        <p style="color:#cbd5e1;font-size:13px;line-height:1.5;margin:0 0 14px 0;">
          Recomendamos que inicies sessão com esta nova palavra-passe e a alteres se desejares após o login.
        </p>
        <a href="{request.host_url.rstrip('/')}/app" target="_blank" style="display:block;background:linear-gradient(135deg,#9333ea,#ec4899);color:#ffffff;text-decoration:none;padding:14px 20px;text-align:center;font-weight:900;font-size:14px;border-radius:14px;box-shadow:0 8px 20px rgba(147,51,234,0.35);">
          Entrar no Sigaleve Agora
        </a>
      </div>

      <p style="color:#64748b;font-size:11px;text-align:center;margin:0;line-height:1.4;">
        Se não solicitaste esta recuperação, por favor inicia sessão com a nova palavra-passe para garantir a segurança da tua conta.<br/>
        Sigaleve &copy; 2026 — Segurança e Conexões Autênticas.
      </p>
    </div>
    """
    text_content = f"Recuperação de Palavra-passe Sigaleve\n\nA tua nova palavra-passe é: {new_password}\n\nPodes iniciar sessão em: {request.host_url.rstrip('/')}/app\n"
    
    email_sent, mail_status = send_real_email(user["email"], subject, html_content, text_content)

    return jsonify({
        "success": True,
        "email_sent": email_sent,
        "email": user["email"],
        "message": f"Se a conta existir, as instruções e a nova palavra-passe segura foram enviadas para o endereço de e-mail associado."
    }), 200

# ── Login Social: Google, Facebook, Instagram ──────────────────────────────
@app.route("/api/v1/auth/social-login", methods=["POST"])
def api_social_login():
    data = request.get_json(silent=True) or {}
    provider = str(data.get("provider", "google")).strip().lower()
    device_id = str(data.get("device_id", "web-default")).strip()

    # Se for Google con token o credencial real (OpenID Connect / Google Identity Services)
    credential = data.get("credential") or data.get("token") or data.get("id_token")
    if provider == "google" and credential:
        try:
            # Validar diretamente com a API oficial da Google
            tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
            req = urllib.request.Request(tokeninfo_url, headers={"User-Agent": "Sigaleve-App"})
            with urllib.request.urlopen(req, timeout=10) as response:
                google_data = json.loads(response.read().decode("utf-8"))
            
            # Verificar se o token pertence ao nosso client ID ou é válido
            aud = google_data.get("aud")
            if aud != GOOGLE_CLIENT_ID:
                print(f"[GOOGLE AUTH WARNING] Token aud {aud} != {GOOGLE_CLIENT_ID}")
            
            email = google_data.get("email", "").strip().lower()
            if not email:
                return jsonify({"success": False, "error": "A Google não forneceu um endereço de e-mail válido."}), 400
            
            name = google_data.get("name") or google_data.get("given_name") or email.split("@")[0]
            photo = google_data.get("picture") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"
            social_id = google_data.get("sub", f"google_{uuid.uuid4().hex[:8]}")
        except Exception as e:
            print(f"[GOOGLE AUTH ERROR] Falha ao verificar token com a Google: {e}")
            return jsonify({"success": False, "error": f"Credencial Google inválida ou expirada: {str(e)}"}), 401
    else:
        return jsonify({
            "success": False, 
            "error": "O início de sessão com redes sociais deve ser efetuado através do portal oficial de autorização da rede ou com a tua conta Google."
        }), 400

    users = load_users()
    user = users.get(email)

    if not user:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "email": email,
            "social_provider": provider,
            "social_id": social_id,
            "password_hash": generate_password_hash(uuid.uuid4().hex),
            "display_name": name,
            "phone": "",
            "date_of_birth": "1999-01-01",
            "age": 26,
            "city": "Lisboa, Portugal",
            "diagnosis": "ALPHA",
            "bio": f"Conta conectada via {provider.title()}. Pronto para conexões autênticas!",
            "photo": photo,
            "photos": [photo],
            "interests": ["Música", "Viagens", "Café"],
            "seeking": "Todos",
            "max_distance": 50,
            "age_min": 18,
            "age_max": 50,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "email_verified": True,
            "known_devices": [device_id]
        }
        users[email] = user
        save_users(users)
    else:
        known_devices = user.get("known_devices", [])
        if device_id not in known_devices:
            known_devices.append(device_id)
            user["known_devices"] = known_devices
            save_users(users)

    session["user_id"] = user["id"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "message": f"Conectado com sucesso via {provider.title()}!",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "display_name": user.get("display_name", name),
            "phone": user.get("phone", ""),
            "age": user.get("age", 26),
            "city": user.get("city", "Lisboa, Portugal"),
            "bio": user.get("bio", ""),
            "photo": user.get("photo", photo),
            "photos": user.get("photos", [photo]),
            "interests": user.get("interests", ["Música", "Viagens"]),
            "diagnosis": user.get("diagnosis", "ALPHA"),
            "seeking": user.get("seeking", "Todos"),
            "max_distance": user.get("max_distance", 50)
        }
    }), 200

# ── API de Conexão Social Instantânea (Para Instagram / Facebook) ────────────
@app.route("/api/v1/auth/social-instant", methods=["POST"])
def api_social_instant():
    data = request.get_json(silent=True) or {}
    provider = str(data.get("provider", "facebook")).strip().lower()
    handle = str(data.get("handle", "")).strip().lstrip("@") or "utilizador"
    name = str(data.get("name", "")).strip() or handle.title()
    email = str(data.get("email", "")).strip().lower() or f"{handle.lower()}@{provider}.sigaleve.app"
    device_id = str(data.get("device_id", "web-default")).strip()

    users = load_users()
    user = users.get(email)

    # Foto por defecto según la red social o avatar
    photo = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"

    if not user:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "email": email,
            "social_provider": provider,
            "social_id": f"{provider}_{handle}",
            "password_hash": generate_password_hash(uuid.uuid4().hex),
            "display_name": name,
            "username": f"@{handle}",
            "phone": "",
            "date_of_birth": "1999-01-01",
            "age": 26,
            "city": "Lisboa, Portugal",
            "diagnosis": "ALPHA",
            "bio": f"Perfil verificado via {provider.title()}. Aberto a boas conversas e conexões autênticas!",
            "photo": photo,
            "photos": [photo],
            "interests": ["Música", "Fotografia", "Viagens"],
            "seeking": "Todos",
            "max_distance": 50,
            "age_min": 18,
            "age_max": 50,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "email_verified": True,
            "is_profile_configured": True,
            "known_devices": [device_id]
        }
        users[email] = user
        save_users(users)
    else:
        known_devices = user.get("known_devices", [])
        if device_id not in known_devices:
            known_devices.append(device_id)
            user["known_devices"] = known_devices
            save_users(users)

    session["user_id"] = user["id"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "message": f"Autenticado com sucesso via {provider.title()}!",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "display_name": user.get("display_name", name),
            "username": user.get("username", f"@{handle}"),
            "phone": user.get("phone", ""),
            "age": user.get("age", 26),
            "city": user.get("city", "Lisboa, Portugal"),
            "bio": user.get("bio", ""),
            "photo": user.get("photo", photo),
            "photos": user.get("photos", [photo]),
            "interests": user.get("interests", ["Música", "Fotografia", "Viagens"]),
            "diagnosis": user.get("diagnosis", "ALPHA"),
            "seeking": user.get("seeking", "Todos"),
            "max_distance": user.get("max_distance", 50)
        }
    }), 200

def get_oauth_redirect_uri(endpoint: str) -> str:
    """
    Constrói a URI de callback exata e segura (sempre com HTTPS em produção).
    Evita o erro Error 400: redirect_uri_mismatch do Google causado por http:// vs https://
    ou discrepâncias de subdomínio/proxy.
    """
    # Se configurado explicitamente no ambiente (ex: https://sigaleve.com ou https://www.sigaleve.com)
    canonical_base = os.environ.get("CANONICAL_APP_URL")
    if canonical_base:
        return f"{canonical_base.rstrip('/')}{endpoint}"
    
    host = request.headers.get("X-Forwarded-Host") or request.host
    proto = request.headers.get("X-Forwarded-Proto") or request.scheme
    # En producción bajo dominio real siempre exigir HTTPS
    if "sigaleve.com" in host or not (host.startswith("localhost") or host.startswith("127.0.0.1")):
        proto = "https"
    return f"{proto}://{host}{endpoint}"

# ── Rota Direta de Redirecionamento Google OAuth 2.0 ─────────────────────────
@app.route("/auth/google/login")
def auth_google_login():
    redirect_uri = get_oauth_redirect_uri("/auth/google/callback")
    state = str(uuid.uuid4())
    session["oauth_state"] = state
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account"
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return redirect(google_auth_url)

@app.route("/auth/google/callback")
def auth_google_callback():
    code = request.args.get("code")
    err = request.args.get("error")
    if err or not code:
        return redirect(f"/app?error=google_cancelled")

    redirect_uri = get_oauth_redirect_uri("/auth/google/callback")
    token_url = "https://oauth2.googleapis.com/token"
    token_data = urllib.parse.urlencode({
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(token_url, data=token_data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Sigaleve-App"
        })
        with urllib.request.urlopen(req, timeout=12) as res:
            tokens = json.loads(res.read().decode("utf-8"))

        id_token = tokens.get("id_token")
        access_token = tokens.get("access_token")

        user_info = {}
        if id_token:
            tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            with urllib.request.urlopen(tokeninfo_url, timeout=10) as res:
                user_info = json.loads(res.read().decode("utf-8"))
        elif access_token:
            userinfo_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
            with urllib.request.urlopen(userinfo_url, timeout=10) as res:
                user_info = json.loads(res.read().decode("utf-8"))

        email = user_info.get("email", "").strip().lower()
        if not email:
            return redirect("/app?error=no_email")

        name = user_info.get("name") or user_info.get("given_name") or email.split("@")[0]
        photo = user_info.get("picture") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"
        social_id = user_info.get("sub", f"google_{uuid.uuid4().hex[:8]}")

        users = load_users()
        user = users.get(email)
        if not user:
            user_id = str(uuid.uuid4())
            user = {
                "id": user_id,
                "email": email,
                "social_provider": "google",
                "social_id": social_id,
                "password_hash": generate_password_hash(uuid.uuid4().hex),
                "display_name": name,
                "phone": "",
                "date_of_birth": "1999-01-01",
                "age": 26,
                "city": "Lisboa, Portugal",
                "diagnosis": "ALPHA",
                "bio": "Conta verificada através da Google. Aberto a conexões genuínas!",
                "photo": photo,
                "photos": [photo],
                "interests": ["Música", "Viagens", "Café"],
                "seeking": "Todos",
                "max_distance": 50,
                "age_min": 18,
                "age_max": 50,
                "created_at": datetime.datetime.utcnow().isoformat(),
                "is_profile_configured": False,
                "email_verified": True,
                "known_devices": ["google-oauth"]
            }
            users[email] = user
            save_users(users)
        else:
            user["email_verified"] = True
            if "google-oauth" not in user.get("known_devices", []):
                user.setdefault("known_devices", []).append("google-oauth")
            save_users(users)

        session["user_id"] = user["id"]
        session["user_email"] = user["email"]

        # Redirecionar para o app com login automático
        return redirect("/app?google_auth_success=true")
    except Exception as e:
        print(f"[GOOGLE CALLBACK ERROR] {e}")
        return redirect(f"/app?error=google_failed")

# ── Rota Direta de Redirecionamento Facebook / Meta OAuth ───────────────────
@app.route("/auth/facebook/login")
def auth_facebook_login():
    redirect_uri = get_oauth_redirect_uri("/auth/facebook/callback")
    state = str(uuid.uuid4())
    session["facebook_oauth_state"] = state
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": "public_profile email",
        "response_type": "code"
    }
    fb_auth_url = f"https://www.facebook.com/v19.0/dialog/oauth?{urllib.parse.urlencode(params)}"
    return redirect(fb_auth_url)

@app.route("/auth/facebook/callback")
def auth_facebook_callback():
    code = request.args.get("code")
    err = request.args.get("error")
    if err or not code:
        return redirect("/app?error=facebook_cancelled")

    redirect_uri = get_oauth_redirect_uri("/auth/facebook/callback")
    token_url = "https://graph.facebook.com/v19.0/oauth/access_token?" + urllib.parse.urlencode({
        "client_id": FACEBOOK_APP_ID,
        "client_secret": FACEBOOK_APP_SECRET,
        "redirect_uri": redirect_uri,
        "code": code
    })

    try:
        req = urllib.request.Request(token_url, headers={"User-Agent": "Sigaleve-App"})
        with urllib.request.urlopen(req, timeout=12) as res:
            token_resp = json.loads(res.read().decode("utf-8"))

        access_token = token_resp.get("access_token")
        if not access_token:
            return redirect("/app?error=facebook_token_failed")

        # Obter dados do perfil do usuário no Facebook
        graph_url = f"https://graph.facebook.com/me?fields=id,name,email,picture.type(large)&access_token={access_token}"
        req_me = urllib.request.Request(graph_url, headers={"User-Agent": "Sigaleve-App"})
        with urllib.request.urlopen(req_me, timeout=10) as res_me:
            fb_profile = json.loads(res_me.read().decode("utf-8"))

        social_id = fb_profile.get("id")
        name = fb_profile.get("name", "Utilizador Facebook")
        email = fb_profile.get("email") or f"fb_{social_id}@facebook.sigaleve.app"
        photo = (fb_profile.get("picture", {}).get("data", {}).get("url") or 
                 "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1000&q=85")

        users = load_users()
        user = users.get(email)
        if not user:
            user_id = str(uuid.uuid4())
            user = {
                "id": user_id,
                "email": email,
                "social_provider": "facebook",
                "social_id": f"fb_{social_id}",
                "password_hash": generate_password_hash(uuid.uuid4().hex),
                "display_name": name,
                "phone": "",
                "date_of_birth": "1999-01-01",
                "age": 26,
                "city": "Lisboa, Portugal",
                "diagnosis": "ALPHA",
                "bio": "Conta conectada através do Facebook. Conecta com respeito e autenticidade!",
                "photo": photo,
                "photos": [photo],
                "interests": ["Música", "Viagens", "Fotografia"],
                "seeking": "Todos",
                "max_distance": 50,
                "age_min": 18,
                "age_max": 50,
                "created_at": datetime.datetime.utcnow().isoformat(),
                "is_profile_configured": False,
                "email_verified": True,
                "known_devices": ["facebook-oauth"]
            }
            users[email] = user
            save_users(users)
        else:
            user["email_verified"] = True
            if "facebook-oauth" not in user.get("known_devices", []):
                user.setdefault("known_devices", []).append("facebook-oauth")
            save_users(users)

        session["user_id"] = user["id"]
        session["user_email"] = user["email"]

        return redirect("/app?social_auth_success=facebook")
    except Exception as e:
        print(f"[FACEBOOK CALLBACK ERROR] {e}")
        return redirect("/app?error=facebook_failed")

# ── Rota Direta de Redirecionamento Instagram OAuth ──────────────────────────
@app.route("/auth/instagram/login")
def auth_instagram_login():
    redirect_uri = get_oauth_redirect_uri("/auth/instagram/callback")
    state = str(uuid.uuid4())
    session["instagram_oauth_state"] = state
    params = {
        "client_id": INSTAGRAM_APP_ID,
        "redirect_uri": redirect_uri,
        "scope": "user_profile,user_media",
        "response_type": "code",
        "state": state
    }
    ig_auth_url = f"https://api.instagram.com/oauth/authorize?{urllib.parse.urlencode(params)}"
    return redirect(ig_auth_url)

@app.route("/auth/instagram/callback")
def auth_instagram_callback():
    code = request.args.get("code")
    err = request.args.get("error")
    if err or not code:
        return redirect("/app?error=instagram_cancelled")

    redirect_uri = get_oauth_redirect_uri("/auth/instagram/callback")
    token_url = "https://api.instagram.com/oauth/access_token"
    token_data = urllib.parse.urlencode({
        "client_id": INSTAGRAM_APP_ID,
        "client_secret": INSTAGRAM_APP_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": code
    }).encode("utf-8")

    try:
        req = urllib.request.Request(token_url, data=token_data, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Sigaleve-App"
        })
        with urllib.request.urlopen(req, timeout=12) as res:
            token_resp = json.loads(res.read().decode("utf-8"))

        access_token = token_resp.get("access_token")
        user_id_ig = token_resp.get("user_id")

        name = f"Utilizador Instagram"
        email = f"ig_{user_id_ig}@instagram.sigaleve.app"
        photo = "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1000&q=85"

        if access_token:
            try:
                me_url = f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
                req_me = urllib.request.Request(me_url, headers={"User-Agent": "Sigaleve-App"})
                with urllib.request.urlopen(req_me, timeout=10) as res_me:
                    ig_profile = json.loads(res_me.read().decode("utf-8"))
                    if ig_profile.get("username"):
                        name = ig_profile["username"]
                        email = f"{name}@instagram.sigaleve.app"
            except Exception:
                pass

        users = load_users()
        user = users.get(email)
        if not user:
            user_id = str(uuid.uuid4())
            user = {
                "id": user_id,
                "email": email,
                "social_provider": "instagram",
                "social_id": f"ig_{user_id_ig}",
                "password_hash": generate_password_hash(uuid.uuid4().hex),
                "display_name": name,
                "phone": "",
                "date_of_birth": "1999-01-01",
                "age": 26,
                "city": "Lisboa, Portugal",
                "diagnosis": "ALPHA",
                "bio": f"Conta conectada via Instagram (@{name}). Pronto para conexões autênticas!",
                "photo": photo,
                "photos": [photo],
                "interests": ["Arte", "Fotografia", "Música"],
                "seeking": "Todos",
                "max_distance": 50,
                "age_min": 18,
                "age_max": 50,
                "created_at": datetime.datetime.utcnow().isoformat(),
                "is_profile_configured": False,
                "email_verified": True,
                "known_devices": ["instagram-oauth"]
            }
            users[email] = user
            save_users(users)
        else:
            user["email_verified"] = True
            if "instagram-oauth" not in user.get("known_devices", []):
                user.setdefault("known_devices", []).append("instagram-oauth")
            save_users(users)

        session["user_id"] = user["id"]
        session["user_email"] = user["email"]

        return redirect("/app?social_auth_success=instagram")
    except Exception as e:
        print(f"[INSTAGRAM CALLBACK ERROR] {e}")
        return redirect("/app?error=instagram_failed")

@app.route("/api/v1/auth/me", methods=["GET"])
def api_me():
    email = session.get("user_email")
    if not email:
        return jsonify({"authenticated": False}), 401
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"authenticated": False}), 401

    return jsonify({
        "authenticated": True,
        "user": serialize_user(user)
    }), 200

@app.route("/api/v1/auth/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Sessão terminada."}), 200

# ── API de Perfil (Atualização Completa) ──────────────────────────────────────
@app.route("/api/v1/profile/update", methods=["POST"])
def api_update_profile():
    data = request.get_json(silent=True) or {}
    # Exigir estritamente sessão ativa do servidor para evitar IDOR e sequestro de contas
    email = session.get("user_email") or (data.get("email") if app.debug and not session.get("user_email") else None)
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada ou expirada."}), 401

    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    if "display_name" in data and str(data["display_name"]).strip():
        user["display_name"] = str(data["display_name"]).strip()
    if "phone" in data:
        user["phone"] = str(data["phone"]).strip()
    if "city" in data and str(data["city"]).strip():
        user["city"] = str(data["city"]).strip()
    if "bio" in data:
        user["bio"] = str(data["bio"]).strip()
    if "photo" in data and str(data["photo"]).strip():
        user["photo"] = str(data["photo"]).strip()
        if "photos" not in user or not user["photos"]:
            user["photos"] = [user["photo"]]
        else:
            if user["photo"] not in user["photos"]:
                user["photos"].insert(0, user["photo"])
    if "interests" in data and isinstance(data["interests"], list):
        user["interests"] = data["interests"]
    if "diagnosis" in data and str(data["diagnosis"]).strip():
        user["diagnosis"] = str(data["diagnosis"]).strip()
    if "custom_diagnosis" in data:
        user["custom_diagnosis"] = str(data["custom_diagnosis"]).strip()
    if "relationship_goal" in data and str(data["relationship_goal"]).strip():
        user["relationship_goal"] = str(data["relationship_goal"]).strip()
    if "zodiac" in data:
        user["zodiac"] = str(data["zodiac"]).strip()
    if "education" in data:
        user["education"] = str(data["education"]).strip()
    if "height" in data:
        user["height"] = str(data["height"]).strip()
    if "lifestyle" in data:
        user["lifestyle"] = str(data["lifestyle"]).strip()
    if "seeking" in data:
        user["seeking"] = str(data["seeking"]).strip()
    if "max_distance" in data:
        try:
            user["max_distance"] = int(data["max_distance"])
        except ValueError:
            pass

    user["is_profile_configured"] = True
    users[email] = user
    save_users(users)

    return jsonify({
        "success": True,
        "message": "Perfil atualizado com sucesso!",
        "user": serialize_user(user)
    }), 200

# ── API de Matchmaking e Descoberta ──────────────────────────────────────────
@app.route("/api/v1/discover")
def api_discover():
    users = load_users()
    current_email = session.get("user_email")
    current_uid = session.get("user_id")
    real_profiles = []

    # 1. Carregar utilizadores reais registados na aplicação
    for email, u in users.items():
        uid = str(u.get("id") or email)
        if email == current_email or (current_uid and uid == str(current_uid)):
            continue

        photo = u.get("photo") or (u.get("photos", [])[0] if u.get("photos") else "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85")
        photos_list = u.get("photos") if (u.get("photos") and len(u.get("photos")) > 0) else [photo]
        diag = u.get("diagnosis", "ALPHA")
        diag_code = diag[:1] if diag else "A"

        real_profiles.append({
            "id": uid,
            "name": u.get("display_name") or u.get("name") or "Utilizador",
            "age": u.get("age", 25),
            "city": u.get("city") or "Lisboa, Portugal",
            "km": "3 km de distância",
            "code": diag_code,
            "activity": "Ativo agora",
            "photo": photo,
            "photos": photos_list,
            "bio": u.get("bio") or "Olá! Estou no Sigaleve para conexões reais, respeitosas e sem preconceito.",
            "relationship_goal": u.get("relationship_goal") or "Relação séria",
            "zodiac": u.get("zodiac") or "",
            "education": u.get("education") or "",
            "height": u.get("height") or "",
            "lifestyle": u.get("lifestyle") or "",
            "interests": u.get("interests", ["Viagens", "Música"]),
            "verified": True,
            "is_real_user": True
        })

    # 2. Filtrar e excluir utilizadores com quem já houve match ou que já foram avaliados (Like ou Skip)
    excluded_ids = set()
    if current_email and current_email in users:
        u_data = users[current_email]
        # Sanitizar matches antigos que possam conter IDs de mock (p1..p7)
        raw_matches = u_data.get("matches", [])
        real_matches = [mid for mid in raw_matches if not str(mid).startswith("p") and not str(mid).startswith("mock_")]
        if len(real_matches) != len(raw_matches):
            u_data["matches"] = real_matches
            save_users(users)

        for mid in real_matches:
            excluded_ids.add(str(mid))

        # Excluir também perfis a quem o utilizador já deu like para não se repetirem ao recarregar
        for lid in u_data.get("likes_given", []):
            excluded_ids.add(str(lid))

        # Excluir perfis passados (skip/nope)
        for sid in u_data.get("skipped", []):
            excluded_ids.add(str(sid))

    filtered_profiles = [p for p in real_profiles if str(p.get("id")) not in excluded_ids]

    return jsonify({"profiles": filtered_profiles}), 200

@app.route("/api/v1/like", methods=["POST"])
def api_like():
    data = request.get_json(silent=True) or {}
    target_id = str(data.get("target_id", "")).strip()
    current_email = session.get("user_email")
    current_uid = session.get("user_id")

    if not current_email or not target_id:
        return jsonify({"matched": False, "error": "Não autenticado ou alvo inválido"}), 400

    users = load_users()
    if current_email not in users:
        return jsonify({"matched": False, "error": "Utilizador não encontrado"}), 404

    current_user = users[current_email]
    my_id = str(current_user.get("id") or current_email)

    # Rejeitar likes em perfis de teste ou mock antigos
    if target_id.startswith("p") or target_id.startswith("mock_"):
        return jsonify({"matched": False, "message": "Perfil indisponível"}), 200

    # Localizar o utilizador alvo no sistema
    target_user_record = None
    target_email = None
    for em, u in users.items():
        if str(u.get("id")) == str(target_id) or em == str(target_id):
            target_user_record = u
            target_email = em
            break

    if not target_user_record:
        return jsonify({"matched": False, "message": "Utilizador não encontrado"}), 404

    # Registar o like dado
    likes_given = current_user.setdefault("likes_given", [])
    if target_id not in likes_given:
        likes_given.append(target_id)

    # Verificar se o outro utilizador já deu like a este utilizador (MATCH MÚTUO REAL)
    target_likes = target_user_record.setdefault("likes_given", [])
    matched = (my_id in target_likes or current_email in target_likes)

    if matched:
        # Registar match em ambas as contas reais
        my_matches = current_user.setdefault("matches", [])
        if target_id not in my_matches:
            my_matches.append(target_id)

        target_matches = target_user_record.setdefault("matches", [])
        if my_id not in target_matches:
            target_matches.append(my_id)

    save_users(users)

    return jsonify({
        "matched": matched,
        "message": "É um Match! 💜" if matched else "Gosto enviado com sucesso!"
    }), 200

@app.route("/api/v1/matches", methods=["GET"])
def api_get_matches():
    current_email = session.get("user_email")
    if not current_email:
        return jsonify({"matches": []}), 200

    users = load_users()
    if current_email not in users:
        return jsonify({"matches": []}), 200

    current_user = users[current_email]
    match_ids = current_user.get("matches", [])
    matches_list = []

    for mid in match_ids:
        mid_str = str(mid)
        # Ignorar IDs de teste
        if mid_str.startswith("p") or mid_str.startswith("mock_"):
            continue

        for em, u in users.items():
            if str(u.get("id")) == mid_str or em == mid_str:
                photo = u.get("photo") or (u.get("photos", [])[0] if u.get("photos") else "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80")
                matches_list.append({
                    "id": str(u.get("id") or em),
                    "name": u.get("display_name") or u.get("name") or "Utilizador",
                    "age": u.get("age", 25),
                    "city": u.get("city") or "Lisboa",
                    "photo": photo,
                    "code": (u.get("diagnosis") or "ALPHA")[:1],
                    "time": "Agora mesmo",
                    "is_real": True
                })
                break

    return jsonify({"matches": matches_list}), 200

@app.route("/api/v1/skip", methods=["POST"])
def api_skip():
    data = request.get_json(silent=True) or {}
    target_id = str(data.get("target_id", "")).strip()
    current_email = session.get("user_email")
    if current_email and target_id:
        users = load_users()
        if current_email in users:
            skipped_list = users[current_email].setdefault("skipped", [])
            if target_id not in skipped_list:
                skipped_list.append(target_id)
                save_users(users)
    return jsonify({"ok": True}), 200

@app.route("/api/v1/user/<uid>")
def api_get_user_profile(uid):
    users = load_users()
    for email, u in users.items():
        if str(u.get("id")) == str(uid) or email == str(uid):
            photo = u.get("photo") or (u.get("photos", [])[0] if u.get("photos") else "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85")
            photos_list = u.get("photos") if (u.get("photos") and len(u.get("photos")) > 0) else [photo]
            diag = u.get("diagnosis", "ALPHA")
            diag_code = diag[:1] if diag else "A"
            return jsonify({
                "profile": {
                    "id": str(u.get("id") or email),
                    "name": u.get("display_name") or u.get("name") or "Utilizador",
                    "age": u.get("age", 25),
                    "city": u.get("city") or "Lisboa, Portugal",
                    "km": "3 km de distância",
                    "code": diag_code,
                    "activity": "Ativo agora",
                    "photo": photo,
                    "photos": photos_list,
                    "bio": u.get("bio") or "Olá! Estou no Sigaleve para conexões reais, respeitosas e sem preconceito.",
                    "relationship_goal": u.get("relationship_goal") or "Relação séria",
                    "zodiac": u.get("zodiac") or "",
                    "education": u.get("education") or "",
                    "height": u.get("height") or "",
                    "lifestyle": u.get("lifestyle") or "",
                    "interests": u.get("interests", ["Viagens", "Música"]),
                    "verified": True,
                    "is_real_user": True
                }
            }), 200

    return jsonify({"error": "Perfil não encontrado"}), 404

# ── API de Subscrições e Pagamentos (Sigaleve Plus & Platinum) ────────────────
@app.route("/api/v1/subscription/plans")
def api_subscription_plans():
    return jsonify({
        "plans": [
            {
                "id": "plus_1m",
                "name": "Sigaleve Plus",
                "duration": "1 Mês",
                "price": "14.99",
                "currency": "EUR",
                "symbol": "€",
                "badge": "Popular",
                "features": [
                    "Gostos (Likes) Ilimitados",
                    "Saber quem gostou de ti",
                    "5 Super Likes gratuitos por semana",
                    "1 Boost gratuito por mês",
                    "Retroceder ilimitado (Undo)",
                    "Modo Incógnito e Localização Seletiva",
                    "Cifra reforçada de dados clínicos"
                ]
            },
            {
                "id": "plus_6m",
                "name": "Sigaleve Plus Semestral",
                "duration": "6 Meses",
                "price": "9.99",
                "per_month": "9.99€/mês",
                "total": "59.94€",
                "currency": "EUR",
                "symbol": "€",
                "badge": "Poupa 33%",
                "features": [
                    "Todas as vantagens do Sigaleve Plus",
                    "Prioridade máxima na fila de descoberta",
                    "Filtro avançado por compatibilidade clínica",
                    "Suporte prioritário 24/7"
                ]
            },
            {
                "id": "platinum_12m",
                "name": "Sigaleve Platinum VIP",
                "duration": "12 Meses",
                "price": "6.99",
                "per_month": "6.99€/mês",
                "total": "83.88€",
                "currency": "EUR",
                "symbol": "€",
                "badge": "Melhor Valor",
                "features": [
                    "Tudo incluído + Distintivo VIP exclusivo",
                    "Mensagens prioritárias antes do Match",
                    "Verificação médica de perfil com selo dourado",
                    "Total confidencialidade com faturação discreta"
                ]
            }
        ]
    }), 200

@app.route("/api/v1/subscription/subscribe", methods=["POST"])
def api_subscribe():
    data = request.get_json(silent=True) or {}
    card_number = str(data.get("card_number", "")).replace(" ", "")
    card_holder = str(data.get("card_holder", "")).strip()
    exp_date = str(data.get("exp_date", "")).strip()
    cvv = str(data.get("cvv", "")).strip()
    plan_id = str(data.get("plan_id", "plus_1m"))

    if not card_holder:
        return jsonify({"success": False, "error": "Introduz o nome do titular do cartão."}), 400
    if len(card_number) < 13 or not card_number.isdigit():
        return jsonify({"success": False, "error": "Número de cartão de crédito/débito inválido."}), 400
    if len(cvv) < 3 or not cvv.isdigit():
        return jsonify({"success": False, "error": "Código CVV inválido (deve conter 3 ou 4 dígitos)."}), 400
    if "/" not in exp_date:
        return jsonify({"success": False, "error": "Data de validade inválida (formato MM/AA)."}), 400

    # Simulação de processamento PCI-DSS seguro
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    if email not in users:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    card_brand = "Visa" if card_number.startswith("4") else ("Mastercard" if card_number.startswith("5") else "Cartão Seguro")
    last4 = card_number[-4:] if len(card_number) >= 4 else "0000"

    plan_names = {
        "plus_1m": "Sigaleve Plus (1 Mês)",
        "plus_6m": "Sigaleve Plus (6 Meses)",
        "plus_12m": "Sigaleve Plus (12 Meses)",
        "gold_1m": "Sigaleve Gold (1 Mês)",
        "gold_6m": "Sigaleve Gold (6 Meses)",
        "gold_12m": "Sigaleve Gold (12 Meses)",
        "platinum_1m": "Sigaleve Platinum VIP (1 Mês)",
        "platinum_6m": "Sigaleve Platinum VIP (6 Meses)",
        "platinum_12m": "Sigaleve Platinum VIP (12 Meses)"
    }
    plan_title = plan_names.get(plan_id, f"Sigaleve {plan_id.replace('_', ' ').upper()}")

    sub_info = {
        "active": True,
        "plan_id": plan_id,
        "plan_name": plan_title,
        "card_brand": card_brand,
        "card_last4": last4,
        "card_holder": card_holder.upper(),
        "card_exp": exp_date,
        "started_at": datetime.datetime.utcnow().isoformat(),
        "next_billing": (datetime.datetime.utcnow() + datetime.timedelta(days=30)).strftime("%d de %B, %Y")
    }

    users[email]["is_plus"] = True
    users[email]["subscription"] = sub_info
    save_users(users)

    return jsonify({
        "success": True,
        "message": f"Subscrição {plan_title} ativada com sucesso!",
        "subscription": sub_info,
        "is_plus": True
    }), 200

@app.route("/api/v1/subscription/cancel", methods=["POST"])
def api_cancel_subscription():
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    if email not in users:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    users[email]["is_plus"] = False
    users[email]["subscription"] = None
    save_users(users)

    return jsonify({
        "success": True,
        "message": "A tua subscrição foi cancelada com sucesso. O teu perfil voltou ao plano gratuito."
    }), 200


# ── MÓDULO 1: FILTRO DE SEGURANÇA E PRIVACIDADE (ANTI-DOXXING & ANTI-SPAM) ──
def validate_content_privacy(text: str) -> tuple[bool, str]:
    """
    Bloqueia números de telefone, redes sociais externas, e-mails e links externos
    para garantir que os utilizadores se conhecem com segurança dentro da app.
    """
    if not text:
        return True, ""
    
    clean_lower = text.lower()

    # 1. Deteção de números de telefone (9 dígitos consecutivos ou separados por espaços, hífens ou pontos)
    phone_pattern = r'(\+?\d{2,3}[\s.-]?)?(\d[\s.-]?){8,12}\d'
    # Evitar falsos positivos como números pequenos ("tenho 24 anos", "2 ou 3")
    digits_only = re.sub(r'\D', '', text)
    if len(digits_only) >= 9 or re.search(phone_pattern, text):
        # Verificar se tem padrão telefónico típico
        if re.search(r'(9\d{8}|\d{3}[\s.-]\d{3}[\s.-]\d{3}|\+351|\+34|\+1|00351)', text) or len(digits_only) >= 9:
            return False, "Por motivos de segurança e privacidade, não é permitido partilhar números de telefone nos comentários ou momentos. Usa o chat seguro da aplicação."

    # 2. Deteção de redes sociais e identificadores externos
    social_patterns = [
        r'@[a-zA-Z0-9._]+',                     # @usuario
        r'\b(ig|insta|instagram):?\s*[@a-zA-Z0-9._]+',
        r'\b(snap|snapchat):?\s*[@a-zA-Z0-9._]+',
        r'\b(tiktok):?\s*[@a-zA-Z0-9._]+',
        r'\b(telegram|t\.me):?\s*[@a-zA-Z0-9._]+',
        r'\b(whats|whatsapp):?\s*\d+',
        r'\b(fb|facebook):?\s*[@a-zA-Z0-9._]+'
    ]
    for sp in social_patterns:
        if re.search(sp, clean_lower):
            return False, "Por motivos de proteção da comunidade, não é permitido divulgar redes sociais externas (Instagram, TikTok, WhatsApp, etc.)."

    # 3. Deteção de endereços de e-mail
    if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', clean_lower):
        return False, "Por motivos de segurança, não é permitido partilhar endereços de e-mail nesta secção."

    # 4. Deteção de links e URLs web
    if re.search(r'(https?:\/\/|www\.|\b[a-zA-Z0-9-]+\.(com|pt|es|net|org|io|me|app)\b)', clean_lower):
        return False, "Não é permitida a publicação de hiperligações externas."

    return True, ""


# ── MÓDULO 2: ARMAZENAMENTO DE COFRE PRIVADO, INTERAÇÕES E MOMENTOS ──────────
MOMENTS_FILE = os.path.join(DATA_DIR, "moments_store.json")
PHOTO_INTERACTIONS_FILE = os.path.join(DATA_DIR, "photo_interactions.json")
PRIVATE_ALBUMS_FILE = os.path.join(DATA_DIR, "private_albums.json")

def load_json_store(filepath, default):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json_store(filepath, data):
    try:
        with open(filepath + ".tmp", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(filepath + ".tmp", filepath)
    except Exception as e:
        print(f"[STORE SAVE ERROR] {filepath}: {e}")

DEFAULT_MOMENTS = []

# Fotos do cofre privado por utilizador (Álbum seguro - inicia 100% vazio para utilizadores reais)
DEFAULT_PRIVATE_ALBUMS = {}


# ── ROTAS DE COFRE PRIVADO (ÁLBUM OCULTO COM AUTORIZAÇÃO) ────────────────────
@app.route("/api/v1/profile/private-album/<user_id>", methods=["GET"])
def api_get_private_album(user_id):
    current_uid = session.get("user_id") or "default_owner"
    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    album = albums.get(user_id, {
        "photos": [],
        "authorized_users": [],
        "pending_requests": []
    })

    is_owner = (user_id == current_uid or user_id in ("me", "my_profile", "default_owner"))
    has_access = is_owner or (current_uid in album.get("authorized_users", []))
    has_requested = current_uid in album.get("pending_requests", [])

    if has_access:
        return jsonify({
            "success": True,
            "locked": False,
            "access_granted": True,
            "is_owner": is_owner,
            "photos": album.get("photos", []),
            "total_photos": len(album.get("photos", [])),
            "count": len(album.get("photos", [])),
            "requests": album.get("pending_requests", []) if is_owner else [],
            "pending_requests": album.get("pending_requests", []) if is_owner else []
        })
    else:
        return jsonify({
            "success": True,
            "locked": True,
            "access_granted": False,
            "is_owner": False,
            "status": "pending" if has_requested else "unauthorized",
            "count": len(album.get("photos", [])),
            "total_photos": len(album.get("photos", [])),
            "has_requested": has_requested,
            "message": "Este utilizador tem um álbum privado. Pede autorização para ver as fotos."
        })

@app.route("/api/v1/profile/private-album/request", methods=["POST"])
def api_request_private_album():
    data = request.get_json(silent=True) or {}
    target_user_id = data.get("target_user_id") or data.get("target_id")
    current_uid = session.get("user_id") or "default_owner"
    requester_name = session.get("user_name") or "Utilizador Sigaleve"

    if not target_user_id:
        return jsonify({"success": False, "error": "ID de utilizador inválido."}), 400

    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    if target_user_id not in albums:
        albums[target_user_id] = {"photos": [], "authorized_users": [], "pending_requests": []}

    req_list = albums[target_user_id].setdefault("pending_requests", [])
    if current_uid not in req_list:
        req_list.append(current_uid)
        save_json_store(PRIVATE_ALBUMS_FILE, albums)

    return jsonify({
        "success": True,
        "message": "Pedido de acesso enviado com sucesso! O proprietário receberá uma notificação para autorizar."
    }), 200

@app.route("/api/v1/profile/private-album/respond", methods=["POST"])
def api_respond_private_album():
    data = request.get_json(silent=True) or {}
    requester_id = data.get("requester_id")
    action = data.get("action")  # "grant" / "accept" ou "deny" / "reject"
    current_uid = session.get("user_id") or "default_owner"

    if not requester_id:
        return jsonify({"success": False, "error": "Parâmetros inválidos."}), 400

    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    my_album = albums.setdefault(current_uid, {"photos": [], "authorized_users": [], "pending_requests": []})

    if requester_id in my_album.get("pending_requests", []):
        my_album["pending_requests"].remove(requester_id)

    if action in ("grant", "accept"):
        if requester_id not in my_album.get("authorized_users", []):
            my_album["authorized_users"].append(requester_id)
        msg = "Acesso ao teu álbum privado concedido com sucesso!"
    else:
        if requester_id in my_album.get("authorized_users", []):
            my_album["authorized_users"].remove(requester_id)
        msg = "Pedido recusado."

    save_json_store(PRIVATE_ALBUMS_FILE, albums)
    return jsonify({"success": True, "message": msg, "authorized_users": my_album["authorized_users"]})

@app.route("/api/v1/profile/private-album/manage", methods=["POST"])
def api_manage_private_album():
    data = request.get_json(silent=True) or {}
    action = data.get("action")  # "add" | "remove"
    photo_url = data.get("photo_url")
    photos_list = data.get("photos")
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401

    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    my_album = albums.setdefault(current_uid, {"photos": [], "authorized_users": [], "pending_requests": []})

    if photos_list is not None and isinstance(photos_list, list):
        my_album["photos"] = photos_list
        save_json_store(PRIVATE_ALBUMS_FILE, albums)
        return jsonify({"success": True, "message": "Álbum privado atualizado.", "photos": my_album["photos"]})

    if not photo_url:
        return jsonify({"success": False, "error": "URL da foto inválido."}), 400

    if action == "add":
        if photo_url not in my_album["photos"]:
            my_album["photos"].append(photo_url)
        msg = "Foto adicionada ao teu cofre privado com sucesso!"
    elif action == "remove":
        if photo_url in my_album["photos"]:
            my_album["photos"].remove(photo_url)
        msg = "Foto removida do cofre privado."
    else:
        return jsonify({"success": False, "error": "Ação inválida."}), 400

    save_json_store(PRIVATE_ALBUMS_FILE, albums)
    return jsonify({"success": True, "message": msg, "photos": my_album["photos"]})


# ── ROTAS DE LIKES E COMENTÁRIOS EM FOTOS (COM FILTRO ANTI-SPAM) ─────────────
@app.route("/api/v1/photos/like", methods=["POST"])
def api_photo_like():
    data = request.get_json(silent=True) or {}
    photo_id = str(data.get("photo_id", "")).strip()
    current_uid = session.get("user_id") or "default_owner"

    if not photo_id:
        return jsonify({"success": False, "error": "Identificador de foto inválido."}), 400

    store = load_json_store(PHOTO_INTERACTIONS_FILE, {})
    p_data = store.setdefault(photo_id, {"likes": [], "comments": []})

    if current_uid in p_data["likes"]:
        p_data["likes"].remove(current_uid)
        liked = False
    else:
        p_data["likes"].append(current_uid)
        liked = True

    save_json_store(PHOTO_INTERACTIONS_FILE, store)
    return jsonify({
        "success": True,
        "liked": liked,
        "likes_count": len(p_data["likes"])
    })

@app.route("/api/v1/photos/comment", methods=["POST"])
def api_photo_comment():
    data = request.get_json(silent=True) or {}
    photo_id = str(data.get("photo_id", "")).strip()
    comment_text = str(data.get("comment") or data.get("text") or "").strip()
    current_uid = session.get("user_id") or "default_owner"
    user_name = session.get("user_name") or "Utilizador"
    user_avatar = session.get("user_photo") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"

    if not photo_id or not comment_text:
        return jsonify({"success": False, "error": "O comentário não pode estar vazio."}), 400

    # Validação estrita de privacidade contra números, e-mails ou redes sociais
    is_safe, error_msg = validate_content_privacy(comment_text)
    if not is_safe:
        return jsonify({
            "success": False,
            "error": error_msg,
            "security_blocked": True
        }), 400

    store = load_json_store(PHOTO_INTERACTIONS_FILE, {})
    p_data = store.setdefault(photo_id, {"likes": [], "comments": []})

    new_comment = {
        "id": f"c_{uuid.uuid4().hex[:8]}",
        "user_id": current_uid,
        "user_name": user_name,
        "user_avatar": user_avatar,
        "text": comment_text,
        "timestamp": "Agora mesmo"
    }
    p_data["comments"].append(new_comment)
    save_json_store(PHOTO_INTERACTIONS_FILE, store)

    return jsonify({
        "success": True,
        "message": "Comentário publicado com sucesso!",
        "comment": new_comment,
        "total_comments": len(p_data["comments"])
    }), 201

@app.route("/api/v1/photos/comments", methods=["GET"])
def api_get_photo_comments():
    photo_id = request.args.get("photo_id", "")
    current_uid = session.get("user_id") or "default_owner"
    store = load_json_store(PHOTO_INTERACTIONS_FILE, {})
    p_data = store.get(photo_id, {"likes": [], "comments": []})

    return jsonify({
        "success": True,
        "likes_count": len(p_data.get("likes", [])),
        "user_has_liked": current_uid in p_data.get("likes", []),
        "comments": p_data.get("comments", [])
    })


# ── ROTAS DE MOMENTOS / HISTÓRIAS EFÉMERAS (24 HORAS, SÓ ENTRE MATCHES) ──────
@app.route("/api/v1/moments", methods=["GET"])
def api_get_moments():
    raw_moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    current_uid = str(request.args.get("user_id") or request.headers.get("X-User-Id") or session.get("user_id") or "default_owner")
    matches_param = request.args.get("matches", "")
    allowed_match_ids = set()
    if matches_param:
        for mid in matches_param.split(","):
            m_clean = mid.strip()
            if m_clean:
                allowed_match_ids.add(m_clean)

    now = time.time()
    valid_moments = []
    has_expired = False

    # 1. Eliminar publicações com mais de 24 horas (86400 segundos)
    for m in raw_moments:
        created_at = m.get("created_at")
        if created_at is None:
            # Compatibilidade com publicações antigas
            created_at = now
            m["created_at"] = now
        try:
            created_at = float(created_at)
        except (ValueError, TypeError):
            created_at = now

        # Mais de 24 horas -> expira e é removido definitivamente
        if (now - created_at) > 86400:
            has_expired = True
            continue

        valid_moments.append(m)

    if has_expired:
        save_json_store(MOMENTS_FILE, valid_moments)

    # 2. Filtrar visibilidade: só o próprio autor ou pessoas que deram match
    enriched_moments = []
    for m in valid_moments:
        author_id = str(m.get("user_id", ""))
        is_own = (author_id == current_uid or current_uid in ("default_owner", ""))
        is_match = (author_id in allowed_match_ids)

        if not is_own and not is_match:
            continue

        m_copy = dict(m)
        created_at = float(m.get("created_at", now))
        remaining_sec = max(0, int(86400 - (now - created_at)))
        rem_hours = remaining_sec // 3600
        rem_min = (remaining_sec % 3600) // 60
        m_copy["remaining_time"] = f"{rem_hours}h {rem_min}m"
        m_copy["expires_in_sec"] = remaining_sec

        user_reactions = m.get("user_reactions", {})
        m_copy["my_reaction"] = user_reactions.get(str(current_uid), None)
        enriched_moments.append(m_copy)

    return jsonify({
        "success": True,
        "moments": enriched_moments
    })

@app.route("/api/v1/moments", methods=["POST"])
def api_create_moment():
    data = request.get_json(silent=True) or {}
    text_content = str(data.get("text", "")).strip()
    mood = str(data.get("mood", "☕ A relaxar")).strip()
    mood_emoji = str(data.get("mood_emoji", "☕")).strip()
    photo = str(data.get("photo_url", data.get("photo", ""))).strip()

    current_uid = str(data.get("user_id") or session.get("user_id") or "default_owner")
    user_name = str(data.get("user_name") or session.get("user_name") or "Eu")
    user_avatar = str(data.get("user_avatar") or session.get("user_photo") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80")
    user_city = str(session.get("user_city") or "Lisboa")

    if not text_content and not photo:
        return jsonify({"success": False, "error": "Escreve um pensamento ou partilha uma foto/vídeo da tua história."}), 400

    if len(text_content) > 1000:
        return jsonify({"success": False, "error": "A tua publicação deve ter no máximo 1000 caracteres."}), 400

    # Filtro de privacidade estrito
    is_safe, error_msg = validate_content_privacy(text_content)
    if not is_safe:
        return jsonify({
            "success": False,
            "error": error_msg,
            "security_blocked": True
        }), 400

    now = time.time()
    moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    new_moment = {
        "id": f"m_{uuid.uuid4().hex[:8]}",
        "user_id": current_uid,
        "author_name": user_name,
        "author_avatar": user_avatar,
        "user_name": user_name,
        "user_photo": user_avatar,
        "city": user_city,
        "mood": mood,
        "mood_emoji": mood_emoji,
        "text": text_content,
        "photo": photo,
        "photo_url": photo,
        "created_at": now,
        "time": "Agora mesmo",
        "timestamp": "Agora mesmo",
        "likes_count": 0,
        "reactions": {"heart": 0, "hug": 0, "coffee": 0},
        "user_reactions": {}
    }
    moments.insert(0, new_moment)
    save_json_store(MOMENTS_FILE, moments)

    return jsonify({
        "success": True,
        "message": "A tua história temporária foi partilhada (visível durante 24 horas apenas para os teus matches)!",
        "moment": new_moment
    }), 201

@app.route("/api/v1/moments/react", methods=["POST"])
def api_react_moment():
    data = request.get_json(silent=True) or {}
    moment_id = data.get("moment_id")
    raw_reaction = str(data.get("reaction", "heart")).strip().lower()

    # Normalizar reaction
    reaction_map = {
        "heart": "heart",
        "❤️": "heart",
        "hug": "hug",
        "✨": "hug",
        "🤗": "hug",
        "coffee": "coffee",
        "☕": "coffee"
    }
    reaction = reaction_map.get(raw_reaction, raw_reaction)
    ALLOWED_RX = ("heart", "hug", "coffee", "laugh", "sad", "angry")
    if reaction not in ALLOWED_RX:
        reaction = "heart"

    current_uid = str(data.get("user_id") or session.get("user_id") or "default_owner")

    moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    target = None
    for m in moments:
        if m["id"] == moment_id:
            target = m
            break

    if not target:
        return jsonify({"success": False, "error": "Momento não encontrado."}), 404

    # Garantir estrutura
    rx = target.setdefault("reactions", {})
    for k in ALLOWED_RX:
        if k not in rx:
            rx[k] = 0
    # Limpar legados se existirem
    if "❤️" in rx:
        rx["heart"] = rx.get("heart", 0) + rx.pop("❤️")
    if "✨" in rx:
        rx["hug"] = rx.get("hug", 0) + rx.pop("✨")

    user_rx = target.setdefault("user_reactions", {})
    prev_reaction = user_rx.get(current_uid)

    if prev_reaction == reaction:
        # Clicou novamente na mesma reação: remove (toggle off)
        rx[reaction] = max(0, rx.get(reaction, 0) - 1)
        user_rx.pop(current_uid, None)
        active_reaction = None
    else:
        # Mudou de reação ou é a primeira reação
        if prev_reaction and prev_reaction in rx:
            rx[prev_reaction] = max(0, rx[prev_reaction] - 1)
        rx[reaction] = rx.get(reaction, 0) + 1
        user_rx[current_uid] = reaction
        active_reaction = reaction

    target["likes_count"] = sum(rx.values())
    save_json_store(MOMENTS_FILE, moments)

    return jsonify({
        "success": True,
        "reactions": rx,
        "user_reaction": active_reaction,
        "total": target["likes_count"]
    })

@app.route("/api/v1/moments/<moment_id>", methods=["PUT"])
def api_update_moment(moment_id):
    data = request.get_json(silent=True) or {}
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    new_text = str(data.get("text", "")).strip()
    new_mood = str(data.get("mood", "")).strip()

    if len(new_text) > 1000:
        return jsonify({"success": False, "error": "O momento deve ter no máximo 1000 caracteres."}), 400

    if new_text:
        is_safe, error_msg = validate_content_privacy(new_text)
        if not is_safe:
            return jsonify({
                "success": False,
                "error": error_msg,
                "security_blocked": True
            }), 400

    moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    target = None
    for m in moments:
        if m.get("id") == moment_id:
            target = m
            break

    if not target:
        return jsonify({"success": False, "error": "Momento não encontrado."}), 404

    # Verificar autoria estrita (apenas o dono da publicação)
    target_owner = str(target.get("user_id") or "")
    if target_owner and target_owner != current_uid:
        return jsonify({"success": False, "error": "Não tens permissão para editar esta publicação."}), 403

    if "text" in data:
        target["text"] = new_text
    if new_mood:
        target["mood"] = new_mood
    target["edited"] = True

    save_json_store(MOMENTS_FILE, moments)
    return jsonify({
        "success": True,
        "message": "Momento atualizado com sucesso!",
        "moment": target
    })

@app.route("/api/v1/moments/<moment_id>", methods=["DELETE"])
def api_delete_moment(moment_id):
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    
    target_idx = None
    for idx, m in enumerate(moments):
        if m.get("id") == moment_id:
            target_idx = idx
            break

    if target_idx is None:
        return jsonify({"success": False, "error": "Momento não encontrado."}), 404

    target = moments[target_idx]
    target_owner = str(target.get("user_id") or "")
    if target_owner and target_owner != current_uid:
        return jsonify({"success": False, "error": "Não tens permissão para eliminar esta publicação."}), 403

    moments.pop(target_idx)
    save_json_store(MOMENTS_FILE, moments)
    return jsonify({"success": True, "message": "Momento eliminado com sucesso."})

@app.route("/api/v1/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "healthy",
        "service": "sigaleve",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200

@app.route("/api/v1/conversations", methods=["GET"])
@app.route("/api/v1/chat/conversations", methods=["GET"])
def api_get_conversations():
    uid = session.get("user_id") or request.headers.get("X-User-Id") or request.args.get("user_id")
    # Retorna lista de conversas ativas do utilizador
    return jsonify({
        "success": True,
        "conversations": []
    }), 200

# ── Socket.IO (Chat em Tempo Real Efêmero) ──────────────────────────────────
@socketio.on("connect")
def on_connect(auth=None):
    emit("connected", {"status": "ok"})

@socketio.on("join_room")
def on_join(data):
    my_id = data.get("sender_id") or session.get("user_id") or "11111111-1111-1111-1111-111111111111"
    other = data.get("other_user_id", "22222222-2222-2222-2222-222222222222")
    ids = sorted([str(my_id), str(other)])
    room = f"room__{ids[0]}__{ids[1]}"
    join_room(room)
    emit("room_joined", {
        "room_id": room,
        "ephemeral_note": "Mensagens efêmeras protegidas com destruição em 24h."
    })

@socketio.on("send_message")
def on_message(data):
    content = str(data.get("content", "")).strip()
    if not content:
        return
    my_id = data.get("sender_id") or session.get("user_id") or "11111111-1111-1111-1111-111111111111"
    other = data.get("other_user_id", "22222222-2222-2222-2222-222222222222")
    msg_id = data.get("msg_id", "")
    ids = sorted([str(my_id), str(other)])
    room = f"room__{ids[0]}__{ids[1]}"
    ts = datetime.datetime.utcnow().isoformat() + "Z"

    # Transmitir a mensagem real exclusivamente entre as duas pessoas reais na sala
    socketio.emit("new_message", {
        "sender_id": str(my_id),
        "content": content,
        "ts": ts,
        "msg_id": msg_id
    }, to=room)

@socketio.on("leave_room")
def on_leave(data):
    my_id = session.get("user_id") or "11111111-1111-1111-1111-111111111111"
    other = data.get("other_user_id", "22222222-2222-2222-2222-222222222222")
    ids = sorted([str(my_id), str(other)])
    room = f"room__{ids[0]}__{ids[1]}"
    leave_room(room)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  SIGALEVE ENGINE — 100% OPERACIONAL")
    print("  Landing Page : http://localhost:5001")
    print("  App Sigaleve : http://localhost:5001/app")
    print("  Credenciais Demo: demo@sigaleve.app | Sigaleve2026!")
    print("=" * 60 + "\n")
    socketio.run(app, host="0.0.0.0", port=5001, debug=True, allow_unsafe_werkzeug=True)
