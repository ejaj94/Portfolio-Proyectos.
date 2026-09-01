import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

CAR_INQUIRIES_DB = []


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/inquiry-car", methods=["POST"])
def inquiry_car():
    try:
        data = request.get_json() or {}
        full_name = data.get("full_name", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip()
        car_model = data.get("car_model", "Consulta Geral Stand Veloce").strip()
        inquiry_type = data.get("inquiry_type", "Compra Direta").strip()
        has_trade_in = data.get("has_trade_in", "Não").strip()
        notes = data.get("notes", "").strip()

        if not full_name or not phone or not email:
            return jsonify({
                "success": False,
                "message": "Por favor, preencha o seu nome, telemóvel e e-mail."
            }), 400

        inquiry_id = f"VELOCE-{len(CAR_INQUIRIES_DB) + 5001}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        new_inquiry = {
            "id": inquiry_id,
            "full_name": full_name,
            "phone": phone,
            "email": email,
            "car_model": car_model,
            "inquiry_type": inquiry_type,
            "has_trade_in": has_trade_in,
            "notes": notes,
            "status": "Reserva VIP / Proposta Solicitada",
            "created_at": created_at
        }

        CAR_INQUIRIES_DB.append(new_inquiry)
        print(f"[+] Nova Solicitação Veloce Luxury Motors: {inquiry_id} | {full_name} | Viatura: {car_model}")

        wa_text = f"🏎️ *SOLICITAÇÃO VIP — VELOCE LUXURY MOTORS* 🏁\n\n" \
                  f"📌 *Código*: {inquiry_id}\n" \
                  f"👤 *Cliente*: {full_name}\n" \
                  f"📞 *Telemóvel*: {phone}\n" \
                  f"✉️ *Email*: {email}\n" \
                  f"🚗 *Viatura*: {car_model}\n" \
                  f"🎯 *Interesse*: {inquiry_type}\n" \
                  f"🔄 *Retoma*: {has_trade_in}\n" \
                  f"📝 *Obs*: {notes if notes else 'Sem observações adicionais'}"

        return jsonify({
            "success": True,
            "message": "Solicitação VIP enviada com sucesso! O nosso consultor entrará em contacto.",
            "inquiry": new_inquiry,
            "whatsapp_url": f"https://wa.me/351123456789?text={request.headers.get('Origin', '') and wa_text}"
        })

    except Exception as e:
        print(f"[!] Erro na consulta Veloce: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando VELOCE LUXURY MOTORS Stand em http://localhost:5090")
    app.run(host="0.0.0.0", port=5090, debug=False)
