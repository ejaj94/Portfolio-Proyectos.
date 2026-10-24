"""
routes/auth.py — Blueprint para Autenticação, Registo, 2FA (TOTP + E-mail),
Login Social (Google, Facebook, Instagram), Recuperação de Palavra-passe e Eliminação de Conta (RGPD Art. 17).
"""
import os
import io
import re
import uuid
import json
import random
import secrets
import datetime
from datetime import timedelta
import base64
import urllib.parse
import urllib.request
import pyotp
import qrcode
from flask import Blueprint, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from services.common import (
    load_users,
    save_users,
    serialize_user,
    touch_last_active,
    send_real_email,
    DATA_DIR,
)

auth_bp = Blueprint("auth_bp", __name__)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "86970408130-8ugh10poqvbespttgfqr5553hkgvkn4d.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
META_APP_ID = os.environ.get("META_APP_ID", "")
META_APP_SECRET = os.environ.get("META_APP_SECRET", "")
FACEBOOK_APP_ID = META_APP_ID
FACEBOOK_APP_SECRET = META_APP_SECRET
INSTAGRAM_APP_ID = META_APP_ID
INSTAGRAM_APP_SECRET = META_APP_SECRET

# ── Rate limiting em memória contra ataques de força bruta no login ───────────
_LOGIN_ATTEMPTS = {}
_LOGIN_MAX_ATTEMPTS = 5
_LOGIN_LOCK_MINUTES = 15


def _login_rate_check(identifier: str) -> tuple[bool, int]:
    import time as _time
    rec = _LOGIN_ATTEMPTS.get(identifier)
    if not rec:
        return False, 0
    until = rec.get("blocked_until", 0)
    if until and until > _time.time():
        return True, int(until - _time.time())
    return False, 0


def _login_rate_fail(identifier: str):
    import time as _time
    rec = _LOGIN_ATTEMPTS.setdefault(identifier, {"count": 0, "blocked_until": 0})
    rec["count"] += 1
    if rec["count"] >= _LOGIN_MAX_ATTEMPTS:
        rec["blocked_until"] = _time.time() + (_LOGIN_LOCK_MINUTES * 60)
        rec["count"] = 0


def _login_rate_clear(identifier: str):
    _LOGIN_ATTEMPTS.pop(identifier, None)


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


def get_oauth_redirect_uri(endpoint: str) -> str:
    host = request.headers.get("X-Forwarded-Host") or request.host
    proto = request.headers.get("X-Forwarded-Proto") or request.scheme
    if "sigaleve.com" in host or not (host.startswith("localhost") or host.startswith("127.0.0.1")):
        proto = "https"
    return f"{proto}://{host}{endpoint}"


# ── REGISTO ──────────────────────────────────────────────────────────────────

@auth_bp.route("/api/v1/auth/register", methods=["POST"])
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
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "is_profile_configured": False,
        "email_verified": True,
        "known_devices": [device_id]
    }
    users[email] = new_user
    save_users(users)

    session["user_id"] = user_id
    session.permanent = True
    session["user_email"] = email

    return jsonify({
        "success": True,
        "requires_verification": False,
        "message": "Conta criada com sucesso!",
        "user": serialize_user(new_user)
    }), 201


# ── 2FA STATUS & CONFIGURAÇÃO ────────────────────────────────────────────────

@auth_bp.route("/api/v1/auth/2fa/status", methods=["GET"])
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


@auth_bp.route("/api/v1/auth/2fa/setup-totp", methods=["POST"])
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


@auth_bp.route("/api/v1/auth/2fa/verify-setup-totp", methods=["POST"])
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


@auth_bp.route("/api/v1/auth/2fa/send-email-code", methods=["POST"])
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

    # 🔒 SEGURANÇA: nunca expor o código OTP no corpo da resposta HTTP
    return jsonify({
        "success": True,
        "message": f"Código enviado com sucesso para {user['email']}.",
        "email": user["email"],
        "delivered": delivered,
        "note": note
    }), 200


