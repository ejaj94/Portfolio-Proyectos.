"""
routes/qa_health.py — Blueprint para Q&A Anónimo de Saúde e Medicina da Comunidade.
"""
import uuid
import hashlib
import re
from flask import Blueprint, jsonify, request, session
from services.common import load_json_store, save_json_store, QA_HEALTH_FILE

qa_bp = Blueprint("qa_health", __name__)

DEFAULT_QA_HEALTH = []


def qa_anonymize(uid):
    """Gera um pseudónimo estável por tópico."""
    topic = "qa-health"
    h = hashlib.sha256((str(uid) + topic).encode()).hexdigest()
    return "Membro #" + str(int(h[:8], 16) % 9000 + 1000)


def qa_filter_content(text):
    """Moderação de segurança em perguntas e respostas."""
    t = (text or "").lower()
    if re.search(r'(whatsapp|wa\.me|telegram|t\.me|@[a-z0-9._-]+\.(com|net|org|pt|es))', t):
        return False, "Não podes partilhar contactos externos (WhatsApp, Telegram, e-mails) por segurança."
    if re.search(r'https?://', t):
        return False, "Não podes partilhar links por segurança."
    if len(t.strip()) < 10:
        return False, "Escreve um pouco mais — a pergunta/resposta precisa de contexto (mín. 10 caracteres)."
    if len(t.strip()) > 2000:
        return False, "Texto demasiado longo (máx. 2000 caracteres)."
    return True, ""


@qa_bp.route("/api/v1/qa-health", methods=["GET"])
def api_qa_health_list():
    qa = load_json_store(QA_HEALTH_FILE, DEFAULT_QA_HEALTH)
    category = request.args.get("category", "")
    items = qa
    if category:
        items = [q for q in qa if q.get("category") == category]
    items = sorted(items, key=lambda q: q.get("created_at", 0), reverse=True)
    safe = []
    for q in items:
        q_copy = {k: v for k, v in q.items() if k not in ("user_id",)}
        q_copy["answers"] = [
            {k: v for k, v in a.items() if k not in ("user_id",)}
            for a in q.get("answers", [])
        ]
        safe.append(q_copy)
    return jsonify({"success": True, "questions": safe})


@qa_bp.route("/api/v1/qa-health", methods=["POST"])
def api_qa_health_create():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"success": False, "message": "Sessão necessária."}), 401
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    detail = str(data.get("detail", "")).strip()
    category = str(data.get("category", "diagnostico")).strip()
    if category not in ("diagnostico", "tratamento"):
        category = "diagnostico"
    ok, why = qa_filter_content(question)
    if not ok:
        return jsonify({"success": False, "message": why}), 400
    if detail:
        ok2, why2 = qa_filter_content(detail)
        if not ok2:
            return jsonify({"success": False, "message": why2}), 400
    qa = load_json_store(QA_HEALTH_FILE, DEFAULT_QA_HEALTH)
    qid = "qa-" + uuid.uuid4().hex[:12]
    import time
    qa.insert(0, {
        "id": qid,
        "category": category,
        "question": question[:200],
        "question_detail": detail[:2000],
        "author": qa_anonymize(uid),
        "user_id": str(uid),
        "created_at": time.time(),
        "views": 0,
        "answers": []
    })
    save_json_store(QA_HEALTH_FILE, qa)
    return jsonify({"success": True, "id": qid})


@qa_bp.route("/api/v1/qa-health/<qid>/answers", methods=["POST"])
def api_qa_health_answer(qid):
    uid = session.get("user_id")
    if not uid:
        return jsonify({"success": False, "message": "Sessão necessária."}), 401
    data = request.get_json(silent=True) or {}
    answer = str(data.get("answer", "")).strip()
    ok, why = qa_filter_content(answer)
    if not ok:
        return jsonify({"success": False, "message": why}), 400
    qa = load_json_store(QA_HEALTH_FILE, DEFAULT_QA_HEALTH)
    found = None
    for q in qa:
        if q.get("id") == qid:
            found = q
            break
    if not found:
        return jsonify({"success": False, "message": "Pergunta não encontrada."}), 404
    import time
    aid = "ans-" + uuid.uuid4().hex[:12]
    found.setdefault("answers", []).append({
        "id": aid,
        "author": qa_anonymize(uid),
        "user_id": str(uid),
        "answer": answer[:2000],
        "created_at": time.time(),
        "likes": 0
    })
    save_json_store(QA_HEALTH_FILE, qa)
    return jsonify({"success": True, "answer_id": aid})


@qa_bp.route("/api/v1/qa-health/<qid>/view", methods=["POST"])
def api_qa_health_view(qid):
    qa = load_json_store(QA_HEALTH_FILE, DEFAULT_QA_HEALTH)
    for q in qa:
        if q.get("id") == qid:
            q["views"] = int(q.get("views", 0)) + 1
            save_json_store(QA_HEALTH_FILE, qa)
            return jsonify({"success": True, "views": q["views"]})
    return jsonify({"success": False}), 404


@qa_bp.route("/api/v1/qa-health/<qid>/like", methods=["POST"])
def api_qa_health_like(qid):
    data = request.get_json(silent=True) or {}
    aid = data.get("answer_id")
    qa = load_json_store(QA_HEALTH_FILE, DEFAULT_QA_HEALTH)
    for q in qa:
        if q.get("id") == qid:
            for a in q.get("answers", []):
                if a.get("id") == aid:
                    a["likes"] = int(a.get("likes", 0)) + 1
                    save_json_store(QA_HEALTH_FILE, qa)
                    return jsonify({"success": True, "likes": a["likes"]})
            return jsonify({"success": False, "message": "Resposta não encontrada."}), 404
    return jsonify({"success": False, "message": "Pergunta não encontrada."}), 404
