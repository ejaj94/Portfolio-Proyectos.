import uuid
import random
from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for

from delivery_app.entities.client import Client
from delivery_app.exceptions import EntityNotFoundError, ValidationError
from delivery_app.services.client_service import ClientService

# Nombre del Blueprint sincronizado con la barra de navegación global (base.html)
client_blueprint = Blueprint("client_blueprint", __name__, url_prefix="/clients")


def _get_service() -> ClientService:
    repositories = current_app.extensions["repositories"]
    return ClientService(repositories["client"], repositories["restaurant"])


@client_blueprint.route("/", methods=["GET"])
def list_clients():
    service = _get_service()
    clients = service.list()
    if request.headers.get("Accept") == "application/json":
        return jsonify([client.__dict__ for client in clients]), 200
        
    # Ruta corregida apuntando directamente a la raíz de templates
    return render_template("list_clients.html", clients=clients)


@client_blueprint.route("/register", methods=["GET"])
def register_client_form():
    # Ruta corregida apuntando directamente a la raíz de templates
    return render_template("register_client.html", error=None)


@client_blueprint.route("/register", methods=["POST"])
def register_client_web():
    # Inyectamos el ID 1 de forma interna para cumplir con las restricciones actuales del backend.
    restaurant_id = 1

    email_token = str(uuid.uuid4())
    phone_pin = f"{random.randint(1000, 9999):04d}"

    client = Client(
        id=None,
        restaurant_id=restaurant_id,
        name=request.form.get("name", ""),
        phone=request.form.get("phone", ""),
        whatsapp=request.form.get("whatsapp", ""),
        email=request.form.get("email", ""),
        address=request.form.get("address", ""),
        map_link=request.form.get("map_link"),
        is_email_verified=0,
        is_phone_verified=0,
        email_verification_token=email_token,
        phone_verification_pin=phone_pin,
        stripe_customer_id=""
    )
    try:
        registered = _get_service().register(client)
        
        # Simulación de envío por Consola
        print("\n" + "="*50)
        print("📨 SIMULACIÓN DE REGISTRO DE CLIENTE (ENTORNO DE PRUEBAS)")
        print(f"Cliente registrado: {registered.name} (ID: {registered.id})")
        print(f"PIN de Verificación de Teléfono: {phone_pin}")
        verify_url = f"{request.host_url.rstrip('/')}{url_for('client_blueprint.verify_email', token=email_token)}"
        print(f"Enlace de Verificación de Email: {verify_url}")
        print("="*50 + "\n")
        
        # Redirección sincronizada con la interfaz de verificación
        return redirect(url_for("client_blueprint.verify_client_view", client_id=registered.id))
    except ValidationError as error:
        # Ruta corregida para recargar el formulario si falla la validación
        return render_template("register_client.html", error=str(error))


@client_blueprint.route("/verify", methods=["GET"])
def verify_client_view():
    client_id = request.args.get("client_id", type=int)
    if not client_id:
        return redirect(url_for("client_blueprint.list_clients"))
    
    repositories = current_app.extensions["repositories"]
    try:
        client = repositories["client"].get_by_id(client_id)
    except EntityNotFoundError:
        return redirect(url_for("client_blueprint.list_clients"))

    # Si ya está verificado completo, podemos dejarlo pasar
    if client.is_email_verified and client.is_phone_verified:
        return redirect(f"/apps/client?client_id={client.id}")
        
    return render_template("verify_client.html", client=client)


@client_blueprint.route("/verify-email", methods=["GET"])
def verify_email():
    token = request.args.get("token", "")
    if not token:
        return "Token inválido.", 400

    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]
    
    # Buscar el cliente correspondiente al token
    all_clients = client_repo.list_all()
    target_client = None
    for c in all_clients:
        if c.email_verification_token == token:
            target_client = c
            break
            
    if not target_client:
        return "Token de verificación no encontrado o expirado.", 404
        
    target_client.is_email_verified = 1
    client_repo.update(target_client)
    
    # Redirigir de vuelta al verificador con éxito
    return redirect(url_for("client_blueprint.verify_client_view", client_id=target_client.id, email_success="1"))


@client_blueprint.route("/", methods=["POST"])
def register_client():
    payload = request.json or {}
    email_token = str(uuid.uuid4())
    phone_pin = f"{random.randint(1000, 9999):04d}"
    
    client = Client(
        id=None,
        restaurant_id=payload.get("restaurant_id", 1),
        name=payload.get("name", ""),
        phone=payload.get("phone", ""),
        whatsapp=payload.get("whatsapp", ""),
        email=payload.get("email", ""),
        address=payload.get("address", ""),
        map_link=payload.get("map_link"),
        is_email_verified=0,
        is_phone_verified=0,
        email_verification_token=email_token,
        phone_verification_pin=phone_pin,
        stripe_customer_id=""
    )
    try:
        result = _get_service().register(client)
        return jsonify(result.__dict__), 201
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400


@client_blueprint.route("/search", methods=["GET"])
def search_client():
    restaurant_id = request.args.get("restaurant_id", type=int)
    term = request.args.get("term", "")
    try:
        clients = _get_service().search(restaurant_id, term)
        return jsonify([client.__dict__ for client in clients]), 200
    except (ValidationError, EntityNotFoundError) as error:
        return jsonify({"error": str(error)}), 400