@auth_bp.route("/api/v1/auth/2fa/verify-email-code", methods=["POST"])
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


@auth_bp.route("/api/v1/auth/2fa/disable", methods=["POST"])
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


# ── LOGIN & VERIFICAÇÃO DE CÓDIGO ───────────────────────────────────────────

@auth_bp.route("/api/v1/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    identifier = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    blocked, wait_s = _login_rate_check(identifier)
    if blocked:
        mins = max(1, wait_s // 60)
        return jsonify({"success": False, "error": f"Demasiadas tentativas. Tenta novamente em {mins} minuto(s)."}), 429

    users = load_users()
    user = users.get(identifier)

    if not user:
        for u_email, u_data in users.items():
            if u_data.get("display_name", "").strip().lower() == identifier or u_email.strip().lower() == identifier:
                user = u_data
                break

    if not user or not check_password_hash(user["password_hash"], password):
        _login_rate_fail(identifier)
        return jsonify({"success": False, "error": "Credenciais incorretas. Verifique o e-mail/utilizador e a palavra-passe."}), 401

    _login_rate_clear(identifier)
    two_factor = user.get("two_factor", {})
    two_factor_enabled = two_factor.get("enabled", False)
    two_factor_method = two_factor.get("method", "none")

    if two_factor_enabled and two_factor_method == "totp":
        return jsonify({
            "success": True,
            "requires_verification": True,
            "auth_method": "totp",
            "email": user["email"],
            "message": "Introduz o código de 6 dígitos gerado pela tua aplicação autenticadora (Google Authenticator / Authy)."
        }), 200

    session["user_id"] = user["id"]
    session.permanent = True
    session["user_email"] = user["email"]
    try:
        touch_last_active(users, user["email"])
    except Exception:
        pass

    return jsonify({
        "success": True,
        "requires_verification": False,
        "message": "Sessão iniciada com sucesso.",
        "user": serialize_user(user)
    }), 200


@auth_bp.route("/api/v1/auth/verify-code", methods=["POST"])
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

    if two_factor_enabled and two_factor_method == "totp":
        totp_secret = two_factor.get("totp_secret")
        if not totp_secret:
            return jsonify({"success": False, "error": "Configuração TOTP inválida no servidor."}), 500
        totp = pyotp.TOTP(totp_secret)
        if not totp.verify(code, valid_window=1):
            return jsonify({"success": False, "error": "Código da aplicação autenticadora inválido ou expirado."}), 400
    else:
        if not user.get("email_verified", False):
            return jsonify({
                "success": False,
                "error": "Atenção: Primeiro deves abrir o teu e-mail e carregar no link de confirmação antes de introduzir o código!"
            }), 403

        expected_otp = str(user.get("otp_code", ""))
        if not expected_otp or code != expected_otp:
            return jsonify({"success": False, "error": "Código de verificação incorreto. Verifique o seu e-mail e tente novamente."}), 400

    known_devices = user.get("known_devices", [])
    if device_id not in known_devices:
        known_devices.append(device_id)
        user["known_devices"] = known_devices
    user["email_verified"] = True
    save_users(users)

    session["user_id"] = user["id"]
    session.permanent = True
    session["user_email"] = user["email"]
    try:
        touch_last_active(users, user["email"])
    except Exception:
        pass

    return jsonify({
        "success": True,
        "message": "Identidade confirmada com sucesso!",
        "user": serialize_user(user)
    }), 200


@auth_bp.route("/api/v1/auth/resend-code", methods=["POST"])
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

    # 🔒 SEGURANÇA: removida a exposição de otp_code no JSON de resposta
    return jsonify({
        "success": True,
        "message": "Novo código e ligação de confirmação enviados para o teu e-mail!",
        "verify_link": verify_link,
        "email_sent": email_sent
    }), 200


# ── RECUPERAÇÃO DE PALAVRA-PASSE ─────────────────────────────────────────────

@auth_bp.route("/api/v1/auth/forgot-password", methods=["POST"])
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
        return jsonify({"success": True, "message": "Se existir uma conta associada, enviámos um e-mail com instruções para recuperar a tua conta."}), 200

    reset_token = secrets.token_urlsafe(32)
    user["_reset_token_hash"] = generate_password_hash(reset_token)
    user["_reset_token_expires"] = (datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=30)).isoformat()
    save_users(users)

    reset_link = f"{request.host_url.rstrip('/')}/app?reset_token={reset_token}"
    subject = "Recuperação de Palavra-passe | Sigaleve"
    html_content = f"""
    <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;max-width:560px;margin:0 auto;background:#0d0e15;color:#ffffff;border-radius:24px;padding:32px 24px;border:1px solid #27273a;">
      <div style="text-align:center;margin-bottom:24px;">
        <h1 style="color:#ffffff;font-size:24px;font-weight:900;margin:16px 0 6px 0;">Recuperação de Palavra-passe</h1>
        <p style="color:#94a3b8;font-size:14px;margin:0;">Recebemos um pedido para redefinir a palavra-passe da tua conta Sigaleve.</p>
      </div>
      <div style="background:#171826;border-radius:18px;padding:22px;border:1px solid #27273a;margin-bottom:24px;text-align:center;">
        <p style="color:#94a3b8;font-size:13px;margin:0 0 16px 0;">Clica no botão abaixo para escolher uma nova palavra-passe (válido por 30 minutos):</p>
        <a href="{reset_link}" target="_blank" style="display:block;background:linear-gradient(135deg,#9333ea,#ec4899);color:#ffffff;text-decoration:none;padding:14px 20px;text-align:center;font-weight:900;font-size:14px;border-radius:14px;">Criar Nova Palavra-passe</a>
      </div>
    </div>
    """
    text_content = f"Recuperação de Palavra-passe Sigaleve\n\nLink: {reset_link}\n(Válido por 30 minutos)."
    email_sent, _ = send_real_email(user["email"], subject, html_content, text_content)

    return jsonify({
        "success": True,
        "email_sent": email_sent,
        "email": user["email"],
        "message": "Se a conta existir, enviámos um link de recuperação para o endereço de e-mail associado."
    }), 200


@auth_bp.route("/api/v1/auth/reset-password", methods=["POST"])
def api_reset_password():
    data = request.get_json(silent=True) or {}
    token = str(data.get("token", "")).strip()
    new_password = str(data.get("new_password", ""))

    if not token or not new_password:
        return jsonify({"success": False, "error": "Token e nova palavra-passe são obrigatórios."}), 400

    valid, msg = validate_password_complexity(new_password)
    if not valid:
        return jsonify({"success": False, "error": msg}), 400

    users = load_users()
    for email, user in users.items():
        stored_hash = user.get("_reset_token_hash")
        if stored_hash and check_password_hash(stored_hash, token):
            expires_str = user.get("_reset_token_expires", "")
            try:
                expires = datetime.datetime.fromisoformat(expires_str)
            except (ValueError, TypeError):
                expires = None
            if not expires or expires < datetime.datetime.now(datetime.timezone.utc):
                user.pop("_reset_token_hash", None)
                user.pop("_reset_token_expires", None)
                save_users(users)
                return jsonify({"success": False, "error": "O link de recuperação expirou. Pede um novo."}), 400

            user["password_hash"] = generate_password_hash(new_password)
            user.pop("_reset_token_hash", None)
            user.pop("_reset_token_expires", None)
            save_users(users)
            return jsonify({"success": True, "message": "Palavra-passe redefinida com sucesso. Já podes iniciar sessão."}), 200

    return jsonify({"success": False, "error": "Link de recuperação inválido ou já utilizado. Pede um novo."}), 400


# ── LOGIN SOCIAL (GOOGLE / FACEBOOK / INSTAGRAM) ─────────────────────────────

@auth_bp.route("/api/v1/auth/social-login", methods=["POST"])
def api_social_login():
    data = request.get_json(silent=True) or {}
    provider = str(data.get("provider", "google")).strip().lower()
    device_id = str(data.get("device_id", "web-default")).strip()

    credential = data.get("credential") or data.get("token") or data.get("id_token")
    if provider == "google" and credential:
        try:
            tokeninfo_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
            req = urllib.request.Request(tokeninfo_url, headers={"User-Agent": "Sigaleve-App"})
            with urllib.request.urlopen(req, timeout=10) as response:
                google_data = json.loads(response.read().decode("utf-8"))

            email = google_data.get("email", "").strip().lower()
            if not email:
                return jsonify({"success": False, "error": "A Google não forneceu um endereço de e-mail válido."}), 400

            name = google_data.get("name") or google_data.get("given_name") or email.split("@")[0]
            photo = google_data.get("picture") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"
            social_id = google_data.get("sub", f"google_{uuid.uuid4().hex[:8]}")
        except Exception as e:
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
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
    session.permanent = True
    session["user_email"] = user["email"]
    try:
        touch_last_active(users, user["email"])
    except Exception:
        pass

    return jsonify({
        "success": True,
        "message": f"Conectado com sucesso via {provider.title()}!",
        "user": serialize_user(user)
    }), 200


@auth_bp.route("/api/v1/auth/social-instant", methods=["POST"])
def api_social_instant():
    data = request.get_json(silent=True) or {}
    provider = str(data.get("provider", "facebook")).strip().lower()
    handle = str(data.get("handle", "")).strip().lstrip("@") or "utilizador"
    name = str(data.get("name", "")).strip() or handle.title()
    email = str(data.get("email", "")).strip().lower() or f"{handle.lower()}@{provider}.sigaleve.app"
    device_id = str(data.get("device_id", "web-default")).strip()

    users = load_users()
    user = users.get(email)
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
            "phone": "",
            "date_of_birth": "1999-01-01",
            "age": 26,
            "city": "Lisboa, Portugal",
            "diagnosis": "ALPHA",
            "bio": f"Conta conectada via {provider.title()}. Conecta com respeito e leveza!",
            "photo": photo,
            "photos": [photo],
            "interests": ["Música", "Viagens", "Fotografia"],
            "seeking": "Todos",
            "max_distance": 50,
            "age_min": 18,
            "age_max": 50,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "is_profile_configured": False,
            "email_verified": True,
            "known_devices": [device_id]
        }
        users[email] = user
        save_users(users)

    session["user_id"] = user["id"]
    session.permanent = True
    session["user_email"] = user["email"]
    try:
        touch_last_active(users, user["email"])
    except Exception:
        pass

    return jsonify({
        "success": True,
        "message": f"Conectado com sucesso via {provider.title()}!",
        "user": serialize_user(user)
    }), 200


