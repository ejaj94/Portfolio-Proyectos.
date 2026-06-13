from flask import Blueprint, current_app, jsonify, request, session, abort
import stripe
import uuid
import os
from delivery_app.entities.order import Order
from delivery_app.entities.client import Client
from delivery_app.exceptions import BusinessRuleError, ValidationError, EntityNotFoundError
from delivery_app.services.restaurant_service import RestaurantService
from delivery_app.services.order_service import OrderService
from delivery_app.services.client_service import ClientService
from delivery_app.extensions import socketio 

client_api_blueprint = Blueprint("client_api_blueprint", __name__, url_prefix="/api/v1/clients")

def _get_restaurant_service() -> RestaurantService:
    repositories = current_app.extensions["repositories"]
    return RestaurantService(repositories["restaurant"])

def _get_order_service() -> OrderService:
    repositories = current_app.extensions["repositories"]
    return OrderService(
        repositories["order"],
        repositories["restaurant"],
        repositories["client"],
        repositories["courier"],
    )

@client_api_blueprint.route("/restaurants", methods=["GET"])
def get_available_restaurants():
    """Lista todos los restaurantes con opción de filtrar por región"""
    if not session.get("client_id") or session.get("role") != "client":
        abort(403)
    service = _get_restaurant_service()
    restaurants = service.list()
    
    region = request.args.get("region")
    if region and region != "ALL":
        restaurants = [r for r in restaurants if r.region == region]
        
    return jsonify([restaurant.to_dict() if hasattr(restaurant, 'to_dict') else restaurant.__dict__ for restaurant in restaurants]), 200


