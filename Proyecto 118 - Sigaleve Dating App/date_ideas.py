# ============================================================
# SIGALEVE — ENCONTROS GRUPAIS COM AMIGOS (Exclusivo Sigaleve Plus)
# ============================================================
# Sem propostas pré-fabricadas da Equipa Sigaleve (começa vazio).
# Funcionalidade exclusiva para membros com subscrição Sigaleve Plus ativa:
#   - GET  /api/v1/date-ideas            → lista encontros reais criados por membros
#   - POST /api/v1/date-ideas            → membro Sigaleve Plus propõe encontro
#   - POST /api/v1/date-ideas/<id>/attend→ presença secreta (apenas Sigaleve Plus)
#   - POST /api/v1/date-ideas/<id>/like  → toggle de like (apenas Sigaleve Plus)
#   - DELETE /api/v1/date-ideas/<id>     → autor apaga o seu encontro
# ============================================================
import os as _os
import time as _time
import uuid as _uuid
import threading as _threading
from datetime import datetime as _datetime
from flask import request as _request, jsonify as _jsonify

DATA_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data")
DATE_IDEAS_FILE = _os.path.join(DATA_DIR, "date_ideas_store.json")
DATE_IDEAS_LOCK = _threading.Lock()

CATEGORIES = ["cafe", "passeio", "cultura", "natureza", "comida", "noite"]

CATEGORY_LABELS = {
    "cafe": {"pt": "☕ Café & Conversa", "emoji": "☕"},
    "passeio": {"pt": "🚶 Passeio", "emoji": "🚶"},
    "cultura": {"pt": "🎭 Cultura", "emoji": "🎭"},
    "natureza": {"pt": "🌿 Natureza", "emoji": "🌿"},
    "comida": {"pt": "🍽️ Comida", "emoji": "🍽️"},
    "noite": {"pt": "🌙 Fim de Noite", "emoji": "🌙"},
}

SEED_IDEAS = []


def _validate_idea(text: str):
    """Reutiliza o validate_content_privacy do preview_server (injetado)."""
    return _validate_idea_fn(text)  # noqa: F821 — injetado pelo init


_validate_idea_fn = None


