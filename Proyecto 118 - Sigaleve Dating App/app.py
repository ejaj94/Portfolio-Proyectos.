"""
app.py — Sigaleve Core Application Server.
Arquitetura Modular Limpa e Escalável de Nível Sénior.

Todos os módulos funcionais foram particionados em rotas e serviços especializados:
- routes.auth (Registo, Login, 2FA, Social Logins, Recuperação de Palavra-passe)
- routes.profile (Perfil, Atualização, Upload de Fotos, Verificação Facial)
- routes.discovery (Descoberta, Likes, Matches e Skips)
- routes.chat (Conversas, Histórico 24h efêmero e Socket.IO em tempo real)
- routes.moments (Histórias de 24h, Reações e Comentários moderados)
- routes.vault (Cofre Privado / Álbum Seguro)
- routes.subscription (Planos e Subscrições)
- routes.push (WebPush VAPID)
- routes.qa_health (Perguntas e Respostas de Saúde Anónimas)
"""
import os
import json
import datetime
from datetime import timedelta
from flask import Flask, jsonify, render_template, request, session
from flask_socketio import SocketIO
from werkzeug.middleware.proxy_fix import ProxyFix

# Importar helpers centrais de dados e serviços
from services.common import (
    load_json_store,
    save_json_store,
    load_users,
    save_users,
    touch_last_active,
    validate_content_privacy,
)

# Carregar variáveis de ambiente se existir .env
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

# Inicialização da Aplicação Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sigaleve-production-super-secret-key-2026")

# Sessão persistente de 30 dias (proteção contra deslog no mobile)
is_prod = os.environ.get("PRODUCTION", "False").lower() in ("true", "1")
app.permanent_session_lifetime = timedelta(days=30)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=is_prod,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_NAME="sigaleve_session",
    TEMPLATES_AUTO_RELOAD=True,
)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
socketio = SocketIO(app, cors_allowed_origins="*")

# ── Importação e Registo dos Blueprints Modulares ───────────────────────────
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.discovery import discovery_bp
from routes.chat import chat_bp, register_socket_events
from routes.moments import moments_bp, start_moments_purger
from routes.vault import vault_bp
from routes.subscription import subscription_bp
from routes.push import push_bp
from routes.qa_health import qa_bp

