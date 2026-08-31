import os
import sys
import json
import base64
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, url_for
from services.cv_service import CVGenerationService

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cv_service = CVGenerationService()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate-pdf", methods=["POST", "GET"])
def generate_pdf():
    try:
        req_data = {}
        if request.is_json:
            req_data = request.get_json() or {}
        elif request.form.get("payload"):
            try:
                req_data = json.loads(request.form.get("payload"))
            except Exception:
                req_data = {}
        else:
            req_data = {
                "personal": {
                    "name": request.form.get("name") or request.args.get("name") or "Enmanuel Jimenez",
                    "title": request.form.get("title") or request.args.get("title") or "Engenheiro de Software",
                    "email": request.form.get("email") or request.args.get("email") or "enmanuel.jimenez@exemplo.pt",
                    "phone": request.form.get("phone") or request.args.get("phone") or "+351 912 345 678",
                    "location": request.form.get("location") or request.args.get("location") or "Lisboa, Portugal",
                    "website": request.form.get("website") or request.args.get("website") or "linkedin.com/in/enmanueljimenez",
                    "summary": request.form.get("summary") or request.args.get("summary") or "Resumo profissional..."
                },
                "skills": ["Python", "Flask", "JavaScript", "HTML5/CSS3", "Git"],
                "languages": ["Português (Nativo)", "Inglês (Avançado)"]
            }

        photo_b64 = req_data.get("photo_b64", "")
        photo_path = None
        if photo_b64 and "," in photo_b64:
            try:
                header, data_str = photo_b64.split(",", 1)
                img_bytes = base64.b64decode(data_str)
                temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                temp_img.write(img_bytes)
                temp_img.close()
                photo_path = temp_img.name
            except Exception as e:
                print(f"[!] Erro foto: {e}")

        output_dir = os.path.join(app.root_path, "output_pdf")
        os.makedirs(output_dir, exist_ok=True)

        result = cv_service.generate(
            data=req_data,
            photo_path=photo_path,
            output_dir=output_dir
        )

        if result.success and os.path.exists(result.output_path):
            filename = os.path.basename(result.output_path)
            return send_file(
                result.output_path,
                as_attachment=True,
                download_name=filename,
                mimetype="application/pdf"
            )
        else:
            return jsonify({"success": False, "message": result.message}), 400

    except Exception as e:
        print(f"[!] Erro inesperado ao gerar PDF: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando CV Studio Builder PRO Web App em http://localhost:5009")
    app.run(host="0.0.0.0", port=5009, debug=False)
