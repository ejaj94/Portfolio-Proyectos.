from flask import Blueprint, current_app, jsonify, request, session, abort
from delivery_app.exceptions import BusinessRuleError, EntityNotFoundError
from delivery_app.services.order_service import OrderService
from delivery_app.extensions import socketio # 🌟 Importamos el motor en tiempo real
from werkzeug.utils import secure_filename
import os
from datetime import datetime

restaurant_api_blueprint = Blueprint("restaurant_api_blueprint", __name__, url_prefix="/api/v1/restaurants")

def _get_order_service() -> OrderService:
    repositories = current_app.extensions["repositories"]
    return OrderService(
        repositories["order"],
        repositories["restaurant"],
        repositories["client"],
        repositories["courier"],
    )

@restaurant_api_blueprint.route("/<int:restaurant_id>/orders", methods=["GET"])
def get_restaurant_orders(restaurant_id):
    if not session.get("restaurant_id") or session.get("role") != "restaurant" or int(session.get("restaurant_id")) != int(restaurant_id):
        abort(403)
    service = _get_order_service()
    all_orders = service.list()
    restaurant_orders = [o for o in all_orders if o.restaurant_id == restaurant_id]
    return jsonify([order.to_dict() for order in restaurant_orders]), 200

@restaurant_api_blueprint.route("/orders/<int:order_id>/status", methods=["PATCH"])
def update_order_status(order_id):
    """El restaurante actualiza la fase de cocina e informa al ecosistema en vivo"""
    service = _get_order_service()
    try:
        order = service.get(order_id)
    except EntityNotFoundError:
        return jsonify({"error": "Order not found"}), 404
        
    if not session.get("restaurant_id") or session.get("role") != "restaurant" or int(session.get("restaurant_id")) != int(order.restaurant_id):
        abort(403)
        
    payload = request.json or {}
    action = payload.get("action", "").lower()
    
    try:
        if action == "start":
            order = service.start(order_id)
            nuevo_estado = "EN_PREPARACION"
        elif action == "complete":
            order = service.complete(order_id)
            nuevo_estado = "LISTO_PARA_RECOGER"
        else:
            return jsonify({"error": "Acción inválida. Use 'start' o 'complete'."}), 400
            
        # 🛰️ Alerta WebSocket: Enviamos la actualización del estado de la orden
        status_update = {
            "order_id": order.id,
            "restaurant_id": order.restaurant_id,
            "status": nuevo_estado
        }
        
        # Si está listo, disparamos un evento especial para que los estafetas lo vean en sus pantallas
        if nuevo_estado == "LISTO_PARA_RECOGER":
            socketio.emit("oferta_disponible", status_update, broadcast=True)
        else:
            socketio.emit("cambio_estado_pedido", status_update, broadcast=True)
            
        return jsonify({
            "message": f"Órden #{order_id} actualizada correctamente",
            "order_id": order.id,
            "status": nuevo_estado
        }), 200
        
    except (BusinessRuleError, EntityNotFoundError) as error:
        return jsonify({"error": str(error)}), 400

# --- FASE 10: ENDPOINTS DE PLATES & CONFIG ---
from delivery_app.entities.plate import Plate

@restaurant_api_blueprint.route("/<int:restaurant_id>/plates", methods=["GET"])
def get_restaurant_plates(restaurant_id):
    role = session.get("role")
    if role == "restaurant":
        if int(session.get("restaurant_id")) != int(restaurant_id):
            abort(403)
    elif role == "client":
        pass  # clients are allowed to read any restaurant's plates
    else:
        abort(403)
        
    plate_repo = current_app.extensions["repositories"]["plate"]
    plates = plate_repo.list_by_restaurant(restaurant_id)
    return jsonify([p.__dict__ for p in plates]), 200

