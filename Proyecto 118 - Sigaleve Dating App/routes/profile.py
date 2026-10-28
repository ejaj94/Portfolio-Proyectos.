"""
routes/profile.py — Blueprint para Perfil de Utilizador, Consulta, Atualização,
Upload de Fotos (com limite estrito de 8MB) e Verificação Facial por Selfie.
"""
import os
import re
import uuid
import base64
import binascii
import datetime
from flask import Blueprint, request, jsonify, session, send_from_directory

from services.common import (
    load_users,
    save_users,
    serialize_user,
    safe_photo,
    presence_label,
    UPLOAD_DIR,
    MAX_UPLOAD_BYTES,
    ALLOWED_UPLOAD_TYPES,
)

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/uploads/<path:filename>")
def serve_upload(filename):
    """Serve fotos guardadas em data/uploads/ de forma segura."""
    return send_from_directory(UPLOAD_DIR, filename, max_age=86400)


@profile_bp.route("/api/v1/photo/upload", methods=["POST"])
def api_upload_photo():
    """Upload de foto (multipart ou base64) para data/uploads/ com validação estrita."""
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401

    raw = None
    ext = None
    f = request.files.get("photo")
    if f and f.filename:
        mime = (f.mimetype or "").lower()
        ext = ALLOWED_UPLOAD_TYPES.get(mime)
        if not ext:
            return jsonify({"success": False, "error": "Tipo não suportado (use JPG, PNG, WebP ou GIF)."}), 415
        f.stream.seek(0, 2)
        size = f.stream.tell()
        f.stream.seek(0)
        if size > MAX_UPLOAD_BYTES:
            return jsonify({"success": False, "error": "Foto maior que 8 MB."}), 413
        raw = f.read()
    else:
        data = request.get_json(silent=True) or {}
        durl = str(data.get("photo_data_url") or "")
        m = re.match(r"^data:image/(png|jpeg|jpg|webp|gif);base64,(.+)$", durl, re.S)
        if not m:
            return jsonify({"success": False, "error": "Ficheiro ausente ou formato inválido."}), 400
        try:
            raw = base64.b64decode(m.group(2), validate=False)
        except (binascii.Error, ValueError):
            return jsonify({"success": False, "error": "base64 inválido."}), 400
        ext = {"png": ".png", "jpeg": ".jpg", "jpg": ".jpg", "webp": ".webp", "gif": ".gif"}[m.group(1)]
        if len(raw) > MAX_UPLOAD_BYTES:
            return jsonify({"success": False, "error": "Foto maior que 8 MB."}), 413

    name = f"{uuid.uuid4().hex}{ext}"
    with open(os.path.join(UPLOAD_DIR, name), "wb") as out:
        out.write(raw)
    return jsonify({"success": True, "url": f"/uploads/{name}"}), 201


@profile_bp.route("/api/v1/profile/update", methods=["POST"])
def api_update_profile():
    """Atualização segura do perfil do utilizador autenticado (sem fallback insecure em email)."""
    data = request.get_json(silent=True) or {}
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada ou expirada."}), 401

    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    import html as _html

    text_fields_to_validate = []
    if "display_name" in data and str(data["display_name"]).strip():
        val = str(data["display_name"]).strip()
        text_fields_to_validate.append(val)
        user["display_name"] = _html.escape(val[:60])
    if "phone" in data:
        user["phone"] = _html.escape(str(data["phone"]).strip()[:30])
    if "city" in data and str(data["city"]).strip():
        val = str(data["city"]).strip()
        text_fields_to_validate.append(val)
        user["city"] = _html.escape(val[:80])
    if "bio" in data:
        val = str(data["bio"]).strip()
        text_fields_to_validate.append(val)
        user["bio"] = _html.escape(val[:1000])
    if "photo" in data and str(data["photo"]).strip():
        user["photo"] = str(data["photo"]).strip()
        if "photos" not in user or not user["photos"]:
            user["photos"] = [user["photo"]]
        else:
            if user["photo"] not in user["photos"]:
                user["photos"].insert(0, user["photo"])
    if "interests" in data and isinstance(data["interests"], list):
        user["interests"] = [_html.escape(str(i).strip()[:40]) for i in data["interests"] if str(i).strip()]
    if "diagnosis" in data and str(data["diagnosis"]).strip():
        user["diagnosis"] = _html.escape(str(data["diagnosis"]).strip()[:40])
    if "custom_diagnosis" in data:
        user["custom_diagnosis"] = _html.escape(str(data["custom_diagnosis"]).strip()[:60])
    if "relationship_goal" in data and str(data["relationship_goal"]).strip():
        user["relationship_goal"] = _html.escape(str(data["relationship_goal"]).strip()[:60])
    if "zodiac" in data:
        user["zodiac"] = _html.escape(str(data["zodiac"]).strip()[:30])
    if "education" in data:
        user["education"] = _html.escape(str(data["education"]).strip()[:80])
    if "height" in data:
        user["height"] = _html.escape(str(data["height"]).strip()[:20])
    if "lifestyle" in data:
        user["lifestyle"] = _html.escape(str(data["lifestyle"]).strip()[:60])
    if "profile_prompt" in data:
        val = str(data["profile_prompt"]).strip()
        text_fields_to_validate.append(val)
        user["profile_prompt"] = _html.escape(val[:250])
    if "seeking" in data:
        user["seeking"] = _html.escape(str(data["seeking"]).strip()[:30])
    if "max_distance" in data:
        try:
            user["max_distance"] = int(data["max_distance"])
        except ValueError:
            pass

    # Validar se algum campo contém tentativas de injeção XSS ou dados proibidos
    from services.common import validate_content_privacy
    for text_sample in text_fields_to_validate:
        is_safe, error_msg = validate_content_privacy(text_sample)
        if not is_safe:
            return jsonify({"success": False, "error": error_msg}), 400

    user["is_profile_configured"] = True
    users[email] = user
    save_users(users)

    return jsonify({
        "success": True,
        "message": "Perfil atualizado com sucesso!",
        "user": serialize_user(user)
    }), 200


