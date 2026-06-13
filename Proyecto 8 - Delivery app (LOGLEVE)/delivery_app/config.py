import os
import flask
from flask import Flask, render_template, request
from flask_babel import Babel

from delivery_app.controllers.client_controller import client_blueprint
from delivery_app.controllers.courier_controller import courier_blueprint
from delivery_app.controllers.order_controller import order_blueprint
from delivery_app.controllers.restaurant_controller import restaurant_blueprint
from delivery_app.infrastructure.database import Database
from delivery_app.repositories.sqlite_repository import (
    SqliteClientRepository,
    SqliteCourierRepository,
    SqliteOrderRepository,
    SqliteRestaurantRepository,
    SqlitePlateRepository,
)

def create_app(database_path: str = "delivery_app.db") -> flask.Flask:
    app = flask.Flask(__name__)
    
    # Solución definitiva al RuntimeError de la sesión
    app.secret_key = os.environ.get('APP_SECRET_KEY', 'dev-secret-key-change-me')
    
    # Configuraciones de la aplicación
    app.config.setdefault('APP_ADMIN_PASSWORD', os.environ.get('APP_ADMIN_PASSWORD', 'adminpass'))
    app.config["DATABASE_PATH"] = database_path
    app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es', 'pt', 'fr', 'de', 'zh', 'hi', 'ar', 'ru', 'ja', 'it', 'nl', 'ko', 'tr', 'vi', 'pl', 'uk', 'ro', 'bn', 'ur', 'id', 'te', 'ta', 'sv', 'no', 'da', 'fi', 'el', 'th', 'he']

    # Localizador de idioma dinámico para Babel
    def get_locale():
        lang = request.args.get('lang')
        if lang and lang in app.config['BABEL_SUPPORTED_LOCALES']:
            return lang
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or 'pt'

    babel = Babel(app)
    babel.init_app(app, locale_selector=get_locale)

    # Base de datos y repositorios
    database = Database(database_path)
    restaurant_repository = SqliteRestaurantRepository(database)
    client_repository = SqliteClientRepository(database)
    courier_repository = SqliteCourierRepository(database)
    order_repository = SqliteOrderRepository(database)
    plate_repository = SqlitePlateRepository(database)

    # Inyección de dependencias en las extensiones de Flask
    app.extensions["repositories"] = {
        "restaurant": restaurant_repository,
        "client": client_repository,
        "courier": courier_repository,
        "order": order_repository,
        "plate": plate_repository,
    }

    # Registro de Blueprints de la app principal (Legacy debug views disabled for security)
    # app.register_blueprint(restaurant_blueprint)
    # app.register_blueprint(client_blueprint)
    # app.register_blueprint(courier_blueprint)
    # app.register_blueprint(order_blueprint)

    # Integración de app_entregador sub-app desactivada por seguridad
    pass

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/support")
    def support():
        return render_template("support.html")

    @app.route("/admin/couriers")
    def admin_couriers_redirect():
        return flask.redirect("/apps/admin/couriers")

    @app.route("/favicon.ico")
    def favicon():
        return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                         'favicon.png', mimetype='image/png')

    return app
