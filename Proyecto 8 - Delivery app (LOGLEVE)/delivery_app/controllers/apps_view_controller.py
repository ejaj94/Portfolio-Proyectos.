from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, abort, flash, send_from_directory
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import json
import os
import random
import smtplib
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from delivery_app.services.ia_verifier import verify_nif_portal_financas, verify_document_with_ia

def send_verification_code(client, method, phone, email, pin):
    print(f"\n=======================================================")
    print(f"ENVIANDO CODIGO DE VERIFICACION LOGLEVE")
    print(f"Cliente: {client.name}")
    print(f"Metodo de envio: {method.upper()}")
    print(f"Codigo PIN: {pin}")
    
    if method == "sms":
        print(f"Destinatario: {phone}")
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_FROM_NUMBER")
        if account_sid and auth_token and from_number:
            try:
                from twilio.rest import Client as TwilioClient
                twilio_client = TwilioClient(account_sid, auth_token)
                twilio_client.messages.create(
                    body=f"Logleve: O seu codigo de verificacao e {pin}",
                    from_=from_number,
                    to=phone
                )
                print(f"Twilio SMS enviado con exito.")
            except Exception as e:
                print(f"Error al enviar Twilio SMS: {e}")
        else:
            print("[SIMULACION SMS] Para envio real, configure las variables de entorno de Twilio (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER).")
            
    else: # email
        print(f"Destinatario: {email}")
        smtp_server = os.environ.get("SMTP_SERVER")
        smtp_port = os.environ.get("SMTP_PORT", "587")
        smtp_user = os.environ.get("SMTP_USER")
        smtp_pass = os.environ.get("SMTP_PASS")
        if smtp_server and smtp_user and smtp_pass:
            try:
                msg = MIMEText(f"Ola {client.name},\n\nO seu codigo de verificacao para ativar a conta Logleve e: {pin}\n\nSe nao solicitou este codigo, por favor ignore este email.\n\nEquipa Logleve.")
                msg['Subject'] = "Logleve - Codigo de Verificacao"
                msg['From'] = smtp_user
                msg['To'] = email
                
                with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
                print(f"Email SMTP enviado con exito.")
            except Exception as e:
                print(f"Error al enviar Email SMTP: {e}")
        else:
            print("[SIMULACION EMAIL] Para envio real, configure las variables de entorno SMTP (SMTP_SERVER, SMTP_USER, SMTP_PASS).")
    print(f"=======================================================\n")

def _is_email_registered(email):
    email_clean = email.strip().lower()
    # Check clients
    c_repo = current_app.extensions["repositories"]["client"]
    if c_repo.get_by_email(email_clean):
        return True
    # Check couriers
    co_repo = current_app.extensions["repositories"]["courier"]
    if co_repo.get_by_email(email_clean):
        return True
    # Check restaurants
    r_repo = current_app.extensions["repositories"]["restaurant"]
    if r_repo.get_by_email(email_clean):
        return True
    return False

def _is_nif_registered(nif):
    nif_clean = nif.strip().replace(" ", "")
    if not nif_clean:
        return False
    # Check couriers
    co_repo = current_app.extensions["repositories"]["courier"]
    for c in co_repo.list_all():
        if c.nif.strip().replace(" ", "") == nif_clean:
            return True
    # Check restaurants
    r_repo = current_app.extensions["repositories"]["restaurant"]
    for r in r_repo.list_all():
        if r.nif.strip().replace(" ", "") == nif_clean:
            return True
    return False


apps_view_blueprint = Blueprint("apps_view_blueprint", __name__, url_prefix="/apps")

# 🔒 DECORADORES DE SEGURIDAD (SESSION GUARDS)
def client_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("client_id") or session.get("role") != "client":
            return redirect(url_for("apps_view_blueprint.client_login"))
        return f(*args, **kwargs)
    return decorated_function

def courier_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("courier_id") or session.get("role") != "courier":
            return redirect(url_for("apps_view_blueprint.courier_login"))
        return f(*args, **kwargs)
    return decorated_function

def restaurant_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("restaurant_id") or session.get("role") != "restaurant":
            return redirect(url_for("apps_view_blueprint.restaurant_login"))
        return f(*args, **kwargs)
    return decorated_function


