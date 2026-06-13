from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for

from delivery_app.entities.courier import Courier
from delivery_app.services.courier_service import CourierService

# Nombre del Blueprint sincronizado exactamente con tu barra de navegación (base.html)
courier_blueprint = Blueprint("courier_blueprint", __name__, url_prefix="/couriers")


def _get_service() -> CourierService:
    repositories = current_app.extensions["repositories"]
    return CourierService(repositories["courier"])


@courier_blueprint.route("/", methods=["GET"])
def list_couriers():
    service = _get_service()
    couriers = service.list()
    if request.headers.get("Accept") == "application/json":
        return jsonify([courier.__dict__ for courier in couriers]), 200
        
    # Ruta corregida apuntando al archivo HTML real en la raíz de templates
    return render_template("list_couriers.html", couriers=couriers)


@courier_blueprint.route("/register", methods=["GET"])
def register_courier_form():
    # Ruta corregida para el formulario de registro en la raíz de templates
    return render_template("register_courier.html", error=None)


@courier_blueprint.route("/register", methods=["POST"])
def register_courier_web():
    birthdate_value = request.form.get("birthdate")
    try:
        # Procesamiento seguro de fechas sin usar utcnow depreciado
        parsed_date = datetime.fromisoformat(birthdate_value).date() if birthdate_value else datetime.now(timezone.utc).date()
    except ValueError:
        return render_template("register_courier.html", error="Formato de fecha de nacimiento inválido.")

    courier = Courier(
        id=None,
        name=request.form.get("name", ""),
        nif=request.form.get("nif", ""),
        birthdate=parsed_date,
        phone=request.form.get("phone", ""),
        whatsapp=request.form.get("whatsapp", ""),
        email=request.form.get("email", ""),
        vehicle=request.form.get("vehicle", ""),
    )
    try:
        _get_service().register(courier)
        # Redirección sincronizada con el nombre del Blueprint unificado
        return redirect(url_for("courier_blueprint.list_couriers"))
    except Exception as error:
        # Ruta corregida para recargar el formulario si ocurre un error
        return render_template("register_courier.html", error=str(error))


@courier_blueprint.route("/", methods=["POST"])
def register_courier():
    payload = request.json or {}
    birthdate_value = payload.get("birthdate")
    try:
        parsed_date = datetime.fromisoformat(birthdate_value).date() if birthdate_value else datetime.now(timezone.utc).date()
    except ValueError:
        return jsonify({"error": "Formato de fecha de nacimiento inválido."}), 400

    courier = Courier(
        id=None,
        name=payload.get("name", ""),
        nif=payload.get("nif", ""),
        birthdate=parsed_date,
        phone=payload.get("phone", ""),
        whatsapp=payload.get("whatsapp", ""),
        email=payload.get("email", ""),
        vehicle=payload.get("vehicle", ""),
    )
    try:
        result = _get_service().register(courier)
        return jsonify(result.__dict__), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@courier_blueprint.route("/active", methods=["GET"])
def list_active_couriers():
    couriers = _get_service().list_active()
    return jsonify([courier.__dict__ for courier in couriers]), 200
