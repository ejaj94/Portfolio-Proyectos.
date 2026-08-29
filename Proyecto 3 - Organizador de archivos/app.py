import os
from flask import Flask, render_template, request, jsonify
from organizador import FileOrganizer

app = Flask(__name__)
organizer = FileOrganizer()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/system-folders", methods=["GET"])
def get_system_folders():
    user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    folders = {
        "Descargas": os.path.join(user_profile, "Downloads"),
        "Documentos": os.path.join(user_profile, "Documents"),
        "Escritorio": os.path.join(user_profile, "Desktop"),
        "Imágenes": os.path.join(user_profile, "Pictures"),
        "Vídeos": os.path.join(user_profile, "Videos"),
        "Música": os.path.join(user_profile, "Music")
    }

    # Filtrar solo carpetas existentes
    valid_folders = {k: v for k, v in folders.items() if os.path.exists(v)}
    return jsonify({"success": True, "folders": valid_folders, "user_home": user_profile})


@app.route("/api/scan", methods=["POST"])
def scan_directory():
    data = request.get_json() or {}
    folder_path = data.get("folder_path", "").strip()
    mode = data.get("mode", "category")

    if not folder_path:
        return jsonify({"success": False, "message": "Debes especificar una ruta de carpeta."}), 400

    try:
        res = organizer.scan(folder_path, modo=mode)
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/organize", methods=["POST"])
def organize_directory():
    data = request.get_json() or {}
    folder_path = data.get("folder_path", "").strip()
    mode = data.get("mode", "category")
    dry_run = data.get("dry_run", False)

    if not folder_path:
        return jsonify({"success": False, "message": "Debes especificar una ruta de carpeta."}), 400

    try:
        res = organizer.organize(folder_path, modo=mode, dry_run=dry_run)
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/undo", methods=["POST"])
def undo_last_operation():
    data = request.get_json() or {}
    folder_path = data.get("folder_path", "").strip()

    if not folder_path:
        return jsonify({"success": False, "message": "Debes especificar una ruta de carpeta."}), 400

    try:
        res = organizer.undo_last(folder_path)
        return jsonify(res)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/duplicates", methods=["POST"])
def scan_duplicates():
    data = request.get_json() or {}
    folder_path = data.get("folder_path", "").strip()

    if not folder_path:
        return jsonify({"success": False, "message": "Debes especificar una ruta de carpeta."}), 400

    try:
        res = organizer.find_duplicates(folder_path)
        return jsonify({"success": True, "data": res})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


if __name__ == "__main__":
    print("🚀 Iniciando Organizador de Archivos Web en http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
