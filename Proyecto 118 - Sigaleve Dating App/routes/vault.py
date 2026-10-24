"""
routes/vault.py — Blueprint para Álbum Oculto / Cofre Privado.
"""
from flask import Blueprint, jsonify, request, session
from services.common import load_json_store, save_json_store, PRIVATE_ALBUMS_FILE

vault_bp = Blueprint("vault", __name__)

DEFAULT_PRIVATE_ALBUMS = {}


@vault_bp.route("/api/v1/profile/private-album/<user_id>", methods=["GET"])
def api_get_private_album(user_id):
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"error": "Autenticação necessária"}), 401
    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    album = albums.get(user_id, {
        "photos": [],
        "authorized_users": [],
        "pending_requests": []
    })

    is_owner = (user_id == current_uid or user_id in ("me", "my_profile"))
    has_access = is_owner or (current_uid in album.get("authorized_users", []))
    has_requested = current_uid in album.get("pending_requests", [])

    if has_access:
        return jsonify({
            "success": True,
            "locked": False,
            "access_granted": True,
            "is_owner": is_owner,
            "photos": album.get("photos", []),
            "total_photos": len(album.get("photos", [])),
            "count": len(album.get("photos", [])),
            "requests": album.get("pending_requests", []) if is_owner else [],
            "pending_requests": album.get("pending_requests", []) if is_owner else []
        })
    else:
        return jsonify({
            "success": True,
            "locked": True,
            "access_granted": False,
            "is_owner": False,
            "status": "pending" if has_requested else "unauthorized",
            "count": len(album.get("photos", [])),
            "total_photos": len(album.get("photos", [])),
            "has_requested": has_requested,
            "message": "Este utilizador tem um álbum privado. Pede autorização para ver as fotos."
        })


@vault_bp.route("/api/v1/profile/private-album/request", methods=["POST"])
def api_request_private_album():
    data = request.get_json(silent=True) or {}
    target_user_id = data.get("target_user_id") or data.get("target_id")
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401

    if not target_user_id:
        return jsonify({"success": False, "error": "ID de utilizador inválido."}), 400

    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    if target_user_id not in albums:
        albums[target_user_id] = {"photos": [], "authorized_users": [], "pending_requests": []}

    req_list = albums[target_user_id].setdefault("pending_requests", [])
    if current_uid not in req_list:
        req_list.append(current_uid)
        save_json_store(PRIVATE_ALBUMS_FILE, albums)

    return jsonify({
        "success": True,
        "message": "Pedido de acesso enviado com sucesso! O proprietário receberá uma notificação para autorizar."
    }), 200


@vault_bp.route("/api/v1/profile/private-album/respond", methods=["POST"])
def api_respond_private_album():
    data = request.get_json(silent=True) or {}
    requester_id = data.get("requester_id")
    action = data.get("action")
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Autenticação necessária"}), 401

    if not requester_id:
        return jsonify({"success": False, "error": "Parâmetros inválidos."}), 400

    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    my_album = albums.setdefault(current_uid, {"photos": [], "authorized_users": [], "pending_requests": []})

    if requester_id in my_album.get("pending_requests", []):
        my_album["pending_requests"].remove(requester_id)

    if action in ("grant", "accept"):
        if requester_id not in my_album.get("authorized_users", []):
            my_album["authorized_users"].append(requester_id)
        msg = "Acesso ao teu álbum privado concedido com sucesso!"
    else:
        if requester_id in my_album.get("authorized_users", []):
            my_album["authorized_users"].remove(requester_id)
        msg = "Pedido recusado."

    save_json_store(PRIVATE_ALBUMS_FILE, albums)
    return jsonify({"success": True, "message": msg, "authorized_users": my_album["authorized_users"]})


@vault_bp.route("/api/v1/profile/private-album/manage", methods=["POST"])
def api_manage_private_album():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    photo_url = data.get("photo_url")
    photos_list = data.get("photos")
    current_uid = session.get("user_id")
    if not current_uid:
        return jsonify({"success": False, "error": "Sessão não iniciada."}), 401

    albums = load_json_store(PRIVATE_ALBUMS_FILE, DEFAULT_PRIVATE_ALBUMS)
    my_album = albums.setdefault(current_uid, {"photos": [], "authorized_users": [], "pending_requests": []})

    if photos_list is not None and isinstance(photos_list, list):
        my_album["photos"] = photos_list
        save_json_store(PRIVATE_ALBUMS_FILE, albums)
        return jsonify({"success": True, "message": "Álbum privado atualizado.", "photos": my_album["photos"]})

    if not photo_url:
        return jsonify({"success": False, "error": "URL da foto inválido."}), 400

    if action == "add":
        if photo_url not in my_album["photos"]:
            my_album["photos"].append(photo_url)
        msg = "Foto adicionada ao teu cofre privado com sucesso!"
    elif action == "remove":
        if photo_url in my_album["photos"]:
            my_album["photos"].remove(photo_url)
        msg = "Foto removida do cofre privado."
    else:
        return jsonify({"success": False, "error": "Ação inválida."}), 400

    save_json_store(PRIVATE_ALBUMS_FILE, albums)
    return jsonify({"success": True, "message": msg, "photos": my_album["photos"]})