def init_date_ideas(app, session, load_json_store, save_json_store, validate_content_privacy_fn, load_users_fn=None, safe_photo_fn=None):
    """Registra as rotas de encontros grupais (exclusivo Sigaleve Plus, sem seeds da equipa)."""
    global _validate_idea_fn
    _validate_idea_fn = validate_content_privacy_fn
    lock = DATE_IDEAS_LOCK

    def _is_user_subscribed():
        """Verifica no servidor se o utilizador autenticado tem subscrição Sigaleve Plus ativa. (Desbloqueado temporariamente para testes)"""
        return True

    def _load():
        data = load_json_store(DATE_IDEAS_FILE, None)
        if data is None or not isinstance(data, list):
            data = []
            save_json_store(DATE_IDEAS_FILE, data)
            return data

        # Remover todas as propostas antigas da Equipa Sigaleve (seed: True ou author_id == 'sigaleve')
        cleaned = [
            item for item in data
            if not item.get("seed")
            and item.get("author_id") != "sigaleve"
            and item.get("author_name") != "Equipa Sigaleve"
            and not str(item.get("id", "")).startswith("di_seed_")
        ]
        if len(cleaned) != len(data):
            data = cleaned
            save_json_store(DATE_IDEAS_FILE, data)
        return data

    def _get_user_info(uid=None, email=None):
        name = "Membro Sigaleve"
        photo = ""
        try:
            if load_users_fn:
                users = load_users_fn() or {}
                u = None
                if email and email in users:
                    u = users.get(email)
                if not u and uid:
                    for record in users.values():
                        if isinstance(record, dict) and str(record.get("id")) == str(uid):
                            u = record
                            break
                if u:
                    name = u.get("display_name") or u.get("name") or name
                    photo = u.get("photo") or ""
        except Exception:
            pass
        if not photo:
            photo = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"
        return name, photo

    def _serialize(idea, current_uid):
        likes = idea.get("likes") or {}
        attendees = idea.get("attendees") or {}
        comments = idea.get("comments") or []
        
        # Obter nome e avatar atualizados do organizador
        author_name = idea.get("author_name") or "Organizador"
        author_avatar = idea.get("author_avatar") or ""
        if not author_avatar or author_name in ("Utilizador", "Organizador"):
            res_name, res_photo = _get_user_info(idea.get("author_id"))
            if res_name:
                author_name = res_name
            if res_photo:
                author_avatar = res_photo

        serialized_comments = []
        for c in comments:
            c_uid = str(c.get("user_id") or "")
            serialized_comments.append({
                "id": c.get("id", ""),
                "user_id": c_uid,
                "user_name": c.get("user_name") or "Membro Sigaleve",
                "user_avatar": c.get("user_avatar") or "",
                "text": c.get("text", ""),
                "created_at": c.get("created_at", 0),
                "mine": bool(current_uid and c_uid == str(current_uid))
            })

        return {
            "id": idea["id"],
            "title": idea["title"],
            "description": idea["description"],
            "category": idea["category"],
            "category_label": CATEGORY_LABELS.get(idea["category"], {"pt": idea["category"], "emoji": "💡"})["pt"],
            "country": idea.get("country", "Portugal"),
            "city": idea.get("city", ""),
            "event_date_iso": idea.get("event_date_iso", ""),
            "event_time_iso": idea.get("event_time_iso", ""),
            "event_date": idea.get("event_date", ""),
            "author_id": idea.get("author_id", ""),
            "author_name": author_name,
            "author_avatar": author_avatar,
            "mine": idea.get("author_id") == current_uid,
            "seed": False,
            "likes_count": len(likes),
            "my_like": bool(current_uid and likes.get(str(current_uid))),
            "attendees_count": len(attendees),
            "my_attending": bool(current_uid and attendees.get(str(current_uid))),
            "comments": serialized_comments,
            "comments_count": len(comments),
            "created_at": idea.get("created_at", 0),
        }

    @app.route("/api/v1/date-ideas", methods=["GET"])
    def api_date_ideas_list():
        if not session.get("user_id"):
            return _jsonify({"error": "Autenticação necessária"}), 401
        if not _is_user_subscribed():
            return _jsonify({
                "success": False,
                "subscription_required": True,
                "error": "Encontros Grupais com Amigos é uma funcionalidade exclusiva para membros com subscrição Sigaleve Plus.",
                "categories": CATEGORY_LABELS,
                "ideas": [],
            }), 403
        current_uid = str(session.get("user_id"))
        cat = (_request.args.get("category") or "").strip().lower()
        country_filter = (_request.args.get("country") or "").strip()
        with lock:
            ideas = _load()
            out = []
            for idea in ideas:
                if cat and cat != "todas" and idea.get("category") != cat:
                    continue
                if country_filter and country_filter.lower() != "todos" and idea.get("country", "Portugal") != country_filter:
                    continue
                out.append(_serialize(idea, current_uid))
        out.sort(key=lambda x: (-x["attendees_count"], -x["likes_count"], -x["created_at"]))
        return _jsonify({"success": True, "categories": CATEGORY_LABELS, "ideas": out}), 200

    @app.route("/api/v1/date-ideas", methods=["POST"])
    def api_date_ideas_create():
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        if not _is_user_subscribed():
            return _jsonify({
                "success": False,
                "subscription_required": True,
                "error": "Apenas membros com subscrição Sigaleve Plus podem propor Encontros Grupais.",
            }), 403
        current_uid = str(session.get("user_id"))
        data = _request.get_json(silent=True) or {}
        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()
        category = str(data.get("category", "cafe")).strip().lower()
        country = str(data.get("country", "")).strip()
        city = str(data.get("city", "")).strip()
        event_date_iso = str(data.get("event_date_iso", "")).strip()
        event_time_iso = str(data.get("event_time_iso", "")).strip()

        if not title or not description:
            return _jsonify({"success": False, "error": "Preenche o título e a descrição do encontro."}), 400
        if not country or not city:
            return _jsonify({"success": False, "error": "Seleciona obrigatoriamente o País e a Cidade na lista oficial."}), 400
        if not event_date_iso or not event_time_iso:
            return _jsonify({"success": False, "error": "Seleciona uma Data e uma Hora exatas para o encontro."}), 400

        # Validar formato estrito de Data (YYYY-MM-DD) e Hora (HH:MM) e impedir datas no passado
        try:
            dt_obj = _datetime.strptime(f"{event_date_iso} {event_time_iso}", "%Y-%m-%d %H:%M")
            now_dt = _datetime.now()
            if dt_obj < now_dt:
                return _jsonify({"success": False, "error": "A data e hora do encontro não podem estar no passado. Escolhe uma data futura."}), 400
            if (dt_obj - now_dt).days > 365:
                return _jsonify({"success": False, "error": "A data do encontro deve ser dentro dos próximos 12 meses."}), 400
            event_date_formatted = f"{dt_obj.strftime('%d/%m/%Y')} às {dt_obj.strftime('%H:%M')}"
        except ValueError:
            return _jsonify({"success": False, "error": "Formato de data ou hora inválido. Usa o seletor de calendário e relógio."}), 400

        if len(title) > 120:
            return _jsonify({"success": False, "error": "O título deve ter no máximo 120 caracteres."}), 400
        if len(description) > 800:
            return _jsonify({"success": False, "error": "A descrição deve ter no máximo 800 caracteres."}), 400
        if category not in CATEGORIES:
            category = "cafe"
        combined = f"{title}. {description}"
        is_safe, error_msg = validate_content_privacy_fn(combined)
        if not is_safe:
            return _jsonify({"success": False, "error": error_msg, "security_blocked": True}), 400

        import html as _html
        clean_title = _html.escape(title)
        clean_description = _html.escape(description)

        author_name, author_avatar = _get_user_info(uid=current_uid, email=session.get("user_email"))
        new_idea = {
            "id": f"di_{_uuid.uuid4().hex[:8]}",
            "title": clean_title,
            "description": clean_description,
            "category": category,
            "country": country,
            "city": city,
            "event_date_iso": event_date_iso,
            "event_time_iso": event_time_iso,
            "event_date": event_date_formatted,
            "author_id": current_uid,
            "author_name": author_name,
            "author_avatar": author_avatar,
            "likes": {},
            "attendees": {current_uid: True},
            "comments": [],
            "seed": False,
            "created_at": _time.time(),
        }
        with lock:
            ideas = _load()
            ideas.insert(0, new_idea)
            save_json_store(DATE_IDEAS_FILE, ideas)
        return _jsonify({"success": True, "message": "Encontro grupal partilhado com a comunidade! 💜", "idea": _serialize(new_idea, current_uid)}), 201

    @app.route("/api/v1/date-ideas/<idea_id>/attend", methods=["POST"])
    def api_date_ideas_attend(idea_id):
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        if not _is_user_subscribed():
            return _jsonify({
                "success": False,
                "subscription_required": True,
                "error": "Apenas membros Sigaleve Plus podem confirmar presença secreta em encontros grupais.",
            }), 403
        current_uid = str(session.get("user_id"))
        with lock:
            ideas = _load()
            idea = next((i for i in ideas if i["id"] == idea_id), None)
            if not idea:
                return _jsonify({"success": False, "error": "Encontro não encontrado."}), 404
            attendees = idea.setdefault("attendees", {})
            if attendees.get(current_uid):
                del attendees[current_uid]
                attending = False
            else:
                attendees[current_uid] = True
                attending = True
            save_json_store(DATE_IDEAS_FILE, ideas)
        return _jsonify({
            "success": True,
            "attending": attending,
            "attendees_count": len(idea.get("attendees", {})),
        }), 200

    @app.route("/api/v1/date-ideas/<idea_id>/like", methods=["POST"])
    def api_date_ideas_like(idea_id):
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        if not _is_user_subscribed():
            return _jsonify({
                "success": False,
                "subscription_required": True,
                "error": "Funcionalidade exclusiva para membros Sigaleve Plus.",
            }), 403
        current_uid = str(session.get("user_id"))
        with lock:
            ideas = _load()
            idea = next((i for i in ideas if i["id"] == idea_id), None)
            if not idea:
                return _jsonify({"success": False, "error": "Ideia não encontrada."}), 404
            likes = idea.setdefault("likes", {})
            if likes.get(current_uid):
                del likes[current_uid]
                liked = False
            else:
                likes[current_uid] = True
                liked = True
            save_json_store(DATE_IDEAS_FILE, ideas)
        return _jsonify({"success": True, "liked": liked, "likes_count": len(idea.get("likes", {}))}), 200

    @app.route("/api/v1/date-ideas/<idea_id>", methods=["DELETE"])
    def api_date_ideas_delete(idea_id):
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        current_uid = str(session.get("user_id"))
        with lock:
            ideas = _load()
            idea = next((i for i in ideas if i["id"] == idea_id), None)
            if not idea:
                return _jsonify({"success": False, "error": "Ideia não encontrada."}), 404
            if idea.get("author_id") != current_uid:
                return _jsonify({"success": False, "error": "Só podes apagar os teus próprios encontros."}), 403
            ideas = [i for i in ideas if i["id"] != idea_id]
            save_json_store(DATE_IDEAS_FILE, ideas)
        return _jsonify({"success": True, "message": "Encontro removido."}), 200

    @app.route("/api/v1/date-ideas/<idea_id>/comments", methods=["POST"])
    def api_date_ideas_comment(idea_id):
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        current_uid = str(session.get("user_id"))
        data = _request.get_json(silent=True) or {}
        text = str(data.get("text", "")).strip()
        if not text:
            return _jsonify({"success": False, "error": "Escreve um comentário antes de enviar."}), 400
        if len(text) > 400:
            return _jsonify({"success": False, "error": "O comentário deve ter no máximo 400 caracteres."}), 400

        is_safe, error_msg = validate_content_privacy_fn(text)
        if not is_safe:
            return _jsonify({"success": False, "error": error_msg, "security_blocked": True}), 400

        import html as _html
        clean_text = _html.escape(text)

        user_name, user_avatar = _get_user_info(uid=current_uid, email=session.get("user_email"))

        new_comment = {
            "id": f"dic_{_uuid.uuid4().hex[:8]}",
            "user_id": current_uid,
            "user_name": user_name,
            "user_avatar": user_avatar,
            "text": clean_text,
            "created_at": _time.time(),
        }

        with lock:
            ideas = _load()
            idea = next((i for i in ideas if i["id"] == idea_id), None)
            if not idea:
                return _jsonify({"success": False, "error": "Encontro não encontrado."}), 404
            comments = idea.setdefault("comments", [])
            comments.append(new_comment)
            save_json_store(DATE_IDEAS_FILE, ideas)
            comments_count = len(comments)

        return _jsonify({
            "success": True,
            "comment": {
                **new_comment,
                "mine": True
            },
            "comments_count": comments_count
        }), 201

    @app.route("/api/v1/date-ideas/<idea_id>/comments/<comment_id>", methods=["DELETE"])
    def api_date_ideas_delete_comment(idea_id, comment_id):
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        current_uid = str(session.get("user_id"))
        with lock:
            ideas = _load()
            idea = next((i for i in ideas if i["id"] == idea_id), None)
            if not idea:
                return _jsonify({"success": False, "error": "Encontro não encontrado."}), 404
            comments = idea.get("comments") or []
            target = next((c for c in comments if c.get("id") == comment_id), None)
            if not target:
                return _jsonify({"success": False, "error": "Comentário não encontrado."}), 404
            # Apenas o autor do comentário ou o organizador do encontro pode apagar
            if str(target.get("user_id")) != current_uid and str(idea.get("author_id")) != current_uid:
                return _jsonify({"success": False, "error": "Sem permissão para apagar este comentário."}), 403
            idea["comments"] = [c for c in comments if c.get("id") != comment_id]
            save_json_store(DATE_IDEAS_FILE, ideas)
            comments_count = len(idea["comments"])

        return _jsonify({"success": True, "comments_count": comments_count}), 200

    return {"routes": ["GET/POST date-ideas", "attend", "like", "delete", "comments"], "seed_count": 0}
