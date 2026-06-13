import os
import sys
from flask import Flask
import stripe

# Forzar a Python a reconocer la raíz para evitar errores de importación
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from delivery_app.config import create_app
import list_routes

# Importamos las extensiones compartidas y las APIs
from delivery_app.extensions import socketio
from delivery_app.api.client_api import client_api_blueprint
from delivery_app.api.restaurant_api import restaurant_api_blueprint
from delivery_app.api.courier_api import courier_api_blueprint

# Controlador de las pantallas de las Apps independientes
from delivery_app.controllers.apps_view_controller import apps_view_blueprint

# Configuración de Stripe desde variables de entorno
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "stripe_mock_test_key_not_secret")

# Inicialización de la aplicación unificada con base de datos dinámica en producción
db_path = os.getenv("DATABASE_PATH", "delivery_app.db")
app = create_app(database_path=db_path)

# Vinculamos e inicializamos SocketIO con nuestra aplicación de Flask
socketio.init_app(app)

# Registro de los Blueprints de la API en el servidor central
app.register_blueprint(client_api_blueprint)
app.register_blueprint(restaurant_api_blueprint)
app.register_blueprint(courier_api_blueprint)

# REGISTRO DE LAS VISTAS DE LAS APPS
app.register_blueprint(apps_view_blueprint)

# Registro del comando CLI 'flask routes'
list_routes.register_commands(app)

if __name__ == "__main__":
    # 🌟 CORREGIDO: use_reloader=False evita la duplicación de hilos que bloquea WebSockets localmente
    socketio.run(app, debug=True, port=5001, use_reloader=False)