# =========================================================================
# 📱 PORTAL DEL CLIENTE (CLIENT APP)
# =========================================================================

@apps_view_blueprint.route("/client", methods=["GET"])
@client_login_required
def client_app_home():
    """Portal principal de la App de Clientes"""
    return render_template("app_client/index.html")

@apps_view_blueprint.route("/client/login", methods=["GET", "POST"])
def client_login():
    if session.get("client_id") and session.get("role") == "client":
        return redirect(url_for("apps_view_blueprint.client_app_home"))
        
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        client_repo = current_app.extensions["repositories"]["client"]
        client = client_repo.get_by_email(email)
        if client and check_password_hash(client.password_hash, password):
            session.clear()
            session["client_id"] = client.id
            session["role"] = "client"
            session["name"] = client.name
            return redirect(url_for("apps_view_blueprint.client_app_home"))
        error = "Email ou senha incorretos."
        
    return render_template("app_client/login.html", error=error)

@apps_view_blueprint.route("/client/register", methods=["GET", "POST"])
def client_register():
    if session.get("client_id") and session.get("role") == "client":
        return redirect(url_for("apps_view_blueprint.client_app_home"))
        
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        phone_prefix = request.form.get("phone_prefix", "").strip()
        phone = request.form.get("phone", "").strip()
        full_phone = f"{phone_prefix} {phone}".strip()
        address = request.form.get("address", "").strip()
        verification_method = request.form.get("verification_method", "email").strip()
        
        from delivery_app.entities.client import Client
        client_repo = current_app.extensions["repositories"]["client"]
        
        if _is_email_registered(email):
            error = "Este e-mail já está registado na plataforma."
        else:
            hashed_pwd = generate_password_hash(password)
            pin_code = str(random.randint(1000, 9999))
            
            # Create client with default restaurant_id=1 for unified sandbox demo
            new_client = Client(
                id=None,
                restaurant_id=1,
                name=name,
                phone=full_phone,
                whatsapp=full_phone,
                email=email.lower(),
                password_hash=hashed_pwd,
                address=address,
                map_link="",
                is_email_verified=1,
                is_phone_verified=0, # Will trigger verification step
                phone_verification_pin=pin_code,
                stripe_customer_id="",
                verification_method=verification_method
            )
            client_repo.add(new_client)
            
            # Send verification code via SMS/Email
            send_verification_code(new_client, verification_method, full_phone, email.lower(), pin_code)
            
            session.clear()
            session["client_id"] = new_client.id
            session["role"] = "client"
            session["name"] = new_client.name
            # Redirect to verify phone PIN
            return redirect(url_for("apps_view_blueprint.client_verify"))
            
    return render_template("app_client/register.html", error=error)

@apps_view_blueprint.route("/client/verify", methods=["GET", "POST"])
@client_login_required
def client_verify():
    error = None
    client_id = session.get("client_id")
    client_repo = current_app.extensions["repositories"]["client"]
    client = client_repo.get_by_id(client_id)
    
    if client.is_phone_verified == 1:
        return redirect(url_for("apps_view_blueprint.client_app_home"))
        
    if request.method == "POST":
        pin = request.form.get("pin", "").strip()
        if pin == client.phone_verification_pin:
            client.is_phone_verified = 1
            client_repo.update(client)
            return redirect(url_for("apps_view_blueprint.client_app_home"))
        error = "Código PIN de verificação incorreto."
        
    return render_template("app_client/verify.html", error=error, pin_demo=client.phone_verification_pin, client=client)

@apps_view_blueprint.route("/client/checkout/<int:restaurant_id>", methods=["GET"])
@client_login_required
def client_app_checkout(restaurant_id):
    client_id = session.get("client_id")
    client_repo = current_app.extensions["repositories"]["client"]
    client = client_repo.get_by_id(client_id)
    # Require phone verification to complete checkout, just like Uber Eats
    if client.is_phone_verified != 1:
        return redirect(url_for("apps_view_blueprint.client_verify"))
    return render_template("app_client/checkout.html", restaurant_id=restaurant_id)

@apps_view_blueprint.route("/client/tracking/<int:order_id>", methods=["GET"])
@client_login_required
def client_app_tracking(order_id):
    return render_template("app_client/tracking.html", order_id=order_id)

