"""
services/common.py — Helpers centrais de dados, sessão, presença e e-mail.
Utilizado por todos os Blueprints e módulos do Sigaleve.
"""
import os
import json
import uuid
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Diretórios base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
USERS_FILE = os.path.join(DATA_DIR, "users_store.json")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages_store.json")
MOMENTS_FILE = os.path.join(DATA_DIR, "moments_store.json")
PHOTO_INTERACTIONS_FILE = os.path.join(DATA_DIR, "photo_interactions.json")
PRIVATE_ALBUMS_FILE = os.path.join(DATA_DIR, "private_albums.json")
PUSH_SUBS_FILE = os.path.join(DATA_DIR, "push_subscriptions.json")
QA_HEALTH_FILE = os.path.join(DATA_DIR, "qa_health_store.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_UPLOAD_BYTES = 8 * 1024 * 1024  # 8 MB por foto
ALLOWED_UPLOAD_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}

# Configurações SMTP
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER or "support@sigaleve.com")


def send_real_email(recipient: str, subject: str, html_content: str, text_content: str = "") -> tuple[bool, str]:
    """Envia e-mail real por SMTP ou faz log em desenvolvimento."""
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

            email_delivered = True
            delivery_note = f"E-mail real entregue na tua caixa de entrada ({recipient})."
        except Exception as exc:
            delivery_note = f"Falha no envio SMTP ({str(exc)})."
    else:
        delivery_note = "Credenciais SMTP não configuradas."

    return email_delivered, delivery_note


def load_json_store(filepath, default=None):
    """Lê um arquivo JSON de forma segura com fallback."""
    if default is None:
        default = {}
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json_store(filepath, data):
    """Guarda dados num JSON de forma atómica para evitar corrupção."""
    try:
        temp_path = filepath + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, filepath)
    except Exception as e:
        print(f"[SAVE_JSON_STORE ERROR] {filepath}: {e}")


def load_users():
    """Carrega os utilizadores a partir de USERS_FILE, decifrando dados sensíveis."""
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
            import crypto as _crypto
            users = {em: (_crypto.decrypt_user_sensitive(u) if isinstance(u, dict) else u) for em, u in users.items()}
        except Exception as e:
            backup_file = USERS_FILE + ".bak"
            if os.path.exists(backup_file):
                try:
                    with open(backup_file, "r", encoding="utf-8") as f_bak:
                        users = json.load(f_bak)
                    import crypto as _crypto
                    users = {em: (_crypto.decrypt_user_sensitive(u) if isinstance(u, dict) else u) for em, u in users.items()}
                except Exception:
                    users = {}
    return users