@client_api_blueprint.route("/orders/initiate-payment", methods=["POST"])
def initiate_payment():
    """PASO 1 BANCARIO (REAL/MOCK): Genera la intención de cobro en Stripe"""
    if not session.get("client_id") or session.get("role") != "client":
        abort(403)
    payload = request.json or {}
    monto_total = payload.get("total_amount", 0) 
    currency = payload.get("currency", "eur")
    payment_method_type = payload.get("payment_method_type", "card") # 'card' o 'mb_way'

    if monto_total <= 0:
        return jsonify({"error": "El monto total debe ser mayor a cero centavos."}), 400

    if payment_method_type == "mb_way":
        currency = "eur" # MB WAY es exclusivo de Euros

    sk = stripe.api_key or ""
    is_mock = sk.startswith("sk_test_51Mockup") or not sk

    if is_mock:
        intent_id = f"pi_mock_mbway_{uuid.uuid4().hex[:10]}" if payment_method_type == "mb_way" else f"pi_mock_charge_{uuid.uuid4().hex[:10]}"
        client_secret = f"{intent_id}_secret_{uuid.uuid4().hex[:15]}"
        return jsonify({
            "status": "REQUIRES_CUSTOMER_ACTION",
            "payment_intent_id": intent_id,
            "client_secret": client_secret,
            "message": "Intención de pago simulada creada."
        }), 200

    try:
        if payment_method_type == "mb_way":
            intent = stripe.PaymentIntent.create(
                amount=monto_total,
                currency=currency,
                payment_method_types=["mb_way"],
            )
        else:
            intent = stripe.PaymentIntent.create(
                amount=monto_total,
                currency=currency,
                automatic_payment_methods={"enabled": True},
            )

        return jsonify({
            "status": "REQUIRES_CUSTOMER_ACTION",
            "payment_intent_id": intent.id,
            "client_secret": intent.client_secret,
            "message": "Intención de pago creada."
        }), 200

    except stripe.error.StripeError as e:
        return jsonify({"error": "Fallo en la comunicación con Stripe.", "details": e.user_message}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor.", "details": str(e)}), 500


@client_api_blueprint.route("/orders/confirm", methods=["POST"])
def confirm_order_and_payment():
    """PASO 2 BANCARIO HÍBRIDO (REAL/MOCK): Valida transacción (tarjeta/efectivo) y procesa orden en DB"""
    s_client_id = session.get("client_id")
    if not s_client_id or session.get("role") != "client":
        abort(403)
    payload = request.json or {}
    payment_method = payload.get("payment_method", "card")  # 'card' o 'cash'
    payment_intent_id = payload.get("payment_intent_id")
    client_id = s_client_id
    restaurant_id = payload.get("restaurant_id", 1)
    note = payload.get("note", "")

    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]

    try:
        client = client_repo.get_by_id(client_id)
    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado para registrar comanda."}), 404

    # 1. FLUJO DE PAGO EN EFECTIVO (CASH)
    if payment_method == "cash" or payment_intent_id == "cash":
        intent_id = "cash_payment_" + uuid.uuid4().hex[:10]
        # Inyectar indicador de efectivo en la nota si no lo tiene
        if "MÉTODO DE PAGO: EFECTIVO" not in note:
            note = f"💵 MÉTODO DE PAGO: EFECTIVO (Pago contra entrega) || {note}"
    
    # 2. FLUJO DE PAGO CON TARJETA GUARDADA O MB WAY (STRIPE)
    else:
        if payment_method == "mb_way":
            if "MÉTODO DE PAGO: MB WAY" not in note:
                note = f"📲 MÉTODO DE PAGO: MB WAY || {note}"
                
        # A. Si ya viene con un payment_intent_id exitoso tras completar 3D Secure en el cliente
        if payment_intent_id:
            if payment_intent_id.startswith("pi_mock"):
                intent_id = payment_intent_id
            else:
                try:
                    intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    if intent.status != "succeeded":
                        return jsonify({"error": f"Pago no liquidado en Stripe. Estado: {intent.status}"}), 402
                    intent_id = intent.id
                except stripe.error.StripeError as e:
                    return jsonify({"error": "No se pudo verificar el pago en Stripe.", "details": e.user_message}), 400
        
        # B. Si nos mandan un payment_method_id para cobrar directamente desde el servidor
        else:
            payment_method_id = payload.get("payment_method_id")
            total_amount = payload.get("total_amount", 0)  # En centavos
            
            if not payment_method_id:
                return jsonify({"error": "Se requiere un método de pago (tarjeta o efectivo)."}), 400
            if total_amount <= 0:
                return jsonify({"error": "Monto de transacción inválido."}), 400

            sk = stripe.api_key or ""
            is_mock = sk.startswith("sk_test_51Mockup") or (client.stripe_customer_id and client.stripe_customer_id.startswith("cus_mock"))

            if is_mock or payment_method_id.startswith("pm_mock"):
                intent_id = "pi_mock_charge_" + uuid.uuid4().hex[:10]
            else:
                try:
                    # Crear y confirmar el cobro inmediatamente (3D Secure compatible)
                    intent = stripe.PaymentIntent.create(
                        amount=total_amount,
                        currency="eur",
                        customer=client.stripe_customer_id,
                        payment_method=payment_method_id,
                        confirm=True,
                        off_session=True,  # Para tarjetas guardadas
                    )
                    intent_id = intent.id
                except stripe.error.CardError as e:
                    err = e.error
                    # Si requiere autenticación 3D Secure / SCA
                    if err.payment_intent and err.payment_intent.status == "requires_action":
                        return jsonify({
                            "status": "REQUIRES_ACTION",
                            "client_secret": err.payment_intent.client_secret,
                            "payment_intent_id": err.payment_intent.id
                        }), 200
                    return jsonify({"error": "Transacción rechazada por la entidad bancaria.", "details": e.user_message}), 402
                except stripe.error.StripeError as e:
                    return jsonify({"error": "Error al procesar cobro en Stripe.", "details": e.user_message}), 400

    # 3. CREAR Y REGISTRAR LA ORDEN EN BASE DE DATOS
    order = Order(
        id=None,
        restaurant_id=restaurant_id,
        client_id=client_id,
        courier_id=None,
        note=note,
        delivery_note=payload.get("delivery_note", ""),
        status="PENDIENTE"
    )

    try:
        order_service = _get_order_service()
        result = order_service.create(order)

        order_data = {
            "order_id": result.id,
            "restaurant_id": result.restaurant_id,
            "client_id": result.client_id,
            "note": result.note,
            "delivery_note": result.delivery_note,
            "status": "PENDIENTE",
            "stripe_intent_id": intent_id
        }

        # Transmitimos el evento por Websockets en tiempo real para la KDS del Restaurante
        socketio.emit("nuevo_pedido", order_data)

        return jsonify({
            "status": "ORDER_PROCESSED",
            "message": "¡Pedido verificado y registrado exitosamente!",
            "order_id": result.id,
            "stripe_charge_id": intent_id
        }), 201

    except (ValidationError, BusinessRuleError, EntityNotFoundError) as error:
        # En caso de error de negocio y si el cobro fue real, intentamos hacer un refund
        if not payment_method == "cash" and not intent_id.startswith("pi_mock") and not intent_id.startswith("cash"):
            try:
                stripe.Refund.create(payment_intent=intent_id)
            except Exception:
                pass
        return jsonify({"error": "Error al registrar la comanda.", "details": str(error)}), 400


