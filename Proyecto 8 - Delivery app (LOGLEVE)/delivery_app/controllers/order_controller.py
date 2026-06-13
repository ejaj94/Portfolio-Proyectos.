from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for

from delivery_app.entities.order import Order
from delivery_app.exceptions import BusinessRuleError, EntityNotFoundError, ValidationError
from delivery_app.services.order_service import OrderService

# Nombre del Blueprint sincronizado con la barra de navegación global (base.html)
order_blueprint = Blueprint("order_blueprint", __name__, url_prefix="/orders")


def _get_service() -> OrderService:
    repositories = current_app.extensions["repositories"]
    return OrderService(
        repositories["order"],
        repositories["restaurant"],
        repositories["client"],
        repositories["courier"],
    )


# --- VISTAS PARA LA INTERFAZ WEB (.html) ---

@order_blueprint.route("/", methods=["GET"])
def list_orders():
    service = _get_service()
    orders = service.list()
    
    # Si la petición solicita JSON (API), responde con datos planos
    if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
        return jsonify([order.__dict__ for order in orders]), 200
        
    # Ruta corregida apuntando directamente a la raíz de templates
    return render_template("list_orders.html", orders=orders)


@order_blueprint.route("/register", methods=["GET"])
def register_order_form():
    # Ruta corregida apuntando directamente a la raíz de templates
    return render_template("register_order.html", error=None)


@order_blueprint.route("/register", methods=["POST"])
def register_order_web():
    # Extracción y conversión segura de tipos numéricos primitivos para la web
    try:
        restaurant_id = int(request.form.get("restaurant_id", 0))
        client_id = int(request.form.get("client_id", 0))
    except (ValueError, TypeError):
        return render_template("register_order.html", error="Los IDs de restaurante y cliente deben ser valores numéricos.")

    order = Order(
        id=None,
        restaurant_id=restaurant_id,
        client_id=client_id,
        courier_id=None,
        note=request.form.get("note", ""),
    )
    try:
        _get_service().create(order)
        return redirect(url_for("order_blueprint.list_orders"))
    except (ValidationError, BusinessRuleError, EntityNotFoundError) as error:
        # Ruta corregida para recargar el formulario si ocurre un error
        return render_template("register_order.html", error=str(error))


# --- ENDPOINTS PARA LA API (JSON) ---

@order_blueprint.route("/", methods=["POST"])
def create_order():
    payload = request.json or {}
    order = Order(
        id=None,
        restaurant_id=payload.get("restaurant_id"),
        client_id=payload.get("client_id"),
        courier_id=None,
        note=payload.get("note"),
    )
    try:
        result = _get_service().create(order)
        return jsonify(result.__dict__), 201
    except (ValidationError, BusinessRuleError, EntityNotFoundError) as error:
        return jsonify({"error": str(error)}), 400


@order_blueprint.route("/<int:order_id>/assign", methods=["POST"])
def assign_order(order_id: int):
    payload = request.json or {}
    courier_id = payload.get("courier_id")
    try:
        order = _get_service().assign_courier(order_id, courier_id)
        return jsonify(order.__dict__), 200
    except (BusinessRuleError, EntityNotFoundError) as error:
        return jsonify({"error": str(error)}), 400


@order_blueprint.route("/<int:order_id>/start", methods=["POST"])
def start_order(order_id: int):
    try:
        order = _get_service().start(order_id)
        return jsonify(order.__dict__), 200
    except (BusinessRuleError, EntityNotFoundError, ValidationError) as error:
        return jsonify({"error": str(error)}), 400


@order_blueprint.route("/<int:order_id>/complete", methods=["POST"])
def complete_order(order_id: int):
    try:
        order = _get_service().complete(order_id)
        return jsonify(order.__dict__), 200
    except (BusinessRuleError, EntityNotFoundError, ValidationError) as error:
        return jsonify({"error": str(error)}), 400
    
@order_blueprint.route("/<int:order_id>/pay", methods=["POST"])
def pay_order(order_id: int):
    """Endpoint para registrar el pago del cliente y pasarlo a preparación."""
    try:
        # Invocamos el método del servicio encargado de procesar la orden
        order = _get_service().process_payment(order_id)
        return jsonify(order.__dict__), 200
    except (BusinessRuleError, EntityNotFoundError, ValidationError) as error:
        return jsonify({"error": str(error)}), 400