app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(discovery_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(moments_bp)
app.register_blueprint(vault_bp)
app.register_blueprint(subscription_bp)
app.register_blueprint(push_bp)
app.register_blueprint(qa_bp)

# Registar eventos de WebSockets (Socket.IO)
register_socket_events(socketio)

# Iniciar integrações especializadas existentes
import payments_manual
payments_manual.init_payments(
    app, session, load_json_store, save_json_store, load_users, save_users
)

import success_stories
success_stories.init_stories(
    app, session, load_json_store, save_json_store, load_users, save_users
)

import date_ideas
date_ideas.init_date_ideas(
    app, session, load_json_store, save_json_store, validate_content_privacy, load_users
)


# ── Headers No-Cache e Blindagem HTTP ───────────────────────────────────────
@app.after_request
def add_security_and_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ── Dicionário SEO Multi-idioma ──────────────────────────────────────────────
SEO_LOCALES = {
    "pt": {
        "title": "Sigaleve | Namoro para pessoas com infeções sexualmente transmissíveis",
        "description": "A comunidade de namoro de Portugal para pessoas que vivem com IST (herpes, HPV, VIH e outras). Conhece quem entende o teu caminho: sem julgamentos, perfis verificados e privacidade total.",
        "og_locale": "pt_PT"
    },
    "br": {
        "title": "Sigaleve | Namoro para pessoas com infecções sexualmente transmissíveis",
        "description": "A comunidade de namoro para pessoas que vivem com IST (herpes, HPV, HIV e outras). Conheça quem entende o seu caminho: sem julgamentos, perfis verificados e privacidade total.",
        "og_locale": "pt_BR"
    },
    "es": {
        "title": "Sigaleve | Citas para personas con infecciones de transmisión sexual",
        "description": "La comunidad de citas de Portugal para personas que viven con ITS (herpes, VPH, VIH y otras). Conoce a quien entiende tu camino: sin juicios, perfiles verificados y privacidad total.",
        "og_locale": "es_ES"
    },
    "en": {
        "title": "Sigaleve | Dating for People Living with STIs",
        "description": "Portugal's dating community for people living with sexually transmitted infections (herpes, HPV, HIV and others). Meet those who understand your journey: no judgment, verified profiles, total privacy.",
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


def resolve_request_language() -> str:
    arg_lang = request.args.get("lang")
    if arg_lang and arg_lang.lower() in SEO_LOCALES:
        return arg_lang.lower()
    cookie_lang = request.cookies.get("sigaleve_lang")
    if cookie_lang and cookie_lang.lower() in SEO_LOCALES:
        return cookie_lang.lower()
    accept = request.headers.get("Accept-Language", "")
    for part in accept.split(","):
        code = part.split(";")[0].strip().lower()
        if code in SEO_LOCALES:
            return code
        if code.startswith("pt-br") or code.startswith("pt_br"):
            return "br"
        base2 = code[:2]
        if base2 in SEO_LOCALES:
            return base2
    return "pt"


# ── ROTAS PÚBLICAS E LANDING PAGE ───────────────────────────────────────────

@app.route("/")
def landing():
    lang = resolve_request_language()
    explicit_lang = request.args.get("lang")
    seo_data = SEO_LOCALES.get(lang, SEO_LOCALES["pt"])
    approved_stories = success_stories.get_approved_stories(load_json_store, save_json_store)
    resp = app.make_response(render_template(
        "landing.html",
        current_lang=lang,
        seo_title=seo_data["title"],
        seo_desc=seo_data["description"],
        seo_locale=seo_data["og_locale"],
        success_stories=approved_stories
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
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
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
        <p class="text-gray-300 text-sm mb-6 leading-relaxed">O teu endereço foi validado. Por motivos de segurança, conclui o início de sessão na aplicação.</p>
        <a href="/app?verified=true" class="block w-full py-3.5 rounded-full font-bold text-white bg-gradient-to-r from-pink-500 to-orange-500 hover:opacity-90 transition-all shadow-lg">
            Voltar à Aplicação
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


# ── ROTAS LEGAIS E INSTITUCIONAIS ───────────────────────────────────────────

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


# ── HEARTBEAT DE PRESENÇA E HEALTH CHECK ─────────────────────────────────────

@app.route("/api/v1/presence/heartbeat", methods=["POST"])
def api_presence_heartbeat():
    email = session.get("user_email")
    if not email:
        return jsonify({"ok": False}), 401
    users = load_users()
    u = users.get(email)
    if not u:
        return jsonify({"ok": False}), 401
    import time
    agora = time.time()
    if agora - float(u.get("last_active") or 0) > 45:
        if u.get("show_recent_activity", True) is False:
            u.pop("last_active", None)
        else:
            u["last_active"] = agora
        save_users(users)
    return jsonify({"ok": True, "last_active": u.get("last_active")}), 200


@app.route("/api/v1/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def api_health():
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return jsonify({
        "status": "healthy",
        "service": "sigaleve",
        "timestamp": now_iso
    }), 200


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

        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source}&tl={target}&dt=t&q=" + urllib.parse.quote(t_str)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                res_data = json.loads(resp.read().decode('utf-8'))
                res_text = "".join([part[0] for part in res_data[0] if part and part[0]])
        except Exception:
            res_text = None

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

        translated[t_str] = res_text if res_text else t_str

    return jsonify({"success": True, "translations": translated})


# ── INICIALIZAÇÃO DO SERVIDOR ───────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  SIGALEVE ENGINE — 100% OPERACIONAL (MODULAR SENIOR ARCH)")
    print("  Landing Page : http://localhost:5001")
    print("  App Sigaleve : http://localhost:5001/app")
    print("  Health Check : http://localhost:5001/api/v1/health")
    print("=" * 60 + "\n")

    # Iniciar daemon de limpeza periódica de histórias expiradas
    start_moments_purger()

    socketio.run(app, host="0.0.0.0", port=5001, debug=False, allow_unsafe_werkzeug=True)