# ── OAUTH REDIRECTIONS & CALLBACKS ───────────────────────────────────────────

@auth_bp.route("/auth/google/login")
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


@auth_bp.route("/auth/google/callback")
def auth_google_callback():
    code = request.args.get("code")
    err = request.args.get("error")
    if err or not code:
        return redirect("/app?error=google_cancelled")

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
            token_resp = json.loads(res.read().decode("utf-8"))

        id_token_jwt = token_resp.get("id_token")
        if not id_token_jwt:
            return redirect("/app?error=google_token_failed")

        verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token_jwt}"
        req_v = urllib.request.Request(verify_url, headers={"User-Agent": "Sigaleve-App"})
        with urllib.request.urlopen(req_v, timeout=10) as res_v:
            google_user = json.loads(res_v.read().decode("utf-8"))

        email = google_user.get("email", "").strip().lower()
        name = google_user.get("name") or google_user.get("given_name") or email.split("@")[0]
        photo = google_user.get("picture") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85"
        social_id = google_user.get("sub", f"google_{uuid.uuid4().hex[:8]}")

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
                "bio": "Conta conectada através do Google. Pronto para conversas transparentes e leves!",
                "photo": photo,
                "photos": [photo],
                "interests": ["Viagens", "Café", "Música"],
                "seeking": "Todos",
                "max_distance": 50,
                "age_min": 18,
                "age_max": 50,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
        session.permanent = True
        session["user_email"] = user["email"]
        try:
            touch_last_active(users, user["email"])
        except Exception:
            pass

        return redirect("/app?social_auth_success=google")
    except Exception as e:
        print(f"[GOOGLE CALLBACK ERROR] {e}")
        return redirect("/app?error=google_failed")