@client_api_blueprint.route("/register", methods=["POST"])
def api_register_client_automatically():
    payload = request.json or {}
    client = Client(
        id=None,
        restaurant_id=1, 
        name=payload.get("name", ""),
        phone=payload.get("phone", ""),
        whatsapp=payload.get("whatsapp", ""),
        email=payload.get("email", ""),
        address=payload.get("address", ""),
        map_link=payload.get("map_link")
    )
    try:
        repositories = current_app.extensions["repositories"]
        client_service = ClientService(repositories["client"], repositories["restaurant"])
        result = client_service.register(client)
        return jsonify({"status": "CLIENT_REGISTERED", "client_id": result.id}), 201
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400


@client_api_blueprint.route("/orders/<int:order_id>", methods=["GET"])
def get_order_details(order_id):
    """Consulta la ficha técnica extendida de un pedido para el rastreo por mapa"""
    try:
        order_service = _get_order_service()
        order = order_service.get(order_id)
        
        # Security Guard: Only client, assigned courier, or restaurant partner can view order details
        role = session.get("role")
        user_authorized = False
        if role == "client":
            user_authorized = (session.get("client_id") == order.client_id)
        elif role == "courier":
            user_authorized = (session.get("courier_id") == order.courier_id) or (order.courier_id is None and order.status == "LISTO_PARA_RECOGER")
        elif role == "restaurant":
            user_authorized = (session.get("restaurant_id") == order.restaurant_id)
            
        if not user_authorized:
            abort(403)
            
        repositories = current_app.extensions["repositories"]
        rest = repositories["restaurant"].get_by_id(order.restaurant_id)
        client = repositories["client"].get_by_id(order.client_id)
        
        courier_data = None
        if order.courier_id:
            try:
                courier = repositories["courier"].get_by_id(order.courier_id)
                courier_data = {
                    "id": courier.id,
                    "name": courier.name,
                    "phone": courier.phone,
                    "vehicle": courier.vehicle
                }
            except Exception:
                pass
                
        return jsonify({
            "order_id": order.id,
            "restaurant_id": order.restaurant_id,
            "client_id": order.client_id,
            "courier_id": order.courier_id,
            "note": order.note,
            "status": order.status,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "accepted_at": order.accepted_at.isoformat() if order.accepted_at else None,
            "picked_up_at": order.picked_up_at.isoformat() if order.picked_up_at else None,
            "delivered_at": order.delivered_at.isoformat() if order.delivered_at else None,
            "restaurant": {
                "id": rest.id,
                "name": rest.name,
                "address": rest.address,
                "phone": rest.phone
            },
            "client": {
                "id": client.id,
                "name": client.name,
                "address": client.address,
                "phone": client.phone
            },
            "courier": courier_data
        }), 200
    except EntityNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor.", "details": str(e)}), 500


