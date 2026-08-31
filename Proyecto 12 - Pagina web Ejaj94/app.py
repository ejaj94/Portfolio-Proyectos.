import os
import sys
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__, static_folder='.', template_folder='.')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return send_from_directory('.', 'index.html')


@app.route("/<path:path>")
def static_proxy(path):
    if os.path.exists(os.path.join('.', path)):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')


@app.route("/api/contact", methods=["POST"])
def contact_api():
    try:
        data = request.get_json() or {}
        name = data.get("name", "Anónimo")
        email = data.get("email", "")
        message = data.get("message", "")
        print(f"[+] Mensagem recebida de {name} ({email}): {message}")
        return jsonify({
            "success": True,
            "message": "Mensagem recebida com sucesso! Responderemos em breve."
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando Plataforma Oficial Ejaj94 / EJAJ TECH em http://localhost:5012")
    app.run(host="0.0.0.0", port=5012, debug=False)