@restaurant_api_blueprint.route("/<int:restaurant_id>/plates", methods=["POST"])
def add_restaurant_plate(restaurant_id):
    if not session.get("restaurant_id") or session.get("role") != "restaurant" or int(session.get("restaurant_id")) != int(restaurant_id):
        abort(403)
    payload = request.json or {}
    name = payload.get("name", "").strip()
    if not name:
        return jsonify({"error": "O nome do prato é obrigatório."}), 400
    try:
        price = float(payload.get("price", 0))
    except ValueError:
        return jsonify({"error": "Preço inválido."}), 400
        
    plate = Plate(
        id=None,
        restaurant_id=restaurant_id,
        name=name,
        price=price,
        image_url=payload.get("image_url", "").strip(),
        description=payload.get("description", "").strip(),
        category=payload.get("category", "Pizzas").strip(),
        is_weekly=bool(payload.get("is_weekly", False))
    )
    plate_repo = current_app.extensions["repositories"]["plate"]
    saved_plate = plate_repo.add(plate)
    return jsonify(saved_plate.__dict__), 201

@restaurant_api_blueprint.route("/plates/<int:plate_id>", methods=["DELETE"])
def delete_restaurant_plate(plate_id):
    if not session.get("restaurant_id") or session.get("role") != "restaurant":
        abort(403)
    plate_repo = current_app.extensions["repositories"]["plate"]
    plate = plate_repo.get_by_id(plate_id)
    if not plate or int(plate.restaurant_id) != int(session.get("restaurant_id")):
        abort(403)
    plate_repo.delete(plate_id)
    return jsonify({"message": f"Prato #{plate_id} removido com sucesso."}), 200

@restaurant_api_blueprint.route("/<int:restaurant_id>/config", methods=["GET"])
def get_restaurant_config(restaurant_id):
    if not session.get("restaurant_id") or session.get("role") != "restaurant" or int(session.get("restaurant_id")) != int(restaurant_id):
        abort(403)
    restaurant_repo = current_app.extensions["repositories"]["restaurant"]
    try:
        restaurant = restaurant_repo.get_by_id(restaurant_id)
        return jsonify({
            "logo_url": restaurant.logo_url or "",
            "banner_url": restaurant.banner_url or "",
            "region": restaurant.region or "Porto",
            "name": restaurant.name
        }), 200
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@restaurant_api_blueprint.route("/<int:restaurant_id>/config", methods=["POST"])
def update_restaurant_config(restaurant_id):
    if not session.get("restaurant_id") or session.get("role") != "restaurant" or int(session.get("restaurant_id")) != int(restaurant_id):
        abort(403)
    restaurant_repo = current_app.extensions["repositories"]["restaurant"]
    try:
        restaurant = restaurant_repo.get_by_id(restaurant_id)
        payload = request.json or {}
        restaurant.logo_url = payload.get("logo_url", restaurant.logo_url)
        restaurant.banner_url = payload.get("banner_url", restaurant.banner_url)
        restaurant.region = payload.get("region", restaurant.region)
        restaurant_repo.update(restaurant)
        return jsonify({
            "message": "Configuração do restaurante actualizada com sucesso.",
            "logo_url": restaurant.logo_url,
            "banner_url": restaurant.banner_url,
            "region": restaurant.region
        }), 200
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@restaurant_api_blueprint.route("/<int:restaurant_id>/upload-plate-image", methods=["POST"])
def upload_plate_image(restaurant_id):
    if not session.get("restaurant_id") or session.get("role") != "restaurant" or int(session.get("restaurant_id")) != int(restaurant_id):
        abort(403)
        
    f = request.files.get("plate_image")
    if not f or not f.filename:
        return jsonify({"error": "Nenhum ficheiro enviado."}), 400
        
    ext = os.path.splitext(f.filename)[1].lower().lstrip('.')
    if ext not in ("png", "jpg", "jpeg", "webp"):
        return jsonify({"error": "Formato de imagem inválido."}), 400
        
    upload_dir = os.path.join(current_app.static_folder, "uploads", "plates")
    os.makedirs(upload_dir, exist_ok=True)
    
    filename = secure_filename(f"{datetime.utcnow().timestamp()}_{f.filename}")
    filepath = os.path.join(upload_dir, filename)
    f.save(filepath)
    
    relative_url = f"/static/uploads/plates/{filename}"
    return jsonify({"image_url": relative_url}), 200


