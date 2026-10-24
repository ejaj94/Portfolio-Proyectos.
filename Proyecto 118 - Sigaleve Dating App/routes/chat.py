"""
routes/chat.py — Blueprint para histórico de mensagens efêmeras (24h) e registo
de eventos de tempo real com Socket.IO (salas privadas, deduplicação e paywall).
"""
import uuid
import datetime
from flask import Blueprint, request, jsonify, session
from flask_socketio import emit, join_room, leave_room

from services.common import (
    load_json_store,
    save_json_store,
    load_users,
    MESSAGES_FILE,
)
from routes.push import send_push_to_user

chat_bp = Blueprint("chat_bp", __name__)


# ── REST ENDPOINTS DE CONVERSAS E HISTÓRICO ──────────────────────────────────

@chat_bp.route("/api/v1/conversations", methods=["GET"])
@chat_bp.route("/api/v1/chat/conversations", methods=["GET"])
def api_get_conversations():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Autenticação necessária"}), 401
    return jsonify({
        "success": True,
        "conversations": []
    }), 200


@chat_bp.route("/api/v1/chat/messages", methods=["GET"])
def api_get_chat_messages():
    """Histórico do chat: mensagens persistidas com autodestruição em 24h."""
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Autenticação necessária"}), 401
    other = request.args.get("peer_id", "")
    if not other:
        return jsonify({"error": "peer_id em falta"}), 400

    ids = sorted([str(uid), str(other)])
    conv_id = f"{ids[0]}__{ids[1]}"

    messages = load_json_store(MESSAGES_FILE, {})
    conv = messages.get(conv_id, [])

    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
    kept = []
    for m in conv:
        try:
            mdt = datetime.datetime.fromisoformat(m["ts"].replace("Z", "+00:00"))
            if mdt.astimezone(datetime.timezone.utc) >= cutoff:
                kept.append(m)
        except Exception:
            kept.append(m)

    return jsonify({
        "success": True,
        "messages": kept
    }), 200


# ── REGISTO DE EVENTOS SOCKET.IO ─────────────────────────────────────────────

def register_socket_events(socketio):
    """Regista os manipuladores de eventos Socket.IO para o chat em tempo real."""

    @socketio.on("connect")
    def on_connect(auth=None):
        uid = session.get("user_id")
        if uid:
            join_room(f"user__{uid}")
            uemail = session.get("user_email")
            if uemail:
                join_room(f"user__{uemail}")
        emit("connected", {"status": "ok"})

    @socketio.on("register_user")
    def on_register_user(data):
        uid = (data or {}).get("user_id") or session.get("user_id")
        uemail = (data or {}).get("user_email") or session.get("user_email")
        if uid:
            join_room(f"user__{uid}")
        if uemail:
            join_room(f"user__{uemail}")
        emit("registered", {"ok": True})

    @socketio.on("join_room")
    def on_join(data):
        my_id = data.get("sender_id") or session.get("user_id") or "11111111-1111-1111-1111-111111111111"
        other = data.get("other_user_id", "22222222-2222-2222-2222-222222222222")
        ids = sorted([str(my_id), str(other)])
        room = f"room__{ids[0]}__{ids[1]}"
        join_room(room)
        emit("room_joined", {
            "room_id": room,
            "ephemeral_note": "Mensagens efêmeras protegidas com destruição em 24h."
        })

    @socketio.on("send_message")
    def on_message(data):
        content = str(data.get("content", "")).strip()
        if not content:
            return
        my_id = data.get("sender_id") or session.get("user_id") or "11111111-1111-1111-1111-111111111111"
        sender_email = session.get("user_email")
        if sender_email:
            users = load_users()
            u = users.get(sender_email)
            sub = (u or {}).get("subscription") or {}
            now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            has_active_sub = bool((u or {}).get("is_plus")) or (
                sub.get("active") is True
                and str(sub.get("expires_at", "")) > now_iso
            )
            if not has_active_sub:
                emit("subscription_required", {
                    "error": "subscricao_necessaria",
                    "message": "As mensagens ilimitadas são exclusivas de membros com subscrição ativa."
                })
                return
        other = data.get("other_user_id", "22222222-2222-2222-2222-222222222222")
        msg_id = data.get("msg_id", "")
        ids = sorted([str(my_id), str(other)])
        room = f"room__{ids[0]}__{ids[1]}"
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"

        try:
            messages = load_json_store(MESSAGES_FILE, {})
            conv_id = f"{ids[0]}__{ids[1]}"
            conv = messages.setdefault(conv_id, [])
            if not (msg_id and any(str(m.get("msg_id")) == str(msg_id) for m in conv)):
                conv.append({
                    "id": msg_id or f"m_{uuid.uuid4().hex[:10]}",
                    "sender_id": str(my_id),
                    "content": content,
                    "ts": ts
                })
                cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)
                kept = []
                for m in conv:
                    try:
                        mdt = datetime.datetime.fromisoformat(m["ts"].replace("Z", "+00:00"))
                    except Exception:
                        kept.append(m)
                        continue
                    if mdt.astimezone(datetime.timezone.utc) >= cutoff:
                        kept.append(m)
                messages[conv_id] = kept
                save_json_store(MESSAGES_FILE, messages)
        except Exception:
            pass

        socketio.emit("new_message", {
            "sender_id": str(my_id),
            "content": content,
            "ts": ts,
            "msg_id": msg_id
        }, to=room)

        try:
            peer_name = "Alguém"
            try:
                users = load_users()
                by_id = {str(u.get("id") or em): u for em, u in users.items()}
                sender = by_id.get(str(my_id))
                if sender:
                    peer_name = sender.get("display_name") or sender.get("name") or "Alguém"
            except Exception:
                pass
            socketio.emit("chat_message", {
                "sender_id": str(my_id),
                "from": str(my_id),
                "peer_name": peer_name,
                "content": content,
                "ts": ts,
                "msg_id": msg_id
            }, to=f"user__{other}")
        except Exception:
            pass

        try:
            target_uid = str(other)
            users = load_users()
            by_id = {str(u.get("id") or em): u for em, u in users.items()}
            sender = by_id.get(str(my_id))
            if sender:
                sender_name = (sender.get("display_name") or "Alguém")
                send_push_to_user(
                    target_uid,
                    f"💬 {sender_name}",
                    content[:120],
                    "/app"
                )
        except Exception:
            pass

    @socketio.on("leave_room")
    def on_leave(data):
        my_id = session.get("user_id") or "11111111-1111-1111-1111-111111111111"
        other = data.get("other_user_id", "22222222-2222-2222-2222-222222222222")
        ids = sorted([str(my_id), str(other)])
        room = f"room__{ids[0]}__{ids[1]}"
        leave_room(room)
