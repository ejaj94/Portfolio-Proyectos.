"""
routes/discovery.py — Blueprint para Descoberta de Perfis, Likes/Swipes mútuos,
ignorar (skip) e listagem de matches mútuos em tempo real.
"""
import datetime
from flask import Blueprint, request, jsonify, session

from services.common import (
    load_users,
    save_users,
    safe_photo,
    presence_label,
    load_json_store,
    MESSAGES_FILE,
)
from routes.push import send_push_to_user

discovery_bp = Blueprint("discovery_bp", __name__)


@discovery_bp.route("/api/v1/discover", methods=["GET"])
def api_discover():
    if not session.get("user_id"):
        return jsonify({"error": "Autenticação necessária"}), 401
    users = load_users()
    current_email = session.get("user_email")
    current_uid = session.get("user_id")
    real_profiles = []
    my_city = ((users.get(current_email, {}) or {}).get("city") or "").strip().lower()

    for email, u in users.items():
        uid = str(u.get("id") or email)
        if email == current_email or (current_uid and uid == str(current_uid)):
            continue

        photo = safe_photo(u, "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1000&q=85")
        photos_list = u.get("photos") if (u.get("photos") and len(u.get("photos")) > 0) else [photo]
        diag = u.get("diagnosis", "ALPHA")
        diag_code = diag[:1] if diag else "A"

        city = u.get("city") or "Lisboa, Portugal"
        if my_city and city.strip().lower() == my_city:
            km_label = "Perto de ti"
        else:
            km_label = city

        import html as _html

        def _safe_str(val, max_len=None):
            if not val or not isinstance(val, str):
                return "" if val is None else str(val)
            s = val[:max_len] if max_len else val
            return _html.escape(s)

        real_profiles.append({
            "id": uid,
            "name": _safe_str(u.get("display_name") or u.get("name") or "Utilizador", 60),
            "age": u.get("age", 25),
            "city": _safe_str(city, 80),
            "km": _safe_str(km_label, 80),
            "code": _safe_str(diag_code, 10),
            "activity": "Ativo agora",
            "photo": photo,
            "photos": photos_list,
            "bio": _safe_str(u.get("bio") or "Olá! Estou no Sigaleve para conexões reais, respeitosas e sem preconceito.", 1000),
            "relationship_goal": _safe_str(u.get("relationship_goal") or "Relação séria", 60),
            "zodiac": _safe_str(u.get("zodiac") or "", 30),
            "education": _safe_str(u.get("education") or "", 80),
            "height": _safe_str(u.get("height") or "", 20),
            "lifestyle": _safe_str(u.get("lifestyle") or "", 60),
            "profile_prompt": _safe_str(u.get("profile_prompt") or "", 250),
            "interests": [_safe_str(i, 40) for i in u.get("interests", ["Viagens", "Música"]) if isinstance(i, str)],
            "verified": bool(u.get("is_verified")),
            "is_real_user": True
        })

    excluded_ids = set()
    if current_email and current_email in users:
        u_data = users[current_email]
        raw_matches = u_data.get("matches", [])
        real_matches = [mid for mid in raw_matches if not str(mid).startswith("p") and not str(mid).startswith("mock_")]
        if len(real_matches) != len(raw_matches):
            u_data["matches"] = real_matches
            save_users(users)

        for mid in real_matches:
            excluded_ids.add(str(mid))

        for lid in u_data.get("likes_given", []):
            excluded_ids.add(str(lid))

        for sid in u_data.get("skipped", []):
            excluded_ids.add(str(sid))

    filtered_profiles = [p for p in real_profiles if str(p.get("id")) not in excluded_ids]

    return jsonify({"profiles": filtered_profiles}), 200