@apps_view_blueprint.route("/client/logout", methods=["GET"])
def client_logout():
    session.clear()
    return redirect(url_for("apps_view_blueprint.client_login"))


# =========================================================================
# 🛵 PORTAL DO ESTAFETA / REPARTIDOR (COURIER APP)
# =========================================================================

@apps_view_blueprint.route("/courier", methods=["GET"])
@courier_login_required
def courier_app_dashboard():
    """Portal principal del Estafeta (Mapa interactivo y pedidos)"""
    courier_id = session.get("courier_id")
    courier_repo = current_app.extensions["repositories"]["courier"]
    courier = courier_repo.get_by_id(courier_id)
    
    if courier.status == "pending":
        return render_template("app_courier/status.html", courier=courier, status="pending")
    elif courier.status == "rejected":
        if not session.get('ia_rejection_reason'):
            session['ia_rejection_reason'] = "Rejeitado na validação automática de documentos da IA Logleve. Por favor, carregue documentos válidos e com qualidade legível."
        return render_template("app_courier/status.html", courier=courier, status="rejected")
        
    return render_template("app_courier/dashboard.html", courier=courier)

@apps_view_blueprint.route("/courier/login", methods=["GET", "POST"])
def courier_login():
    if session.get("courier_id") and session.get("role") == "courier":
        return redirect(url_for("apps_view_blueprint.courier_app_dashboard"))
        
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        courier_repo = current_app.extensions["repositories"]["courier"]
        courier = courier_repo.get_by_email(email)
        if courier and check_password_hash(courier.password_hash, password):
            session.clear()
            session["courier_id"] = courier.id
            session["role"] = "courier"
            session["name"] = courier.name
            return redirect(url_for("apps_view_blueprint.courier_app_dashboard"))
        error = "Email ou senha incorretos."
        
    return render_template("app_courier/login.html", error=error)

