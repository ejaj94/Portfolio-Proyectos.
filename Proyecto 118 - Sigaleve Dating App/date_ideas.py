# ============================================================
# SIGALEVE — IDEIAS DE 1º ENCONTRO (UGC + likes)
# ============================================================
# Feature #1 da análise de concorrentes (MPWH tem secção dedicada;
# PS tem fóruns de dates). Fluxo:
#   - GET  /api/v1/date-ideas            → lista (com filtro por categoria)
#   - POST /api/v1/date-ideas            → usuário submete a ideia dele
#   - POST /api/v1/date-ideas/<id>/like  → toggle de like
# Ideias iniciais (seed) vêm marcadas seed:true; UGC passa pelo
# validate_content_privacy (anti-doxxing) — nada de contactos/links.
# Arquitetura: mesmo padrão init(app, ...) do payments_manual (pitfall 40).
# ============================================================
import os as _os
import re as _re
import time as _time
import uuid as _uuid
import threading as _threading
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

SEED_IDEAS = [
    {"title": "Café com vista no elevador", "description": "Um café simples perto de um miradouro — conversa flui e se não correr bem, terminou em 40 minutos sem constrangimento.", "category": "cafe", "city": "Lisboa"},
    {"title": "Feira da Ladra ao sábado", "description": "Vulgar e vintage, com espaço para caminhar lado a lado. Perfeito para quebrar o gelo procurando achados juntos.", "category": "passeio", "city": "Lisboa"},
    {"title": "Fundação Gulbenkian", "description": "Arte, jardim e café no mesmo sítio. Seguro, público e sempre com tema novo para comentar.", "category": "cultura", "city": "Lisboa"},
    {"title": "Pôr do sol na Ericeira", "description": "Conduzir até à costa, ver o sol cair e jantar peixe. Um clássico que nunca falha.", "category": "natureza", "city": "Ericeira"},
    {"title": "Time Out Market", "description": "Cada um escolhe o prato que quiser — zero pressão de menu e muita conversa sobre comida.", "category": "comida", "city": "Lisboa"},
    {"title": "Fado num bistró pequeno", "description": "Casa pequena, poucas pessoas. A música faz a metade da conversa por ti.", "category": "noite", "city": "Lisboa"},
    {"title": "Livraria Lello + café", "description": "A livraria mais bonita do mundo e depois um café a falar do que cada um gosta de ler.", "category": "cultura", "city": "Porto"},
    {"title": "Caminhada no Parque da Cidade", "description": "Andar sem destino no parque, gelado ou café no fim. Leve e sem pressão.", "category": "natureza", "city": "Porto"},
    {"title": "Francesinha dividida", "description": "Pedir uma para os dois — é descontraído, engraçado e rende boas conversas.", "category": "comida", "city": "Porto"},
    {"title": "Ribeira ao anoitecer", "description": "Andar junto ao Douro quando as luzes acendem. Romântico sem ser intenso.", "category": "passeio", "city": "Porto"},
    {"title": "Escape room para dois", "description": "Trabalham juntos num objetivo — é o atalho mais rápido para quebrar o gelo e ver como a pessoa pensa.", "category": "noite", "city": ""},
    {"title": "Brunch de domingo", "description": "Sem pressa, sem relógio. Se correr bem estende-se para a tarde; se não, acabou às 13h.", "category": "cafe", "city": ""},
]


def _validate_idea(text: str):
    """Reutiliza o validate_content_privacy do preview_server (injetado)."""
    return _validate_idea_fn(text)  # noqa: F821 — injetado pelo init


_validate_idea_fn = None