# =========================================================================
# 🔒 NUEVAS APIS DE VERIFICACIÓN DE CLIENTES (EMAIL Y PIN TELEFÓNICO)
# =========================================================================

@client_api_blueprint.route("/verify-status", methods=["GET"])
def get_verify_status():
    """Consulta en vivo el estado de verificación de la cuenta del cliente (Polling)"""
    client_id = request.args.get("client_id", type=int)
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    if not client_id:
        return jsonify({"error": "Se requiere el parámetro client_id."}), 400

    repositories = current_app.extensions["repositories"]
    try:
        client = repositories["client"].get_by_id(client_id)
        return jsonify({
            "client_id": client.id,
            "is_email_verified": bool(client.is_email_verified),
            "is_phone_verified": bool(client.is_phone_verified)
        }), 200
    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado."}), 404


@client_api_blueprint.route("/verify-phone", methods=["POST"])
def verify_phone_pin():
    """Valida el código PIN de 4 dígitos para activar el número telefónico del cliente"""
    payload = request.json or {}
    client_id = payload.get("client_id")
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    pin = payload.get("pin")

    if not client_id or not pin:
        return jsonify({"error": "client_id y pin son campos requeridos."}), 400

    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]
    try:
        client = client_repo.get_by_id(client_id)
        
        # Validación de PIN
        if client.phone_verification_pin == str(pin).strip():
            client.is_phone_verified = 1
            client_repo.update(client)
            return jsonify({"status": "verified", "message": "Número telefónico activado correctamente."}), 200
        else:
            return jsonify({"error": "El código PIN ingresado es incorrecto. Vuelve a intentarlo."}), 400
    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado."}), 404


# =========================================================================
# 💳 NUEVAS APIS DE LA BILLETERA DIGITAL (STRIPE WALLET CARDS INTEGRATION)
# =========================================================================

@client_api_blueprint.route("/payment-config", methods=["GET"])
def get_payment_config():
    """Entrega la publishable key de Stripe configurada para Elements"""
    sk = stripe.api_key or ""
    if sk.startswith("sk_test_51Mockup") or not sk:
        pk = "pk_test_51MockupKeyDePruebaTotalmenteSeguraParaTuFrontendFlask1234567890"
    else:
        pk = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_51MockupKeyDePruebaTotalmenteSeguraParaTuFrontendFlask1234567890")
    return jsonify({"publishable_key": pk}), 200


@client_api_blueprint.route("/cards/setup-intent", methods=["POST"])
def create_setup_intent():
    """Genera un SetupIntent vinculando al cliente en base de datos con Stripe"""
    payload = request.json or {}
    client_id = payload.get("client_id")
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    
    if not client_id:
        return jsonify({"error": "client_id es requerido."}), 400

    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]
    try:
        client = client_repo.get_by_id(client_id)
        
        sk = stripe.api_key or ""
        is_mock = sk.startswith("sk_test_51Mockup")

        customer_id = client.stripe_customer_id

        # 1. Crear el cliente en Stripe si no está creado aún
        if not customer_id:
            if is_mock:
                customer_id = f"cus_mock_{uuid.uuid4().hex[:10]}"
            else:
                try:
                    customer = stripe.Customer.create(
                        email=client.email,
                        name=client.name,
                        phone=client.phone,
                        metadata={"client_id": client.id}
                    )
                    customer_id = customer.id
                except stripe.error.StripeError as e:
                    return jsonify({"error": "Error al registrar cliente en Stripe.", "details": e.user_message}), 400

            client.stripe_customer_id = customer_id
            client_repo.update(client)

        # 2. Generar SetupIntent
        if is_mock or customer_id.startswith("cus_mock"):
            setup_intent_id = f"seti_mock_{uuid.uuid4().hex[:10]}"
            client_secret = f"seti_mock_secret_{uuid.uuid4().hex[:15]}"
        else:
            try:
                setup_intent = stripe.SetupIntent.create(
                    customer=customer_id,
                    payment_method_types=["card"]
                )
                setup_intent_id = setup_intent.id
                client_secret = setup_intent.client_secret
            except stripe.error.StripeError as e:
                return jsonify({"error": "Error al generar SetupIntent en Stripe.", "details": e.user_message}), 400

        return jsonify({
            "setup_intent_id": setup_intent_id,
            "client_secret": client_secret,
            "stripe_customer_id": customer_id
        }), 200

    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado."}), 404


