"""
routes/push.py — Blueprint para Notificações WebPush (VAPID).
"""
import os
import json
import datetime
from flask import Blueprint, jsonify, request, session
from services.common import load_json_store, save_json_store, PUSH_SUBS_FILE

push_bp = Blueprint("push", __name__)

VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PUBLIC_KEY = os.environ.get("VAPID_PUBLIC_KEY", "")
VAPID_SUBJECT = os.environ.get("VAPID_SUBJECT", "mailto:contato@sigaleve.com")
PUSH_ENABLED = bool(VAPID_PRIVATE_KEY and VAPID_PUBLIC_KEY)


def send_push_to_user(user_id, title, body, url_path="/app"):
    """Enviar push notification a todas as subscrições de um utilizador."""
    try:
        if not PUSH_ENABLED:
            return
        subs = load_json_store(PUSH_SUBS_FILE, {})
        user_subs = subs.get(str(user_id), [])
        if not user_subs:
            return
        from pywebpush import webpush, WebPushException
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = json.dumps({
            "title": title,
            "body": body,
            "url": url_path,
            "ts": now.isoformat(),
        })
        alive = []
        for sub in user_subs:
            try:
                webpush(
                    subscription_info=sub,
                    data=payload,
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims={"sub": VAPID_SUBJECT},
                )
                alive.append(sub)
            except WebPushException as e:
                if e.response is not None and e.response.status_code in (404, 410):
                    continue
                alive.append(sub)
            except Exception:
                alive.append(sub)
        if len(alive) != len(user_subs):
            subs[str(user_id)] = alive
            save_json_store(PUSH_SUBS_FILE, subs)
    except Exception:
        pass


@push_bp.route("/api/v1/push/public-key", methods=["GET"])
def api_push_public_key():
    return jsonify({"public_key": VAPID_PUBLIC_KEY}), 200


@push_bp.route("/api/v1/push/subscribe", methods=["POST"])
def api_push_subscribe():
    if not session.get("user_id"):
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    data = request.get_json(silent=True) or {}
    sub = data.get("subscription")
    if not sub or not isinstance(sub, dict) or not sub.get("endpoint"):
        return jsonify({"success": False, "error": "Subscrição inválida"}), 400
    subs = load_json_store(PUSH_SUBS_FILE, {})
    uid = str(session.get("user_id"))
    if uid not in subs or not isinstance(subs[uid], list):
        subs[uid] = []
    endpoint = sub.get("endpoint")
    if not any(s.get("endpoint") == endpoint for s in subs[uid]):
        subs[uid].append(sub)
    save_json_store(PUSH_SUBS_FILE, subs)
    return jsonify({"success": True}), 200


@push_bp.route("/api/v1/push/unsubscribe", methods=["POST"])
def api_push_unsubscribe():
    if not session.get("user_id"):
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401
    data = request.get_json(silent=True) or {}
    endpoint = str(data.get("endpoint", ""))
    subs = load_json_store(PUSH_SUBS_FILE, {})
    uid = str(session.get("user_id"))
    if uid in subs and isinstance(subs[uid], list):
        before = len(subs[uid])
        subs[uid] = [s for s in subs[uid] if s.get("endpoint") != endpoint]
        save_json_store(PUSH_SUBS_FILE, subs)
        return jsonify({"success": True, "removed": before - len(subs[uid])}), 200
    return jsonify({"success": True, "removed": 0}), 200