def init_date_ideas(app, session, load_json_store, save_json_store, validate_content_privacy_fn, safe_photo_fn=None):
    """Registra as rotas de ideias de 1º encontro (mesmo padrão do payments_manual)."""
    global _validate_idea_fn
    _validate_idea_fn = validate_content_privacy_fn
    lock = DATE_IDEAS_LOCK

    def _load():
        data = load_json_store(DATE_IDEAS_FILE, None)
        if data is None:
            now = _time.time()
            data = []
            for i, s in enumerate(SEED_IDEAS):
                data.append({
                    "id": f"di_seed_{i+1}",
                    "title": s["title"],
                    "description": s["description"],
                    "category": s["category"],
                    "city": s.get("city", ""),
                    "author_id": "sigaleve",
                    "author_name": "Equipa Sigaleve",
                    "author_avatar": "",
                    "likes": {},
                    "seed": True,
                    "created_at": now - (len(SEED_IDEAS) - i) * 86400,
                })
            save_json_store(DATE_IDEAS_FILE, data)
        return data

    def _serialize(idea, current_uid):
        likes = idea.get("likes") or {}
        return {
            "id": idea["id"],
            "title": idea["title"],
            "description": idea["description"],
            "category": idea["category"],
            "category_label": CATEGORY_LABELS.get(idea["category"], {"pt": idea["category"], "emoji": "💡"})["pt"],
            "city": idea.get("city", ""),
            "author_id": idea.get("author_id", ""),
            "author_name": idea.get("author_name", "Utilizador"),
            "author_avatar": idea.get("author_avatar", ""),
            "mine": idea.get("author_id") == current_uid,
            "seed": bool(idea.get("seed")),
            "likes_count": len(likes),
            "my_like": bool(current_uid and likes.get(str(current_uid))),
            "created_at": idea.get("created_at", 0),
        }

    @app.route("/api/v1/date-ideas", methods=["GET"])
    def api_date_ideas_list():
        if not session.get("user_id"):
            return _jsonify({"error": "Autenticação necessária"}), 401
        current_uid = str(session.get("user_id"))
        cat = (_request.args.get("category") or "").strip().lower()
        with lock:
            ideas = _load()
            out = []
            for idea in ideas:
                if cat and cat != "todas" and idea.get("category") != cat:
                    continue
                out.append(_serialize(idea, current_uid))
        # mais curtidas primeiro, depois mais recentes
        out.sort(key=lambda x: (-x["likes_count"], -x["created_at"]))
        return _jsonify({"success": True, "categories": CATEGORY_LABELS, "ideas": out}), 200

    @app.route("/api/v1/date-ideas", methods=["POST"])
    def api_date_ideas_create():
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        current_uid = str(session.get("user_id"))
        data = _request.get_json(silent=True) or {}
        title = str(data.get("title", "")).strip()
        description = str(data.get("description", "")).strip()
        category = str(data.get("category", "cafe")).strip().lower()
        city = str(data.get("city", "")).strip()
        if not title or not description:
            return _jsonify({"success": False, "error": "Preenche o título e a descrição da ideia."}), 400
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

        author_name = session.get("user_name") or "Utilizador"
        author_avatar = session.get("user_photo") or ""
        if not author_avatar:
            # buscar do store de usuários (injetado como _load_users_fn pelo preview_server? não —
            # manter simples: avatar vazio → frontend usa fallback)
            author_avatar = ""
        new_idea = {
            "id": f"di_{_uuid.uuid4().hex[:8]}",
            "title": title,
            "description": description,
            "category": category,
            "city": city,
            "author_id": current_uid,
            "author_name": author_name,
            "author_avatar": author_avatar,
            "likes": {},
            "seed": False,
            "created_at": _time.time(),
        }
        with lock:
            ideas = _load()
            ideas.insert(0, new_idea)
            save_json_store(DATE_IDEAS_FILE, ideas)
        return _jsonify({"success": True, "message": "Ideia partilhada com a comunidade! 💜", "idea": _serialize(new_idea, current_uid)}), 201

    @app.route("/api/v1/date-ideas/<idea_id>/like", methods=["POST"])
    def api_date_ideas_like(idea_id):
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
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
            if idea.get("author_id") != current_uid or idea.get("seed"):
                return _jsonify({"success": False, "error": "Só podes apagar as tuas próprias ideias."}), 403
            ideas = [i for i in ideas if i["id"] != idea_id]
            save_json_store(DATE_IDEAS_FILE, ideas)
        return _jsonify({"success": True, "message": "Ideia removida."}), 200

    return {"routes": ["GET/POST date-ideas", "like", "delete"], "seed_count": len(SEED_IDEAS)}