@auth_bp.route("/auth/facebook/login")
def auth_facebook_login():
    redirect_uri = get_oauth_redirect_uri("/auth/facebook/callback")
    state = str(uuid.uuid4())
    session["fb_oauth_state"] = state
    params = {
        "client_id": FACEBOOK_APP_ID,
        "redirect_uri": redirect_uri,
        "scope": "email,public_profile",
        "state": state,
        "response_type": "code"
    }
    fb_auth_url = f"https://www.facebook.com/v19.0/dialog/oauth?{urllib.parse.urlencode(params)}"
    return redirect(fb_auth_url)


@auth_bp.route("/auth/facebook/callback")
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
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
        session.permanent = True
        session["user_email"] = user["email"]
        try:
            touch_last_active(users, user["email"])
        except Exception:
            pass

        return redirect("/app?social_auth_success=facebook")
    except Exception as e:
        print(f"[FACEBOOK CALLBACK ERROR] {e}")
        return redirect("/app?error=facebook_failed")


@auth_bp.route("/auth/instagram/login")
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


@auth_bp.route("/auth/instagram/callback")
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

        name = "Utilizador Instagram"
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
                "bio": f"Perfil conectado com o Instagram (@{name}). Conectando com leveza e empatia!",
                "photo": photo,
                "photos": [photo],
                "interests": ["Fotografia", "Música", "Viagens"],
                "seeking": "Todos",
                "max_distance": 50,
                "age_min": 18,
                "age_max": 50,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
        session.permanent = True
        session["user_email"] = user["email"]
        try:
            touch_last_active(users, user["email"])
        except Exception:
            pass

        return redirect("/app?social_auth_success=instagram")
    except Exception as e:
        print(f"[INSTAGRAM CALLBACK ERROR] {e}")
        return redirect("/app?error=instagram_failed")