@client_api_blueprint.route("/cards", methods=["GET"])
def list_client_cards():
    """Recupera la lista de tarjetas guardadas en la billetera del cliente"""
    client_id = request.args.get("client_id", type=int)
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    if not client_id:
        return jsonify({"error": "client_id es requerido."}), 400

    repositories = current_app.extensions["repositories"]
    try:
        client = repositories["client"].get_by_id(client_id)
        customer_id = client.stripe_customer_id

        if not customer_id:
            return jsonify([]), 200

        sk = stripe.api_key or ""
        is_mock = sk.startswith("sk_test_51Mockup") or customer_id.startswith("cus_mock")

        if is_mock:
            # Recuperar tarjetas simuladas guardadas en el store de la app
            mock_store = current_app.config.setdefault("MOCK_CARDS_STORE", {})
            cards = mock_store.get(client.id, [
                {
                    "id": "pm_mock_default_visa",
                    "brand": "visa",
                    "last4": "4242",
                    "exp_month": 12,
                    "exp_year": 2030,
                    "funding": "credit",
                    "cardholder": client.name
                }
            ])
            return jsonify(cards), 200
        else:
            try:
                payment_methods = stripe.PaymentMethod.list(
                    customer=customer_id,
                    type="card"
                )
                cards = []
                for pm in payment_methods.data:
                    cards.append({
                        "id": pm.id,
                        "brand": pm.card.brand,
                        "last4": pm.card.last4,
                        "exp_month": pm.card.exp_month,
                        "exp_year": pm.card.exp_year,
                        "funding": pm.card.funding,
                        "cardholder": pm.billing_details.name or client.name
                    })
                return jsonify(cards), 200
            except stripe.error.StripeError as e:
                return jsonify({"error": "Error al listar tarjetas desde Stripe.", "details": e.user_message}), 400

    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado."}), 404


@client_api_blueprint.route("/cards/attach", methods=["POST"])
def attach_client_card():
    """Asocia un nuevo método de pago confirmado al cliente en Stripe"""
    payload = request.json or {}
    client_id = payload.get("client_id")
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    payment_method_id = payload.get("payment_method_id")

    if not client_id or not payment_method_id:
        return jsonify({"error": "client_id y payment_method_id son requeridos."}), 400

    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]
    try:
        client = client_repo.get_by_id(client_id)
        customer_id = client.stripe_customer_id

        if not customer_id:
            return jsonify({"error": "El cliente no tiene un perfil de pagos inicializado."}), 400

        sk = stripe.api_key or ""
        is_mock = sk.startswith("sk_test_51Mockup") or customer_id.startswith("cus_mock")

        if is_mock or payment_method_id.startswith("pm_mock"):
            # Flujo simulado de adjuntar tarjeta
            mock_store = current_app.config.setdefault("MOCK_CARDS_STORE", {})
            cards = mock_store.setdefault(client.id, [])
            
            # Sanitizar id y marca
            pm_id = payment_method_id if payment_method_id.startswith("pm_") else f"pm_mock_{uuid.uuid4().hex[:10]}"
            brand = "mastercard" if "master" in pm_id.lower() or "5555" in pm_id else "visa"
            last4 = "4242"
            if len(payment_method_id) >= 4 and payment_method_id[-4:].isdigit():
                last4 = payment_method_id[-4:]

            new_card = {
                "id": pm_id,
                "brand": brand,
                "last4": last4,
                "exp_month": 10,
                "exp_year": 2031,
                "funding": "credit",
                "cardholder": client.name
            }
            
            if not any(c["id"] == pm_id for c in cards):
                cards.append(new_card)
                
            return jsonify({"status": "attached", "card": new_card}), 200
        else:
            try:
                # Adjuntar tarjeta al Customer de Stripe
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer_id
                )
                # Opcional: Registrarla como predeterminada de facturas
                stripe.Customer.modify(
                    customer_id,
                    invoice_settings={"default_payment_method": payment_method_id}
                )

                pm = stripe.PaymentMethod.retrieve(payment_method_id)
                card_data = {
                    "id": pm.id,
                    "brand": pm.card.brand,
                    "last4": pm.card.last4,
                    "exp_month": pm.card.exp_month,
                    "exp_year": pm.card.exp_year,
                    "funding": pm.card.funding,
                    "cardholder": pm.billing_details.name or client.name
                }
                return jsonify({"status": "attached", "card": card_data}), 200
            except stripe.error.StripeError as e:
                return jsonify({"error": "Error al adjuntar método de pago en Stripe.", "details": e.user_message}), 400

    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado."}), 404


