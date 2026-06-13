from flask import Blueprint, current_app, jsonify, request, session, abort
from delivery_app.exceptions import BusinessRuleError, EntityNotFoundError
from delivery_app.services.order_service import OrderService
from delivery_app.extensions import socketio # 🌟 Importamos el motor en tiempo real

courier_api_blueprint = Blueprint("courier_api_blueprint", __name__, url_prefix="/api/v1/couriers")

def _get_order_service() -> OrderService:
    repositories = current_app.extensions["repositories"]
    return OrderService(
        repositories["order"],
        repositories["restaurant"],
        repositories["client"],
        repositories["courier"],
    )

@courier_api_blueprint.route("/available-orders", methods=["GET"])
def get_available_delivery_offers():
    if not session.get("courier_id") or session.get("role") != "courier":
        abort(403)
    service = _get_order_service()
    all_orders = service.list()
    available_orders = [o for o in all_orders if o.status == "LISTO_PARA_RECOGER" and not o.courier_id]
    return jsonify([order.to_dict() for order in available_orders]), 200

@courier_api_blueprint.route("/orders/<int:order_id>/accept", methods=["POST"])
def accept_delivery_offer(order_id):
    """El estafeta acepta el envío. Avisamos instantáneamente al cliente de que su moto va en camino"""
    s_courier_id = session.get("courier_id")
    if not s_courier_id or session.get("role") != "courier":
        abort(403)
    payload = request.json or {}
    courier_id = s_courier_id
    service = _get_order_service()
    
    try:
        order = service.assign_courier(order_id, courier_id)
        
        # 🛰️ Alerta WebSocket: Avisa a la App del Cliente quién es su repartidor
        delivery_data = {
            "order_id": order.id,
            "client_id": order.client_id,
            "courier_id": order.courier_id,
            "status": "REPARTIDOR_EN_CAMINO"
        }
        socketio.emit("repartidor_asignado", delivery_data, broadcast=True)
        
        return jsonify({
            "message": f"¡Oferta aceptada! Órden #{order_id} asignada al estafeta {courier_id}",
            "order_id": order.id,
            "courier_id": order.courier_id
        }), 200
    except (BusinessRuleError, EntityNotFoundError) as error:
        return jsonify({"error": str(error)}), 400

@courier_api_blueprint.route("/gps", methods=["POST"])
def update_courier_gps():
    s_courier_id = session.get("courier_id")
    if not s_courier_id or session.get("role") != "courier":
        abort(403)
    payload = request.json or {}
    lat = payload.get("latitude")
    lng = payload.get("longitude")
    courier_id = s_courier_id
    order_id = payload.get("order_id") # ID de la orden que está entregando
    
    # 🛰️ Alerta WebSocket Crítica: Envía las coordenadas en vivo directamente a la pantalla del cliente
    gps_data = {
        "courier_id": courier_id,
        "order_id": order_id,
        "latitude": lat,
        "longitude": lng
    }
    socketio.emit("rastreo_gps_en_vivo", gps_data, broadcast=True)
    
    print(f"[GPS LIVE] Estafeta {courier_id} en ruta. Lat {lat}, Lng {lng}")
    return jsonify({"status": "Coordenadas transmitidas en tiempo real"}), 200


@courier_api_blueprint.route("/orders/<int:order_id>/status", methods=["PATCH"])
def update_delivery_status(order_id):
    """Permite al estafeta actualizar el estado del reparto en tiempo real"""
    s_courier_id = session.get("courier_id")
    if not s_courier_id or session.get("role") != "courier":
        abort(403)
        
    service = _get_order_service()
    try:
        order = service.get(order_id)
    except EntityNotFoundError:
        return jsonify({"error": "Order not found"}), 404
        
    if int(order.courier_id) != int(s_courier_id):
        abort(403)
        
    payload = request.json or {}
    action = payload.get("action", "").lower()
    
    try:
        if action == "start":
            order = service.start(order_id)
        elif action == "complete":
            order = service.complete(order_id)
        else:
            return jsonify({"error": "Acción inválida. Use 'start' o 'complete'."}), 400
            
        status_update = {
            "order_id": order.id,
            "status": order.status
        }
        socketio.emit("cambio_estado_pedido", status_update, broadcast=True)
        
        return jsonify({
            "message": f"Estado de reparto de la órden #{order_id} actualizado a {order.status}",
            "order_id": order.id,
            "status": order.status
        }), 200
        
    except (BusinessRuleError, EntityNotFoundError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

