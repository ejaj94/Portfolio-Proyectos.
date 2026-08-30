import os
import sys
import threading
import webbrowser
from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime

from database import SessionLocal, Base, engine, get_db_type
from models import User
from services import UserActionService

# Inicializar tablas en la BD activa
Base.metadata.create_all(bind=engine)

app = Flask(__name__, template_folder="templates")

# Helper para obtener sesión limpia
def get_service():
    db = SessionLocal()
    return UserActionService(db), db

# ==========================================
# RUTAS DE INTERFAZ Y RECURSOS
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats", methods=["GET"])
def get_stats():
    service, db = get_service()
    try:
        stats = service.get_stats()
        stats["db_type"] = get_db_type()
        return jsonify(stats)
    finally:
        db.close()

@app.route("/api/users", methods=["GET"])
def get_users():
    service, db = get_service()
    try:
        query = request.args.get("q", "").strip()
        if query:
            users = service.search_users(query)
        else:
            users = service.repo.get_all()
        
        result = []
        for u in users:
            fecha_str = u.created_at.strftime("%d/%m/%Y %H:%M") if u.created_at else None
            result.append({
                "id": u.id,
                "name": u.name,
                "last_name": u.last_name,
                "age": u.age,
                "created_at": fecha_str
            })
        return jsonify(result)
    finally:
        db.close()

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    last_name = data.get("last_name")
    age = data.get("age")

    if not name or not last_name or age is None:
        return jsonify({"error": "Campos incompletos"}), 400

    service, db = get_service()
    try:
        res = service.ejecutar_y_notificar("add", send_email=False, name=name, last_name=last_name, age=int(age))
        if res:
            return jsonify({"message": "Usuario creado", "id": res.id}), 201
        return jsonify({"error": "No se pudo crear"}), 400
    finally:
        db.close()

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json() or {}
    name = data.get("name")
    last_name = data.get("last_name")
    age = data.get("age")

    service, db = get_service()
    try:
        res = service.ejecutar_y_notificar("update", send_email=False, id=user_id, name=name, last_name=last_name, age=age)
        if res:
            return jsonify({"message": "Usuario actualizado", "id": res.id}), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    finally:
        db.close()

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    service, db = get_service()
    try:
        res = service.ejecutar_y_notificar("delete", send_email=False, id=user_id)
        if res:
            return jsonify({"message": "Usuario eliminado"}), 200
        return jsonify({"error": "No se pudo eliminar"}), 404
    finally:
        db.close()

@app.route("/download-pdf", methods=["GET"])
def download_pdf():
    service, db = get_service()
    try:
        pdf_path = service.generar_pdf_manual()
        filename = os.path.basename(pdf_path)
        return send_file(pdf_path, as_attachment=True, download_name=filename)
    finally:
        db.close()

@app.route("/api/send-email", methods=["POST"])
def send_email():
    service, db = get_service()
    try:
        exito, pdf_path = service.enviar_email_manual()
        return jsonify({"success": exito, "pdf": os.path.basename(pdf_path)})
    finally:
        db.close()

def main():
    port = 5000
    url = f"http://localhost:{port}"
    print(f"[OK] Iniciando Servidor Web Gestor Pro DB en {url}")
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()