@client_api_blueprint.route("/cards/detach", methods=["POST"])
def detach_client_card():
    """Elimina una tarjeta (PaymentMethod) del perfil de pagos del cliente"""
    payload = request.json or {}
    client_id = payload.get("client_id")
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    payment_method_id = payload.get("payment_method_id")

    if not client_id or not payment_method_id:
        return jsonify({"error": "client_id y payment_method_id son requeridos."}), 400

    repositories = current_app.extensions["repositories"]
    try:
        client = repositories["client"].get_by_id(client_id)
        customer_id = client.stripe_customer_id

        sk = stripe.api_key or ""
        is_mock = sk.startswith("sk_test_51Mockup") or (customer_id and customer_id.startswith("cus_mock"))

        if is_mock:
            # Flujo simulado de eliminar tarjeta
            mock_store = current_app.config.setdefault("MOCK_CARDS_STORE", {})
            if client.id in mock_store:
                mock_store[client.id] = [c for c in mock_store[client.id] if c["id"] != payment_method_id]
            return jsonify({"status": "detached", "message": "Tarjeta desvinculada correctamente de tu billetera."}), 200
        else:
            try:
                stripe.PaymentMethod.detach(payment_method_id)
                return jsonify({"status": "detached", "message": "Tarjeta eliminada de Stripe con éxito."}), 200
            except stripe.error.StripeError as e:
                return jsonify({"error": "Error al eliminar tarjeta en Stripe.", "details": e.user_message}), 400

    except EntityNotFoundError:
        return jsonify({"error": "Cliente no encontrado."}), 404