@profile_bp.route("/api/v1/user/<uid>", methods=["GET"])
def api_get_user_profile(uid):
    """Consulta segura do perfil de outro membro."""
    if not session.get("user_id"):
        return jsonify({"error": "Autenticação necessária"}), 401
    users = load_users()
    cur_email = session.get("user_email")
    my_city = ((users.get(cur_email, {}) or {}).get("city") or "").strip().lower()

    for email, u in users.items():
        if str(u.get("id")) == str(uid) or email == str(uid):
            photo = safe_photo(u, "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85")
            photos_list = u.get("photos") if (u.get("photos") and len(u.get("photos")) > 0) else [photo]
            diag = u.get("diagnosis", "ALPHA")
            diag_code = diag[:1] if diag else "A"
            city = u.get("city") or "Lisboa, Portugal"
            km_label = "Perto de ti" if (my_city and city.strip().lower() == my_city) else city
            return jsonify({
                "profile": {
                    "id": str(u.get("id") or email),
                    "name": u.get("display_name") or u.get("name") or "Utilizador",
                    "age": u.get("age", 25),
                    "city": city,
                    "km": km_label,
                    "code": diag_code,
                    "last_active": u.get("last_active"),
                    "presence": presence_label(u.get("last_active"))["label"] if u.get("show_recent_activity", True) else None,
                    "activity": presence_label(u.get("last_active"))["label"] if u.get("show_recent_activity", True) else "",
                    "photo": photo,
                    "photos": photos_list,
                    "bio": u.get("bio") or "Olá! Estou no Sigaleve para conexões reais, respeitosas e sem preconceito.",
                    "relationship_goal": u.get("relationship_goal") or "Relação séria",
                    "zodiac": u.get("zodiac") or "",
                    "education": u.get("education") or "",
                    "height": u.get("height") or "",
                    "lifestyle": u.get("lifestyle") or "",
                    "interests": u.get("interests", ["Viagens", "Música"]),
                    "verified": bool(u.get("is_verified")),
                    "is_real_user": True
                }
            }), 200

    return jsonify({"error": "Perfil não encontrado"}), 404


@profile_bp.route("/api/v1/verify/selfie", methods=["POST"])
def api_verify_selfie():
    """Verificação biométrica facial através de comparação de selfie."""
    import face_verify as fv

    if not fv.is_available():
        return jsonify({
            "success": False,
            "available": False,
            "error": "Verificação por selfie indisponível neste momento. Tenta novamente mais tarde."
        }), 503

    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401

    data = request.get_json(silent=True) or {}
    selfie = data.get("selfie")
    if not selfie or not str(selfie).startswith("data:image"):
        return jsonify({"success": False, "error": "Selfie inválida. Captura uma foto com a câmara."}), 400

    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({"success": False, "error": "Utilizador não encontrado."}), 404

    profile_photos = [p for p in (user.get("photos") or []) if p] or ([user.get("photo")] if user.get("photo") else [])
    if not profile_photos:
        return jsonify({"success": False, "error": "Adiciona primeiro pelo menos uma foto de perfil com o teu rosto visível."}), 400

    ok, msg, detail = fv.verify_selfie_vs_profile(selfie, profile_photos)
    if ok:
        user["is_verified"] = True
        user["verified_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        users[email] = user
        save_users(users)

    return jsonify({
        "success": ok,
        "message": msg,
        "verified": ok,
        "detail": {k: v for k, v in detail.items() if k != "available"},
    }), (200 if ok else 422)


@profile_bp.route("/api/v1/verify/status", methods=["GET"])
def api_verify_status():
    import face_verify as fv
    email = session.get("user_email")
    if not email:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    users = load_users()
    user = users.get(email) or {}
    return jsonify({
        "success": True,
        "verified": bool(user.get("is_verified")),
        "available": fv.is_available()
    }), 200
