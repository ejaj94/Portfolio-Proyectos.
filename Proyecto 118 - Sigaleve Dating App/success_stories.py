# ============================================================
# SIGALEVE — HISTÓRIAS DE SUCESSO (landing, curadoria do dono)
# ============================================================
# Feature #2 da análise de concorrentes (PS exibe 60k+ histórias na
# landing; prova social que converte visitante em registro).
# Fluxo honesto (pitfall 5 — claims e código juntos):
#   - Usuários submetem a história deles NO APP (pode ser anónima)
#   - O dono aprova/rejeita no painel /admin/stories?token=...
#   - A landing mostra SÓ as aprovadas (server-side injetado — SEO lê)
# Seeds iniciais: marcadas seed:true — a landing identifica-as como
# "histórias ilustrativas da comunidade" enquanto não houver reais.
# Arquitetura: mesmo padrão init() (pitfall 40).
# ============================================================
import os as _os
import time as _time
import uuid as _uuid
import threading as _threading
import html as _html
from flask import request as _request, jsonify as _jsonify, render_template as _render_template

DATA_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data")
STORIES_FILE = _os.path.join(DATA_DIR, "success_stories_store.json")
STORIES_LOCK = _threading.Lock()

# Seeds ilustrativas — PT-PT, contexto PT, tom realista SEM números falsos.
SEED_STORIES = [
    {
        "names": "M. & R.",
        "city": "Lisboa, Portugal",
        "text": "Ambos receámos o mesmo: a conversa difícil no primeiro encontro. Aqui ela nunca precisou de acontecer — começámos já do mesmo ponto. Um café virou jantar, o jantar virou dois anos juntos.",
        "seed": True,
    },
    {
        "names": "Sofia",
        "city": "Porto, Portugal",
        "text": "Tinha parado de tentar conhecer alguém porque cansava explicar a minha condição. Aqui não tive de explicar nada — e encontrei quem me respeita todos os dias.",
        "seed": True,
    },
    {
        "names": "A. & J.",
        "city": "Braga, Portugal",
        "text": "Começámos a falar pelos Momentos dele. Ele publicava o que sentia e eu reconheci-me em cada linha. A primeira mensagem foi a mais fácil da minha vida.",
        "seed": True,
    },
]