@client_api_blueprint.route("/reset-demo-db", methods=["POST"])
def reset_demo_database_api():
    """Limpia todos los pedidos e historiales y vuelve a sembrar los datos demo para la demostración en vivo."""
    if not session.get("dev_authorized"):
        abort(403)
        
    import sqlite3
    
    db_path = current_app.config.get("DATABASE_PATH", "delivery_app.db")
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = OFF;")
    
    try:
        tables = [
            "orders", 
            "clients", 
            "couriers", 
            "restaurants", 
            "restaurant_favorite_couriers", 
            "restaurant_blocked_couriers",
            "plates",
            "client_favorite_restaurants"
        ]
        for table in tables:
            conn.execute(f"DELETE FROM {table};")
            conn.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")
            
        conn.execute(
            """
            INSERT INTO restaurants (
                id, name, owner_name, nif, phone, whatsapp, email, address, map_link, logo_url, banner_url, region
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "Com Cheiro de Amor",
                "Manuel Silva",
                "500123456",
                "+351210000000",
                "+351910000000",
                "geral@comcheirodeamor.pt",
                "Rua de Santa Catarina 123, Porto, Portugal",
                "https://maps.google.com/?q=Rua+de+Santa+Catarina+123+Porto",
                "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=150&q=80",
                "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
                "Porto"
            )
        )
        
        plates = [
            (1, 1, "Pizza Margherita", 8.50, "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=400&q=80", "Molho de tomate fresco, mozzarella fior di latte, manjericão fresco e azeite extra virgem.", "Pizzas", 0),
            (2, 1, "Pizza Pepperoni", 9.50, "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=400&q=80", "Molho de tomate, queijo mozzarella e pepperoni artesanal picante fatiado.", "Pizzas", 0),
            (3, 1, "Hambúrguer Clássico", 7.90, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=400&q=80", "Carne bovina grelhada 150g, queijo cheddar, alface, tomate e molho especial da casa.", "Hambúrgueres", 0),
            (4, 1, "Hambúrguer de Frango Crocante", 8.20, "https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?auto=format&fit=crop&w=400&q=80", "Peito de frango crocante, bacon caramelizado, maionese de alho e rúcula fresca.", "Hambúrgueres", 1),
            (5, 1, "Tiramisú Clássico", 4.50, "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=400&q=80", "Sobremesa italiana caseira com biscoito champanhe, café e queijo mascarpone polvilhado com cacau.", "Sobremesas", 0),
            (6, 1, "Petit Gâteau", 4.90, "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=400&q=80", "Bolo quente de chocolate com recheio cremoso, servido com uma bola de gelado de baunilha.", "Sobremesas", 1),
            (7, 1, "Cerveja Sagres 33cl", 2.00, "https://images.unsplash.com/photo-1608270176054-8a7300f6e6b0?auto=format&fit=crop&w=400&q=80", "Cerveja lager portuguesa clássica e fresca.", "Bebidas", 0),
            (8, 1, "Refrigerante Coca-Cola", 1.80, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80", "Lata de 33cl servida bem gelada.", "Bebidas", 0)
        ]
        
        for p in plates:
            conn.execute(
                """
                INSERT INTO plates (id, restaurant_id, name, price, image_url, description, category, is_weekly)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                p
            )
        
        conn.commit()
        return jsonify({"status": "success", "message": "Base de datos demo restablecida con éxito."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# --- FASE 10: ENDPOINTS DE FAVORITOS ---
@client_api_blueprint.route("/<int:client_id>/favorites", methods=["GET"])
def get_client_favorites(client_id):
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]
    try:
        favs = client_repo.list_favorites(client_id)
        return jsonify(favs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_api_blueprint.route("/<int:client_id>/favorites", methods=["POST"])
def toggle_client_favorite(client_id):
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    payload = request.json or {}
    restaurant_id = payload.get("restaurant_id")
    action = payload.get("action", "add") # "add" or "remove"
    if not restaurant_id:
        return jsonify({"error": "restaurant_id es requerido."}), 400
        
    repositories = current_app.extensions["repositories"]
    client_repo = repositories["client"]
    try:
        if action == "add":
            client_repo.add_favorite(client_id, restaurant_id)
        else:
            client_repo.remove_favorite(client_id, restaurant_id)
        return jsonify({"status": "success", "favorites": client_repo.list_favorites(client_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@client_api_blueprint.route("/<int:client_id>/orders", methods=["GET"])
def get_client_orders(client_id):
    if not session.get("client_id") or session.get("role") != "client" or int(session.get("client_id")) != int(client_id):
        abort(403)
    repositories = current_app.extensions["repositories"]
    order_repo = repositories["order"]
    try:
        orders = order_repo.list_all()
        client_orders = [o for o in orders if o.client_id == client_id]
        
        # Decorar con nombre de restaurante
        rest_repo = repositories["restaurant"]
        decorated_orders = []
        for o in client_orders:
            try:
                rest = rest_repo.get_by_id(o.restaurant_id)
                rest_name = rest.name
            except Exception:
                rest_name = f"Restaurante #{o.restaurant_id}"
                
            decorated_orders.append({
                "id": o.id,
                "restaurant_name": rest_name,
                "note": o.note,
                "delivery_note": o.delivery_note or "",
                "status": o.status,
                "created_at": o.created_at.isoformat() if o.created_at else None
            })
        return jsonify(decorated_orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