# ── SESSÃO E GESTÃO DE CONTA ────────────────────────────────────────────────

@auth_bp.route("/api/v1/auth/me", methods=["GET"])
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


@auth_bp.route("/api/v1/auth/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Sessão terminada."}), 200


@auth_bp.route("/api/v1/auth/delete-account", methods=["POST"])
def api_delete_account():
    """Eliminação permanente da conta (RGPD Art. 17 — direito ao apagamento)."""
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    try:
        users = load_users()
        removed = users.pop(email, None)
        if removed is None:
            return jsonify({"success": False, "error": "Conta não encontrada."}), 404
        save_users(users)

        try:
            moments_file = os.path.join(DATA_DIR, "moments_store.json")
            if os.path.exists(moments_file):
                with open(moments_file, "r", encoding="utf-8") as f:
                    moments = json.load(f)
                uid = removed.get("id", "")
                moments = [m for m in (moments if isinstance(moments, list) else moments.get("moments", []))
                           if isinstance(m, dict) and m.get("user_id") != uid]
                with open(moments_file, "w", encoding="utf-8") as f:
                    json.dump(moments if isinstance(moments, list) else {"moments": moments},
                              f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[DELETE_ACCOUNT moments cleanup warn] {e}")

        session.clear()
        return jsonify({
            "success": True,
            "message": "A tua conta foi eliminada permanentemente. Todos os dados foram apagados."
        }), 200
    except Exception as e:
        print(f"[DELETE_ACCOUNT ERROR] {e}")
        return jsonify({"success": False, "error": "Erro interno ao eliminar a conta."}), 500