@apps_view_blueprint.route("/courier/register", methods=["GET", "POST"])
def courier_register():
    if session.get("courier_id") and session.get("role") == "courier":
        return redirect(url_for("apps_view_blueprint.courier_app_dashboard"))
        
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        phone_prefix = request.form.get("phone_prefix", "").strip()
        phone = request.form.get("phone", "").strip()
        full_phone = f"{phone_prefix} {phone}".strip()
        nif = request.form.get("nif", "").strip()
        vehicle = request.form.get("vehicle", "motorcycle").strip()
        plate = request.form.get("plate", "").strip()
        
        # Files uploads
        saved = {}
        upload_dir = current_app.config.get('APP_ENTREGADOR_UPLOADS')
        if not upload_dir:
            upload_dir = os.path.join(current_app.root_path, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            current_app.config['APP_ENTREGADOR_UPLOADS'] = upload_dir
            
        for key in ('id_doc', 'vehicle_insurance', 'driver_license', 'profile_picture'):
            f = request.files.get(key)
            if f and f.filename:
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{f.filename}")
                dest = os.path.join(upload_dir, filename)
                f.save(dest)
                saved[key] = filename

        courier_repo = current_app.extensions["repositories"]["courier"]
        
        nif_ok, nif_msg = verify_nif_portal_financas(nif)
        
        is_motorized = vehicle in ('motorcycle', 'car')
        
        if _is_email_registered(email):
            error = "Este e-mail já está registado na plataforma."
        elif _is_nif_registered(nif):
            error = "Este NIF já está registado na plataforma."
        elif not nif_ok:
            error = f"Erro de NIF: {nif_msg}"
        elif not saved.get('profile_picture'):
            error = "A foto de perfil é de preenchimento obrigatório."
        elif not saved.get('id_doc'):
            error = "O Documento de Identidade ou Seguro é de preenchimento obrigatório."
        elif is_motorized and not saved.get('driver_license'):
            error = "A Carta de Condução é obrigatória para veículos motorizados."
        elif is_motorized and not saved.get('vehicle_insurance'):
            error = "O Seguro Veicular é obrigatório para vehículos motorizados."
        elif is_motorized and not plate:
            error = "A Matrícula do Veículo é obrigatória para vehículos motorizados."
        else:
            # Document verification with IA
            id_res = verify_document_with_ia('id_doc', os.path.join(upload_dir, saved['id_doc']))
            
            lic_res = {"status": "valid", "reason": "Não motorizado"}
            ins_res = {"status": "valid", "reason": "Não motorizado"}
            
            if is_motorized:
                lic_res = verify_document_with_ia('driver_license', os.path.join(upload_dir, saved['driver_license']))
                ins_res = verify_document_with_ia('vehicle_insurance', os.path.join(upload_dir, saved['vehicle_insurance']))
            
            # Combine IA status
            if id_res["status"] == "valid" and lic_res["status"] == "valid" and ins_res["status"] == "valid":
                status = "approved"
                session.pop('ia_rejection_reason', None)
            else:
                status = "rejected"
                reasons = []
                if id_res["status"] != "valid":
                    reasons.append(id_res["reason"])
                if is_motorized and lic_res["status"] != "valid":
                    reasons.append(lic_res["reason"])
                if is_motorized and ins_res["status"] != "valid":
                    reasons.append(ins_res["reason"])
                session['ia_rejection_reason'] = " | ".join(reasons)
            
            hashed_pwd = generate_password_hash(password)
            from delivery_app.entities.courier import Courier
            new_courier = Courier(
                id=None,
                name=name,
                nif=nif,
                birthdate=date(1995, 1, 1),
                phone=full_phone,
                whatsapp=full_phone,
                email=email.lower(),
                password_hash=hashed_pwd,
                vehicle=vehicle,
                active=True,
                vehicle_plate=plate if is_motorized else "",
                id_doc=saved.get('id_doc', ''),
                license_doc=saved.get('driver_license', '') if is_motorized else '',
                insurance_doc=saved.get('vehicle_insurance', '') if is_motorized else '',
                status=status,
                online_status=0,
                latitude=41.1579, # Default Porto Coordinates
                longitude=-8.6291,
                balance=0.0,
                profile_picture=saved.get('profile_picture', '')
            )
            courier_repo.add(new_courier)
            session.clear()
            # Restore rejection reason in session if rejected
            if status == "rejected":
                session['ia_rejection_reason'] = " | ".join(reasons)
            session["courier_id"] = new_courier.id
            session["role"] = "courier"
            session["name"] = new_courier.name
            
            return redirect(url_for("apps_view_blueprint.courier_app_dashboard"))
            
    return render_template("app_courier/register.html", error=error)

@apps_view_blueprint.route("/courier/earnings", methods=["GET"])
@courier_login_required
def courier_app_earnings():
    courier_id = session.get("courier_id")
    courier_repo = current_app.extensions["repositories"]["courier"]
    courier = courier_repo.get_by_id(courier_id)
    return render_template("app_courier/earnings.html", courier=courier)

@apps_view_blueprint.route("/courier/profile", methods=["GET"])
@courier_login_required
def courier_app_profile():
    courier_id = session.get("courier_id")
    courier_repo = current_app.extensions["repositories"]["courier"]
    courier = courier_repo.get_by_id(courier_id)
    return render_template("app_courier/profile.html", courier=courier)

@apps_view_blueprint.route("/courier/upload-doc", methods=["POST"])
@courier_login_required
def courier_upload_doc():
    courier_id = session.get("courier_id")
    courier_repo = current_app.extensions["repositories"]["courier"]
    courier = courier_repo.get_by_id(courier_id)
    
    doc_type = request.form.get("doc_type")
    f = request.files.get("file")
    
    if doc_type not in ('profile_picture', 'id_doc', 'driver_license', 'vehicle_insurance'):
        flash("Tipo de documento inválido.", "error")
        return redirect(url_for("apps_view_blueprint.courier_app_profile"))
        
    if not f or not f.filename:
        flash("Nenhum ficheiro selecionado.", "error")
        return redirect(url_for("apps_view_blueprint.courier_app_profile"))
        
    upload_dir = current_app.config.get('APP_ENTREGADOR_UPLOADS')
    if not upload_dir:
        upload_dir = os.path.join(current_app.root_path, "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        current_app.config['APP_ENTREGADOR_UPLOADS'] = upload_dir
        
    filename = secure_filename(f"{datetime.utcnow().timestamp()}_{f.filename}")
    dest = os.path.join(upload_dir, filename)
    f.save(dest)
    
    if doc_type == "profile_picture":
        courier.profile_picture = filename
    elif doc_type == "id_doc":
        courier.id_doc = filename
    elif doc_type == "driver_license":
        courier.license_doc = filename
    elif doc_type == "vehicle_insurance":
        courier.insurance_doc = filename
        
    # Recalculate status using OCR simulator
    is_motorized = courier.vehicle in ('motorcycle', 'car')
    
    id_file = os.path.join(upload_dir, courier.id_doc) if courier.id_doc else ""
    id_res = verify_document_with_ia('id_doc', id_file)
    
    lic_res = {"status": "valid", "reason": "Não motorizado"}
    ins_res = {"status": "valid", "reason": "Não motorizado"}
    
    if is_motorized:
        lic_file = os.path.join(upload_dir, courier.license_doc) if courier.license_doc else ""
        ins_file = os.path.join(upload_dir, courier.insurance_doc) if courier.insurance_doc else ""
        lic_res = verify_document_with_ia('driver_license', lic_file)
        ins_res = verify_document_with_ia('vehicle_insurance', ins_file)
        
    if id_res["status"] == "valid" and lic_res["status"] == "valid" and ins_res["status"] == "valid":
        courier.status = "approved"
        session.pop('ia_rejection_reason', None)
    else:
        courier.status = "rejected"
        reasons = []
        if id_res["status"] != "valid":
            reasons.append(id_res["reason"])
        if is_motorized and lic_res["status"] != "valid":
            reasons.append(lic_res["reason"])
        if is_motorized and ins_res["status"] != "valid":
            reasons.append(ins_res["reason"])
        session['ia_rejection_reason'] = " | ".join(reasons)
        
    courier_repo.update(courier)
    flash("Ficheiro atualizado e analisado por IA com sucesso.", "success")
    return redirect(url_for("apps_view_blueprint.courier_app_profile"))

@apps_view_blueprint.route("/uploads/<path:filename>", methods=["GET"])
def serve_upload(filename):
    upload_dir = current_app.config.get('APP_ENTREGADOR_UPLOADS')
    if not upload_dir:
        upload_dir = os.path.join(current_app.root_path, "uploads")
    return send_from_directory(upload_dir, filename)

@apps_view_blueprint.route("/courier/logout", methods=["GET"])
def courier_logout():
    session.clear()
    return redirect(url_for("apps_view_blueprint.courier_login"))


# =========================================================================
# 🍳 PORTAL DO RESTAURANTE (RESTAURANT APP)
# =========================================================================

@apps_view_blueprint.route("/restaurant", methods=["GET"])
@restaurant_login_required
def restaurant_app_home():
    """Portal principal del restaurante"""
    restaurant_id = session.get("restaurant_id")
    return redirect(url_for("apps_view_blueprint.restaurant_app_dashboard", restaurant_id=restaurant_id))

@apps_view_blueprint.route("/restaurant/dashboard/<int:restaurant_id>", methods=["GET"])
@restaurant_login_required
def restaurant_app_dashboard(restaurant_id):
    # Security block: Only allow restaurants to view their OWN dashboard
    if session.get("restaurant_id") != restaurant_id:
        return redirect(url_for("apps_view_blueprint.restaurant_app_dashboard", restaurant_id=session.get("restaurant_id")))
    return render_template("app_restaurant/dashboard.html", restaurant_id=restaurant_id)

@apps_view_blueprint.route("/restaurant/login", methods=["GET", "POST"])
def restaurant_login():
    if session.get("restaurant_id") and session.get("role") == "restaurant":
        return redirect(url_for("apps_view_blueprint.restaurant_app_home"))
        
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        restaurant_repo = current_app.extensions["repositories"]["restaurant"]
        restaurant = restaurant_repo.get_by_email(email)
        if restaurant and check_password_hash(restaurant.password_hash, password):
            session.clear()
            session["restaurant_id"] = restaurant.id
            session["role"] = "restaurant"
            session["name"] = restaurant.name
            return redirect(url_for("apps_view_blueprint.restaurant_app_home"))
        error = "Email ou senha incorretos."
        
    return render_template("app_restaurant/login.html", error=error)

@apps_view_blueprint.route("/restaurant/register", methods=["GET", "POST"])
def restaurant_register():
    if session.get("restaurant_id") and session.get("role") == "restaurant":
        return redirect(url_for("apps_view_blueprint.restaurant_app_home"))
        
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        owner = request.form.get("owner", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        phone_prefix = request.form.get("phone_prefix", "").strip()
        phone = request.form.get("phone", "").strip()
        full_phone = f"{phone_prefix} {phone}".strip()
        nif = request.form.get("nif", "").strip()
        address = request.form.get("address", "").strip()
        region = request.form.get("region", "Porto").strip()
        
        restaurant_repo = current_app.extensions["repositories"]["restaurant"]
        
        nif_ok, nif_msg = verify_nif_portal_financas(nif)
        
        if _is_email_registered(email):
            error = "Este e-mail já está registado na plataforma."
        elif _is_nif_registered(nif):
            error = "Este NIF já está registado na plataforma."
        elif not nif_ok:
            error = f"Erro de NIF: {nif_msg}"
        else:
            hashed_pwd = generate_password_hash(password)
            from delivery_app.entities.restaurant import Restaurant
            new_rest = Restaurant(
                id=None,
                name=name,
                owner_name=owner,
                nif=nif,
                phone=full_phone,
                whatsapp=full_phone,
                email=email.lower(),
                password_hash=hashed_pwd,
                address=address,
                map_link="",
                logo_url="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=150&q=80",
                banner_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
                region=region
            )
            restaurant_repo.add(new_rest)
            session.clear()
            session["restaurant_id"] = new_rest.id
            session["role"] = "restaurant"
            session["name"] = new_rest.name
            
            return redirect(url_for("apps_view_blueprint.restaurant_app_home"))
            
    return render_template("app_restaurant/register.html", error=error)

@apps_view_blueprint.route("/restaurant/logout", methods=["GET"])
def restaurant_logout():
    session.clear()
    return redirect(url_for("apps_view_blueprint.restaurant_login"))


# =========================================================================
# ⚙️ DEV PORTAL
# =========================================================================

@apps_view_blueprint.route("/dev-portal", methods=["GET", "POST"])
def developer_portal():
    admin_password = current_app.config.get("APP_ADMIN_PASSWORD", "adminpass")
    
    error = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "login":
            password = request.form.get("password")
            if password == admin_password:
                session["dev_authorized"] = True
                return redirect(url_for("apps_view_blueprint.developer_portal"))
            else:
                error = "Clave de acceso incorrecta. Inténtalo de nuevo."
        elif action == "logout":
            session.pop("dev_authorized", None)
            return redirect(url_for("apps_view_blueprint.developer_portal"))
            
    is_authorized = session.get("dev_authorized", False)
    return render_template("dev_portal.html", is_authorized=is_authorized, error=error)

@apps_view_blueprint.route("/admin/couriers", methods=["GET", "POST"])
def admin_couriers():
    admin_password = current_app.config.get("APP_ADMIN_PASSWORD", "adminpass")
    courier_repo = current_app.extensions["repositories"]["courier"]
    
    error = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "login":
            password = request.form.get("password")
            if password == admin_password:
                session["admin_authorized"] = True
                return redirect(url_for("apps_view_blueprint.admin_couriers"))
            else:
                error = "Palavra-passe de administração incorreta."
        elif action == "logout":
            session.pop("admin_authorized", None)
            return redirect(url_for("apps_view_blueprint.admin_couriers"))
        elif action == "update_status":
            if not session.get("admin_authorized"):
                abort(403)
            courier_id = int(request.form.get("courier_id"))
            new_status = request.form.get("status")
            new_balance = float(request.form.get("balance", 0.0))
            new_vehicle = request.form.get("vehicle")
            new_plate = request.form.get("vehicle_plate", "")
            
            c = courier_repo.get_by_id(courier_id)
            c.status = new_status
            c.balance = new_balance
            c.vehicle = new_vehicle
            c.vehicle_plate = new_plate
            courier_repo.update(c)
            flash(f"Perfil de {c.name} atualizado com sucesso.", "success")
            return redirect(url_for("apps_view_blueprint.admin_couriers"))
            
    is_authorized = session.get("admin_authorized", False)
    couriers = []
    if is_authorized:
        couriers = courier_repo.list_all()
        
    return render_template("admin_couriers.html", is_authorized=is_authorized, couriers=couriers, error=error)
