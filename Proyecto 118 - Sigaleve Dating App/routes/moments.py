"""
routes/moments.py — Gestão de Momentos (histórias de 24 horas) e interações em fotos.
Inclui bloqueio de concorrência, purga automática de histórias expiradas e filtros anti-spam/doxxing.
"""
import uuid
import time
import threading
from flask import Blueprint, request, jsonify, session

from services.common import (
    load_json_store,
    save_json_store,
    load_users,
    validate_content_privacy,
    MOMENTS_FILE,
    PHOTO_INTERACTIONS_FILE,
)

moments_bp = Blueprint("moments_bp", __name__)

MOMENTS_LOCK = threading.Lock()
MOMENTS_TTL_SECONDS = 86400  # 24 horas
MOMENTS_PURGE_INTERVAL_SECONDS = 900  # 15 minutos
DEFAULT_MOMENTS = []


def purge_expired_moments() -> int:
    """
    Remove do disco os moments com mais de 24h, garantindo consistência
    através do lock compartilhado.
    """
    removed = 0
    try:
        with MOMENTS_LOCK:
            moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
            if not isinstance(moments, list):
                return 0
            now = time.time()
            valid_moments = []
            changed = False
            for m in moments:
                if not isinstance(m, dict):
                    removed += 1
                    changed = True
                    continue
                created_at = m.get("created_at")
                try:
                    created_at = float(created_at)
                    m["created_at"] = created_at
                except (TypeError, ValueError):
                    created_at = now
                    m["created_at"] = now
                    changed = True

                if (now - created_at) > MOMENTS_TTL_SECONDS:
                    removed += 1
                    changed = True
                    continue

                valid_moments.append(m)

            if changed:
                save_json_store(MOMENTS_FILE, valid_moments)
    except Exception as e:
        print(f"[MOMENTS PURGE ERROR] {e}")
    return removed


def _moments_purge_loop():
    """Loop daemon: expurga moments vencidos periodicamente."""
    while True:
        purge_expired_moments()
        time.sleep(MOMENTS_PURGE_INTERVAL_SECONDS)


def start_moments_purger():
    """Inicia thread de limpeza periódica de momentos expirados."""
    t = threading.Thread(target=_moments_purge_loop, daemon=True, name="MomentsPurger")
    t.start()


# ── INTERAÇÕES EM FOTOS DO PERFIL ───────────────────────────────────────────

@moments_bp.route("/api/v1/photos/like", methods=["POST"])
def api_photo_like():
    data = request.get_json(silent=True) or {}
    photo_id = str(data.get("photo_id", "")).strip()
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401

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


@moments_bp.route("/api/v1/photos/comment", methods=["POST"])
def api_photo_comment():
    data = request.get_json(silent=True) or {}
    photo_id = str(data.get("photo_id", "")).strip()
    comment_text = str(data.get("comment") or data.get("text") or "").strip()
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    user_name = session.get("user_name") or "Utilizador"
    user_avatar = session.get("user_photo") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"

    if not photo_id or not comment_text:
        return jsonify({"success": False, "error": "O comentário não pode estar vazio."}), 400

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


@moments_bp.route("/api/v1/photos/comments", methods=["GET"])
def api_get_photo_comments():
    photo_id = request.args.get("photo_id", "")
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    store = load_json_store(PHOTO_INTERACTIONS_FILE, {})
    p_data = store.get(photo_id, {"likes": [], "comments": []})

    return jsonify({
        "success": True,
        "likes_count": len(p_data.get("likes", [])),
        "user_has_liked": current_uid in p_data.get("likes", []),
        "comments": p_data.get("comments", [])
    })


# ── MOMENTOS / HISTÓRIAS EFÉMERAS ──────────────────────────────────────────

@moments_bp.route("/api/v1/moments", methods=["GET"])
def api_get_moments():
    if not session.get("user_id"):
        return jsonify({"error": "Autenticação necessária"}), 401
    raw_moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    current_uid = str(session.get("user_id"))
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

    for m in raw_moments:
        created_at = m.get("created_at")
        if created_at is None:
            created_at = now
            m["created_at"] = now
        try:
            created_at = float(created_at)
        except (ValueError, TypeError):
            created_at = now

        if (now - created_at) > 86400:
            has_expired = True
            continue

        valid_moments.append(m)

    if has_expired:
        with MOMENTS_LOCK:
            save_json_store(MOMENTS_FILE, valid_moments)

    enriched_moments = []
    for m in valid_moments:
        author_id = str(m.get("user_id", ""))
        is_own = (author_id == current_uid)
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