@discovery_bp.route("/api/v1/like", methods=["POST"])
def api_like():
    data = request.get_json(silent=True) or {}
    target_id = str(data.get("target_id", "")).strip()
    current_email = session.get("user_email")

    if not current_email:
        return jsonify({"matched": False, "error": "Autenticação necessária"}), 401
    if not target_id:
        return jsonify({"matched": False, "error": "Alvo inválido"}), 400

    users = load_users()
    if current_email not in users:
        return jsonify({"matched": False, "error": "Utilizador não encontrado"}), 404

    current_user = users[current_email]
    my_id = str(current_user.get("id") or current_email)

    if target_id.startswith("p") or target_id.startswith("mock_"):
        return jsonify({"matched": False, "message": "Perfil indisponível"}), 200

    target_user_record = None
    target_email = None
    for em, u in users.items():
        if str(u.get("id")) == str(target_id) or em == str(target_id):
            target_user_record = u
            target_email = em
            break

    if not target_user_record:
        return jsonify({"matched": False, "message": "Utilizador não encontrado"}), 404

    likes_given = current_user.setdefault("likes_given", [])
    if target_id not in likes_given:
        likes_given.append(target_id)

    target_likes = target_user_record.setdefault("likes_given", [])
    matched = (my_id in target_likes or current_email in target_likes)

    if matched:
        my_matches = current_user.setdefault("matches", [])
        if target_id not in my_matches:
            my_matches.append(target_id)

        target_matches = target_user_record.setdefault("matches", [])
        if my_id not in target_matches:
            target_matches.append(my_id)

    save_users(users)

    if matched:
        target_name = (current_user.get("display_name") or "Alguém")
        send_push_to_user(
            target_id,
            "É um Match! 💜",
            f"{target_name} também gostou de ti — abre a conversa!",
            "/app"
        )
        try:
            from app import socketio
            socketio.emit("match", {
                "with_user": {
                    "id": my_id,
                    "name": target_name,
                    "photo": safe_photo(current_user)
                },
                "message": "É um Match! 💜"
            }, to=f"user__{target_id}")
        except Exception:
            pass

    return jsonify({
        "matched": matched,
        "message": "É um Match! 💜" if matched else "Gosto enviado com sucesso!"
    }), 200


@discovery_bp.route("/api/v1/matches", methods=["GET"])
def api_get_matches():
    current_email = session.get("user_email")
    if not current_email:
        return jsonify({"error": "Autenticação necessária"}), 401

    users = load_users()
    if current_email not in users:
        return jsonify({"matches": []}), 200

    current_user = users[current_email]
    match_ids = current_user.get("matches", [])
    matches_list = []

    for mid in match_ids:
        mid_str = str(mid)
        if mid_str.startswith("p") or mid_str.startswith("mock_"):
            continue

        for em, u in users.items():
            if str(u.get("id")) == mid_str or em == mid_str:
                photo = safe_photo(u)
                peer_uid = str(u.get("id") or em)
                
                last_msg = "Novo match! Inicia a conversa 👋"
                msg_time = presence_label(u.get("last_active"))["label"] if u.get("show_recent_activity", True) else ""
                is_new = True
                try:
                    c_ids = sorted([str(current_user.get("id") or current_email), peer_uid])
                    conv_id = f"{c_ids[0]}__{c_ids[1]}"
                    all_msgs = load_json_store(MESSAGES_FILE, {}).get(conv_id, [])
                    if all_msgs and len(all_msgs) > 0:
                        lm = all_msgs[-1]
                        last_msg = lm.get("content", last_msg)
                        is_new = False
                        if lm.get("ts"):
                            try:
                                dt = datetime.datetime.fromisoformat(lm["ts"].replace("Z", "+00:00"))
                                msg_time = dt.strftime("%H:%M")
                            except Exception:
                                pass
                except Exception:
                    pass

                matches_list.append({
                    "id": peer_uid,
                    "name": u.get("display_name") or u.get("name") or "Utilizador",
                    "age": u.get("age", 25),
                    "city": u.get("city") or "Lisboa",
                    "photo": photo,
                    "code": (u.get("diagnosis") or "ALPHA")[:1],
                    "last_active": u.get("last_active"),
                    "presence": presence_label(u.get("last_active"))["label"] if u.get("show_recent_activity", True) else None,
                    "time": msg_time or "Agora",
                    "lastMsg": last_msg,
                    "isNew": is_new,
                    "is_real": True
                })
                break

    return jsonify({"matches": matches_list}), 200


@discovery_bp.route("/api/v1/skip", methods=["POST"])
def api_skip():
    data = request.get_json(silent=True) or {}
    target_id = str(data.get("target_id", "")).strip()
    current_email = session.get("user_email")
    if not current_email:
        return jsonify({"error": "Autenticação necessária"}), 401
    if current_email and target_id:
        users = load_users()
        if current_email in users:
            skipped_list = users[current_email].setdefault("skipped", [])
            if target_id not in skipped_list:
                skipped_list.append(target_id)
                save_users(users)
    return jsonify({"ok": True}), 200


@discovery_bp.route("/api/v1/profile/reset-skipped", methods=["POST"])
def api_reset_skipped():
    current_email = session.get("user_email")
    if not current_email:
        return jsonify({"error": "Autenticação necessária"}), 401
    users = load_users()
    if current_email not in users:
        return jsonify({"error": "Utilizador não encontrado"}), 404
    users[current_email]["skipped"] = []
    save_users(users)
    return jsonify({"ok": True}), 200
