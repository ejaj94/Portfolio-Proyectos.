import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

VIP_INQUIRIES_DB = []


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/contact-vip", methods=["POST"])
def contact_vip():
    try:
        data = request.get_json() or {}
        full_name = data.get("full_name", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip()
        property_title = data.get("property_title", "Consulta Geral Vale do Lobo").strip()
        preferred_date = data.get("preferred_date", "").strip()
        notes = data.get("notes", "").strip()

        if not full_name or not phone or not email:
            return jsonify({
                "success": False,
                "message": "Por favor, preencha o seu nome completo, telemóvel e e-mail."
            }), 400

        inquiry_id = f"VL-{len(VIP_INQUIRIES_DB) + 1001}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        new_inquiry = {
            "id": inquiry_id,
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "property_title": property_title,
            "preferred_date": preferred_date if preferred_date else "A agendar",
            "notes": notes,
            "status": "Dossier Solicitado / Visita Privada",
            "created_at": created_at
        }

        VIP_INQUIRIES_DB.append(new_inquiry)
        print(f"[+] Nova Consulta VIP Inmobiliária: {inquiry_id} | {full_name} | Propriedade: {property_title}")

        wa_text = f"🏰 *SOLICITAÇÃO DOSSIER PRIVADO — VALE DO LOBO LUXURY* ✨\n\n" \
                  f"📌 *Código*: {inquiry_id}\n" \
                  f"👤 *Cliente*: {full_name}\n" \
                  f"📞 *Telemóvel*: {phone}\n" \
                  f"✉️ *Email*: {email}\n" \
                  f"🏛️ *Propriedade de Interesse*: {property_title}\n" \
                  f"📅 *Data Preferencial Visita*: {preferred_date if preferred_date else 'A definir'}\n" \
                  f"📝 *Obs*: {notes if notes else 'Sem requisitos adicionais'}"

        return jsonify({
            "success": True,
            "message": "Solicitação enviada com sucesso! O nosso consultor privado entrará em contacto.",
            "inquiry": new_inquiry,
            "whatsapp_url": f"https://wa.me/351123456789?text={request.headers.get('Origin', '') and wa_text}"
        })

    except Exception as e:
        print(f"[!] Erro na consulta VIP: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando VALE DO LOBO LUXURY REAL ESTATE em http://localhost:5080")
    app.run(host="0.0.0.0", port=5080, debug=False)