def save_users(users):
    """Cifra dados sensíveis e grava USERS_FILE com backup de segurança atómico."""
    if not isinstance(users, dict):
        return
    import crypto as _crypto
    safe_users = {}
    for email, u in users.items():
        if isinstance(u, dict):
            safe_users[email] = _crypto.encrypt_user_sensitive(dict(u))
        else:
            safe_users[email] = u
    temp_file = USERS_FILE + ".tmp"
    backup_file = USERS_FILE + ".bak"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(safe_users, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        if os.path.exists(USERS_FILE):
            try:
                import shutil
                shutil.copyfile(USERS_FILE, backup_file)
            except Exception:
                pass
        os.replace(temp_file, USERS_FILE)
    except Exception as e:
        print(f"[SAVE_USERS ERROR] {e}")


def safe_photo(u: dict, fallback: str = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80") -> str:
    """Devolve uma URL de foto válida e leve."""
    for v in (u.get("photo"), (u.get("photos") or [None])[0]):
        s = v if isinstance(v, str) else ""
        if s.startswith(("http://", "https://", "/")):
            return s
    return fallback


def presence_label(last_active_ts):
    """Devolve estado de atividade e formatação elegante."""
    if not last_active_ts:
        return {"online": False, "label": "Offline"}
    now = time.time()
    diff = now - float(last_active_ts)
    if diff < 120:
        return {"online": True, "label": "Online agora"}
    if diff < 3600:
        m = int(diff / 60)
        return {"online": False, "label": f"Ativo há {m} min"}
    if diff < 86400:
        h = int(diff / 3600)
        return {"online": False, "label": f"Ativo há {h}h"}
    d = int(diff / 86400)
    return {"online": False, "label": f"Ativo há {d}d"}


def touch_last_active(users, email):
    """Atualiza timestamp de última atividade."""
    if email in users and isinstance(users[email], dict):
        users[email]["last_active"] = time.time()
        save_users(users)


def serialize_user(user: dict) -> dict:
    """Serializa o utilizador para consumo na interface de forma segura."""
    if not user:
        return {}
    import crypto as _crypto
    u = _crypto.decrypt_user_sensitive(user)
    def _thumb(v, max_len=180):
        s = v if isinstance(v, str) else ""
        return s if len(s) <= max_len or not s.startswith("data:") else None
    photos_field = u.get("photos", [])
    if isinstance(photos_field, list) and any(
        isinstance(p, str) and p.startswith("data:") and len(p) > 512 for p in photos_field
    ):
        photos_field = []
    return {
        "id": u.get("id"),
        "email": u.get("email"),
        "display_name": u.get("display_name", "Utilizador"),
        "phone": u.get("phone", ""),
        "age": u.get("age", 25),
        "city": u.get("city", "Lisboa, Portugal"),
        "bio": u.get("bio", ""),
        "photo": _thumb(u.get("photo")) or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85",
        "photos": photos_field,
        "interests": u.get("interests", ["Viagens", "Música"]),
        "diagnosis": u.get("diagnosis", "ALPHA"),
        "custom_diagnosis": u.get("custom_diagnosis", ""),
        "relationship_goal": u.get("relationship_goal", ""),
        "zodiac": u.get("zodiac", ""),
        "education": u.get("education", ""),
        "height": u.get("height", ""),
        "lifestyle": u.get("lifestyle", ""),
        "profile_prompt": u.get("profile_prompt", ""),
        "seeking": u.get("seeking", "Todos"),
        "max_distance": u.get("max_distance", 50),
        "is_profile_configured": u.get("is_profile_configured", False),
        "is_plus": u.get("is_plus", False),
        "subscription": u.get("subscription", None),
        "last_active": u.get("last_active"),
        "presence": presence_label(u.get("last_active"))["label"] if u.get("show_recent_activity", True) else None
    }


def validate_content_privacy(text: str) -> tuple[bool, str]:
    """
    Bloqueia números de telefone, redes sociais externas, e-mails e links externos
    para garantir que os utilizadores se conhecem com segurança dentro da app.
    """
    import re
    if not text:
        return True, ""
    
    clean_lower = text.lower()

    # 1. Deteção de números de telefone
    phone_pattern = r'(\+?\d{2,3}[\s.-]?)?(\d[\s.-]?){8,12}\d'
    digits_only = re.sub(r'\D', '', text)
    if len(digits_only) >= 9 or re.search(phone_pattern, text):
        if re.search(r'( 9\d{8} | \d{3}[\s.-]\d{3}[\s.-]\d{3} |\+351|\+34|\+1| 00351)', text) or len(digits_only) >= 9:
            return False, "Por motivos de segurança e privacidade, não é permitido partilhar números de telefone nos comentários ou momentos. Usa o chat seguro da aplicação."

    # 2. Deteção de redes sociais e identificadores externos
    social_patterns = [
        r'@[a-zA-Z0-9._]+',
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

    # 4. Deteção de injeção de código / scripts HTML (XSS)
    if re.search(r'<\s*script\b|javascript:|onerror\s*=|onload\s*=|onclick\s*=|<\s*iframe\b|<\s*img\b|<\s*svg\b|<\s*style\b|<\s*link\b', clean_lower):
        return False, "Por motivos de segurança, código ou tags HTML não são permitidos nesta aplicação."

    # 5. Deteção de links e URLs web
    if re.search(r'(https?:\/\/|www\.|\b[a-zA-Z0-9-]+\.(com|pt|es|net|org|io|me|app)\b)', clean_lower):
        return False, "Não é permitida a publicação de hiperligações externas."

    return True, ""
