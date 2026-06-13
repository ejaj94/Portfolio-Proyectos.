from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for

from delivery_app.entities.restaurant import Restaurant
from delivery_app.exceptions import BusinessRuleError, EntityNotFoundError, ValidationError
from delivery_app.services.restaurant_service import RestaurantService

# Nombre del Blueprint sincronizado exactamente con tu barra de navegación (base.html)
restaurant_blueprint = Blueprint("restaurant_blueprint", __name__, url_prefix="/restaurants")


def _get_service() -> RestaurantService:
    repositories = current_app.extensions["repositories"]
    return RestaurantService(repositories["restaurant"])


@restaurant_blueprint.route("/", methods=["GET"])
def list_restaurants():
    service = _get_service()
    restaurants = service.list()
    if request.headers.get('Accept') == 'application/json':
        return jsonify([restaurant.__dict__ for restaurant in restaurants]), 200
    else:
        # Ruta corregida apuntando a la raíz del directorio de plantillas
        return render_template("list_restaurants.html", restaurants=restaurants)


@restaurant_blueprint.route("/register", methods=["GET"])
def register_restaurant_form():
    # Ruta de plantilla unificada corregida y sangrado corregido
    return render_template("register_restaurant.html")


@restaurant_blueprint.route("/register", methods=["POST"])
def register_restaurant_web():
    restaurant = Restaurant(
        id=None,
        name=request.form.get("name", ""),
        owner_name=request.form.get("owner_name", ""),
        nif=request.form.get("nif", ""),
        phone=request.form.get("phone", ""),
        whatsapp=request.form.get("whatsapp", ""),
        email=request.form.get("email", ""),
        address=request.form.get("address", ""),
        map_link=request.form.get("map_link"),
        logo_url=request.form.get("logo_url"),
    )
    try:
        _get_service().register(restaurant)
        # Redirección sincronizada con el nombre del Blueprint unificado
        return redirect(url_for("restaurant_blueprint.list_restaurants"))
    except (ValidationError, BusinessRuleError) as error:
        # Ruta corregida para manejar errores devolviendo la misma plantilla correcta
        return render_template("register_restaurant.html", error=str(error))


# --- ENDPOINTS PARA LA API (JSON) ---

@restaurant_blueprint.route("/", methods=["POST"])
def register_restaurant():
    payload = request.json or {}
    restaurant = Restaurant(
        id=None,
        name=payload.get("name", ""),
        owner_name=payload.get("owner_name", ""),
        nif=payload.get("nif", ""),
        phone=payload.get("phone", ""),
        whatsapp=payload.get("whatsapp", ""),
        email=payload.get("email", ""),
        address=payload.get("address", ""),
        map_link=payload.get("map_link"),
        logo_url=payload.get("logo_url"),
    )
    try:
        result = _get_service().register(restaurant)
        return jsonify(result.__dict__), 201
    except (ValidationError, BusinessRuleError) as error:
        return jsonify({"error": str(error)}), 400


@restaurant_blueprint.route("/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id: int):
    try:
        restaurant = _get_service().get(restaurant_id)
        return jsonify(restaurant.__dict__), 200
    except EntityNotFoundError as error:
        return jsonify({"error": str(error)}), 404