@moments_bp.route("/api/v1/moments", methods=["POST"])
def api_create_moment():
    data = request.get_json(silent=True) or {}
    text_content = str(data.get("text", "")).strip()
    mood = str(data.get("mood", "☕ A relaxar")).strip()
    mood_emoji = str(data.get("mood_emoji", "☕")).strip()
    photo = str(data.get("photo_url", data.get("photo", ""))).strip()
    
    photos_raw = data.get("photos")
    photos = []
    if isinstance(photos_raw, list):
        photos = [str(p).strip() for p in photos_raw if str(p).strip()]
        photos = photos[:5]
    if photo and photo not in photos:
        photos.insert(0, photo)

    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    user_name = str(data.get("user_name") or session.get("user_name") or "Eu")
    user_avatar = str(data.get("user_avatar") or session.get("user_photo") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80")
    user_city = str(session.get("user_city") or "Lisboa")

    if not text_content and not photos:
        return jsonify({"success": False, "error": "Escreve um pensamento ou partilha uma foto/vídeo da tua história."}), 400

    if len(text_content) > 1000:
        return jsonify({"success": False, "error": "A tua publicação deve ter no máximo 1000 caracteres."}), 400

    is_safe, error_msg = validate_content_privacy(text_content)
    if not is_safe:
        return jsonify({
            "success": False,
            "error": error_msg,
            "security_blocked": True
        }), 400

    now = float(time.time())
    with MOMENTS_LOCK:
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
            "photo": photos[0] if photos else "",
            "photo_url": photos[0] if photos else "",
            "photos": photos,
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


@moments_bp.route("/api/v1/moments/react", methods=["POST"])
def api_react_moment():
    data = request.get_json(silent=True) or {}
    moment_id = data.get("moment_id")
    raw_reaction = str(data.get("reaction", "heart")).strip().lower()

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

    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401

    with MOMENTS_LOCK:
        moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
        target = None
        for m in moments:
            if m["id"] == moment_id:
                target = m
                break

        if not target:
            return jsonify({"success": False, "error": "Momento não encontrado."}), 404

        rx = target.setdefault("reactions", {})
        for k in ALLOWED_RX:
            if k not in rx:
                rx[k] = 0
        if "❤️" in rx:
            rx["heart"] = rx.get("heart", 0) + rx.pop("❤️")
        if "✨" in rx:
            rx["hug"] = rx.get("hug", 0) + rx.pop("✨")

        user_rx = target.setdefault("user_reactions", {})
        prev_reaction = user_rx.get(current_uid)

        if prev_reaction == reaction:
            rx[reaction] = max(0, rx.get(reaction, 0) - 1)
            user_rx.pop(current_uid, None)
            active_reaction = None
        else:
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


@moments_bp.route("/api/v1/moments/comment", methods=["POST"])
def api_moment_comment():
    data = request.get_json(silent=True) or {}
    moment_id = str(data.get("moment_id", "")).strip()
    comment_text = str(data.get("text") or data.get("comment") or "").strip()

    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    user_name = session.get("user_name") or "Utilizador"
    user_avatar = session.get("user_photo") or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"

    if not moment_id or not comment_text:
        return jsonify({"success": False, "error": "O comentário não pode estar vazio."}), 400
    if len(comment_text) > 500:
        return jsonify({"success": False, "error": "Comentário demasiado longo (máx. 500 caracteres)."}), 400

    with MOMENTS_LOCK:
        moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
        target = next((m for m in moments if m["id"] == moment_id), None)
        if not target:
            return jsonify({"success": False, "error": "Momento não encontrado."}), 404

        users = load_users()
        me = users.get(session.get("user_email") or "", {})
        author_id = target.get("user_id")
        if str(author_id) != str(current_uid):
            my_matches = me.get("matches") or []
            if author_id not in my_matches:
                return jsonify({"success": False, "error": "Só podes comentar histórias de matches."}), 403

        is_safe, error_msg = validate_content_privacy(comment_text)
        if not is_safe:
            return jsonify({"success": False, "error": error_msg, "security_blocked": True}), 400

        new_comment = {
            "id": f"c_{uuid.uuid4().hex[:8]}",
            "user_id": current_uid,
            "user_name": user_name,
            "user_avatar": user_avatar,
            "text": comment_text,
            "timestamp": "Agora mesmo"
        }
        target.setdefault("comments", []).append(new_comment)
        save_json_store(MOMENTS_FILE, moments)

    return jsonify({
        "success": True,
        "message": "Comentário publicado com sucesso!",
        "comment": new_comment,
        "total_comments": len(target["comments"])
    }), 201


@moments_bp.route("/api/v1/moments/comments", methods=["GET"])
def api_get_moment_comments():
    moment_id = request.args.get("moment_id", "")
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401

    moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
    target = next((m for m in moments if m["id"] == moment_id), None)
    if not target:
        return jsonify({"success": False, "error": "Momento não encontrado."}), 404

    if str(target.get("user_id")) != str(current_uid):
        users = load_users()
        me = users.get(session.get("user_email") or "", {})
        if target.get("user_id") not in (me.get("matches") or []):
            return jsonify({"success": False, "error": "Só podes ver comentários de matches."}), 403

    return jsonify({
        "success": True,
        "comments": target.get("comments", [])
    })


@moments_bp.route("/api/v1/moments/<moment_id>", methods=["PUT"])
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

    with MOMENTS_LOCK:
        moments = load_json_store(MOMENTS_FILE, DEFAULT_MOMENTS)
        target = None
        for m in moments:
            if m.get("id") == moment_id:
                target = m
                break

        if not target:
            return jsonify({"success": False, "error": "Momento não encontrado."}), 404

        target_owner = str(target.get("user_id") or "")
        if target_owner and target_owner != current_uid:
            return jsonify({"success": False, "error": "Não tens permissão para editar esta publicação."}), 403

        try:
            target["created_at"] = float(target.get("created_at"))
        except (TypeError, ValueError):
            target["created_at"] = float(time.time())

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


@moments_bp.route("/api/v1/moments/<moment_id>", methods=["DELETE"])
def api_delete_moment(moment_id):
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401
    with MOMENTS_LOCK:
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