def init_stories(app, session, load_json_store, save_json_store, load_users, save_users):
    """Rotas: submit (app), moderação (admin), leitura (landing injeta)."""
    lock = STORIES_LOCK

    def _load():
        data = load_json_store(STORIES_FILE, None)
        if data is None:
            now = _time.time()
            data = []
            for i, s in enumerate(SEED_STORIES):
                data.append({
                    "id": f"st_seed_{i+1}",
                    "names": s["names"],
                    "city": s["city"],
                    "text": s["text"],
                    "author_email": "",
                    "anonymous": True,
                    "status": "approved",
                    "seed": True,
                    "created_ts": now - (len(SEED_STORIES) - i) * 86400 * 7,
                    "reviewed_ts": now,
                })
            save_json_store(STORIES_FILE, data)
        return data

    # ── SUBMISSÃO (app, sessão-gated, pode ser anónima) ──────────────
    @app.route("/api/v1/stories/submit", methods=["POST"])
    def api_stories_submit():
        if not session.get("user_id"):
            return _jsonify({"success": False, "error": "Autenticação necessária"}), 401
        data = _request.get_json(silent=True) or {}
        text = str(data.get("text", "")).strip()
        names = str(data.get("names", "")).strip()
        city = str(data.get("city", "")).strip()
        anonymous = bool(data.get("anonymous", False))
        if len(text) < 80:
            return _jsonify({"success": False, "error": "Conta um pouco mais — mínimo de 80 caracteres."}), 400
        if len(text) > 1200:
            return _jsonify({"success": False, "error": "Máximo de 1200 caracteres."}), 400
        if not anonymous and not names:
            return _jsonify({"success": False, "error": "Diz como queres aparecer (nomes/primeiros nomes)."}), 400
        with lock:
            stories = _load()
            # 1 história pendente por usuário (evita spam de moderação)
            pending = [s for s in stories if s.get("author_email") == session.get("user_email") and s.get("status") == "pending"]
            if pending:
                return _jsonify({"success": False, "error": "Já tens uma história à espera de revisão. 💜"}), 429
            stories.append({
                "id": f"st_{_uuid.uuid4().hex[:8]}",
                "names": ("Anónimo" if anonymous else names)[:60],
                "city": city[:60],
                "text": text,
                "author_email": session.get("user_email"),
                "anonymous": anonymous,
                "status": "pending",
                "seed": False,
                "created_ts": _time.time(),
            })
            save_json_store(STORIES_FILE, stories)
        return _jsonify({"success": True, "message": "História enviada! Se for aprovada, aparece na página inicial. 💜"}), 201

    # ── PAINEL DE MODERAÇÃO (dono) ────────────────────────────────────
    @app.route("/admin/stories", methods=["GET"])
    def admin_stories_page():
        token = _request.args.get("token", "").strip()
        if not token or token != _os.environ.get("SIGALEVE_ADMIN_TOKEN", ""):
            return "<h2 style='font-family:sans-serif;color:#b91c1c'>403 — Token inválido. Usa /admin/stories?token=SEU_TOKEN</h2>", 403
        with lock:
            stories = _load()
        pend = [s for s in stories if s.get("status") == "pending"]
        appr = sorted([s for s in stories if s.get("status") == "approved"], key=lambda s: -s.get("reviewed_ts", 0))

        def card(s, actions_html):
            seed_tag = " <span style='background:#7c3aed;color:#fff;font-size:10px;padding:2px 6px;border-radius:6px'>SEED ILUSTRATIVA</span>" if s.get("seed") else ""
            return (
                "<div style='background:#fff;border-radius:12px;padding:16px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.1)'>"
                f"<b style='font-size:15px'>{_html.escape(s['names'])}</b> <span style='color:#6b7280;font-size:13px'>· {_html.escape(s.get('city') or '')}</span>{seed_tag}"
                f"<p style='margin:10px 0;color:#374151;font-size:14px;line-height:1.6'>{_html.escape(s['text'])}</p>"
                f"<div style='font-size:12px;color:#9ca3af'>{_html.escape(str(s.get('author_email') or 'anónimo'))} · {actions_html}</div>"
                "</div>"
            )

        pend_html = "".join(card(s, (
            f"<button onclick=\"act('{s['id']}','approve')\" style=\"background:#10b981;color:#fff;border:none;padding:6px 14px;border-radius:8px;font-weight:700;cursor:pointer;margin-right:6px\">✓ Aprovar</button>"
            f"<button onclick=\"act('{s['id']}','reject')\" style=\"background:#6b7280;color:#fff;border:none;padding:6px 14px;border-radius:8px;font-weight:700;cursor:pointer\">✗ Rejeitar</button>"
        )) for s in pend) or "<p style='color:#6b7280'>Sem histórias à espera de revisão.</p>"
        appr_html = "".join(card(s, "<span style='color:#10b981;font-weight:700'>✓ Publicada</span>") for s in appr) or "<p style='color:#6b7280'>Nenhuma ainda.</p>"

        return (
            "<!doctype html><html lang=\"pt\"><head><meta charset=\"utf-8\"><title>Sigaleve — Histórias de Sucesso</title></head>"
            "<body style=\"font-family:-apple-system,sans-serif;margin:24px;background:#fafafa\">"
            "<h1 style=\"font-size:22px\">💜 Histórias de Sucesso — moderação</h1>"
            "<p style=\"color:#6b7280;font-size:13px\">Só o que aprovares aqui aparece na landing (secção «Histórias Reais»).</p>"
            "<h2 style=\"font-size:16px;margin-top:24px\">⏳ À espera de revisão</h2>" + pend_html +
            "<h2 style=\"font-size:16px;margin-top:24px\">✅ Publicadas</h2>" + appr_html +
            f"<script>async function act(id, action) {{ const r = await fetch('/admin/stories/act', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify({{ token: '{token}', id: id, action: action }}) }}); if (r.ok) location.reload(); else alert(await r.text()); }}</script>"
            "</body></html>"
        )

    @app.route("/admin/stories/act", methods=["POST"])
    def admin_stories_act():
        data = _request.get_json(silent=True) or {}
        token = str(data.get("token", "")).strip()
        if not token or token != _os.environ.get("SIGALEVE_ADMIN_TOKEN", ""):
            return _jsonify({"success": False, "error": "Token inválido"}), 403
        sid = str(data.get("id", "")).strip()
        action = str(data.get("action", "")).strip()
        with lock:
            stories = _load()
            s = next((x for x in stories if x["id"] == sid), None)
            if not s:
                return _jsonify({"success": False, "error": "História não encontrada"}), 404
            if action == "approve":
                s["status"] = "approved"
                s["reviewed_ts"] = _time.time()
            elif action == "reject":
                s["status"] = "rejected"
            else:
                return _jsonify({"success": False, "error": "Ação desconhecida"}), 400
            save_json_store(STORIES_FILE, stories)
        return _jsonify({"success": True}), 200

    return {"routes": ["submit", "admin/stories", "admin/stories/act"], "seed_count": len(SEED_STORIES)}


def ensure_stories_seeded(load_json_store, save_json_store):
    """Garante que o store existe com as seeds (chamado pela landing no boot).
    O _load() do init só roda dentro das rotas — a landing injeta ANTES de
    qualquer rota ser chamada, por isso a inicialização vive aqui."""
    data = load_json_store(STORIES_FILE, None)
    if data is None:
        now = _time.time()
        data = []
        for i, s in enumerate(SEED_STORIES):
            data.append({
                "id": f"st_seed_{i+1}",
                "names": s["names"],
                "city": s["city"],
                "text": s["text"],
                "author_email": "",
                "anonymous": True,
                "status": "approved",
                "seed": True,
                "created_ts": now - (len(SEED_STORIES) - i) * 86400 * 7,
                "reviewed_ts": now,
            })
        save_json_store(STORIES_FILE, data)
    return data


def get_approved_stories(load_json_store, save_json_store=None):
    """Helper para a landing injetar server-side (chamado pelo preview_server)."""
    with STORIES_LOCK:
        if save_json_store is not None:
            data = ensure_stories_seeded(load_json_store, save_json_store)
        else:
            data = load_json_store(STORIES_FILE, [])
    approved = [s for s in data if s.get("status") == "approved"]
    # seeds vão para o fim (reais primeiro), mais recentes primeiro
    approved.sort(key=lambda s: (bool(s.get("seed")), -s.get("reviewed_ts", s.get("created_ts", 0))))
    return approved[:6]
